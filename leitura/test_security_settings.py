import importlib
import os
import sys
from contextlib import contextmanager

from django.core.exceptions import ImproperlyConfigured
from django.test import SimpleTestCase


BASE_PROD_ENV = {
    "DEBUG": "0",
    "SECRET_KEY": "segredo-super-forte",
    "ALLOWED_HOSTS": "example.com,www.example.com",
    "CSRF_TRUSTED_ORIGINS": "https://example.com,https://www.example.com",
    "DATABASE_ENGINE": "mysql",
    "MYSQL_DATABASE": "blog_leitura",
    "MYSQL_USER": "blog_user",
    "MYSQL_PASSWORD": "senha-forte",
    "MYSQL_HOST": "localhost",
    "MYSQL_PORT": "3306",
}


@contextmanager
def production_env(extra_env=None, removed=None):
    extra_env = extra_env or {}
    removed = removed or []

    backup = {}
    tracked_keys = set(BASE_PROD_ENV) | set(extra_env) | set(removed)
    tracked_keys.update(
        {
            "DJANGO_SECRET_KEY",
            "DJANGO_ALLOWED_HOSTS",
            "DJANGO_CSRF_TRUSTED_ORIGINS",
            "POSTGRES_DB",
            "POSTGRES_USER",
            "POSTGRES_PASSWORD",
            "POSTGRES_HOST",
            "POSTGRES_PORT",
            "DB_NAME",
            "DB_USER",
            "DB_PASSWORD",
            "DB_HOST",
            "DB_PORT",
            "AWS_STORAGE_BUCKET_NAME",
            "AWS_S3_REGION_NAME",
            "AWS_ACCESS_KEY_ID",
            "AWS_SECRET_ACCESS_KEY",
        }
    )

    for key in tracked_keys:
        backup[key] = os.environ.get(key)

    try:
        for key in tracked_keys:
            os.environ.pop(key, None)

        os.environ.update(BASE_PROD_ENV)
        os.environ.update(extra_env)

        for key in removed:
            os.environ.pop(key, None)

        yield
    finally:
        for key in tracked_keys:
            os.environ.pop(key, None)
            if backup[key] is not None:
                os.environ[key] = backup[key]


def load_production_settings_module():
    module_name = "config.settings.production"
    if module_name in sys.modules:
        del sys.modules[module_name]
    return importlib.import_module(module_name)


class ProductionSettingsSecurityTests(SimpleTestCase):
    def test_production_requires_secret_key(self):
        with production_env(removed=["SECRET_KEY", "DJANGO_SECRET_KEY"]):
            with self.assertRaises(ImproperlyConfigured):
                load_production_settings_module()

    def test_production_rejects_debug_true(self):
        with production_env({"DEBUG": "1"}):
            with self.assertRaises(ImproperlyConfigured):
                load_production_settings_module()

    def test_production_rejects_wildcard_allowed_hosts(self):
        with production_env({"ALLOWED_HOSTS": "*"}):
            with self.assertRaises(ImproperlyConfigured):
                load_production_settings_module()

    def test_production_requires_https_csrf_origins(self):
        with production_env({"CSRF_TRUSTED_ORIGINS": "http://example.com"}):
            with self.assertRaises(ImproperlyConfigured):
                load_production_settings_module()

    def test_production_loads_with_valid_security_env(self):
        with production_env():
            settings_module = load_production_settings_module()

        self.assertFalse(settings_module.DEBUG)
        self.assertEqual(settings_module.ALLOWED_HOSTS, ["example.com", "www.example.com"])
        self.assertEqual(
            settings_module.CSRF_TRUSTED_ORIGINS,
            ["https://example.com", "https://www.example.com"],
        )
        self.assertTrue(settings_module.SESSION_COOKIE_SECURE)
        self.assertTrue(settings_module.CSRF_COOKIE_SECURE)
        self.assertTrue(settings_module.SECURE_SSL_REDIRECT)
        self.assertEqual(settings_module.X_FRAME_OPTIONS, "DENY")

    def test_production_uses_local_media_storage_without_aws(self):
        with production_env():
            settings_module = load_production_settings_module()

        self.assertEqual(
            settings_module.STORAGES["default"]["BACKEND"],
            "django.core.files.storage.FileSystemStorage",
        )

    def test_production_uses_s3_storage_when_aws_config_is_complete(self):
        with production_env(
            {
                "AWS_STORAGE_BUCKET_NAME": "bucket-exemplo",
                "AWS_S3_REGION_NAME": "us-east-1",
                "AWS_ACCESS_KEY_ID": "ak-test",
                "AWS_SECRET_ACCESS_KEY": "sk-test",
            }
        ):
            settings_module = load_production_settings_module()

        self.assertEqual(
            settings_module.STORAGES["default"]["BACKEND"],
            "storages.backends.s3.S3Storage",
        )
        self.assertTrue(settings_module.MEDIA_URL.startswith("https://bucket-exemplo.s3."))

    def test_production_rejects_partial_aws_configuration(self):
        with production_env({"AWS_STORAGE_BUCKET_NAME": "bucket-incompleto"}):
            with self.assertRaises(ImproperlyConfigured):
                load_production_settings_module()
