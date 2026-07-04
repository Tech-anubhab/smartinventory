# DWP Inventory Management

A Django-based inventory management application with custom user authentication, item tracking, sales reporting, and audit logging.

## Features

- Custom user model and authentication via `accounts`
- Inventory management and sales tracking via `inventory`
- Audit logging and views via `audit`
- Built with Django 6.0 and SQLite by default
- Production-ready static file handling using WhiteNoise

## Requirements

- Python 3.11+ (recommended)
- Django 6.0.5
- `psycopg2-binary` (for PostgreSQL if used in production)
- `gunicorn`
- `whitenoise`

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Setup

1. Create a virtual environment:

```bash
python -m venv venv
```

2. Activate the virtual environment:

```powershell
venv\Scripts\Activate.ps1
```

3. Install requirements:

```bash
pip install -r requirements.txt
```

4. Apply migrations:

```bash
python manage.py migrate
```

5. Create a superuser:

```bash
python manage.py createsuperuser
```

6. Run the development server:

```bash
python manage.py runserver
```

## Environment variables

- `SECRET_KEY` - Django secret key
- `DEBUG` - Set to `False` in production
- `ALLOWED_HOSTS` - Comma-separated allowed hosts

The project uses SQLite by default at `db.sqlite3`. For production, update `DATABASES` in `config/settings.py`.

## Deployment

- The app includes a `Procfile` for deployment platforms like Heroku / Railway.
- Static files are served with WhiteNoise.

## Project structure

- `accounts/` - custom user model, auth views and forms
- `inventory/` - item inventory, sales, reports
- `audit/` - auditing, logging, and audit views
- `config/` - Django project settings, URL config, WSGI/ASGI

## Useful commands

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Notes

- Templates are stored under `templates/`
- Static assets are in `static/`
- `STATIC_ROOT` is configured to `staticfiles/` for production collectstatic
