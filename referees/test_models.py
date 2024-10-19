from django.test import TestCase

from accounts.models import ProfileReferee
from .models import Referee, RefereeLicenceType, Unavailability
from competitions.models import City, CompetitionLevel
from datetime import date
from django.contrib.auth.models import User


class RefereeLicenceTypeModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        print('-' * 80)
        level_1 = CompetitionLevel.objects.create(name="extra_league")
        level_2 = CompetitionLevel.objects.create(name="first_league")
        level_3 = CompetitionLevel.objects.create(name="regional")

        licence_1 = RefereeLicenceType.objects.create(name="A")
        licence_2 = RefereeLicenceType.objects.create(name="B")

        licence_1.competition_levels.add(level_1)
        licence_1.competition_levels.add(level_2)
        licence_1.competition_levels.add(level_3)
        licence_2.competition_levels.add(level_3)

        licence_1.save()
        licence_2.save()

    def test_referee_licence_str(self):
        licence = RefereeLicenceType.objects.get(name="A")
        print(f"test_referee_licence_str: '{licence.__str__()}'")
        self.assertEqual(licence.__str__(), "A")

    def test_referee_licence_repr(self):
        licence = RefereeLicenceType.objects.get(name="A")
        print(f"test_referee_licence_repr: '{licence.__repr__()}'")
        self.assertEqual(licence.__repr__(), "Licence(name=A)")

    def test_referee_licence_has_level(self):
        licence = RefereeLicenceType.objects.get(name="A")
        level_count = licence.competition_levels.count()
        print(f"test_referee_licence_has_level: {level_count}")
        self.assertEqual(level_count, 3)


class RefereeModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        print('-' * 80)
        user = User.objects.create_user(username='jan_novak', first_name='Jan', last_name='Novák', password='testpass')
        city = City.objects.create(name="Praha")
        licence = RefereeLicenceType.objects.create(name="A")
        referee = Referee.objects.create(
            licence_number=12345,
            licence_type=licence,
            city=city,
            rating=95.5,
            phone="123456789"
        )
        referee.profile = ProfileReferee.objects.create(user=user, referee=referee)
        print(referee.name)
        referee.save()

    def test_referee_str(self):
        referee = Referee.objects.get(licence_number=12345)
        print(f"test_referee_str: '{referee.__str__()}'")
        self.assertEqual(referee.__str__(), "Jan Novák (A, 95.5, Praha)")

    def test_referee_repr(self):
        referee = Referee.objects.get(licence_number=12345)
        print(f"test_referee_repr: '{referee.__repr__()}'")
        self.assertEqual(referee.__repr__(), "Referee(name=Jan, surname=Novák, licence=A, rating=95.5, city=Praha)")

    def test_referee_city_relation(self):
        referee = Referee.objects.get(licence_number=12345)
        city_name = referee.city.name
        print(f"test_referee_city_relation: {city_name}")
        self.assertEqual(city_name, "Praha")

    def test_referee_licence_relation(self):
        referee = Referee.objects.get(licence_number=12345)
        licence_name = referee.licence_type.name
        print(f"test_referee_licence_relation: {licence_name}")
        self.assertEqual(licence_name, "A")

    def test_referee_name_property(self):
        referee = Referee.objects.get(licence_number=12345)
        licence_name = referee.licence_type.name
        print(f"test_referee_licence_relation: {licence_name}")
        self.assertEqual(licence_name, "A")


class UnavailabilityModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        print('-' * 80)
        user = User.objects.create_user(username='josef_dvorak', first_name='Josef', last_name='Dvořák',
                                        password='test')
        city = City.objects.create(name="Brno")
        licence = RefereeLicenceType.objects.create(name="A")
        referee = Referee.objects.create(
            licence_number=54321,
            licence_type=licence,
            city=city
        )
        # Create ProfileReferee
        referee.profile = ProfileReferee.objects.create(user=user, referee=referee)
        referee.unavailability = Unavailability.objects.create(
            referee=referee,
            date_from=date(2024, 9, 1),
            date_to=date(2024, 9, 5)
        )

        referee.save()

    def test_unavailability_str(self):
        unavailability = Unavailability.objects.get(referee__profile__user__first_name="Josef")
        print(f"test_unavailability_str: '{unavailability.__str__()}'")
        self.assertEqual(
            unavailability.__str__(),
            "Josef Dvořák unavailable from 2024-09-01 to 2024-09-05."
        )

    def test_unavailability_repr(self):
        unavailability = Unavailability.objects.get(referee__profile__user__first_name="Josef")
        print(f"test_unavailability_repr: '{unavailability.__repr__()}'")
        self.assertEqual(
            unavailability.__repr__(),
            "Referee(name=Josef Dvořák), unavailable from: 2024-09-01 to: 2024-09-05"
        )

    def test_unavailability_dates(self):
        unavailability = Unavailability.objects.get(referee__profile__user__first_name="Josef")
        print(f"test_unavailability_dates: from {unavailability.date_from} to {unavailability.date_to}")
        self.assertEqual(unavailability.date_from, date(2024, 9, 1))
        self.assertEqual(unavailability.date_to, date(2024, 9, 5))

    def test_unavailability_referee_relation(self):
        unavailability = Unavailability.objects.get(referee__profile__user__first_name="Josef")
        referee_name = unavailability.referee.profile.user.first_name
        print(f"test_unavailability_referee_relation: {referee_name}")
        self.assertEqual(referee_name, "Josef")
