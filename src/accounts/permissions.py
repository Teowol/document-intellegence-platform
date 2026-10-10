"""RBAC helpers for Phase 2, reused by views and DRF in later phases."""

from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from .models import CustomUser


def require_role(*roles):
    """
    View decorator: allow access only to users with one of the given roles.
    Superusers always pass. Combine with login by default.
    Usage: @require_role(CustomUser.Roles.ADMIN, CustomUser.Roles.EDITOR)
    """

    def decorator(view):
        @wraps(view)
        @login_required
        def _wrapped(request, *args, **kwargs):
            user = request.user
            if isinstance(user, CustomUser):
                allowed = user.is_superuser or user.role in roles
            else:
                allowed = user.is_superuser
            if not allowed:
                raise PermissionDenied("Bu işlem için yetkiniz yok.")
            return view(request, *args, **kwargs)

        return _wrapped

    return decorator


def require_admin(view):
    """Shortcut: only admin-role users (or superusers) may proceed."""
    return require_role(CustomUser.Roles.ADMIN)(view)
