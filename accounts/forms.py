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


class AddProfileRefereeForm(ModelForm):
    name = CharField(max_length=16, label='First name')
    surname = CharField(max_length=16, label='Last name')
    email = EmailField(label='E-mail')


    class Meta:
        model = Referee
        fields = ['name', 'surname', 'licence_number', 'licence_type', 'email', 'city', 'rating', 'phone']

    def clean_name(self):
        initial = self.cleaned_data.get('name')
        if initial:
            return initial.strip().capitalize()
        return initial

    def clean_surname(self):
        initial = self.cleaned_data.get('surname')
        if initial:
            return initial.strip().capitalize()
        return initial

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            try:
                forms.EmailField().clean(email)
            except ValidationError:
                raise ValidationError('Invalid e-mail format.')
        return email

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating is not None:
            if rating < 0.0 or rating > 100.0:
                raise ValidationError('Rating must be between 0 and 100.')
            if round(rating, 1) != rating:
                raise ValidationError('Rating can have at most one decimal place.')
        return rating

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name', '').strip()
        surname = cleaned_data.get('surname', '').strip()

        if not name or not surname:
            raise ValidationError('The name and surname fields are required.')

        cleaned_data['name'] = name
        cleaned_data['surname'] = surname
        return cleaned_data

    @atomic
    def save(self, commit=True):
        name = self.cleaned_data.get('name')
        surname = self.cleaned_data.get('surname')
        email = self.cleaned_data.get('email')

        def generate_unique_username(name, surname):
            base_username = f"{name}.{surname}".lower()
            username = base_username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1
            return username

        # 2. Generování unikátního uživatelského jména
        username = generate_unique_username(name, surname)
        initial_password = "Admin1234"


        referee = super().save(commit=False)
        user = User(
            username=username,
            password=initial_password,
            first_name=name,
            last_name=surname,
            email=email,
        )
        profile_referee = ProfileReferee(user=user, referee=referee)

        if commit:
            referee.save()
            user.save()
            profile_referee.save()

        return referee


@login_required
def user_logout(request):
    logout(request)
    #return render(request, 'home.html')
    return redirect(request.META.get('HTTP_REFERER', '/'))

