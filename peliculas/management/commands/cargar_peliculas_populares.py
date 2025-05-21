from django.core.management.base import BaseCommand
from peliculas.models import Pelicula
from peliculas.tmdb import cargar_peliculas_populares, actualizar_creditos

class Command(BaseCommand):
    help = 'Carga las películas populares desde la API de TMDB'

    def handle(self, *args, **kwargs):
        cargar_peliculas_populares()

        for pelicula in Pelicula.objects.all():
            actualizar_creditos(pelicula)

        self.stdout.write(self.style.SUCCESS('Créditos actualizados correctamente.'))
        self.stdout.write(self.style.SUCCESS('Películas cargadas correctamente desde TMDB.'))
