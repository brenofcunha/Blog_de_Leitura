from django.db.models import QuerySet

from leitura.models import Post
from leitura.repositories.post_repository import PostRepository


def published_posts(query=None, category=None, tag=None) -> QuerySet[Post]:
    return PostRepository.list_published(query=query, category=category, tag=tag)


def all_posts_for_user(user) -> QuerySet[Post]:
    return PostRepository.list_for_user(user)


def can_manage_everything(user) -> bool:
    if user.is_staff or user.is_superuser:
        return True
    profile = getattr(user, "userprofile", None)
    return bool(profile and profile.role == "admin")


def can_manage_post(user, post: Post) -> bool:
    if not user.is_authenticated:
        return False
    return can_manage_everything(user) or post.author_id == user.id
