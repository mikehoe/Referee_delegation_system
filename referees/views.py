from logging import getLogger

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from competitions.models import Match
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

        current_user = self.request.user
        current_referee = None

        if current_user.is_authenticated and hasattr(current_user, 'profile'):
            profile = current_user.profile
            if hasattr(profile, 'referee'):
                current_referee = profile.referee

        referees = Referee.objects.all()

        if selected_licence_id:
            referees = referees.filter(licence_type_id=selected_licence_id)
            context['selected_licence'] = RefereeLicenceType.objects.get(id=selected_licence_id)

        if selected_city_id:
            referees = referees.filter(city_id=selected_city_id)
            context['selected_city'] = City.objects.get(id=selected_city_id)

        referees = referees.order_by('profile__user__last_name', 'profile__user__first_name')

        if current_referee:
            referees = list(referees)  # Create list for manipulations
            if current_referee not in referees:  # Making sure we don’t add a referee twice
                referees.insert(0, current_referee)

        context['referees'] = referees
        context['current_referee'] = current_referee

        return context


class RefereeDetailView(DetailView):
    model = Referee
    template_name = "referee_detail.html"
    context_object_name = 'referee'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['licences'] = RefereeLicenceType.objects.all()
        context['cities'] = City.objects.all()

        # Checks, if the user is logged-in
        if self.request.user.is_authenticated:
            profile_referee = getattr(self.request.user, 'profile', None)
            is_referee = profile_referee and profile_referee.referee == self.object
            has_permission = self.request.user.has_perm('referees.view_unavailability')

            # Referee can see their own unavailibilities and assigned matches
            if is_referee:
                context['unavailabilities'] = Unavailability.objects.filter(referee=self.object)
                context['show_unavailability_button'] = True
                context['assigned_matches'] = Match.objects.filter(delegated_referees__referee=self.object)

            # Manager can see the unavailabilities of any referee and assigned matches
            elif has_permission:
                context['unavailability_list_url'] = reverse('unavailabilities_list', kwargs={'pk': self.object.id})
                context['show_unavailability_button'] = True
                context['assigned_matches'] = Match.objects.filter(delegated_referees__referee=self.object)

        return context


class UnavailabilityListView(ListView):
    model = Unavailability
    template_name = "unavailabilities_list.html"
    context_object_name = 'unavailabilities'
    referee = None

    def get_queryset(self):
        referee_id = self.kwargs['pk']
        referee = Referee.objects.get(id=referee_id)

        # Allows access to the logged-in user or user with permission
        if referee.profile.user == self.request.user or self.request.user.has_perm('referees.view_unavailability'):
            self.referee = referee
            return Unavailability.objects.filter(referee=referee).order_by('date_from', 'date_to')

        raise PermissionDenied

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['referee'] = self.referee
        context['referee_id'] = self.referee.id
        return context


class UnavailabilityCreateView(CreateView):
    model = Unavailability
    form_class = UnavailabilityForm
    template_name = "unavailability_form.html"
    success_url = reverse_lazy('unavailabilities_list')

    def form_valid(self, form):
        referee_id = self.kwargs['pk']  # Get referee ID from URL
        referee = Referee.objects.get(id=referee_id)

        # Assign the referee to the form instance
        form.instance.referee = referee

        # Check if the logged-in user is the referee or has the right permission
        if referee.profile.user != self.request.user and not self.request.user.has_perm('referees.add_unavailability'):
            raise PermissionDenied

        return super().form_valid(form)

    def get_success_url(self):
        referee_id = self.kwargs['pk']  # ID from URL
        return reverse('unavailabilities_list', kwargs={'pk': referee_id})


class UnavailabilityUpdateView(LoginRequiredMixin, UpdateView):
    model = Unavailability
    form_class = UnavailabilityForm
    template_name = 'unavailability_form.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        # Check if the user is the referee or has the right permission
        if obj.referee.profile.user != self.request.user and not self.request.user.has_perm('referees.change_unavailability'):
            raise PermissionDenied
        return obj

    def get_success_url(self):
        referee_id = self.kwargs['referee_pk']
        return reverse('unavailabilities_list', kwargs={'pk': referee_id})


class UnavailabilityDeleteView(LoginRequiredMixin, DeleteView):
    model = Unavailability
    template_name = "unavailability_delete.html"
    success_url = reverse_lazy('unavailabilities_list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        # Check if the user is the referee or has the right permission
        if obj.referee.profile.user != self.request.user and not self.request.user.has_perm('referees.delete_unavailability'):
            raise PermissionDenied
        return obj

    def get_success_url(self):
        referee_id = self.kwargs['referee_pk']
        return reverse('unavailabilities_list', kwargs={'pk': referee_id})


