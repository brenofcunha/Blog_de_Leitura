import os

from .base import *  # noqa: F403

# Local development defaults.
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "django-insecure-development-key-change-me")
DEBUG = get_bool_env("DEBUG", default=True)
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
CSRF_TRUSTED_ORIGINS = ["http://127.0.0.1:8000", "http://localhost:8000"]

USE_POSTGRES = os.getenv("USE_POSTGRES", "0") == "1"
if USE_POSTGRES:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("POSTGRES_DB", "blog_leitura"),
            "USER": os.getenv("POSTGRES_USER", "postgres"),
            "PASSWORD": os.getenv("POSTGRES_PASSWORD", "postgres"),
            "HOST": os.getenv("POSTGRES_HOST", "localhost"),
            "PORT": os.getenv("POSTGRES_PORT", "5432"),
        }
    }
