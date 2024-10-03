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


class ProfileRefereeEditView(UpdateView):
    model = Referee
    form_class = AddProfileRefereeForm
    template_name = "form.html"
    success_url = reverse_lazy('referees_list')


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
        return redirect('referees_list')  # Přejděte na stránku úspěchu
    return render(request, 'form_delete.html', {'referee': referee})
