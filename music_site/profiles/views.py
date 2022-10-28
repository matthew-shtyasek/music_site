from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import DetailView, CreateView

from auth.models import CustomUser
from musics.forms import PlaylistCreateForm
from musics.models import Song
from profiles.models import Playlist


class UserProfileView(DetailView):
    model = CustomUser
    context_object_name = 'current_user'
    template_name = 'profiles/user_profile.html'
    extra_context = dict()

    def get(self, request, pk=0):
        self.extra_context = dict()
        if pk == 0:
            context = {'current_user': request.user}
            return render(request, self.template_name, context)
        else:
            public_playlists = Playlist.objects.filter(owner_id=pk, public=True)
            private_playlists = request.user.playlists.filter(owner_id=pk, public=False)
            self.extra_context['public_playlists'] = public_playlists
            self.extra_context['private_playlists'] = private_playlists
            return super().get(request, pk)


class PlaylistCreateView(CreateView):
    form_class = PlaylistCreateForm
    model = Playlist
    template_name = 'profiles/playlists/create_playlist.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for field in form:
            if field.name == 'public':
                field.label_class = 'form-check-label'
            else:
                field.label_class = ''
        return form

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        if self.request.is_ajax():
            return JsonResponse(dict())
        return redirect(self.get_success_url())

    def get(self, request):
        if request.is_ajax():

            self.template_name = 'profiles/playlists/create_playlist_ajax.html'
        else:
            self.template_name = 'profiles/playlists/create_playlist.html'
        return super().get(request)


def add_song_to_playlist(request, song_id, playlist_id):
    if request.is_ajax():
        song = Song.objects.get(id=song_id)
        playlist = Playlist.objects.get(id=playlist_id)
        playlist.songs.add(song)
        playlist.save()
        return JsonResponse(dict())
    raise PermissionDenied()


class PlaylistDetailView(DetailView):
    model = Playlist
    template_name = 'profiles/playlists/playlist_detail.html'
    context_object_name = 'playlist'
