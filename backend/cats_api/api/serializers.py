from cats.models import Breed, Cat
from django.conf import settings
from rest_framework import serializers


class BreedSerializer(serializers.ModelSerializer):
    """Serializer for Breed model instances."""
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


class CatSerializer(serializers.ModelSerializer):
    """Serializer for Cat model instances."""
    breed = serializers.StringRelatedField()
    color = serializers.StringRelatedField()
    owner = serializers.StringRelatedField()

    class Meta:
        model = Cat
        fields = '__all__'
