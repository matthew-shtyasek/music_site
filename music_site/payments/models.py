from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.crypto import get_random_string


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

    def __str__(self):
        return f'«{self.title}» {self.percent}%'

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Скидка'
        verbose_name_plural = 'Скидки'


class Promo(StockBase):
    discount = models.OneToOneField(Discount,
                                    on_delete=models.CASCADE,
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
    type = models.ForeignKey(PremiumType,
                             on_delete=models.CASCADE,
                             verbose_name='Тип')
    months = models.PositiveIntegerField(verbose_name='Активен (в месяцах)')
    discount = models.OneToOneField(Discount,
                                    on_delete=models.SET_NULL,
                                    null=True,
                                    default=None,
                                    verbose_name='Скидка')
    price = models.DecimalField(max_digits=10,
                                decimal_places=2,
                                verbose_name='Цена')
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name='Создан')
    updated = models.DateTimeField(auto_now=True,
                                   verbose_name='Изменён')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Премиум'
        verbose_name_plural = 'Премиумы'

Promo._meta.get_field('created').verbose_name = 'Создан'
Promo._meta.get_field('updated').verbose_name = 'Изменён'
