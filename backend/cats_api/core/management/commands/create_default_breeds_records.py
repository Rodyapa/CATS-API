from core.csv_loaders import breeds_import
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        breeds_import()
