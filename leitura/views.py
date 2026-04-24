from leitura.controllers.admin_views import (
    admin_dashboard as painel_admin,
    admin_post_create,
    admin_post_edit,
    admin_post_list,
)
from leitura.controllers.auth_views import post_login_redirect as pos_login_redirect
from leitura.controllers.public_views import home, post_detail, post_list

__all__ = [
    "painel_admin",
    "admin_post_create",
    "admin_post_edit",
    "admin_post_list",
    "pos_login_redirect",
    "home",
    "post_detail",
    "post_list",
]
