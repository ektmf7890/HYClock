from django.urls import path
from weather import views

urlpatterns = [
    path('', views.show_weather, name='show_weather'),
]