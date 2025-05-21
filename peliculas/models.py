
from django.db import models
from django.conf import settings

class Rating(models.Model):
    user      = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  on_delete=models.CASCADE,
                                  related_name='ratings')
    tmdb_id   = models.IntegerField()
    score     = models.PositiveSmallIntegerField()  # 1–5
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'tmdb_id')
        ordering = ['-updated_at']

    def __str__(self):
        return f'{self.user} · #{self.tmdb_id} = {self.score}'


class Actor(models.Model):
    nombre = models.CharField(max_length=255)
    foto_url = models.URLField(blank=True)

    def __str__(self):
        return self.nombre

class Pelicula(models.Model):
    TIPO_CHOICES = [
        ('movie', 'Película'),
        ('tv', 'Serie'),
    ]

    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    fecha_estreno = models.DateField(null=True, blank=True)
    poster_url = models.URLField(blank=True)
    tmdb_id = models.IntegerField(unique=True)
    director = models.CharField(max_length=255, blank=True)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='movie')
    actores = models.ManyToManyField(Actor, blank=True)

    def __str__(self):
        return self.titulo



from django.db import models
from django.conf import settings


