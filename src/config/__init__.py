# Ensure the Celery app is loaded when Django starts (shared task registry).
from config.celery import app as celery_app

__all__ = ("celery_app",)
