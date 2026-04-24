from django.urls import include, path

urlpatterns = [
    path("", include("leitura.routes.public_urls")),
    path("", include("leitura.routes.admin_urls")),
    path("", include("leitura.routes.auth_urls")),
    path("", include("leitura.routes.book_urls")),
]
