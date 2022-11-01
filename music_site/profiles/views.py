import redis
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import DetailView, CreateView

from auth.models import CustomUser
from musics.forms import PlaylistCreateForm
from musics.models import Song
from profiles.models import Playlist
from profiles.recommender import get_recommended_songs

r = redis.StrictRedis('localhost')


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
            self.extra_context['recommended_songs'] = get_recommended_songs(request.user)
            self.extra_context['current_page'] = 'profile'
            return super().get(request, pk)


class PlaylistCreateView(CreateView):
    form_class = PlaylistCreateForm
    model = Playlist
    template_name = 'profiles/playlists/create_playlist.html'
    extra_context = {'current_page': 'profile'}

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
            return JsonResponse({'playlist_id': self.object.pk,
                                 'playlist_name': self.object.name})
        return redirect(self.get_success_url())

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect(reverse('auth:login'), kwargs={'next': f'{request.build_absolute_uri()}'})
        if request.is_ajax():
            self.template_name = 'profiles/playlists/create_playlist_ajax.html'
        else:
            self.template_name = 'profiles/playlists/create_playlist.html'
        return super().get(request)


class PlaylistDetailView(DetailView):
    model = Playlist
    template_name = 'profiles/playlists/playlist_detail.html'
    context_object_name = 'playlist'
    extra_context = {'current_page': 'profile'}


@login_required
def add_song_to_playlist(request, song_id, playlist_id):
    if request.is_ajax():
        song = Song.objects.get(id=song_id)
        playlist = Playlist.objects.get(id=playlist_id)
        playlist.songs.add(song)
        playlist.save()
        r.sadd(f'user:playlists:{request.user.id}', f'song:{song_id}')

        incr_value = 1
        try:
            incr_value = int(r.get(f'song:{song_id}')) + 1
        except:
            pass
        r.set(f'song:{song_id}', incr_value)

        for song_item in playlist.songs.all():
            if song_item != song:
                r.zincrby(f'song:{song_item.id}:z', 1, f'song:{song_id}')
                r.zincrby(f'song:{song_id}:z', 1, f'song:{song_item.id}')
        return JsonResponse(dict())
    raise PermissionDenied()

