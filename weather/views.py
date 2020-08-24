from django.shortcuts import render
from weather.weatherAPI import *


def show_weather(request):
    # 초단기 예보
    current_weather_key, hourly_weather = get_ultra_srt_fcst()
    # 초단기 실황 정보로 업데이트
    hourly_weather[current_weather_key].update(get_ultra_srt_ncst())
    #동네 예보 (3시간 단위)
    three_hourly_weather = get_vilage_fcst()

    print(get_ultra_srt_ncst())
    for i in hourly_weather.items():
        print(i)
    for i in three_hourly_weather.items():
        print(i)

    return render(request, 'weather/weather.html', {
        'weather_list': hourly_weather.items(),
        'current_weather': hourly_weather[current_weather_key],
    })




