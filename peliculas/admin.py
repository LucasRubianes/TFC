from django.contrib import admin
from .models import Pelicula

class PeliculaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha_estreno', 'poster_url', 'tmdb_id')  # Asegúrate de que estos campos existan en tu modelo
from django.contrib import admin
from .models import Rating

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('user','tmdb_id','score')
    list_filter  = ('score',)
    search_fields = ('user__username','tmdb_id')

admin.site.register(Pelicula, PeliculaAdmin)
