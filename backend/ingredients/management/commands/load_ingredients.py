from csv import reader
from django.core.management import BaseCommand

from ingredients.models import Ingredient


class Command(BaseCommand):
    help = "Loads data from ingredient.csv"

    def handle(self, *args, **options):
        print("Loading ingredient data")
        PATH_CSV = '/code/ingredients/management/commands/ingredients.csv'
        ingredients = []
        for row in reader(open(PATH_CSV)):
            ingredients.append(
                Ingredient(name=row[0], measurement_unit=row[1]))
        if Ingredient.objects.bulk_create(ingredients):
            print("Download was successful")
        else:
            print("Download failed")
