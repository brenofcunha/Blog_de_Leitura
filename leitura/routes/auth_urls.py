from django.contrib.auth import views as auth_views
from django.urls import path

from leitura.controllers.auth_views import post_login_redirect

urlpatterns = [
    path(
        "login",
        auth_views.LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path("logout", auth_views.LogoutView.as_view(next_page="home"), name="logout"),
    path("pos-login", post_login_redirect, name="post_login_redirect"),
]
