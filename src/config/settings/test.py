"""Test settings: inherit everything, speed up password hashing."""

from config.settings.base import *  # noqa: F401,F403

PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
