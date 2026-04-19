from django.urls import path

from leitura.controllers.public_views import home, post_detail, post_list

urlpatterns = [
    path("", home, name="home"),
    path("posts", post_list, name="post_list"),
    path("posts/<slug:slug>", post_detail, name="post_detail"),
]
