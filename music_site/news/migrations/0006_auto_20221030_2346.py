# Generated by Django 3.2.15 on 2022-10-30 18:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0005_alter_comment_text'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='comments',
        ),
        migrations.AddField(
            model_name='comment',
            name='news',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='news.news', verbose_name='Новость'),
        ),
    ]
