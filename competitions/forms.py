from django.forms import ModelForm

from competitions.models import City


class CityModelForm(ModelForm):
    class Meta:
        model = City
        fields = '__all__'