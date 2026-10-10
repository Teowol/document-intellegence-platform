from django.db import models
from pgvector.django import VectorField

EMBEDDING_DIMENSIONS = 1536  # text-embedding-3-small output size


class DocumentChunk(models.Model):
    """
    Minimal chunk model for Phase 1 (pgvector migration sanity check).

    Phase 3 will extend this with a Document FK; Phase 6 fills the
    embedding column during batch embedding.
    """

    text = models.TextField()
    embedding = VectorField(
        dimensions=EMBEDDING_DIMENSIONS,
        blank=True,
        null=True,
    )
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Document chunk"
        verbose_name_plural = "Document chunks"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Chunk {self.pk} ({len(self.text)} chars)"
