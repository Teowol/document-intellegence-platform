from django.contrib import admin

from .models import Document, DocumentChunk


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "owner",
        "doc_type",
        "status",
        "size_bytes",
        "is_public",
        "created_at",
    )
    list_filter = ("status", "doc_type", "is_public")
    search_fields = ("title", "original_filename", "owner__email")
    readonly_fields = ("mime_type", "size_bytes", "original_filename")


@admin.register(DocumentChunk)
class DocumentChunkAdmin(admin.ModelAdmin):
    list_display = ("pk", "document", "chunk_index", "page_number")
    list_filter = ("document__doc_type",)
    search_fields = ("text",)
