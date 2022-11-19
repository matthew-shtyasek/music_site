from django.contrib.sitemaps.views import sitemap
from django.urls import path

from news.sitemaps import NewsSitemap
from news.views import NewsListView, NewsDetailView, NewsCreateView

app_name = 'news'

sitemaps = {
    'news': NewsSitemap,
}

urlpatterns = [
    path('sitemap.xml/', sitemap, {'sitemaps': sitemaps}),
    path('create/', NewsCreateView.as_view(), name='news_create'),
    path('<slug:slug>/', NewsDetailView.as_view(), name='news_detail'),
    path('', NewsListView.as_view(), name='news_list'),
]
