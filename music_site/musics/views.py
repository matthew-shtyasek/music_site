from django.shortcuts import render
from django.views.generic import ListView

from musics.models import Song


class MostPopularMusicView(ListView):
    model = Song
    extra_context = {'current_page': 'music'}
    context_object_name = 'songs'
    template_name = 'musics/index.html'
