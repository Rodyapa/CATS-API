from cats.models import Breed
from django.conf import settings
from rest_framework import serializers


class BreedSerializer(serializers.ModelSerializer):
    """Serializer for Cats model instances."""
    class Meta:
        model = Breed
        fields = '__all__'

    def validate_name(self, value):
        if (settings.DATABASES['default']['ENGINE'] ==
                'django.db.backends.sqlite3'):
            # Only apply this validation for SQLite (local development)
            if Breed.objects.filter(name__iexact=value.lower()).exists():
                raise serializers.ValidationError(
                    "A breed with this name already "
                    "exists (case-insensitive).")
        return value
