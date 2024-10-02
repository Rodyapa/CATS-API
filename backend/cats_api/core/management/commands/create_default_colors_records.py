from core.csv_loaders import colors_import
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        colors_import()
