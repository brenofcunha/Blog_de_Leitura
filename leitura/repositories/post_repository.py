from django.db.models import QuerySet
from django.db.models import Q

from leitura.models import Post


class PostRepository:
    @staticmethod
    def list_for_user(user, status=None, title=None) -> QuerySet[Post]:
        queryset = Post.objects.select_related("author").prefetch_related("categories", "tags")
        if not (user.is_staff or user.is_superuser):
            queryset = queryset.filter(author=user)

        if status in {Post.STATUS_DRAFT, Post.STATUS_PUBLISHED}:
            queryset = queryset.filter(status=status)

        if title:
            queryset = queryset.filter(title__icontains=title)

        return queryset

    @staticmethod
    def list_published(query=None, category=None, tag=None) -> QuerySet[Post]:
        queryset = (
            Post.objects.select_related("author")
            .prefetch_related("categories", "tags")
            .filter(status=Post.STATUS_PUBLISHED)
        )

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query)
                | Q(summary__icontains=query)
                | Q(content__icontains=query)
            )

        if category:
            queryset = queryset.filter(categories__slug=category)

        if tag:
            queryset = queryset.filter(tags__slug=tag)

        return queryset.order_by("-published_at", "-created_at").distinct()

    @staticmethod
    def get_by_id(post_id: int) -> Post:
        return Post.objects.select_related("author").get(pk=post_id)

    @staticmethod
    def save(post: Post) -> Post:
        post.save()
        return post

    @staticmethod
    def delete(post: Post) -> None:
        post.delete()
