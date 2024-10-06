from logging import getLogger

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from accounts.models import ProfileReferee
from referees.forms import UnavailabilityForm
from referees.models import Referee, RefereeLicenceType, City, Unavailability

LOGGER = getLogger()


class RefereesListView(ListView):
    model = Referee
    template_name = "referees_list.html"
    context_object_name = 'referees'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['licences'] = RefereeLicenceType.objects.all()
        context['cities'] = City.objects.all()
        context['selected_licence_id'] = self.request.GET.get('licence', None)
        context['selected_city_id'] = self.request.GET.get('city', None)

        selected_licence_id = context['selected_licence_id']
        selected_city_id = context['selected_city_id']

        referees = Referee.objects.all()

        if selected_licence_id:
            referees = referees.filter(licence_type_id=selected_licence_id)
            context['selected_licence'] = RefereeLicenceType.objects.get(id=selected_licence_id)

        if selected_city_id:
            referees = referees.filter(city_id=selected_city_id)
            context['selected_city'] = City.objects.get(id=selected_city_id)

        referees = referees.order_by('profile__user__last_name', 'profile__user__first_name')

        context['referees'] = referees
        return context


class RefereeDetailView(DetailView):
    model = Referee
    template_name = "referee_detail.html"
    context_object_name = 'referee'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['licences'] = RefereeLicenceType.objects.all()
        context['cities'] = City.objects.all()
        return context


class UnavailabilityListView(ListView):
    model = Unavailability
    template_name = "unavailabilities_list.html"
    context_object_name = 'unavailabilities'
    referee = None

    def get_queryset(self):
        referee_id = self.kwargs['pk']
        referee = Referee.objects.get(id=referee_id)

        if referee.profile.user != self.request.user:
            raise PermissionDenied

        self.referee = referee

        return Unavailability.objects.filter(referee=referee)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['referee'] = self.referee
        context['referee_id'] = self.referee.id
        return context


class UnavailabilityCreateView(CreateView):
    model = Unavailability
    form_class = UnavailabilityForm
    template_name = "form.html"
    success_url = reverse_lazy('unavailabilities_list')

    def form_valid(self, form):
        # Getting ProfileReferee for logged-in User
        profile_referee = ProfileReferee.objects.get(user=self.request.user)
        form.instance.referee = profile_referee.referee  # assigning referee
        return super().form_valid(form)

    def get_success_url(self):
        referee_id = self.kwargs['pk'] # ID from URL
        return reverse('unavailabilities_list', kwargs={'pk': referee_id})


class UnavailabilityUpdateView(LoginRequiredMixin, UpdateView):
    model = Unavailability
    fields = ['date_from', 'date_to']
    template_name = 'form.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.referee.profile.user != self.request.user:
            raise PermissionDenied
        return obj

    def get_queryset(self):
        referee_id = self.kwargs['referee_pk']
        return Unavailability.objects.filter(referee_id=referee_id)

    def get_success_url(self):
        referee_id = self.kwargs['referee_pk']
        return reverse('unavailabilities_list', kwargs={'pk': referee_id})


class UnavailabilityDeleteView(DeleteView):
    model = Unavailability
    template_name = "unavailability_delete.html"
    success_url = reverse_lazy('unavailabilities_list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.referee.profile.user != self.request.user:
            raise PermissionDenied("You do not have permission to delete this unavailability.")
        return obj

    def get_queryset(self):
        referee_id = self.kwargs['referee_pk']
        return Unavailability.objects.filter(referee_id=referee_id)

    def get_success_url(self):
        referee_id = self.kwargs['referee_pk']
        return reverse('unavailabilities_list', kwargs={'pk': referee_id})


# TODO: date_time format = "10.5.2024"
# TODO: create and update -> calendar (Javascript?)
# TODO: unavailalibities_list - ordering date_from, date_to
# TODO: unavailabilities list, view, edit and delete also for ProfileManager and Superuser (now only for the logged_in referee)