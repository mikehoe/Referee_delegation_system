from django.db.models import *
from competitions.models import City

class Referee(Model):
    class Licence(TextChoices):
        INTERNATIONAL = 'AM', 'International'
        EXTRA_LEAGUE = 'A', 'Extra League'
        FIRST_LEAGUE = 'B', 'First League'
        REGIONAL = 'C', 'Regional'

    name = CharField(max_length=32, null=False, blank=False)
    surname = CharField(max_length=32, null=False, blank=False)
    date_of_birth = DateField(null=True, blank=True)
    city = ForeignKey(City, null=True, blank=True, on_delete=SET_NULL, related_name='referees')
    licence = CharField(max_length=2, choices=Licence.choices, null=False, blank=False)
    rating = FloatField(null=True, blank=True)
    count_of_matches = IntegerField(null=True, blank=True)
    phone = CharField(max_length=20, null=True, blank=True)
    e_mail = EmailField(null=True, blank=True)

    def __repr__(self):
        return f"Referee(name={self.name}, surname={self.surname})"

    def __str__(self):
        return f"{self.name} {self.surname} - licence: {self.get_licence_display()}, city:{self.city}"


class Unavailability(Model):
    referee = ForeignKey(Referee, null=True, on_delete=SET_NULL, related_name='unavailabilities')
    date_from = DateField(null=False, blank=False)
    date_to = DateField(null=False, blank=False)

    def __str__(self):
        return f'{self.referee} unavailable from {self.date_from} to {self.date_to}'