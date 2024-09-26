import csv
from django.core.management.base import BaseCommand

from competitions.models import City


class Command(BaseCommand):
    help = 'Create cieties from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the CSV file')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        with open(file_path, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                name = row['name']
                city, created = City.objects.get_or_create(name=name)
                if created:
                    city.save()
                    self.stdout.write(self.style.SUCCESS(f'Successfully created city: {name}'))
                else:
                    self.stdout.write(self.style.WARNING(f'City {name} already exists'))
