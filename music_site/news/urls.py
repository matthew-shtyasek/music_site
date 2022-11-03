from django.urls import path

from news.views import NewsListView, NewsDetailView, NewsCreateView

app_name = 'news'

urlpatterns = [
    path('create/', NewsCreateView.as_view(), name='news_create'),
    path('<slug:slug>/', NewsDetailView.as_view(), name='news_detail'),
    path('', NewsListView.as_view(), name='news_list'),
]
