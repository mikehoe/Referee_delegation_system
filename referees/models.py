from django.db.models import *
from competitions.models import City, CompetitionLevel
from referee_delegation_system.settings import REFEREE_LICENCE_TYPES


class RefereeLicenceType(Model):
    REFEREE_LICENCE_TYPES = REFEREE_LICENCE_TYPES

    name = CharField(max_length=5, null=False, blank=False, choices=REFEREE_LICENCE_TYPES)
    competition_level = ManyToManyField(CompetitionLevel, blank=True, related_name='licence_types')

    class Meta:
        ordering = ['id']

    def __repr__(self):
        return f"Licence(name={self.name})"

    def __str__(self):
        return f"{self.name}"


class Referee(Model):
    licence_number = IntegerField(null=False, blank=False, unique=True, default=None)
    licence_type = ForeignKey(RefereeLicenceType, null=True, blank=True, on_delete=SET_NULL, related_name='referees')
    city = ForeignKey(City, null=True, blank=True, on_delete=SET_NULL, related_name='referees')
    rating = FloatField(null=True, blank=True)
    phone = CharField(max_length=20, null=True, blank=True)

    @property
    def name(self):
        return self.profile.user.first_name

    @property
    def surname(self):
        return self.profile.user.last_name

    @property
    def email(self):
        return self.profile.user.email

    class Meta:
        ordering = ['licence_type__id', 'profile__user__last_name', 'profile__user__first_name']

    def __repr__(self):
        return f"Referee(name={self.name}, surname={self.surname})"

    def __str__(self):
        return f"{self.name} {self.surname} ({self.licence_type}, {self.rating}, {self.city})"


class Unavailability(Model):
    referee = ForeignKey(Referee, null=True, on_delete=SET_NULL, related_name='unavailabilities')
    date_from = DateField(null=False, blank=False)
    date_to = DateField(null=False, blank=False)

    class Meta:
        ordering = ['date_from', 'date_to']
        verbose_name_plural = "Unavailabilities"

    def __repr__(self):
        return f"Referee(name={self.referee.name} {self.referee.surname}), unavailable from: {self.date_from} to: {self.date_to}"

    def __str__(self):
        return f'{self.referee.name} {self.referee.surname} unavailable from {self.date_from} to {self.date_to}.'
