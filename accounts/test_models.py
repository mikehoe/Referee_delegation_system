from django.test import TestCase
from django.contrib.auth.models import User

from competitions.models import City
from referees.models import RefereeLicenceType, Referee
from .models import ProfileReferee, ProfileManager


class ProfileRefereeModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        print('-' * 80)
        city = City.objects.create(name="Praha")
        licence = RefereeLicenceType.objects.create(name="A")
        user = User.objects.create_user(username='jan.novak', password='test', first_name='Jan', last_name='Novák')
        referee = Referee.objects.create(
            licence_number=123456,
            licence_type=licence,
            city=city
        )
        ProfileReferee.objects.create(user=user, referee=referee)

    def test_profile_referee_str(self):
        profile = ProfileReferee.objects.get(user__username='jan.novak')
        print(f"test_profile_referee_str: '{profile.__str__()}'")
        self.assertEqual(profile.__str__(), "Profile referee Jan Novák (username=jan.novak)")

    def test_profile_referee_repr(self):
        profile = ProfileReferee.objects.get(user__username='jan.novak')
        print(f"test_profile_referee_repr: '{profile.__repr__()}'")
        self.assertEqual(profile.__repr__(), "ProfileReferee(username=jan.novak, licence=123456)")

    def test_referee_attributes(self):
        profile = ProfileReferee.objects.get(user__username='jan.novak')
        referee = profile.referee
        self.assertEqual(referee.name, "Jan")
        self.assertEqual(referee.surname, "Novák")
        self.assertEqual(referee.city.name, "Praha")
        self.assertEqual(referee.licence_type.name, "A")


class ProfileManagerModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        print('-' * 80)
        user = User.objects.create_user(username='josef.dvorak', password='test', first_name='Josef', last_name='Dvořák')
        ProfileManager.objects.create(user=user, phone='123456789')

    def test_profile_manager_str(self):
        profile = ProfileManager.objects.get(user__username='josef.dvorak')
        print(f"test_profile_manager_str: '{profile.__str__()}'")
        self.assertEqual(profile.__str__(), "Profile manager Josef Dvořák (username=josef.dvorak, type=None)")

    def test_profile_manager_repr(self):
        profile = ProfileManager.objects.get(user__username='josef.dvorak')
        print(f"test_profile_manager_repr: '{profile.__repr__()}'")
        self.assertEqual(profile.__repr__(), "ProfileManager(username=josef.dvorak, type=None)")