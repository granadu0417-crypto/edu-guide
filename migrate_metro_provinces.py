#!/usr/bin/env python3
"""
광역시 및 도 단위 URL 마이그레이션 스크립트
Phase 2: 부산, 인천
Phase 3: 대구, 대전, 광주, 울산, 세종
Phase 4: 강원, 충북, 충남, 전북, 전남, 경북, 경남, 제주
"""

import os

# =============================================
# Phase 2 & 3: 광역시 데이터
# =============================================

METRO_CITIES = {
    # 부산 (16개 구군)
    'busan': {
        'korean': '부산광역시',
        'short': '부산',
        'districts': {
            'haeundae': {'korean': '해운대구', 'schools': ['해운대고', '센텀고', '반송고', '반여고']},
            'suyeong': {'korean': '수영구', 'schools': ['수영고', '광안고', '망미고', '민락고']},
            'nam': {'korean': '남구', 'schools': ['남고', '대연고', '분포고', '용호고']},
            'dongnae': {'korean': '동래구', 'schools': ['동래고', '동래여고', '명호고', '안락고']},
            'yeonje': {'korean': '연제구', 'schools': ['연제고', '거제고', '연산고', '토현고']},
            'busanjin': {'korean': '부산진구', 'schools': ['부산진고', '부산중앙고', '동의고', '부일여고']},
            'dong': {'korean': '동구', 'schools': ['동구고', '부산자동차고', '성광고', '초량중']},
            'jung_bs': {'korean': '중구', 'schools': ['중앙고', '부산상고', '부산외고', '해양고']},
            'seo': {'korean': '서구', 'schools': ['서구고', '부산공고', '서여고', '남천고']},
            'yeongdo': {'korean': '영도구', 'schools': ['영도고', '영선고', '한바다고', '청운고']},
            'buk': {'korean': '북구', 'schools': ['북구고', '구포고', '덕천고', '화명고']},
            'sasang': {'korean': '사상구', 'schools': ['사상고', '덕포고', '모라고', '동주여고']},
            'gangseo_bs': {'korean': '강서구', 'schools': ['강서고', '명지고', '가락고', '녹산고']},
            'geumjeong': {'korean': '금정구', 'schools': ['금정고', '부산대부고', '오륜고', '금명여고']},
            'saha': {'korean': '사하구', 'schools': ['사하고', '다대고', '괴정고', '신평고']},
            'gijang': {'korean': '기장군', 'schools': ['기장고', '일광고', '정관고', '장안고']},
        },
        'aliases': ['busan-education-guide', 'busan-math-tutoring', 'busan-english-tutoring'],
        'image': '/images/edu_0080_wwy-z7NPTTM.jpg'
    },
    # 인천 (10개 구군)
    'incheon': {
        'korean': '인천광역시',
        'short': '인천',
        'districts': {
            'yeonsu': {'korean': '연수구', 'schools': ['연수고', '인천포스코고', '송도고', '선학고']},
            'namdong': {'korean': '남동구', 'schools': ['남동고', '인천논현고', '구월고', '만수고']},
            'bupyeong': {'korean': '부평구', 'schools': ['부평고', '부개고', '부평여고', '삼산고']},
            'seo_ic': {'korean': '서구', 'schools': ['서구고', '검단고', '가좌고', '인천공고']},
            'gyeyang': {'korean': '계양구', 'schools': ['계양고', '인천계산고', '작전고', '효성고']},
            'michuhol': {'korean': '미추홀구', 'schools': ['인천고', '제물포고', '숭덕여고', '도화고']},
            'dong_ic': {'korean': '동구', 'schools': ['동인천고', '송림고', '인명여고', '창영초']},
            'jung_ic': {'korean': '중구', 'schools': ['인천중앙고', '인천여상', '신흥고', '답동초']},
            'ganghwa': {'korean': '강화군', 'schools': ['강화고', '강화여고', '합일고', '덕신고']},
            'ongjin': {'korean': '옹진군', 'schools': ['영흥고', '옹진고', '북도초', '자월초']},
        },
        'aliases': ['incheon-education-guide', 'incheon-math-tutoring', 'incheon-english-tutoring'],
        'image': '/images/edu_0081_feLC4ZCxGqk.jpg'
    },
    # 대구 (8개 구군)
    'daegu': {
        'korean': '대구광역시',
        'short': '대구',
        'districts': {
            'suseong': {'korean': '수성구', 'schools': ['대구고', '경신고', '정화여고', '수성고']},
            'dalseo': {'korean': '달서구', 'schools': ['달서고', '상원고', '성산고', '월배고']},
            'dong_dg': {'korean': '동구', 'schools': ['동구고', '신명고', '효성여고', '대진고']},
            'buk_dg': {'korean': '북구', 'schools': ['북구고', '복현고', '대구공고', '무학고']},
            'jung_dg': {'korean': '중구', 'schools': ['대구중앙고', '경북고', '계성고', '대구상고']},
            'seo_dg': {'korean': '서구', 'schools': ['서구고', '서부고', '협성고', '비슬고']},
            'nam_dg': {'korean': '남구', 'schools': ['남구고', '대명고', '영남고', '덕화여고']},
            'dalseong': {'korean': '달성군', 'schools': ['달성고', '다사고', '화원고', '논공고']},
        },
        'aliases': ['daegu-education-guide', 'daegu-math-tutoring', 'daegu-english-tutoring'],
        'image': '/images/edu_0082_Hav7EXRbDoE.jpg'
    },
    # 대전 (5개 구)
    'daejeon': {
        'korean': '대전광역시',
        'short': '대전',
        'districts': {
            'seo_dj': {'korean': '서구', 'schools': ['대전고', '충남고', '대전여고', '둔원고']},
            'yuseong': {'korean': '유성구', 'schools': ['유성고', '대전과학고', '충남삼성고', '노은고']},
            'jung_dj': {'korean': '중구', 'schools': ['대전중앙고', '호수돈여고', '대전상고', '대전공고']},
            'dong_dj': {'korean': '동구', 'schools': ['동구고', '대전대신고', '보문고', '대성고']},
            'daedeok': {'korean': '대덕구', 'schools': ['대덕고', '신탄진고', '송촌고', '법동고']},
        },
        'aliases': ['daejeon-education-guide', 'daejeon-math-tutoring', 'daejeon-english-tutoring'],
        'image': '/images/edu_0083_G8NOmGenyeU.jpg'
    },
    # 광주 (5개 구)
    'gwangju': {
        'korean': '광주광역시',
        'short': '광주',
        'districts': {
            'nam_gj': {'korean': '남구', 'schools': ['광주고', '광주제일고', '전남고', '수완고']},
            'seo_gj': {'korean': '서구', 'schools': ['서구고', '광주동성고', '금호고', '광덕고']},
            'buk_gj': {'korean': '북구', 'schools': ['북구고', '전대부고', '광주과학고', '문정고']},
            'dong_gj': {'korean': '동구', 'schools': ['동구고', '광주중앙고', '조대부고', '성덕고']},
            'gwangsan': {'korean': '광산구', 'schools': ['광산고', '첨단고', '운남고', '하남고']},
        },
        'aliases': ['gwangju-education-guide', 'gwangju-math-tutoring', 'gwangju-english-tutoring'],
        'image': '/images/edu_0084_g4WinrGsMl0.jpg'
    },
    # 울산 (5개 구군)
    'ulsan': {
        'korean': '울산광역시',
        'short': '울산',
        'districts': {
            'nam_us': {'korean': '남구', 'schools': ['울산고', '현대고', '학성고', '무거고']},
            'jung_us': {'korean': '중구', 'schools': ['중앙고', '울산여고', '함월고', '학성여고']},
            'dong_us': {'korean': '동구', 'schools': ['동구고', '현대청운고', '방어진고', '울산미용고']},
            'buk_us': {'korean': '북구', 'schools': ['북구고', '울산과학고', '매곡고', '천곡고']},
            'ulju': {'korean': '울주군', 'schools': ['언양고', '범서고', '온양고', '서생고']},
        },
        'aliases': ['ulsan-education-guide', 'ulsan-math-tutoring', 'ulsan-english-tutoring'],
        'image': '/images/edu_0085_SrJuOjX2qso.jpg'
    },
    # 세종 (단일 도시)
    'sejong': {
        'korean': '세종특별자치시',
        'short': '세종',
        'districts': {
            'sejong': {'korean': '세종시', 'schools': ['세종고', '양지고', '아름고', '도담고']},
        },
        'aliases': ['sejong-education-guide', 'sejong-math-tutoring', 'sejong-english-tutoring'],
        'image': '/images/edu_0086_8T-lK9FkzyI.jpg'
    },
}

# =============================================
# Phase 4: 도 단위 데이터
# =============================================

PROVINCES = {
    'gangwon': {
        'korean': '강원특별자치도',
        'short': '강원',
        'cities': {
            'chuncheon': {'korean': '춘천시', 'schools': ['춘천고', '봉의고', '강원고', '춘천여고']},
            'wonju': {'korean': '원주시', 'schools': ['원주고', '상지대부고', '진광고', '원주여고']},
            'gangneung': {'korean': '강릉시', 'schools': ['강릉고', '명륜고', '강릉중앙고', '강릉여고']},
        },
        'aliases': ['gangwon-education-guide', 'gangwon-tutoring-guide'],
        'image': '/images/edu_0087_mblRP7b3Ubo.jpg'
    },
    'chungbuk': {
        'korean': '충청북도',
        'short': '충북',
        'cities': {
            'cheongju': {'korean': '청주시', 'schools': ['청주고', '충북고', '청주여고', '세광고']},
            'chungju': {'korean': '충주시', 'schools': ['충주고', '충주상고', '충주공고', '충주여고']},
        },
        'aliases': ['chungbuk-education-guide', 'chungbuk-tutoring-guide'],
        'image': '/images/edu_0088_-2vD8lIhdnw.jpg'
    },
    'chungnam': {
        'korean': '충청남도',
        'short': '충남',
        'cities': {
            'cheonan': {'korean': '천안시', 'schools': ['천안고', '천안북고', '천안여고', '천안중앙고']},
            'asan': {'korean': '아산시', 'schools': ['아산고', '온양고', '배방고', '아산여고']},
        },
        'aliases': ['chungnam-education-guide', 'chungnam-tutoring-guide'],
        'image': '/images/edu_0089_QR-XQbUVC1s.jpg'
    },
    'jeonbuk': {
        'korean': '전북특별자치도',
        'short': '전북',
        'cities': {
            'jeonju': {'korean': '전주시', 'schools': ['전주고', '전북고', '전주여고', '신흥고']},
            'iksan': {'korean': '익산시', 'schools': ['익산고', '이리고', '남성고', '원광고']},
        },
        'aliases': ['jeonbuk-education-guide', 'jeonbuk-tutoring-guide'],
        'image': '/images/edu_0090_ORDz1m1-q0I.jpg'
    },
    'jeonnam': {
        'korean': '전라남도',
        'short': '전남',
        'cities': {
            'suncheon': {'korean': '순천시', 'schools': ['순천고', '매산고', '순천여고', '팔마고']},
            'yeosu': {'korean': '여수시', 'schools': ['여수고', '여천고', '여수여고', '중앙여고']},
        },
        'aliases': ['jeonnam-education-guide', 'jeonnam-tutoring-guide'],
        'image': '/images/edu_0091_jugJ0wmZ7wk.jpg'
    },
    'gyeongbuk': {
        'korean': '경상북도',
        'short': '경북',
        'cities': {
            'pohang': {'korean': '포항시', 'schools': ['포항고', '포항제철고', '포항여고', '영흥고']},
            'gumi': {'korean': '구미시', 'schools': ['구미고', '금오고', '구미여고', '현일고']},
        },
        'aliases': ['gyeongbuk-education-guide', 'gyeongbuk-tutoring-guide'],
        'image': '/images/edu_0092_JexAuNCfefs.jpg'
    },
    'gyeongnam': {
        'korean': '경상남도',
        'short': '경남',
        'cities': {
            'changwon': {'korean': '창원시', 'schools': ['창원고', '마산고', '창원중앙고', '진해고']},
            'jinju': {'korean': '진주시', 'schools': ['진주고', '경남고', '진주여고', '대아고']},
        },
        'aliases': ['gyeongnam-education-guide', 'gyeongnam-tutoring-guide'],
        'image': '/images/edu_0093_Y125COCWeuQ.jpg'
    },
    'jeju': {
        'korean': '제주특별자치도',
        'short': '제주',
        'cities': {
            'jeju_city': {'korean': '제주시', 'schools': ['제주고', '오현고', '제주여고', '제주중앙고']},
            'seogwipo': {'korean': '서귀포시', 'schools': ['서귀포고', '대정고', '남주고', '서귀포여고']},
        },
        'aliases': ['jeju-education-guide', 'jeju-tutoring-guide'],
        'image': '/images/edu_0094_f1YfrZ1o2r8.jpg'
    },
}


def generate_metro_hub(metro_eng, metro_data):
    """광역시 허브 페이지 생성"""
    metro_kor = metro_data['korean']
    short = metro_data['short']
    districts = metro_data['districts']
    image = metro_data['image']
    aliases = metro_data.get('aliases', [])

    # 별칭
    alias_lines = [f"  - /local/{a}/" for a in aliases]
    aliases_str = '\n'.join(alias_lines)

    # 구 버튼 생성
    buttons = []
    for d_eng, d_info in districts.items():
        buttons.append(f'<a href="/{metro_eng}/{d_eng}/" style="padding: 12px; background: #3b82f6; color: white; text-decoration: none; border-radius: 8px; text-align: center; font-weight: 600;">{d_info["korean"]}</a>')
    buttons_html = '\n'.join(buttons)

    return f"""---
title: "{metro_kor} 과외 | 구별 맞춤 과외 정보"
date: 2025-12-10
description: "{metro_kor} 중등·고등 수학·영어 과외. {short} 전 지역 학교 내신 완벽 대비."
featured_image: "{image}"
regions:
  - {short}
tags:
  - {short}과외
  - {short}수학과외
  - {short}영어과외
aliases:
{aliases_str}
---

## {metro_kor} 과외 안내

{metro_kor} 지역 학생들을 위한 맞춤형 1:1 과외를 제공합니다.

### {short} 구/군 선택

<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(100px, 1fr)); gap: 10px; margin: 20px 0;">
{buttons_html}
</div>

{{{{< cta-dual type="final" >}}}}
"""


def generate_district_hub(metro_eng, metro_kor, district_eng, district_kor, schools, image):
    """구 허브 페이지 생성"""
    schools_str = ', '.join(schools[:4])

    return f"""---
title: "{district_kor} 과외 | 중등·고등 맞춤 과외"
date: 2025-12-10
description: "{district_kor} 중등·고등 수학·영어 과외. {schools_str} 등 내신 완벽 대비."
featured_image: "{image}"
regions:
  - {metro_kor}
cities:
  - {district_kor}
tags:
  - {district_kor}과외
  - {district_kor}수학과외
---

## {district_kor} 과외 안내

{district_kor} 지역 학생들을 위한 맞춤형 1:1 과외입니다.

### {district_kor} 주요 학교

{schools_str}

### 과외 과목

아래에서 과목별 정보를 확인하세요.
"""


def generate_content(region_kor, level, subject, schools, image):
    """콘텐츠 페이지 생성"""
    level_kor = '중등' if level == 'middle' else '고등'
    subject_kor = '수학' if subject == 'math' else '영어'
    schools_str = '·'.join(schools[:3])

    if level == 'middle':
        price = "**중학생**은 주1회 22만원 - 32만원, 주2회 29만원 - 47만원 선입니다."
    else:
        price = """**고1-2**는 주1회 25만원 - 36만원, 주2회 33만원 - 53만원 선입니다.

**고3**은 주1회 28만원 - 40만원, 주2회 37만원 - 59만원이 일반적입니다."""

    return f"""---
title: "{region_kor} {level_kor} {subject_kor}과외 | {schools_str} 내신 대비"
date: 2025-12-10
description: "{region_kor} {level_kor}학생 {subject_kor}과외 전문. {schools_str} 등 내신 맞춤 관리."
featured_image: "{image}"
categories:
  - {level_kor}교육
  - {subject_kor}과외
tags:
  - {region_kor}{subject_kor}과외
  - {region_kor}{level_kor}{subject_kor}
---

{region_kor} {level_kor}학생 {subject_kor}, 체계적인 1:1 과외로 실력을 높여드립니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
첫 수업에서 학생의 실력을 정확히 진단합니다. 약점을 파악하고 맞춤 전략을 수립합니다.
</div>

## {region_kor} {level_kor} {subject_kor}이 중요한 이유

{level_kor} {subject_kor}은 학교 내신과 수능 모두에서 중요합니다. 기초부터 탄탄히 잡아야 합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
개념을 완벽히 이해한 후 다양한 유형의 문제를 풀어봅니다.
</div>

## {region_kor} 주요 학교

{schools_str} 등 {region_kor} 학교들의 내신 특성에 맞춘 수업을 진행합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
학교 기출문제를 분석하여 출제 경향을 파악합니다.
</div>

## 수업료 안내

{price}

정확한 금액은 상담을 통해 안내드립니다.

{{{{< cta-dual type="final" >}}}}

## 자주 묻는 질문

**Q. 기초가 부족해도 수업 가능한가요?**

가능합니다. 학생의 현재 수준에서 시작합니다.

**Q. 내신 시험 전에 집중 수업이 가능한가요?**

가능합니다. 시험 기간에 수업 횟수를 늘릴 수 있습니다.

## 마무리

{region_kor} {level_kor}학생 여러분, 지금 시작하세요.
"""


def generate_province_hub(province_eng, province_data):
    """도 허브 페이지 생성"""
    province_kor = province_data['korean']
    short = province_data['short']
    cities = province_data['cities']
    image = province_data['image']
    aliases = province_data.get('aliases', [])

    alias_lines = [f"  - /local/{a}/" for a in aliases]
    aliases_str = '\n'.join(alias_lines)

    buttons = []
    for c_eng, c_info in cities.items():
        buttons.append(f'<a href="/provinces/{province_eng}/{c_eng}/" style="padding: 12px; background: #f97316; color: white; text-decoration: none; border-radius: 8px; text-align: center; font-weight: 600;">{c_info["korean"]}</a>')
    buttons_html = '\n'.join(buttons)

    return f"""---
title: "{province_kor} 과외 | 지역별 맞춤 과외 정보"
date: 2025-12-10
description: "{province_kor} 중등·고등 수학·영어 과외. {short} 주요 도시 학교 내신 완벽 대비."
featured_image: "{image}"
regions:
  - {short}
tags:
  - {short}과외
  - {short}수학과외
  - {short}영어과외
aliases:
{aliases_str}
---

## {province_kor} 과외 안내

{province_kor} 지역 학생들을 위한 맞춤형 1:1 과외를 제공합니다.

### {short} 주요 도시

<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(100px, 1fr)); gap: 10px; margin: 20px 0;">
{buttons_html}
</div>

{{{{< cta-dual type="final" >}}}}
"""


def create_metro_city(metro_eng, metro_data):
    """광역시 폴더 및 파일 생성"""
    metro_kor = metro_data['korean']
    districts = metro_data['districts']
    image = metro_data['image']

    # 광역시 폴더 생성
    metro_path = f"content/{metro_eng}"
    os.makedirs(metro_path, exist_ok=True)

    # 허브 페이지 생성
    hub = generate_metro_hub(metro_eng, metro_data)
    with open(f"{metro_path}/_index.md", 'w', encoding='utf-8') as f:
        f.write(hub)
    print(f"Created: {metro_path}/_index.md")

    # 각 구별 페이지 생성
    for d_eng, d_info in districts.items():
        d_kor = d_info['korean']
        schools = d_info['schools']

        d_path = f"{metro_path}/{d_eng}"
        os.makedirs(d_path, exist_ok=True)

        # 구 허브
        d_hub = generate_district_hub(metro_eng, metro_kor, d_eng, d_kor, schools, image)
        with open(f"{d_path}/_index.md", 'w', encoding='utf-8') as f:
            f.write(d_hub)

        # 4개 콘텐츠 파일
        for level in ['middle', 'high']:
            for subject in ['math', 'english']:
                content = generate_content(d_kor, level, subject, schools, image)
                with open(f"{d_path}/{level}-{subject}.md", 'w', encoding='utf-8') as f:
                    f.write(content)

        print(f"Created: {d_path}/ (5 files)")


def create_province(province_eng, province_data):
    """도 폴더 및 파일 생성"""
    province_kor = province_data['korean']
    cities = province_data['cities']
    image = province_data['image']

    # 도 폴더 생성
    province_path = f"content/provinces/{province_eng}"
    os.makedirs(province_path, exist_ok=True)

    # 허브 페이지 생성
    hub = generate_province_hub(province_eng, province_data)
    with open(f"{province_path}/_index.md", 'w', encoding='utf-8') as f:
        f.write(hub)
    print(f"Created: {province_path}/_index.md")

    # 각 도시별 페이지 생성
    for c_eng, c_info in cities.items():
        c_kor = c_info['korean']
        schools = c_info['schools']

        c_path = f"{province_path}/{c_eng}"
        os.makedirs(c_path, exist_ok=True)

        # 도시 허브
        c_hub = generate_district_hub(province_eng, province_kor, c_eng, c_kor, schools, image)
        with open(f"{c_path}/_index.md", 'w', encoding='utf-8') as f:
            f.write(c_hub)

        # 4개 콘텐츠 파일
        for level in ['middle', 'high']:
            for subject in ['math', 'english']:
                content = generate_content(c_kor, level, subject, schools, image)
                with open(f"{c_path}/{level}-{subject}.md", 'w', encoding='utf-8') as f:
                    f.write(content)

        print(f"Created: {c_path}/ (5 files)")


def main():
    print("=" * 50)
    print("Phase 2 & 3: 광역시 마이그레이션")
    print("=" * 50)

    for metro_eng, metro_data in METRO_CITIES.items():
        print(f"\n--- {metro_data['korean']} ({metro_eng}) ---")
        create_metro_city(metro_eng, metro_data)

    print("\n" + "=" * 50)
    print("Phase 4: 도 단위 마이그레이션")
    print("=" * 50)

    # provinces 폴더 생성
    os.makedirs("content/provinces", exist_ok=True)

    # provinces 허브 페이지
    provinces_hub = """---
title: "도 단위 지역 과외 | 전국 지역별 맞춤 과외"
date: 2025-12-10
description: "강원, 충북, 충남, 전북, 전남, 경북, 경남, 제주 지역 중등·고등 과외 정보."
featured_image: "/images/edu_0087_mblRP7b3Ubo.jpg"
tags:
  - 지역과외
  - 전국과외
---

## 도 단위 지역 과외 안내

전국 도 단위 지역의 과외 정보를 제공합니다.

### 지역 선택

<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(100px, 1fr)); gap: 10px; margin: 20px 0;">
<a href="/provinces/gangwon/" style="padding: 12px; background: #f97316; color: white; text-decoration: none; border-radius: 8px; text-align: center; font-weight: 600;">강원</a>
<a href="/provinces/chungbuk/" style="padding: 12px; background: #f97316; color: white; text-decoration: none; border-radius: 8px; text-align: center; font-weight: 600;">충북</a>
<a href="/provinces/chungnam/" style="padding: 12px; background: #f97316; color: white; text-decoration: none; border-radius: 8px; text-align: center; font-weight: 600;">충남</a>
<a href="/provinces/jeonbuk/" style="padding: 12px; background: #f97316; color: white; text-decoration: none; border-radius: 8px; text-align: center; font-weight: 600;">전북</a>
<a href="/provinces/jeonnam/" style="padding: 12px; background: #f97316; color: white; text-decoration: none; border-radius: 8px; text-align: center; font-weight: 600;">전남</a>
<a href="/provinces/gyeongbuk/" style="padding: 12px; background: #f97316; color: white; text-decoration: none; border-radius: 8px; text-align: center; font-weight: 600;">경북</a>
<a href="/provinces/gyeongnam/" style="padding: 12px; background: #f97316; color: white; text-decoration: none; border-radius: 8px; text-align: center; font-weight: 600;">경남</a>
<a href="/provinces/jeju/" style="padding: 12px; background: #f97316; color: white; text-decoration: none; border-radius: 8px; text-align: center; font-weight: 600;">제주</a>
</div>

{{< cta-dual type="final" >}}
"""
    with open("content/provinces/_index.md", 'w', encoding='utf-8') as f:
        f.write(provinces_hub)
    print("\nCreated: content/provinces/_index.md")

    for province_eng, province_data in PROVINCES.items():
        print(f"\n--- {province_data['korean']} ({province_eng}) ---")
        create_province(province_eng, province_data)

    print("\n" + "=" * 50)
    print("마이그레이션 완료!")
    print("=" * 50)


if __name__ == "__main__":
    main()
