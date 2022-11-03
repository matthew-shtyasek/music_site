from django.conf import settings
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords, truncatechars
from django.urls import reverse_lazy, reverse

from news.models import News


class NewsFeed(Feed):
    title = 'Musify - Музыка нас связала!'
    description = 'Последние новости с сайта Musify'
    link = '/'

    def items(self):
        return News.objects.filter(published=True)[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return f'{truncatechars(truncatewords(item.body, 40), 340)}' \
               f'<p>Статья была опубликована на <a href="{settings.CURRENT_HOST}{reverse("news:news_list")}">Musify</a></p>'
