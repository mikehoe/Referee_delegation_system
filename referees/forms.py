from django.core.exceptions import ValidationError
from django.forms import ModelForm

from referees.models import Unavailability


class UnavailabilityForm(ModelForm):
    class Meta:
        model = Unavailability
        fields = ['date_from', 'date_to']

    def clean(self):
        cleaned_data = super().clean()
        date_from = cleaned_data.get('date_from')
        date_to = cleaned_data.get('date_to')

        if date_from and date_to and date_from > date_to:
            raise ValidationError("Date 'from' must be before date 'to'.")

        return cleaned_data