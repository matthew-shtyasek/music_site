# Generated by Django 3.2.15 on 2022-10-26 15:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('musics', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Название')),
                ('icon', models.ImageField(default='default_icon.jpg', upload_to='playlist/icons/%Y/%m/%d/', verbose_name='Обложка')),
                ('public', models.BooleanField(default=True, verbose_name='Публичный')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Изменён')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='playlists', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('songs', models.ManyToManyField(related_name='playlists', to='musics.Song', verbose_name='Песни')),
                ('subscribers', models.ManyToManyField(related_name='subscribed_playlists', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Плейлист',
                'verbose_name_plural': 'Плейлисты',
                'ordering': ('name',),
            },
        ),
    ]
