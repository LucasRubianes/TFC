# peliculas/urls.py
from django.urls import path
from . import views

app_name = 'peliculas'

urlpatterns = [
    # Home y búsqueda
    path('', views.lista_peliculas, name='lista_peliculas'),
    path('buscar/', views.buscar_pelicula, name='buscar_pelicula'),

    # Detalle y rating
    path('detalle/<str:tipo>/<int:tmdb_id>/',
         views.detalle_pelicula_tmdb, name='detalle_pelicula_tmdb'),
    path('rate_movie/<int:tmdb_id>/',
         views.rate_movie,           name='rate_movie'),

    # Otras vistas
    path('persona/<int:persona_id>/', views.detalle_persona, name='detalle_persona'),
    path('genero/<slug:slug>/',      views.genero,          name='genero'),
    path('coleccion/<slug:slug>/',   views.coleccion,       name='coleccion'),
]
