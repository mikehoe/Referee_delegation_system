import unicodedata
from django import forms
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.transaction import atomic
from django.forms import ModelForm, CharField, EmailField
from django.shortcuts import redirect

from referees.models import Referee
from accounts.models import ProfileReferee


def remove_diacritics(input_str):
    # Normalize the string to NFD (Normalization Form Decomposition),
    # which decomposes accented characters into the base character and diacritics as separate components.
    normalized_str = unicodedata.normalize('NFD', input_str)

    # Filtering characters that are not combining characters (i.e. diacritics)
    filtered_str = ''.join([char for char in normalized_str if not unicodedata.combining(char)])
    return filtered_str


def generate_unique_username_and_password(first_name, last_name, number):
    base_username = remove_diacritics(f"{first_name}.{last_name}".lower())
    username = base_username
    counter = 1
    while User.objects.filter(username=username).exists():
        username = f"{base_username}{counter}"
        counter += 1
    return username, f"{username}{number}"


class AddProfileRefereeForm(ModelForm):
    first_name = CharField(max_length=150, required=True)
    last_name = CharField(max_length=150, required=True)
    email = EmailField(required=True)

    class Meta:
        model = Referee
        fields = ['first_name', 'last_name', 'licence_number', 'licence_type', 'email', 'city', 'rating', 'phone']

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if first_name:
            first_name = ' '.join([n.capitalize() for n in first_name.strip().split()])  # Capitalize also middle names
            print(first_name)
            return first_name
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if last_name:
            return last_name.strip().capitalize()
        return last_name

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating is not None:
            if rating < 0.0 or rating > 100.0:
                raise ValidationError('The Rating must be between 0 and 100.')
            if round(rating, 1) != rating:
                raise ValidationError('The Rating must have at most one decimal place.')
        return rating

    @atomic
    def save(self, commit=True):
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data.get('last_name')
        email = self.cleaned_data.get('email')
        licence_number = self.cleaned_data.get('licence_number')

        username, raw_password = generate_unique_username_and_password(first_name, last_name, licence_number)

        user = User(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email
        )
        referee = super().save(commit=False)
        profile_referee = ProfileReferee(user=user, referee=referee)

        if commit:
            user.set_password(raw_password)
            user.save()
            referee.save()
            profile_referee.save()

        return profile_referee


@login_required
def user_logout(request):
    logout(request)
    # return render(request, 'home.html')
    return redirect(request.META.get('HTTP_REFERER', '/'))
