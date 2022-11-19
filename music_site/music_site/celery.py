import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'music_site.settings')

app = Celery('music_site')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
