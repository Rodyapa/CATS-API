from cats.constants import DESCRIPTION_MAX_LENGTH, MAX_CAT_AGE, MAX_NAME
from cats.validators import TextValidator, TitleValidator
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

UserModel = get_user_model()


class Cat(models.Model):
    name = models.CharField(
        verbose_name='Кличка',
        max_length=MAX_NAME,
        null=False,
        blank=False,
        validators=(TitleValidator(), )
    )
    color = models.ForeignKey(
        verbose_name='Цвет',
        to='Color',
        on_delete=models.SET_NULL,
        related_name='cats',
        null=True,
        blank=True
    )
    age = models.PositiveSmallIntegerField(
        verbose_name='Возраст(полных месяцев)',
        null=False,
        blank=False,
        validators=(MaxValueValidator(MAX_CAT_AGE,
                                      'Еще не одно кошка не прожила больше '
                                      '30-ти лет'), )
    )
    description = models.TextField(
        verbose_name='Описание',
        max_length=DESCRIPTION_MAX_LENGTH,
        validators=(TextValidator(), )
    )
    breed = models.ForeignKey(
        verbose_name='Порода',
        to='Breed',
        on_delete=models.SET_NULL,
        related_name='cats',
        null=True,
        blank=True
    )
    owner = models.ForeignKey(
        verbose_name='Хозяин',
        to=UserModel,
        on_delete=models.CASCADE,
        related_name='cats'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['owner', 'name'],
                                    name='unique_owner_cat_name',
                                    violation_error_message=(
                                        'У пользователя уже есть кот с таким'
                                        'имнем.'
            ))
        ]
        ordering = ('name', )

    def __str__(self) -> str:
        return self.name


class Breed(models.Model):
    name = models.CharField(
        verbose_name='Название породы',
        max_length=MAX_NAME,
        unique=True,
        null=False,
        blank=False,
        validators=(TitleValidator(), )
    )

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs) -> None:
        self.name = self.name.lower()
        return super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                models.functions.Lower('name'), name='unique_lower_name')
        ]
        ordering = ('name', )


class Color(models.Model):
    name = models.CharField(
        verbose_name='Название цвета',
        max_length=MAX_NAME,
        unique=True,
        blank=False,
        null=False
    )

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs) -> None:
        self.name = self.name.lower()
        return super().save(*args, **kwargs)


class Score(models.Model):
    """Model for scores of cats."""
    cat = models.ForeignKey(
        Cat,
        on_delete=models.CASCADE,
        related_name='scores',
        verbose_name='Кот'
    )
    author = models.ForeignKey(
        verbose_name='Пользователь',
        to=UserModel,
        on_delete=models.CASCADE,
    )
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, message='Оценка должна быть не меньше 1'),
            MaxValueValidator(5, message='Оценка должна быть не более 5')],
        verbose_name='Оценка'
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценка'
        constraints = (
            models.UniqueConstraint(
                fields=['author', 'cat'],
                name='unique_author_title',
                violation_error_message=(
                    'У кота не может быть больше одной от одного пользователя'
                )
            ),
        )
