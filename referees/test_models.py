from django.test import TestCase
from .models import Referee, RefereeLicence, Unavailability
from competitions.models import City, CompetitionLevel
from datetime import date


class RefereeLicenceModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        print('-' * 80)
        level_1 = CompetitionLevel.objects.create(name="extra_league")
        level_2 = CompetitionLevel.objects.create(name="first_league")
        level_3 = CompetitionLevel.objects.create(name="regional")

        licence_1 = RefereeLicence.objects.create(name="A")
        licence_2 = RefereeLicence.objects.create(name="B")

        licence_1.level.add(level_1)
        licence_1.level.add(level_2)
        licence_1.level.add(level_3)
        licence_2.level.add(level_3)

    def test_referee_licence_str(self):
        licence = RefereeLicence.objects.get(name="A")
        print(f"test_referee_licence_str: '{licence.__str__()}'")
        self.assertEqual(licence.__str__(), "Licence = A")

    def test_referee_licence_repr(self):
        licence = RefereeLicence.objects.get(name="A")
        print(f"test_referee_licence_repr: '{licence.__repr__()}'")
        self.assertEqual(licence.__repr__(), "Licence(name=A)")

    def test_referee_licence_has_level(self):
        licence = RefereeLicence.objects.get(name="A")
        level_count = licence.level.count()
        print(f"test_referee_licence_has_level: {level_count}")
        self.assertEqual(level_count, 3)


class RefereeModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        print('-' * 80)
        city = City.objects.create(name="Praha")
        licence = RefereeLicence.objects.create(name="A")
        referee = Referee.objects.create(
            name="Jan",
            surname="Novák",
            city=city,
            licence=licence,
            rating=95.5,
            phone="123456789"
        )

    def test_referee_str(self):
        referee = Referee.objects.get(name="Jan", surname="Novák")
        print(f"test_referee_str: '{referee.__str__()}'")
        self.assertEqual(referee.__str__(), "Jan Novák - licence: A, city: Praha")

    def test_referee_repr(self):
        referee = Referee.objects.get(name="Jan", surname="Novák")
        print(f"test_referee_str: '{referee.__repr__()}'")
        self.assertEqual(referee.__repr__(), "Referee(name=Jan, surname=Novák)")

    def test_referee_city_relation(self):
        referee = Referee.objects.get(name="Jan", surname="Novák")
        city_name = referee.city.name
        print(f"test_referee_city_relation: {city_name}")
        self.assertEqual(city_name, "Praha")

    def test_referee_licence_relation(self):
        referee = Referee.objects.get(name="Jan", surname="Novák")
        licence_name = referee.licence.name
        print(f"test_referee_licence_relation: {licence_name}")
        self.assertEqual(licence_name, "A")


class UnavailabilityModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        print('-' * 80)
        city = City.objects.create(name="Brno")
        licence = RefereeLicence.objects.create(name="A")
        referee = Referee.objects.create(
            name="Josef",
            surname="Dvořák",
            city=city,
            licence=licence
        )
        unavailability = Unavailability.objects.create(
            referee=referee,
            date_from=date(2024, 9, 1),
            date_to=date(2024, 9, 5)
        )

    def test_unavailability_str(self):
        unavailability = Unavailability.objects.get(referee__name="Josef")
        print(f"test_unavailability_str: '{unavailability.__str__()}'")
        self.assertEqual(
            unavailability.__str__(),
            "Josef Dvořák unavailable from 2024-09-01 to 2024-09-05."
        )

    def test_unavailability_repr(self):
        unavailability = Unavailability.objects.get(referee__name="Josef")
        print(f"test_unavailability_str: '{unavailability.__repr__()}'")
        self.assertEqual(
            unavailability.__repr__(),
            "Referee(name=Josef Dvořák), unavailable from: 2024-09-01 to: 2024-09-05"
        )

    def test_unavailability_dates(self):
        unavailability = Unavailability.objects.get(referee__name="Josef")
        print(f"test_unavailability_dates: from {unavailability.date_from} to {unavailability.date_to}")
        self.assertEqual(unavailability.date_from, date(2024, 9, 1))
        self.assertEqual(unavailability.date_to, date(2024, 9, 5))

    def test_unavailability_referee_relation(self):
        unavailability = Unavailability.objects.get(referee__name="Josef")
        referee_name = unavailability.referee.name
        print(f"test_unavailability_referee_relation: {referee_name}")
        self.assertEqual(referee_name, "Josef")