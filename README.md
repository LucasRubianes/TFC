# CineApp - Plataforma de Películas y Series con Django

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.0%2B-green)](https://www.djangoproject.com/)
[![TMDB API](https://img.shields.io/badge/TMDB%20API-v3-yellow)](https://developers.themoviedb.org/)
[![License](https://img.shields.io/badge/License-MIT-lightgrey)](LICENSE)

CineApp es una aplicación web desarrollada con Django que permite explorar, buscar y valorar películas y series de televisión utilizando el API de The Movie Database (TMDB).

![CineApp Screenshot](screenshot.png)

## 🎬 Características

- **Exploración de Contenido**:
  - Películas y series populares y tendencias actuales
  - Listados por género
  - Colecciones especiales (mejor valoradas, próximos estrenos)
  - Detalles completos de películas y series

- **Búsqueda Avanzada**:
  - Búsqueda por título con resultados instantáneos
  - Filtrado por tipo de contenido (película o serie)

- **Perfiles Detallados**:
  - Biografías de actores y directores
  - Filmografías completas
  - Roles principales y secundarios

- **Sistema de Valoraciones**:
  - Valoración de películas y series (1-5 estrellas)
  - Almacenamiento persistente de valoraciones para usuarios registrados
  - Valoraciones temporales para usuarios anónimos

## 🛠️ Tecnologías Utilizadas

- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Base de Datos**: SQLite (desarrollo) / PostgreSQL (producción)
- **API Externa**: The Movie Database (TMDB) API v3

## 📋 Requisitos

- Python 3.8+
- Django 4.0+
- Cuenta de desarrollador en TMDB y API Key

## 🚀 Instalación

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/yourusername/cineapp.git
   cd cineapp
   ```

2. **Crear y activar entorno virtual**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**:
   Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido:
   ```
   SECRET_KEY=your_django_secret_key
   DEBUG=True
   TMDB_API_KEY=your_tmdb_api_key
   ```

5. **Ejecutar migraciones**:
   ```bash
   python manage.py migrate
   ```

6. **Iniciar servidor de desarrollo**:
   ```bash
   python manage.py runserver
   ```

7. **Acceder a la aplicación**:
   Abre tu navegador y visita `http://localhost:8000`

## 🔧 Configuración de TMDB

Para utilizar esta aplicación, necesitas una API Key de TMDB:

1. Regístrate en [The Movie Database](https://www.themoviedb.org/)
2. Ve a la sección de configuración de tu cuenta y solicita una API Key
3. Añade la API Key al archivo `.env` o en las variables de entorno

## 📚 Estructura del Proyecto

```
cineapp/
├── cineapp/               # Configuración del proyecto Django
├── peliculas/             # Aplicación principal
│   ├── migrations/        # Migraciones de la base de datos
│   ├── templates/         # Plantillas HTML
│   ├── apps.py            # Configuración de la aplicación
│   ├── models.py          # Modelos de datos
│   ├── tmdb.py            # Funciones para interactuar con la API de TMDB
│   ├── urls.py            # Definición de URLs
│   └── views.py           # Vistas y lógica de negocio
├── static/                # Archivos estáticos (CSS, JS, imágenes)
├── templates/             # Plantillas globales
├── manage.py              # Script de administración de Django
└── requirements.txt       # Dependencias del proyecto
```

## 👥 Contribución

Las contribuciones son bienvenidas. Por favor, sigue estos pasos:

1. Fork del repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Realiza tus cambios y commitea (`git commit -am 'Añade nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crea un Pull Request

## 📝 Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 🙏 Agradecimientos

- [The Movie Database (TMDB)](https://www.themoviedb.org/) por proporcionar una API robusta y completa
- [Django](https://www.djangoproject.com/) por su framework web potente y flexible
- Todos los contribuidores que ayudan a mejorar este proyecto

---

⭐ Desarrollado con ❤️ por [Tu Nombre](https://github.com/yourusername) ⭐
