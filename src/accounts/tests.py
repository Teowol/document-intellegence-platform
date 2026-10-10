"""Smoke tests for the accounts app (custom User model)."""

import pytest

from accounts.models import CustomUser

pytestmark = pytest.mark.django_db


def test_create_user_with_email():
    user = CustomUser.objects.create_user(
        username="ali", email="ali@example.com", password="S3cure-pass!"
    )
    assert user.email == "ali@example.com"
    assert user.is_active
    assert not user.is_staff
    assert str(user) == "ali@example.com"


def test_email_is_unique():
    CustomUser.objects.create_user(username="a", email="dup@example.com", password="x")
    with pytest.raises(Exception):
        CustomUser.objects.create_user(
            username="b", email="dup@example.com", password="x"
        )
