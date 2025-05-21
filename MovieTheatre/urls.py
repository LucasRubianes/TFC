# MovieTheatre/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Rutas de autenticación (login/logout)
    path('accounts/', include('django.contrib.auth.urls')),

    # URLs de la app "peliculas"
    path('', include('peliculas.urls', namespace='peliculas')),
]
