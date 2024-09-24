from referee_delegation_system.settings import SEASON_NAMES, COMPETITION_NAMES, COMPETITION_LEVELS, \
    COMPETITION_CATEGORIES

from django.db.models import Model, CharField, DateField, ForeignKey, SET_NULL, EmailField, DateTimeField, CASCADE


class City(Model):
    name = CharField(max_length=64, null=False, blank=False, unique=True)

    class Meta:
        verbose_name_plural = "Cities"
        ordering = ['name']

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


class CompetitionLevel(Model):
    COMPETITION_LEVELS = COMPETITION_LEVELS

    name = CharField(max_length=64, null=False, blank=False, unique=True, choices=COMPETITION_LEVELS)

    def __repr__(self):
        return f"CompetitionLevel(name={self.name})"

    def __str__(self):
        return f"{self.name}"

    # TODO: It should be how it is ordered in configuration file
    def __lt__(self, other):
        return self.COMPETITION_LEVELS.index() < self.COMPETITION_LEVELS.index()


class Competition(Model):
    COMPETITION_NAMES = COMPETITION_NAMES
    COMPETITION_CATEGORIES = COMPETITION_CATEGORIES

    name = CharField(max_length=64, null=False, blank=False, unique=True, choices=COMPETITION_NAMES)
    level = ForeignKey(CompetitionLevel, null=True, blank=True, on_delete=SET_NULL, related_name='competitions')
    category = CharField(max_length=64, null=True, blank=True, choices=COMPETITION_CATEGORIES)

    class Meta:
        ordering = ['level', 'name']  # TODO: It should be how it is defined in configuration file

    def __repr__(self):
        return f"Competition(name={self.name})"

    def __str__(self):
        return f"{self.name}"


class CompetitionInSeason(Model):
    competition = ForeignKey(Competition, null=False, blank=False, on_delete=CASCADE,
                             related_name='competition_in_seasons')
    season = ForeignKey(Season, null=False, blank=False, on_delete=CASCADE, related_name='competitions_in_season')

    class Meta:
        verbose_name_plural = "Competitions in seasons"
        ordering = ['-season__name', 'competition__level', 'competition__name']  # descending TODO: IS it OK?

    def __repr__(self):
        return f"CompetitionInSeason(name={self.competition.name} {self.season.name})"

    def __str__(self):
        return f"{self.competition.name} {self.season.name}"


class Team(Model):
    name = CharField(max_length=64, null=False, blank=False)
    city = ForeignKey(City, null=True, blank=True, on_delete=SET_NULL, related_name='teams')
    contact_person = CharField(max_length=64, null=True, blank=True)
    phone = CharField(max_length=20, null=True, blank=True)
    e_mail = EmailField(null=True, blank=True)
    competition_in_season = ForeignKey(CompetitionInSeason, null=True, blank=True, on_delete=SET_NULL,
                                       related_name='teams')

    class Meta:
        ordering = ['name']

    def __repr__(self):
        return (f"Team(name={self.name}, "
                f"competition_in_season={self.competition_in_season.competition.name} "
                f"{self.competition_in_season.season.name})")

    def __str__(self):
        return f"{self.name}"


class Match(Model):
    code = CharField(max_length=10, null=False, blank=False)
    competition_in_season = ForeignKey(CompetitionInSeason, null=True, blank=True, on_delete=SET_NULL,
                                       related_name='matches')
    home_team = ForeignKey(Team, null=True, blank=True, on_delete=SET_NULL, related_name='matches_home')
    away_team = ForeignKey(Team, null=True, blank=True, on_delete=SET_NULL, related_name='matches_away')
    date_time = DateTimeField(null=True, blank=True)
    city = ForeignKey(City, null=True, blank=True, on_delete=SET_NULL, related_name='matches')

    class Meta:
        verbose_name_plural = "Matches"
        ordering = ['date_time']

    def __repr__(self):
        return (f"Match(code={self.code}, "
                f"competition_in_season={self.competition_in_season.competition.name} "
                f"{self.competition_in_season.season.name}, "
                f"home_team={self.home_team.name}, away_team={self.away_team.name}, "
                f"date_time={self.date_time.strftime('%Y-%m-%d %H:%M:%S')}, city={self.city.name})")

    def __str__(self):
        return (f"{self.code} {self.home_team} vs. {self.away_team} {self.date_time.strftime("%x %H:%M")} "
                f"sports hall: {self.city}")
