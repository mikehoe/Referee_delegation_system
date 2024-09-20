from referee_delegation_system.settings import SEASON_NAMES, COMPETITION_NAMES, COMPETITION_LEVELS, \
    COMPETITION_CATEGORIES

from django.db.models import Model, CharField, DateField, ForeignKey, SET_NULL, EmailField, DateTimeField


class City(Model):
    name = CharField(max_length=64, null=False, blank=False, unique=True)

    class Meta:
        verbose_name_plural = "Cities"
        ordering = ['name']  # ascending

    def __repr__(self):
        return f"City(name={self.name})"

    def __str__(self):
        return f"{self.name}"


class Season(Model):
    SEASON_NAMES = SEASON_NAMES
    name = CharField(max_length=20, null=False, blank=False, unique=True, choices=SEASON_NAMES)
    date_of_start = DateField(null=True, blank=True)
    date_of_end = DateField(null=True, blank=True)

    class Meta:
        ordering = ['-name']  # descending

    def __repr__(self):
        return f"Season(name={self.name})"

    def __str__(self):
        return f"{self.name}"


class Competition(Model):
    COMPETITION_NAMES = COMPETITION_NAMES
    COMPETITION_LEVELS = COMPETITION_LEVELS
    COMPETITION_CATEGORIES = COMPETITION_CATEGORIES

    name = CharField(max_length=64, null=False, blank=False, unique=True, choices=COMPETITION_NAMES)
    level = CharField(max_length=64, null=True, blank=True, unique=True, choices=COMPETITION_LEVELS)
    category = CharField(max_length=64, null=True, blank=True, unique=True, choices=COMPETITION_CATEGORIES)
    season = ForeignKey(Season, null=True, blank=True, on_delete=SET_NULL, related_name='competition_in')

    class Meta:
        ordering = ['name']  # TODO: it should be from high to low level

    def __repr__(self):
        return f"Season(name={self.name})"

    def __str__(self):
        return f"{self.name}"


class Team(Model):
    name = CharField(max_length=64, null=False, blank=False)
    city = ForeignKey(City, null=True, blank=True, on_delete=SET_NULL, related_name='team_from')
    contact_person = CharField(max_length=64, null=True, blank=True)
    phone = CharField(max_length=20, null=True, blank=True)
    e_mail = EmailField(max_length=64)

    class Meta:
        ordering = ['name']  # ascending

    def __repr__(self):
        return f"Team(name={self.name})"

    def __str__(self):
        return f"{self.name}"


class Match(Model):
    code = CharField(max_length=10, null=False, blank=False)
    competition = ForeignKey(Competition, on_delete=SET_NULL)
    home_team = ForeignKey(Team, null=True, blank=True, on_delete=SET_NULL, related_name='home_team')
    away_team = ForeignKey(Team, null=True, blank=True, on_delete=SET_NULL, related_name='away_team')
    date_time = DateTimeField(null=True, blank=True)
    city = ForeignKey(City, null=True, blank=True, on_delete=SET_NULL, related_name='match_played_in')

    def __str__(self):
        return f"{self.home_team} vs {self.away_team} - {self.competition}"
