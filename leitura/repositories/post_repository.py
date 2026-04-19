from django.db.models import QuerySet

from leitura.models import Post


class PostRepository:
    @staticmethod
    def list_for_user(user, status=None, title=None) -> QuerySet[Post]:
        queryset = Post.objects.select_related("author")
        if not (user.is_staff or user.is_superuser):
            queryset = queryset.filter(author=user)

        if status in {Post.STATUS_DRAFT, Post.STATUS_PUBLISHED}:
            queryset = queryset.filter(status=status)

        if title:
            queryset = queryset.filter(title__icontains=title)

        return queryset

    @staticmethod
    def list_published() -> QuerySet[Post]:
        return Post.objects.select_related("author").filter(status=Post.STATUS_PUBLISHED)

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
