# from datetime import datetime, timedelta
from django.utils import timezone
import requests

category_map = {
    'POP': '강수확률',
    'PTY': '강수형태',
    'R06': '6시간 강수량',
    'REH': '습도',
    'S06': '6시간 신적설',
    'SKY': '하늘상태',
    'T3H': '3시간 기온',
    'TMN': '아침 최저기온',
    'TMX': '낮 최고기온',
    'UUU': '풍속(동서)',
    'VVV': '풍속(남북)',
    'WAV': '파고',
    'VEC': '풍향',
    'WSD': '풍속',
    'T1H': '기온',
    'RN1': '1시간 강수량',
    'LGT': '낙뢰',
}

# 초단기 실황 조회 -> 1시간 단위 기온
def get_ultra_srt_ncst():
    now = timezone.localtime()
    if str(now.hour) == "0" or str(now.hour) == "1":
        now = now - timezone.timedelta(hours=1)
        base_time = now
    else:
        base_time = now - timezone.timedelta(hours=1)
    base_date = now.strftime("%Y%m%d")

    base_url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService/getUltraSrtNcst'
    key = 'X5SR1tXGMMIIhiGfESNHl934eVnCDtQwTN%2B7JYgkGs2vWFkDdter5IhoTH8zNSKPuohVnrycbdhG%2F%2B5tHqQBVw%3D%3D'

    url = f'{base_url}?serviceKey={key}&dataType=JSON&numOfRows=36&base_date={base_date}&base_time={base_time.strftime("%H")}00&nx=61&ny=127'
    result = requests.get(url).json()['response']['body']['items']['item']

    current_weather = {}
    for data in result:
        current_weather[category_map[data['category']]] = data['obsrValue']

    return current_weather


# 초단기 예보 조회
def get_ultra_srt_fcst():
    now = timezone.localtime()
    if str(now.hour) == "0" or str(now.hour) == "1":
        now = now - timezone.timedelta(hours=1)
        base_time = now
    else:
        base_time = (now - timezone.timedelta(hours=1))

    base_date = now.strftime("%Y%m%d")
    print(base_date, base_time)

    base_url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService/getUltraSrtFcst'
    key = 'X5SR1tXGMMIIhiGfESNHl934eVnCDtQwTN%2B7JYgkGs2vWFkDdter5IhoTH8zNSKPuohVnrycbdhG%2F%2B5tHqQBVw%3D%3D'

    url = f'{base_url}?serviceKey={key}&dataType=JSON&numOfRows=60&base_date={base_date}&base_time={base_time.strftime("%H")}30&nx=61&ny=127'
    result = requests.get(url).json()['response']['body']['items']['item']

    hourly_weather = {
        f'{(base_time + timezone.timedelta(hours=1)).strftime("%H")}00': {},
        f'{(base_time + timezone.timedelta(hours=2)).strftime("%H")}00': {},
        f'{(base_time + timezone.timedelta(hours=3)).strftime("%H")}00': {},
        f'{(base_time + timezone.timedelta(hours=4)).strftime("%H")}00': {},
        f'{(base_time + timezone.timedelta(hours=5)).strftime("%H")}00': {},
        f'{(base_time + timezone.timedelta(hours=6)).strftime("%H")}00': {},
    }
    for data in result:
        target = hourly_weather[data['fcstTime']]
        target[category_map[data['category']]] = data['fcstValue']

    CURRENT_WEATHER_KEY = f'{(base_time + timezone.timedelta(hours=1)).strftime("%H")}00'
    return CURRENT_WEATHER_KEY, hourly_weather


# 동네 예보 -> 3시간 단위  정보
# NUM_OF_ITEMS = 4    # 총 15개 가져올 수 있음
# MAX_CATEGORY = 14
# def get_vilage_fcst():
#     now = timezone.localtime()
#     if str(now.hour) == "0" or str(now.hour) == "1":
#         delta = timezone.timedelta(hours=1)
#         now = now - delta
#
#     base_url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService/getVilageFcst'
#     key = 'X5SR1tXGMMIIhiGfESNHl934eVnCDtQwTN%2B7JYgkGs2vWFkDdter5IhoTH8zNSKPuohVnrycbdhG%2F%2B5tHqQBVw%3D%3D'
#     base_date = now.strftime("%Y%m%d")
#     if (now.hour) % 3 == 0:
#         base_time = now - timezone.timedelta(hours=4)
#     elif (now.hour) % 3 == 1:
#         base_time = now - timezone.timedelta(hours=5)
#     else:
#         base_time = now - timezone.timedelta(hours=3)
#     print(base_date, base_time)
#     url = f'{base_url}?serviceKey={key}&dataType=JSON&numOfRows={NUM_OF_ITEMS*MAX_CATEGORY}&base_date={base_date}&base_time={base_time.strftime("%H")}00&nx=61&ny=127'
#     result = requests.get(url).json()['response']['body']['items']['item']
#
#     three_hourly_weather = {
#         f'{(base_time + timezone.timedelta(hours=4)).strftime("%H")}00': {},
#         f'{(base_time + timezone.timedelta(hours=7)).strftime("%H")}00': {},
#         f'{(base_time + timezone.timedelta(hours=1)).strftime("%H")}00': {},
#         f'{(base_time + timezone.timedelta(hours=1)).strftime("%H")}00': {},
#     }
#     for data in result:
#         target = three_hourly_weather.get(data['fcstTime'])
#         if target == None:
#             break
#         target[category_map[data['category']]] = data['fcstValue']
#
#     return three_hourly_weather

