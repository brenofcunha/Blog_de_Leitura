from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render

from leitura.forms import BookForm
from leitura.models import Book
from leitura.repositories.book_repository import BookRepository
from leitura.services.book_service import all_books_for_user, can_manage_book


@login_required
def book_list(request):
    status = request.GET.get("status", "").strip()
    title = request.GET.get("titulo", "").strip()
    books = BookRepository.list_for_user(request.user, status=status, title=title)
    return render(
        request,
        "views/admin/book_list.html",
        {
            "books": books,
            "status_filter": status,
            "title_filter": title,
            "status_choices": Book.STATUS_CHOICES,
        },
    )


@login_required
def book_create(request):
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.added_by = request.user
            BookRepository.save(book)
            form.save_m2m()
            return redirect("admin_books")
    else:
        form = BookForm()

    return render(
        request,
        "views/admin/book_form.html",
        {"form": form, "page_title": "Adicionar livro", "submit_label": "Salvar livro"},
    )


@login_required
def book_edit(request, book_id):
    book = get_object_or_404(Book.objects.select_related("added_by"), pk=book_id)
    if not can_manage_book(request.user, book):
        raise PermissionDenied("Voce nao pode editar este livro.")

    if request.method == "POST":
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            BookRepository.save(form.save(commit=False))
            form.save_m2m()
            return redirect("admin_books")
    else:
        form = BookForm(instance=book)

    return render(
        request,
        "views/admin/book_form.html",
        {"form": form, "page_title": "Editar livro", "submit_label": "Salvar alteracoes"},
    )


@login_required
def book_delete(request, book_id):
    if request.method != "POST":
        return redirect("admin_books")

    book = get_object_or_404(Book.objects.select_related("added_by"), pk=book_id)
    if not can_manage_book(request.user, book):
        raise PermissionDenied("Voce nao pode excluir este livro.")

    BookRepository.delete(book)
    return redirect("admin_books")
