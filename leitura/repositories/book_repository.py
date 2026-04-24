from django.db.models import Q, QuerySet

from leitura.models import Book


class BookRepository:
    @staticmethod
    def list_for_user(user, status=None, title=None) -> QuerySet[Book]:
        queryset = Book.objects.select_related("added_by").prefetch_related("categories", "tags")
        if not (user.is_staff or user.is_superuser):
            queryset = queryset.filter(added_by=user)

        if status in {Book.STATUS_READING, Book.STATUS_READ, Book.STATUS_WISHLIST}:
            queryset = queryset.filter(status=status)

        if title:
            queryset = queryset.filter(
                Q(title__icontains=title) | Q(author_name__icontains=title)
            )

        return queryset

    @staticmethod
    def list_all(query=None, category=None, tag=None) -> QuerySet[Book]:
        queryset = (
            Book.objects.select_related("added_by")
            .prefetch_related("categories", "tags")
        )

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query)
                | Q(author_name__icontains=query)
                | Q(description__icontains=query)
            )

        if category:
            queryset = queryset.filter(categories__slug=category)

        if tag:
            queryset = queryset.filter(tags__slug=tag)

        return queryset.order_by("-created_at").distinct()

    @staticmethod
    def get_by_id(book_id: int) -> Book:
        return Book.objects.select_related("added_by").get(pk=book_id)

    @staticmethod
    def get_by_slug(slug: str) -> Book:
        return Book.objects.select_related("added_by").get(slug=slug)

    @staticmethod
    def save(book: Book) -> Book:
        book.save()
        return book

    @staticmethod
    def delete(book: Book) -> None:
        book.delete()
