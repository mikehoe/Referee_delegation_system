from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from accounts.forms import AddProfileRefereeForm
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
            'phone': '123456789',
            'name': 'Josef',
            'surname': 'Sikela',
        }
        self.empty_form_data = {}

    def test_valid_form_creates_user_referee_profile(self):
        """Test that valid form data creates a User, Referee, and ProfileReferee with generated username."""
        form = AddProfileRefereeForm(data=self.valid_form_data)

        # Assert the form is valid
        self.assertTrue(form.is_valid(), msg=str(form.errors))

        # Save form and create related instances
        referee, user = form.save(commit=True)

        # Assert the user was created with the expected username format
        expected_username = 'josef.sikela'  # Change this based on your username generation logic
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
        form = AddProfileRefereeForm(data=self.empty_form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)

    def test_clean_name_and_surname(self):
        """Test that the clean methods strip and capitalize names."""
        form_data = self.valid_form_data.copy()
        form_data['name'] = '  john  '  # Leading and trailing spaces
        form_data['surname'] = '  doe  '  # Leading and trailing spaces

        form = AddProfileRefereeForm(data=form_data)
        form.is_valid()  # Call is_valid to trigger clean methods

        self.assertEqual(form.cleaned_data['name'], 'John')
        self.assertEqual(form.cleaned_data['surname'], 'Doe')

    def test_clean_rating_valid(self):
        """Test that rating is valid between 0 and 100."""
        form_data = self.valid_form_data.copy()
        form_data['rating'] = 50  # Valid rating
        form = AddProfileRefereeForm(data=form_data)
        self.assertTrue(form.is_valid())  # Rating is valid

    def test_clean_rating_out_of_bounds(self):
        """Test that rating raises a validation error if out of bounds."""
        form_data = self.valid_form_data.copy()

        # Test with a rating less than 0
        form_data['rating'] = -1
        form = AddProfileRefereeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('rating', form.errors)

        # Test with a rating greater than 100
        form_data['rating'] = 101
        form = AddProfileRefereeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('rating', form.errors)

        # Test with a rating with more than one decimal place
        form_data['rating'] = 50.123
        form = AddProfileRefereeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('rating', form.errors)


class EditProfileRefereeFormTest(TestCase):
    """Test for EditProfileRefereeForm."""

    def setUp(self):
        self.licence_type = RefereeLicenceType.objects.create(name='B')
        self.city = City.objects.create(name='Hradec Králové')

        self.referee = Referee.objects.create(
            licence_number='654321',
            licence_type=self.licence_type,
            city=self.city
        )

        self.valid_form_data = {
            'email': 'jan.novak@example.com',
            'licence_number': '654321',
            'licence_type': self.licence_type.id,
            'city': self.city.id,
            'rating': 85,
            'phone': '987654321',
            'name': 'Jan',
            'surname': 'Novak',
        }
        self.empty_form_data = {}

    def test_valid_form_updates_referee_profile(self):
        """Test that valid form data updates the Referee and ProfileReferee instances."""
        form = AddProfileRefereeForm(data=self.valid_form_data, instance=self.referee)

        # Assert the form is valid
        self.assertTrue(form.is_valid(), msg=str(form.errors))

        # Save form and update related instances
        updated_referee, _ = form.save(commit=True)

        # Assert the referee fields were updated
        self.assertEqual(updated_referee.rating, 85)
        self.assertEqual(updated_referee.city, self.city)

    def test_invalid_form_empty_fields(self):
        """Test that the form is invalid when required fields are missing."""
        form = AddProfileRefereeForm(data=self.empty_form_data, instance=self.referee)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)

    def test_clean_name_and_surname(self):
        """Test that the clean methods strip and capitalize names."""
        form_data = self.valid_form_data.copy()
        form_data['name'] = '  jan  '  # Leading and trailing spaces
        form_data['surname'] = '  novak  '  # Leading and trailing spaces

        form = AddProfileRefereeForm(data=form_data, instance=self.referee)
        form.is_valid()  # Call is_valid to trigger clean methods

        self.assertEqual(form.cleaned_data['name'], 'Jan')
        self.assertEqual(form.cleaned_data['surname'], 'Novak')

    def test_clean_rating_valid(self):
        """Test that rating is valid between 0 and 100."""
        form_data = self.valid_form_data.copy()
        form_data['rating'] = 75  # Valid rating
        form = AddProfileRefereeForm(data=form_data, instance=self.referee)
        self.assertTrue(form.is_valid())  # Rating is valid

    def test_clean_rating_out_of_bounds(self):
        """Test that rating raises a validation error if out of bounds."""
        form_data = self.valid_form_data.copy()

        # Test with a rating less than 0
        form_data['rating'] = -1
        form = AddProfileRefereeForm(data=form_data, instance=self.referee)
        self.assertFalse(form.is_valid())
        self.assertIn('rating', form.errors)

        # Test with a rating greater than 100
        form_data['rating'] = 101
        form = AddProfileRefereeForm(data=form_data, instance=self.referee)
        self.assertFalse(form.is_valid())
        self.assertIn('rating', form.errors)

        # Test with a rating with more than one decimal place
        form_data['rating'] = 75.432
        form = AddProfileRefereeForm(data=form_data, instance=self.referee)
        self.assertFalse(form.is_valid())
        self.assertIn('rating', form.errors)

    def test_rating_unchanged(self):
        """Test that the form behaves correctly when the rating field is not modified."""
        form_data = self.valid_form_data.copy()

        # Do not include the 'rating' key in the form data to simulate an unchanged rating
        form_data.pop('rating', None)

        form = AddProfileRefereeForm(data=form_data, instance=self.referee)
        self.assertTrue(form.is_valid())  # Form should be valid even without the rating field

        # Save form and update related instances
        updated_referee, _ = form.save(commit=True)  # Extract the updated referee object from the tuple

        # Assert the referee fields were not changed
        self.assertEqual(updated_referee.rating, self.referee.rating)