from django.conf import settings
import requests

API_KEY = settings.TMDB_API_KEY
API_BASE = "https://api.themoviedb.org/3"
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

# Palabras clave a excluir en títulos y personajes
EXCLUDE_KEYWORDS = [
    # Genéricos
    "show", "late night", "talk", "interview", "special", "documental", "featurette",
    "behind the scenes", "making of", "short", "presenta", "galas", "homenaje",
    "oscars", "oscar", "academy awards", "emmys", "emmy", "bafta", "golden globes",
    "globos de oro", "critics choice", "mtv", "red carpet", "alfombra roja",
    "cannes", "venice", "berlinale", "ceremony", "premios", "award",

    # Específicos anteriores
    "watch what happens live", "real time with bill maher",
    "diners, drive-ins and dives", "live with kelly and mark",
    "el programa de kelly clarkson", "the kelly clarkson show",
    "honest trailers",

    # Nuevos específicos
    "the view", "off camera", "conan", "saturday night live", "snl",
    "last week tonight", "bbc", "play for today", "wwe", "raw", "today"
]


def get_language(request):
    lang = request.session.get('django_language', 'es')
    return 'es-ES' if lang == 'es' else 'en-US'


def buscar_peliculas(request, consulta):
    url = f"{API_BASE}/search/multi"
    params = {
        'api_key': API_KEY,
        'query': consulta,
        'language': get_language(request),
        'include_adult': False
    }
    r = requests.get(url, params=params)
    if r.status_code != 200:
        return []
    resultados = []
    for item in r.json().get('results', []):
        if item.get('media_type') not in ('movie', 'tv'):
            continue
        poster = item.get('poster_path')
        resultados.append({
            'id': item['id'],
            'titulo': item.get('title') or item.get('name'),
            'fecha': item.get('release_date') or item.get('first_air_date'),
            'poster_url': f"{IMAGE_BASE_URL}{poster}" if poster else '',
            'tipo': item['media_type']
        })
    return resultados


def obtener_reparto(request, tmdb_id, tipo='movie'):
    creds = requests.get(f"{API_BASE}/{tipo}/{tmdb_id}/credits", params={
        'api_key': API_KEY,
        'language': get_language(request)
    }).json()

    # Director
    d = None
    if tipo == 'movie':
        d = next((c for c in creds.get('crew', []) if c.get('job') == 'Director'), None)
    else:
        info = requests.get(f"{API_BASE}/{tipo}/{tmdb_id}", params={
            'api_key': API_KEY,
            'language': get_language(request)
        }).json()
        d = (info.get('created_by') or [{}])[0]

    director = None
    if d and d.get('id'):
        profile = d.get('profile_path')
        director = {
            'id': d['id'],
            'nombre': d.get('name'),
            'foto': f"{IMAGE_BASE_URL}{profile}" if profile else ''
        }

    # Actores principales (hasta 5)
    actores = []
    for a in creds.get('cast', [])[:5]:
        profile = a.get('profile_path')
        actores.append({
            'id': a['id'],
            'nombre': a.get('name'),
            'foto': f"{IMAGE_BASE_URL}{profile}" if profile else ''
        })

    return {'director': director, 'actores': actores}


def obtener_detalles_tmdb(request, tmdb_id, tipo='movie'):
    url = f"{API_BASE}/{tipo}/{tmdb_id}"
    params = {
        'api_key': API_KEY,
        'language': get_language(request)
    }
    r = requests.get(url, params=params)
    if r.status_code != 200:
        return {}

    d = r.json()
    poster = d.get('poster_path')
    detalles = {
        'titulo':        d.get('title') or d.get('name'),
        'descripcion':   d.get('overview', 'No disponible.'),
        'poster_url':    f"{IMAGE_BASE_URL}{poster}" if poster else '',
        'fecha_estreno': d.get('release_date') if tipo == 'movie'
                          else d.get('first_air_date'),
        'generos':       [g['name'] for g in d.get('genres', []) if g.get('name')],
        'rating':        d.get('vote_average'),
        'votos':         d.get('vote_count')
    }

    if d.get('budget'):
        detalles['presupuesto'] = d['budget']
    if d.get('revenue'):
        detalles['recaudacion'] = d['revenue']
    if d.get('runtime'):
        detalles['duracion'] = d['runtime']
    if d.get('episode_run_time'):
        detalles['duracion_serie'] = d['episode_run_time'][0]
    if d.get('tagline'):
        detalles['frase'] = d['tagline']

    return detalles


def obtener_detalles_persona(request, person_id):
    lang = get_language(request)
    r = requests.get(f"{API_BASE}/person/{person_id}", params={
        'api_key': API_KEY,
        'language': lang
    })
    if r.status_code != 200:
        return {}
    d = r.json()

    # Fallback biografía en inglés si no hay en ES
    bio = d.get('biography', '').strip()
    if not bio:
        r2 = requests.get(f"{API_BASE}/person/{person_id}", params={
            'api_key': API_KEY,
            'language': 'en-US'
        })
        if r2.status_code == 200:
            bio = r2.json().get('biography', '').strip()

    profile = d.get('profile_path')
    persona = {
        "id":                d['id'],
        "nombre":            d.get('name'),
        "foto":              f"{IMAGE_BASE_URL}{profile}" if profile else '',
        "cumpleanos":        d.get('birthday'),
        "lugar_nacimiento":  d.get('place_of_birth'),
        "biografia":         bio or 'No hay biografía disponible.',
        "actuaciones":       [],
        "peliculas_dirigidas": []
    }

    def es_relevante(titulo):
        return titulo and not any(p in titulo.lower() for p in EXCLUDE_KEYWORDS)

    # Créditos combinados
    r2 = requests.get(f"{API_BASE}/person/{person_id}/combined_credits", params={
        'api_key': API_KEY,
        'language': lang
    })
    if r2.status_code != 200:
        return persona
    data = r2.json()

    # Actuaciones (cast)
    for item in data.get('cast', []):
        character = (item.get('character') or '').lower()
        titulo = item.get('title') or item.get('name') or ''
        if 'cameo' in character:
            continue
        if item.get('poster_path') and item.get('media_type') in ("movie", "tv") and es_relevante(titulo):
            persona["actuaciones"].append({
                "id":          item["id"],
                "titulo":      titulo,
                "fecha":       item.get("release_date") or item.get("first_air_date"),
                "poster_url":  f"{IMAGE_BASE_URL}{item['poster_path']}",
                "tipo":        item["media_type"],
                "popularidad": item.get("popularity", 0)
            })

    # Películas dirigidas
    for item in data.get('crew', []):
        if item.get("job") == "Director":
            titulo = item.get("title") or item.get("name") or ""
            if item.get('poster_path') and es_relevante(titulo):
                persona["peliculas_dirigidas"].append({
                    "id":          item["id"],
                    "titulo":      titulo,
                    "fecha":       item.get("release_date") or item.get("first_air_date"),
                    "poster_url":  f"{IMAGE_BASE_URL}{item['poster_path']}",
                    "tipo":        item["media_type"],
                    "popularidad": item.get("popularity", 0)
                })

    persona["known_for_department"] = d.get("known_for_department")
    return persona


def obtener_credits_persona(request, person_id):
    r = requests.get(f"{API_BASE}/person/{person_id}/combined_credits", params={
        "api_key": API_KEY,
        "language": get_language(request)
    })
    data = r.json()

    actuaciones = []
    dirigidas = []

    def es_relevante(titulo):
        return titulo and not any(p in titulo.lower() for p in EXCLUDE_KEYWORDS)

    for item in data.get('cast', []):
        character = (item.get('character') or '').lower()
        titulo = item.get("title") or item.get("name") or ""
        if (
            item.get("poster_path") and
            item.get("popularity", 0) > 3 and
            item.get("media_type") in ("movie", "tv") and
            es_relevante(titulo) and
            "cameo" not in character
        ):
            actuaciones.append({
                "id":          item["id"],
                "titulo":      titulo,
                "fecha":       item.get("release_date") or item.get("first_air_date"),
                "poster_url":  f"{IMAGE_BASE_URL}{item['poster_path']}",
                "tipo":        item["media_type"],
                "popularidad": item.get("popularity", 0)
            })

    for item in data.get('crew', []):
        if (
            item.get("job") == "Director" and
            item.get("poster_path") and
            item.get("popularity", 0) > 3
        ):
            titulo = item.get("title") or item.get("name")
            if es_relevante(titulo):
                dirigidas.append({
                    "id":          item["id"],
                    "titulo":      titulo,
                    "fecha":       item.get("release_date") or item.get("first_air_date"),
                    "poster_url":  f"{IMAGE_BASE_URL}{item['poster_path']}",
                    "tipo":        item["media_type"],
                    "popularidad": item.get("popularity", 0)
                })

    actuaciones.sort(key=lambda x: x['popularidad'], reverse=True)
    dirigidas.sort(key=lambda x: x['popularidad'], reverse=True)

    return {
        "actuaciones": actuaciones[:20],
        "peliculas_dirigidas": dirigidas[:20],
    }


def obtener_populares(request):
    url = f"{API_BASE}/trending/all/week"
    params = {
        'api_key': API_KEY,
        'language': get_language(request)
    }
    r = requests.get(url, params=params)
    if r.status_code != 200:
        return []
    resultados = []
    for item in r.json().get('results', []):
        if item.get('media_type') not in ('movie', 'tv'):
            continue
        poster = item.get('poster_path')
        resultados.append({
            'id':         item['id'],
            'titulo':     item.get('title') or item.get('name'),
            'fecha':      item.get('release_date') or item.get('first_air_date'),
            'poster_url': f"{IMAGE_BASE_URL}{poster}" if poster else '',
            'tipo':       item['media_type']
        })
    return resultados


def obtener_por_genero(request, slug, pages=3, tipo='movie'):
    results = []
    genre_id = settings.TMDB_GENRES.get(slug)
    if not genre_id:
        return results

    url = f"{API_BASE}/discover/{tipo}"
    for page in range(1, pages + 1):
        params = {
            'api_key':    API_KEY,
            'language':   get_language(request),
            'with_genres': genre_id,
            'sort_by':    'popularity.desc',
            'page':       page,
        }
        resp = requests.get(url, params=params)
        if resp.status_code != 200:
            break
        for m in resp.json().get('results', []):
            poster = m.get('poster_path')
            results.append({
                'id':         m['id'],
                'titulo':     m.get('title') or m.get('name'),
                'poster_url': f"{IMAGE_BASE_URL}{poster}" if poster else '',
                'tipo':       tipo,
                'fecha':      m.get('release_date') or m.get('first_air_date')
            })
    return results


def obtener_top_rated(request, tipo='movie', pages=3):
    url = f"{API_BASE}/{tipo}/top_rated"
    results = []
    for page in range(1, pages+1):
        r = requests.get(url, params={
            'api_key':  API_KEY,
            'language': get_language(request),
            'page':     page
        })
        if r.status_code != 200:
            break
        for m in r.json().get('results', []):
            poster = m.get('poster_path')
            results.append({
                'id':         m['id'],
                'titulo':     m.get('title') or m.get('name'),
                'poster_url': f"{IMAGE_BASE_URL}{poster}" if poster else '',
                'tipo':       tipo,
                'fecha':      m.get('release_date') or m.get('first_air_date')
            })
    return results


def obtener_estrenos_proximos(request, pages=3):
    url = f"{API_BASE}/movie/upcoming"
    results = []
    for page in range(1, pages+1):
        resp = requests.get(url, params={
            'api_key':  API_KEY,
            'language': get_language(request),
            'page':     page
        })
        if resp.status_code != 200:
            break
        for m in resp.json().get('results', []):
            poster = m.get('poster_path')
            results.append({
                'id':         m['id'],
                'titulo':     m.get('title'),
                'poster_url': f"{IMAGE_BASE_URL}{poster}" if poster else '',
                'tipo':       'movie',
                'fecha':      m.get('release_date')
            })
    return results
