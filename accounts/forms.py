import unicodedata
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.db.transaction import atomic
from django.forms import ModelForm, CharField, EmailField
from django.forms.widgets import NumberInput
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from accounts.models import ProfileReferee, ProfileManager
from referees.models import Referee


def clean_first_name(self):
    first_name = self.cleaned_data.get('first_name')
    if first_name:
        first_name = ' '.join([n.capitalize() for n in first_name.strip().split()])  # Capitalize also middle names
        print(f"clean first name: {first_name}")
        return first_name
    return first_name


def clean_last_name(self):
    last_name = self.cleaned_data.get('last_name')
    if last_name:
        last_name = ' '.join([n.capitalize() for n in last_name.strip().split()])  # Capitalize all surnames
        print(f"clean last name: {last_name}")
        return last_name
    return last_name


def remove_diacritics(input_str):
    # Normalize the string to NFD (Normalization Form Decomposition),
    # which decomposes accented characters into the base character and diacritics as separate components.
    normalized_str = unicodedata.normalize('NFD', input_str)

    # Filtering characters that are not combining characters (i.e. diacritics)
    filtered_str = ''.join([char for char in normalized_str if not unicodedata.combining(char)])
    return filtered_str


def generate_unique_username_and_password(first_name, last_name, number):
    first_name = first_name.strip().split()[0]  # If there are more names, it takes first one.
    last_name = '-'.join(last_name.strip().split())  # If there are more surnames, is takes all
    base_username = remove_diacritics(f"{first_name}.{last_name}".lower())
    username = base_username
    counter = 2
    while User.objects.filter(username=username).exists():
        username = f"{base_username}{counter}"
        counter += 1
    password = f"{username}-{number}"
    print(f"username = {username}, password: {password}")
    return username, password


def send_welcome_email(user, raw_password):
    # Create reset URL using uidb64 and token
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    reset_url = reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
    full_reset_url = f"http://localhost:8000{reset_url}"

    # Message for user
    subject = f"{settings.EMAIL_SUBJECT_PREFIX}: Welcome {user.first_name}!"
    message = f"""
        Dear {user.first_name},

        your account has been created. Here are your login credentials:

        Username: {user.username}
        Password: {raw_password}

        You can reset your password using the following link:
        {full_reset_url}

        Best regards,
        The Referee Delegation System Team
        """

    send_mail(
        subject,
        message,
        'delegationsystem@seznam.cz',
        [user.email],
        fail_silently=False,
    )


class ProfileRefereeForm(ModelForm):
    first_name = CharField(max_length=150, required=True)
    last_name = CharField(max_length=150, required=True)
    email = EmailField(required=True)

    class Meta:
        model = Referee
        fields = ['first_name', 'last_name', 'licence_number', 'licence_type', 'email', 'city', 'rating', 'phone']
        widgets = {
            'licence_number': NumberInput(attrs={'min': 1}),
            'rating': NumberInput(attrs={'min': 0.1, 'max': 100, 'step': 0.1})
        }

    def clean_first_name(self):
        return clean_first_name(self)

    def clean_last_name(self):
        return clean_last_name(self)

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
            print(f"Add profile_referee: {profile_referee}")

            send_welcome_email(user, raw_password)
            print(f"Welcome email sent to user: {profile_referee}")

        return profile_referee

    @atomic
    def update(self, pk, commit=True):
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data.get('last_name')
        email = self.cleaned_data.get('email')

        referee = Referee.objects.get(pk=pk)
        profile_referee = ProfileReferee.objects.get(referee=referee)
        user = profile_referee.user

        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        referee = super().save(commit=False)

        if commit:
            user.save()
            referee.save()
            print(f"Update referee profile = {profile_referee}")

        return profile_referee


class ProfileLoggedRefereeForm(ProfileRefereeForm):
    class Meta:
        model = Referee
        fields = ['first_name', 'last_name', 'email', 'city', 'phone']


class ProfileManagerForm(ModelForm):
    first_name = CharField(max_length=150, required=True)
    last_name = CharField(max_length=150, required=True)
    email = EmailField(required=True)

    class Meta:
        model = ProfileManager
        fields = ['manager_type', 'first_name', 'last_name', 'email', 'phone']

    def clean_first_name(self):
        return clean_first_name(self)

    def clean_last_name(self):
        return clean_last_name(self)

    @atomic
    def save(self, commit=True):
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data.get('last_name')
        email = self.cleaned_data.get('email')

        username, raw_password = generate_unique_username_and_password(first_name, last_name, "1234")

        user = User(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email
        )
        profile_manager = super().save(commit=False)
        profile_manager.user = user

        if commit:
            user.set_password(raw_password)
            user.save()
            profile_manager.save()
            print(f"Add profile_manager: {profile_manager}")

            profile_manager.set_permissions()
            print(f"Set permissions: {profile_manager.manager_type}")

            send_welcome_email(user, raw_password)
            print(f"Welcome email sent to user: {profile_manager}")

        return profile_manager

    @atomic
    def update(self, pk, commit=True):

        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data.get('last_name')
        email = self.cleaned_data.get('email')

        profile_manager = ProfileManager.objects.get(pk=pk)
        user = profile_manager.user

        user.first_name = first_name
        user.last_name = last_name
        user.email = email

        profile_manager.unset_permissions()
        print(f"Unset permissions: {profile_manager.manager_type}")

        profile_manager = super().save(commit=False)

        profile_manager.set_permissions()
        print(f"Set permissions: {profile_manager.manager_type}")

        if commit:
            user.save()
            profile_manager.save()
            print(f"Update manager profile = {profile_manager}")

        return profile_manager


class ProfileLoggedManagerForm(ProfileManagerForm):
    class Meta:
        model = ProfileManager
        fields = ['first_name', 'last_name', 'email', 'phone']
