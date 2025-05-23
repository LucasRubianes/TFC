# Generated by Django 5.2.1 on 2025-05-21 08:07

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('peliculas', '0005_alter_rating_options_rating_created_at_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rating',
            options={'verbose_name': 'Valoración', 'verbose_name_plural': 'Valoraciones'},
        ),
        migrations.RemoveIndex(
            model_name='rating',
            name='peliculas_r_user_id_6524b8_idx',
        ),
        migrations.AlterField(
            model_name='rating',
            name='score',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.AlterField(
            model_name='rating',
            name='tmdb_id',
            field=models.IntegerField(),
        ),
    ]
