from logging import getLogger

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from accounts.models import ProfileReferee
from referees.forms import RefereeForm
from referees.models import Referee, RefereeLicenceType, City

LOGGER = getLogger()


class RefereeListView(ListView):
    model = Referee
    template_name = "referees.html"
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

        context['referees'] = referees
        return context


class RefereeAddView(CreateView):
    model = Referee
    template_name = "form_add.html"
    form_class = RefereeForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['licence_types'] = RefereeLicenceType.objects.all()
        context['cities'] = City.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        licence_number = request.POST.get('licence_number')
        licence_type_id = request.POST.get('licence_type')
        city_id = request.POST.get('city')
        rating = request.POST.get('rating')
        phone = request.POST.get('phone')
        username = request.POST.get('username')
        password = request.POST.get('password')
        name = request.POST.get('name')
        surname = request.POST.get('surname')

        if User.objects.filter(username=username).exists():
            form = self.get_form()
            form.add_error(None, 'Username already exists.')
            return self.form_invalid(form)

        user = User.objects.create_user(username=username, password=password, first_name=name, last_name=surname)

        referee = Referee(
            licence_number=licence_number,
            licence_type_id=licence_type_id,
            city_id=city_id,
            rating=rating,
            phone=phone
        )
        referee.save()

        ProfileReferee.objects.create(
            user=user,
            referee=referee
        )

        return super().form_valid(referee)

    def get_success_url(self):
        return reverse('referees')


class RefereeEditView(UpdateView):
    model = Referee
    template_name = "form_edit.html"
    fields = ['licence_number', 'licence_type', 'city', 'rating', 'phone']
    success_url = reverse_lazy('referees')

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
        profile_referee = ProfileReferee.objects.get(referee=self.object)

        profile_referee.user.first_name = self.request.POST.get('name')
        profile_referee.user.last_name = self.request.POST.get('surname')
        profile_referee.user.save()

        form.save()
        return super().form_valid(form)


class RefereeDeleteView(DeleteView):
    model = Referee
    template_name = 'form_delete.html'
    success_url = reverse_lazy('referees')

    def delete(self, request, *args, **kwargs):
        referee = self.get_object()
        profile_referee = get_object_or_404(ProfileReferee, referee=referee)
        user = profile_referee.user

        response = super().delete(request, *args, **kwargs)

        user.delete()
        return response
