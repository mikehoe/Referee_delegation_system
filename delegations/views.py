from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import View

from competitions.models import Match
from delegations.forms import MatchDelegationForm


class MatchDelegationView(PermissionRequiredMixin, View):
    permission_required = 'delegations.add_delegation'

    def get(self, request, pk):
        match = get_object_or_404(Match, id=pk)
        form = MatchDelegationForm(match=match)
        return render(request, 'match_delegations.html', {'form': form, 'match': match})

    def post(self, request, pk):
        match = get_object_or_404(Match, id=pk)
        form = MatchDelegationForm(request.POST, match=match)

        if form.is_valid():
            form.save(match)

            messages.success(request, 'Referees have been successfully delegated to the match.')

            competition_in_season = match.competition_in_season

            redirect_url = reverse('matches_list', args=[competition_in_season.id])
            return HttpResponseRedirect(redirect_url)
        else:
            messages.error(request, "Each referee can be delegated to only one role.")

        return render(request, 'match_delegations.html', {'form': form, 'match': match})


