from django.shortcuts import render
from weather.weatherAPI import *


def show_weather(request):
    weather_info = get_ultra_srt_ncst()
    weather_info.update(get_vilage_fcst())

    return render(request, 'weather/weather.html', {
        'weather_info': weather_info,
    })



