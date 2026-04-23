from .base import *  # noqa: F403
from .base import BASE_DIR
from .components.database import get_database_settings
from .components.env import get_bool_env

# Local development defaults.
SECRET_KEY = SECRET_KEY or "django-insecure-development-key-change-me"  # noqa: F405
DEBUG = get_bool_env("DEBUG", default=True)
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
CSRF_TRUSTED_ORIGINS = ["http://127.0.0.1:8000", "http://localhost:8000"]

DATABASES = get_database_settings(base_dir=BASE_DIR, production=False)

