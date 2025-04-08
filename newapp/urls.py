# from django.contrib.auth import views as auth_views
from django.urls import path, include

from .views import (PostCreateView, PostDeleteView, PostUpdateView, home_view,
                    news_detail, news_list, news_search, become_author)

namespace = 'newapp'

urlpatterns = [
    path('', home_view, name='home'),
    path('news/', news_list, name='post_list'),
    path('news/<int:id>/', news_detail, name='post_detail'),
    path('news/add/', PostCreateView.as_view(), name='post_create'),
    path('news/<int:pk>/edit/', PostUpdateView.as_view(), name='post_edit'),
    path(
        'news/<int:pk>/delete/',
        PostDeleteView.as_view(),
        name='post_delete'
    ),
    path('search/', news_search, name='post_search'),
    path('accounts/', include('allauth.urls')),
    path('become-author/', become_author, name='become_author'),
]
