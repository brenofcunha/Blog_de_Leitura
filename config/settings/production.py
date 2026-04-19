import os

from django.core.exceptions import ImproperlyConfigured

from .base import *  # noqa: F403
from .base import get_list_env


def get_required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ImproperlyConfigured(f"Environment variable '{name}' is required in production.")
    return value


DEBUG = False
SECRET_KEY = get_required_env("DJANGO_SECRET_KEY")

ALLOWED_HOSTS = get_list_env("DJANGO_ALLOWED_HOSTS")
if not ALLOWED_HOSTS:
    raise ImproperlyConfigured("DJANGO_ALLOWED_HOSTS must be defined in production.")

CSRF_TRUSTED_ORIGINS = get_list_env("DJANGO_CSRF_TRUSTED_ORIGINS")
if not CSRF_TRUSTED_ORIGINS:
    raise ImproperlyConfigured("DJANGO_CSRF_TRUSTED_ORIGINS must be defined in production.")

invalid_origins = [origin for origin in CSRF_TRUSTED_ORIGINS if not origin.startswith("https://")]
if invalid_origins:
    invalid = ", ".join(invalid_origins)
    raise ImproperlyConfigured(
        f"Invalid CSRF trusted origins (must include https://): {invalid}"
    )

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": get_required_env("POSTGRES_DB"),
        "USER": get_required_env("POSTGRES_USER"),
        "PASSWORD": get_required_env("POSTGRES_PASSWORD"),
        "HOST": get_required_env("POSTGRES_HOST"),
        "PORT": get_required_env("POSTGRES_PORT"),
    }
}

AWS_STORAGE_BUCKET_NAME = get_required_env("AWS_STORAGE_BUCKET_NAME")
AWS_S3_REGION_NAME = get_required_env("AWS_S3_REGION_NAME")
AWS_ACCESS_KEY_ID = get_required_env("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = get_required_env("AWS_SECRET_ACCESS_KEY")
AWS_S3_SIGNATURE_VERSION = "s3v4"
AWS_DEFAULT_ACL = None
AWS_QUERYSTRING_AUTH = False
AWS_S3_FILE_OVERWRITE = False

AWS_S3_CUSTOM_DOMAIN = os.getenv("AWS_S3_CUSTOM_DOMAIN", "")
if AWS_S3_CUSTOM_DOMAIN:
    MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/media/"
else:
    MEDIA_URL = f"https://{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com/media/"

# Django 5 storage API.
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "bucket_name": AWS_STORAGE_BUCKET_NAME,
            "region_name": AWS_S3_REGION_NAME,
            "access_key": AWS_ACCESS_KEY_ID,
            "secret_key": AWS_SECRET_ACCESS_KEY,
            "default_acl": AWS_DEFAULT_ACL,
            "querystring_auth": AWS_QUERYSTRING_AUTH,
            "file_overwrite": AWS_S3_FILE_OVERWRITE,
            "location": "media",
            "custom_domain": AWS_S3_CUSTOM_DOMAIN or None,
        },
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
SECURE_BROWSER_XSS_FILTER = True

if os.getenv("DJANGO_USE_X_FORWARDED_PROTO", "1") == "1":
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SECURE_SSL_REDIRECT = os.getenv("DJANGO_SECURE_SSL_REDIRECT", "1") == "1"
SECURE_HSTS_SECONDS = int(os.getenv("DJANGO_SECURE_HSTS_SECONDS", "31536000"))
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
