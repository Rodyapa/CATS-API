# Generated by Django 5.1.1 on 2024-10-04 10:53

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cats', '0003_alter_breed_options'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cat',
            options={'ordering': ('name',)},
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1, message='Оценка должна быть не меньше 1'), django.core.validators.MaxValueValidator(5, message='Оценка должна быть не более 5')], verbose_name='Оценка')),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
                ('cat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scores', to='cats.cat', verbose_name='Кот')),
            ],
            options={
                'verbose_name': 'Оценка',
                'verbose_name_plural': 'Оценка',
                'constraints': [models.UniqueConstraint(fields=('author', 'cat'), name='unique_author_title', violation_error_message='У кота не может быть больше одной от одного пользователя')],
            },
        ),
    ]
