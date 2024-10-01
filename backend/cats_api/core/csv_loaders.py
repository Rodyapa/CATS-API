
import csv
import os

from cats.models import Breed, Color
from django.conf import settings
from django.contrib.auth import get_user_model

UserModel = get_user_model()

# Data that used for project to start adequately
DEFAULT_DATA_FOLDER = os.path.join(settings.BASE_DIR, 'default_data/')


def import_data(model, csv_file, *fields):
    path = os.path.join(DEFAULT_DATA_FOLDER, csv_file)

    with open(path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            data = {field: row[i] for i, field in enumerate(fields)}
            model.objects.get_or_create(**data)


def breeds_import():
    csv_file = 'breeds.csv'
    path = os.path.join(DEFAULT_DATA_FOLDER, csv_file)

    with open(path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            name = row[0]
            Breed.objects.get_or_create(name=name.lower())


def colors_import():
    csv_file = 'colors.csv'
    path = os.path.join(DEFAULT_DATA_FOLDER, csv_file)

    with open(path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            name = row[0]
            Color.objects.get_or_create(name=name.lower())
