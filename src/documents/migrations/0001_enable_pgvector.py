from django.db import migrations


class Migration(migrations.Migration):
    """Ensure the pgvector extension is available before any VectorField."""

    initial = True

    dependencies = []

    operations = [
        migrations.RunSQL(
            sql="CREATE EXTENSION IF NOT EXISTS vector;",
            reverse_sql="DROP EXTENSION IF EXISTS vector;",
        ),
    ]
