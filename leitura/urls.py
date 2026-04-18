from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path(
        "programador-pragmatico/",
        views.programador_pragmatico,
        name="programador_pragmatico",
    ),
]
