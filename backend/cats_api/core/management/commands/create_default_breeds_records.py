from django.core.management.base import BaseCommand
from core.csv_loaders import breeds_import


class Command(BaseCommand):
    def handle(self, *args, **options):
        breeds_import()
