import os

from django.core.exceptions import ImproperlyConfigured


TRUTHY_VALUES = {"1", "true", "yes", "on"}


def get_bool_env(name: str, default: bool = False) -> bool:
    raw_value = os.getenv(name)
    if raw_value is None:
        return default
    return raw_value.strip().lower() in TRUTHY_VALUES


def get_first_env(*names: str, default: str | None = None) -> str | None:
    for name in names:
        value = os.getenv(name)
        if value is not None and value != "":
            return value
    return default


def get_list_env_alias(primary_name: str, secondary_name: str, default: str = "") -> list[str]:
    raw_value = get_first_env(primary_name, secondary_name, default=default)
    if not raw_value:
        return []
    return [item.strip() for item in raw_value.split(",") if item.strip()]


def get_required_env(name: str, error_context: str = "production") -> str:
    value = os.getenv(name)
    if value:
        return value
    raise ImproperlyConfigured(f"Environment variable '{name}' is required in {error_context}.")


def get_required_env_alias(primary_name: str, secondary_name: str, error_context: str = "production") -> str:
    value = get_first_env(primary_name, secondary_name)
    if value:
        return value
    raise ImproperlyConfigured(
        f"Environment variable '{primary_name}' (or '{secondary_name}') is required in {error_context}."
    )

