from django.shortcuts import render
from api.weatherAPI import *
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def show_weather(request):
    current_weather_key, hourly_weather = get_ultra_srt_fcst()
    current_weather = get_ultra_srt_ncst()
    hourly_weather[current_weather_key].update(current_weather)
    three_hourly_weather = get_vilage_fcst()

    context = {
        'ultra_srt_fcst': hourly_weather,
        'ultra_srt_ncst': current_weather,
        'vilage_fcst': three_hourly_weather,
    }
    return Response(context)







