"""Phase 0-2 tests: custom User model, RBAC roles, allauth flows."""

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from accounts.models import CustomUser

pytestmark = pytest.mark.django_db

User = get_user_model()


# --------------------------------------------------------------------------
# Phase 0 — custom User model
# --------------------------------------------------------------------------

def test_create_user_with_email():
    user = User.objects.create_user(
        username="ali", email="ali@example.com", password="S3cure-pass!"
    )
    assert user.email == "ali@example.com"
    assert user.is_active
    assert not user.is_staff
    assert str(user) == "ali@example.com"


def test_email_is_unique():
    User.objects.create_user(username="a", email="dup@example.com", password="x")
    with pytest.raises(Exception):
        User.objects.create_user(username="b", email="dup@example.com", password="x")


# --------------------------------------------------------------------------
# Phase 2 — roles & group sync
# --------------------------------------------------------------------------

def test_default_role_is_viewer():
    user = User.objects.create_user(username="v", email="v@example.com", password="x")
    assert user.role == CustomUser.Roles.VIEWER


def test_role_group_sync_on_change():
    user = User.objects.create_user(username="g", email="g@example.com", password="x")
    assert user.groups.filter(name="role_viewer").exists()

    user.role = CustomUser.Roles.EDITOR
    user.save()
    assert user.groups.filter(name="role_editor").exists()
    assert not user.groups.filter(name="role_viewer").exists()


def test_superuser_counts_as_admin_role():
    user = User.objects.create_superuser(
        username="s", email="s@example.com", password="x"
    )
    assert user.is_admin_role


# --------------------------------------------------------------------------
# Phase 2 — @require_admin decorator
# --------------------------------------------------------------------------

def test_admin_demo_view_blocked_for_viewer(client):
    User.objects.create_user(username="v1", email="v1@example.com", password="Pass123!")
    client.force_login(User.objects.get(email="v1@example.com"))
    resp = client.get(reverse("accounts:admin_only_demo"))
    assert resp.status_code == 403


def test_admin_demo_view_blocked_for_editor(client):
    User.objects.create_user(
        username="e1", email="e1@example.com", password="Pass123!",
        role=CustomUser.Roles.EDITOR,
    )
    client.force_login(User.objects.get(email="e1@example.com"))
    resp = client.get(reverse("accounts:admin_only_demo"))
    assert resp.status_code == 403


def test_admin_demo_view_allowed_for_admin(client):
    User.objects.create_user(
        username="a1", email="a1@example.com", password="Pass123!",
        role=CustomUser.Roles.ADMIN,
    )
    client.force_login(User.objects.get(email="a1@example.com"))
    resp = client.get(reverse("accounts:admin_only_demo"))
    assert resp.status_code == 200


def test_admin_demo_view_requires_login(client):
    resp = client.get(reverse("accounts:admin_only_demo"))
    assert resp.status_code == 302  # redirect to login


# --------------------------------------------------------------------------
# Phase 2 — allauth signup / login / logout
# --------------------------------------------------------------------------

SIGNUP_DATA = {
    "email": "new@example.com",
    "username": "newbie",
    "password1": "Sturdy-Pass-2024",
    "password2": "Sturdy-Pass-2024",
}


def test_signup_creates_viewer(client):
    resp = client.post(reverse("account_signup"), SIGNUP_DATA)
    assert resp.status_code == 302
    user = User.objects.get(email="new@example.com")
    assert user.role == CustomUser.Roles.VIEWER


def test_login_with_email(client):
    User.objects.create_user(username="l1", email="l1@example.com", password="Pass123!")
    resp = client.post(
        reverse("account_login"),
        {"login": "l1@example.com", "password": "Pass123!"},
    )
    assert resp.status_code == 302
    assert client.session.get("_auth_user_id")


def test_profile_requires_login_and_shows_role(client):
    resp = client.get(reverse("accounts:profile"))
    assert resp.status_code == 302

    User.objects.create_user(username="p1", email="p1@example.com", password="Pass123!")
    client.force_login(User.objects.get(email="p1@example.com"))
    resp = client.get(reverse("accounts:profile"))
    assert resp.status_code == 200
    assert b"Viewer" in resp.content


def test_logout_flow(client):
    User.objects.create_user(username="o1", email="o1@example.com", password="Pass123!")
    client.force_login(User.objects.get(email="o1@example.com"))
    resp = client.post(reverse("account_logout"))
    assert resp.status_code == 302
