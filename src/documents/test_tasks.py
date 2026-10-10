"""Phase 4 tests: Celery task drives the document status machine."""

import pytest
from django.core.files.base import ContentFile

from accounts.models import CustomUser
from documents.models import Document
from documents.tasks import process_document

pytestmark = pytest.mark.django_db

MINIMAL_PDF = b"%PDF-1.4\n1 0 obj<</Type/Catalog>>endobj\ntrailer<</Root 1 0 R>>"


@pytest.fixture(autouse=True)
def _eager(settings, tmp_path):
    """Run tasks synchronously and store results in memory during tests."""
    settings.CELERY_TASK_ALWAYS_EAGER = True
    settings.CELERY_TASK_EAGER_PROPAGATES = True
    settings.MEDIA_ROOT = str(tmp_path)


@pytest.fixture
def user():
    return CustomUser.objects.create_user(
        username="u", email="u@example.com", password="Pass123!"
    )


def make_doc(owner):
    doc = Document(
        owner=owner, title="t", original_filename="t.pdf", doc_type="pdf"
    )
    doc.file.save("t.pdf", ContentFile(MINIMAL_PDF), save=True)
    return doc


def test_task_moves_uploaded_to_ready(user):
    doc = make_doc(user)
    assert doc.status == Document.Status.UPLOADED

    result = process_document.delay(doc.pk)

    assert result.get() == Document.Status.READY
    doc.refresh_from_db()
    assert doc.status == Document.Status.READY
    assert doc.error_message == ""


def test_task_marks_error_when_missing(user, settings, monkeypatch):
    """A vanished document is reported, not crash-looped."""
    result = process_document.delay(99999)
    assert result.get() == "missing"


def test_uploaded_doc_transitions_via_helper(user):
    doc = make_doc(user)
    doc.status = Document.Status.PROCESSING
    doc.save(update_fields=["status"])
    process_document.delay(doc.pk).get()
    doc.refresh_from_db()
    assert doc.status == Document.Status.READY
