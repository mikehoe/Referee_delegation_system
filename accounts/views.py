from django.contrib.auth import logout
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.transaction import atomic
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from accounts.forms import ProfileRefereeForm, ProfileLoggedRefereeForm, ProfileManagerForm, ProfileLoggedManagerForm
from accounts.models import ProfileReferee, ProfileManager
from referees.models import Referee


@login_required
def user_logout(request):
    logout(request)
    return redirect('competitions_in_season')


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
    else:
        raise PermissionDenied


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


class ProfileManagersListView(ListView):
    model = ProfileManager
    template_name = "profile_managers_list.html"
    context_object_name = 'profile_managers'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        current_user = self.request.user
        current_profile_manager = None

        if current_user.is_authenticated and hasattr(current_user, 'profile_manager'):
            current_profile_manager = current_user.profile_manager

        profile_managers = ProfileManager.objects.filter(user__is_staff=False).order_by('user__last_name',
                                                                                        'user__first_name')
        if current_profile_manager:
            profile_managers = list(profile_managers)  # Create list for manipulations
            if current_profile_manager not in profile_managers:  # Making sure we don’t add a referee twice
                profile_managers.insert(0, current_profile_manager)

        context['profile_managers'] = profile_managers
        context['current_profile_manager'] = current_profile_manager

        return context


class ProfileManagerDetailView(DetailView):
    model = ProfileManager
    template_name = 'profile_manager_detail.html'
    context_object_name = 'profile_manager'


class ProfileManagerAddView(PermissionRequiredMixin, CreateView):
    form_class = ProfileManagerForm
    template_name = "form.html"
    success_url = reverse_lazy('profile_managers_list')
    permission_required = 'accounts.add_profile_manager'


def profile_manager_update(request, pk):
    profile_manager = get_object_or_404(ProfileManager, pk=pk)
    user = profile_manager.user

    if request.user == profile_manager.user or request.user.has_perm('accounts.change_profile_manager'):
        initial_data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
        }

        if request.method == 'POST':
            if request.user == profile_manager.user:
                form = ProfileLoggedManagerForm(request.POST, instance=profile_manager, initial=initial_data)
            else:
                form = ProfileManagerForm(request.POST, instance=profile_manager, initial=initial_data)
            if form.is_valid():
                form.update(pk)
                return redirect('profile_manager_detail', pk=pk)
        else:
            if request.user == profile_manager.user:
                form = ProfileLoggedManagerForm(instance=profile_manager, initial=initial_data)
            else:
                form = ProfileManagerForm(instance=profile_manager, initial=initial_data)
            print(f"Load initial form data from manager profile: {profile_manager}")

        return render(request, 'form.html', {'form': form})
    else:
        raise PermissionDenied


@permission_required('accounts.delete_profile_manager', raise_exception=True)
@atomic
def profile_manager_delete(request, pk):
    profile_manager = ProfileManager.objects.get(pk=pk)
    user = profile_manager.user
    if request.method == 'POST':
        print(f"Delete user: {user} and delete on cascade profile: {profile_manager}")
        user.delete()
        return redirect('profile_managers_list')
    return render(request, 'form_delete.html', {'object': profile_manager})
