import requests
from bs4 import BeautifulSoup

MAX_PAGES = 10
NUM_OF_ITEMS = 15
BASE_URL = 'https://www.hanyang.ac.kr/web/www/main-notices'


def extract_notices(page_num):
    params = f'?p_p_id=mainNotice_WAR_noticeportlet&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&p_p_col_id=column-1&p_p_col_count=1&_mainNotice_WAR_noticeportlet_sCurPage={page_num}&_mainNotice_WAR_noticeportlet_action=view'
    url = f'{BASE_URL}{params}'
    result = requests.get(url)
    soup = BeautifulSoup(result.text, 'html.parser')

    notices = soup.find_all('div', {'class': 'title-info'})

    seoul_hyu_notices = []
    for notice in notices:
        campus = notice.p.span.get('class')
        if ('label_hyu' in campus) or ('label_seoul' in campus):
            seoul_hyu_notices.append(notice)
    return seoul_hyu_notices


def get_recent_notice():
    total_notices = []
    for page_num in range(MAX_PAGES):
        total_notices += extract_notices(page_num + 1)
        if len(total_notices) >= NUM_OF_ITEMS:
            if len(total_notices) > NUM_OF_ITEMS:
                diff = len(total_notices) - NUM_OF_ITEMS
                total_notices = total_notices[:-diff]
            break
    for i in total_notices:
        print(i)
    print('공지 개수 : ', len(total_notices))
    return total_notices

get_recent_notice()


'''
<div class="title-info">
    <p class="title">
        <span class="label_ERICA">ERICA</span>
        <a href="javascript:_mainNotice_WAR_noticeportlet_view_message(489701);">[ERICA 학부] 2020-2학기 1주차 원격수업 청강 신청 방법 및 개강 후 수강정정 안내</a>
    </p>
    <div class="notice-writer">
        학사팀 / 배원진
    </div>
    <div class="notice-date">
        <span class="date"> 2020.08.25 ~ 2020.09.18 </span>
    </div>
</div>
'''
