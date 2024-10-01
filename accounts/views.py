from django.db.transaction import atomic
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView

from accounts.models import ProfileReferee
from accounts.forms import AddProfileRefereeForm
from competitions.models import City
from referees.models import Referee, RefereeLicenceType


class ProfileRefereeAddView(CreateView):
    model = Referee
    form_class = AddProfileRefereeForm
    template_name = "form_add.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['licence_types'] = RefereeLicenceType.objects.all()
        context['cities'] = City.objects.all()
        return context

    def form_valid(self, form):
        referee, user = form.save(commit=True)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('referees_list')


class ProfileRefereeEditView(UpdateView):
    model = Referee
    form_class = AddProfileRefereeForm
    template_name = "form_edit.html"

    def get_object(self, queryset=None):
        referee_id = self.kwargs.get("pk")
        return get_object_or_404(Referee, pk=referee_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['licence_types'] = RefereeLicenceType.objects.all()
        context['cities'] = City.objects.all()

        referee = self.get_object()
        profile = ProfileReferee.objects.get(referee=referee)
        context['user'] = profile.user
        return context

    def form_valid(self, form):
        referee = self.get_object()
        profile = ProfileReferee.objects.get(referee=referee)

        # Update referee information
        referee.licence_number = form.cleaned_data['licence_number']
        referee.licence_type = form.cleaned_data['licence_type']
        referee.city = form.cleaned_data['city']
        referee.rating = form.cleaned_data['rating']
        referee.phone = form.cleaned_data['phone']
        referee.save()

        # Update user information
        user = profile.user
        user.first_name = form.cleaned_data['name']
        user.last_name = form.cleaned_data['surname']
        user.email = form.cleaned_data['email']
        user.save()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('referees_list')


class ProfileRefereeDeleteView(DeleteView):
    model = ProfileReferee
    template_name = "form_delete.html"
    success_url = reverse_lazy('referees_list')

    @atomic
    def delete(self, request, *args, **kwargs):
        profile_referee = self.get_object()
        referee = profile_referee.referee
        user = profile_referee.user

        # Deaktivace uživatele
        user.is_active = False
        user.save()

        # Smazání rozhodčího, pokud má přiřazený profil
        referee.delete()

        # Smazání profilu rozhodčího
        profile_referee.delete()

        # Kontrola a smazání orphan referee záznamů
        orphaned_referees = Referee.objects.filter(profile=None)
        orphaned_referees.delete()

        return HttpResponseRedirect(self.get_success_url())
