from django.db.models import *
from competitions.models import City, CompetitionLevel
from referee_delegation_system.settings import REFEREE_LICENCES


class RefereeLicence(Model):
    REFEREE_LICENCES = REFEREE_LICENCES

    name = CharField(max_length=5, null=False, blank=False, choices=REFEREE_LICENCES)
    level = ManyToManyField(CompetitionLevel, null=True, blank=True, on_delete=SET_NULL, related_name='licences')

    def __repr__(self):
        return f"Licence(name={self.name})"

    def __str__(self):
        return f"Licence = {self.name}"


class Referee(Model):
    name = CharField(max_length=32, null=False, blank=False)
    surname = CharField(max_length=32, null=False, blank=False)
    date_of_birth = DateField(null=True, blank=True)
    city = ForeignKey(City, null=True, blank=True, on_delete=SET_NULL, related_name='referees')
    licence = ForeignKey(RefereeLicence, null=True, blank=True, on_delete=SET_NULL, related_name='referees')
    rating = FloatField(null=True, blank=True)
    phone = CharField(max_length=20, null=True, blank=True)
    # e_mail = EmailField(null=True, blank=True)  - 'e-mail' is in User ?

    class Meta:
        ordering = ['name']

    def __repr__(self):
        return f"Referee(name={self.name}, surname={self.surname})"

    def __str__(self):
        return f"{self.name} {self.surname} - licence: {self.licence.name}, city:{self.city}"


class Unavailability(Model):
    referee = ForeignKey(Referee, null=True, on_delete=SET_NULL, related_name='unavailabilities')
    date_from = DateField(null=False, blank=False)
    date_to = DateField(null=False, blank=False)

    class Meta:
        ordering = ['date_from', 'date_to']

    def __repr__(self):
        return f"Referee(name={self.referee}), unavailable from: {self.date_from} to: {self.date_to}"

    def __str__(self):
        return f'{self.referee} unavailable from {self.date_from} to {self.date_to}.'