"""Phase 3 tests: secure upload, RBAC on documents, malicious file rejection."""

import io
import zipfile

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from accounts.models import CustomUser
from documents.models import Document

pytestmark = pytest.mark.django_db

MINIMAL_PDF = b"%PDF-1.4\n1 0 obj<</Type/Catalog>>endobj\ntrailer<</Root 1 0 R>>"


@pytest.fixture(autouse=True)
def _media_root(settings, tmp_path):
    settings.MEDIA_ROOT = str(tmp_path)
    settings.MAX_UPLOAD_SIZE = 25 * 1024 * 1024


@pytest.fixture
def users():
    return {
        "owner": CustomUser.objects.create_user(
            username="owner", email="owner@example.com", password="Pass123!"
        ),
        "other": CustomUser.objects.create_user(
            username="other", email="other@example.com", password="Pass123!"
        ),
        "admin": CustomUser.objects.create_user(
            username="adm", email="adm@example.com", password="Pass123!",
            role=CustomUser.Roles.ADMIN,
        ),
        "editor": CustomUser.objects.create_user(
            username="edt", email="edt@example.com", password="Pass123!",
            role=CustomUser.Roles.EDITOR,
        ),
        "viewer": CustomUser.objects.create_user(
            username="vwr", email="vwr@example.com", password="Pass123!"
        ),
    }


def make_pdf(name="doc.pdf"):
    return SimpleUploadedFile(name, MINIMAL_PDF, content_type="application/pdf")


def upload(client, file):
    return client.post(
        reverse("documents:upload"),
        {"file": file, "title": "Test doc", "is_public": False},
    )


def make_document(owner, **kwargs):
    """Create a Document directly (bypasses upload flow) for RBAC tests."""
    from django.core.files.base import ContentFile

    doc = Document(
        owner=owner, title=kwargs.get("title", "t"),
        original_filename="t.pdf", doc_type=Document.DocType.PDF,
        is_public=kwargs.get("is_public", False),
    )
    doc.file.save("t.pdf", ContentFile(MINIMAL_PDF), save=True)
    doc.doc_type = "pdf"
    doc.save()
    return doc


# ----------------------------------------------------------------------
# Upload & validation (magic bytes)
# ----------------------------------------------------------------------

def test_upload_pdf_succeeds(client, users):
    client.force_login(users["owner"])
    resp = upload(client, make_pdf())
    assert resp.status_code == 302
    doc = Document.objects.get()
    assert doc.owner == users["owner"]
    assert doc.doc_type == Document.DocType.PDF
    assert doc.status == Document.Status.UPLOADED
    assert doc.size_bytes == len(MINIMAL_PDF)


def test_zip_file_rejected(client, users):
    """Zip (incl. zip-bomb style) content is not on the allowlist."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr("big.txt", b"0" * 10_000_000)  # highly compressible
    buf.seek(0)
    client.force_login(users["owner"])
    resp = upload(client, SimpleUploadedFile("bomb.zip", buf.getvalue()))
    assert resp.status_code == 200  # form re-rendered with errors
    assert Document.objects.count() == 0


def test_exe_disguised_as_pdf_rejected(client, users):
    """Fake extension cannot fool the magic-byte check."""
    client.force_login(users["owner"])
    resp = upload(client, SimpleUploadedFile("evil.pdf", b"MZ\x90\x00fake-exe"))
    assert resp.status_code == 200
    assert Document.objects.count() == 0


def test_empty_file_rejected(client, users):
    client.force_login(users["owner"])
    resp = upload(client, SimpleUploadedFile("empty.pdf", b""))
    assert resp.status_code == 200
    assert Document.objects.count() == 0


def test_oversized_file_rejected(client, users, settings):
    settings.MAX_UPLOAD_SIZE = 10
    client.force_login(users["owner"])
    resp = upload(client, make_pdf())
    assert resp.status_code == 200
    assert Document.objects.count() == 0


def test_upload_requires_login(client):
    resp = client.get(reverse("documents:upload"))
    assert resp.status_code == 302


# ----------------------------------------------------------------------
# Listing / visibility
# ----------------------------------------------------------------------

def test_list_shows_own_and_public_only(client, users):
    private = make_document(users["owner"], is_public=False)
    public = make_document(users["owner"], is_public=True)
    make_document(users["other"], is_public=False)

    client.force_login(users["other"])
    resp = client.get(reverse("documents:list"))
    pks = {d.pk for d in resp.context["object_list"]}
    assert pks == {public.pk, users["other"].documents.first().pk}


def test_detail_denied_for_private_doc(client, users):
    doc = make_document(users["owner"], is_public=False)
    client.force_login(users["viewer"])
    resp = client.get(reverse("documents:detail", args=[doc.pk]))
    assert resp.status_code == 403


def test_detail_public_doc_readable(client, users):
    doc = make_document(users["owner"], is_public=True)
    client.force_login(users["viewer"])
    resp = client.get(reverse("documents:detail", args=[doc.pk]))
    assert resp.status_code == 200


def test_admin_sees_everything(client, users):
    make_document(users["owner"], is_public=False)
    client.force_login(users["admin"])
    resp = client.get(reverse("documents:list"))
    assert resp.context["object_list"].count() == 1


# ----------------------------------------------------------------------
# Deletion (DoD: başkasının dosyası silinemez)
# ----------------------------------------------------------------------

def test_owner_can_delete_own(client, users):
    doc = make_document(users["owner"])
    client.force_login(users["owner"])
    resp = client.post(reverse("documents:delete", args=[doc.pk]))
    assert resp.status_code == 302
    assert Document.objects.count() == 0


def test_other_user_cannot_delete(client, users):
    doc = make_document(users["owner"])
    client.force_login(users["other"])
    resp = client.post(reverse("documents:delete", args=[doc.pk]))
    assert resp.status_code == 403
    assert Document.objects.count() == 1


def test_editor_cannot_delete_others_file(client, users):
    doc = make_document(users["owner"])
    client.force_login(users["editor"])
    resp = client.post(reverse("documents:delete", args=[doc.pk]))
    assert resp.status_code == 403
    assert Document.objects.count() == 1


def test_viewer_cannot_delete_anything(client, users):
    doc = make_document(users["owner"])
    client.force_login(users["viewer"])
    resp = client.post(reverse("documents:delete", args=[doc.pk]))
    assert resp.status_code == 403
    assert Document.objects.count() == 1


def test_admin_can_delete_any(client, users):
    doc = make_document(users["owner"])
    client.force_login(users["admin"])
    resp = client.post(reverse("documents:delete", args=[doc.pk]))
    assert resp.status_code == 302
    assert Document.objects.count() == 0
