from cats.constants import DESCRIPTION_MAX_LENGTH, MAX_CAT_AGE, MAX_NAME
from cats.validators import TextValidator
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator
from django.db import models

UserModel = get_user_model()


class Cat(models.Model):
    name = models.CharField(
        verbose_name='Кличка',
        max_length=MAX_NAME,
        null=False,
        blank=False
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

    def __str__(self) -> str:
        return self.name


class Breed(models.Model):
    name = models.CharField(
        verbose_name='Название породы',
        max_length=MAX_NAME,
        unique=True,
        null=False,
        blank=False
    )

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs) -> None:
        self.name = self.name.lower()
        return super().save(*args, **kwargs)


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
