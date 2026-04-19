import re
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.utils.safestring import mark_safe
from django.utils.html import escape

from leitura.models import Category, Post, Tag
from leitura.services.post_service import published_posts


def render_basic_markdown(content: str):
    escaped = escape(content)
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"\[(.+?)\]\((https?://[^\s)]+)\)", r'<a href="\2" target="_blank" rel="noopener noreferrer">\1</a>', escaped)

    lines = escaped.split("\n")
    html_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("## "):
            html_lines.append(f"<h2>{stripped[3:]}</h2>")
        elif stripped.startswith("# "):
            html_lines.append(f"<h1>{stripped[2:]}</h1>")
        elif stripped.startswith("- "):
            html_lines.append(f"<li>{stripped[2:]}</li>")
        elif stripped:
            html_lines.append(f"<p>{stripped}</p>")
        else:
            html_lines.append("<br>")

    return mark_safe("".join(html_lines))


def home(request):
    query = request.GET.get("q", "").strip()
    posts = list(published_posts(query=query))
    featured_post = posts[0] if posts else None
    recent_posts = posts[1:7] if featured_post else []
    highlighted_posts = posts[:3]
    categories = Category.objects.all()

    context = {
        "query": query,
        "featured_post": featured_post,
        "recent_posts": recent_posts,
        "highlighted_posts": highlighted_posts,
        "categories": categories,
        "published_total": len(posts),
    }
    return render(request, "views/public/home.html", context)


def post_list(request):
    query = request.GET.get("q", "").strip()
    category = request.GET.get("categoria", "").strip()
    tag = request.GET.get("tag", "").strip()

    posts = published_posts(query=query, category=category, tag=tag)
    paginator = Paginator(posts, 6)
    page_obj = paginator.get_page(request.GET.get("page", 1))

    return render(
        request,
        "views/public/post_list.html",
        {
            "posts": page_obj.object_list,
            "page_obj": page_obj,
            "pagination_ready": True,
            "query": query,
            "selected_category": category,
            "selected_tag": tag,
            "categories": Category.objects.all(),
            "tags": Tag.objects.all(),
        },
    )


def post_detail(request, slug):
    published_qs = published_posts()
    post = get_object_or_404(published_qs, slug=slug)
    post_html = render_basic_markdown(post.content)

    ordered_ids = list(published_qs.values_list("id", flat=True))
    post_index = ordered_ids.index(post.id)
    previous_post = None
    next_post = None
    if post_index > 0:
        next_post = Post.objects.filter(id=ordered_ids[post_index - 1]).first()
    if post_index < len(ordered_ids) - 1:
        previous_post = Post.objects.filter(id=ordered_ids[post_index + 1]).first()

    suggestions = published_qs.exclude(id=post.id)[:3]

    return render(
        request,
        "views/public/post_detail.html",
        {
            "post": post,
            "post_html": post_html,
            "previous_post": previous_post,
            "next_post": next_post,
            "suggestions": suggestions,
        },
    )
