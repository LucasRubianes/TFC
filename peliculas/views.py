from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseNotAllowed
from .models import Rating  # tu modelo de valoraciones


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings

from .tmdb import (
    buscar_peliculas,
    obtener_populares,
    obtener_por_genero,
    obtener_detalles_tmdb,
    obtener_reparto,
    obtener_detalles_persona,
    obtener_top_rated,
    obtener_estrenos_proximos,
)
from django.http import JsonResponse
from django.views.decorators.http import require_POST

# en peliculas/views.py

from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Rating

from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Rating
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Rating

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .models import Rating

# películas/views.py
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponseNotAllowed
from .models import Rating

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Rating

@require_POST
@login_required
def rate_movie(request, tmdb_id):
    try:
        score = int(request.POST.get('score', 0))
        if score < 1 or score > 5:
            raise ValueError
    except ValueError:
        return JsonResponse({'error': 'Invalid score'}, status=400)

    # update or create
    rating, _ = Rating.objects.update_or_create(
        user=request.user,
        tmdb_id=tmdb_id,
        defaults={'score': score}
    )

    return JsonResponse({'score': rating.score})

def lista_peliculas(request):
    tendencias = obtener_populares(request)
    secciones = []
    preview_pages = getattr(settings, 'TMDB_PREVIEW_PAGES', 1)
    for slug, genre_id in settings.TMDB_GENRES.items():
        nombre = slug.replace('_', ' ').capitalize()
        peliculas = obtener_por_genero(request, slug, pages=preview_pages)
        secciones.append((nombre, slug, peliculas))

    colecciones = [
        ('Top Rated',         'top_rated',  obtener_top_rated(request, pages=preview_pages)),
        ('Próximos Estrenos', 'upcoming',   obtener_estrenos_proximos(request, pages=preview_pages)),
    ]

    return render(request, 'index.html', {
        'tendencias':  tendencias,
        'secciones':   secciones,
        'colecciones': colecciones,
    })


def buscar_pelicula(request):
    consulta = request.GET.get('q', '').strip()
    resultados = buscar_peliculas(request, consulta) if consulta else []
    return render(request, 'buscar.html', {
        'consulta': consulta,
        'resultados_tmdb': resultados
    })

from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .models import Rating  # asume que creaste el modelo Rating


# peliculas/views.py

from django.shortcuts import render
from django.http import Http404
from django.db.models import Avg

from .tmdb import obtener_detalles_tmdb, obtener_reparto
from .models import Rating
from django.http import Http404
from django.shortcuts import render
from .tmdb import obtener_detalles_tmdb, obtener_reparto
from .models import Rating

def detalle_pelicula_tmdb(request, tipo, tmdb_id):
    # 1) Llamadas al API siempre, para todos los usuarios
    detalles = obtener_detalles_tmdb(request, tmdb_id, tipo=tipo)
    if not detalles:
        raise Http404("No se encontró esa película o serie.")

    reparto = obtener_reparto(request, tmdb_id, tipo=tipo)
    generos = detalles.get('generos', [])

    # 2) Valoración del usuario (persistida en BD si está logueado, o en session si es anónimo)
    if request.user.is_authenticated:
        # usamos modelo Rating
        try:
            user_rating = Rating.objects.get(user=request.user, tmdb_id=tmdb_id).score
        except Rating.DoesNotExist:
            user_rating = 0
    else:
        # recogemos de session (te quedaría si ya votó antes)
        user_rating = request.session.get(f'rating_{tmdb_id}', 0)

    # 3) Una única llamada a render con todos los contextos
    return render(request, 'detalle_pelicula.html', {
        'detalles':    detalles,
        'director':    reparto.get('director'),
        'actores':     reparto.get('actores', []),
        'generos':     generos,
        'tmdb_id':     tmdb_id,
        'star_range':  range(1, 6),
        'user_rating': user_rating,
    })
 # 1) Trailers/videos
    videos = []
    vresp = requests.get(
        f"https://api.themoviedb.org/3/{tipo}/{tmdb_id}/videos",
        params={'api_key': settings.TMDB_API_KEY, 'language': 'es-ES'}
    ).json()
    # filtramos solo trailers de YouTube
    for v in vresp.get('results', []):
        if v['site'].lower() == 'youtube' and v['type'].lower() == 'trailer':
            videos.append(v)

    # 2) Imágenes destacadas (backdrops)
    images = []
    iresp = requests.get(
        f"https://api.themoviedb.org/3/{tipo}/{tmdb_id}/images",
        params={'api_key': settings.TMDB_API_KEY}
    ).json()
    for img in iresp.get('backdrops', [])[:8]:  # por ejemplo, 8 imágenes
        images.append(img['file_path'])

    context = {
        # … tu contexto actual …
        'videos': videos,
        'backdrops': images,
    }
    return render(request, 'detalle_pelicula.html', context)

def detalle_persona(request, persona_id):
    data = obtener_detalles_persona(request, persona_id)
    if not data:
        raise Http404("Persona no encontrada.")

    # Parsear cumpleaños y lugar
    cumple_str = data.get("cumpleanos") or data.get("birthday") or ''
    try:
        cumple = datetime.strptime(cumple_str, "%Y-%m-%d") if cumple_str else None
    except ValueError:
        cumple = None
    lugar_nac = data.get("lugar_nacimiento") or data.get("place_of_birth") or ''

    actuaciones = data.get("actuaciones", [])
    dirigidas   = data.get("peliculas_dirigidas", [])
    dept        = (data.get("known_for_department") or "").lower()

    # Construcción del dict que pasamos al template
    persona = {
        "nombre":              data.get("nombre") or data.get("name", ''),
        "foto":                data.get("foto", ''),
        "biografia":           data.get("biografia") or data.get("biography", ''),
        "cumpleanos":          cumple,
        "lugar_nacimiento":    lugar_nac,
        "actuaciones":         actuaciones,
        "peliculas_dirigidas": dirigidas,
    }

    # Lógica _solo_ por departamento principal
    if dept == "directing":
        mostrar_dirigidas   = True
        mostrar_actuaciones = False
    else:
        # actors y todo lo demás caen aquí
        mostrar_actuaciones = bool(actuaciones)
        mostrar_dirigidas   = False

    return render(request, "detalle_persona.html", {
        "persona":             persona,
        "mostrar_dirigidas":   mostrar_dirigidas,
        "mostrar_actuaciones": mostrar_actuaciones,
    })


def genero(request, slug):
    detail_pages = getattr(settings, 'TMDB_DETAIL_PAGES', 5)
    lista = obtener_por_genero(request, slug, pages=detail_pages, tipo='movie')
    if not lista:
        raise Http404("Género no encontrado.")

    per_page = getattr(settings, 'TMDB_ITEMS_PER_PAGE', 24)
    paginator = Paginator(lista, per_page)
    page_num = request.GET.get('page', 1)
    try:
        page_obj = paginator.page(page_num)
    except (PageNotAnInteger, EmptyPage):
        page_obj = paginator.page(1)

    nombre = slug.replace('_', ' ').capitalize()
    return render(request, 'genero.html', {
        'nombre':    nombre,
        'page_obj':  page_obj,
        'paginator': paginator,
    })


def coleccion(request, slug):
    detail_pages = getattr(settings, 'TMDB_DETAIL_PAGES', 5)
    if slug == 'top_rated':
        lista, nombre = obtener_top_rated(request, pages=detail_pages), 'Top Rated'
    elif slug == 'upcoming':
        lista, nombre = obtener_estrenos_proximos(request, pages=detail_pages), 'Próximos Estrenos'
    else:
        raise Http404("Colección no encontrada.")

    per_page = getattr(settings, 'TMDB_ITEMS_PER_PAGE', 24)
    paginator = Paginator(lista, per_page)
    page_num = request.GET.get('page', 1)
    try:
        page_obj = paginator.page(page_num)
    except (PageNotAnInteger, EmptyPage):
        page_obj = paginator.page(1)

    return render(request, 'genero.html', {
        'nombre':    nombre,
        'page_obj':  page_obj,
        'paginator': paginator,
    })



@login_required
def rate_movie(request, tmdb_id):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    score = int(request.POST.get('score', 0))
    if score < 1 or score > 5:
        return JsonResponse({'error': 'Puntuación inválida'}, status=400)
    # Guarda o actualiza la valoración
    rating, created = Rating.objects.update_or_create(
        user=request.user,
        tmdb_id=tmdb_id,
        defaults={'score': score}
    )
    return JsonResponse({'score': rating.score})
from django.http import JsonResponse
from django.views.decorators.http import require_GET
import requests
from django.conf import settings

@require_GET
def suggest_titles(request):
    q = request.GET.get('q', '').strip()
    if not q:
        return JsonResponse({'results': []})

    resp = requests.get(
        'https://api.themoviedb.org/3/search/movie',
        params={'api_key': settings.TMDB_API_KEY, 'query': q, 'page': 1, 'include_adult': False}
    )
    data = resp.json().get('results', [])[:5]

    results = [{'id': m['id'], 'title': m['title']} for m in data]
    return JsonResponse({'results': results})
