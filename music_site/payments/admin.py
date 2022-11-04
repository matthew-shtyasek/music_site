from django.contrib import admin

from payments.models import Discount, Promo, Premium, PremiumType


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    fields = ('title',
              'description',
              'percent',
              'start',
              'end',
              'created',
              'updated')
    list_display = ('title',
                    'percent',
                    'start',
                    'end')
    list_editable = ('percent',)
    list_filter = ('start',
                   'end',
                   'created',
                   'updated')
    search_fields = ('title',
                     'description',
                     'percent')
    readonly_fields = ('created',
                       'updated')


@admin.register(Promo)
class PromoAdmin(admin.ModelAdmin):
    fields = ('promo',
              'discount',
              'is_active',
              'start',
              'end',
              'created',
              'updated')
    list_display = ('promo',
                    'is_active',
                    'start',
                    'end')
    list_editable = ('is_active',)
    list_filter = ('is_active',
                   'start',
                   'end',
                   'created',
                   'updated')
    search_fields = ('promo',)
    readonly_fields = ('created',
                       'updated')


@admin.register(PremiumType)
class PremiumTypeAdmin(admin.ModelAdmin):
    fields = ('type',
              'created',
              'updated')
    list_display = ('type',
                    'created',
                    'updated')
    search_fields = ('type',)
    list_filter = ('created',
                   'updated')
    readonly_fields = ('created',
                       'updated')



@admin.register(Premium)
class PremiumAdmin(admin.ModelAdmin):
    fields = ('name',
              'type',
              'months',
              'discount',
              'price',
              'created',
              'updated')
    list_display = ('name',
                    'type',
                    'months',
                    'price')
    list_editable = ('type',
                     'months',
                     'price')
    list_filter = ('type',
                   'created',
                   'updated')
    search_fields = ('name',
                     'months',
                     'price')
    readonly_fields = ('created',
                       'updated')
