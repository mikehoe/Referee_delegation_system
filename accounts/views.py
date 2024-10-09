from django.db.transaction import atomic
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from accounts.forms import ProfileRefereeForm
from accounts.models import ProfileReferee
from referees.models import Referee


class ProfileRefereeAddView(CreateView):
    form_class = ProfileRefereeForm
    template_name = "form.html"
    success_url = reverse_lazy('referees_list')


def profile_referee_update(request, pk):
    referee = get_object_or_404(Referee, pk=pk)
    profile_referee = ProfileReferee.objects.get(referee=referee)
    user = profile_referee.user

    initial_data = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
    }

    if request.method == 'POST':
        form = ProfileRefereeForm(request.POST, instance=referee, initial=initial_data)
        if form.is_valid():
            form.update(pk)
            return redirect('referees_list')
    else:
        form = ProfileRefereeForm(instance=referee, initial=initial_data)
        print(f"Load initial form data from referee profile: {profile_referee}")

    return render(request, 'form.html', {'form': form})


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
