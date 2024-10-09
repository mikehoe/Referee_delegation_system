from django.core.exceptions import ValidationError
from django.forms import ModelForm, DateTimeField, NumberInput, DateInput

from competitions.models import City, Match, Team, Season


class CityModelForm(ModelForm):
    class Meta:
        model = City
        fields = ['name']

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if name:
            name = name.strip().capitalize()
            return name
        else:
            raise ValidationError("City name cannot be empty.")


class MatchModelForm(ModelForm):

    date_time = DateTimeField(required=False, widget=NumberInput(attrs={'type': 'datetime-local'}))

    class Meta:
        model = Match
        fields = ['competition_in_season', 'code', 'city', 'date_time', 'home_team', 'away_team']

    def clean_teams(self):
        cleaned_data = super().clean()
        home_team = cleaned_data.get("home_team")
        away_team = cleaned_data.get("away_team")

        if home_team == away_team:
            raise ValidationError("Home team and Away team must be different.")

        return cleaned_data

    def clean_code(self):
        code = self.cleaned_data.get("code")
        if code:
            code = code.strip()
            code = ''.join(code.split())  # Deletes all the spaces
        return code


class TeamModelForm(ModelForm):
    class Meta:
        model = Team
        fields = '__all__'

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if name:
            name = name.strip().title() # capitalizes every word
        return name

    def clean_contact_person(self):
        contact_person = self.cleaned_data.get("contact_person")
        if contact_person:
            contact_person = contact_person.strip().capitalize()
        return contact_person


class SeasonModelForm(ModelForm):
    class Meta:
        model = Season
        fields = ['name', 'date_of_start', 'date_of_end']
        widgets = {
            'date_of_start': DateInput(attrs={'type': 'date'}),
            'date_of_end': DateInput(attrs={'type': 'date'}),
        }

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if name:
            name = name.strip()
            # Control of format - 2 numbers divided by '/'
            if not all(part.isdigit() for part in name.split('/')) or name.count('/') != 1:
                raise ValidationError("Season name must be in the format 'YYYY/YYYY' with numbers only.")
            cleaned_name = name
            return cleaned_name
        raise ValidationError("Season name cannot be empty.")

    def clean(self):
        cleaned_data = super().clean()
        date_of_start = cleaned_data.get("date_of_start")
        date_of_end = cleaned_data.get("date_of_end")
        if date_of_start and date_of_end and date_of_start > date_of_end:
            raise ValidationError("Start date cannot be after end date.")
        return cleaned_data

