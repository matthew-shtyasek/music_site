from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.postgres.search import SearchVector, SearchQuery, TrigramSimilarity, SearchRank
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView

from news.forms import CommentForm, NewsForm
from news.models import News, Comment


class NewsListView(ListView):
    model = News
    context_object_name = 'news_list'
    template_name = 'news/news_list.html'
    ajax_template_name = 'news/news_list_ajax.html'
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

    def get_context_data(self, *, object_list=None, **kwargs):
        if not object_list:
            return super().get_context_data(object_list=object_list, **kwargs)
        context = {self.context_object_name: object_list}
        context.update(self.extra_context)
        return context

    def get(self, request, *args, **kwargs):
        news = self.get_queryset()
        paginator = Paginator(news, 25)
        page = request.GET.get('page')

        try:
            news = paginator.page(page)
        except PageNotAnInteger:
            news = paginator.page(1)

        if request.is_ajax():
            if not news:
                return JsonResponse('')
            return render(request, self.ajax_template_name, self.get_context_data(object_list=news))
        return render(request, self.template_name, self.get_context_data(object_list=news))


class NewsDetailView(DetailView):
    model = News
    template_name = 'news/news_detail.html'

    def get_queryset(self):
        return super().get_queryset().filter(published=True)

    def get(self, request, *args, **kwargs):
        self.extra_context = dict()
        self.extra_context['comments'] = Comment.objects.filter(published=True,
                                                                news=self.get_queryset().get(slug=kwargs['slug']))
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


class NewsCreateView(PermissionRequiredMixin, CreateView):
    form_class = NewsForm
    model = News
    template_name = 'news/news_creation.html'
