from Lib import os
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError
from django.views import View
from django.views.generic import ListView, DetailView

from musics.models import Song, Artist, MusicGroup, Musician


class MostPopularMusicView(ListView):
    model = Song
    extra_context = {'current_page': 'music'}
    context_object_name = 'songs'
    template_name = 'musics/index.html'
    ajax_template_name = 'musics/music_list_wd.html'

    def get(self, request, *args, **kwargs):
        objects = self.model.objects.all()

        try:
            page = request.GET['page']
        except MultiValueDictKeyError:
            page = 1

        try:
            max_items = request.GET['max_items']
        except MultiValueDictKeyError:
            max_items = 20

        paginator = Paginator(objects, per_page=max_items, allow_empty_first_page=False)

        try:
            if int(page) > paginator.num_pages:
                raise EmptyPage
            objects = paginator.get_page(page)
        except PageNotAnInteger:
            objects = paginator.get_page(1)
        except EmptyPage:
            if request.is_ajax():
                return HttpResponse('')
            objects = paginator.get_page(paginator.num_pages)

        context = {self.context_object_name: objects,
                   'current_page': 'music'}
        template_name = self.template_name

        if request.is_ajax():
            template_name = self.ajax_template_name
        return render(request, template_name=template_name, context=context)


class SongView(DetailView):
    model = Song
    template_name = 'musics/song.html'

    def get_context_data(self, **kwargs):
        song = kwargs['object']
        songs = Song.objects \
            .filter(album__artist_id=song.album.artist_id, album__artist_type=song.album.artist_type)\
            .exclude(slug=song.slug)
        context = {
            'song': song,
            'songs': songs,
        }
        return context


class ArtistView(View):
    def get(self, request, slug):
        try:
            artist = MusicGroup.objects.get(slug=slug)
            template_name = 'musics/group.html'
            artist_type = 'musicgroup'
        except MusicGroup.DoesNotExist:
            artist = Musician.objects.get(slug=slug)
            template_name = 'musics/musician.html'
            artist_type = 'musician'

        songs = Song.objects.filter(album__artist_id=artist.id, album__artist_type__model=artist_type)
        pg = Paginator(object_list=songs, per_page=8)
        try:
            songs = pg.page(request.GET.get('page', 1))
        except PageNotAnInteger:
            songs = pg.page(1)
        except EmptyPage:
            return JsonResponse('')

        if request.is_ajax():
            return JsonResponse({'songs': songs})

        context = {
            'artist': artist,
            'songs': songs,
        }
        return render(request, template_name=template_name, context=context)


def song_url_ajax_view(request):
    if not request.is_ajax():
        raise PermissionError('Request must be ajax')
    '''fname = Song.objects.get(pk=request.GET['pk']).track.path
    f = open(fname, "rb")
    response = HttpResponse()
    response.write(f.read())
    response['Content-Type'] = 'audio/mp3'
    response['Content-Length'] = os.path.getsize(fname)
    return response'''
    return JsonResponse({'song_url': Song.objects.get(pk=request.GET['pk']).track.url })
