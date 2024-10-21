from datetime import datetime

from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from django.test import TestCase

from accounts.models import ProfileReferee
from competitions.models import City, Match, Team, CompetitionInSeason, CompetitionLevel, Competition, Season
from delegations.models import Delegation, RefereeRole
from referees.models import Referee, RefereeLicenceType, Unavailability


class DelegationModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        print('-' * 80)

        city_brno = City.objects.create(name="Brno")
        city_pd = City.objects.create(name="Prievidza")
        city_pu = City.objects.create(name="Púchov")
        city_my = City.objects.create(name="Myjava")
        city_ba = City.objects.create(name="Bratislava")
        city_nr = City.objects.create(name="Nitra")
        city_mt = City.objects.create(name="Martin")

        licence_am = RefereeLicenceType.objects.create(name="AM")
        licence_a = RefereeLicenceType.objects.create(name="A")
        licence_b = RefereeLicenceType.objects.create(name="B")
        licence_c = RefereeLicenceType.objects.create(name="C")

        extra_league = CompetitionLevel.objects.create(name="extra_league")
        first_league = CompetitionLevel.objects.create(name="first_league")
        regional_league = CompetitionLevel.objects.create(name="regional_league")

        licence_am.competition_levels.add(extra_league, first_league, regional_league)
        licence_a.competition_levels.add(extra_league, first_league, regional_league)
        licence_b.competition_levels.add(first_league, regional_league)
        licence_c.competition_levels.add(regional_league)

        cls.user1 = User.objects.create(username="fedor.tirsel", first_name="Fedor", last_name="Tiršel")
        cls.referee1 = Referee.objects.create(licence_number=1, city=city_brno, licence_type=licence_am, rating=89.5)
        cls.profile1 = ProfileReferee.objects.create(user=cls.user1, referee=cls.referee1)
        Unavailability.objects.create(referee=cls.referee1, date_from='2024-10-28', date_to='2024-10-31')

        cls.user2 = User.objects.create(username="lubos.kohut", first_name="Ľuboš", last_name="Kohút")
        cls.referee2 = Referee.objects.create(licence_number=2, city=city_pd, licence_type=licence_a, rating=87.5)
        cls.profile2 = ProfileReferee.objects.create(user=cls.user2, referee=cls.referee2)

        cls.user3 = User.objects.create(username="jaroslav.stepanek", first_name="Jaroslav", last_name="Štěpánek")
        cls.referee3 = Referee.objects.create(licence_number=3, city=city_pd, licence_type=licence_a, rating=82.5)
        cls.profile3 = ProfileReferee.objects.create(user=cls.user3, referee=cls.referee3)
        Unavailability.objects.create(referee=cls.referee3, date_from='2024-10-31', date_to='2024-10-31')

        cls.user4 = User.objects.create(username="peter.cuntala", first_name="Peter", last_name="Čuntala")
        cls.referee4 = Referee.objects.create(licence_number=4, city=city_pu, licence_type=licence_a, rating=88.5)
        cls.profile4 = ProfileReferee.objects.create(user=cls.user4, referee=cls.referee4)

        cls.user5 = User.objects.create(username="miroslav.juracek", first_name="Miroslav", last_name="Juráček")
        cls.referee5 = Referee.objects.create(licence_number=5, city=city_ba, licence_type=licence_am, rating=92.5)
        cls.profile5 = ProfileReferee.objects.create(user=cls.user5, referee=cls.referee5)

        cls.user6 = User.objects.create(username="matej.gala", first_name="Matej", last_name="Gála")
        cls.referee6 = Referee.objects.create(licence_number=6, city=city_my, licence_type=licence_b, rating=85.5)
        cls.profile6 = ProfileReferee.objects.create(user=cls.user6, referee=cls.referee6)

        cls.user7 = User.objects.create(username="michaela.dubenova", first_name="Michaela", last_name="Dubeňová")
        cls.referee7 = Referee.objects.create(licence_number=7, city=city_ba, licence_type=licence_b, rating=82.5)
        cls.profile7 = ProfileReferee.objects.create(user=cls.user7, referee=cls.referee7)
        Unavailability.objects.create(referee=cls.referee7, date_from='2024-10-31', date_to='2024-11-3')

        cls.user8 = User.objects.create(username="marian.kovacik", first_name="Marian", last_name="Kováčik")
        cls.referee8 = Referee.objects.create(licence_number=8, city=city_pd, licence_type=licence_c, rating=83.5)
        cls.profile8 = ProfileReferee.objects.create(user=cls.user8, referee=cls.referee8)

        cls.user9 = User.objects.create(username="juraj.mokry", first_name="Juraj", last_name="Mokrý")
        cls.referee9 = Referee.objects.create(licence_number=9, city=city_mt, licence_type=licence_am, rating=96.5)
        cls.profile9 = ProfileReferee.objects.create(user=cls.user9, referee=cls.referee9)

        cls.user10 = User.objects.create(username="peter.malik", first_name="Peter", last_name="Malík")
        cls.referee10 = Referee.objects.create(licence_number=10, city=city_mt, licence_type=licence_a, rating=95.5)
        cls.profile10 = ProfileReferee.objects.create(user=cls.user10, referee=cls.referee10)

        cls.user11 = User.objects.create(username="peter.toman", first_name="Peter", last_name="Toman")
        cls.referee11 = Referee.objects.create(licence_number=11)
        cls.profile11 = ProfileReferee.objects.create(user=cls.user11, referee=cls.referee11)

        team_ba = Team.objects.create(name="VKP FTVŠ UK Bratislava")
        team_my = Team.objects.create(name="TJ Spartak Myjava")
        team_nr = Team.objects.create(name="VK Slávia SPU Nitra")
        team_po = Team.objects.create(name="VK MIRAD UNIPO Prešov")

        competition = Competition.objects.create(name="Extraliga muži", level=extra_league)
        # competition = Competition.objects.create(name="1. liga muži", level=first_league)

        season = Season.objects.create(name="2024/2025")
        competition_in_season = CompetitionInSeason.objects.create(competition=competition, season=season)

        cls.match_em01 = Match.objects.create(
            code="EM01",
            competition_in_season=competition_in_season,
            home_team=team_ba,
            away_team=team_my,
            date_time=datetime(2024, 10, 31, 18, 00),
            city=city_ba
        )

        cls.match_em02 = Match.objects.create(
            code="EM02",
            competition_in_season=competition_in_season,
            home_team=team_nr,
            away_team=team_po,
            date_time=datetime(2024, 10, 31, 18, 00),
            city=city_nr
        )

        cls.delegation1 = Delegation.objects.create(match=cls.match_em01, referee=cls.referee5, referee_role='1.R')

        cls.delegation2 = Delegation.objects.create(match=cls.match_em02, referee=cls.referee2, referee_role='2.R')

    def test_delegation_str(self):
        result = self.delegation1.__str__()
        print(f"test_delegation_str: {result}")
        self.assertEqual(result, "EM01, Miroslav Juráček, (1.R)")

    def test_delegation_repr(self):
        result = self.delegation1.__repr__()
        print(f"test_delegation_repr: {result}")
        self.assertEqual(result, f"Delegation(match=EM01, referee=Miroslav Juráček, referee_role=1.R)")

    def test_delegation_attributes(self):
        delegation = self.delegation1
        self.assertEqual(delegation.referee.name, "Miroslav")
        self.assertEqual(delegation.referee.surname, "Juráček")
        self.assertEqual(delegation.referee.city.name, "Bratislava")
        self.assertEqual(delegation.referee.licence_type.name, "AM")
        self.assertEqual(delegation.referee_role, "1.R")
        self.assertEqual(delegation.match.date_time.strftime('%x %H:%M'), "10/31/24 18:00")

    def test_delegation_match_relationship(self):
        delegation = self.delegation1
        self.assertIn(delegation, delegation.match.delegated_referees.all())
        self.assertEqual(delegation.match, Match.objects.get(code='EM01'))

    def test_delegation_referee_relationship(self):
        delegation = self.delegation1
        self.assertIn(delegation, delegation.referee.delegations.all())
        self.assertEqual(delegation.referee, Referee.objects.get(licence_number=5))

    def test_unique_together_constraint(self):
        # Creating a second delegation for the same match with the same referee
        with transaction.atomic():
            with self.assertRaises(IntegrityError):
                Delegation.objects.create(match=self.match_em02, referee=self.referee2, referee_role='1.R')

        with transaction.atomic():
            with self.assertRaises(IntegrityError):
                Delegation.objects.create(match=self.match_em02, referee=self.referee2, referee_role='2.R')

    def test_get_available_referees(self):
        Delegation.objects.create(match=self.match_em01, referee=self.referee10, referee_role='2.R')

        available_referees = Delegation.get_available_referees(self.match_em02, RefereeRole.FIRST_REFEREE)

        print(f"test_get_available_referees(EM02, {RefereeRole.FIRST_REFEREE}): \n{available_referees}")

        self.assertNotIn(self.referee1, available_referees)
        self.assertNotIn(self.referee2, available_referees)
        self.assertNotIn(self.referee3, available_referees)
        self.assertIn(self.referee4, available_referees)
        self.assertNotIn(self.referee5, available_referees)
        self.assertNotIn(self.referee6, available_referees)
        # self.assertIn(self.referee6, available_referees)
        self.assertNotIn(self.referee7, available_referees)
        self.assertNotIn(self.referee8, available_referees)
        self.assertIn(self.referee9, available_referees)
        self.assertNotIn(self.referee10, available_referees)
        self.assertNotIn(self.referee11, available_referees)

        available_line_judges = Delegation.get_available_referees(self.match_em02, RefereeRole.FIRST_LINE_JUDGE)

        print(f"test_get_available_referees(EM02, {RefereeRole.FIRST_LINE_JUDGE}): \n{available_line_judges}")

        self.assertNotIn(self.referee1, available_line_judges)
        self.assertNotIn(self.referee2, available_line_judges)
        self.assertNotIn(self.referee3, available_line_judges)
        self.assertIn(self.referee4, available_line_judges)
        self.assertNotIn(self.referee5, available_line_judges)
        self.assertIn(self.referee6, available_line_judges)
        self.assertNotIn(self.referee7, available_line_judges)
        self.assertIn(self.referee8, available_line_judges)
        self.assertIn(self.referee9, available_line_judges)
        self.assertNotIn(self.referee10, available_line_judges)
        self.assertIn(self.referee11, available_line_judges)
