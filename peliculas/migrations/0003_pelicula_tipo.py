# Generated by Django 5.2.1 on 2025-05-15 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('peliculas', '0002_actor_pelicula_director_pelicula_actores'),
    ]

    operations = [
        migrations.AddField(
            model_name='pelicula',
            name='tipo',
            field=models.CharField(choices=[('movie', 'Película'), ('tv', 'Serie')], default='movie', max_length=10),
        ),
    ]
