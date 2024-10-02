from django.core.management.base import BaseCommand
from core.csv_loaders import colors_import


class Command(BaseCommand):
    def handle(self, *args, **options):
        colors_import()
