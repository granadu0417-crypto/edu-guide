#!/usr/bin/env python3
"""성남시 동단위 콘텐츠 생성 스크립트"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from create_suwon_content import (
    INTRO_POOL_HIGH_MATH, INTRO_POOL_HIGH_ENG,
    INTRO_POOL_MID_MATH, INTRO_POOL_MID_ENG,
    BOX_POOL, ENDING_POOL, IMAGE_POOL, get_expression
)

# 성남시 3개 구별 행정동 및 학교 정보
SEONGNAM_DATA = {
    "sujeong": {  # 수정구
        "name_ko": "수정구",
        "dongs": {
            "sinheung1": {"name": "신흥1동", "schools": ["성남고", "성남여고", "복정고"]},
            "sinheung2": {"name": "신흥2동", "schools": ["성남고", "태원고", "성남여고"]},
            "sinheung3": {"name": "신흥3동", "schools": ["태원고", "성남고", "복정고"]},
            "taepyeong1": {"name": "태평1동", "schools": ["태원고", "성일고", "성남고"]},
            "taepyeong2": {"name": "태평2동", "schools": ["태원고", "성남여고", "성일고"]},
            "taepyeong3": {"name": "태평3동", "schools": ["성일고", "태원고", "성남고"]},
            "taepyeong4": {"name": "태평4동", "schools": ["성일고", "성남여고", "태원고"]},
            "sujin1": {"name": "수진1동", "schools": ["성남고", "복정고", "태원고"]},
            "sujin2": {"name": "수진2동", "schools": ["복정고", "성남고", "성일고"]},
            "dandae": {"name": "단대동", "schools": ["단대부고", "성남고", "태원고"]},
            "sanseong": {"name": "산성동", "schools": ["성남고", "성일고", "태원고"]},
            "yangji": {"name": "양지동", "schools": ["성남고", "복정고", "성남여고"]},
            "bokjeong": {"name": "복정동", "schools": ["복정고", "성남고", "태원고"]},
            "wirye": {"name": "위례동", "schools": ["위례고", "복정고", "성남고"]},
        }
    },
    "jungwon": {  # 중원구
        "name_ko": "중원구",
        "dongs": {
            "seongnam": {"name": "성남동", "schools": ["성남고", "성일고", "동광고"]},
            "jungang": {"name": "중앙동", "schools": ["성일고", "성남고", "성남여고"]},
            "geumgwang1": {"name": "금광1동", "schools": ["동광고", "성일고", "성남고"]},
            "geumgwang2": {"name": "금광2동", "schools": ["성일고", "동광고", "성남여고"]},
            "eunhaeng1": {"name": "은행1동", "schools": ["성남고", "동광고", "성일고"]},
            "eunhaeng2": {"name": "은행2동", "schools": ["동광고", "성남고", "성일고"]},
            "sangdaewon1": {"name": "상대원1동", "schools": ["성일고", "성남고", "동광고"]},
            "sangdaewon2": {"name": "상대원2동", "schools": ["성남고", "성일고", "성남여고"]},
            "sangdaewon3": {"name": "상대원3동", "schools": ["동광고", "성일고", "성남고"]},
            "hadaewon": {"name": "하대원동", "schools": ["성남고", "성일고", "동광고"]},
            "dochon": {"name": "도촌동", "schools": ["성일고", "성남고", "동광고"]},
        }
    },
    "bundang": {  # 분당구
        "name_ko": "분당구",
        "dongs": {
            "seohyeon1": {"name": "서현1동", "schools": ["성남외고", "분당고", "서현고"]},
            "seohyeon2": {"name": "서현2동", "schools": ["서현고", "성남외고", "분당고"]},
            "imae1": {"name": "이매1동", "schools": ["이매고", "분당고", "성남외고"]},
            "imae2": {"name": "이매2동", "schools": ["이매고", "분당고", "서현고"]},
            "yatap1": {"name": "야탑1동", "schools": ["야탑고", "분당영덕여고", "분당고"]},
            "yatap2": {"name": "야탑2동", "schools": ["야탑고", "분당고", "성남외고"]},
            "yatap3": {"name": "야탑3동", "schools": ["야탑고", "분당영덕여고", "분당고"]},
            "sunae1": {"name": "수내1동", "schools": ["수내고", "분당고", "성남외고"]},
            "sunae2": {"name": "수내2동", "schools": ["수내고", "분당고", "서현고"]},
            "sunae3": {"name": "수내3동", "schools": ["수내고", "성남외고", "분당고"]},
            "jeongja1": {"name": "정자1동", "schools": ["정자고", "분당고", "성남외고"]},
            "jeongja2": {"name": "정자2동", "schools": ["정자고", "수내고", "분당고"]},
            "jeongja3": {"name": "정자3동", "schools": ["정자고", "성남외고", "분당고"]},
            "gumi1": {"name": "구미1동", "schools": ["분당고", "성남외고", "분당영덕여고"]},
            "gumi2": {"name": "구미2동", "schools": ["분당고", "구미고", "성남외고"]},
            "geumgok": {"name": "금곡동", "schools": ["분당고", "분당영덕여고", "성남외고"]},
            "unjung1": {"name": "운중동", "schools": ["늘푸른고", "분당고", "성남외고"]},
            "baekhyeon": {"name": "백현동", "schools": ["성남외고", "판교고", "분당고"]},
            "pangyo": {"name": "판교동", "schools": ["판교고", "성남외고", "분당고"]},
            "sampyeong": {"name": "삼평동", "schools": ["판교고", "늘푸른고", "성남외고"]},
        }
    }
}

def create_high_math_content(city_name, gu_name, dong_name, dong_name_en, schools, file_index):
    """고등 수학 콘텐츠 생성"""
    school_str = "·".join(schools[:3])
    intro = get_expression(INTRO_POOL_HIGH_MATH, file_index + 50)  # 수원과 다른 인덱스
    boxes = [get_expression(BOX_POOL, file_index + i * 7 + 3) for i in range(7)]
    ending = get_expression(ENDING_POOL, file_index + 5)
    image = get_expression(IMAGE_POOL, file_index + 2)

    content = f'''---
aliases:
  - /high/seongnam-{dong_name_en}-high-math/
title: "성남시 {gu_name} {dong_name} 고등 수학과외 | {school_str} 내신·수능 대비"
date: 2025-01-15
categories:
  - 고등교육
regions:
  - 경기도
  - 성남시
cities:
  - {gu_name}
description: "성남시 {gu_name} {dong_name} 고등학생 수학과외 전문. {schools[0]} 내신과 수능 동시 대비. 개념부터 킬러문항까지 체계적 1:1 지도."
tags:
  - 성남시
  - {gu_name}
  - {dong_name}
  - 고등수학
  - 수학과외
  - 내신관리
  - 수능대비
  - {schools[0]}
featured_image: "https://images.unsplash.com/{image}?w=1200&h=630&fit=crop"
---
{intro}

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[0]}
</div>

## 고등학교 수학, 왜 어려워질까요?

고등학교 수학은 중학교와 차원이 다릅니다. 추상적인 개념이 많아지고, 함수, 미적분, 확률과 통계 등 새로운 영역이 등장합니다. 중학교 때 수학을 잘했던 학생도 고등학교에서 어려움을 겪는 경우가 많습니다.

{dong_name} 지역 {schools[0]} 학생들은 높은 내신 경쟁과 수능 준비를 동시에 해야 합니다. 학교 시험은 학교별 특성에 맞춰 대비해야 하고, 수능은 전국 단위 경쟁이므로 또 다른 전략이 필요합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[1]}
</div>

## {schools[0]} 내신 시험 분석

{schools[0]}은 내신 시험 난이도가 높습니다. 교과서 기본 문제는 물론, 심화 문제와 변형 문제가 많이 출제됩니다. 단순히 공식을 외워서는 좋은 점수를 받기 어렵고, 개념을 깊이 이해하고 다양한 유형에 적용할 수 있어야 합니다.

시험 시간 대비 문제 양이 많은 편이어서 시간 관리도 중요합니다. 평소 시간을 재고 문제를 푸는 연습을 해야 실전에서 당황하지 않습니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[2]}
</div>

## 수능 수학의 핵심

수능 수학은 내신과 출제 방식이 다릅니다. 킬러 문항이라 불리는 21번, 29번, 30번 문제는 여러 개념을 복합적으로 적용해야 풀 수 있습니다. 시간 압박 속에서 정확하게 문제를 푸는 능력이 필요합니다.

수능에서 1등급을 받으려면 킬러 문항 중 최소 1-2개는 맞혀야 합니다. 이를 위해서는 기본 개념이 완벽해야 하고, 다양한 심화 문제를 풀어본 경험이 있어야 합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[3]}
</div>

## 학원과 과외의 차이

학원에서는 많은 학생을 한꺼번에 가르치다 보니 개인별 약점을 보완하기 어렵습니다. 1:1 과외는 학생의 현재 수준에서 출발하여 약한 부분을 집중적으로 보강합니다.

질문하기 어려운 학생도 1:1 수업에서는 편하게 물어볼 수 있습니다. 이해될 때까지 설명을 듣고, 스스로 문제를 풀어보며 실력을 키울 수 있습니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[4]}
</div>

## 학년별 학습 전략

고1은 수학의 기초를 다시 점검하고, 고등 수학의 핵심인 함수 개념을 확실히 익혀야 합니다. 다항식, 방정식과 부등식, 도형의 방정식 등 수학(상), 수학(하) 내용을 탄탄히 해야 고2, 고3에서 수월합니다.

고2는 수학I, 수학II를 배우며 지수, 로그, 삼각함수, 미분과 적분을 익힙니다. 이 시기에 배우는 내용이 수능 수학의 핵심이므로 확실히 이해하고 넘어가야 합니다.

고3은 본격적인 수능 대비 시기입니다. 기출문제 분석, 모의고사 훈련, 약점 보완을 집중적으로 해야 합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[5]}
</div>

## 수업료 안내

**고1-2**는 주1회 25만원 - 36만원, 주2회 33만원 - 53만원 선입니다.

**고3**은 주1회 28만원 - 40만원, 주2회 37만원 - 59만원이 일반적입니다.

정확한 금액은 상담을 통해 안내드립니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[6]}
</div>

{{{{< cta-dual type="final" >}}}}

## 자주 묻는 질문

**Q. 내신과 수능 중 어떤 것을 먼저 준비해야 하나요?**

고1-2는 내신 위주로 공부하면서 수능 기초를 다지고, 고3은 내신과 수능을 병행합니다. 학생 상황에 따라 비중을 조절합니다.

**Q. 수학 기초가 많이 부족한데 따라갈 수 있을까요?**

중학교 내용부터 다시 점검하고 필요한 부분을 보강합니다. 기초를 확실히 다진 후 고등 내용을 진행합니다.

**Q. 킬러 문항은 어떻게 대비하나요?**

기본 개념을 완벽히 익힌 후, 고난도 문제 유형별 접근법을 체계적으로 훈련합니다.

**Q. 내신 시험 대비는 어떻게 하나요?**

시험 2-3주 전부터 학교 기출문제와 예상 문제 풀이로 집중 대비합니다.

## 마무리

{gu_name} {dong_name} 학생 여러분, {ending}
'''
    return content

def create_high_english_content(city_name, gu_name, dong_name, dong_name_en, schools, file_index):
    """고등 영어 콘텐츠 생성"""
    school_str = "·".join(schools[:3])
    intro = get_expression(INTRO_POOL_HIGH_ENG, file_index + 50)
    boxes = [get_expression(BOX_POOL, file_index + i * 5 + 7) for i in range(7)]
    ending = get_expression(ENDING_POOL, file_index + 6)
    image = get_expression(IMAGE_POOL, file_index + 3)

    content = f'''---
aliases:
  - /high/seongnam-{dong_name_en}-high-english/
title: "성남시 {gu_name} {dong_name} 고등 영어과외 | {school_str} 내신·수능 대비"
date: 2025-01-15
categories:
  - 고등교육
regions:
  - 경기도
  - 성남시
cities:
  - {gu_name}
description: "성남시 {gu_name} {dong_name} 고등학생 영어과외 전문. {schools[0]} 내신과 수능 동시 대비. 독해부터 문법까지 체계적 1:1 지도."
tags:
  - 성남시
  - {gu_name}
  - {dong_name}
  - 고등영어
  - 영어과외
  - 내신관리
  - 수능대비
  - {schools[0]}
featured_image: "https://images.unsplash.com/{image}?w=1200&h=630&fit=crop"
---
{intro}

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[0]}
</div>

## 고등학교 영어, 왜 어려워질까요?

고등학교 영어는 중학교와 차원이 다릅니다. 지문 길이가 길어지고, 어휘 수준이 높아지며, 복잡한 구문이 등장합니다. 중학교 때 영어를 잘했던 학생도 고등학교에서 어려움을 겪는 경우가 많습니다.

{dong_name} 지역 {schools[0]} 학생들은 높은 내신 경쟁과 수능 준비를 동시에 해야 합니다. 학교 시험은 학교별 특성에 맞춰 대비해야 하고, 수능은 전국 단위 경쟁이므로 또 다른 전략이 필요합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[1]}
</div>

## {schools[0]} 내신 시험 분석

{schools[0]}은 영어 내신 시험 난이도가 높습니다. 교과서 본문 암기는 기본이고, 변형 문제와 외부 지문이 출제되기도 합니다. 문법, 어휘, 독해를 균형 있게 준비해야 합니다.

시험 시간 대비 문제 양이 많은 편이어서 시간 관리도 중요합니다. 평소 시간을 재고 문제를 푸는 연습을 해야 실전에서 당황하지 않습니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[2]}
</div>

## 수능 영어의 핵심

수능 영어는 절대평가이지만 1등급을 받기는 쉽지 않습니다. 빈칸 추론, 순서 배열, 문장 삽입 등 고난도 문제 유형에서 실수하면 등급이 떨어집니다.

독해 속도와 정확성을 동시에 갖춰야 합니다. 이를 위해서는 구문 분석 능력과 충분한 어휘력이 필수입니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[3]}
</div>

## 학원과 과외의 차이

학원에서는 많은 학생을 한꺼번에 가르치다 보니 개인별 약점을 보완하기 어렵습니다. 1:1 과외는 학생의 현재 수준에서 출발하여 약한 부분을 집중적으로 보강합니다.

질문하기 어려운 학생도 1:1 수업에서는 편하게 물어볼 수 있습니다. 이해될 때까지 설명을 듣고, 스스로 문제를 풀어보며 실력을 키울 수 있습니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[4]}
</div>

## 학년별 학습 전략

고1은 영어의 기초를 다시 점검하고, 기본 문법과 구문 분석 능력을 확실히 익혀야 합니다. 어휘력도 꾸준히 쌓아야 합니다.

고2는 독해 실력을 본격적으로 키우는 시기입니다. 다양한 주제의 지문을 읽으며 배경지식을 쌓고, 고난도 문제 유형에 익숙해져야 합니다.

고3은 본격적인 수능 대비 시기입니다. 기출문제 분석, 모의고사 훈련, 약점 보완을 집중적으로 해야 합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[5]}
</div>

## 수업료 안내

**고1-2**는 주1회 25만원 - 36만원, 주2회 33만원 - 53만원 선입니다.

**고3**은 주1회 28만원 - 40만원, 주2회 37만원 - 59만원이 일반적입니다.

정확한 금액은 상담을 통해 안내드립니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[6]}
</div>

{{{{< cta-dual type="final" >}}}}

## 자주 묻는 질문

**Q. 내신과 수능 중 어떤 것을 먼저 준비해야 하나요?**

고1-2는 내신 위주로 공부하면서 수능 기초를 다지고, 고3은 내신과 수능을 병행합니다. 학생 상황에 따라 비중을 조절합니다.

**Q. 영어 기초가 많이 부족한데 따라갈 수 있을까요?**

중학교 문법부터 다시 점검하고 필요한 부분을 보강합니다. 기초를 확실히 다진 후 고등 내용을 진행합니다.

**Q. 단어 암기는 어떻게 해야 하나요?**

문맥 속에서 단어를 익히는 것이 효과적입니다. 단어장과 독해를 병행합니다.

**Q. 내신 시험 대비는 어떻게 하나요?**

시험 2-3주 전부터 학교 기출문제와 예상 문제 풀이로 집중 대비합니다.

## 마무리

{gu_name} {dong_name} 학생 여러분, {ending}
'''
    return content

def create_middle_math_content(city_name, gu_name, dong_name, dong_name_en, schools, file_index):
    """중등 수학 콘텐츠 생성"""
    school_str = "·".join([s.replace("고", "중") for s in schools[:3]])
    intro = get_expression(INTRO_POOL_MID_MATH, file_index + 50)
    boxes = [get_expression(BOX_POOL, file_index + i * 4 + 5) for i in range(7)]
    ending = get_expression(ENDING_POOL, file_index + 7)
    image = get_expression(IMAGE_POOL, file_index + 4)

    content = f'''---
aliases:
  - /middle/seongnam-{dong_name_en}-middle-math/
title: "성남시 {gu_name} {dong_name} 중등 수학과외 | {school_str} 내신 완벽 대비"
date: 2025-01-15
categories:
  - 중등교육
regions:
  - 경기도
  - 성남시
cities:
  - {gu_name}
description: "성남시 {gu_name} {dong_name} 중학생 수학과외 전문. {school_str.split('·')[0]} 내신 대비와 고등 선행까지. 개념부터 심화까지 체계적 1:1 지도."
tags:
  - 성남시
  - {gu_name}
  - {dong_name}
  - 중등수학
  - 수학과외
  - 내신관리
  - 고등선행
featured_image: "https://images.unsplash.com/{image}?w=1200&h=630&fit=crop"
---
{intro}

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[0]}
</div>

## 중학교 수학, 왜 중요할까요?

중학교 수학은 초등학교와 차원이 다릅니다. 음수, 문자식, 방정식 등 추상적인 개념이 등장합니다. 초등학교 때 수학을 잘했던 학생도 중학교에서 어려움을 겪는 경우가 많습니다.

{dong_name} 지역 중학생들은 내신 경쟁과 고등학교 준비를 동시에 해야 합니다. 중학교 수학이 고등학교의 기초이므로 지금 확실히 잡아야 합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[1]}
</div>

## 내신 시험 완벽 분석

{dong_name} 지역 중학교들은 내신 시험 난이도가 높습니다. 교과서 기본 문제는 물론, 심화 문제와 변형 문제가 많이 출제됩니다. 단순히 공식을 외워서는 좋은 점수를 받기 어렵고, 개념을 깊이 이해하고 다양한 유형에 적용할 수 있어야 합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[2]}
</div>

## 고등학교 수학의 기초

중학교 수학은 고등학교의 기초입니다. 중학교에서 배우는 방정식, 함수, 도형 개념이 고등학교에서 더 어렵게 확장됩니다. 중학교 때 기초가 부실하면 고등학교에서 큰 어려움을 겪습니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[3]}
</div>

## 학원과 과외의 차이

학원에서는 많은 학생을 한꺼번에 가르치다 보니 개인별 약점을 보완하기 어렵습니다. 1:1 과외는 학생의 현재 수준에서 출발하여 약한 부분을 집중적으로 보강합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[4]}
</div>

## 학년별 학습 전략

중1은 수학의 기초를 다시 점검하고, 중학 수학의 핵심인 방정식과 함수 개념을 확실히 익혀야 합니다.

중2는 일차함수, 연립방정식, 도형의 성질을 배우며 수학적 사고력을 키웁니다.

중3은 이차방정식, 이차함수, 피타고라스 정리 등 중학 수학의 정점을 찍는 시기입니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[5]}
</div>

## 수업료 안내

**중학생**은 주1회 22만원 - 32만원, 주2회 29만원 - 47만원 선입니다.

정확한 금액은 상담을 통해 안내드립니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[6]}
</div>

{{{{< cta-dual type="final" >}}}}

## 자주 묻는 질문

**Q. 내신과 선행 중 어떤 것을 먼저 해야 하나요?**

학년에 따라 다릅니다. 중1-2는 내신에 집중하고, 중3부터는 내신과 고등 선행을 병행합니다.

**Q. 수학 기초가 많이 부족한데 따라갈 수 있을까요?**

초등 내용부터 다시 점검하고 필요한 부분을 보강합니다. 기초를 확실히 다진 후 진행합니다.

**Q. 고등 선행은 언제부터 시작하나요?**

보통 중3 여름방학부터 시작합니다. 학생 상황에 따라 조절할 수 있습니다.

## 마무리

{gu_name} {dong_name} 학생 여러분, {ending}
'''
    return content

def create_middle_english_content(city_name, gu_name, dong_name, dong_name_en, schools, file_index):
    """중등 영어 콘텐츠 생성"""
    school_str = "·".join([s.replace("고", "중") for s in schools[:3]])
    intro = get_expression(INTRO_POOL_MID_ENG, file_index + 50)
    boxes = [get_expression(BOX_POOL, file_index + i * 6 + 4) for i in range(7)]
    ending = get_expression(ENDING_POOL, file_index + 8)
    image = get_expression(IMAGE_POOL, file_index + 5)

    content = f'''---
aliases:
  - /middle/seongnam-{dong_name_en}-middle-english/
title: "성남시 {gu_name} {dong_name} 중등 영어과외 | {school_str} 내신 완벽 대비"
date: 2025-01-15
categories:
  - 중등교육
regions:
  - 경기도
  - 성남시
cities:
  - {gu_name}
description: "성남시 {gu_name} {dong_name} 중학생 영어과외 전문. {school_str.split('·')[0]} 내신 대비와 고등 선행까지. 문법부터 독해까지 체계적 1:1 지도."
tags:
  - 성남시
  - {gu_name}
  - {dong_name}
  - 중등영어
  - 영어과외
  - 내신관리
  - 고등선행
featured_image: "https://images.unsplash.com/{image}?w=1200&h=630&fit=crop"
---
{intro}

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[0]}
</div>

## 중학교 영어, 왜 중요할까요?

중학교 영어는 초등학교와 차원이 다릅니다. 문법이 본격적으로 등장하고, 독해 지문도 길어집니다. 초등학교 때 영어를 잘했던 학생도 중학교에서 어려움을 겪는 경우가 많습니다.

{dong_name} 지역 중학생들은 내신 경쟁과 고등학교 준비를 동시에 해야 합니다. 중학교 영어가 고등학교의 기초이므로 지금 확실히 잡아야 합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[1]}
</div>

## 내신 시험 완벽 분석

{dong_name} 지역 중학교들은 영어 내신 시험 난이도가 높습니다. 교과서 본문 암기는 기본이고, 문법 문제와 독해 문제가 균형 있게 출제됩니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[2]}
</div>

## 고등학교 영어의 기초

중학교 영어는 고등학교의 기초입니다. 중학교에서 배우는 문법과 독해 능력이 고등학교에서 더 높은 수준으로 요구됩니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[3]}
</div>

## 학원과 과외의 차이

학원에서는 많은 학생을 한꺼번에 가르치다 보니 개인별 약점을 보완하기 어렵습니다. 1:1 과외는 학생의 현재 수준에서 출발하여 약한 부분을 집중적으로 보강합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[4]}
</div>

## 학년별 학습 전략

중1은 영어의 기초를 다시 점검하고, 기본 문법을 확실히 익혀야 합니다.

중2는 문법 실력을 본격적으로 키우는 시기입니다. 다양한 문장 구조를 익히고, 독해 연습을 시작합니다.

중3은 고등학교 진학을 앞두고 선행 학습을 시작해야 합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[5]}
</div>

## 수업료 안내

**중학생**은 주1회 22만원 - 32만원, 주2회 29만원 - 47만원 선입니다.

정확한 금액은 상담을 통해 안내드립니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[6]}
</div>

{{{{< cta-dual type="final" >}}}}

## 자주 묻는 질문

**Q. 내신과 선행 중 어떤 것을 먼저 해야 하나요?**

학년에 따라 다릅니다. 중1-2는 내신에 집중하고, 중3부터는 내신과 고등 선행을 병행합니다.

**Q. 영어 기초가 많이 부족한데 따라갈 수 있을까요?**

초등 문법부터 다시 점검하고 필요한 부분을 보강합니다. 기초를 확실히 다진 후 진행합니다.

**Q. 고등 선행은 언제부터 시작하나요?**

보통 중3 여름방학부터 시작합니다. 학생 상황에 따라 조절할 수 있습니다.

## 마무리

{gu_name} {dong_name} 학생 여러분, {ending}
'''
    return content

def create_index_content(path_type, gu_name=None, dong_name=None):
    """인덱스 파일 생성"""
    if path_type == "city":
        return '''---
title: "성남시 과외"
date: 2025-01-15
description: "성남시 전 지역 초중고 과외 정보. 수정구, 중원구, 분당구 지역별 맞춤 과외."
---
성남시 전 지역 과외 정보를 안내합니다.
'''
    elif path_type == "gu":
        return f'''---
title: "성남시 {gu_name} 과외"
date: 2025-01-15
description: "성남시 {gu_name} 지역 초중고 과외 정보. 동별 맞춤 과외 안내."
---
성남시 {gu_name} 지역 과외 정보를 안내합니다.
'''
    elif path_type == "dong":
        return f'''---
title: "성남시 {gu_name} {dong_name} 과외"
date: 2025-01-15
description: "성남시 {gu_name} {dong_name} 지역 초중고 과외 정보."
---
{dong_name} 지역 과외 정보를 안내합니다.
'''

def main():
    base_path = "/home/user/edu-guide/content/gyeonggi/seongnam"

    # 기존 seongnam 폴더 삭제 후 재생성
    if os.path.exists(base_path):
        import shutil
        shutil.rmtree(base_path)

    os.makedirs(base_path, exist_ok=True)

    # 성남시 인덱스
    with open(f"{base_path}/_index.md", "w", encoding="utf-8") as f:
        f.write(create_index_content("city"))

    file_index = 0
    total_files = 0

    for gu_key, gu_data in SEONGNAM_DATA.items():
        gu_name = gu_data["name_ko"]
        gu_path = f"{base_path}/{gu_key}"
        os.makedirs(gu_path, exist_ok=True)

        # 구 인덱스
        with open(f"{gu_path}/_index.md", "w", encoding="utf-8") as f:
            f.write(create_index_content("gu", gu_name=gu_name))

        for dong_key, dong_data in gu_data["dongs"].items():
            dong_name = dong_data["name"]
            schools = dong_data["schools"]
            dong_path = f"{gu_path}/{dong_key}"
            os.makedirs(dong_path, exist_ok=True)

            # 동 인덱스
            with open(f"{dong_path}/_index.md", "w", encoding="utf-8") as f:
                f.write(create_index_content("dong", gu_name=gu_name, dong_name=dong_name))

            # 4개 파일 생성
            with open(f"{dong_path}/high-math.md", "w", encoding="utf-8") as f:
                f.write(create_high_math_content("성남시", gu_name, dong_name, dong_key, schools, file_index))

            with open(f"{dong_path}/high-english.md", "w", encoding="utf-8") as f:
                f.write(create_high_english_content("성남시", gu_name, dong_name, dong_key, schools, file_index))

            with open(f"{dong_path}/middle-math.md", "w", encoding="utf-8") as f:
                f.write(create_middle_math_content("성남시", gu_name, dong_name, dong_key, schools, file_index))

            with open(f"{dong_path}/middle-english.md", "w", encoding="utf-8") as f:
                f.write(create_middle_english_content("성남시", gu_name, dong_name, dong_key, schools, file_index))

            file_index += 1
            total_files += 4
            print(f"Created: {gu_name} {dong_name} (4 files)")

    print(f"\n총 {total_files}개 파일 생성 완료!")

if __name__ == "__main__":
    main()
