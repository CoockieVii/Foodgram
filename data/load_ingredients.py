from csv import DictReader
from django.core.management import BaseCommand

from ingredients.models import Ingredient


class Command(BaseCommand):
    help = "Loads data from ingredient.csv"

    def handle(self, *args, **options):

        # Show this if the data already exist in the database
        if Ingredient.objects.exists():
            print('Запись уже добавлена.')

        # Show this before loading the data into the database
        print("Loading ingredient data")

        # Code to load the data into database
        for row in DictReader(open('./ingredients.csv')):
            ingredient = Ingredient(name=row['name'],
                                    measurement_unit=row['measurement_unit'])
            ingredient.save()
