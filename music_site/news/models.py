from django.db import models
from django.urls import reverse

from auth.models import CustomUser


class News(models.Model):
    title = models.CharField(max_length=128,
                             verbose_name='Заголовок')
    slug = models.SlugField(unique=True,
                            verbose_name='Человекопонятная ссылка')
    body = models.TextField(blank=False,
                            verbose_name='Текст')
    image = models.ImageField(upload_to='media/news/%Y/%m/%d/',
                              verbose_name='Изображение')
    author = models.ForeignKey(CustomUser,
                               on_delete=models.CASCADE,
                               blank=True,
                               null=True,
                               related_name='many_news',
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

    def get_absolute_url(self):
        return reverse('news:news_detail', args=[self.slug])

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-created', '-updated')
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'


class Comment(models.Model):
    text = models.TextField(blank=False,
                            verbose_name='Текст комментария')
    author = models.ForeignKey(CustomUser,
                               on_delete=models.CASCADE,
                               blank=True,
                               null=True,
                               related_name='comments',
                               verbose_name='Автор')
    likes = models.ManyToManyField(CustomUser,
                                   related_name='liked_comments',
                                   verbose_name='Лайки')
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name='Написан')
    updated = models.DateTimeField(auto_now=True,
                                   verbose_name='Изменён')
    published = models.BooleanField(default=False,
                                    verbose_name='Опубликован')
    news = models.ForeignKey(News,
                             null=True,
                             related_name='comments',
                             on_delete=models.CASCADE,
                             verbose_name='Новость')

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
