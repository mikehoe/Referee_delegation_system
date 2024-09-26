from logging import getLogger
from django.views.generic import ListView
from referees.models import Referee, RefereeLicenceType, City

LOGGER = getLogger()


class RefereesListView(ListView):
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


