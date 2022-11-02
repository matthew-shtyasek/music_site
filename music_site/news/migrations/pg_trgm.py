from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('news', '0006_auto_20221030_2346'),
    ]
    operations = [
        migrations.RunSQL('CREATE EXTENSION IF NOT EXISTS pg_trgm'),
    ]