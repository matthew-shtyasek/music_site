from django.contrib.contenttypes import fields
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Artist(models.Model):
    slug = models.SlugField(unique=True,
                            db_index=True,
                            verbose_name='Человекопонятная ссылка')
    songs = fields.GenericRelation('Song',
                                   content_type_field='content_type',
                                   object_id_field='object_id',
                                   related_name='artists')
    description = models.TextField(blank=True,
                                   verbose_name='Биография')
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
                                  verbose_name='Отчество')

    @property
    def name(self):
        return str(self)

    def get_absolute_url(self):
        return '#'

    def __str__(self):
        name = f'{self.last_name} {self.first_name[0]}.'
        try:
            return name + f'{self.patronymic[0]}.'
        except AttributeError:
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

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name', )
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'


class Song(models.Model):
    artist_type = models.ForeignKey(ContentType,
                                    on_delete=models.CASCADE,
                                    limit_choices_to={'model__in': ('musician', 'musicgroup')})
    artist_id = models.PositiveIntegerField()
    artist = fields.GenericForeignKey('artist_type', 'artist_id')

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
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name='Запись создана')
    updated = models.DateTimeField(auto_now=True,
                                   verbose_name='Запись изменена')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('written', 'name')
        verbose_name = 'Песня'
        verbose_name_plural = 'Песни'


MusicGroup._meta.get_field('date_of_birth').verbose_name = 'Дата основания'
MusicGroup._meta.get_field('date_of_death').verbose_name = 'Дата распада'
MusicGroup._meta.get_field('description').verbose_name = 'Описание'
