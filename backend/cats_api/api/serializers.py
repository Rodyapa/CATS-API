from api.validators import OnlyOneScorePerCatValidator
from cats.models import Breed, Cat, Score
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
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Cat
        fields = ["id", "name", "age", "breed",
                  "color", "description", "owner",
                  "rating"]


class ScoreSerializer(serializers.ModelSerializer):
    """Serializer for Scores."""
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Score
        fields = [
            'id',
            'score',
            'author',
            'pub_date',
        ]
        read_only_fields = ['id', 'author', 'pub_date']
        validators = [
            OnlyOneScorePerCatValidator(),
        ]
