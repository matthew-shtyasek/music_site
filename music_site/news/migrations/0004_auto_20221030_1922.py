# Generated by Django 3.2.15 on 2022-10-30 14:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news', '0003_auto_20221030_1919'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='comments',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='news', to='news.comment', verbose_name='Комментарии'),
        ),
        migrations.AlterField(
            model_name='news',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='many_news', to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
    ]
