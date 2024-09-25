from django.contrib.auth.models import User
from django.test import TestCase

from accounts.models import ProfileReferee
from competitions.models import City, Match, Team, CompetitionInSeason, CompetitionLevel, Competition, Season
from delegations.models import Delegation
from referees.models import Referee, RefereeLicenceType

class DelegationModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        print('-' * 80)

        city = City.objects.create(name="Olomouc")
        licence = RefereeLicenceType.objects.create(name="A")
        user = User.objects.create(username="bedrich", first_name="Bedřich", last_name="Smetana")
        referee = Referee.objects.create(
            licence_number=12345,
            city=city,
            licence_type=licence
        )
        ProfileReferee.objects.create(user=user, referee=referee)

        home_team = Team.objects.create(name="Volejbal Brno")
        away_team = Team.objects.create(name="ČEZ Karlovarsko")

        competition_level = CompetitionLevel.objects.create(name="first_league")
        competition = Competition.objects.create(
            name="1. liga muži",
            level=competition_level
        )
        season = Season.objects.create(name="2024/2025")

        competition_in_season = CompetitionInSeason.objects.create(
            competition=competition,
            season=season
        )

        match = Match.objects.create(
            code="MT001",
            competition_in_season=competition_in_season,
            home_team=home_team,
            away_team=away_team,
            date_time='2024-10-01 15:30:00',
            city=city
        )

        cls.delegation = Delegation.objects.create(
            match=match,
            referee=referee,
            referee_role='1.R'
        )

    def test_delegation_str(self):
        delegation = self.delegation
        print(f"test_delegation_str: '{delegation.__str__()}'")
        self.assertEqual(delegation.__str__(), "MT001, Bedřich Smetana, (1.R)")

    def test_delegation_repr(self):
        delegation = self.delegation
        print(f"test_delegation_repr: '{delegation.__repr__()}'")
        self.assertEqual(delegation.__repr__(), f"Delegation(match=MT001, referee=Bedřich Smetana, referee_role=1.R)")

    def test_delegation_attributes(self):
        delegation = self.delegation
        self.assertEqual(delegation.referee.name, "Bedřich")
        self.assertEqual(delegation.referee.surname, "Smetana")
        self.assertEqual(delegation.referee.city.name, "Olomouc")
        self.assertEqual(delegation.referee.licence_type.name, "A")
        self.assertEqual(delegation.referee_role, "1.R")
        self.assertEqual(delegation.match.date_time, "2024-10-01 15:30:00")

    def test_delegation_match_relationship(self):
        delegation = self.delegation
        self.assertIn(delegation, delegation.match.delegated_referees.all())
        self.assertEqual(delegation.match, Match.objects.get(code='MT001'))

    def test_delegation_referee_relationship(self):
        delegation = self.delegation
        self.assertIn(delegation, delegation.referee.delegations.all())
        self.assertEqual(delegation.referee, Referee.objects.get(licence_number=12345))