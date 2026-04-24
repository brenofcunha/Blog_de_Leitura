from django.urls import path

from leitura.controllers.book_views import book_create, book_delete, book_edit, book_list

urlpatterns = [
    path("admin/livros", book_list, name="admin_books"),
    path("admin/livros/novo", book_create, name="admin_book_new"),
    path("admin/livros/<int:book_id>/editar", book_edit, name="admin_book_edit"),
    path("admin/livros/<int:book_id>/excluir", book_delete, name="admin_book_delete"),
]
