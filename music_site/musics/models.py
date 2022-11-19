from django.contrib.contenttypes import fields
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse


class ModelLogging(models.Model):
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name='Запись добавлена')
    updated = models.DateTimeField(auto_now=True,
                                   verbose_name='Запись изменена')
    class Meta:
        abstract = True


class Artist(ModelLogging):
    slug = models.SlugField(unique=True,
                            db_index=True,
                            verbose_name='Человекопонятная ссылка')
    description = models.TextField(blank=True,
                                   verbose_name='Биография')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d',
                              null=True,
                              blank=True,
                              verbose_name='Фотография')
    date_of_birth = models.DateField(verbose_name='Дата рождения')
    date_of_death = models.DateField(blank=True,
                                     null=True,
                                     verbose_name='Дата смерти')

    class Meta:
        abstract = True


class Musician(Artist):
    first_name = models.CharField(max_length=64,
                                  verbose_name='Имя')
    last_name = models.CharField(max_length=64,
                                 verbose_name='Фамилия')
    patronymic = models.CharField(max_length=64,
                                  blank=True,
                                  null=True,
                                  verbose_name='Отчество')

    @property
    def name(self):
        return f'{self.last_name} ' \
               f'{self.first_name}' \
               f'{(" " + self.patronymic) if self.patronymic else ""} '

    def get_absolute_url(self):
        return reverse('musics:artist', args=[self.slug])

    def __str__(self):
        name = f'{self.last_name} {self.first_name[0]}.'
        try:
            return name + f'{self.patronymic[0]}.'
        except TypeError:
            return name

    class Meta:
        ordering = ('last_name', )
        verbose_name = 'Музыкант'
        verbose_name_plural = 'Музыканты'


class MusicGroup(Artist):
    musicians = models.ManyToManyField(Musician,
                                       related_name='music_groups',
                                       verbose_name='Музыканты')
    name = models.CharField(max_length=200,
                            verbose_name='Название')

    def get_absolute_url(self):
        return reverse('musics:artist', args=[self.slug])

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name', )
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'


class Song(ModelLogging):
    album = models.ForeignKey('Album',
                              on_delete=models.CASCADE,
                              verbose_name='Альбом')

    name = models.CharField(max_length=200,
                            verbose_name='Название')
    description = models.TextField(blank=True,
                                   verbose_name='Описание')
    track = models.FileField(upload_to='songs/%Y/%m/%d/',
                             verbose_name='Трек')
    slug = models.SlugField(unique=True,
                            db_index=True,
                            verbose_name='Человекопонятная ссылка')
    written = models.DateField(blank=False,
                               verbose_name='Написана')

    def album_genre(self):
        return self.album.genre

    def album_artist(self):
        return self.album.artist

    album_genre.short_description = 'Жанр'
    album_artist.short_description = 'Исполнитель'

    def get_absolute_url(self):
        return reverse('musics:song', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('written', 'name')
        verbose_name = 'Песня'
        verbose_name_plural = 'Песни'


class Album(ModelLogging):
    name = models.CharField(blank=True,
                            max_length=64,
                            verbose_name='Название альбома')
    slug = models.SlugField(max_length=64,
                            verbose_name='Человекопонятная ссылка')
    image = models.ImageField(upload_to='album_covers/%Y/%m/%d/',
                              verbose_name='Обложка альбома')
    genre = models.ForeignKey('Genre',
                              on_delete=models.CASCADE,
                              verbose_name='Жанр')
    artist_type = models.ForeignKey(ContentType,
                                    on_delete=models.CASCADE,
                                    limit_choices_to={'model__in': ('musician', 'musicgroup')})
    artist_id = models.PositiveIntegerField(verbose_name='ID исполнителя')
    artist = fields.GenericForeignKey('artist_type',
                                      'artist_id')
    is_single = models.BooleanField(verbose_name='Сингл')
    released = models.DateField(blank=False,
                                verbose_name='Выпущен')

    def get_absolute_url(self):
        return '#'

    def __str__(self):
        return 'Сингл' if self.is_single else self.name

    class Meta:
        ordering = ('name', 'created')
        verbose_name = 'Альбом'
        verbose_name_plural = 'Альбомы'


class Genre(models.Model):
    name = models.CharField(max_length=64,
                            verbose_name='Жанр')
    slug = models.SlugField(unique=True,
                            db_index=True,
                            verbose_name='Человекопонятная ссылка')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


MusicGroup._meta.get_field('date_of_birth').verbose_name = 'Дата основания'
MusicGroup._meta.get_field('date_of_death').verbose_name = 'Дата распада'
MusicGroup._meta.get_field('description').verbose_name = 'Описание'
