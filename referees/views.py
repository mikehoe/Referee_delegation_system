from logging import getLogger

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
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

        return Unavailability.objects.filter(referee=referee).order_by('date_from', 'date_to')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['referee'] = self.referee
        context['referee_id'] = self.referee.id
        return context


class AllUnavailabilitiesListView(PermissionRequiredMixin, ListView):
    model = Unavailability
    template_name = "all_unavailabilities_list.html"
    context_object_name = 'all_unavailabilities'
    permission_required = 'referees.view_unavailability'

    def get_queryset(self):
        # Getting all unavailabilities with a referee
        return Unavailability.objects.select_related('referee').order_by('referee', 'date_from', 'date_to')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        referees = Referee.objects.filter(unavailabilities__isnull=False).distinct()
        referee_unavailabilities = []

        # Getting selected referee from GET parameter
        selected_referee_pk = self.request.GET.get('referee')

        # If selected filter his unavailabilities
        if selected_referee_pk:
            selected_referee = Referee.objects.get(pk=selected_referee_pk)
            referee_unavailability = Unavailability.objects.filter(referee=selected_referee).order_by('date_from')
            referee_unavailabilities.append((selected_referee, referee_unavailability))
        else:
            # If not selected, show all
            for referee in referees:
                referee_unavailability = Unavailability.objects.filter(referee=referee).order_by('date_from')
                referee_unavailabilities.append((referee, referee_unavailability))

        context['referee_unavailabilities'] = referee_unavailabilities
        context['referees'] = referees
        context['selected_referee'] = selected_referee_pk
        return context


class UnavailabilityCreateView(CreateView):
    model = Unavailability
    form_class = UnavailabilityForm
    template_name = "unavailability_form.html"
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
    template_name = 'unavailability_form.html'

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


# TODO: merge of unavailabilities in case of overlaying time intervals
