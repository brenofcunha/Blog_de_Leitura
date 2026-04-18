from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("painel-admin/", views.painel_admin, name="painel_admin"),
    path("pos-login/", views.pos_login_redirect, name="pos_login_redirect"),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="home"), name="logout"),
    path(
        "programador-pragmatico/",
        views.programador_pragmatico,
        name="programador_pragmatico",
    ),
]
