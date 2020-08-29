from django.shortcuts import render
from api.weatherAPI import *
from api.noticeAPI import *
from api.slackAPI import slack
from rest_framework.decorators import api_view
from rest_framework.response import Response
import re
import requests
from django.utils import timezone
from bs4 import BeautifulSoup


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
        duration = notice.find('div', {'class': 'notice-date'}).span.get_text()
        href = notice.p.a.get('href')
        notice_number = int(re.search(r'\((.*?)\)', href).group(1))
        base_url = 'https://www.hanyang.ac.kr/web/www/main-notices'
        params = 'p_p_id=mainNotice_WAR_noticeportlet&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&p_p_col_id=column-1&p_p_col_count=1&_mainNotice_WAR_noticeportlet_sCurPage=1&_mainNotice_WAR_noticeportlet_action=view_message'
        href_url = f'{base_url}?{params}&_mainNotice_WAR_noticeportlet_messageId={notice_number}'
        result = requests.get(href_url)
        soup = BeautifulSoup(result.text, 'html.parser')
        date = soup.find('span', {'class': 'date'}).get_text()

        notice_list.append({
            'title': title,
            'writer': writer,
            'date': date,
            'duration': duration,
            'href_url': href_url,
        })

    context = {
        'range': ['서울', '전체'],
        'numberOfNotices': len(notice_list),
        'noticeList': notice_list,
    }
    return Response(context)



@api_view(['POST'])
def post_suggestion(request):
    
    context = {
        "result": "success"
    }

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    email = request.data.get("email")
    if email is None:
        context["result"] = "fail"
        context["error"] = "이메일이 입력되지 않았습니다."
        return Response(context)
    
    content = request.data.get("content")
    if content is None:
        context["result"] = "fail"
        context["error"] = "내용이 입력되지 않았습니다."
        return Response(context)

    name = request.data.get("name", "익명")
    student_id = request.data.get("student_id", "None")
    
    title = "{name}({student_id}학번)님에게서 cs 사항이 도착했습니다.".format(
        name=name,
        student_id=student_id,
    )

    res = slack(title, content + '\n' + email + " " + ip)
    return Response(context)







