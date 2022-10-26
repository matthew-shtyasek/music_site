from django.urls import path

from profiles.views import UserProfileView, add_song_to_playlist

app_name = 'profiles'

urlpatterns = [
    path('add_song/<int:song_id>/<int:playlist_id>/', add_song_to_playlist, name='add_song'),
    path('<int:pk>/', UserProfileView.as_view(), name='profile'),
    path('', UserProfileView.as_view(), name='current_profile'),
]
