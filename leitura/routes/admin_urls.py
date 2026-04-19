from django.urls import path

from leitura.controllers.admin_views import (
    admin_dashboard,
    admin_post_create,
    admin_post_delete,
    admin_post_edit,
    admin_post_list,
)

urlpatterns = [
    path("admin", admin_dashboard, name="admin_dashboard"),
    path("admin/posts", admin_post_list, name="admin_posts"),
    path("admin/posts/novo", admin_post_create, name="admin_post_new"),
    path("admin/posts/<int:post_id>/editar", admin_post_edit, name="admin_post_edit"),
    path("admin/posts/<int:post_id>/excluir", admin_post_delete, name="admin_post_delete"),
]
