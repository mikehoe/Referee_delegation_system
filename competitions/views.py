from django.db.models import Count
from django.views.generic import ListView, DetailView

from competitions.models import Match, CompetitionInSeason, Team, City


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

        # Získání pouze těch měst, ve kterých existují týmy
        context['cities'] = City.objects.annotate(num_teams=Count('teams')).filter(num_teams__gt=0)
        context['competitions_in_seasons'] = CompetitionInSeason.objects.all()

        context['selected_city_id'] = self.request.GET.get('city', None)
        context['selected_competition_id'] = self.request.GET.get('competition', None)

        selected_city_id = context['selected_city_id']
        selected_competition_id = context['selected_competition_id']

        teams = Team.objects.all().distinct()

        if selected_city_id:
            teams = teams.filter(city_id=selected_city_id)
            context['selected_city'] = City.objects.get(id=selected_city_id)

        if selected_competition_id:
            teams = teams.filter(competition_in_season_id=selected_competition_id)
            context['selected_competition'] = CompetitionInSeason.objects.get(id=selected_competition_id)

        teams = teams.distinct().order_by('name')

        context['teams_list'] = teams
        return context

# TODO: potřebuji, aby se každý tým zobrazil jednou
# TODO: chci, aby se při nulování jednoho filtru nevynuloval druhý (competitions x cities)

class TeamDetailView(DetailView):
    model = Team
    template_name = "team_detail.html"
    context_object_name = 'team'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team = self.get_object()
        context['cities'] = City.objects.all()
        return context