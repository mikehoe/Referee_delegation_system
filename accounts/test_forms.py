from django.test import TestCase
from django.contrib.auth import get_user_model

from accounts.forms import ProfileRefereeForm
from referees.models import Referee, RefereeLicenceType
from accounts.models import ProfileReferee
from competitions.models import City

User = get_user_model()


class AddProfileRefereeFormTest(TestCase):
    """Test for AddProfileRefereeForm."""

    def setUp(self):
        self.licence_type = RefereeLicenceType.objects.create(name='A')
        self.city = City.objects.create(name='Rychnov nad Kněžnou')

        self.valid_form_data = {
            'email': 'josef.sikela@example.com',
            'licence_number': '123456',
            'licence_type': self.licence_type.id,
            'city': self.city.id,
            'rating': 90,
            'phone': '+420733339891',
            'first_name': 'Josef',
            'last_name': 'Sikela',
        }
        self.empty_form_data = {}

    def test_valid_form_creates_user_referee_profile(self):
        """Test that valid form data creates a User, Referee, and ProfileReferee with generated username."""
        form = ProfileRefereeForm(data=self.valid_form_data)

        # Assert the form is valid
        self.assertTrue(form.is_valid(), msg=str(form.errors))

        # Save form and create related instances
        profile_referee = form.save(commit=True)
        user = profile_referee.user
        referee = profile_referee.referee

        # Assert the user was created with the expected username format
        expected_username = 'josef.sikela'
        self.assertEqual(user.username, expected_username)

        # Assert the referee was created
        referee_in_db = Referee.objects.get(licence_number='123456')
        self.assertEqual(referee_in_db.licence_type, self.licence_type)
        self.assertEqual(referee_in_db.city, self.city)

        # Assert the profile referee was created and linked correctly
        profile_referee_in_db = ProfileReferee.objects.get(user=user)
        self.assertEqual(profile_referee_in_db.referee, referee_in_db)

    def test_invalid_form_empty_fields(self):
        """Test that the form is invalid when required fields are missing."""
        form = ProfileRefereeForm(data=self.empty_form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)

    def test_clean_first_name_and_last_name(self):
        """Test that the clean methods strip and capitalize names."""
        form_data = self.valid_form_data.copy()
        form_data['first_name'] = '  jan  '
        form_data['last_name'] = '  novak  '

        form = ProfileRefereeForm(data=form_data)
        form.is_valid()  # Call is_valid to trigger clean methods

        self.assertEqual(form.cleaned_data['first_name'], 'Jan')
        self.assertEqual(form.cleaned_data['last_name'], 'Novak')

    def test_clean_rating_valid(self):
        """Test that rating is valid between 0 and 100."""
        form_data = self.valid_form_data.copy()
        form_data['rating'] = 75  # Valid rating
        form = ProfileRefereeForm(data=form_data)
        self.assertTrue(form.is_valid())  # Rating is valid

    def test_clean_rating_out_of_bounds(self):
        """Test that rating raises a validation error if out of bounds."""
        form_data = self.valid_form_data.copy()

        # Test with a rating less than 0
        form_data['rating'] = -1
        form = ProfileRefereeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('rating', form.errors)

        # Test with a rating greater than 100
        form_data['rating'] = 101
        form = ProfileRefereeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('rating', form.errors)

        # Test with a rating with more than one decimal place
        form_data['rating'] = 50.123
        form = ProfileRefereeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('rating', form.errors)