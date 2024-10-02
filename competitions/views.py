from datetime import datetime

from django.db.models import Count
from django.views.generic import ListView, DetailView

from competitions.models import Match, CompetitionInSeason, Team, City, Season
from competitions.view_home import get_current_season


class MatchesListView(ListView):
    model = Match
    template_name = 'matches_list.html'
    context_object_name = 'competition_matches'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        competition_in_season = CompetitionInSeason.objects.get(pk=self.kwargs['pk'])
        context['competition_in_season'] = competition_in_season
        return context

    def get_queryset(self):
        competition_in_season = CompetitionInSeason.objects.get(pk=self.kwargs['pk'])
        return Match.objects.filter(competition_in_season=competition_in_season)


class TeamsListView(ListView):
    model = Team
    template_name = "teams_list.html"
    context_object_name = 'teams_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Získání aktuální sezóny pomocí pomocné funkce
        selected_season_id = self.request.GET.get('season')
        current_season = get_current_season(selected_season_id)

        # Získání soutěží v aktuální sezóně
        competitions = CompetitionInSeason.objects.filter(season=current_season)

        # Pro každou soutěž v sezóně získáme týmy
        competitions_teams = []
        for competition_in_season in competitions:
            teams_in_competition = Team.objects.filter(
                competition_in_season=competition_in_season).order_by('name')
            competitions_teams.append((competition_in_season, teams_in_competition))

        # Přidání sezón a soutěží do kontextu
        context['seasons'] = Season.objects.all()
        context['competitions'] = competitions
        context['current_season'] = current_season
        context['competition_teams'] = competitions_teams

        return context

# TODO: chci, aby se při nulování jednoho filtru nevynuloval druhý (competitions x cities)

class TeamDetailView(DetailView):
    model = Team
    template_name = "team_detail.html"
    context_object_name = 'team'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cities'] = City.objects.all()
        return context