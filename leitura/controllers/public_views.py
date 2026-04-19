from django.shortcuts import get_object_or_404, render

from leitura.models import Post
from leitura.services.post_service import published_posts


def home(request):
    recent_posts = published_posts()[:6]
    return render(request, "views/public/home.html", {"recent_posts": recent_posts})


def post_list(request):
    posts = published_posts()
    return render(request, "views/public/post_list.html", {"posts": posts})


def post_detail(request, slug):
    post = get_object_or_404(published_posts(), slug=slug)
    return render(request, "views/public/post_detail.html", {"post": post})
