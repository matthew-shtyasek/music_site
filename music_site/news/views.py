from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.postgres.search import SearchVector, SearchQuery, TrigramSimilarity, SearchRank
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView

from news.forms import CommentForm, NewsForm
from news.models import News, Comment


class NewsListView(ListView):
    model = News
    template_name = 'news/news_list.html'
    extra_context = {'current_page': 'news',
                     'current_sort': 'Времени публикации (от новых к старым)',
                     'sort_types': {'-created': 'Времени публикации (от новых к старым)',
                                    'created': 'Времени публикации (от старых к новым)',
                                    '-updated': 'Времени последнего изменения (от новых к старым)',
                                    'updated': 'Времени последнего изменения (от старых к новым)',
                                    'title': 'Алфавиту (а-я)',
                                    '-title': 'Алфавиту (я-а)'}}

    def get_queryset(self):
        queryset = super().get_queryset().filter(published=True)

        if self.request.method == 'GET':
            if 'sort' in self.request.GET:
                queryset = queryset.order_by(self.request.GET['sort'])
                self.extra_context['current_sort'] = self.extra_context['sort_types'][self.request.GET['sort']]
            if 'search' in self.request.GET and self.request.GET['search']:
                vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
                query = SearchQuery(self.request.GET['search'])
                _queryset = queryset\
                    .annotate(search=vector, rank=SearchRank(vector, query))\
                    .filter(search=query)\
                    .order_by('-rank')

                query = self.request.GET['search'].replace('+', ' ')
                trigram_similarity = TrigramSimilarity('title', query)
                queryset = _queryset or queryset\
                    .annotate(similarity=trigram_similarity)\
                    .filter(similarity__gt=0.15)\
                    .order_by('-similarity')

        return queryset


class NewsDetailView(DetailView):
    model = News
    template_name = 'news/news_detail.html'

    def get_queryset(self):
        return super().get_queryset().filter(published=True)

    def get(self, request, *args, **kwargs):
        self.extra_context = dict()
        self.extra_context['comments'] = Comment.objects.filter(published=True,
                                                                news=self.get_queryset()[0])
        self.extra_context['comment_form'] = CommentForm()
        self.extra_context['current_page'] = 'news'
        return super().get(request, *args, **kwargs)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            news = News.objects.get(slug=kwargs['slug'])
            obj.news = news
            obj.author = request.user
            if request.user.is_superuser:
                obj.published = True
            obj.save()
            return redirect(reverse('news:news_detail', args=[obj.news.slug]))
        self.extra_context = dict()
        self.extra_context['comments'] = Comment.objects.filter(published=True,
                                                                news=self.get_queryset()[0])
        self.extra_context['comment_form'] = form
        self.extra_context['current_page'] = 'news'
        return super().get(request, *args, **kwargs)


class NewsCreateView(CreateView):
    form_class = NewsForm
    model = News
    template_name = 'news/news_creation.html'
