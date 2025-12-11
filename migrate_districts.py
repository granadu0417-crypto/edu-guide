#!/usr/bin/env python3
"""
서울시 구별 URL 마이그레이션 스크립트
강남구 완료 후 나머지 24개 구 생성
"""

import os
import subprocess
from datetime import datetime

# 구별 정보 (영문, 한글, 주요 학교)
DISTRICTS = {
    'seocho': {
        'korean': '서초구',
        'schools_middle': ['반포중', '서초중', '원촌중', '언남중', '서래중'],
        'schools_high': ['서초고', '반포고', '세화고', '세화여고', '상문고'],
        'dongs': []  # 아래에서 채움
    },
    'songpa': {
        'korean': '송파구',
        'schools_middle': ['잠실중', '잠일중', '방이중', '오금중', '문정중'],
        'schools_high': ['잠실고', '잠일고', '방산고', '잠신고', '보성고'],
        'dongs': []
    },
    'gangdong': {
        'korean': '강동구',
        'schools_middle': ['천호중', '둔촌중', '강동중', '배명중', '한산중'],
        'schools_high': ['배재고', '광문고', '한영고', '명일여고', '동북고'],
        'dongs': []
    },
    'gangbuk': {
        'korean': '강북구',
        'schools_middle': ['삼각산중', '수유중', '송천중', '영훈국제중'],
        'schools_high': ['창문여고', '성신여고', '수유고', '미양고'],
        'dongs': []
    },
    'gangseo': {
        'korean': '강서구',
        'schools_middle': ['등촌중', '가양중', '화곡중', '명덕중', '공항중'],
        'schools_high': ['명덕외고', '경인고', '진명여고', '신목고', '마포고'],
        'dongs': []
    },
    'gwanak': {
        'korean': '관악구',
        'schools_middle': ['서울관악중', '신림중', '봉천중', '인헌중', '난곡중'],
        'schools_high': ['서울대부고', '신림고', '관악고', '인헌고', '영등포고'],
        'dongs': []
    },
    'gwangjin': {
        'korean': '광진구',
        'schools_middle': ['광진중', '자양중', '군자중', '건대부중', '성수중'],
        'schools_high': ['대원고', '대원외고', '건대부고', '광남고', '성수고'],
        'dongs': []
    },
    'guro': {
        'korean': '구로구',
        'schools_middle': ['구로중', '고척중', '개봉중', '오류중', '신도림중'],
        'schools_high': ['구로고', '고척고', '세곡고', '신도림고', '항동고'],
        'dongs': []
    },
    'geumcheon': {
        'korean': '금천구',
        'schools_middle': ['독산중', '시흥중', '가산중', '문성중'],
        'schools_high': ['독산고', '시흥고', '금천고', '문영여고'],
        'dongs': []
    },
    'nowon': {
        'korean': '노원구',
        'schools_middle': ['상계중', '중계중', '공릉중', '월계중', '하계중'],
        'schools_high': ['대진고', '재현고', '청원고', '서라벌고', '노원고'],
        'dongs': []
    },
    'dobong': {
        'korean': '도봉구',
        'schools_middle': ['창동중', '도봉중', '방학중', '쌍문중', '신창중'],
        'schools_high': ['창동고', '도봉고', '선덕고', '덕성여고', '대진여고'],
        'dongs': []
    },
    'dongdaemun': {
        'korean': '동대문구',
        'schools_middle': ['장안중', '전농중', '휘경중', '답십리중', '청량리중'],
        'schools_high': ['경희고', '휘경여고', '장안고', '청량고', '해성여고'],
        'dongs': []
    },
    'dongjak': {
        'korean': '동작구',
        'schools_middle': ['흑석중', '노량진중', '사당중', '상도중', '대방중'],
        'schools_high': ['숭실고', '동작고', '중앙대부고', '노량진고', '대방고'],
        'dongs': []
    },
    'mapo': {
        'korean': '마포구',
        'schools_middle': ['서강중', '마포중', '홍대부중', '신수중', '상암중'],
        'schools_high': ['홍대부고', '서강고', '마포고', '성산고', '상암고'],
        'dongs': []
    },
    'seodaemun': {
        'korean': '서대문구',
        'schools_middle': ['연희중', '홍은중', '대신중', '금화중', '북가좌중'],
        'schools_high': ['이화여고', '대신고', '명지고', '서대문고', '숭문고'],
        'dongs': []
    },
    'seongdong': {
        'korean': '성동구',
        'schools_middle': ['성수중', '옥수중', '금호중', '무학중', '행당중'],
        'schools_high': ['성동고', '한양대부고', '금옥여고', '무학고', '행당고'],
        'dongs': []
    },
    'seongbuk': {
        'korean': '성북구',
        'schools_middle': ['동덕여중', '고려대부중', '길음중', '돈암중', '정덕중'],
        'schools_high': ['고려대부고', '경동고', '성신여고', '정덕고', '돈암고'],
        'dongs': []
    },
    'yangcheon': {
        'korean': '양천구',
        'schools_middle': ['목운중', '신목중', '신서중', '월촌중', '영도중'],
        'schools_high': ['목동고', '신목고', '진명여고', '영도고', '월촌고'],
        'dongs': []
    },
    'yeongdeungpo': {
        'korean': '영등포구',
        'schools_middle': ['영등포중', '대림중', '당산중', '신길중', '여의도중'],
        'schools_high': ['영등포고', '여의도고', '당산고', '대림고', '선유고'],
        'dongs': []
    },
    'yongsan': {
        'korean': '용산구',
        'schools_middle': ['용산중', '이촌중', '한강중', '보광중', '원효중'],
        'schools_high': ['용산고', '선린인고', '중경고', '배문고', '한강고'],
        'dongs': []
    },
    'eunpyeong': {
        'korean': '은평구',
        'schools_middle': ['은평중', '불광중', '진관중', '녹번중', '신사중'],
        'schools_high': ['은평고', '대성고', '불광고', '진관고', '신도고'],
        'dongs': []
    },
    'jongno': {
        'korean': '종로구',
        'schools_middle': ['종로중', '창덕여중', '혜화중', '교남중', '숭인중'],
        'schools_high': ['경복고', '동성고', '중앙고', '창덕여고', '정화여고'],
        'dongs': []
    },
    'jung': {
        'korean': '중구',
        'schools_middle': ['장충중', '무학중', '광희중', '동국대부중', '황학중'],
        'schools_high': ['장충고', '동국대부고', '중앙여고', '동대부고', '환일고'],
        'dongs': []
    },
    'jungnang': {
        'korean': '중랑구',
        'schools_middle': ['면목중', '묵현중', '상봉중', '신내중', '중화중'],
        'schools_high': ['면목고', '서울사대부고', '광운대부고', '신현고', '태릉고'],
        'dongs': []
    }
}

# 동 목록 (위에서 추출한 데이터 기반)
DONG_DATA = """
seocho-bangbae2dong
seocho-bangbae3dong
seocho-bangbae4dong
seocho-bangbaebondong
seocho-banpo2dong
seocho-banpo3dong
seocho-banpo4dong
seocho-banpobondong
seocho-jamwondong
seocho-naegokdong
seocho-seochodong
seocho-yangjae1dong
seocho-yangjae2dong
songpa-bangi-1
songpa-bangi-2
songpa-garak-1
songpa-garak-2
songpa-garakbon
songpa-geoyeo-1
songpa-geoyeo-2
songpa-jamsil-2
songpa-jamsil-3
songpa-jamsil-4
songpa-jamsil-6
songpa-jamsil-7
songpa-jamsilbon
songpa-jangji
songpa-macheon-1
songpa-macheon-2
songpa-munjeong-1
songpa-munjeong-2
songpa-ogeum
songpa-oryun
songpa-pungnapdong-1
songpa-pungnapdong-2
songpa-samjeon
songpa-seokchon
songpa-songpa1
songpa-songpa2
songpa-wirye
gangdong-amsa1
gangdong-amsa2
gangdong-amsa3
gangdong-cheonho1
gangdong-cheonho2
gangdong-cheonho3
gangdong-dunchon1
gangdong-dunchon2
gangdong-gangil
gangdong-gildong
gangdong-godeok1
gangdong-godeok2
gangdong-myeongil1
gangdong-myeongil2
gangdong-sangil1
gangdong-sangil2
gangdong-seongnae1
gangdong-seongnae2
gangdong-seongnae3
gangbuk-beon1
gangbuk-beon2
gangbuk-beon3
gangbuk-insu
gangbuk-mia
gangbuk-samgaksan
gangbuk-samyang
gangbuk-songcheon
gangbuk-songjung
gangbuk-suyu1
gangbuk-suyu2
gangbuk-suyu3
gangbuk-ui
gangseo-balsan1
gangseo-banghwa1
gangseo-banghwa2
gangseo-banghwa3
gangseo-deungchon1
gangseo-deungchon2
gangseo-deungchon3
gangseo-gayang1
gangseo-gayang2
gangseo-gayang3
gangseo-gonghang
gangseo-hwagok1
gangseo-hwagok2
gangseo-hwagok3
gangseo-hwagok4
gangseo-hwagok5
gangseo-hwagok6
gangseo-hwagok7
gangseo-hwagok8
gangseo-hwagokbon
gangseo-magok
gangseo-ujangsan
gangseo-yeomchang
gwanak-boramae
gwanak-cheongnyong
gwanak-daehak
gwanak-euncheon
gwanak-haengun
gwanak-inheon
gwanak-jowon
gwanak-jungang
gwanak-miseong
gwanak-nakseongdae
gwanak-namhyeon
gwanak-nangok
gwanak-nanhyang
gwanak-samseong
gwanak-seonghyeon
gwanak-seorim
gwanak-seowon
gwanak-sillim
gwanak-sinsa
gwanak-sinwon
gwangjin-gunja
gwangjin-guui1
gwangjin-guui2
gwangjin-guui3
gwangjin-gwangjang
gwangjin-hwayang
gwangjin-jayang1
gwangjin-jayang2
gwangjin-jayang3
gwangjin-jayang4
gwangjin-junggok1
gwangjin-junggok2
gwangjin-junggok3
gwangjin-junggok4
gwangjin-neungdong
guro-gaebong1
guro-gaebong2
guro-gaebong3
guro-garibong
guro-gocheok1
guro-gocheok2
guro-guro1
guro-guro2
guro-guro3
guro-guro4
guro-guro5
guro-hangdong
guro-oryu1
guro-oryu2
guro-sindorim
guro-sugung
geumcheon-doksan1
geumcheon-doksan2
geumcheon-doksan3
geumcheon-doksan4
geumcheon-gasan
geumcheon-siheung1
geumcheon-siheung2
geumcheon-siheung3
geumcheon-siheung4
geumcheon-siheung5
nowon-gongneung1
nowon-gongneung2
nowon-hagye1
nowon-hagye2
nowon-junggye1
nowon-junggye23
nowon-junggye4
nowon-junggyebon
nowon-sanggye1
nowon-sanggye10
nowon-sanggye2
nowon-sanggye34
nowon-sanggye5
nowon-sanggye67
nowon-sanggye8
nowon-sanggye9
nowon-wolgye1
nowon-wolgye2
nowon-wolgye3
dobong-banghak1
dobong-banghak2
dobong-banghak3
dobong-chang1
dobong-chang2
dobong-chang3
dobong-chang4
dobong-chang5
dobong-dobong1
dobong-dobong2
dobong-ssangmun1
dobong-ssangmun2
dobong-ssangmun3
dobong-ssangmun4
dongdaemun-cheongnyangni
dongdaemun-dapsimni1
dongdaemun-dapsimni2
dongdaemun-hoegi
dongdaemun-hwigyeong1
dongdaemun-hwigyeong2
dongdaemun-imun1
dongdaemun-imun2
dongdaemun-jangan1
dongdaemun-jangan2
dongdaemun-jegi
dongdaemun-jeonnong1
dongdaemun-jeonnong2
dongdaemun-yongsin
dongjak-daebang
dongjak-heukseok
dongjak-noryangjin1
dongjak-noryangjin2
dongjak-sadang1
dongjak-sadang2
dongjak-sadang3
dongjak-sadang4
dongjak-sadang5
dongjak-sangdo1
dongjak-sangdo2
dongjak-sangdo3
dongjak-sangdo4
dongjak-sindaebang1
dongjak-sindaebang2
mapo-ahyeon
mapo-daeheung
mapo-dohwa
mapo-gongdeok
mapo-hapjeong
mapo-mangwon1
mapo-mangwon2
mapo-sangam
mapo-seogang
mapo-seogyo
mapo-seongsan1
mapo-seongsan2
mapo-sinsu
mapo-yeomni
mapo-yeonnam
mapo-yonggang
seodaemun-bukahyeon
seodaemun-bukgajwa1
seodaemun-bukgajwa2
seodaemun-cheongyeon
seodaemun-chunghyeon
seodaemun-hongeun1
seodaemun-hongeun2
seodaemun-hongje1
seodaemun-hongje2
seodaemun-hongje3
seodaemun-namgajwa1
seodaemun-namgajwa2
seodaemun-sinchon
seodaemun-yeonhui
seongdong-eungbong
seongdong-geumho1ga
seongdong-geumho2-3ga
seongdong-geumho4ga
seongdong-haengdang1
seongdong-haengdang2
seongdong-majang
seongdong-oksu
seongdong-sageun
seongdong-seongsu1ga1
seongdong-seongsu1ga2
seongdong-seongsu2ga1
seongdong-seongsu2ga3
seongdong-songjeong
seongdong-wangsimni-doseondong
seongdong-wangsimni2
seongdong-yongdap
seongbuk-anam
seongbuk-bomun
seongbuk-donam1
seongbuk-donam2
seongbuk-dongseon
seongbuk-gileum1
seongbuk-gileum2
seongbuk-hawolgok
seongbuk-jangwi1
seongbuk-jangwi2
seongbuk-jangwi3
seongbuk-jeongneung1
seongbuk-jeongneung2
seongbuk-jeongneung3
seongbuk-jeongneung4
seongbuk-jongam
seongbuk-samseong
seongbuk-sangwolgok
seongbuk-seokgwan
seongbuk-seongbuk
seongbuk-wolgok1
seongbuk-wolgok2
yangcheon-mok1
yangcheon-mok2
yangcheon-mok3
yangcheon-mok4
yangcheon-mok5
yangcheon-sinjeong1
yangcheon-sinjeong2
yangcheon-sinjeong3
yangcheon-sinjeong4
yangcheon-sinjeong6
yangcheon-sinjeong7
yangcheon-sinwol1
yangcheon-sinwol2
yangcheon-sinwol3
yangcheon-sinwol4
yangcheon-sinwol5
yangcheon-sinwol6
yangcheon-sinwol7
yeongdeungpo-daerim1
yeongdeungpo-daerim2
yeongdeungpo-daerim3
yeongdeungpo-dangsan1
yeongdeungpo-dangsan2
yeongdeungpo-dorim
yeongdeungpo-mullae
yeongdeungpo-singil1
yeongdeungpo-singil3
yeongdeungpo-singil4
yeongdeungpo-singil5
yeongdeungpo-singil6
yeongdeungpo-singil7
yeongdeungpo-yangpyeong1
yeongdeungpo-yangpyeong2
yeongdeungpo-yeongdeungpo
yeongdeungpo-yeongdeungpo-bon
yeongdeungpo-yeui
yongsan-bogwang
yongsan-cheongpa
yongsan-hangang-ro
yongsan-hannam
yongsan-huam
yongsan-hyochang
yongsan-ichon1
yongsan-ichon2
yongsan-itaewon1
yongsan-itaewon2
yongsan-namyeong
yongsan-seobinggo
yongsan-wonhyoro1
yongsan-wonhyoro2
yongsan-yongmun
yongsan-yongsan2ga
eunpyeong-bulgwang1
eunpyeong-bulgwang2
eunpyeong-daejo
eunpyeong-eungam1
eunpyeong-eungam2
eunpyeong-eungam3
eunpyeong-galhyeon1
eunpyeong-galhyeon2
eunpyeong-gusan
eunpyeong-jeungsan
eunpyeong-jingwan
eunpyeong-nokbeon
eunpyeong-sinsa1
eunpyeong-sinsa2
eunpyeong-susaek
eunpyeong-yeokchon
jongno-buam
jongno-changsin1
jongno-changsin2
jongno-changsin3
jongno-cheongunhyoja
jongno-gahoe
jongno-gyonam
jongno-hyehwa
jongno-ihwa
jongno-jongno1234
jongno-jongno56
jongno-muak
jongno-pyeongchang
jongno-sajik
jongno-samcheong
jongno-sungin1
jongno-sungin2
junggu-cheonggu
junggu-dasan
junggu-donghwa
junggu-euljiro
junggu-gwanghui
junggu-hoehyeon
junggu-hwanghak
junggu-jangchung
junggu-junglim
junggu-myeongdong
junggu-pildong
junggu-sindang
junggu-sindang5
junggu-sogong
junggu-yaksu
jungnang-junghwa1
jungnang-junghwa2
jungnang-mangwu3
jungnang-mangwubon
jungnang-muk1
jungnang-muk2
jungnang-myeonmok2
jungnang-myeonmok38
jungnang-myeonmok4
jungnang-myeonmok5
jungnang-myeonmok7
jungnang-myeonmokbon
jungnang-sangbong1
jungnang-sangbong2
jungnang-sinnae1
jungnang-sinnae2
"""

# 동 데이터 파싱
for line in DONG_DATA.strip().split('\n'):
    if not line.strip():
        continue
    parts = line.split('-', 1)
    if len(parts) == 2:
        district = parts[0]
        dong = parts[1]
        # junggu 특별 처리
        if district == 'junggu':
            district = 'jung'
        if district in DISTRICTS:
            DISTRICTS[district]['dongs'].append(dong)

# 이미지 매핑 (구별로 다른 이미지 사용)
IMAGE_MAP = {
    'seocho': '/images/edu_0021_1KNAPQ9Oq6k.jpg',
    'songpa': '/images/edu_0022_0nyR0Aw5fCA.jpg',
    'gangdong': '/images/edu_0023_I_LxDFIIRIA.jpg',
    'gangbuk': '/images/edu_0024_zgq9OXecyqI.jpg',
    'gangseo': '/images/edu_0025_ADcGTvU-lF0.jpg',
    'gwanak': '/images/edu_0026_4syO0fP1Bf0.jpg',
    'gwangjin': '/images/edu_0027_oCWYjKfWQP8.jpg',
    'guro': '/images/edu_0028_ec3SJoypVKM.jpg',
    'geumcheon': '/images/edu_0029_DRZB3gjiHeY.jpg',
    'nowon': '/images/edu_0030_4r5Hogjbgkw.jpg',
    'dobong': '/images/edu_0031_XFajQ988KNI.jpg',
    'dongdaemun': '/images/edu_0032_GGlz-QSvL38.jpg',
    'dongjak': '/images/edu_0033_AiCJW1QhLB0.jpg',
    'mapo': '/images/edu_0034_K1P_W3JbCpI.jpg',
    'seodaemun': '/images/edu_0035_iaJ6xi44LTU.jpg',
    'seongdong': '/images/edu_0036_svnLIZ6jgCQ.jpg',
    'seongbuk': '/images/edu_0037_GYzbHU7dr3E.jpg',
    'yangcheon': '/images/edu_0038_wGzmUZMW2rE.jpg',
    'yeongdeungpo': '/images/edu_0039_90ctJcyrRLs.jpg',
    'yongsan': '/images/edu_0040_EYkx28n9Gi0.jpg',
    'eunpyeong': '/images/edu_0041_9-PE3C5p7NE.jpg',
    'jongno': '/images/edu_0042_PLeMfbzWA90.jpg',
    'jung': '/images/edu_0043_8VRKYQ_pVwo.jpg',
    'jungnang': '/images/edu_0044_FoB-ImUjLqE.jpg',
}


def generate_hub_page(district_eng, district_kor, dongs, schools_middle, schools_high, image):
    """구 허브 페이지 생성"""
    schools_str = ', '.join(schools_high[:4])

    return f"""---
title: "{district_kor} 과외 | 중등·고등 맞춤 과외"
date: 2025-12-10
description: "{district_kor} 중등·고등 수학·영어 과외. {schools_str} 등 {district_kor} 학교 내신 완벽 대비."
featured_image: "{image}"
regions:
  - 서울
cities:
  - {district_kor}
tags:
  - {district_kor}과외
  - {district_kor}수학과외
  - {district_kor}영어과외
---

## {district_kor} 과외 안내

{district_kor} 지역 학생들을 위한 맞춤형 1:1 과외를 제공합니다. 학교별 내신 특성에 맞춘 체계적인 수업으로 성적 향상을 도와드립니다.

### {district_kor} 주요 학교

**중학교**: {', '.join(schools_middle)}

**고등학교**: {', '.join(schools_high)}

### 과외 과목

아래에서 과목별, 학년별 과외 정보를 확인하세요.
"""


def generate_content_page(district_eng, district_kor, level, subject, dongs, schools, image):
    """콘텐츠 페이지 생성"""
    level_kor = '중등' if level == 'middle' else '고등'
    subject_kor = '수학' if subject == 'math' else '영어'
    schools_str = '·'.join(schools[:4])

    # 별칭 생성
    aliases = []
    for dong in dongs:
        aliases.append(f"  - /{level}/{district_eng}-{dong}-{level}-{subject}/")
    aliases_str = '\n'.join(aliases)

    # 학년별 비용 정보
    if level == 'middle':
        price_section = """## 수업료 안내

{district_kor} {level_kor} {subject_kor}과외 수업료는 다음과 같습니다.

**중학생**은 주1회 22만원 - 32만원, 주2회 29만원 - 47만원 선입니다.

정확한 금액은 상담을 통해 안내드립니다.""".format(
            district_kor=district_kor, level_kor=level_kor, subject_kor=subject_kor
        )
    else:
        price_section = """## 수업료 안내

{district_kor} {level_kor} {subject_kor}과외 수업료는 다음과 같습니다.

**고1-2**는 주1회 25만원 - 36만원, 주2회 33만원 - 53만원 선입니다.

**고3**은 주1회 28만원 - 40만원, 주2회 37만원 - 59만원이 일반적입니다.

정확한 금액은 상담을 통해 안내드립니다.""".format(
            district_kor=district_kor, level_kor=level_kor, subject_kor=subject_kor
        )

    # 과목별 콘텐츠
    if subject == 'math':
        content = generate_math_content(district_kor, level_kor, schools)
    else:
        content = generate_english_content(district_kor, level_kor, schools)

    return f"""---
title: "{district_kor} {level_kor} {subject_kor}과외 | {schools_str} 내신·수능 대비"
date: 2025-12-10
description: "{district_kor} {level_kor}학생 {subject_kor}과외 전문. {schools_str} 등 {district_kor} 학교 내신 맞춤 관리."
featured_image: "{image}"
categories:
  - {level_kor}교육
  - {subject_kor}과외
regions:
  - 서울
cities:
  - {district_kor}
tags:
  - {district_kor}{subject_kor}과외
  - {district_kor}{level_kor}{subject_kor}
aliases:
{aliases_str}
---

{content}

{price_section}

{{{{< cta-dual type="final" >}}}}

## 자주 묻는 질문

**Q. 기초가 부족해도 수업 가능한가요?**

가능합니다. 학생의 현재 수준에서 시작합니다. 기초부터 차근차근 쌓아가면 충분히 성적을 올릴 수 있습니다.

**Q. 내신 시험 전에 집중 수업이 가능한가요?**

가능합니다. 시험 기간에는 수업 횟수를 늘리거나 특별 대비 수업을 진행할 수 있습니다.

**Q. 학원과 병행해도 되나요?**

가능합니다. 학원에서 기본기를 다지고, 과외에서 약점 보완과 심화 학습을 병행하는 학생이 많습니다.

## 마무리

{district_kor} {level_kor}학생 여러분, {subject_kor} 성적 향상이 필요하시다면 지금 시작하세요.

체계적인 1:1 수업으로 학교 내신 완벽 대비하고, 실력을 한 단계 높여보세요.
"""


def generate_math_content(district_kor, level_kor, schools):
    """수학 과목 콘텐츠"""
    if level_kor == '중등':
        return f"""{district_kor} 중학교 수학, 기초부터 탄탄히 잡아야 고등학교에서 흔들리지 않습니다. 개념 이해와 문제 풀이력을 균형 있게 키워드립니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
첫 수업에서 학생의 수학 실력을 종합 진단합니다. 개념 이해도, 계산 정확도, 문제 해결력을 파악하고 약점부터 집중 보완합니다.
</div>

## {district_kor} 중학교 수학이 중요한 이유

중학교 수학은 고등학교 수학의 기초입니다. 일차방정식, 함수, 도형 등 핵심 개념이 제대로 잡히지 않으면 고등학교에서 어려움을 겪습니다.

{district_kor} 학교들은 내신 시험에서 응용 문제 비중이 높습니다. 단순 계산보다 개념 응용 능력을 평가합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
개념을 완벽히 이해한 후 다양한 유형의 문제를 풀어봅니다. 단순 암기가 아닌 원리 이해에 집중합니다.
</div>

## {district_kor} 주요 중학교 특징

### {schools[0]}

{schools[0]}은 내신 시험 난이도가 높습니다. 서술형 문제 비중이 높고 풀이 과정 채점이 엄격합니다. 꼼꼼한 풀이 연습이 필요합니다.

### {schools[1] if len(schools) > 1 else schools[0]}

심화 문제 출제 비중이 높습니다. 기본 개념을 응용한 고난도 문제가 출제됩니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
학생이 다니는 학교의 기출문제를 분석합니다. 출제 경향과 자주 나오는 유형을 파악하여 맞춤 대비합니다.
</div>

## 학년별 학습 전략

### 중학교 1학년

중1은 수학 학습 습관을 잡는 시기입니다. 정수, 유리수, 방정식 등 기초 개념을 탄탄히 다집니다.

### 중학교 2학년

중2는 함수와 도형이 본격적으로 등장합니다. 일차함수, 삼각형, 사각형 등 고등학교 수학의 기반이 되는 단원입니다.

### 중학교 3학년

중3은 고등학교 수학 선행과 내신 관리를 병행합니다. 이차방정식, 이차함수, 피타고라스 정리 등을 완벽히 익힙니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
학년별 맞춤 커리큘럼으로 진행합니다. 학기 중에는 내신 대비, 방학에는 선행 학습을 병행합니다.
</div>

## 1:1 과외가 필요한 이유

수학은 개인별 약점이 다릅니다. 계산이 느린 학생, 응용이 약한 학생, 서술형이 어려운 학생 각각 다른 접근이 필요합니다.

학원은 정해진 커리큘럼으로 진행됩니다. 1:1 과외는 학생의 약점에 맞춤 집중하여 효율적으로 실력을 올립니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
매 수업 오답 노트를 정리합니다. 틀린 문제를 분석하고 같은 실수를 반복하지 않도록 훈련합니다.
</div>
"""
    else:  # 고등
        return f"""{district_kor} 고등학교 수학, 중학교와 차원이 다릅니다. 내신과 수능을 동시에 준비해야 하며, 체계적인 학습 전략이 필수입니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
첫 수업에서 학생의 수학 실력을 정밀 진단합니다. 개념 이해도, 문제 해결력, 수능형 사고력까지 파악하고 맞춤 전략을 수립합니다.
</div>

## {district_kor} 고등학교 수학이 어려운 이유

고등학교 수학은 추상적 개념이 많습니다. 집합, 명제, 함수의 극한 등 눈에 보이지 않는 개념을 다룹니다.

{district_kor} 고등학교들은 내신 난이도가 높습니다. 교과서 수준을 넘어선 심화 문제가 출제됩니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
개념을 완벽히 이해한 후, 다양한 유형의 고난도 문제를 훈련합니다. 수능형 사고력을 기르는 데 집중합니다.
</div>

## {district_kor} 주요 고등학교별 특징

### {schools[0]}

{schools[0]}은 내신 시험 난이도가 높습니다. 심화 문제 비중이 높고 서술형 채점이 엄격합니다.

### {schools[1] if len(schools) > 1 else schools[0]}

{schools[1] if len(schools) > 1 else schools[0]}은 수능형 문제 출제 비중이 높습니다. 수능 대비와 내신 대비를 병행해야 합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
학생이 다니는 학교의 기출문제를 철저히 분석합니다. 출제 선생님 스타일, 자주 나오는 유형을 파악하여 맞춤 대비합니다.
</div>

## 내신과 수능 병행 전략

### 고1-2: 내신 중심

고1, 고2는 내신을 우선합니다. 학생부 종합전형을 고려하면 내신 등급이 중요합니다. 동시에 수능 기초 개념을 다져둡니다.

### 고3: 내신과 수능 병행

고3은 내신과 수능을 동시에 준비합니다. 9월까지는 병행하고, 이후에는 수능에 집중합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
학생의 입시 목표에 맞춰 내신과 수능 비중을 조절합니다. 수시 vs 정시, 목표 대학에 따라 전략을 달리합니다.
</div>

## 수능 수학 대비

### 킬러 문항 대비

21번, 29번, 30번은 1등급을 가르는 문제입니다. 기본 개념의 깊은 이해와 여러 개념을 연결하는 능력이 필요합니다.

### 4점 문제 완벽 방어

4점 문제에서 실수를 줄이는 것이 고득점의 핵심입니다. 자주 틀리는 유형을 분석하고 반복 훈련합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
수능 기출문제와 EBS 연계 교재를 활용합니다. 킬러 문항 접근법을 단계별로 훈련하고, 오답 원인을 철저히 분석합니다.
</div>

## 1:1 과외가 필요한 이유

고등학교 수학은 개인별 약점이 다양합니다. 1:1 과외는 학생의 약점을 정확히 파악하고 맞춤 훈련을 제공합니다.

특히 킬러 문항 대비는 개별 지도가 효과적입니다. 학생의 사고 과정을 점검하고 오류를 교정하는 데 1:1이 유리합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
매 수업 오답을 철저히 분석합니다. 왜 틀렸는지, 어떻게 접근해야 하는지 학생이 스스로 깨달을 때까지 지도합니다.
</div>
"""


def generate_english_content(district_kor, level_kor, schools):
    """영어 과목 콘텐츠"""
    if level_kor == '중등':
        return f"""{district_kor} 중학교 영어, 문법과 독해 실력을 균형 있게 키워야 합니다. 고등학교 영어의 기초를 탄탄히 다져드립니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
첫 수업에서 학생의 영어 실력을 종합 진단합니다. 문법, 어휘, 독해, 듣기 각 영역의 수준을 파악하고 약점부터 집중 보완합니다.
</div>

## {district_kor} 중학교 영어가 중요한 이유

중학교 영어는 고등학교 수능 영어의 기초입니다. 핵심 문법, 기본 어휘, 독해 능력이 제대로 잡히지 않으면 고등학교에서 어려움을 겪습니다.

{district_kor} 학교들은 영어 내신 변별력을 높이기 위해 까다로운 문제를 출제합니다. 교과서 본문 외 지문이 등장하고, 문법 응용 문제가 출제됩니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
교과서 본문을 완벽히 이해한 후, 변형 문제에 대응하는 연습을 합니다. 빈칸, 어순, 영작 등 다양한 유형을 훈련합니다.
</div>

## {district_kor} 주요 중학교 특징

### {schools[0]}

{schools[0]}은 서술형 비중이 높습니다. 영작 문제가 어렵고 채점이 엄격합니다. 정확한 문법 사용과 표현력이 중요합니다.

### {schools[1] if len(schools) > 1 else schools[0]}

독해 지문 난이도가 높습니다. 긴 지문을 빠르게 이해하는 능력이 필요합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
학생이 다니는 학교의 영어 기출문제를 수집하여 출제 패턴을 분석합니다. 학교별 맞춤 대비 전략을 세웁니다.
</div>

## 영역별 학습 전략

### 문법 학습

문법은 영어의 기초입니다. 시제, 조동사, 부정사, 동명사, 분사, 관계사 등 핵심 문법을 체계적으로 정리합니다.

### 독해 학습

독해력은 꾸준한 훈련이 필요합니다. 끊어 읽기, 구문 분석, 문맥 파악 순서로 단계별 훈련합니다.

### 어휘 학습

어휘력은 모든 영역의 기본입니다. 중학교 필수 어휘를 체계적으로 암기합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
문법, 독해, 어휘를 균형있게 학습합니다. 학생의 약한 영역에 더 많은 시간을 배분하여 효율적으로 실력을 올립니다.
</div>

## 학년별 학습 전략

### 중학교 1학년

중1은 영어 학습 습관을 잡는 시기입니다. 매일 영어를 접하는 습관, 단어 암기 습관을 형성합니다.

### 중학교 2학년

중2는 문법이 본격적으로 어려워지는 시기입니다. 관계대명사, 분사, 가정법 등 고등학교 영어의 핵심 문법이 등장합니다.

### 중학교 3학년

중3은 중학교 영어를 총정리하고 고등학교에 대비하는 시기입니다. 수능 영어의 기초가 되는 구문 독해 연습을 시작합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
학년별 맞춤 커리큘럼으로 진행합니다. 학기 중에는 내신 대비, 방학에는 영역별 심화 학습을 병행합니다.
</div>

## 1:1 과외가 필요한 이유

영어는 개인별 약점이 다릅니다. 문법이 약한 학생, 독해가 느린 학생, 어휘력이 부족한 학생 각각 다른 접근이 필요합니다.

학원은 정해진 커리큘럼으로 진행됩니다. 1:1 과외는 학생의 약점에 집중하여 효율적으로 보완합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
매 수업 단어 테스트를 진행합니다. 문법은 개념 설명 후 다양한 문제로 적용 연습을 합니다. 독해는 끊어 읽기부터 훈련합니다.
</div>
"""
    else:  # 고등
        return f"""{district_kor} 고등학교 영어, 내신과 수능 모두 만만치 않습니다. 체계적인 준비로 영어 실력을 한 단계 높여드립니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
첫 수업에서 학생의 영어 실력을 종합 진단합니다. 문법, 독해, 어휘, 듣기 각 영역을 점검하고 약점부터 집중 보완합니다.
</div>

## {district_kor} 고등학교 영어가 어려운 이유

고등학교 영어 내신은 변별력을 위해 높은 난이도로 출제됩니다. 교과서 외 지문이 등장하고, 심화 문법 문제가 까다롭습니다.

수능 영어도 절대평가이지만 1등급은 쉽지 않습니다. 빈칸 추론, 순서 배열, 문장 삽입 등 고난도 유형에서 실수 없이 맞춰야 합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
내신과 수능을 균형있게 대비합니다. 학기 중에는 내신 집중, 방학에는 수능 유형 훈련을 병행합니다.
</div>

## {district_kor} 주요 고등학교별 영어 특징

### {schools[0]}

{schools[0]} 영어 내신은 독해 지문 난이도가 높습니다. 긴 지문을 빠르게 파악하는 능력이 필요합니다.

### {schools[1] if len(schools) > 1 else schools[0]}

{schools[1] if len(schools) > 1 else schools[0]}은 문법 심화 문제가 많습니다. 구문 분석 능력이 필수입니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
학생이 다니는 학교의 영어 기출문제를 분석합니다. 출제 경향과 자주 나오는 유형을 파악하여 맞춤 대비합니다.
</div>

## 내신과 수능 병행 전략

### 고1-2: 내신 중심

고1, 고2는 내신을 우선합니다. 학생부 관리가 중요하기 때문입니다. 동시에 수능 영어 기초인 구문 독해력을 키워둡니다.

### 고3: 내신과 수능 병행

고3은 상반기에 내신과 수능을 병행합니다. 9월 이후에는 수능에 집중합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
학생의 입시 목표에 맞춰 내신과 수능 비중을 조절합니다. 수시 vs 정시, 목표 대학에 따라 전략을 달리합니다.
</div>

## 수능 영어 대비 전략

### 고난도 유형 공략

빈칸 추론, 순서 배열, 문장 삽입은 수능 영어의 핵심입니다. 글의 논리적 흐름을 파악하는 연습이 필요합니다.

### 듣기 완벽 대비

듣기는 17문항으로 비중이 큽니다. 꾸준한 훈련으로 만점을 목표로 합니다.

### 어휘와 구문

수능 영어의 기본은 어휘와 구문입니다. 수능 필수 어휘를 암기하고, 복잡한 구문을 정확히 해석하는 능력을 키웁니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
수능 기출문제와 EBS 교재를 활용합니다. 고난도 유형의 접근법을 단계별로 훈련하고, 오답 원인을 분석합니다.
</div>

## 1:1 과외가 필요한 이유

영어는 개인별 약점이 다릅니다. 독해가 느린 학생, 문법이 약한 학생, 듣기에서 실수하는 학생 각각 다른 접근이 필요합니다.

학원은 정해진 커리큘럼으로 진행됩니다. 1:1 과외는 학생의 약점에 맞춤 집중하여 효율적으로 실력을 올립니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
매 수업 단어 테스트와 독해 훈련을 진행합니다. 학생이 어디서 막히는지 정확히 파악하고 맞춤 지도합니다.
</div>
"""


def create_district(district_eng):
    """한 개 구 생성"""
    if district_eng not in DISTRICTS:
        print(f"Unknown district: {district_eng}")
        return

    info = DISTRICTS[district_eng]
    district_kor = info['korean']
    dongs = info['dongs']
    schools_middle = info['schools_middle']
    schools_high = info['schools_high']
    image = IMAGE_MAP.get(district_eng, '/images/edu_0001_stwfGwdy67g.jpg')

    # 폴더 생성
    folder_path = f"content/seoul/{district_eng}"
    os.makedirs(folder_path, exist_ok=True)

    # 1. 허브 페이지 생성
    hub_content = generate_hub_page(district_eng, district_kor, dongs, schools_middle, schools_high, image)
    with open(f"{folder_path}/_index.md", 'w', encoding='utf-8') as f:
        f.write(hub_content)
    print(f"Created: {folder_path}/_index.md")

    # 2. 콘텐츠 페이지 생성
    for level in ['middle', 'high']:
        schools = schools_middle if level == 'middle' else schools_high
        for subject in ['math', 'english']:
            content = generate_content_page(
                district_eng, district_kor, level, subject,
                dongs, schools, image
            )
            filename = f"{folder_path}/{level}-{subject}.md"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Created: {filename} ({len(dongs)} aliases)")


def main():
    """메인 실행"""
    print("=== 서울시 구별 URL 마이그레이션 ===\n")

    # 강남구 제외하고 나머지 구 생성
    for district in DISTRICTS.keys():
        if district != 'gangnam':  # 강남구는 이미 완료
            print(f"\n--- {DISTRICTS[district]['korean']} ({district}) ---")
            create_district(district)

    print("\n=== 마이그레이션 완료 ===")
    print(f"총 {len(DISTRICTS) - 1}개 구 생성됨")


if __name__ == "__main__":
    main()
