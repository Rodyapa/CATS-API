from cats.models import Score
from django.core.exceptions import ValidationError


class OnlyOneScorePerCatValidator:
    """
    Validator for Score instance.
    Check that user can not leave more than
    one score for a single cat instance.
    """

    requires_context = True

    def __call__(self, attrs, serializer):
        method = serializer.context['request'].method
        if method != 'POST':
            return serializer
        current_user = serializer.context['request'].user
        cat_id = serializer.context['cat_id']
        if current_user.is_authenticated and Score.objects.filter(
            cat=cat_id,
            author=current_user
        ).exists():
            raise ValidationError('Sorry you cannot leave '
                                  'more than one score for a single cat')
