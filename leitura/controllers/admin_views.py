from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render

from leitura.forms import PostForm
from leitura.models import Post
from leitura.repositories.post_repository import PostRepository
from leitura.services.post_service import all_posts_for_user, can_manage_post


@login_required
def admin_dashboard(request):
    posts = all_posts_for_user(request.user)
    context = {
        "total_posts": posts.count(),
        "draft_count": posts.filter(status=Post.STATUS_DRAFT).count(),
        "published_count": posts.filter(status=Post.STATUS_PUBLISHED).count(),
    }
    return render(request, "views/admin/dashboard.html", context)


@login_required
def admin_post_list(request):
    status = request.GET.get("status", "").strip()
    title = request.GET.get("titulo", "").strip()
    posts = PostRepository.list_for_user(request.user, status=status, title=title)
    return render(
        request,
        "views/admin/post_list.html",
        {
            "posts": posts,
            "status_filter": status,
            "title_filter": title,
            "status_choices": Post.STATUS_CHOICES,
        },
    )


@login_required
def admin_post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            action = request.POST.get("action")
            if action == "publish":
                post.status = Post.STATUS_PUBLISHED
            elif action == "save_draft":
                post.status = Post.STATUS_DRAFT

            PostRepository.save(post)
            form.save_related(post)
            return redirect("admin_posts")
    else:
        form = PostForm()

    return render(
        request,
        "views/admin/post_form.html",
        {
            "form": form,
            "page_title": "Novo post",
            "submit_label": "Criar post",
            "quick_category_options": PostForm.QUICK_CATEGORY_OPTIONS,
            "quick_tag_options": PostForm.QUICK_TAG_OPTIONS,
        },
    )


@login_required
def admin_post_edit(request, post_id):
    post = get_object_or_404(Post.objects.select_related("author"), pk=post_id)
    if not can_manage_post(request.user, post):
        raise PermissionDenied("Voce nao pode editar este post.")

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            edited_post = form.save(commit=False)
            action = request.POST.get("action")
            if action == "publish":
                edited_post.status = Post.STATUS_PUBLISHED
            elif action == "save_draft":
                edited_post.status = Post.STATUS_DRAFT

            PostRepository.save(edited_post)
            form.save_related(edited_post)
            return redirect("admin_posts")
    else:
        form = PostForm(instance=post)

    return render(
        request,
        "views/admin/post_form.html",
        {
            "form": form,
            "page_title": "Editar post",
            "submit_label": "Salvar alteracoes",
            "quick_category_options": PostForm.QUICK_CATEGORY_OPTIONS,
            "quick_tag_options": PostForm.QUICK_TAG_OPTIONS,
        },
    )


@login_required
def admin_post_delete(request, post_id):
    if request.method != "POST":
        return redirect("admin_posts")

    post = get_object_or_404(Post.objects.select_related("author"), pk=post_id)
    if not can_manage_post(request.user, post):
        raise PermissionDenied("Voce nao pode excluir este post.")

    PostRepository.delete(post)
    return redirect("admin_posts")
