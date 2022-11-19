import redis
from celery import uuid
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string

from music_site.celery import app
from payments.tasks import remove_discount


class StockBase(models.Model):
    start = models.DateTimeField(verbose_name='Начало')
    end = models.DateTimeField(verbose_name='Конец')

    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name='Создана')
    updated = models.DateTimeField(auto_now=True,
                                   verbose_name='Изменена')

    class Meta:
        abstract = True


class Discount(StockBase):
    title = models.CharField(max_length=128,
                             verbose_name='Название')
    description = models.TextField(blank=False,
                                   verbose_name='Описание')

    percent = models.IntegerField(default=10,
                                  validators=[
                                      MinValueValidator(1),
                                      MaxValueValidator(100)],
                                  verbose_name='Размер')

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        task = remove_discount.apply_async(kwargs={'pk': self.pk}, eta=self.end, task_id=f'discount:{self.pk}:task')
        app.control.revoke(f'discount:{self.pk}:task')

    def __str__(self):
        return f'«{self.title}» {self.percent}%'

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Скидка'
        verbose_name_plural = 'Скидки'


class Promo(StockBase):
    discount = models.ForeignKey(Discount,
                                 on_delete=models.CASCADE,
                                 related_name='promos',
                                 verbose_name='Скидка')
    promo = models.CharField(max_length=64,
                             blank=True,
                             verbose_name='Промокод')

    is_active = models.BooleanField(default=True,
                                    verbose_name='Активен')

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.promo:
            self.promo = get_random_string(length=64)
        return super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return f'{self.promo}'

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоды'


class PremiumType(models.Model):
    type = models.CharField(max_length=32,
                            unique=True,
                            db_index=True,
                            verbose_name='Тип')
    level = models.PositiveIntegerField(default=0,
                                        verbose_name='Уровень')
    public_playlists = models.PositiveIntegerField(default=8,
                                                   verbose_name='Количество публичных плейлистов')
    private_playlists = models.PositiveIntegerField(default=5,
                                                    verbose_name='Количество скрытых плейлистов')
    songs_per_playlist = models.PositiveIntegerField(default=50,
                                                     verbose_name='Максимальное количество песен в плейлисте')
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name='Создан')
    updated = models.DateTimeField(auto_now=True,
                                   verbose_name='Изменён')

    def __str__(self):
        return self.type

    class Meta:
        ordering = ('type',)
        verbose_name = 'Тип премиум-аккаунта'
        verbose_name_plural = 'Типы премиум-аккаунтов'


class Premium(models.Model):
    name = models.CharField(max_length=64,
                            verbose_name='Название')
    description = models.TextField(blank=False,
                                   verbose_name='Описание')
    type = models.ForeignKey(PremiumType,
                             on_delete=models.CASCADE,
                             related_name='premiums',
                             verbose_name='Тип')
    months = models.PositiveIntegerField(verbose_name='Активен (в месяцах)')
    discount = models.ForeignKey(Discount,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True,
                                 default=None,
                                 related_name='premiums',
                                 verbose_name='Скидка')
    price = models.DecimalField(max_digits=10,
                                decimal_places=2,
                                verbose_name='Цена')
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name='Создан')
    updated = models.DateTimeField(auto_now=True,
                                   verbose_name='Изменён')

    def get_result_price(self):
        if self.discount:
            return self.price - self.price * self.discount.percent / 100
        return self.price

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Премиум'
        verbose_name_plural = 'Премиумы'


class Receipt(models.Model):
    premium = models.ForeignKey(Premium,
                                on_delete=models.DO_NOTHING,
                                related_name='receipts',
                                verbose_name='Премиум')
    owner = models.ForeignKey('custom_auth.CustomUser',
                              on_delete=models.DO_NOTHING,
                              related_name='receipts',
                              verbose_name='Покупатель')
    discount = models.ForeignKey(Discount,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True,
                                 default=None,
                                 related_name='receipts',
                                 verbose_name='Скидка')
    price = models.DecimalField(max_digits=10,
                                decimal_places=2,
                                verbose_name='Цена')
    transaction_date = models.DateTimeField(auto_now_add=True,
                                            verbose_name='Дата сделки')
    premium_end_date = models.DateTimeField(null=True,
                                            verbose_name='Дата окончания премиума')

    def get_result_price(self):
        if self.discount:
            return self.price - self.price * self.discount.percent / 100
        return self.price

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.premium_end_date = timezone.now() + timezone.timedelta(days=self.premium.months*30)
        self.discount = self.premium.discount
        self.price = self.premium.price
        return super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return f'Чек №{self.pk}'

    class Meta:
        ordering = ('-transaction_date',)
        verbose_name = 'Чек'
        verbose_name_plural = 'Чеки'


Promo._meta.get_field('created').verbose_name = 'Создан'
Promo._meta.get_field('updated').verbose_name = 'Изменён'
