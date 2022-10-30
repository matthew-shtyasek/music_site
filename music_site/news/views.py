from django.shortcuts import render
from django.views.generic import ListView, DetailView

from news.models import News


class NewsListView(ListView):
    model = News
    template_name = 'news/news_list.html'

    def get_queryset(self):
        return self.model.objects.filter(published=True)


class NewsDetailView(DetailView):
    model = News
    template_name = 'news/news_detail.html'

    def get_queryset(self):
        return super().get_queryset().filter(published=True)
