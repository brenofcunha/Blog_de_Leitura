from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path(
        "programator-pragmatico/",
        views.programator_pragmatico,
        name="programator_pragmatico",
    ),
]
