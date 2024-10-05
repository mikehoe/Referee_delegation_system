from django.db.transaction import atomic
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView

from accounts.models import ProfileReferee
from accounts.forms import AddProfileRefereeForm
from competitions.models import City
from referees.models import Referee, RefereeLicenceType


class ProfileRefereeAddView(CreateView):
    form_class = AddProfileRefereeForm
    template_name = "form.html"
    success_url = reverse_lazy('referees_list')


# TODO FIX
def update_profile_referee(request, pk):
    referee = get_object_or_404(Referee, pk=pk)
    profile_referee = ProfileReferee.objects.get(referee=referee)
    user = profile_referee.user
    if request.method == 'POST':
        form = AddProfileRefereeForm(request.POST, instance=referee)
        if form.is_valid():
            form.save()
            return redirect('referees_list')
    else:
        form = AddProfileRefereeForm(instance=referee)
        print(user.first_name)
    return render(request, 'form.html', {'form': form})


@atomic
def profile_referee_delete(request, pk):
    referee = get_object_or_404(Referee, pk=pk)
    profile_referee = ProfileReferee.objects.get(referee=referee)
    user = profile_referee.user
    if request.method == 'POST':
        print(profile_referee)
        referee.profile.delete()
        print(referee)
        referee.delete()
        print(user)
        user.delete()
        return redirect('referees_list')
    return render(request, 'form_delete.html', {'object': referee})
