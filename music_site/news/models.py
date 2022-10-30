from django.db import models

from auth.models import CustomUser


class News(models.Model):
    title = models.CharField(max_length=128,
                             verbose_name='Заголовок')
    slug = models.SlugField(unique=True,
                            verbose_name='Человекопонятная ссылка')
    body = models.TextField(blank=False,
                            verbose_name='Текст')
    image = models.ImageField(upload_to='media/news/%Y/%m/%d/')
    author = models.ForeignKey(CustomUser,
                               on_delete=models.CASCADE,
                               blank=True,
                               null=True,
                               related_name='news',
                               verbose_name='Автор')
    likes = models.ManyToManyField(CustomUser,
                                   related_name='liked_news',
                                   verbose_name='Лайки')
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name='Создана')
    updated = models.DateTimeField(auto_now=True,
                                   verbose_name='Изменена')
    published = models.BooleanField(default=False,
                                    verbose_name='Опубликована')

    class Meta:
        ordering = ('-created', '-updated')
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

