import csv
import os

from cats.models import Color, Cat, Breed
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

UserModel = get_user_model()

'''Load test data. Can be used for Local Development.'''


def users_import(row):
    if not UserModel.objects.filter(username=row[0]):
        UserModel.objects.create_user(
            username=row[0],
            email=row[1],
            password=row[2]
        )


def colors_import(row):
    Color.objects.get_or_create(
        name=row[0].lower(),
    )


def breeds_import(row):
    Breed.objects.get_or_create(
        name=row[0].lower(),
    )


def cats_import(row):
    owner = UserModel.objects.get(id=row[5])
    breed = Breed.objects.get(id=row[4])
    color = Color.objects.get(id=row[5])
    Cat.objects.get_or_create(
        name=row[0],
        age=row[1],
        description=row[2],
        color=color,
        breed=breed,
        owner=owner,
    )


action = {
    'users.csv': users_import,
    'colors.csv': colors_import,  # Must to be after user_import
    'breeds.csv': breeds_import,  # Must to be after user_import
    'cats.csv': cats_import,  # Must to be after colors and breeds import
}


class Command(BaseCommand):
    def handle(self, *args, **options):
        path = os.path.join(settings.BASE_DIR, 'tests/test_data/')
        for key in action.keys():
            with open(path + key, 'r', encoding='utf-8') as csv_file:
                reader = csv.reader(csv_file)
                for row in reader:
                    action[key](row)
