from django.forms import ModelForm, DateTimeField, NumberInput

from competitions.models import City, Match, Team


class CityModelForm(ModelForm):
    class Meta:
        model = City
        fields = '__all__'


class MatchModelForm(ModelForm):

    date_time = DateTimeField(required=False, widget=NumberInput(attrs={'type': 'datetime-local'}))

    class Meta:
        model = Match
        fields = ['competition_in_season', 'city', 'date_time', 'home_team', 'away_team']


class TeamModelForm(ModelForm):
    class Meta:
        model = Team
        fields = '__all__'