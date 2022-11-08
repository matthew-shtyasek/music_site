from celery import shared_task
from redis import StrictRedis

from . import models


@shared_task
def remove_discount(pk):
    redis = StrictRedis('localhost')
    incorrect_premiums = models.Premium.objects.filter(discount_id=pk)
    for premium in incorrect_premiums:
        premium.discount = None
        premium.save()
    redis.delete(f'discount:{pk}:task')
