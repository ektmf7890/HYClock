from django.utils import timezone
from datetime import timedelta
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
    if now.hour == 0 or now.hour == 1:
        base_date = (now - timedelta(days=1)).strftime("%Y%m%d")
    else:
        base_date = now.strftime("%Y%m%d")
    base_time = (now - timezone.timedelta(hours=1)).strftime("%H")

    base_url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService/getUltraSrtNcst'
    key = 'X5SR1tXGMMIIhiGfESNHl934eVnCDtQwTN%2B7JYgkGs2vWFkDdter5IhoTH8zNSKPuohVnrycbdhG%2F%2B5tHqQBVw%3D%3D'
    url = f'{base_url}?serviceKey={key}&dataType=JSON&numOfRows=36&base_date={base_date}&base_time={base_time}00&nx=61&ny=127'

    response = requests.get(url)
    # 응답코드 != "00" -> 에러
    if response.json()['response']['header']['resultCode'] == '00':
        result = response.json()['response']['body']['items']['item']
    else:
        return 'API_ERROR'

    current_weather = {
        'time': f'{now.strftime("%H")}시',
        'content': {},
    }
    for data in result:
        content = current_weather['content']
        content[category_map[data['category']]] = data['obsrValue']

    return current_weather


# 동네 예보 -> 3시간 단위  정보
NUM_OF_ITEMS = 5    # 총 15개 가져올 수 있음
MAX_CATEGORY = 14
def get_vilage_fcst():
    now = timezone.localtime()
    if now.hour == 0 or now.hour == 1 or now.hour == 2 or now.hour == 3 or now.hour == 4:
        base_date = (now - timedelta(days=1)).strftime("%Y%m%d")
    else:
        base_date = now.strftime("%Y%m%d")

    if (now.hour) % 3 == 0:
        base_time = now - timezone.timedelta(hours=4)
    elif (now.hour) % 3 == 1:
        base_time = now - timezone.timedelta(hours=5)
    else:
        base_time = now - timezone.timedelta(hours=3)

    base_url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService/getVilageFcst'
    key = 'X5SR1tXGMMIIhiGfESNHl934eVnCDtQwTN%2B7JYgkGs2vWFkDdter5IhoTH8zNSKPuohVnrycbdhG%2F%2B5tHqQBVw%3D%3D'
    url = f'{base_url}?serviceKey={key}&dataType=JSON&numOfRows={NUM_OF_ITEMS*MAX_CATEGORY}&base_date={base_date}&base_time={base_time.strftime("%H")}00&nx=61&ny=127'

    response = requests.get(url)
    # 응답코드 != "00" -> 에러
    if response.json()['response']['header']['resultCode'] == '00':
        result = response.json()['response']['body']['items']['item']
    else:
        return 'API_ERROR'

    three_hourly_weather = {
        f'{(base_time + timezone.timedelta(hours=4)).strftime("%H")}00': {
            'time': f'{(base_time + timezone.timedelta(hours=4)).strftime("%H")}시',
            'content': {},
            'weather_emoji': '',
        },
        f'{(base_time + timezone.timedelta(hours=7)).strftime("%H")}00': {
            'time': f'{(base_time + timezone.timedelta(hours=7)).strftime("%H")}시',
            'content': {},
            'weather_emoji': '',
        },
        f'{(base_time + timezone.timedelta(hours=10)).strftime("%H")}00': {
            'time': f'{(base_time + timezone.timedelta(hours=10)).strftime("%H")}시',
            'content': {},
            'weather_emoji': '',
        },
        f'{(base_time + timezone.timedelta(hours=13)).strftime("%H")}00': {
            'time': f'{(base_time + timezone.timedelta(hours=13)).strftime("%H")}시',
            'content': {},
            'weather_emoji': '',
        },
        f'{(base_time + timezone.timedelta(hours=16)).strftime("%H")}00': {
            'time': f'{(base_time + timezone.timedelta(hours=16)).strftime("%H")}시',
            'content': {},
            'weather_emoji': '',
        },
    }

    for data in result:
        target = three_hourly_weather.get(data['fcstTime'])
        if target is None:
            break
        else:
            target_content = target['content']
        target_content[category_map[data['category']]] = data['fcstValue']

    for value in three_hourly_weather.values():
        content = value['content']
        if content.get('강수형태') and content.get('하늘상태'):
            emoji = get_weather_emoji(precipitation=content['강수형태'], sky=content['하늘상태'])
            value['weather_emoji'] = emoji

    return three_hourly_weather


# 초단기 예보 조회
def get_ultra_srt_fcst():
    now = timezone.localtime()
    if now.hour == 0 or now.hour == 1:
        base_date = (now - timedelta(days=1)).strftime("%Y%m%d")
    else:
        base_date = now.strftime("%Y%m%d")
    base_time = now - timezone.timedelta(hours=1)

    base_url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService/getUltraSrtFcst'
    key = 'X5SR1tXGMMIIhiGfESNHl934eVnCDtQwTN%2B7JYgkGs2vWFkDdter5IhoTH8zNSKPuohVnrycbdhG%2F%2B5tHqQBVw%3D%3D'
    url = f'{base_url}?serviceKey={key}&dataType=JSON&numOfRows=60&base_date={base_date}&base_time={base_time.strftime("%H")}30&nx=61&ny=127'

    response = requests.get(url)
    # 응답코드 != "00" -> 에러
    if response.json()['response']['header']['resultCode'] == '00':
        result = response.json()['response']['body']['items']['item']
    else:
        return 'API_ERROR'

    hourly_weather = {
        f'{(base_time + timedelta(hours=1)).strftime("%H")}00': {
            'time': f'{(base_time + timedelta(hours=1)).strftime("%H")}시',
            'content': {},
        },
        f'{(base_time + timedelta(hours=2)).strftime("%H")}00': {
            'time': f'{(base_time + timedelta(hours=2)).strftime("%H")}시',
            'content': {},
        },
        f'{(base_time + timedelta(hours=3)).strftime("%H")}00': {
            'time': f'{(base_time + timedelta(hours=3)).strftime("%H")}시',
            'content': {},
        },
        f'{(base_time + timedelta(hours=4)).strftime("%H")}00': {
            'time': f'{(base_time + timedelta(hours=4)).strftime("%H")}시',
            'content': {},
        },
        f'{(base_time + timedelta(hours=5)).strftime("%H")}00': {
            'time': f'{(base_time + timedelta(hours=5)).strftime("%H")}시',
            'content': {},
        },
        f'{(base_time + timedelta(hours=6)).strftime("%H")}00': {
            'time': f'{(base_time + timedelta(hours=6)).strftime("%H")}시',
            'content': {},
        },
    }

    for data in result:
        target = hourly_weather[data['fcstTime']]
        target_content = target['content']
        target_content[category_map[data['category']]] = data['fcstValue']

    return hourly_weather


# 강수형태와 하늘상태를 고려하여 날씨 이모티콘 전송
def get_weather_emoji(precipitation, sky):
    if precipitation == "0":
        # 맑음
        if sky == "1":
            return '☀️'
        # 구름 많음
        elif sky == "3":
            return '☁️'
        # 흐림
        elif sky == "4":
            return '🌥️'
        else:
            return ''
    # 비
    elif precipitation == "1" or precipitation == "4" or precipitation == "5":
        return '🌧️'
    #눈
    else:
        return '🌨️'


