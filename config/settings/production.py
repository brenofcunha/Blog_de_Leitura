import os

from django.core.exceptions import ImproperlyConfigured

from .base import *  # noqa: F403
from .base import BASE_DIR
from .components.database import get_database_settings
from .components.env import (
    get_bool_env,
    get_list_env_alias,
    get_required_env_alias,
)
from .components.storage import get_storage_settings

DEBUG = get_bool_env("DEBUG", default=False)
if DEBUG:
    raise ImproperlyConfigured("DEBUG must be False in production.")

SECRET_KEY = get_required_env_alias("DJANGO_SECRET_KEY", "SECRET_KEY")

ALLOWED_HOSTS = get_list_env_alias("ALLOWED_HOSTS", "DJANGO_ALLOWED_HOSTS")
if not ALLOWED_HOSTS:
    raise ImproperlyConfigured(
        "ALLOWED_HOSTS (or DJANGO_ALLOWED_HOSTS) must be defined in production."
    )
if "*" in ALLOWED_HOSTS:
    raise ImproperlyConfigured("Wildcard '*' is not allowed in ALLOWED_HOSTS for production.")

CSRF_TRUSTED_ORIGINS = get_list_env_alias(
    "CSRF_TRUSTED_ORIGINS", "DJANGO_CSRF_TRUSTED_ORIGINS"
)
if not CSRF_TRUSTED_ORIGINS:
    raise ImproperlyConfigured(
        "CSRF_TRUSTED_ORIGINS (or DJANGO_CSRF_TRUSTED_ORIGINS) must be defined in production."
    )

invalid_origins = [origin for origin in CSRF_TRUSTED_ORIGINS if not origin.startswith("https://")]
if invalid_origins:
    invalid = ", ".join(invalid_origins)
    raise ImproperlyConfigured(f"Invalid CSRF trusted origins (must include https://): {invalid}")

DATABASES = get_database_settings(base_dir=BASE_DIR, production=True)

storage_settings = get_storage_settings()
for key, value in storage_settings.items():
    globals()[key] = value

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
SECURE_BROWSER_XSS_FILTER = True
SECURE_REFERRER_POLICY = "same-origin"

if get_bool_env("DJANGO_USE_X_FORWARDED_PROTO", default=True):
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SECURE_SSL_REDIRECT = get_bool_env("DJANGO_SECURE_SSL_REDIRECT", default=True)
SECURE_HSTS_SECONDS = int(os.getenv("DJANGO_SECURE_HSTS_SECONDS", "31536000"))
SECURE_HSTS_INCLUDE_SUBDOMAINS = get_bool_env("DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True)
SECURE_HSTS_PRELOAD = get_bool_env("DJANGO_SECURE_HSTS_PRELOAD", default=True)

