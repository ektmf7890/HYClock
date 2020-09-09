from api.weatherAPI import *
from api.noticeAPI import *
from api.slackAPI import slack
from rest_framework.decorators import api_view
from rest_framework.response import Response
import re
import requests
from bs4 import BeautifulSoup
from django.core.cache import cache

@api_view(['GET'])
def return_weather(request):
    context = cache.get("weather_context")
    if context is None:
        current_weather = get_ultra_srt_ncst()
        three_hourly_weather = get_vilage_fcst()

        context = {
            'current_weather': current_weather,
            'three_hourly_weather': three_hourly_weather,
        }
        cache.set("weather_context", context)
    return Response(context)


@api_view(['GET'])
def return_notices(request):
    context = cache.get("notice_context")
    if context is None:
        notices = get_recent_notice()
        notice_list = []
        for item in notices:
            notice = item['notice']
            page_num = item['page_num']
            title = notice.p.a.get_text()
            writer = notice.find('div', {'class': 'notice-writer'}).get_text()
            duration = notice.find('div', {'class': 'notice-date'}).span.get_text()
            href = notice.p.a.get('href')
            notice_number = int(re.search(r'\((.*?)\)', href).group(1))
            base_url = 'https://www.hanyang.ac.kr/web/www/main-notices'
            params = f'p_p_id=mainNotice_WAR_noticeportlet&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&p_p_col_id=column-1&p_p_col_count=1&_mainNotice_WAR_noticeportlet_sCurPage={page_num}&_mainNotice_WAR_noticeportlet_action=view_message'
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
        cache.set("notice_context", context)
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


@api_view(['GET'])
def return_menulist(request):
    print(request.build_absolute_uri())
    context = {
        "data": [
            "짜장면",
            "연어",
            "돈까스",
            "알밥",
            "덮밥",
            "김치찌개",
            "육회",
            "샤브샤브",
            "샌드위치",
            "타코",
            "부리또",
            "돼지국밥",
            "오므라이스",
        ]
    }
    return Response(context)


@api_view(['GET'])
def return_wordlist(request):
    context = {
        "data": [
            "성공하려면 귀는 열고 입은 닫아라. -존 데이비슨 록펠러",
            "때로는 한 순간의 결정이 인생을 바꾼다. -나폴레온 힐",
            "무조건 믿지 마라. 검증하라 -스티븐 D. 레빗",
            "중요한 일을 절대 e메일로 보내지 마라 -엘리어트 스피처(미국 뉴욕주 검찰총장)",
            "타협의 범위를 최대한 넓혀라 -한스-올로브 올슨(볼보 자동차 회장)",
            "누군가를 위해서 일할 때는 진심으로 하라 -지그 지글러",
            "가장 훌륭한 일은 모험과 도전정신으로 이루어진다. -윌리엄 맥나이트(3M 전CEO)",
            "학벌이나 경력이 아닌 태도를 먼저 봐라 -도널드 트럼프",
            "돈의 힘을 제대로 이해하라 -말콤 S. 포브스",
            "회의시간 3분의 2는 듣는 시간 -A.G. 래플리(P&G CEO)",
            "인내는 어떤 실력보다 강하다. -백 호건",
            "당신의 지위가 아니라 누구인지를 기억하라 -브래드 앤더슨",
            "당신은 뭔가 더 대단한 것을 해낼 수 있다. -칼로스 M 구티에레즈(미국 상무장관)",
            "즐기려면 먼저 관심을 가져라 -짐 콜린스",
            "당신의 소신을 믿어라 -폴 프레슬러(갭 CEO)",
            "열심히 일하고 기대는 낮춰라 -비노드 코슬라",
            "큰 야망을 품었을 때 결실을 얻을 수 있다. -힐러리 클린턴",
            "약해지지 마라 -래리 페이지",
            "당신이 리더라고 생각하고 일하라 -조지 샤힌",
            "진정한 혁신이란 문제 해결사가 되는 것이다. -헥터 루이즈",
            "모든 어려움 뒤에는 인간관계에 따른 문제가 있다. -데일 카네기",
            "다른 사람을 이해하라 -스티븐 코비",
            "모든 사람을 존중하라 -리 스콧(월마트 CEO)",
            "남들이 나와 같지 않다는 점을 인정하라 -존 그레이('화성에서 온 남자 금성에서 온 여자'저자)",
            "경쟁자의 성공을 탐내지 말라 -제럴딘 레이본느",
            "정직한 사람은 절대 속일 수 없다. -필 헬무스(포커 월드 챔피언)",
            "다른 사람들을 판단할 때 행운과 능력을 혼동하지 말라 -칼 아이칸",
            "항상 다른 사람들과 나눠라 -스콧 맥닐리",
            "다른 사람의 좋은 아이디어를 칭찬하라 -마이클 아이즈너(전 월트디즈니 CEO)",
            "현명한 사람들을 가까이 둬라 -크리스 올브렉트",
            "돈이 아니라 사람을 위해 일하라 -앨런 더쇼비츠(하버드대 로스쿨 교수)",
            "할 수 있다!고 말하다보면, 결국 실천하게 된다. -사이먼 쿠퍼",
            "편집광만이 살아남는다. -앤디 그로브(인텔 전 CEO)",
            "먼저 행동으로 옮기고 나서 말하라 -스티븐 스필버그",
            "아무리 어려워도 한 번 시작한 일은 까지 마라 -안드레아 정",
            "매일 아침 삶의 목표를 생각하며 일어나라 -아이제이아 토마스(NBA뉴욕닉스 사장)",
            "탁상공론에 머물지 말고 행동하라 -짐 굿나잇",
            "'할 수 없다'고 생각하면 이룰 수 없다. -캐롤 바츠(오토데스크 회장)",
            "사람은 어려움 속에서 성장한다. -제임스 캐시 페니",
            "내일 아침 신문 면에 나올만 한 일에 전념하라.  -워렌 버핏",
            "변화의 첫 걸음은 행동에 옮기는 것이다. -루 거스너(IBM 전 CEO)",
            "성공하려면 이미 했던 일을 제대로 활용하라 -블레이크 로스",
            "실수를 저지른 사람이라도 두 번째 기회를 줘라 -리처드 브랜슨(버진그룹 회장)",
            "배고픔과 함께, 미련함과 함께 -스티브 잡스",
            "실수를 두려워 말고 계속 도전하라 -전 시몬즈",
            "당신의 실수에서 교훈을 얻어라 -크레이그 뉴마크",
            "사람을 먼저 생각하라. 기술은 그 다음이다. -제리 양(야후 창립자)",
            "문제를 명쾌하고 간결하게 만들어야 진짜 프로다. -카를로스 곤(르노, 닛산그룹 회장)",
            "시련을 당하면 가능한 한 웃어 넘겨라 -앤드류 카네기",
            "자신의 것만 챙기는 것을 멈춰라 -러셀 시몬스",
            "위기를 기회로 만들어라 -얀 티머(필립스 전 회장)",
            "거절당할 것을 미리부터 두려워하지 말라 -할런드 샌더스(KFC 창립자)",
            "어떤 사업적 성공도 행복보다 중요하지 않다. -셀리 라자러스",
            "소중한 사람에게는 최고의 서비스를 하라 -마이클 블룸버그",
            "다른 사람들을 잘 모셔라 -데이비드 닐먼",
            "남에게 되돌려주는 법을 배워라 -마이클 그레이브스",
            "사는 데 더 나은 방법을 찾아라 -앨빈 토플러",
            "경쟁력은 제품이나 기술이 아닌 사람이 좌우한다. -스티브 발머(마이크로소프트 CEO)",
            "무엇을 하지 말아야 할지 결정하는 게 더 어렵다. -마이크 델(델 컴퓨터 창립자)",
            "단순한 것이 가장 아름답다. -베라 왕",
            "틀에 박힌 지식들은 언제나 틀렸다. -폴 제이콥스",
            "모든 일에는 타이밍이 중요하다. -레이 커즈웨일",
            "하루에 한 번쯤 머리를 비우는 시간을 가져라 -미레이유 줄리아노",
            "고결함을 잃지 마라 -스탠리 오닐 ",
        ],
    }
    return Response(context)
    
