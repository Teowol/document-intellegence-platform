from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path

from config.health import healthz


def home(request):
    """Root: authenticated users go to their profile, others to login."""
    if request.user.is_authenticated:
        return redirect("accounts:profile")
    return redirect("account_login")


urlpatterns = [
    path("", home, name="home"),
    path("admin/", admin.site.urls),
    path("healthz", healthz, name="healthz"),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("allauth.urls")),
]
