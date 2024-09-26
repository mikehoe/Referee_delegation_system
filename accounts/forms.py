from django import forms
from django.contrib.auth.models import User
from django.db.transaction import atomic
from django.forms import ModelForm

from referees.models import Referee
from accounts.models import ProfileReferee


class AddProfileRefereeForm(ModelForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    name = forms.CharField(max_length=30)
    surname = forms.CharField(max_length=30)

    class Meta:
        model = Referee
        fields = ['licence_number', 'licence_type', 'city', 'rating', 'phone']

    @atomic
    def save(self, commit=True):
        referee = super().save(commit=False)

        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
            first_name=self.cleaned_data['name'],
            last_name=self.cleaned_data['surname']
        )

        if commit:
            user.save()
            referee.save()

            ProfileReferee.objects.create(user=user, referee=referee)

        return referee


class EditProfileRefereeForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    name = forms.CharField(max_length=30)
    surname = forms.CharField(max_length=30)

    class Meta:
        model = Referee
        fields = ['licence_number', 'licence_type', 'city', 'rating', 'phone']

    def save(self, commit=True):
        referee = super().save(commit=False)
        user = self.instance.profile_referee.user

        user.username = self.cleaned_data['username']
        user.first_name = self.cleaned_data['name']
        user.last_name = self.cleaned_data['surname']

        if commit:
            user.save()
            referee.save()

        return referee