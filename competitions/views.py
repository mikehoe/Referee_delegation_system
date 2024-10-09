from logging import getLogger

from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from competitions.forms import CityModelForm, MatchModelForm, TeamModelForm
from competitions.models import Match, CompetitionInSeason, Team, City, Season
from competitions.view_home import get_current_season

LOGGER = getLogger()


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


class MatchAddView(CreateView):
    form_class = MatchModelForm
    template_name = "form.html"

    def get_success_url(self):
        # Gets correct URL with 'pk' of CompetitionInSeason from kwargs
        return reverse_lazy('matches_list', kwargs={'pk': self.kwargs['pk']})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Get the CompetitionInSeason instance based on pk in URL
        competition_in_season = CompetitionInSeason.objects.get(pk=self.kwargs['pk'])
        # Pass the CompetitionInSeason instance as the initial value for the form
        kwargs['initial']['competition_in_season'] = competition_in_season
        return kwargs

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        competition_in_season = CompetitionInSeason.objects.get(pk=self.kwargs['pk'])
        # Limits the choice of teams to home_team an away_team from the chosen competition_in_season
        form.fields['home_team'].queryset = Team.objects.filter(competition_in_season=competition_in_season)
        form.fields['away_team'].queryset = Team.objects.filter(competition_in_season=competition_in_season)
        return form

    def form_invalid(self, form):
        LOGGER.warning('User provided invalid data while adding a city.')
        return super().form_invalid(form)


class MatchUpdateView(UpdateView):
    model = Match
    form_class = MatchModelForm
    template_name = "form.html"

    def get_success_url(self):
        return reverse_lazy('matches_list', kwargs={'pk': self.object.competition_in_season.pk})

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        competition_in_season = self.object.competition_in_season
        form.fields['home_team'].queryset = Team.objects.filter(competition_in_season=competition_in_season)
        form.fields['away_team'].queryset = Team.objects.filter(competition_in_season=competition_in_season)
        return form

    def form_invalid(self, form):
        LOGGER.warning('User provided invalid data while updating a match.')
        return super().form_invalid(form)


class MatchDeleteView(DeleteView):
    model = Match
    template_name = "match_delete.html"

    def get_success_url(self):
        # gets back to the CompetitionInSeason of the deleted match
        competition_in_season_id = self.object.competition_in_season.id
        return reverse_lazy('matches_list', kwargs={'pk': competition_in_season_id})


class TeamsListView(ListView):
    model = Team
    template_name = "teams_list.html"
    context_object_name = 'teams_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Getting current season with a function
        selected_season_id = self.request.GET.get('season')
        current_season = get_current_season(selected_season_id)

        # Getting competitions in current season
        competitions = CompetitionInSeason.objects.filter(season=current_season)

        # For each competition in season we get teams
        competitions_teams = [] # [(competition), ([team1, team2...]),
        for competition_in_season in competitions:
            teams_in_competition = Team.objects.filter(
                competition_in_season=competition_in_season).order_by('name')
            competitions_teams.append((competition_in_season, teams_in_competition))

        # Adding seasons and competitions in context
        context['seasons'] = Season.objects.all()
        context['competitions'] = competitions
        context['current_season'] = current_season
        context['competitions_teams'] = competitions_teams

        return context


class TeamDetailView(DetailView):
    model = Team
    template_name = "team_detail.html"
    context_object_name = 'team'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cities'] = City.objects.all()
        return context


class TeamAddView(CreateView):
    model = Team
    form_class = TeamModelForm
    template_name = "form.html"
    success_url = reverse_lazy('teams_list')

    def form_invalid(self, form):
        LOGGER.warning('User provided invalid data while adding a city.')
        return super().form_invalid(form)


class TeamUpdateView(UpdateView):
    model = Team
    form_class = TeamModelForm
    template_name = "form.html"
    success_url = reverse_lazy('teams_list')

    def form_invalid(self, form):
        LOGGER.warning('User provided invalid data while updating a city.')
        return super().form_invalid(form)


class TeamDeleteView(DeleteView):
    model = Team
    template_name = "team_delete.html"
    success_url = reverse_lazy('teams_list')


class CitiesListView(ListView):
    model = City
    template_name = 'cities_list.html'
    context_object_name = 'cities'


class CityAddView(CreateView):
    form_class = CityModelForm
    template_name = "form.html"
    success_url = reverse_lazy('cities_list')

    def form_invalid(self, form):
        LOGGER.warning('User provided invalid data while adding a city.')
        return super().form_invalid(form)


class CityUpdateView(UpdateView):
    model = City
    form_class = CityModelForm
    template_name = "form.html"
    success_url = reverse_lazy('cities_list')

    def form_invalid(self, form):
        LOGGER.warning('User provided invalid data while updating a city.')
        return super().form_invalid(form)


class CityDeleteView(DeleteView):
    model = City
    template_name = "city_delete.html"
    success_url = reverse_lazy('cities_list')


