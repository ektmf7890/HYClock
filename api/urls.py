from django.urls import path
from api import views

urlpatterns = [
    path('weather/', views.return_weather, name='return_weather'),
    path('notice/', views.return_notices, name='return_notices'),
    path('suggestion', views.post_suggestion, name='post_suggestion'),
    path('menulist', views.return_menulist, name='menulist'),
    path('wordlist', views.return_wordlist, name='wordlist'),
]