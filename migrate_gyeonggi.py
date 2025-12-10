#!/usr/bin/env python3
"""
경기도 시별 URL 마이그레이션 스크립트
/local/gyeonggi/ → /gyeonggi/{시}/
"""

import os

# 경기도 시/군 정보
CITIES = {
    # 주요 15개 시 (인구 30만 이상)
    'suwon': {
        'korean': '수원시',
        'schools_middle': ['수원중', '영통중', '매탄중', '권선중', '장안중'],
        'schools_high': ['수원고', '영통고', '매탄고', '권선고', '장안고'],
        'aliases': ['suwon-education-guide', 'suwon-math-tutoring', 'suwon-english-tutoring', 'suwon-science-tutoring']
    },
    'yongin': {
        'korean': '용인시',
        'schools_middle': ['수지중', '기흥중', '처인중', '죽전중', '신갈중'],
        'schools_high': ['용인고', '수지고', '기흥고', '죽전고', '용인외대부고'],
        'aliases': ['yongin-education-guide', 'yongin-math-tutoring', 'yongin-english-tutoring', 'yongin-science-tutoring']
    },
    'goyang': {
        'korean': '고양시',
        'schools_middle': ['일산중', '백석중', '저동중', '화정중', '행신중'],
        'schools_high': ['일산고', '백석고', '저동고', '화정고', '행신고'],
        'aliases': ['goyang-math-tutoring', 'goyang-english-tutoring', 'goyang-science-tutoring']
    },
    'seongnam': {
        'korean': '성남시',
        'schools_middle': ['성남중', '분당중', '수내중', '야탑중', '태원중'],
        'schools_high': ['성남고', '분당고', '수내고', '야탑고', '태원고'],
        'aliases': ['seongnam-math-tutoring', 'seongnam-english-tutoring', 'seongnam-science-tutoring']
    },
    'bucheon': {
        'korean': '부천시',
        'schools_middle': ['중원중', '부천중', '소사중', '원미중', '상동중'],
        'schools_high': ['부천고', '중원고', '소사고', '원미고', '상동고'],
        'aliases': ['bucheon-education-guide', 'bucheon-math-tutoring', 'bucheon-english-tutoring', 'bucheon-science-tutoring']
    },
    'hwaseong': {
        'korean': '화성시',
        'schools_middle': ['동탄중', '반송중', '화성중', '봉담중', '병점중'],
        'schools_high': ['동탄고', '반송고', '화성고', '봉담고', '병점고'],
        'aliases': ['hwaseong-education-guide', 'hwaseong-math-tutoring', 'hwaseong-english-tutoring', 'hwaseong-science-tutoring']
    },
    'namyangju': {
        'korean': '남양주시',
        'schools_middle': ['다산중', '별내중', '진접중', '호평중', '화도중'],
        'schools_high': ['다산고', '별내고', '진접고', '호평고', '화도고'],
        'aliases': ['namyangju-education-guide', 'namyangju-math-tutoring', 'namyangju-english-tutoring']
    },
    'ansan': {
        'korean': '안산시',
        'schools_middle': ['안산중', '상록중', '단원중', '원곡중', '선부중'],
        'schools_high': ['안산고', '상록고', '단원고', '원곡고', '선부고'],
        'aliases': ['ansan-education-guide', 'ansan-math-tutoring', 'ansan-english-tutoring']
    },
    'anyang': {
        'korean': '안양시',
        'schools_middle': ['안양중', '평촌중', '범계중', '귀인중', '부흥중'],
        'schools_high': ['안양고', '평촌고', '범계고', '귀인고', '부흥고'],
        'aliases': ['anyang-math-tutoring', 'anyang-english-tutoring', 'anyang-science-tutoring']
    },
    'pyeongtaek': {
        'korean': '평택시',
        'schools_middle': ['평택중', '비전중', '세교중', '고덕중', '안중중'],
        'schools_high': ['평택고', '비전고', '세교고', '고덕고', '안중고'],
        'aliases': ['pyeongtaek-education-guide', 'pyeongtaek-math-tutoring', 'pyeongtaek-english-tutoring', 'pyeongtaek-science-tutoring']
    },
    'uijeongbu': {
        'korean': '의정부시',
        'schools_middle': ['의정부중', '호원중', '민락중', '녹양중', '발곡중'],
        'schools_high': ['의정부고', '호원고', '민락고', '녹양고', '발곡고'],
        'aliases': ['uijeongbu-education-guide', 'uijeongbu-math-tutoring', 'uijeongbu-english-tutoring', 'uijeongbu-science-tutoring']
    },
    'siheung': {
        'korean': '시흥시',
        'schools_middle': ['시흥중', '정왕중', '배곧중', '월곶중', '은행중'],
        'schools_high': ['시흥고', '정왕고', '배곧고', '월곶고', '은행고'],
        'aliases': ['siheung-education-guide', 'siheung-math-tutoring', 'siheung-english-tutoring']
    },
    'paju': {
        'korean': '파주시',
        'schools_middle': ['파주중', '운정중', '교하중', '금촌중', '문산중'],
        'schools_high': ['파주고', '운정고', '교하고', '금촌고', '문산고'],
        'aliases': ['paju-education-guide', 'paju-math-tutoring', 'paju-english-tutoring', 'paju-science-tutoring']
    },
    'gimpo': {
        'korean': '김포시',
        'schools_middle': ['김포중', '장기중', '운양중', '풍무중', '고촌중'],
        'schools_high': ['김포고', '장기고', '운양고', '풍무고', '고촌고'],
        'aliases': ['gimpo-education-guide', 'gimpo-math-tutoring', 'gimpo-english-tutoring']
    },
    'gwangmyeong': {
        'korean': '광명시',
        'schools_middle': ['광명중', '철산중', '하안중', '소하중', '충현중'],
        'schools_high': ['광명고', '광명북고', '진성고', '명문고', '충현고'],
        'aliases': ['gwangmyeong-education-guide', 'gwangmyeong-math-tutoring', 'gwangmyeong-english-tutoring']
    },
    # 특수 교육지역 (별도 URL)
    'bundang': {
        'korean': '분당',
        'schools_middle': ['분당중', '수내중', '서현중', '이매중', '정자중'],
        'schools_high': ['분당고', '수내고', '서현고', '이매고', '낙생고'],
        'aliases': ['bundang-english-tutoring'],
        'is_special': True
    },
    'ilsan': {
        'korean': '일산',
        'schools_middle': ['일산중', '백석중', '저동중', '주엽중', '대화중'],
        'schools_high': ['일산고', '백석고', '저동고', '주엽고', '대화고'],
        'aliases': ['ilsan-math-tutoring'],
        'is_special': True
    },
    'pyeongchon': {
        'korean': '평촌',
        'schools_middle': ['평촌중', '범계중', '귀인중', '부흥중', '인덕원중'],
        'schools_high': ['평촌고', '범계고', '귀인고', '부흥고', '인덕원고'],
        'aliases': ['pyeongchon-english-tutoring'],
        'is_special': True
    },
    # 기타 시/군 (인구 30만 미만)
    'hanam': {
        'korean': '하남시',
        'schools_middle': ['하남중', '미사중', '풍산중', '덕풍중', '위례중'],
        'schools_high': ['하남고', '미사고', '풍산고', '덕풍고', '위례고'],
        'aliases': ['hanam-education-guide']
    },
    'guri': {
        'korean': '구리시',
        'schools_middle': ['구리중', '인창중', '동구중', '수택중', '갈매중'],
        'schools_high': ['구리고', '인창고', '동구고', '수택고', '갈매고'],
        'aliases': ['guri-education-guide']
    },
    'gunpo': {
        'korean': '군포시',
        'schools_middle': ['군포중', '산본중', '금정중', '당정중', '광정중'],
        'schools_high': ['군포고', '산본고', '금정고', '당정고', '광정고'],
        'aliases': ['gunpo-education-guide']
    },
    'osan': {
        'korean': '오산시',
        'schools_middle': ['오산중', '세마중', '운암중', '매홀중', '성호중'],
        'schools_high': ['오산고', '세마고', '운암고', '매홀고', '성호고'],
        'aliases': ['osan-education-guide']
    },
    'icheon': {
        'korean': '이천시',
        'schools_middle': ['이천중', '부발중', '창전중', '증포중', '설봉중'],
        'schools_high': ['이천고', '부발고', '창전고', '증포고', '설봉고'],
        'aliases': ['icheon-education-guide']
    },
    'yangju': {
        'korean': '양주시',
        'schools_middle': ['양주중', '덕정중', '회천중', '옥정중', '고읍중'],
        'schools_high': ['양주고', '덕정고', '회천고', '옥정고', '고읍고'],
        'aliases': ['yangju-education-guide']
    },
    'anseong': {
        'korean': '안성시',
        'schools_middle': ['안성중', '공도중', '죽산중', '미양중', '서운중'],
        'schools_high': ['안성고', '공도고', '죽산고', '미양고', '서운고'],
        'aliases': ['anseong-education-guide']
    },
    'gwangju_gg': {
        'korean': '광주시',  # 경기도 광주
        'schools_middle': ['광주중', '경안중', '태전중', '오포중', '초월중'],
        'schools_high': ['광주고', '경안고', '태전고', '오포고', '초월고'],
        'aliases': ['gwangju-education-guide']
    },
}

# 이미지 매핑
IMAGE_MAP = {
    'suwon': '/images/edu_0050_VOUicg8Ejus.jpg',
    'yongin': '/images/edu_0051_6Bae9-46yeU.jpg',
    'goyang': '/images/edu_0052_hlfh_7qQQYs.jpg',
    'seongnam': '/images/edu_0053_9A9ayYqsI5M.jpg',
    'bucheon': '/images/edu_0054_syyjbNKTzjs.jpg',
    'hwaseong': '/images/edu_0055_DknG_UtWXyA.jpg',
    'namyangju': '/images/edu_0056_FMk_-rH3zjg.jpg',
    'ansan': '/images/edu_0057_T5r6OUgw5tw.jpg',
    'anyang': '/images/edu_0058_zn9QqA-JTmY.jpg',
    'pyeongtaek': '/images/edu_0059_0sljWIZH4IQ.jpg',
    'uijeongbu': '/images/edu_0060_7ebCN7FwH3g.jpg',
    'siheung': '/images/edu_0061_GMvn7T0Ha8M.jpg',
    'paju': '/images/edu_0062_iQPr1XkF5F0.jpg',
    'gimpo': '/images/edu_0063_v7FT5ngIEfA.jpg',
    'gwangmyeong': '/images/edu_0064_xKJUnFwfz3s.jpg',
    'bundang': '/images/edu_0065_awnu4mkV0nw.jpg',
    'ilsan': '/images/edu_0066_s9CC2SKySJM.jpg',
    'pyeongchon': '/images/edu_0067_4-EeTnaC1S4.jpg',
    'hanam': '/images/edu_0068_4-4WPFLVhAY.jpg',
    'guri': '/images/edu_0069_wWgfpLY7Ims.jpg',
    'gunpo': '/images/edu_0070_zFSo6bnZJTw.jpg',
    'osan': '/images/edu_0071_FcLyt7lW5wg.jpg',
    'icheon': '/images/edu_0072_oikrPWDdbF4.jpg',
    'yangju': '/images/edu_0073_kcT-7cirBEw.jpg',
    'anseong': '/images/edu_0074_OyCl7Y4y0Bk.jpg',
    'gwangju_gg': '/images/edu_0075_SDK5pLlxF4M.jpg',
}


def generate_gyeonggi_hub():
    """경기도 메인 허브 페이지 생성"""
    return """---
title: "경기도 과외 | 31개 시군 맞춤 과외 정보"
date: 2025-12-10
description: "경기도 31개 시군별 중등·고등 수학·영어 과외. 분당, 일산, 평촌 등 교육특구 맞춤 과외 정보."
featured_image: "/images/edu_0050_VOUicg8Ejus.jpg"
regions:
  - 경기도
tags:
  - 경기도과외
  - 경기도수학과외
  - 경기도영어과외
  - 분당과외
  - 일산과외
aliases:
  - /local/gyeonggi/
  - /local/gyeonggi/gyeonggi-education-guide/
---

## 경기도 과외 안내

경기도는 대한민국 최대 규모의 교육 인프라를 보유한 지역입니다. 31개 시군마다 독특한 교육 환경을 가지고 있으며, 분당, 일산, 평촌, 수지 등 교육특구가 밀집해 있습니다.

### 경기도 교육특구

**분당**: 성남시 분당구, 수도권 대표 교육특구
**일산**: 고양시 일산동구/서구, 서북부 최대 교육지역
**평촌**: 안양시 동안구, 학원가 밀집 지역
**수지**: 용인시 수지구, 신흥 교육도시

### 경기도 주요 시

아래에서 지역을 선택하여 상세 과외 정보를 확인하세요.

<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(120px, 1fr)); gap: 10px; margin: 20px 0;">
<a href="/gyeonggi/suwon/" style="padding: 12px; background: #10b981; color: white; text-decoration: none; border-radius: 8px; text-align: center; font-weight: 600;">수원시</a>
<a href="/gyeonggi/yongin/" style="padding: 12px; background: #10b981; color: white; text-decoration: none; border-radius: 8px; text-align: center; font-weight: 600;">용인시</a>
<a href="/gyeonggi/goyang/" style="padding: 12px; background: #10b981; color: white; text-decoration: none; border-radius: 8px; text-align: center; font-weight: 600;">고양시</a>
<a href="/gyeonggi/seongnam/" style="padding: 12px; background: #10b981; color: white; text-decoration: none; border-radius: 8px; text-align: center; font-weight: 600;">성남시</a>
<a href="/gyeonggi/bundang/" style="padding: 12px; background: #059669; color: white; text-decoration: none; border-radius: 8px; text-align: center; font-weight: 600;">분당</a>
<a href="/gyeonggi/ilsan/" style="padding: 12px; background: #059669; color: white; text-decoration: none; border-radius: 8px; text-align: center; font-weight: 600;">일산</a>
<a href="/gyeonggi/bucheon/" style="padding: 12px; background: #10b981; color: white; text-decoration: none; border-radius: 8px; text-align: center; font-weight: 600;">부천시</a>
<a href="/gyeonggi/hwaseong/" style="padding: 12px; background: #10b981; color: white; text-decoration: none; border-radius: 8px; text-align: center; font-weight: 600;">화성시</a>
<a href="/gyeonggi/anyang/" style="padding: 12px; background: #10b981; color: white; text-decoration: none; border-radius: 8px; text-align: center; font-weight: 600;">안양시</a>
<a href="/gyeonggi/pyeongchon/" style="padding: 12px; background: #059669; color: white; text-decoration: none; border-radius: 8px; text-align: center; font-weight: 600;">평촌</a>
<a href="/gyeonggi/ansan/" style="padding: 12px; background: #10b981; color: white; text-decoration: none; border-radius: 8px; text-align: center; font-weight: 600;">안산시</a>
<a href="/gyeonggi/namyangju/" style="padding: 12px; background: #10b981; color: white; text-decoration: none; border-radius: 8px; text-align: center; font-weight: 600;">남양주시</a>
<a href="/gyeonggi/paju/" style="padding: 12px; background: #10b981; color: white; text-decoration: none; border-radius: 8px; text-align: center; font-weight: 600;">파주시</a>
<a href="/gyeonggi/gimpo/" style="padding: 12px; background: #10b981; color: white; text-decoration: none; border-radius: 8px; text-align: center; font-weight: 600;">김포시</a>
<a href="/gyeonggi/uijeongbu/" style="padding: 12px; background: #10b981; color: white; text-decoration: none; border-radius: 8px; text-align: center; font-weight: 600;">의정부시</a>
<a href="/gyeonggi/siheung/" style="padding: 12px; background: #10b981; color: white; text-decoration: none; border-radius: 8px; text-align: center; font-weight: 600;">시흥시</a>
<a href="/gyeonggi/pyeongtaek/" style="padding: 12px; background: #10b981; color: white; text-decoration: none; border-radius: 8px; text-align: center; font-weight: 600;">평택시</a>
<a href="/gyeonggi/gwangmyeong/" style="padding: 12px; background: #10b981; color: white; text-decoration: none; border-radius: 8px; text-align: center; font-weight: 600;">광명시</a>
<a href="/gyeonggi/hanam/" style="padding: 12px; background: #10b981; color: white; text-decoration: none; border-radius: 8px; text-align: center; font-weight: 600;">하남시</a>
<a href="/gyeonggi/guri/" style="padding: 12px; background: #10b981; color: white; text-decoration: none; border-radius: 8px; text-align: center; font-weight: 600;">구리시</a>
</div>

{{< cta-dual type="final" >}}
"""


def generate_city_hub(city_eng, city_kor, schools_middle, schools_high, image, aliases):
    """시 허브 페이지 생성"""
    schools_str = ', '.join(schools_high[:4])

    # 별칭 생성
    alias_lines = []
    for alias in aliases:
        alias_lines.append(f"  - /local/gyeonggi/{alias}/")
    aliases_str = '\n'.join(alias_lines)

    return f"""---
title: "{city_kor} 과외 | 중등·고등 맞춤 과외"
date: 2025-12-10
description: "{city_kor} 중등·고등 수학·영어 과외. {schools_str} 등 {city_kor} 학교 내신 완벽 대비."
featured_image: "{image}"
regions:
  - 경기도
cities:
  - {city_kor}
tags:
  - {city_kor}과외
  - {city_kor}수학과외
  - {city_kor}영어과외
aliases:
{aliases_str}
---

## {city_kor} 과외 안내

{city_kor} 지역 학생들을 위한 맞춤형 1:1 과외를 제공합니다. 학교별 내신 특성에 맞춘 체계적인 수업으로 성적 향상을 도와드립니다.

### {city_kor} 주요 학교

**중학교**: {', '.join(schools_middle)}

**고등학교**: {', '.join(schools_high)}

### 과외 과목

아래에서 과목별, 학년별 과외 정보를 확인하세요.
"""


def generate_content_page(city_eng, city_kor, level, subject, schools, image, aliases):
    """콘텐츠 페이지 생성"""
    level_kor = '중등' if level == 'middle' else '고등'
    subject_kor = '수학' if subject == 'math' else '영어'
    schools_str = '·'.join(schools[:4])

    # 해당 과목 별칭만 필터링
    filtered_aliases = []
    for alias in aliases:
        if subject in alias or 'education-guide' in alias:
            filtered_aliases.append(f"  - /local/gyeonggi/{alias}/")
    aliases_str = '\n'.join(filtered_aliases) if filtered_aliases else "  - /local/gyeonggi/"

    # 학년별 비용
    if level == 'middle':
        price_section = f"""## 수업료 안내

{city_kor} {level_kor} {subject_kor}과외 수업료는 다음과 같습니다.

**중학생**은 주1회 22만원 - 32만원, 주2회 29만원 - 47만원 선입니다.

정확한 금액은 상담을 통해 안내드립니다."""
    else:
        price_section = f"""## 수업료 안내

{city_kor} {level_kor} {subject_kor}과외 수업료는 다음과 같습니다.

**고1-2**는 주1회 25만원 - 36만원, 주2회 33만원 - 53만원 선입니다.

**고3**은 주1회 28만원 - 40만원, 주2회 37만원 - 59만원이 일반적입니다.

정확한 금액은 상담을 통해 안내드립니다."""

    if subject == 'math':
        content = generate_math_content(city_kor, level_kor, schools)
    else:
        content = generate_english_content(city_kor, level_kor, schools)

    return f"""---
title: "{city_kor} {level_kor} {subject_kor}과외 | {schools_str} 내신·수능 대비"
date: 2025-12-10
description: "{city_kor} {level_kor}학생 {subject_kor}과외 전문. {schools_str} 등 {city_kor} 학교 내신 맞춤 관리."
featured_image: "{image}"
categories:
  - {level_kor}교육
  - {subject_kor}과외
regions:
  - 경기도
cities:
  - {city_kor}
tags:
  - {city_kor}{subject_kor}과외
  - {city_kor}{level_kor}{subject_kor}
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

{city_kor} {level_kor}학생 여러분, {subject_kor} 성적 향상이 필요하시다면 지금 시작하세요.

체계적인 1:1 수업으로 학교 내신 완벽 대비하고, 실력을 한 단계 높여보세요.
"""


def generate_math_content(city_kor, level_kor, schools):
    """수학 콘텐츠 생성"""
    if level_kor == '중등':
        return f"""{city_kor} 중학교 수학, 기초부터 탄탄히 잡아야 고등학교에서 흔들리지 않습니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
첫 수업에서 학생의 수학 실력을 종합 진단합니다. 개념 이해도, 계산 정확도, 문제 해결력을 파악하고 약점부터 집중 보완합니다.
</div>

## {city_kor} 중학교 수학이 중요한 이유

중학교 수학은 고등학교 수학의 기초입니다. 일차방정식, 함수, 도형 등 핵심 개념이 탄탄해야 고등학교에서 무너지지 않습니다.

{city_kor} 학교들은 내신 시험에서 응용 문제 비중이 높습니다. 단순 계산보다 개념 응용 능력을 평가합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
개념을 완벽히 이해한 후 다양한 유형의 문제를 풀어봅니다. 원리 이해에 집중합니다.
</div>

## {city_kor} 주요 중학교 특징

### {schools[0]}

{schools[0]}은 내신 시험 난이도가 높습니다. 서술형 문제 비중이 높고 풀이 과정 채점이 엄격합니다.

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

중2는 함수와 도형이 본격적으로 등장합니다. 고등학교 수학의 기반이 되는 단원입니다.

### 중학교 3학년

중3은 고등학교 수학 선행과 내신 관리를 병행합니다. 이차방정식, 이차함수를 완벽히 익힙니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
학년별 맞춤 커리큘럼으로 진행합니다. 학기 중에는 내신 대비, 방학에는 선행 학습을 병행합니다.
</div>
"""
    else:
        return f"""{city_kor} 고등학교 수학, 중학교와 차원이 다릅니다. 체계적인 학습이 필수입니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
첫 수업에서 학생의 수학 실력을 정밀 진단합니다. 개념 이해도, 문제 해결력, 수능형 사고력까지 파악합니다.
</div>

## {city_kor} 고등학교 수학이 어려운 이유

고등학교 수학은 추상적 개념이 많습니다. 집합, 명제, 함수의 극한 등 눈에 보이지 않는 개념을 다룹니다.

{city_kor} 고등학교들은 내신 난이도가 높습니다. 교과서 수준을 넘어선 심화 문제가 출제됩니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
개념을 완벽히 이해한 후, 다양한 유형의 고난도 문제를 훈련합니다. 수능형 사고력을 기릅니다.
</div>

## {city_kor} 주요 고등학교 특징

### {schools[0]}

{schools[0]}은 내신 시험 난이도가 높습니다. 심화 문제 비중이 높고 서술형 채점이 엄격합니다.

### {schools[1] if len(schools) > 1 else schools[0]}

수능형 문제 출제 비중이 높습니다. 수능 대비와 내신 대비를 병행해야 합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
학교의 기출문제를 철저히 분석합니다. 출제 선생님 스타일, 자주 나오는 유형을 파악합니다.
</div>

## 내신과 수능 병행 전략

### 고1-2: 내신 중심

고1, 고2는 내신을 우선합니다. 학생부 종합전형을 고려하면 내신 등급이 중요합니다.

### 고3: 내신과 수능 병행

고3은 내신과 수능을 동시에 준비합니다. 9월까지는 병행하고, 이후에는 수능에 집중합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
학생의 입시 목표에 맞춰 내신과 수능 비중을 조절합니다. 수시 vs 정시에 따라 전략을 달리합니다.
</div>
"""


def generate_english_content(city_kor, level_kor, schools):
    """영어 콘텐츠 생성"""
    if level_kor == '중등':
        return f"""{city_kor} 중학교 영어, 문법과 독해 실력을 균형 있게 키워야 합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
첫 수업에서 학생의 영어 실력을 종합 진단합니다. 문법, 어휘, 독해, 듣기 각 영역의 수준을 파악합니다.
</div>

## {city_kor} 중학교 영어가 중요한 이유

중학교 영어는 고등학교 수능 영어의 기초입니다. 핵심 문법, 기본 어휘, 독해 능력이 탄탄해야 합니다.

{city_kor} 학교들은 영어 내신 변별력을 높이기 위해 까다로운 문제를 출제합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
교과서 본문을 완벽히 이해한 후, 변형 문제에 대응하는 연습을 합니다.
</div>

## {city_kor} 주요 중학교 특징

### {schools[0]}

{schools[0]}은 서술형 비중이 높습니다. 영작 문제가 어렵고 채점이 엄격합니다.

### {schools[1] if len(schools) > 1 else schools[0]}

독해 지문 난이도가 높습니다. 긴 지문을 빠르게 이해하는 능력이 필요합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
학교의 영어 기출문제를 수집하여 출제 패턴을 분석합니다. 학교별 맞춤 대비 전략을 세웁니다.
</div>

## 영역별 학습 전략

### 문법 학습

문법은 영어의 기초입니다. 시제, 조동사, 부정사, 동명사, 분사, 관계사 등을 체계적으로 정리합니다.

### 독해 학습

독해력은 꾸준한 훈련이 필요합니다. 끊어 읽기, 구문 분석, 문맥 파악 순서로 훈련합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
문법, 독해, 어휘를 균형있게 학습합니다. 학생의 약한 영역에 더 많은 시간을 배분합니다.
</div>
"""
    else:
        return f"""{city_kor} 고등학교 영어, 내신과 수능 모두 만만치 않습니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
첫 수업에서 학생의 영어 실력을 종합 진단합니다. 문법, 독해, 어휘, 듣기 각 영역을 점검합니다.
</div>

## {city_kor} 고등학교 영어가 어려운 이유

고등학교 영어 내신은 변별력을 위해 높은 난이도로 출제됩니다. 교과서 외 지문이 등장합니다.

수능 영어도 절대평가이지만 1등급은 쉽지 않습니다. 빈칸 추론, 순서 배열, 문장 삽입이 핵심입니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
내신과 수능을 균형있게 대비합니다. 학기 중에는 내신 집중, 방학에는 수능 유형 훈련을 병행합니다.
</div>

## {city_kor} 주요 고등학교 영어 특징

### {schools[0]}

{schools[0]} 영어 내신은 독해 지문 난이도가 높습니다. 빠른 독해력이 필요합니다.

### {schools[1] if len(schools) > 1 else schools[0]}

문법 심화 문제가 많습니다. 구문 분석 능력이 필수입니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
학교의 영어 기출문제를 분석합니다. 출제 경향과 자주 나오는 유형을 파악합니다.
</div>

## 수능 영어 대비 전략

### 고난도 유형 공략

빈칸 추론, 순서 배열, 문장 삽입은 수능 영어의 핵심입니다. 글의 논리적 흐름을 파악하는 연습이 필요합니다.

### 듣기 완벽 대비

듣기는 17문항으로 비중이 큽니다. 꾸준한 훈련으로 만점을 목표로 합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
수능 기출문제와 EBS 교재를 활용합니다. 고난도 유형의 접근법을 단계별로 훈련합니다.
</div>
"""


def create_city(city_eng):
    """도시 폴더 및 파일 생성"""
    if city_eng not in CITIES:
        print(f"Unknown city: {city_eng}")
        return

    info = CITIES[city_eng]
    city_kor = info['korean']
    schools_middle = info['schools_middle']
    schools_high = info['schools_high']
    aliases = info.get('aliases', [])
    image = IMAGE_MAP.get(city_eng, '/images/edu_0050_VOUicg8Ejus.jpg')

    # 폴더 생성
    folder_path = f"content/gyeonggi/{city_eng}"
    os.makedirs(folder_path, exist_ok=True)

    # 1. 허브 페이지 생성
    hub_content = generate_city_hub(city_eng, city_kor, schools_middle, schools_high, image, aliases)
    with open(f"{folder_path}/_index.md", 'w', encoding='utf-8') as f:
        f.write(hub_content)
    print(f"Created: {folder_path}/_index.md")

    # 2. 콘텐츠 페이지 생성
    for level in ['middle', 'high']:
        schools = schools_middle if level == 'middle' else schools_high
        for subject in ['math', 'english']:
            content = generate_content_page(
                city_eng, city_kor, level, subject,
                schools, image, aliases
            )
            filename = f"{folder_path}/{level}-{subject}.md"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Created: {filename}")


def main():
    """메인 실행"""
    print("=== 경기도 URL 마이그레이션 ===\n")

    # 경기도 폴더 생성
    os.makedirs("content/gyeonggi", exist_ok=True)

    # 경기도 메인 허브 생성
    hub_content = generate_gyeonggi_hub()
    with open("content/gyeonggi/_index.md", 'w', encoding='utf-8') as f:
        f.write(hub_content)
    print("Created: content/gyeonggi/_index.md\n")

    # 각 도시별 생성
    for city in CITIES.keys():
        print(f"--- {CITIES[city]['korean']} ({city}) ---")
        create_city(city)
        print()

    print("=== 마이그레이션 완료 ===")
    print(f"총 {len(CITIES)}개 시/지역 생성됨")


if __name__ == "__main__":
    main()
