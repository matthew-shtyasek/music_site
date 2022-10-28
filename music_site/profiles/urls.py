from django.urls import path

from profiles.views import UserProfileView, add_song_to_playlist, PlaylistCreateView, PlaylistDetailView

app_name = 'profiles'

urlpatterns = [
    path('playlist/<int:pk>/', PlaylistDetailView.as_view(), name='detail_playlist'),
    path('create_playlist/', PlaylistCreateView.as_view(), name='create_playlist'),
    path('add_song/<int:song_id>/<int:playlist_id>/', add_song_to_playlist, name='add_song'),
    path('<int:pk>/', UserProfileView.as_view(), name='profile'),
    path('', UserProfileView.as_view(), name='current_profile'),
]
