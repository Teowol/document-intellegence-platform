"""Background tasks for document processing (Phase 4).

Phase 5 will replace the placeholder body with real parsing/chunking.
The status machine is already production-shaped:

    uploaded -> processing -> ready
                        \\-----> error (any unexpected failure)
"""

import logging

from celery import shared_task
from django.db import transaction

from .models import Document

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=5)
def process_document(self, document_id: int) -> str:
    """
    Mark a document ready for downstream phases.

    Simulated pipeline cost keeps the state transitions observable in dev
    (you can watch status flip uploaded -> processing -> ready).
    """
    try:
        doc = Document.objects.get(pk=document_id)
    except Document.DoesNotExist:
        logger.warning("process_document: document %s vanished; skipping", document_id)
        return "missing"

    doc.status = Document.Status.PROCESSING
    doc.save(update_fields=["status", "updated_at"])

    try:
        # Phase 5 will parse + chunk here; nothing to do yet.
        pass
    except Exception as exc:  # pragma: no cover - placeholder until Phase 5
        doc.status = Document.Status.ERROR
        doc.error_message = str(exc)[:2000]
        doc.save(update_fields=["status", "error_message", "updated_at"])
        raise

    with transaction.atomic():
        doc.refresh_from_db()
        if doc.status != Document.Status.PROCESSING:
            logger.warning("document %s changed state mid-flight", document_id)
            return doc.status
        doc.status = Document.Status.READY
        doc.error_message = ""
        doc.save(update_fields=["status", "error_message", "updated_at"])

    logger.info("document %s processed", document_id)
    return doc.status
