from django.core.exceptions import ValidationError
from django.forms import ModelForm

from referees.models import Referee


class RefereeForm(ModelForm):
    class Meta:
        model = Referee
        fields = '__all__'

    def clean_name(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        if name is None or len(name.strip()) == 0:
            raise ValidationError('Please enter a name.')
        return name.strip().capitalize()

    def clean_surname(self):
        cleaned_data = super().clean()
        surname = cleaned_data.get('surname')
        if surname is None or len(surname.strip()) == 0:
            raise ValidationError('Please enter a surname.')
        return surname.strip().capitalize()

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name', '').strip()
        surname = cleaned_data.get('surname', '').strip()

        if len(name) == 0 and len(surname) == 0:
            raise ValidationError('You must enter either a name or a surname.')

        cleaned_data['name'] = name
        cleaned_data['surname'] = surname
        return cleaned_data