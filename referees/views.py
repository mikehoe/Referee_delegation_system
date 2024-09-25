from django.views.generic import ListView
from referees.models import Referee, RefereeLicenceType

class RefereeListView(ListView):
    model = Referee
    template_name = "referees.html"
    context_object_name = 'referees'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['licences'] = RefereeLicenceType.objects.all()
        context['selected_licence_id'] = self.request.GET.get('licence', None)

        selected_licence_id = context['selected_licence_id']
        if selected_licence_id:
            context['referees'] = Referee.objects.filter(licence_type_id=selected_licence_id)
        else:
            context['referees'] = Referee.objects.all()

        return context