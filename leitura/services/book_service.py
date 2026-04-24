from django.db.models import QuerySet

from leitura.models import Book
from leitura.repositories.book_repository import BookRepository


def all_books_for_user(user) -> QuerySet[Book]:
    return BookRepository.list_for_user(user)


def list_books(query=None, category=None, tag=None) -> QuerySet[Book]:
    return BookRepository.list_all(query=query, category=category, tag=tag)


def can_manage_book(user, book: Book) -> bool:
    if not user.is_authenticated:
        return False
    if user.is_staff or user.is_superuser:
        return True
    return book.added_by_id == user.id
