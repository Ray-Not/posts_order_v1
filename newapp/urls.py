from django.urls import path
from .views import home_view, news_detail, news_list

namespace = 'newapp'

urlpatterns = [
    path('', home_view, name='home'),
    path('news/', news_list, name='news_list'),
    path('news/<int:id>/', news_detail, name='news_detail'),
]
