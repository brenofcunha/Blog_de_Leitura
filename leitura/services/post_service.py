from django.db.models import QuerySet

from leitura.models import Post
from leitura.repositories.post_repository import PostRepository


def published_posts() -> QuerySet[Post]:
    return PostRepository.list_published()


def all_posts_for_user(user) -> QuerySet[Post]:
    return PostRepository.list_for_user(user)


def can_manage_everything(user) -> bool:
    if user.is_staff or user.is_superuser:
        return True
    profile = getattr(user, "userprofile", None)
    return bool(profile and profile.role == "admin")
