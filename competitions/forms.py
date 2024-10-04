from django.forms import ModelForm

from competitions.models import City, Match, Team


class CityModelForm(ModelForm):
    class Meta:
        model = City
        fields = '__all__'


class MatchModelForm(ModelForm):
    class Meta:
        model = Match
        fields = ['competition_in_season', 'city', 'date_time', 'home_team', 'away_team']


class TeamModelForm(ModelForm):
    class Meta:
        model = Team
        fields = '__all__'