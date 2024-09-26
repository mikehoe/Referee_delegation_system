from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView

from accounts.models import ProfileReferee
from accounts.forms import AddProfileRefereeForm, EditProfileRefereeForm
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

    def get_success_url(self):
        return reverse('referees_list')


class ProfileRefereeEditView(UpdateView):
    model = Referee
    template_name = "form_edit.html"
    fields = ['licence_number', 'licence_type', 'city', 'rating', 'phone']
    success_url = reverse_lazy('referees_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['licence_types'] = RefereeLicenceType.objects.all()
        context['cities'] = City.objects.all()

        referee = self.get_object()
        context['referee'] = referee

        profile_referee = ProfileReferee.objects.get(referee=referee)
        context['profile_referee'] = profile_referee

        context['first_name'] = profile_referee.user.first_name
        context['last_name'] = profile_referee.user.last_name

        return context

    def form_valid(self, form):
        # Získání rozhodčího a jeho profilu
        referee = form.save(commit=False)
        profile_referee = ProfileReferee.objects.get(referee=referee)

        # Aktualizace jména a příjmení v User modelu
        user = profile_referee.user
        user.first_name = self.request.POST.get('name')
        user.last_name = self.request.POST.get('surname')
        user.save()

        # Uložení samotného rozhodčího
        referee.save()
        return super().form_valid(form)

    def get_initial(self):
        profile_referee = ProfileReferee.objects.get(referee=self.object)
        initial = super().get_initial()
        initial['name'] = profile_referee.user.first_name
        initial['surname'] = profile_referee.user.last_name
        return initial


class ProfileRefereeDeleteView(DeleteView):
    model = Referee
    template_name = 'form_delete.html'
    success_url = reverse_lazy('referees_list')

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        referee = self.get_object()

        try:
            # Nalezení profilu rozhodčího
            profile_referee = ProfileReferee.objects.get(referee=referee)
        except ProfileReferee.DoesNotExist:
            return HttpResponse("No Profile found for this Referee.", status=400)

        # Uložení uživatele pro pozdější smazání
        user = profile_referee.user

        # Smažeme všechny tři objekty v rámci jedné atomické transakce
        profile_referee.delete()  # Smažeme profil
        referee.delete()          # Smažeme rozhodčího

        # Smažeme uživatele mimo transakci
        user.delete()

        return HttpResponseRedirect(self.success_url)
