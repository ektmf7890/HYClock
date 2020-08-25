from django.urls import path
from api import views

urlpatterns = [
    path('weather/', views.show_weather, name='show_weather'),
]