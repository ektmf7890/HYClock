from django.shortcuts import render
from api.weatherAPI import *
from api.noticeAPI import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
import re


@api_view(['GET'])
def return_weather(request):
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


@api_view(['GET'])
def return_notices(request):
    notices = get_recent_notice()
    notice_list = []
    for notice in notices:
        title = notice.p.a.get_text()
        writer = notice.find('div', {'class': 'notice-writer'}).get_text()
        date = notice.find('div', {'class': 'notice-date'}).span.get_text()
        href = notice.p.a.get('href')
        notice_number = int(re.search(r'\((.*?)\)', href).group(1))
        base_url = 'https://www.hanyang.ac.kr/web/www/main-notices'
        params = 'p_p_id=mainNotice_WAR_noticeportlet&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&p_p_col_id=column-1&p_p_col_count=1&_mainNotice_WAR_noticeportlet_sCurPage=1&_mainNotice_WAR_noticeportlet_action=view_message'
        href_url = f'{base_url}?{params}&_mainNotice_WAR_noticeportlet_messageId={notice_number}'

        notice_list.append({
            'title': title,
            'writer': writer,
            'date': date,
            'href_url': href_url,
        })

    context = {
        'range': ['서울', '전체'],
        'numberOfNotices': len(notice_list),
        'noticeList': notice_list,
    }
    return Response(context)








