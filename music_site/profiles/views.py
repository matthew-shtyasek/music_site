from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import DetailView

from auth.models import CustomUser
from musics.models import Song
from profiles.models import Playlist


class UserProfileView(DetailView):
    model = CustomUser
    context_object_name = 'current_user'
    template_name = 'profiles/user_profile.html'

    def get(self, request, pk=0):
        if pk == 0:
            context = {'current_user': request.user}
            return render(request, self.template_name, context)
        else:
            return super().get(request, pk)


def add_song_to_playlist(request, song_id, playlist_id):
    if request.is_ajax():
        song = Song.objects.get(id=song_id)
        playlist = Playlist.objects.get(id=playlist_id)
        playlist.songs.add(song)
        playlist.save()
        return JsonResponse('')
    raise PermissionDenied()
