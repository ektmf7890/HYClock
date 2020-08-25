from django.urls import path
from api import views

urlpatterns = [
    path('weather/', views.return_weather, name='return_weather'),
    path('notice/', views.return_notices, name='return_notices'),
]