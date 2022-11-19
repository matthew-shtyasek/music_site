from django.contrib.sitemaps.views import sitemap
from django.urls import path

from musics.sitemaps import SongSitemap, MusicianSitemap, MusicGroupSitemap
from musics.views import MostPopularMusicView, SongView, ArtistView, song_url_ajax_view

app_name = 'musics'

song_sitemaps = {
    'songs': SongSitemap,
}

artist_sitemaps = {
    'musicians': MusicianSitemap,
    'music_groups': MusicGroupSitemap,
}

urlpatterns = [
    path('songs/sitemap.xml/', sitemap, {'sitemaps': song_sitemaps}),
    path('artists/sitemap.xml/', sitemap, {'sitemaps': artist_sitemaps}),
    path('song/<slug:slug>/', SongView.as_view(), name='song'),
    path('artist/<slug:slug>/', ArtistView.as_view(), name='artist'),
    path('song/', song_url_ajax_view, name='get_song_ajax'),
    path('', MostPopularMusicView.as_view(), name='main'),
]
