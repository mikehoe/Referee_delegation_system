from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View

from competitions.models import Match
from delegations.models import Delegation
from delegations.forms import BulkDelegationForm, MatchDelegationForm


class MatchDelegationView(PermissionRequiredMixin, View):
    permission_required = 'delegations.add_delegation'

    def get(self, request, pk):
        match = get_object_or_404(Match, id=pk)
        form = MatchDelegationForm(match=match)
        return render(request, 'match_delegation.html', {'form': form, 'match': match})

    def post(self, request, pk):
        match = get_object_or_404(Match, id=pk)
        form = MatchDelegationForm(request.POST, match=match)

        if form.is_valid():
            form.save(match)

            messages.success(request, 'Referees have been successfully delegated to the match.')

            # Gets competition_in_season for given match
            competition_in_season = match.competition_in_season

            # create URL for redirect
            redirect_url = reverse('matches_list', args=[competition_in_season.id])
            return HttpResponseRedirect(redirect_url)

        return render(request, 'match_delegation.html', {'form': form, 'match': match})


def bulk_delegation_view(request):
    if request.method == "POST":
        selected_match_ids = request.POST.getlist('selected_matches')
        print(f"Selected match IDs: {selected_match_ids}")  # Zkontrolujte, zda se ID zápasů správně odesílají

        if not selected_match_ids:
            print("No matches selected.")  # Pro debugging

        matches = Match.objects.filter(id__in=selected_match_ids)
        print(f"Selected matches: {matches}")  # Zkontrolujte, zda jsou zápasy správně načteny z databáze

        if not matches.exists():
            print("No matches exist.")  # Pro debugging
            return redirect('matches_list', pk=17)  # Pokud nejsou žádné zápasy, přesměrujte zpět

        competition_in_season_id = matches.first().competition_in_season.id

        form = BulkDelegationForm(matches=matches, data=request.POST)

        if form.is_valid():
            for match in matches:
                for role in ['1R', '2R', '1L', '2L']:
                    referee = form.cleaned_data.get(f'referee_{match.id}_{role}')
                    if referee:
                        Delegation.objects.create(match=match, referee=referee, referee_role=role)

            return redirect('matches_list', pk=competition_in_season_id)

        return render(request, 'bulk_delegation.html', {'form': form, 'matches': matches})

    return redirect('matches_list', pk=17)
