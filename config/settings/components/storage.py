from django.core.exceptions import ImproperlyConfigured

from .env import get_first_env


AWS_REQUIRED_VARS = [
    "AWS_STORAGE_BUCKET_NAME",
    "AWS_S3_REGION_NAME",
    "AWS_ACCESS_KEY_ID",
    "AWS_SECRET_ACCESS_KEY",
]


def get_storage_settings() -> dict[str, object]:
    aws_values = {key: get_first_env(key) for key in AWS_REQUIRED_VARS}
    has_any_aws_setting = any(aws_values.values())
    has_full_aws_settings = all(aws_values.values())

    if has_any_aws_setting and not has_full_aws_settings:
        missing = [key for key, value in aws_values.items() if not value]
        missing_text = ", ".join(missing)
        raise ImproperlyConfigured(
            f"Incomplete AWS S3 configuration. Missing required variables: {missing_text}"
        )

    if not has_full_aws_settings:
        return {
            "STORAGES": {
                "default": {
                    "BACKEND": "django.core.files.storage.FileSystemStorage",
                },
                "staticfiles": {
                    "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
                },
            }
        }

    bucket_name = aws_values["AWS_STORAGE_BUCKET_NAME"] or ""
    region_name = aws_values["AWS_S3_REGION_NAME"] or ""
    access_key = aws_values["AWS_ACCESS_KEY_ID"] or ""
    secret_key = aws_values["AWS_SECRET_ACCESS_KEY"] or ""
    custom_domain = get_first_env("AWS_S3_CUSTOM_DOMAIN", default="")
    media_prefix = get_first_env("AWS_MEDIA_LOCATION", default="media") or "media"

    if custom_domain:
        media_url = f"https://{custom_domain}/{media_prefix}/"
    else:
        media_url = f"https://{bucket_name}.s3.{region_name}.amazonaws.com/{media_prefix}/"

    return {
        "MEDIA_URL": media_url,
        "STORAGES": {
            "default": {
                "BACKEND": "storages.backends.s3.S3Storage",
                "OPTIONS": {
                    "bucket_name": bucket_name,
                    "region_name": region_name,
                    "access_key": access_key,
                    "secret_key": secret_key,
                    "default_acl": None,
                    "querystring_auth": False,
                    "file_overwrite": False,
                    "location": media_prefix,
                    "custom_domain": custom_domain or None,
                },
            },
            "staticfiles": {
                "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
            },
        },
    }
