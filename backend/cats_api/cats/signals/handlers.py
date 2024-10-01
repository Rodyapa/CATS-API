from core.csv_loaders import breeds_import, colors_import
from django.db.models.signals import post_migrate
from django.dispatch import receiver


@receiver(post_migrate)
def create_default_breeds_records(sender, **kwargs):
    """
    Creates (if not created) database entries for standard breeds
    for cats instances.
    After every migration.
    """
    breeds_import()


@receiver(post_migrate)
def create_default_colors_records(sender, **kwargs):
    """
    Creates (if not created) database entries for standard colors
    for cats insctances.
    After every migration.
    """
    colors_import()
