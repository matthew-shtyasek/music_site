from django.contrib.sitemaps import Sitemap

from news.models import News


class NewsSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.7

    def items(self):
        return News.objects.filter(published=True)

    def lastmod(self, obj):
        return obj.updated
