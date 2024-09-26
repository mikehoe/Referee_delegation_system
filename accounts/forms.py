from django.core.exceptions import ValidationError
from django.forms import ModelForm

from referees.models import Referee


class RefereeForm(ModelForm):
    class Meta:
        model = Referee
        fields = '__all__'

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if len(name) == 0:
            raise ValidationError('Please enter a name.')
        return name.capitalize()

    def clean_surname(self):
        surname = self.cleaned_data.get('surname', '').strip()
        if len(surname) == 0:
            raise ValidationError('Please enter a surname.')
        return surname.capitalize()