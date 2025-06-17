# Proyecto TMDB – Plataforma de Películas y Series con Django 🎥

**Python · Django · TMDB API · SQLite**

ProyectoTMDB es una aplicación web desarrollada con Django que permite explorar, buscar, valorar y organizar películas y series de televisión utilizando la API de The Movie Database (TMDB).

---

## 🎬 Características

**Exploración de Contenido**  
- Películas y series populares, tendencias actuales y próximos estrenos.  
- Listados filtrables por género.  
- Detalles completos: sinopsis, fecha de estreno, póster, elenco y director.

**Búsqueda Avanzada**  
- Autocompletado por título con resultados instantáneos.  
- Filtrado por tipo (movie o tv).

**Perfiles de Actores y Directores**  
- Biografías con foto.  
- Filmografía completa y roles principales.

**Interacción del Usuario**  
- ✅ Guardar favoritos.  
- ⭐ Valoraciones de 1 a 5 estrellas (persistentes para usuarios registrados).  
- 📝 Crear listas personalizadas de películas/series.

---

## 🛠️ Tecnologías Utilizadas

- **Backend**: Django (Python 3.x)  
- **Frontend**: HTML5, CSS3, JavaScript  
- **Base de Datos**: SQLite (desarrollo) – se puede cambiar a PostgreSQL en producción  
- **API Externa**: TMDB API v3 (requests + dotenv)  
- **Gestión de Entorno**: python-dotenv  

---

## 📋 Requisitos

- Python 3.8 o superior  
- Django 4.x  
- Cuenta de desarrollador en TMDB y **TMDB_API_KEY**

---

## 🚀 Instalación

1. **Clonar el repositorio**  
   ```bash
   git clone https://github.com/tuusuario/ProyectoTMDB.git
   cd ProyectoTMDB/ProyectoTMDB
   ```

2. **Crear y activar un entorno virtual**  
   ```bash
   python -m venv venv
   source venv/bin/activate    # Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**  
   Crea un archivo `.env` en la raíz del proyecto con:  
   ```env
   SECRET_KEY=tu_django_secret_key
   DEBUG=True
   TMDB_API_KEY=tu_api_key_de_tmdb
   ```

5. **Aplicar migraciones y arrancar el servidor**  
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

6. **Acceder a la aplicación**  
   Abre en tu navegador: `http://127.0.0.1:8000/`

---

## 🔧 Configuración de TMDB

1. Crea una cuenta gratuita en The Movie Database.  
2. Obtén tu **API Key** desde tu panel de usuario → Configuración → API.  
3. Añádela al archivo `.env` como `TMDB_API_KEY`.

---

## 📂 Estructura del Proyecto

```
ProyectoTMDB/
├── .env                      
├── .gitignore
├── db.sqlite3                
├── manage.py
├── requirements.txt
├── MovieTheatre/             
│   ├── settings.py
│   ├── urls.py
│   └── …
├── peliculas/                
│   ├── admin.py
│   ├── forms.py
│   ├── models.py             
│   ├── tmdb.py               
│   ├── urls.py
│   └── views.py
├── static/                   
├── staticfiles/              
└── docs/
    └── Documentacion_CineBD_Final.odt
```

---

## 👥 Contribución

¡Todas las contribuciones son bienvenidas!  
1. Haz un **fork** del repositorio.  
2. Crea una rama: `git checkout -b feature/nueva-funcionalidad`.  
3. Realiza tus cambios y haz **commit**: `git commit -m "Añade X funcionalidad"`.  
4. Envía tu rama: `git push origin feature/nueva-funcionalidad`.  
5. Abre un **Pull Request** en GitHub.

---

## 📝 Licencia

Este proyecto está licenciado bajo la **Licencia MIT**.  
Consulta el archivo LICENSE para más detalles.

---

## 🙏 Agradecimientos

- **The Movie Database (TMDB)** por su API abierta y completa  
- **Django** por su framework web robusto y flexible  
- **Todos los contribuidores** que hacen crecer este proyecto  

Desarrollado por Lucas Rubianes Eiras
