from datetime import datetime, timedelta
import requests

fcst_time_map = {
    '0': '20',
    '1': '20',
    '2': '23',
    '3': '23',
    '4': '23',
    '5': '02',
    '6': '02',
    '7': '02',
    '8': '05',
    '9': '05',
    '10': '05',
    '11': '08',
    '12': '08',
    '13': '08',
    '14': '11',
    '15': '11',
    '16': '11',
    '17': '14',
    '18': '14',
    '19': '14',
    '20': '17',
    '21': '17',
    '22': '17',
    '23': '20',
}

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
    'RN1': '1시간 강수량'
}


# 초단기 실황 조회 -> 1시간 단위 기온
def get_ultra_srt_ncst():
    now = datetime.now()
    base_url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService/getUltraSrtNcst'
    key = 'X5SR1tXGMMIIhiGfESNHl934eVnCDtQwTN%2B7JYgkGs2vWFkDdter5IhoTH8zNSKPuohVnrycbdhG%2F%2B5tHqQBVw%3D%3D'
    base_date = now.strftime('%Y%m%d')
    if now.hour == 0:
        base_time = str(23)
    else:
        now = now - timedelta(hours=1)
        base_time = now.strftime("%H")

    url = f'{base_url}?serviceKey={key}&dataType=JSON&numOfRows=36&base_date={base_date}&base_time={base_time}00&nx=61&ny=127'
    weather_list = requests.get(url).json()['response']['body']['items']['item']

    for weather in weather_list:
        print(weather)


# 동네 예보 -> 3시간 단위 기온 4개 & 가장 가까운 시간 기준 하늘상태/강수확률/강수형태
def get_vilage_fcst():
    now = datetime.now()
    base_url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService/getVilageFcst'
    key = 'X5SR1tXGMMIIhiGfESNHl934eVnCDtQwTN%2B7JYgkGs2vWFkDdter5IhoTH8zNSKPuohVnrycbdhG%2F%2B5tHqQBVw%3D%3D'
    base_date = now.strftime('%Y%m%d')
    base_time = fcst_time_map[str(now.hour)]
    url = f'{base_url}?serviceKey={key}&dataType=JSON&numOfRows=36&base_date={base_date}&base_time={base_time}00&nx=61&ny=127'
    weather_list = requests.get(url).json()['response']['body']['items']['item']

    for weather in weather_list:
        print(weather)

get_vilage_fcst()