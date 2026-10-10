import django.db.models.deletion

from django.db import migrations, models


class Migration(migrations.Migration):
    """Chunk.document becomes non-null (table was empty; no backfill needed)."""

    dependencies = [
        ("documents", "0003_alter_documentchunk_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="documentchunk",
            name="document",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="chunks",
                to="documents.document",
            ),
        ),
    ]
