from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from leitura.models import UserProfile


@login_required
def post_login_redirect(request):
    user = request.user
    try:
        UserProfile.objects.get_or_create(
            user=user,
            defaults={"role": UserProfile.ROLE_ADMIN if (user.is_staff or user.is_superuser) else UserProfile.ROLE_AUTHOR},
        )
    except Exception:
        pass
    return redirect("admin_dashboard")
