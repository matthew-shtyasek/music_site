from django.contrib.sitemaps import Sitemap

from musics.models import Song, Musician, MusicGroup


class SongSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.7

    def items(self):
        return Song.objects.all()

    def lastmod(self, obj):
        return obj.updated


class MusicianSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5

    def items(self):
        return Musician.objects.all()

    def lastmod(self, obj):
        return obj.updated


class MusicGroupSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5

    def items(self):
        return MusicGroup.objects.all()

    def lastmod(self, obj):
        return obj.updated
