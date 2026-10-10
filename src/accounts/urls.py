from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("demo/admin-only/", views.admin_only_demo, name="admin_only_demo"),
]
