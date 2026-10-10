from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.views.generic import TemplateView

from .models import CustomUser
from .permissions import require_admin


class ProfileView(LoginRequiredMixin, TemplateView):
    """Simple profile page showing the user's role badge."""

    template_name = "accounts/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_role"] = self.request.user.get_role_display()
        return context


@require_admin
def admin_only_demo(request):
    """Demo view proving @require_admin blocks non-admins (tested in Phase 2 DoD)."""
    return render(request, "accounts/admin_only.html")
