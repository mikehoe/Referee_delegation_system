from django.test import TestCase
from competitions.models import City, Season, CompetitionLevel, Competition, CompetitionInSeason, Team, Match
from datetime import date, datetime

class CityModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.city = City.objects.create(name="Praha")

    def test_city_str(self):
        self.assertEqual(self.city.__str__(), "Praha")

    def test_city_repr(self):
        self.assertEqual(self.city.__repr__(), "City(name=Praha)")


class SeasonModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.season = Season.objects.create(name="2024/2025", date_of_start=date(2024, 9, 1), date_of_end=date(2025, 6, 30))

    def test_season_str(self):
        self.assertEqual(self.season.__str__(), "2024/2025")

    def test_season_repr(self):
        self.assertEqual(self.season.__repr__(), "Season(name=2024/2025)")


class CompetitionLevelModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.level = CompetitionLevel.objects.create(name="extra_league")

    def test_competition_level_str(self):
        self.assertEqual(self.level.__str__(), "extra_league")

    def test_competition_level_repr(self):
        self.assertEqual(self.level.__repr__(), "CompetitionLevel(name=extra_league)")


class CompetitionModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        level = CompetitionLevel.objects.create(name="extra_league")
        Competition.objects.create(name="Extraliga muži", level=level, category="men")

    def test_competition_str(self):
        competition = Competition.objects.get(name="Extraliga muži")
        self.assertEqual(competition.__str__(), "Extraliga muži")

    def test_competition_repr(self):
        competition = Competition.objects.get(name="Extraliga muži")
        self.assertEqual(competition.__repr__(), "Competition(name=Extraliga muži)")

    def test_competition_level_relation(self):
        competition = Competition.objects.get(name="Extraliga muži")
        self.assertEqual(competition.level.name, "extra_league")


class CompetitionInSeasonModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        level = CompetitionLevel.objects.create(name="first_league")
        competition = Competition.objects.create(name="1. liga ženy", level=level, category="women")
        season = Season.objects.create(name="2024/2025", date_of_start=date(2024, 9, 1), date_of_end=date(2025, 6, 30))
        CompetitionInSeason.objects.create(competition=competition, season=season)

    def test_competition_in_season_str(self):
        competition_in_season = CompetitionInSeason.objects.get(competition__name="1. liga ženy")
        self.assertEqual(competition_in_season.__str__(), "1. liga ženy 2024/2025")

    def test_competition_in_season_repr(self):
        competition_in_season = CompetitionInSeason.objects.get(competition__name="1. liga ženy")
        self.assertEqual(competition_in_season.__repr__(), "CompetitionInSeason(name=1. liga ženy 2024/2025)")

    def test_competition_in_season_relations(self):
        competition_in_season = CompetitionInSeason.objects.get(competition__name="1. liga ženy")
        self.assertEqual(competition_in_season.competition.name, "1. liga ženy")
        self.assertEqual(competition_in_season.season.name, "2024/2025")


class TeamModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        city = City.objects.create(name="Ostrava")
        level = CompetitionLevel.objects.create(name="extra_league")
        competition = Competition.objects.create(name="Extraliga ženy", level=level, category="women")
        season = Season.objects.create(name="2024/2025", date_of_start=date(2024, 9, 1), date_of_end=date(2025, 6, 30))
        competition_in_season = CompetitionInSeason.objects.create(competition=competition, season=season)
        Team.objects.create(name="TJ Ostrava", city=city, competition_in_season=competition_in_season)

    def test_team_str(self):
        team = Team.objects.get(name="TJ Ostrava")
        self.assertEqual(team.__str__(), "TJ Ostrava")

    def test_team_repr(self):
        team = Team.objects.get(name="TJ Ostrava")
        self.assertEqual(team.__repr__(), "Team(name=TJ Ostrava, competition_in_season=Extraliga ženy 2024/2025)")

    def test_team_city_relation(self):
        team = Team.objects.get(name="TJ Ostrava")
        self.assertEqual(team.city.name, "Ostrava")

    def test_team_competition_in_season_relation(self):
        team = Team.objects.get(name="TJ Ostrava")
        self.assertEqual(team.competition_in_season.competition.name, "Extraliga ženy")
        self.assertEqual(team.competition_in_season.season.name, "2024/2025")


class MatchModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        city_1 = City.objects.create(name="Brno")
        city_2 = City.objects.create(name="Praha")
        level = CompetitionLevel.objects.create(name="extra_league")
        competition = Competition.objects.create(name="Extraliga muži", level=level, category="men")
        season = Season.objects.create(name="2023/2024", date_of_start=date(2023, 9, 1), date_of_end=date(2024, 6, 30))
        competition_in_season = CompetitionInSeason.objects.create(competition=competition, season=season)
        home_team = Team.objects.create(name="Volejbal Brno", city=city_1, competition_in_season=competition_in_season)
        away_team = Team.objects.create(name="VK Lvi Praha", city=city_2, competition_in_season=competition_in_season)
        Match.objects.create(code="M001", competition_in_season=competition_in_season, home_team=home_team, away_team=away_team, date_time=datetime(2023, 10, 1, 15, 30), city=city_1)

    def test_match_str(self):
        match = Match.objects.get(code="M001")
        self.assertEqual(match.__str__(), "M001 Volejbal Brno vs. VK Lvi Praha 10/01/23 15:30 sports hall: Brno")

    def test_match_repr(self):
        match = Match.objects.get(code="M001")
        self.assertEqual(match.__repr__(), "Match(code=M001, competition_in_season=Extraliga muži 2023/2024, home_team=Volejbal Brno, away_team=VK Lvi Praha, date_time=2023-10-01 15:30:00, city=Brno)")

    def test_match_teams_relation(self):
        match = Match.objects.get(code="M001")
        self.assertEqual(match.home_team.name, "Volejbal Brno")
        self.assertEqual(match.away_team.name, "VK Lvi Praha")

    def test_match_city_relation(self):
        match = Match.objects.get(code="M001")
        self.assertEqual(match.city.name, "Brno")

    def test_match_competition_in_season_relation(self):
        match = Match.objects.get(code="M001")
        self.assertEqual(match.competition_in_season.competition.name, "Extraliga muži")
        self.assertEqual(match.competition_in_season.season.name, "2023/2024")