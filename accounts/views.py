from django.contrib.auth import logout
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.transaction import atomic
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from accounts.forms import ProfileRefereeForm, ProfileLoggedRefereeForm
from accounts.models import ProfileReferee
from referees.models import Referee


class ProfileRefereeAddView(PermissionRequiredMixin, CreateView):
    form_class = ProfileRefereeForm
    template_name = "form.html"
    success_url = reverse_lazy('referees_list')
    permission_required = 'referees.add_referee'


def profile_referee_update(request, pk):
    referee = get_object_or_404(Referee, pk=pk)
    profile_referee = ProfileReferee.objects.get(referee=referee)
    user = profile_referee.user

    if request.user == referee.profile.user or request.user.has_perm('referees.change_referee'):

        initial_data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
        }

        if request.method == 'POST':
            if request.user == referee.profile.user:
                form = ProfileLoggedRefereeForm(request.POST, instance=referee, initial=initial_data)
            else:
                form = ProfileRefereeForm(request.POST, instance=referee, initial=initial_data)
            if form.is_valid():
                form.update(pk)
                return redirect('referees_list')
        else:
            if request.user == referee.profile.user:
                form = ProfileLoggedRefereeForm(instance=referee, initial=initial_data)
            else:
                form = ProfileRefereeForm(instance=referee, initial=initial_data)
            print(f"Load initial form data from referee profile: {profile_referee}")

        return render(request, 'form.html', {'form': form})


@permission_required('referees.delete_referee', raise_exception=True)
@atomic
def profile_referee_delete(request, pk):
    referee = get_object_or_404(Referee, pk=pk)
    profile_referee = ProfileReferee.objects.get(referee=referee)
    user = profile_referee.user
    if request.method == 'POST':
        print(f"Delete referee profile: {profile_referee}")
        referee.profile.delete()
        print(f"Delete referee: {referee}")
        referee.delete()
        print(f"Delete user: {user}")
        user.delete()
        return redirect('referees_list')
    return render(request, 'form_delete.html', {'object': referee})


@login_required
def user_logout(request):
    logout(request)
    return redirect('competitions_in_season')
