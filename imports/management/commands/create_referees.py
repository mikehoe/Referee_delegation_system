import csv
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from accounts.models import ProfileReferee
from referees.models import Referee


class Command(BaseCommand):
    help = 'Create referees from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the CSV file')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        with open(file_path, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                username = row['username']
                password = row['password']
                first_name = row['first_name']
                last_name = row['last_name']
                email = row['email']
                is_superuser = row['is_superuser']
                is_staff = row['is_staff']
                is_active = row['is_active']
                date_joined = row['date_joined']
                # last_login = row['last_login']

                licence_number = row['licence_number']
                licence_type_id = row['licence_type_id']
                city_id = row['city_id']
                rating = row['rating']
                phone = row['phone']

                user, user_created = User.objects.get_or_create(
                    username=username, first_name=first_name, last_name=last_name, email=email,
                    is_superuser=is_superuser, is_staff=is_staff, is_active=is_active, date_joined=date_joined, )
                # last_login=last_login)
                if user_created:
                    user.set_password(password)
                    user.save()
                    self.stdout.write(self.style.SUCCESS(f'Successfully created user: {username}'))
                else:
                    self.stdout.write(self.style.WARNING(f'User {username} already exists'))

                referee, referee_created = Referee.objects.get_or_create(
                    licence_number=licence_number, licence_type_id=licence_type_id, city_id=city_id, rating=rating,
                    phone=phone)
                if referee_created:
                    self.stdout.write(self.style.SUCCESS(f'Successfully created referee: {username}'))
                else:
                    self.stdout.write(self.style.WARNING(f'Referee {username} already exists'))

                profile_referee, profile_referee_created = ProfileReferee.objects.get_or_create(
                    user_id=user.id, referee_id=referee.id)
                if profile_referee_created:
                    self.stdout.write(self.style.SUCCESS(f'Successfully created profile_referee: {username}'))
                else:
                    self.stdout.write(self.style.WARNING(f'Profile_referee {username} already exists'))
