"""File validation: magic-byte sniffing, size limit, filename sanitizing."""

import magic
from django.core.exceptions import ValidationError
from django.utils.text import get_valid_filename

from .models import Document

# Mimes detectable purely from content.
_CONTENT_MIMES = {
    "application/pdf": Document.DocType.PDF,
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": (
        Document.DocType.XLSX
    ),
}

# Text formats share "text/plain"-ish mimes; the extension disambiguates
# (magic bytes cannot tell csv/md/txt apart).
_TEXT_MIMES = {"text/plain", "text/csv", "application/csv", "text/markdown"}
_TEXT_EXT_TO_TYPE = {
    "txt": Document.DocType.TXT,
    "md": Document.DocType.MD,
    "markdown": Document.DocType.MD,
    "csv": Document.DocType.CSV,
}


def _sniff_mime(header: bytes) -> str:
    return magic.from_buffer(header, mime=True)


def sniff_doc_type(fileobj) -> tuple[str, str]:
    """
    Return (doc_type, mime_type) detected from the file's real content.

    Raises ValidationError for unsupported or unknown content.
    """
    header = fileobj.read(8192)
    fileobj.seek(0)
    mime = _sniff_mime(header).lower()

    if mime in _CONTENT_MIMES:
        return _CONTENT_MIMES[mime], mime

    if mime in _TEXT_MIMES:
        ext = fileobj.name.rsplit(".", 1)[-1].lower() if "." in fileobj.name else ""
        doc_type = _TEXT_EXT_TO_TYPE.get(ext)
        if doc_type:
            return doc_type, mime

    raise ValidationError(
        f"Unsupported or unrecognized file content (detected: {mime or 'unknown'})."
    )


def sanitize_filename(name: str) -> str:
    """Strip paths and neutralize risky characters; keep the real name."""
    return get_valid_filename(name.rsplit("\\", 1)[-1].rsplit("/", 1)[-1])


def validate_upload(fileobj) -> tuple[str, str]:
    """Full server-side validation: size limit, non-empty, magic-byte type."""
    from django.conf import settings as dj_settings

    max_size = getattr(dj_settings, "MAX_UPLOAD_SIZE", 25 * 1024 * 1024)

    if fileobj.size == 0:
        raise ValidationError("Empty files are not allowed.")
    if fileobj.size > max_size:
        raise ValidationError(
            f"File too large ({fileobj.size} bytes). Limit is {max_size} bytes."
        )

    return sniff_doc_type(fileobj)
