from pathlib import Path

from django.core.exceptions import ImproperlyConfigured

from .env import get_bool_env, get_first_env


DATABASE_ENGINE_ALIASES = {
    "sqlite": "sqlite",
    "sqlite3": "sqlite",
    "postgres": "postgresql",
    "postgresql": "postgresql",
    "postgresql_psycopg2": "postgresql",
    "mysql": "mysql",
}


def _normalize_database_engine(raw_engine: str | None) -> str:
    engine = (raw_engine or "").strip().lower()
    normalized = DATABASE_ENGINE_ALIASES.get(engine)
    if normalized:
        return normalized
    raise ImproperlyConfigured(
        "Unsupported database engine. Use one of: sqlite, postgresql, mysql."
    )


def _get_database_engine(production: bool) -> str:
    explicit_engine = get_first_env("DATABASE_ENGINE", "DB_ENGINE")
    if explicit_engine:
        return _normalize_database_engine(explicit_engine)

    # Backward compatibility for local development.
    if not production and get_bool_env("USE_POSTGRES", default=False):
        return "postgresql"

    return "postgresql" if production else "sqlite"


def _required_in_production(value: str | None, label: str) -> str:
    if value:
        return value
    raise ImproperlyConfigured(f"Database setting '{label}' is required in production.")


def _build_postgresql_database(production: bool) -> dict[str, object]:
    name = get_first_env("POSTGRES_DB", "DB_NAME", "DATABASE_NAME")
    user = get_first_env("POSTGRES_USER", "DB_USER", "DATABASE_USER")
    password = get_first_env("POSTGRES_PASSWORD", "DB_PASSWORD", "DATABASE_PASSWORD")
    host = get_first_env("POSTGRES_HOST", "DB_HOST", "DATABASE_HOST", default="localhost")
    port = get_first_env("POSTGRES_PORT", "DB_PORT", "DATABASE_PORT", default="5432")

    if production:
        name = _required_in_production(name, "POSTGRES_DB/DB_NAME")
        user = _required_in_production(user, "POSTGRES_USER/DB_USER")
        password = _required_in_production(password, "POSTGRES_PASSWORD/DB_PASSWORD")
        host = _required_in_production(host, "POSTGRES_HOST/DB_HOST")
        port = _required_in_production(port, "POSTGRES_PORT/DB_PORT")
    else:
        name = name or "blog_leitura"
        user = user or "postgres"
        password = password or "postgres"

    return {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": name,
        "USER": user,
        "PASSWORD": password,
        "HOST": host,
        "PORT": port,
    }


def _build_mysql_database(production: bool) -> dict[str, object]:
    try:
        import pymysql
    except ImportError:
        # mysqlclient may be available in the runtime, so keep graceful fallback.
        pymysql = None
    if pymysql is not None:
        pymysql.install_as_MySQLdb()

    name = get_first_env("MYSQL_DATABASE", "MYSQL_DB", "DB_NAME", "DATABASE_NAME")
    user = get_first_env("MYSQL_USER", "DB_USER", "DATABASE_USER")
    password = get_first_env("MYSQL_PASSWORD", "DB_PASSWORD", "DATABASE_PASSWORD")
    host = get_first_env("MYSQL_HOST", "DB_HOST", "DATABASE_HOST", default="localhost")
    port = get_first_env("MYSQL_PORT", "DB_PORT", "DATABASE_PORT", default="3306")

    if production:
        name = _required_in_production(name, "MYSQL_DATABASE/DB_NAME")
        user = _required_in_production(user, "MYSQL_USER/DB_USER")
        password = _required_in_production(password, "MYSQL_PASSWORD/DB_PASSWORD")
        host = _required_in_production(host, "MYSQL_HOST/DB_HOST")
        port = _required_in_production(port, "MYSQL_PORT/DB_PORT")
    else:
        name = name or "blog_leitura"
        user = user or "root"
        password = password or ""

    options: dict[str, object] = {}
    ssl_ca = get_first_env("MYSQL_SSL_CA")
    if ssl_ca:
        options["ssl"] = {"ca": ssl_ca}

    database = {
        "ENGINE": "django.db.backends.mysql",
        "NAME": name,
        "USER": user,
        "PASSWORD": password,
        "HOST": host,
        "PORT": port,
    }
    if options:
        database["OPTIONS"] = options
    return database


def _build_sqlite_database(base_dir: Path, production: bool) -> dict[str, object]:
    db_name = get_first_env("SQLITE_PATH", "DB_NAME", "DATABASE_NAME")
    sqlite_name: str | Path = db_name or (base_dir / "db.sqlite3")

    if production and not get_bool_env("DJANGO_ALLOW_SQLITE_IN_PRODUCTION", default=False):
        raise ImproperlyConfigured(
            "SQLite in production is blocked by default. Set DATABASE_ENGINE=mysql/postgresql "
            "or set DJANGO_ALLOW_SQLITE_IN_PRODUCTION=1 only for exceptional scenarios."
        )

    return {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": sqlite_name,
    }


def get_database_settings(base_dir: Path, production: bool) -> dict[str, dict[str, object]]:
    engine = _get_database_engine(production=production)
    if engine == "postgresql":
        default_db = _build_postgresql_database(production=production)
    elif engine == "mysql":
        default_db = _build_mysql_database(production=production)
    else:
        default_db = _build_sqlite_database(base_dir=base_dir, production=production)

    return {"default": default_db}
