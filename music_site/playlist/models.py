from django.conf import settings
from django.db import models

from musics.models import Song


class Playlist(models.Model):
    name = models.CharField(max_length=64,
                            verbose_name='Название')
    icon = models.ImageField(upload_to='playlist/icons/%Y/%m/%d/',
                             default='default_icon.jpg',
                             verbose_name='Обложка')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE,
                              related_name='playlists',
                              db_index=True,
                              verbose_name='Автор')
    songs = models.ManyToManyField(Song,
                                   related_name='playlists',
                                   verbose_name='Песни')
    subscribers = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                         related_name='subscribed_playlists')
    public = models.BooleanField(default=True,
                                 verbose_name='Публичный')
    created = models.DateTimeField(auto_now_add=True,
                                  verbose_name='Создан')
    updated = models.DateTimeField(auto_now=True,
                                  verbose_name='Изменён')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'Плейлист'
        verbose_name_plural = 'Плейлисты'
