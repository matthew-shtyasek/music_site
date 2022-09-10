from django.urls import path

from musics.views import MostPopularMusicView

app_name = 'musics'

urlpatterns = [
    path('', MostPopularMusicView.as_view(), name='main'),
]
