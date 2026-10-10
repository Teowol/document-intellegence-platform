"""Health check endpoint for Docker healthchecks and uptime monitoring."""

import json

from django.core.cache import cache
from django.db import connection
from django.http import HttpResponse
from django.views.decorators.http import require_GET


@require_GET
def healthz(request):
    """Report service readiness: database and Redis connectivity."""
    checks = {"database": "ok", "redis": "ok"}
    status = 200

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
    except Exception as exc:  # pragma: no cover - infrastructure failure path
        checks["database"] = f"error: {type(exc).__name__}"
        status = 503

    try:
        cache.set("healthz", "ping", timeout=5)
        if cache.get("healthz") != "ping":
            raise RuntimeError("cache read-back failed")
    except Exception as exc:  # pragma: no cover - infrastructure failure path
        checks["redis"] = f"error: {type(exc).__name__}"
        status = 503

    return HttpResponse(
        json.dumps({"status": "ok" if status == 200 else "degraded", **checks}),
        status=status,
        content_type="application/json",
    )
