#!/usr/bin/env python3
"""
경기도 콘텐츠 확장 재생성 스크립트
- 250-300줄 콘텐츠 생성
- 표현 풀 시스템 활용
"""

import os
import sys
import re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from expression_pools import (
    INTRO_HIGH_MATH, INTRO_HIGH_ENG, INTRO_MID_MATH, INTRO_MID_ENG,
    H2_HIGH_MATH_WHY, H2_HIGH_MATH_EXAM, H2_HIGH_MATH_SUNEUNG,
    H2_HIGH_MATH_COMPARE, H2_HIGH_MATH_GRADE,
    H2_HIGH_ENG_WHY, H2_MID_MATH_WHY, H2_MID_ENG_WHY,
    IVORY_BOX_POOL, ENDING_POOL, IMAGE_POOL,
    BODY_HIGH_MATH_WHY, BODY_COMPARE, BODY_GRADE_STRATEGY,
    FAQ_Q1_VARIANTS, FAQ_A1_VARIANTS,
    FAQ_Q2_VARIANTS, FAQ_A2_VARIANTS,
    FAQ_Q3_VARIANTS, FAQ_A3_VARIANTS,
    FAQ_Q4_VARIANTS, FAQ_A4_VARIANTS,
    get_pool_item
)

# 도시 정보
CITY_INFO = {
    "suwon": {"name": "수원시", "gu_map": {"jangan": "장안구", "gwonseon": "권선구", "paldal": "팔달구", "yeongtong": "영통구"}},
    "seongnam": {"name": "성남시", "gu_map": {"sujeong": "수정구", "jungwon": "중원구", "bundang": "분당구"}},
    "yongin": {"name": "용인시", "gu_map": {"suji": "수지구", "giheung": "기흥구", "cheoin": "처인구"}},
    "goyang": {"name": "고양시", "gu_map": {}},
    "bucheon": {"name": "부천시", "gu_map": {}},
    "ansan": {"name": "안산시", "gu_map": {"danwon": "단원구", "sangnok": "상록구"}},
    "anyang": {"name": "안양시", "gu_map": {"dongan": "동안구", "manan": "만안구"}},
    "namyangju": {"name": "남양주시", "gu_map": {}},
    "hwaseong": {"name": "화성시", "gu_map": {}},
    "pyeongtaek": {"name": "평택시", "gu_map": {}},
    "uijeongbu": {"name": "의정부시", "gu_map": {}},
    "siheung": {"name": "시흥시", "gu_map": {}},
    "paju": {"name": "파주시", "gu_map": {}},
    "gimpo": {"name": "김포시", "gu_map": {}},
    "gwangmyeong": {"name": "광명시", "gu_map": {}},
    "gunpo": {"name": "군포시", "gu_map": {}},
    "hanam": {"name": "하남시", "gu_map": {}},
    "osan": {"name": "오산시", "gu_map": {}},
    "icheon": {"name": "이천시", "gu_map": {}},
    "yangju": {"name": "양주시", "gu_map": {}},
    "guri": {"name": "구리시", "gu_map": {}},
    "bundang": {"name": "분당구", "gu_map": {}},
    "ilsan": {"name": "일산구", "gu_map": {}},
    "pyeongchon": {"name": "평촌", "gu_map": {}},
    "gwangju_gg": {"name": "광주시", "gu_map": {}},
    "anseong": {"name": "안성시", "gu_map": {}},
}

# 도시별 학교
CITY_SCHOOLS = {
    "suwon": (["수원외고", "경기과학고", "삼일공고", "수원고", "영통고", "매탄고", "청명고"], ["수원중", "영통중", "매탄중", "청명중", "장안중", "권선중"]),
    "seongnam": (["분당고", "서현고", "야탑고", "성남외고", "낙생고", "태평고", "수내고"], ["분당중", "서현중", "야탑중", "수내중", "정자중", "이매중"]),
    "yongin": (["용인고", "수지고", "기흥고", "죽전고", "풍덕고", "용인외고"], ["용인중", "수지중", "기흥중", "죽전중", "풍덕중"]),
    "goyang": (["일산고", "정발고", "저현고", "주엽고", "백마고", "덕양고"], ["일산중", "정발중", "저현중", "주엽중", "백마중"]),
    "bucheon": (["부천고", "부명고", "원미고", "상동고", "소사고", "중흥고"], ["부천중", "부명중", "원미중", "상동중", "소사중"]),
    "ansan": (["안산고", "단원고", "성포고", "원곡고", "광덕고", "선부고"], ["안산중", "단원중", "성포중", "원곡중", "광덕중"]),
    "anyang": (["안양고", "평촌고", "범계고", "관양고", "비산고", "동안고"], ["안양중", "평촌중", "범계중", "관양중", "비산중"]),
    "namyangju": (["남양주고", "호평고", "도농고", "진접고", "별내고", "다산고"], ["남양주중", "호평중", "도농중", "진접중", "별내중"]),
    "hwaseong": (["화성고", "동탄고", "병점고", "능동고", "반월고", "향남고"], ["화성중", "동탄중", "병점중", "능동중", "반월중"]),
    "pyeongtaek": (["평택고", "세교고", "비전고", "청북고", "한광고", "평택여고"], ["평택중", "세교중", "비전중", "청북중", "한광중"]),
    "uijeongbu": (["의정부고", "송양고", "호원고", "발곡고", "경민고", "의정부여고"], ["의정부중", "송양중", "호원중", "발곡중", "경민중"]),
    "siheung": (["시흥고", "배곧고", "은행고", "함현고", "정왕고", "시화고"], ["시흥중", "배곧중", "은행중", "함현중", "정왕중"]),
    "paju": (["파주고", "금촌고", "교하고", "운정고", "한민고", "문산고"], ["파주중", "금촌중", "교하중", "운정중", "한민중"]),
    "gimpo": (["김포고", "양촌고", "장기고", "풍무고", "솔터고", "김포외고"], ["김포중", "양촌중", "장기중", "풍무중", "솔터중"]),
    "gwangmyeong": (["광명고", "광명북고", "충현고", "진성고", "명문고", "광휘고"], ["광명중", "광명북중", "충현중", "진성중", "명문중"]),
    "gunpo": (["군포고", "흥진고", "산본고", "당정고", "수리고", "군포중앙고"], ["군포중", "흥진중", "산본중", "당정중", "수리중"]),
    "hanam": (["하남고", "위례고", "미사고", "창우고", "덕풍고", "풍산고"], ["하남중", "위례중", "미사중", "창우중", "덕풍중"]),
    "osan": (["오산고", "세마고", "성호고", "운암고", "매홀고", "오산정보고"], ["오산중", "세마중", "성호중", "운암중", "매홀중"]),
    "icheon": (["이천고", "효양고", "증포고", "부발고", "대월고", "이천제일고"], ["이천중", "효양중", "증포중", "부발중", "대월중"]),
    "yangju": (["양주고", "덕정고", "회천고", "백석고", "고읍고", "양주백석고"], ["양주중", "덕정중", "회천중", "백석중", "고읍중"]),
    "guri": (["구리고", "인창고", "토평고", "갈매고", "동구고", "구리여고"], ["구리중", "인창중", "토평중", "갈매중", "동구중"]),
    "bundang": (["분당고", "서현고", "야탑고", "수내고", "낙생고"], ["분당중", "서현중", "야탑중", "수내중", "낙생중"]),
    "ilsan": (["일산고", "정발고", "저현고", "주엽고", "백마고"], ["일산중", "정발중", "저현중", "주엽중", "백마중"]),
    "pyeongchon": (["평촌고", "범계고", "관양고", "비산고", "귀인고"], ["평촌중", "범계중", "관양중", "비산중", "귀인중"]),
    "gwangju_gg": (["광주고", "중앙고", "경기광주고", "태전고", "곤지암고"], ["광주중", "중앙중", "경기광주중", "태전중", "곤지암중"]),
    "anseong": (["안성고", "안성여고", "공도고", "미양고", "안법고"], ["안성중", "안성여중", "공도중", "미양중", "안법중"]),
}


def get_dong_name_ko(dong_path):
    """_index.md에서 동 한글 이름만 추출"""
    index_file = os.path.join(dong_path, "_index.md")
    if os.path.exists(index_file):
        with open(index_file, "r", encoding="utf-8") as f:
            content = f.read()
            match = re.search(r'title:\s*"?([^"\n]+)"?', content)
            if match:
                title = match.group(1).strip()
                title = title.replace(" 과외", "").strip()
                parts = title.split()
                if len(parts) > 0:
                    return parts[-1]
    return os.path.basename(dong_path)


def create_high_math_content(city_name, gu_name, dong_name, schools_high, file_index):
    """고등 수학 콘텐츠 생성 (250-300줄)"""
    school_str = "·".join(schools_high[:3])
    idx = file_index

    intro = get_pool_item(INTRO_HIGH_MATH, idx)
    h2_why = get_pool_item(H2_HIGH_MATH_WHY, idx + 3)
    h2_exam = get_pool_item(H2_HIGH_MATH_EXAM, idx + 7)
    h2_suneung = get_pool_item(H2_HIGH_MATH_SUNEUNG, idx + 11)
    h2_compare = get_pool_item(H2_HIGH_MATH_COMPARE, idx + 13)
    h2_grade = get_pool_item(H2_HIGH_MATH_GRADE, idx + 17)

    body_why = get_pool_item(BODY_HIGH_MATH_WHY, idx + 5)
    body_compare = get_pool_item(BODY_COMPARE, idx + 9)
    body_grade = get_pool_item(BODY_GRADE_STRATEGY, idx + 15)

    boxes = [get_pool_item(IVORY_BOX_POOL, idx + i * 7) for i in range(12)]
    ending = get_pool_item(ENDING_POOL, idx + 19)
    image = get_pool_item(IMAGE_POOL, idx + 23)

    faq_q1 = get_pool_item(FAQ_Q1_VARIANTS, idx)
    faq_a1 = get_pool_item(FAQ_A1_VARIANTS, idx + 2)
    faq_q2 = get_pool_item(FAQ_Q2_VARIANTS, idx + 1)
    faq_a2 = get_pool_item(FAQ_A2_VARIANTS, idx + 3)
    faq_q3 = get_pool_item(FAQ_Q3_VARIANTS, idx + 4)
    faq_a3 = get_pool_item(FAQ_A3_VARIANTS, idx + 5)
    faq_q4 = get_pool_item(FAQ_Q4_VARIANTS, idx + 6)
    faq_a4 = get_pool_item(FAQ_A4_VARIANTS, idx + 7)

    if gu_name:
        location = f"{city_name} {gu_name} {dong_name}"
        location_short = f"{gu_name} {dong_name}"
    else:
        location = f"{city_name} {dong_name}"
        location_short = dong_name

    content = f'''---
title: "{location} 고등 수학과외 | {school_str} 내신·수능 대비"
date: 2025-01-15
categories:
  - 고등교육
regions:
  - 경기도
  - {city_name}
cities:
  - {gu_name if gu_name else city_name}
description: "{location} 고등학생 수학과외 전문. {schools_high[0]} 내신과 수능 동시 대비. 개념부터 킬러문항까지 체계적 1:1 지도."
tags:
  - {city_name}
  - {gu_name if gu_name else dong_name}
  - {dong_name}
  - 고등수학
  - 수학과외
  - 내신관리
  - 수능대비
  - {schools_high[0]}
featured_image: "https://images.unsplash.com/{image}?w=1200&h=630&fit=crop"
---
{intro}

{dong_name} 지역에서 고등학교 수학 때문에 고민하고 계신가요? 많은 학생들이 중학교까지는 수학을 잘했는데 고등학교에 올라오면서 성적이 떨어지는 경험을 합니다. 이는 자연스러운 현상이지만, 적절한 대비 없이는 격차가 점점 벌어질 수 있습니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[0]}
</div>

## {h2_why}

{body_why}

고등학교 수학은 중학교와 질적으로 다릅니다. 단순 계산에서 벗어나 논리적 사고력과 추상적 개념 이해가 필요합니다. 수학 I, 수학 II, 미적분, 확률과 통계 등 과목도 세분화되어 각 영역에 대한 깊은 이해가 요구됩니다.

{dong_name} 지역 {schools_high[0]} 학생들은 높은 내신 경쟁과 수능 준비를 동시에 해야 합니다. 학교 시험은 학교별 특성에 맞춰 대비해야 하고, 수능은 전국 단위 경쟁이므로 또 다른 전략이 필요합니다.

특히 고등학교 수학에서는 개념 간의 연결이 중요합니다. 함수의 개념이 미적분으로 이어지고, 수열이 극한과 연결됩니다. 하나의 개념을 놓치면 연쇄적으로 어려움을 겪게 됩니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[1]}
</div>

## {h2_exam}

{schools_high[0]}은 내신 시험 난이도가 높습니다. 교과서 기본 문제는 물론, 심화 문제와 변형 문제가 많이 출제됩니다. 단순히 공식을 외워서는 좋은 점수를 받기 어렵고, 개념을 깊이 이해하고 다양한 유형에 적용할 수 있어야 합니다.

시험 시간 대비 문제 양이 많은 편이어서 시간 관리도 중요합니다. 평소 시간을 재고 문제를 푸는 연습을 해야 실전에서 당황하지 않습니다.

내신 시험에서는 학교 선생님의 출제 스타일을 파악하는 것이 중요합니다. 수업 시간에 강조한 내용, 프린트로 나눠준 문제, 기출문제의 패턴을 분석하면 시험 대비에 큰 도움이 됩니다.

{schools_high[1]}과 {schools_high[2]}도 각각의 특성이 있습니다. 학교마다 선호하는 문제 유형과 난이도가 다르기 때문에 학교별 맞춤 대비가 필요합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[2]}
</div>

## 자주 하는 실수와 해결법

고등학생들이 수학에서 자주 하는 실수가 있습니다. 이런 실수를 인식하고 고치는 것이 성적 향상의 지름길입니다.

첫째, 개념을 대충 넘어가는 것입니다. 문제만 많이 풀면 된다고 생각하지만, 개념이 불완전하면 응용 문제에서 막힙니다. 개념 이해에 충분한 시간을 투자해야 합니다.

둘째, 오답 정리를 하지 않는 것입니다. 틀린 문제를 그냥 넘어가면 같은 실수를 반복합니다. 왜 틀렸는지, 어떤 개념이 부족했는지 분석하는 습관이 필요합니다.

셋째, 계산 실수를 가볍게 여기는 것입니다. 개념은 알았는데 계산에서 틀리면 아는 문제도 틀리게 됩니다. 검산 습관을 들이고, 자주 하는 계산 실수 유형을 파악해야 합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[3]}
</div>

## {h2_suneung}

수능 수학은 내신과 출제 방식이 다릅니다. 킬러 문항이라 불리는 21번, 29번, 30번 문제는 여러 개념을 복합적으로 적용해야 풀 수 있습니다. 시간 압박 속에서 정확하게 문제를 푸는 능력이 필요합니다.

수능에서 1등급을 받으려면 킬러 문항 중 최소 1-2개는 맞혀야 합니다. 이를 위해서는 기본 개념이 완벽해야 하고, 다양한 심화 문제를 풀어본 경험이 있어야 합니다.

수능 수학의 또 다른 특징은 시간 관리입니다. 100분 동안 30문제를 풀어야 하는데, 앞부분 쉬운 문제에서 시간을 절약해야 뒷부분 어려운 문제에 집중할 수 있습니다.

EBS 연계율도 고려해야 합니다. 수능특강, 수능완성 교재에서 출제 비중이 높으므로, EBS 교재를 꼼꼼히 학습하면 유리합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[4]}
</div>

## 효과적인 학습 방법

수학 성적을 올리기 위한 효과적인 학습 방법을 소개합니다.

개념 학습 단계에서는 교과서와 개념서를 꼼꼼히 읽고, 각 개념이 왜 필요한지 이해해야 합니다. 공식을 외우기보다 공식이 어떻게 유도되는지 알면 기억에 오래 남습니다.

문제 풀이 단계에서는 난이도를 점진적으로 높여가야 합니다. 기본 문제로 개념을 확인하고, 유형 문제로 적용력을 키우고, 심화 문제로 사고력을 높입니다.

복습 단계에서는 틀린 문제를 중심으로 해야 합니다. 오답노트를 만들어 주기적으로 확인하면 같은 실수를 반복하지 않게 됩니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[5]}
</div>

## {h2_compare}

{body_compare}

학원에서는 정해진 커리큘럼을 따라가야 합니다. 내가 이미 아는 내용도 들어야 하고, 모르는 부분이 있어도 진도를 맞춰야 합니다. 질문 시간도 제한적입니다.

1:1 과외에서는 학생의 현재 수준과 목표에 맞춘 맞춤 수업이 가능합니다. 아는 부분은 빠르게 넘어가고, 모르는 부분은 이해할 때까지 설명을 들을 수 있습니다.

질문하기 어려운 학생도 1:1 수업에서는 편하게 물어볼 수 있습니다. 이해될 때까지 설명을 듣고, 스스로 문제를 풀어보며 실력을 키울 수 있습니다.

또한 과외에서는 학생의 학습 습관과 성향까지 고려한 지도가 가능합니다. 집중 시간이 짧은 학생, 꼼꼼하지만 느린 학생, 빠르지만 실수가 많은 학생 등 각각에 맞는 접근법이 있습니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[6]}
</div>

## {h2_grade}

{body_grade}

고1은 고등학교 수학의 기초를 다지는 시기입니다. 수학(상), 수학(하)에서 다항식, 방정식, 부등식, 함수의 기본 개념을 확실히 잡아야 합니다. 이 시기에 기초가 흔들리면 고2, 고3에서 더 힘들어집니다.

고2는 본격적인 심화 학습 시기입니다. 수학 I, 수학 II를 배우면서 삼각함수, 수열, 미분, 적분의 개념을 익힙니다. 문·이과 선택에 따라 학습 내용이 달라지므로 진로와 연계해서 전략을 세워야 합니다.

고3은 실전 대비 시기입니다. 새로운 개념 학습보다 문제 풀이력 향상에 집중합니다. 모의고사와 기출문제를 통해 실전 감각을 키우고, 취약 단원을 보완합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[7]}
</div>

## 단원별 학습 포인트

고등학교 수학의 주요 단원별 학습 포인트를 안내합니다.

다항식과 방정식 단원에서는 인수분해와 근의 공식을 확실히 익혀야 합니다. 이 단원은 이후 모든 단원의 기초가 됩니다.

함수 단원에서는 함수의 개념과 그래프를 이해하는 것이 핵심입니다. 합성함수, 역함수까지 자연스럽게 연결해서 학습해야 합니다.

삼각함수 단원에서는 삼각비에서 시작해서 삼각함수의 그래프, 삼각방정식까지 단계적으로 학습합니다. 공식이 많아 혼란스러울 수 있으므로 정리가 중요합니다.

미적분 단원에서는 극한의 개념부터 정확히 이해해야 합니다. 미분과 적분의 관계를 이해하고, 다양한 함수에 적용할 수 있어야 합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[8]}
</div>

## 수업료 안내

{location} 지역 고등학교 수학 과외 수업료를 안내합니다.

**고1-2**는 주1회 25만원 - 36만원, 주2회 33만원 - 53만원 선입니다.

**고3**은 주1회 28만원 - 40만원, 주2회 37만원 - 59만원이 일반적입니다.

수업료는 학생의 현재 수준, 목표, 수업 강도에 따라 달라질 수 있습니다. 정확한 금액은 상담을 통해 안내드립니다.

첫 수업은 무료 체험으로 진행할 수 있습니다. 학생과 선생님의 궁합을 확인하고 결정하시면 됩니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[9]}
</div>

## 수업 진행 방식

수업은 다음과 같이 진행됩니다.

첫 수업에서는 학생의 현재 실력을 진단합니다. 어떤 단원이 취약한지, 어떤 유형에서 실수가 많은지 파악합니다. 이를 바탕으로 맞춤 커리큘럼을 설계합니다.

매 수업은 지난 시간 복습으로 시작합니다. 숙제 검사와 오답 분석을 통해 이해도를 확인합니다. 새로운 내용을 배운 후에는 확인 문제를 풀어봅니다.

시험 기간에는 시험 대비 수업으로 전환합니다. 시험 범위에 맞춰 핵심 개념을 정리하고, 예상 문제를 풀어봅니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[10]}
</div>

{{{{< cta-dual type="final" >}}}}

## 자주 묻는 질문

**Q. {faq_q1}**

{faq_a1}

**Q. {faq_q2}**

{faq_a2}

**Q. {faq_q3}**

{faq_a3}

**Q. {faq_q4}**

{faq_a4}

**Q. 수업 시간과 장소는 어떻게 되나요?**

학생과 협의하여 결정합니다. 방문 수업, 카페 수업, 온라인 수업 모두 가능합니다. 시간은 학생의 학교 일정에 맞춰 조정합니다.

**Q. 교재는 어떤 것을 사용하나요?**

학생의 수준과 목표에 맞는 교재를 추천해드립니다. 학교 교과서, 기본서, 유형서, 심화서 등을 조합하여 사용합니다. 내신 대비 시에는 학교 프린트와 기출문제도 활용합니다.

## 마무리

{location_short} 지역에서 고등학교 수학 때문에 고민하고 계신다면, 지금이 시작할 때입니다.

수학은 한 번 놓치면 따라잡기 어려운 과목입니다. 하지만 제대로 된 방법으로 공부하면 누구나 실력을 올릴 수 있습니다.

{location_short} 학생 여러분, {ending}

상담은 무료입니다. 부담 없이 연락 주세요.
'''
    return content


def create_high_english_content(city_name, gu_name, dong_name, schools_high, file_index):
    """고등 영어 콘텐츠 생성 (250-300줄)"""
    school_str = "·".join(schools_high[:3])
    idx = file_index + 50

    intro = get_pool_item(INTRO_HIGH_ENG, idx)
    h2_why = get_pool_item(H2_HIGH_ENG_WHY, idx + 3)

    boxes = [get_pool_item(IVORY_BOX_POOL, idx + i * 11) for i in range(12)]
    ending = get_pool_item(ENDING_POOL, idx + 29)
    image = get_pool_item(IMAGE_POOL, idx + 37)

    if gu_name:
        location = f"{city_name} {gu_name} {dong_name}"
        location_short = f"{gu_name} {dong_name}"
    else:
        location = f"{city_name} {dong_name}"
        location_short = dong_name

    content = f'''---
title: "{location} 고등 영어과외 | {school_str} 내신·수능 대비"
date: 2025-01-15
categories:
  - 고등교육
regions:
  - 경기도
  - {city_name}
cities:
  - {gu_name if gu_name else city_name}
description: "{location} 고등학생 영어과외 전문. {schools_high[0]} 내신과 수능 동시 대비. 독해력 향상부터 고난도 문법까지 체계적 1:1 지도."
tags:
  - {city_name}
  - {gu_name if gu_name else dong_name}
  - {dong_name}
  - 고등영어
  - 영어과외
  - 내신관리
  - 수능대비
  - {schools_high[0]}
featured_image: "https://images.unsplash.com/{image}?w=1200&h=630&fit=crop"
---
{intro}

{dong_name} 지역에서 고등학교 영어 성적 때문에 고민하고 계신가요? 고등학교 영어는 중학교와 차원이 다릅니다. 지문 길이가 길어지고, 어휘 수준이 높아지며, 문법도 복잡해집니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[0]}
</div>

## {h2_why}

고등학교 영어는 중학교와 질적으로 다릅니다. 수능 영어는 70분 안에 45문제를 풀어야 하는 시간 싸움이기도 합니다. 지문 하나의 길이가 200단어를 넘는 경우도 많고, 추상적인 내용을 다루는 지문도 자주 등장합니다.

{dong_name} 지역 {schools_high[0]} 학생들은 내신과 수능을 동시에 준비해야 합니다. 내신은 교과서 중심, 수능은 EBS 연계와 비연계 지문 모두 준비해야 합니다.

영어 실력을 올리기 위해서는 어휘, 문법, 독해 세 가지를 균형 있게 학습해야 합니다. 어느 하나라도 부족하면 성적 향상에 한계가 있습니다.

특히 고등학교 영어에서는 문맥 파악 능력이 중요합니다. 단순히 문장을 해석하는 것을 넘어, 글 전체의 흐름과 논리를 이해해야 합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[1]}
</div>

## 내신 영어 시험 분석

{schools_high[0]} 영어 시험은 교과서 본문 암기만으로는 부족합니다. 변형 문제, 서술형 문제, 문법 적용 문제가 출제됩니다. 본문의 핵심 구문을 정확히 이해하고, 다양한 형태로 변형된 문제에 대응할 수 있어야 합니다.

서술형 비중이 높아 영작 능력도 필요합니다. 문법적으로 정확하고 문맥에 맞는 문장을 쓸 수 있어야 합니다.

내신 시험에서는 교과서뿐 아니라 부교재와 프린트 내용도 출제됩니다. 수업 시간에 선생님이 강조한 표현, 추가로 설명한 문법 사항을 꼼꼼히 정리해야 합니다.

{schools_high[1]}과 {schools_high[2]}도 각각의 출제 특성이 있습니다. 학교별로 선호하는 문제 유형이 다르기 때문에 학교별 맞춤 대비가 필요합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[2]}
</div>

## 자주 하는 실수와 해결법

고등학생들이 영어에서 자주 하는 실수가 있습니다. 이런 실수를 인식하고 고치는 것이 성적 향상의 지름길입니다.

첫째, 단어만 외우고 문장에서 활용하지 못하는 것입니다. 단어는 문장 속에서 어떻게 쓰이는지까지 함께 학습해야 합니다.

둘째, 문법을 규칙만 외우고 적용하지 못하는 것입니다. 문법 문제를 풀 때뿐 아니라 독해와 영작에서도 활용할 수 있어야 합니다.

셋째, 직독직해를 하지 않고 한국어 어순으로 해석하는 것입니다. 영어 어순대로 읽는 습관을 들여야 속도가 빨라집니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[3]}
</div>

## 수능 영어의 특징

수능 영어는 절대평가입니다. 90점 이상이면 1등급입니다. 하지만 매년 1등급 비율은 5-10%에 불과합니다. 빈칸 추론, 순서 배열, 문장 삽입 등 고난도 문제에서 차이가 납니다.

독해 속도와 정확도가 핵심입니다. 지문을 빠르게 읽고 핵심을 파악하는 훈련이 필요합니다. 모든 문장을 꼼꼼히 해석하기보다 글의 구조와 논리 흐름을 파악하는 것이 중요합니다.

듣기 평가도 17문항으로 비중이 큽니다. 듣기는 꾸준한 연습으로 실력을 올릴 수 있는 영역이므로, 매일 조금씩 듣기 연습을 하는 것이 좋습니다.

EBS 연계율도 중요합니다. 수능특강, 수능완성 교재를 꼼꼼히 학습하면 유리합니다. 연계 지문이 변형되어 출제되므로 핵심 내용과 구조를 파악해두어야 합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[4]}
</div>

## 효과적인 학습 방법

영어 성적을 올리기 위한 효과적인 학습 방법을 소개합니다.

어휘 학습은 매일 꾸준히 해야 합니다. 하루에 30-50개씩 외우고, 주기적으로 복습합니다. 단어장을 만들어 자투리 시간에 보는 습관을 들이면 좋습니다.

문법 학습은 개념 정리 후 문제 풀이로 확인합니다. 문법책 한 권을 정해 반복해서 보면 효과적입니다. 틀린 문제는 왜 틀렸는지 분석해야 합니다.

독해 학습은 매일 2-3지문씩 꾸준히 읽는 것이 중요합니다. 처음에는 시간에 구애받지 말고 정확하게 읽는 연습을 하고, 점차 속도를 높여갑니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[5]}
</div>

## 학원과 과외의 차이

학원에서는 많은 학생을 한꺼번에 가르치다 보니 개인별 약점을 보완하기 어렵습니다. 1:1 과외는 학생의 현재 수준에서 출발하여 약한 부분을 집중적으로 보강합니다.

어휘가 부족한 학생, 문법이 약한 학생, 독해 속도가 느린 학생 각각 다른 접근이 필요합니다. 학원에서는 이런 개인차를 반영하기 어렵습니다.

또한 과외에서는 질문을 자유롭게 할 수 있습니다. 부끄러워서 질문하지 못하는 학생도 1:1 상황에서는 편하게 물어볼 수 있습니다.

학생의 학습 스타일에 맞춘 지도도 가능합니다. 시각적 학습을 선호하는 학생, 반복이 필요한 학생, 빠르게 진도를 나가야 하는 학생 등에게 맞춤 지도가 가능합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[6]}
</div>

## 학년별 학습 전략

고1은 영어 기초를 점검하고, 고등 영어에 적응하는 시기입니다. 문법의 기본기를 다지고, 어휘력을 꾸준히 늘려야 합니다. 특히 문장 구조를 파악하는 능력을 키워야 합니다.

고2는 본격적인 수능 준비 시작입니다. 독해 유형을 익히고, EBS 교재를 시작합니다. 빈칸, 순서, 삽입 등 고난도 유형에 대한 접근법을 배웁니다.

고3은 실전 훈련 시기입니다. 모의고사 분석과 약점 보완에 집중합니다. 시간 관리 연습도 중요합니다. 70분 안에 45문제를 실수 없이 풀 수 있도록 연습합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[7]}
</div>

## 유형별 학습 포인트

수능 영어의 주요 유형별 학습 포인트를 안내합니다.

빈칸 추론 문제는 논리적 사고가 필요합니다. 빈칸 앞뒤의 문맥을 파악하고, 글 전체의 흐름을 이해해야 합니다.

순서 배열 문제는 연결어와 지시어에 주목해야 합니다. 문장 간의 논리적 연결고리를 찾는 연습이 필요합니다.

문장 삽입 문제는 주어진 문장의 역할을 파악해야 합니다. 예시인지, 부연인지, 반박인지에 따라 들어갈 위치가 결정됩니다.

요약 문제는 글의 핵심 내용을 한 문장으로 정리할 수 있어야 합니다. 주제문과 supporting details를 구분하는 능력이 필요합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[8]}
</div>

## 수업료 안내

{location} 지역 고등학교 영어 과외 수업료를 안내합니다.

**고1-2**는 주1회 25만원 - 36만원, 주2회 33만원 - 53만원 선입니다.

**고3**은 주1회 28만원 - 40만원, 주2회 37만원 - 59만원이 일반적입니다.

수업료는 학생의 현재 수준, 목표, 수업 강도에 따라 달라질 수 있습니다. 정확한 금액은 상담을 통해 안내드립니다.

첫 수업은 무료 체험으로 진행할 수 있습니다. 학생과 선생님의 궁합을 확인하고 결정하시면 됩니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[9]}
</div>

## 수업 진행 방식

수업은 다음과 같이 진행됩니다.

첫 수업에서는 학생의 현재 실력을 진단합니다. 어휘 수준, 문법 이해도, 독해 속도를 파악합니다. 이를 바탕으로 맞춤 커리큘럼을 설계합니다.

매 수업은 지난 시간 복습으로 시작합니다. 단어 테스트, 숙제 검사, 오답 분석을 통해 이해도를 확인합니다.

시험 기간에는 시험 대비 수업으로 전환합니다. 교과서 본문 분석, 예상 문제 풀이, 서술형 대비를 집중적으로 합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[10]}
</div>

{{{{< cta-dual type="final" >}}}}

## 자주 묻는 질문

**Q. 영어 기초가 많이 부족한데 따라갈 수 있을까요?**

기초 문법과 필수 어휘부터 다시 시작합니다. 학생 수준에 맞춰 차근차근 진행합니다.

**Q. 단어를 외워도 자꾸 까먹어요. 어떻게 해야 하나요?**

반복 학습이 핵심입니다. 여러 번 반복해서 보고, 문장 속에서 단어를 익히는 방법을 알려드립니다.

**Q. 독해가 너무 느려요. 시간 안에 못 풀어요.**

속독 훈련과 함께 지문 구조 파악 방법을 가르칩니다. 꾸준히 연습하면 속도가 빨라집니다.

**Q. 내신 시험 대비는 어떻게 하나요?**

시험 2-3주 전부터 교과서 본문 분석과 예상 문제 풀이로 집중 대비합니다.

**Q. 수업 시간과 장소는 어떻게 되나요?**

학생과 협의하여 결정합니다. 방문 수업, 카페 수업, 온라인 수업 모두 가능합니다.

**Q. 교재는 어떤 것을 사용하나요?**

학생의 수준과 목표에 맞는 교재를 추천해드립니다. 수능 대비 시에는 EBS 교재를 함께 활용합니다.

## 마무리

{location_short} 지역에서 고등학교 영어 때문에 고민하고 계신다면, 지금이 시작할 때입니다.

영어는 꾸준함이 필요한 과목입니다. 하루아침에 실력이 오르지 않지만, 올바른 방법으로 꾸준히 하면 반드시 결과가 나옵니다.

{location_short} 학생 여러분, {ending}

상담은 무료입니다. 부담 없이 연락 주세요.
'''
    return content


def create_middle_math_content(city_name, gu_name, dong_name, schools_mid, file_index):
    """중등 수학 콘텐츠 생성 (250-300줄)"""
    school_str = "·".join(schools_mid[:3])
    idx = file_index + 25

    intro = get_pool_item(INTRO_MID_MATH, idx)
    h2_why = get_pool_item(H2_MID_MATH_WHY, idx + 3)

    boxes = [get_pool_item(IVORY_BOX_POOL, idx + i * 13) for i in range(12)]
    ending = get_pool_item(ENDING_POOL, idx + 31)
    image = get_pool_item(IMAGE_POOL, idx + 41)

    if gu_name:
        location = f"{city_name} {gu_name} {dong_name}"
        location_short = f"{gu_name} {dong_name}"
    else:
        location = f"{city_name} {dong_name}"
        location_short = dong_name

    content = f'''---
title: "{location} 중등 수학과외 | {school_str} 내신·선행 대비"
date: 2025-01-15
categories:
  - 중등교육
regions:
  - 경기도
  - {city_name}
cities:
  - {gu_name if gu_name else city_name}
description: "{location} 중학생 수학과외 전문. {schools_mid[0]} 내신 완벽 대비. 기초부터 심화까지 체계적 1:1 지도."
tags:
  - {city_name}
  - {gu_name if gu_name else dong_name}
  - {dong_name}
  - 중등수학
  - 수학과외
  - 내신관리
  - 선행학습
  - {schools_mid[0]}
featured_image: "https://images.unsplash.com/{image}?w=1200&h=630&fit=crop"
---
{intro}

{dong_name} 지역에서 중학교 수학 때문에 고민하고 계신가요? 중학교 수학은 고등학교 수학의 기초입니다. 이 시기에 개념을 확실히 잡아야 고등학교에서 수월합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[0]}
</div>

## {h2_why}

중학교 수학은 초등학교와 질적으로 다릅니다. 문자를 사용한 식이 등장하고, 추상적인 개념이 늘어납니다. 문자와 식, 함수, 도형 등 핵심 개념이 모두 이 시기에 시작됩니다.

{dong_name} 지역 {schools_mid[0]} 학생들은 내신 관리와 함께 고등학교 진학을 준비해야 합니다. 중학교 때 기초를 확실히 잡아야 고등학교에서 힘들지 않습니다.

특히 중학교 수학에서 배우는 개념들은 고등학교로 직접 연결됩니다. 일차방정식이 이차방정식으로, 일차함수가 이차함수로 이어집니다. 기초가 부실하면 고등학교에서 더 힘들어집니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[1]}
</div>

## 내신 수학 대비

{schools_mid[0]} 수학 시험은 교과서 기본 문제부터 심화 문제까지 골고루 출제됩니다. 기본 개념을 정확히 이해하고, 다양한 유형의 문제를 풀어봐야 합니다.

서술형 문제 비중이 높아지고 있습니다. 풀이 과정을 논리적으로 작성하는 연습이 필요합니다. 답만 맞으면 된다는 생각을 버리고, 풀이 과정까지 꼼꼼히 써야 합니다.

내신 시험에서는 학교 선생님의 출제 스타일을 파악하는 것이 중요합니다. 수업 시간에 강조한 내용, 프린트로 나눠준 문제를 잘 정리해두면 시험 대비에 도움이 됩니다.

{schools_mid[1]}과 {schools_mid[2]}도 각각의 출제 특성이 있습니다. 학교별로 선호하는 문제 유형이 다르기 때문에 학교별 맞춤 대비가 필요합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[2]}
</div>

## 자주 하는 실수와 해결법

중학생들이 수학에서 자주 하는 실수가 있습니다. 이런 실수를 인식하고 고치는 것이 성적 향상의 지름길입니다.

첫째, 연산 실수입니다. 부호 실수, 약분 실수 등이 빈번합니다. 검산 습관을 들이고, 자주 하는 실수 유형을 파악해야 합니다.

둘째, 문제를 제대로 읽지 않는 것입니다. 무엇을 구하는 문제인지 확인하지 않고 풀다가 엉뚱한 답을 쓰는 경우가 많습니다.

셋째, 개념을 대충 넘어가는 것입니다. 문제만 많이 풀면 된다고 생각하지만, 개념이 불완전하면 응용 문제에서 막힙니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[3]}
</div>

## 1:1 과외의 장점

학원에서는 많은 학생을 한꺼번에 가르치다 보니 개인별 약점을 보완하기 어렵습니다. 1:1 과외는 학생의 현재 수준에서 출발하여 약한 부분을 집중적으로 보강합니다.

연산이 느린 학생, 문제 이해가 어려운 학생, 응용력이 부족한 학생 각각 다른 접근이 필요합니다. 맞춤 수업이 효과적인 이유입니다.

또한 과외에서는 질문을 자유롭게 할 수 있습니다. 수업 시간에 물어보기 부끄러웠던 것도 1:1 상황에서는 편하게 질문할 수 있습니다.

학습 습관 형성에도 도움이 됩니다. 숙제 검사, 오답 분석, 복습 점검을 통해 스스로 공부하는 습관을 잡아줍니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[4]}
</div>

## 효과적인 학습 방법

수학 성적을 올리기 위한 효과적인 학습 방법을 소개합니다.

개념 학습 단계에서는 교과서를 꼼꼼히 읽고, 각 개념이 왜 필요한지 이해해야 합니다. 공식을 외우기보다 공식이 어떻게 나왔는지 알면 기억에 오래 남습니다.

문제 풀이 단계에서는 난이도를 점진적으로 높여가야 합니다. 기본 문제로 개념을 확인하고, 유형 문제로 적용력을 키웁니다.

복습 단계에서는 틀린 문제를 중심으로 해야 합니다. 오답노트를 만들어 주기적으로 확인하면 같은 실수를 반복하지 않게 됩니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[5]}
</div>

## 학년별 학습 전략

중1은 수학의 기초를 다지는 시기입니다. 정수와 유리수, 문자와 식, 방정식을 확실히 익혀야 합니다. 특히 음수 개념과 문자 사용에 적응하는 것이 중요합니다.

중2는 함수가 처음 등장하는 중요한 시기입니다. 일차함수 개념을 확실히 잡아야 합니다. 연립방정식, 부등식도 이 시기에 배웁니다.

중3은 고등학교 진학을 앞둔 시기입니다. 이차방정식, 이차함수, 피타고라스 정리 등 핵심 개념을 정리합니다. 이 내용들은 고등학교에서 바로 심화됩니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[6]}
</div>

## 단원별 학습 포인트

중학교 수학의 주요 단원별 학습 포인트를 안내합니다.

수와 연산 단원에서는 정수, 유리수의 사칙연산을 정확하게 할 수 있어야 합니다. 특히 음수가 포함된 계산에서 실수하지 않도록 연습이 필요합니다.

문자와 식 단원에서는 문자가 수를 대신한다는 개념을 이해해야 합니다. 다항식의 계산, 인수분해까지 자연스럽게 연결됩니다.

방정식과 부등식 단원에서는 등식의 성질을 이용해 미지수를 구하는 과정을 익힙니다. 연립방정식, 이차방정식까지 단계적으로 학습합니다.

함수 단원에서는 함수의 개념과 그래프를 이해하는 것이 핵심입니다. 일차함수에서 이차함수로 확장됩니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[7]}
</div>

## 선행학습에 대하여

선행학습에 대한 질문을 많이 받습니다. 선행이 필요한 경우도 있지만, 무조건 선행이 좋은 것은 아닙니다.

현행 학습이 충실하지 않은 상태에서 선행을 하면 오히려 역효과가 날 수 있습니다. 기초가 부실한 상태에서 어려운 내용을 배우면 둘 다 제대로 익히지 못합니다.

선행을 하더라도 적정 수준이 있습니다. 한 학기에서 한 학년 정도의 선행이 적당합니다. 너무 앞서 나가면 배운 내용을 잊어버리기 쉽습니다.

가장 중요한 것은 현재 배우는 내용을 완벽히 이해하는 것입니다. 현행이 확실하면 선행도 자연스럽게 따라옵니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[8]}
</div>

## 수업료 안내

{location} 지역 중학교 수학 과외 수업료를 안내합니다.

**중학생**은 주1회 22만원 - 32만원, 주2회 29만원 - 47만원 선입니다.

수업료는 학생의 현재 수준, 목표, 수업 강도에 따라 달라질 수 있습니다. 정확한 금액은 상담을 통해 안내드립니다.

첫 수업은 무료 체험으로 진행할 수 있습니다. 학생과 선생님의 궁합을 확인하고 결정하시면 됩니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[9]}
</div>

## 수업 진행 방식

수업은 다음과 같이 진행됩니다.

첫 수업에서는 학생의 현재 실력을 진단합니다. 어떤 단원이 취약한지, 어떤 유형에서 실수가 많은지 파악합니다. 이를 바탕으로 맞춤 커리큘럼을 설계합니다.

매 수업은 지난 시간 복습으로 시작합니다. 숙제 검사와 오답 분석을 통해 이해도를 확인합니다. 새로운 내용을 배운 후에는 확인 문제를 풀어봅니다.

시험 기간에는 시험 대비 수업으로 전환합니다. 시험 범위에 맞춰 핵심 개념을 정리하고, 예상 문제를 풀어봅니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[10]}
</div>

{{{{< cta-dual type="final" >}}}}

## 자주 묻는 질문

**Q. 수학 기초가 많이 부족한데 따라갈 수 있을까요?**

초등 연산부터 필요하면 다시 시작합니다. 기초를 확실히 다진 후 중학교 내용을 진행합니다.

**Q. 선행학습은 꼭 해야 하나요?**

선행보다 현행이 우선입니다. 현재 학년 내용이 확실하면 선행을 진행합니다.

**Q. 내신 시험 대비는 어떻게 하나요?**

시험 2-3주 전부터 학교 기출문제와 예상 문제 풀이로 집중 대비합니다.

**Q. 수업 시간과 장소는 어떻게 되나요?**

학생과 협의하여 결정합니다. 방문 수업, 카페 수업, 온라인 수업 모두 가능합니다.

**Q. 교재는 어떤 것을 사용하나요?**

학생의 수준과 목표에 맞는 교재를 추천해드립니다. 학교 교과서, 기본서, 유형서 등을 조합하여 사용합니다.

## 마무리

{location_short} 지역에서 중학교 수학 때문에 고민하고 계신다면, 지금이 시작할 때입니다.

중학교 수학은 고등학교의 기초입니다. 이 시기에 기초를 확실히 잡아야 나중에 힘들지 않습니다.

{location_short} 학생 여러분, {ending}

상담은 무료입니다. 부담 없이 연락 주세요.
'''
    return content


def create_middle_english_content(city_name, gu_name, dong_name, schools_mid, file_index):
    """중등 영어 콘텐츠 생성 (250-300줄)"""
    school_str = "·".join(schools_mid[:3])
    idx = file_index + 75

    intro = get_pool_item(INTRO_MID_ENG, idx)
    h2_why = get_pool_item(H2_MID_ENG_WHY, idx + 3)

    boxes = [get_pool_item(IVORY_BOX_POOL, idx + i * 17) for i in range(12)]
    ending = get_pool_item(ENDING_POOL, idx + 43)
    image = get_pool_item(IMAGE_POOL, idx + 53)

    if gu_name:
        location = f"{city_name} {gu_name} {dong_name}"
        location_short = f"{gu_name} {dong_name}"
    else:
        location = f"{city_name} {dong_name}"
        location_short = dong_name

    content = f'''---
title: "{location} 중등 영어과외 | {school_str} 내신·선행 대비"
date: 2025-01-15
categories:
  - 중등교육
regions:
  - 경기도
  - {city_name}
cities:
  - {gu_name if gu_name else city_name}
description: "{location} 중학생 영어과외 전문. {schools_mid[0]} 내신 완벽 대비. 문법부터 독해까지 체계적 1:1 지도."
tags:
  - {city_name}
  - {gu_name if gu_name else dong_name}
  - {dong_name}
  - 중등영어
  - 영어과외
  - 내신관리
  - 선행학습
  - {schools_mid[0]}
featured_image: "https://images.unsplash.com/{image}?w=1200&h=630&fit=crop"
---
{intro}

{dong_name} 지역에서 중학교 영어 때문에 고민하고 계신가요? 중학교 영어는 고등학교 영어의 기초입니다. 이 시기에 문법과 어휘의 기본기를 다져야 고등학교에서 수월합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[0]}
</div>

## {h2_why}

중학교 영어는 초등학교와 질적으로 다릅니다. 문법이 본격적으로 시작되고, 읽어야 할 지문의 길이가 늘어납니다. 시제, 문장 구조, 기본 문법이 모두 이 시기에 정립됩니다.

{dong_name} 지역 {schools_mid[0]} 학생들은 내신 관리와 함께 고등학교 영어를 준비해야 합니다. 중학교 때 기초를 확실히 잡아야 고등학교에서 수월합니다.

특히 중학교 영어에서 배우는 문법은 고등학교로 직접 연결됩니다. 5형식 문장, 시제, 조동사, 수동태 등을 완벽히 이해해야 합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[1]}
</div>

## 내신 영어 대비

{schools_mid[0]} 영어 시험은 교과서 본문이 중심입니다. 단어, 숙어, 문법 포인트를 정리하고, 본문 내용을 완벽히 이해해야 합니다.

서술형 문제 비중이 높아지고 있습니다. 영작 연습과 함께 문법 개념을 정확히 알아야 합니다. 빈칸 채우기, 문장 완성, 짧은 영작 등 다양한 유형에 대비해야 합니다.

내신 시험에서는 교과서뿐 아니라 부교재와 프린트 내용도 출제됩니다. 수업 시간에 선생님이 강조한 표현을 꼼꼼히 정리해야 합니다.

{schools_mid[1]}과 {schools_mid[2]}도 각각의 출제 특성이 있습니다. 학교별로 선호하는 문제 유형이 다르기 때문에 학교별 맞춤 대비가 필요합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[2]}
</div>

## 자주 하는 실수와 해결법

중학생들이 영어에서 자주 하는 실수가 있습니다. 이런 실수를 인식하고 고치는 것이 성적 향상의 지름길입니다.

첫째, 단어를 철자까지 정확히 외우지 않는 것입니다. 뜻은 알지만 철자를 틀리면 서술형에서 감점됩니다.

둘째, 문법 규칙만 외우고 적용하지 못하는 것입니다. 문법 문제를 풀 때뿐 아니라 독해와 영작에서도 활용해야 합니다.

셋째, 독해할 때 모르는 단어에 집착하는 것입니다. 문맥으로 의미를 유추하는 연습이 필요합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[3]}
</div>

## 1:1 과외의 장점

학원에서는 많은 학생을 한꺼번에 가르치다 보니 개인별 약점을 보완하기 어렵습니다. 1:1 과외는 학생의 현재 수준에서 출발하여 약한 부분을 집중적으로 보강합니다.

문법이 약한 학생, 독해가 느린 학생, 어휘력이 부족한 학생 각각 다른 접근이 필요합니다. 맞춤 수업이 효과적인 이유입니다.

또한 과외에서는 질문을 자유롭게 할 수 있습니다. 수업 시간에 물어보기 부끄러웠던 것도 1:1 상황에서는 편하게 질문할 수 있습니다.

학습 습관 형성에도 도움이 됩니다. 단어 암기, 숙제 검사, 복습 점검을 통해 스스로 공부하는 습관을 잡아줍니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[4]}
</div>

## 효과적인 학습 방법

영어 성적을 올리기 위한 효과적인 학습 방법을 소개합니다.

어휘 학습은 매일 꾸준히 해야 합니다. 하루에 20-30개씩 외우고, 주기적으로 복습합니다. 단어장을 만들어 자투리 시간에 보는 습관을 들이면 좋습니다.

문법 학습은 개념 정리 후 문제 풀이로 확인합니다. 문법책 한 권을 정해 반복해서 보면 효과적입니다.

독해 학습은 교과서 본문을 완벽히 이해하는 것부터 시작합니다. 모르는 문장이 없을 때까지 반복해서 읽습니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[5]}
</div>

## 학년별 학습 전략

중1은 영어의 기초를 다지는 시기입니다. 기본 문법을 정리하고, 어휘력을 꾸준히 늘려가야 합니다. 특히 품사의 개념과 문장의 기본 구조를 익히는 것이 중요합니다.

중2는 문법이 어려워지는 시기입니다. 시제, 조동사, 수동태 등 핵심 문법을 확실히 익혀야 합니다. 문법이 복잡해지는 만큼 체계적인 정리가 필요합니다.

중3은 고등학교 진학을 앞둔 중요한 시기입니다. 중학교 전체 문법을 정리하고, 고등 영어를 준비합니다. 독해 지문의 길이와 난이도를 점차 높여갑니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[6]}
</div>

## 문법별 학습 포인트

중학교 영어의 주요 문법별 학습 포인트를 안내합니다.

품사와 문장 성분은 영어의 기초입니다. 명사, 동사, 형용사, 부사의 역할을 이해하고, 주어, 동사, 목적어, 보어를 구분할 수 있어야 합니다.

시제는 현재, 과거, 미래, 진행, 완료까지 단계적으로 학습합니다. 각 시제가 언제 쓰이는지 정확히 알아야 합니다.

문장의 종류도 중요합니다. 평서문, 의문문, 명령문, 감탄문의 구조를 익히고, 부정문 만들기를 연습합니다.

수동태와 관계대명사는 고등학교까지 이어지는 중요한 문법입니다. 확실히 익혀두어야 합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[7]}
</div>

## 선행학습에 대하여

선행학습에 대한 질문을 많이 받습니다. 영어는 수학과 달리 선행의 개념이 조금 다릅니다.

영어에서 선행이란 주로 문법 선행과 어휘 선행을 의미합니다. 고등학교 문법을 미리 배우거나, 수능 필수 어휘를 미리 익히는 것입니다.

하지만 현행 학습이 충실하지 않은 상태에서 선행을 하면 효과가 떨어집니다. 기초가 부실하면 어려운 내용이 더 어렵게 느껴집니다.

가장 중요한 것은 현재 배우는 내용을 완벽히 이해하는 것입니다. 현행이 확실하면 선행도 자연스럽게 따라옵니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[8]}
</div>

## 수업료 안내

{location} 지역 중학교 영어 과외 수업료를 안내합니다.

**중학생**은 주1회 22만원 - 32만원, 주2회 29만원 - 47만원 선입니다.

수업료는 학생의 현재 수준, 목표, 수업 강도에 따라 달라질 수 있습니다. 정확한 금액은 상담을 통해 안내드립니다.

첫 수업은 무료 체험으로 진행할 수 있습니다. 학생과 선생님의 궁합을 확인하고 결정하시면 됩니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[9]}
</div>

## 수업 진행 방식

수업은 다음과 같이 진행됩니다.

첫 수업에서는 학생의 현재 실력을 진단합니다. 어휘 수준, 문법 이해도, 독해 능력을 파악합니다. 이를 바탕으로 맞춤 커리큘럼을 설계합니다.

매 수업은 지난 시간 복습으로 시작합니다. 단어 테스트, 숙제 검사, 오답 분석을 통해 이해도를 확인합니다.

시험 기간에는 시험 대비 수업으로 전환합니다. 교과서 본문 분석, 예상 문제 풀이, 서술형 대비를 집중적으로 합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[10]}
</div>

{{{{< cta-dual type="final" >}}}}

## 자주 묻는 질문

**Q. 영어 기초가 많이 부족한데 따라갈 수 있을까요?**

파닉스부터 필요하면 다시 시작합니다. 기초를 확실히 다진 후 중학교 내용을 진행합니다.

**Q. 문법이 너무 어려워요. 어떻게 해야 하나요?**

문법은 이해가 중요합니다. 암기보다 원리를 설명하고, 다양한 예문으로 연습합니다.

**Q. 내신 시험 대비는 어떻게 하나요?**

시험 2-3주 전부터 교과서 본문 분석과 예상 문제 풀이로 집중 대비합니다.

**Q. 수업 시간과 장소는 어떻게 되나요?**

학생과 협의하여 결정합니다. 방문 수업, 카페 수업, 온라인 수업 모두 가능합니다.

**Q. 교재는 어떤 것을 사용하나요?**

학생의 수준과 목표에 맞는 교재를 추천해드립니다. 학교 교과서, 문법책, 단어장 등을 조합하여 사용합니다.

## 마무리

{location_short} 지역에서 중학교 영어 때문에 고민하고 계신다면, 지금이 시작할 때입니다.

중학교 영어는 고등학교의 기초입니다. 이 시기에 기초를 확실히 잡아야 나중에 힘들지 않습니다.

{location_short} 학생 여러분, {ending}

상담은 무료입니다. 부담 없이 연락 주세요.
'''
    return content


def main():
    """메인 실행 함수"""
    base_path = "/home/user/edu-guide/content/gyeonggi"
    file_index = 0
    total_files = 0

    print("=" * 60)
    print("경기도 콘텐츠 확장 재생성 (250-300줄)")
    print("=" * 60)

    for city_dir in sorted(os.listdir(base_path)):
        city_path = os.path.join(base_path, city_dir)
        if not os.path.isdir(city_path) or city_dir.startswith("_"):
            continue

        city_info = CITY_INFO.get(city_dir, {"name": city_dir, "gu_map": {}})
        city_name = city_info["name"]
        gu_map = city_info.get("gu_map", {})
        schools_high, schools_mid = CITY_SCHOOLS.get(city_dir, (["지역고"], ["지역중"]))

        print(f"\n{city_name} 처리 중...")
        city_files = 0

        for item in sorted(os.listdir(city_path)):
            item_path = os.path.join(city_path, item)
            if not os.path.isdir(item_path) or item.startswith("_"):
                continue

            sub_items = [d for d in os.listdir(item_path) if os.path.isdir(os.path.join(item_path, d)) and not d.startswith("_")]

            if sub_items:
                gu_name = gu_map.get(item, item)
                for dong_dir in sorted(sub_items):
                    dong_path = os.path.join(item_path, dong_dir)
                    dong_name = get_dong_name_ko(dong_path)

                    with open(os.path.join(dong_path, "high-math.md"), "w", encoding="utf-8") as f:
                        f.write(create_high_math_content(city_name, gu_name, dong_name, schools_high, file_index))
                    with open(os.path.join(dong_path, "high-english.md"), "w", encoding="utf-8") as f:
                        f.write(create_high_english_content(city_name, gu_name, dong_name, schools_high, file_index))
                    with open(os.path.join(dong_path, "middle-math.md"), "w", encoding="utf-8") as f:
                        f.write(create_middle_math_content(city_name, gu_name, dong_name, schools_mid, file_index))
                    with open(os.path.join(dong_path, "middle-english.md"), "w", encoding="utf-8") as f:
                        f.write(create_middle_english_content(city_name, gu_name, dong_name, schools_mid, file_index))

                    file_index += 1
                    total_files += 4
                    city_files += 4
            else:
                dong_path = item_path
                dong_name = get_dong_name_ko(dong_path)

                with open(os.path.join(dong_path, "high-math.md"), "w", encoding="utf-8") as f:
                    f.write(create_high_math_content(city_name, None, dong_name, schools_high, file_index))
                with open(os.path.join(dong_path, "high-english.md"), "w", encoding="utf-8") as f:
                    f.write(create_high_english_content(city_name, None, dong_name, schools_high, file_index))
                with open(os.path.join(dong_path, "middle-math.md"), "w", encoding="utf-8") as f:
                    f.write(create_middle_math_content(city_name, None, dong_name, schools_mid, file_index))
                with open(os.path.join(dong_path, "middle-english.md"), "w", encoding="utf-8") as f:
                    f.write(create_middle_english_content(city_name, None, dong_name, schools_mid, file_index))

                file_index += 1
                total_files += 4
                city_files += 4

        print(f"  {city_name}: {city_files}개")

    print(f"\n{'=' * 60}")
    print(f"총 {total_files}개 파일 생성 완료")
    print("=" * 60)


if __name__ == "__main__":
    main()
