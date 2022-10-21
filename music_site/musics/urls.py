from django.urls import path

from musics.views import MostPopularMusicView, SongView, ArtistView

app_name = 'musics'

urlpatterns = [
    path('song/<slug:slug>/', SongView.as_view(), name='song'),
    path('artist/<slug:slug>/', ArtistView.as_view(), name='artist'),
    path('', MostPopularMusicView.as_view(), name='main'),
]
