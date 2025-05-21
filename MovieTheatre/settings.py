import os
from pathlib import Path
from decouple import config
from django.utils.translation import gettext_lazy as _

# ———————————————— BASE ——————————————————
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY', default='reemplaza-esto-en-tu-.env')
DEBUG      = config('DEBUG',      cast=bool, default=True)
ALLOWED_HOSTS = []

# ————————————— INSTALLED APPS ——————————————
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.humanize',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'peliculas',
    'widget_tweaks',
]

# ————————————— MIDDLEWARE ———————————————
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # 'whitenoise.middleware.WhiteNoiseMiddleware',  # producción
    'django.contrib.sessions.middleware.SessionMiddleware',

    # para internacionalización de URLs
    'django.middleware.locale.LocaleMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'MovieTheatre.urls'

# ————————————— TEMPLATES ————————————————
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # carpeta global para tus propias plantillas
        'DIRS': [
            BASE_DIR / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',   # ⚠ necesario para auth y next
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'MovieTheatre.wsgi.application'

# ————————————— DATABASES ————————————————
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ————————————— PASSWORD VALIDATORS —————————
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# ———————————— INTERNATIONALIZATION ——————————
LANGUAGE_CODE = 'es-es'
TIME_ZONE     = 'UTC'
USE_I18N      = True
USE_L10N      = True
USE_TZ        = True

LANGUAGES = [
    ('es', _('Español')),
    ('en', _('English')),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

# ————————————— STATIC FILES ——————————————
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'peliculas' / 'static',
]
STATIC_ROOT = BASE_DIR / 'staticfiles'
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ————————————— AUTH ————————————————
LOGIN_URL          = 'login'
LOGIN_REDIRECT_URL = 'peliculas:lista_peliculas'
LOGOUT_REDIRECT_URL= 'peliculas:lista_peliculas'

# ————————————— TMDB SETTINGS ——————————————
TMDB_API_KEY       = config('TMDB_API_KEY')
TMDB_GENRES = {
    'accion': 28,
    'comedia': 35,
    'drama': 18,
    'romance': 10749,
    'terror': 27,
    'aventura': 12,
    'animacion': 16,
    'ciencia_ficcion': 878,
    'documental': 99,
}
TMDB_PREVIEW_PAGES = 1
TMDB_DETAIL_PAGES  =50
TMDB_ITEMS_PER_PAGE= 24
