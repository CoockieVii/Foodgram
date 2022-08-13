from csv import reader

from django.core.management import BaseCommand

from ingredients.models import Ingredient
from tags.models import Tag


class Command(BaseCommand):
    help = "Loads data from ingredient.csv"

    def handle(self, *args, **options):
        print("Start loading")

        print("*ingredients")
        # PATH_CSV = '/code/core/management/commands/ingredients.csv'
        PATH_CSV = 'core/management/commands/ingredients.csv'
        ingredients = []
        for row in reader(open(PATH_CSV)):
            ingredients.append(
                Ingredient(name=row[0], measurement_unit=row[1]))
        Ingredient.objects.bulk_create(ingredients)

        print("**tags")
        # PATH_CSV = '/code/core/management/commands/tags.csv'
        PATH_CSV = 'core/management/commands/tags.csv'
        tags = []
        for row in reader(open(PATH_CSV)):
            tags.append(
                Tag(name=row[0], color=row[1], slug=row[2]))
        Tag.objects.bulk_create(tags)
