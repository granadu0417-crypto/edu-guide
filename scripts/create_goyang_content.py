#!/usr/bin/env python3
"""
고양시 동단위 콘텐츠 생성 스크립트
- 중등/고등 수학/영어 4개 파일씩 생성
- 동별 학교 정보 반영
- 고유 이미지 배정
- 다양한 표현 사용
"""

import os
import random
from datetime import datetime

# 이미지 풀 (1000개 중 순환 사용)
def get_available_images():
    images = []
    for i in range(1, 1001):
        images.append(f"/images/edu_{i:04d}_placeholder.jpg")
    # 실제 이미지 파일 확인
    import glob
    actual_images = sorted(glob.glob('/home/user/edu-guide/static/images/edu_*.jpg'))
    if actual_images:
        return [f"/images/{os.path.basename(img)}" for img in actual_images]
    return images

IMAGE_POOL = get_available_images()
image_index = 0

def get_next_image():
    global image_index
    img = IMAGE_POOL[image_index % len(IMAGE_POOL)]
    image_index += 1
    return img

# 고양시 동/학교 데이터
GOYANG_DATA = {
    "deokyang": {  # 덕양구
        "name_kr": "덕양구",
        "dongs": {
            "samsong": {"name": "삼송동", "middle": ["고양중"], "high": ["고양고"]},
            "hwajeong1": {"name": "화정1동", "middle": ["화정중", "백양중"], "high": ["화정고"]},
            "hwajeong2": {"name": "화정2동", "middle": ["지도중", "백양중"], "high": ["화정고"]},
            "haengsin1": {"name": "행신1동", "middle": ["서정중"], "high": ["서정고"]},
            "haengsin2": {"name": "행신2동", "middle": ["무원중"], "high": ["서정고"]},
            "haengsin3": {"name": "행신3동", "middle": ["행신중"], "high": ["서정고"]},
            "haengsin4": {"name": "행신4동", "middle": ["서정중", "행신중"], "high": ["서정고"]},
            "wonheung": {"name": "원흥동", "middle": ["도래울중"], "high": ["도래울고"]},
            "hyangdong": {"name": "향동동", "middle": ["향동중"], "high": ["향동고"]},
            "deokeun": {"name": "덕은동", "middle": ["덕양중"], "high": ["능곡고"]},
            "wonsin": {"name": "원신동", "middle": ["가람중"], "high": ["백양고"]},
            "naeyu": {"name": "내유동", "middle": ["고양제일중"], "high": ["고양외고"]},
            "sinwon": {"name": "신원동", "middle": ["능곡중"], "high": ["능곡고"]},
            "juyeop": {"name": "주교동", "middle": ["주교중"], "high": ["고양고"]},
            "seongsa": {"name": "성사동", "middle": ["성사중"], "high": ["화정고"]},
            "goyang": {"name": "고양동", "middle": ["고양중"], "high": ["고양일고"]},
            "gwansan": {"name": "관산동", "middle": ["고양관산중"], "high": ["고양외고"]},
            "heungnong": {"name": "흥농동", "middle": ["흥도중"], "high": ["도래울고"]},
        }
    },
    "ilsandong": {  # 일산동구
        "name_kr": "일산동구",
        "dongs": {
            "madu1": {"name": "마두1동", "middle": ["백마중"], "high": ["백석고"]},
            "madu2": {"name": "마두2동", "middle": ["정발중"], "high": ["정발고"]},
            "baekseok1": {"name": "백석1동", "middle": ["백신중"], "high": ["백신고"]},
            "baekseok2": {"name": "백석2동", "middle": ["백신중"], "high": ["백신고"]},
            "janghang1": {"name": "장항1동", "middle": ["중산중"], "high": ["중산고"]},
            "janghang2": {"name": "장항2동", "middle": ["중산중"], "high": ["중산고"]},
            "siksa": {"name": "식사동", "middle": ["양일중"], "high": ["고양국제고"]},
            "pungsan": {"name": "풍산동", "middle": ["풍산중"], "high": ["대진고"]},
            "jeongbalsan": {"name": "정발산동", "middle": ["정발중"], "high": ["정발고"]},
            "seonsa": {"name": "산황동", "middle": ["산황중"], "high": ["대진고"]},
        }
    },
    "ilsanseo": {  # 일산서구
        "name_kr": "일산서구",
        "dongs": {
            "juyeop1": {"name": "주엽1동", "middle": ["발산중", "오마중"], "high": ["주엽고"]},
            "juyeop2": {"name": "주엽2동", "middle": ["한수중", "오마중"], "high": ["주엽고"]},
            "daehwa": {"name": "대화동", "middle": ["대화중", "저현중"], "high": ["저현고", "저동고"]},
            "tanhyeon1": {"name": "탄현1동", "middle": ["탄현중"], "high": ["일산동고"]},
            "tanhyeon2": {"name": "탄현2동", "middle": ["탄현중"], "high": ["일산동고"]},
            "ilsan1": {"name": "일산1동", "middle": ["신일중"], "high": ["일산고"]},
            "ilsan2": {"name": "일산2동", "middle": ["일산중"], "high": ["일산고"]},
            "ilsan3": {"name": "일산3동", "middle": ["신일중", "일산중"], "high": ["신일비즈니스고"]},
            "deogi": {"name": "덕이동", "middle": ["대화중"], "high": ["고양예술고"]},
            "gaswa": {"name": "가좌동", "middle": ["가좌중"], "high": ["주엽고"]},
        }
    }
}

# 서두 변형 (과목별)
MATH_INTROS = [
    "수학 성적이 오르지 않아 고민이신가요?",
    "수학, 어디서부터 잡아야 할지 막막하신가요?",
    "수학 때문에 스트레스 받고 계신가요?",
    "수학 실력, 지금 바로 키울 수 있습니다.",
    "수학이 어렵다고 느껴지시나요?",
    "수학 점수, 올리고 싶으시죠?",
    "수학 공부, 제대로 해본 적 있으신가요?",
    "수학 기초가 부족하다고 느끼시나요?",
    "수학, 혼자 공부하기 힘드시죠?",
    "수학 문제만 보면 막막하신가요?",
]

ENGLISH_INTROS = [
    "영어 성적이 생각만큼 안 오르나요?",
    "영어, 어떻게 공부해야 할지 모르겠다면",
    "영어 때문에 고민이 많으시죠?",
    "영어 실력, 확실하게 올려드립니다.",
    "영어가 어렵게 느껴지시나요?",
    "영어 점수, 올리는 방법이 있습니다.",
    "영어 공부, 제대로 시작해보세요.",
    "영어 기초부터 다시 잡고 싶으시다면",
    "영어, 혼자 공부하기 어려우시죠?",
    "영어 문법이 헷갈리시나요?",
]

# 섹션 제목 변형
SECTION_TITLES = {
    "middle_math": [
        "중학교 수학, 무엇이 중요할까요",
        "중등 수학의 핵심 포인트",
        "중학교 수학이 어려운 이유",
        "수학 실력을 키우는 방법",
        "내신 수학의 비밀",
    ],
    "middle_english": [
        "중학교 영어, 이렇게 공부하세요",
        "중등 영어의 핵심은 무엇일까요",
        "영어 실력 향상의 지름길",
        "내신 영어를 잡는 방법",
        "중학교 영어가 중요한 이유",
    ],
    "high_math": [
        "고등학교 수학, 왜 어려울까요",
        "고등 수학의 특징과 대비법",
        "수능 수학을 위한 준비",
        "내신과 수능을 동시에 잡는 법",
        "고등 수학 정복하기",
    ],
    "high_english": [
        "고등학교 영어, 이렇게 준비하세요",
        "고등 영어의 핵심 전략",
        "수능 영어 대비법",
        "내신과 수능 영어 병행하기",
        "고등 영어 실력 키우기",
    ],
}

# 마무리 변형
ENDINGS = [
    "지금 시작하세요. 변화는 첫 걸음에서 시작됩니다.",
    "더 늦기 전에 시작하세요. 함께하면 달라집니다.",
    "오늘 상담받고, 내일부터 달라지세요.",
    "시작이 반입니다. 지금 바로 문의하세요.",
    "수업 한 번으로 달라질 수 있습니다.",
    "고민만 하지 마세요. 지금 행동하세요.",
    "변화는 결심에서 시작됩니다.",
    "지금이 가장 빠른 시작입니다.",
]

# 가격 정보 (고정)
PRICING = {
    "middle_math": """**중1-2**는 주1회 기준 18만원에서 25만원, 주2회 기준 32만원에서 44만원 선입니다.

**중3**은 주1회 기준 20만원에서 28만원, 주2회 기준 36만원에서 50만원이 일반적입니다.""",

    "middle_english": """**중1-2**는 주1회 기준 17만원에서 24만원, 주2회 기준 30만원에서 42만원 선입니다.

**중3**은 주1회 기준 19만원에서 26만원, 주2회 기준 34만원에서 48만원이 일반적입니다.""",

    "high_math": """**고1~2**는 주1회 기준 25만원에서 35만원, 주2회 기준 42만원에서 58만원 선입니다.

**고3**은 주1회 기준 30만원에서 42만원, 주2회 기준 50만원에서 70만원이 일반적입니다.""",

    "high_english": """**고1~2**는 주1회 기준 22만원에서 32만원, 주2회 기준 38만원에서 52만원 선입니다.

**고3**은 주1회 기준 28만원에서 38만원, 주2회 기준 45만원에서 62만원이 일반적입니다.""",
}

def generate_middle_math_content(gu_name, dong_name, schools_middle, schools_high, image_path, variation_seed):
    """중등 수학 콘텐츠 생성"""
    random.seed(variation_seed)

    middle_schools = ", ".join(schools_middle)
    intro = random.choice(MATH_INTROS)
    section_title = random.choice(SECTION_TITLES["middle_math"])
    ending = random.choice(ENDINGS)

    # 학교 설명 변형
    school_desc_variants = [
        f"{schools_middle[0]}는 내신 시험 난이도가 높기로 유명합니다. 서술형 문제 비중이 크고, 응용력을 요구하는 문제가 많이 출제됩니다.",
        f"{schools_middle[0]} 학생들은 치열한 내신 경쟁을 하고 있습니다. 심화 문제와 서술형 문제에 대한 대비가 필수입니다.",
        f"{schools_middle[0]}의 수학 시험은 기본 개념 위에 응용력을 요구합니다. 단순 암기로는 좋은 성적을 받기 어렵습니다.",
    ]
    school_desc = random.choice(school_desc_variants)

    # 추가 단원 설명 변형
    unit_desc_variants = [
        "중학교 수학에서 가장 중요한 단원 중 하나는 함수입니다. 함수의 개념을 정확히 이해해야 고등학교 수학에서 수월하게 따라갈 수 있습니다. 일차함수의 그래프, 기울기, y절편의 의미를 명확히 알고 있어야 합니다.",
        "도형 단원은 많은 학생들이 어려워하는 부분입니다. 삼각형의 합동 조건, 닮음의 성질, 피타고라스 정리 등을 증명과 함께 이해해야 합니다. 단순 공식 암기가 아닌 원리 이해가 중요합니다.",
        "방정식과 부등식은 중학교 수학의 핵심입니다. 일차방정식에서 시작해 연립방정식, 이차방정식으로 확장됩니다. 각 단계를 차근차근 이해하지 않으면 다음 단계에서 막히게 됩니다.",
    ]
    unit_desc = random.choice(unit_desc_variants)

    # 학습 방법 변형
    study_method_variants = [
        "수학은 이해와 연습이 함께 가야 합니다. 개념을 이해했다고 생각해도 막상 문제를 풀면 적용이 안 되는 경우가 많습니다. 충분한 문제 풀이 연습이 필수입니다.",
        "오답 노트를 활용하는 것이 효과적입니다. 틀린 문제를 다시 풀어보고, 왜 틀렸는지 분석하는 습관을 들이면 같은 유형에서 실수를 줄일 수 있습니다.",
        "예습과 복습의 균형이 중요합니다. 수업 전 미리 교과서를 읽어보고, 수업 후에는 그날 배운 내용을 정리하는 습관을 들이면 학습 효과가 배가 됩니다.",
    ]
    study_method = random.choice(study_method_variants)

    content = f"""---
aliases:
  - /middle/goyang-{dong_name.replace('동', '')}-middle-math/
title: "고양시 {gu_name} {dong_name} 중등 수학과외 | {middle_schools} 내신 완벽 대비"
date: 2025-01-15
categories:
  - 중등교육
regions:
  - 경기도
  - 고양시
cities:
  - {gu_name}
description: "고양시 {gu_name} {dong_name} 중학생 수학과외 전문. {middle_schools} 내신 맞춤 관리. 개념부터 심화까지 체계적 1:1 지도."
tags:
  - 고양시
  - {gu_name}
  - {dong_name}
  - 중등수학
  - 수학과외
  - 내신관리
{chr(10).join([f'  - {s}' for s in schools_middle])}
featured_image: "{image_path}"
---

{intro} 고양시 {gu_name} {dong_name}에서 중학교 수학 과외를 찾고 계시다면, 지역 학교 특성에 맞춘 맞춤형 수업이 필요합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
첫 수업에서 학생의 현재 수학 실력을 정확하게 진단합니다. 어떤 개념이 부족한지, 어디서 실수가 나는지 파악한 후 맞춤 커리큘럼을 설계합니다.
</div>

## {section_title}

중학교 수학은 초등학교와 완전히 다릅니다. 음수, 문자와 식, 방정식 등 추상적인 개념이 등장하면서 많은 학생들이 어려움을 겪습니다. 기초 개념을 제대로 이해하지 못하면 상위 단원으로 갈수록 더 힘들어집니다.

특히 {dong_name} 지역 학생들이 다니는 {middle_schools}의 내신 시험은 단순 계산 문제보다 응용 문제와 서술형 문제 비중이 높습니다. 개념을 정확히 이해하고 다양한 유형의 문제를 풀어본 경험이 있어야 좋은 성적을 받을 수 있습니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
개념 설명 후 바로 관련 문제를 풀어봅니다. 이해했다고 생각해도 문제에 적용하면 막히는 경우가 많기 때문입니다. 직접 풀어보며 개념을 확실히 익힙니다.
</div>

## {schools_middle[0]} 수학 시험의 특징

{school_desc}

내신 시험에서 좋은 성적을 받으려면 학교별 출제 경향을 파악하는 것이 중요합니다. 어떤 유형의 문제가 자주 나오는지, 서술형 채점 기준은 어떤지 알아야 효과적으로 대비할 수 있습니다.

{unit_desc}

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{schools_middle[0]} 기출문제를 분석하여 자주 출제되는 유형을 정리합니다. 학교 선생님의 출제 스타일을 파악하여 맞춤 대비를 합니다.
</div>

## 1:1 과외의 장점

학원에서는 여러 학생을 한꺼번에 가르치다 보니 개인별 부족한 부분을 채워주기 어렵습니다. 1:1 과외는 학생의 현재 수준에 맞춰 수업이 진행됩니다. 이해가 안 되는 부분은 이해될 때까지 설명하고, 이미 아는 내용은 빠르게 넘어갑니다.

또한 수업 시간과 장소를 유연하게 조절할 수 있어 학생의 일정에 맞출 수 있습니다. 학원 시간에 맞춰 다른 일정을 포기할 필요가 없습니다.

{study_method}

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
매 수업 시작 전 지난 수업 내용을 복습합니다. 숙제 검사와 오답 분석을 통해 같은 실수를 반복하지 않도록 지도합니다.
</div>

## 학년별 학습 전략

중1은 수학적 사고의 기초를 다지는 시기입니다. 정수와 유리수, 문자와 식, 일차방정식의 개념을 확실히 이해해야 합니다. 이 시기에 기초가 흔들리면 중2, 중3에서 더 큰 어려움을 겪게 됩니다. 특히 음수의 개념과 문자를 사용한 식의 계산은 앞으로의 모든 수학 학습의 토대가 됩니다.

중2는 연립방정식, 일차함수 등 함수 개념이 본격적으로 등장합니다. 그래프를 해석하고 그리는 능력, 식을 세우고 푸는 능력이 필요합니다. 도형의 성질과 증명도 중요한 단원입니다. 특히 증명 문제는 논리적 사고력을 키우는 데 매우 중요합니다.

중3은 이차방정식, 이차함수, 삼각비, 원의 성질 등 고등학교 수학의 기초가 되는 내용을 배웁니다. 이 시기에 배운 내용이 고1 수학과 직결되므로 확실히 이해하고 넘어가야 합니다. 특히 이차함수의 그래프와 성질은 고등학교에서 더 깊이 다루게 됩니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
학생의 학년과 수준에 맞춰 커리큘럼을 구성합니다. 부족한 단원은 이전 학년 내용까지 돌아가서 보완합니다.
</div>

## 효과적인 수학 학습법

수학 실력을 키우려면 단순히 많은 문제를 푸는 것보다 한 문제를 깊이 이해하는 것이 중요합니다. 문제를 풀 때는 왜 그렇게 푸는지, 다른 방법은 없는지 생각해보는 습관을 들여야 합니다.

틀린 문제는 반드시 다시 풀어봐야 합니다. 해설을 보고 이해했다고 넘어가면 같은 유형에서 또 틀리게 됩니다. 스스로 풀 수 있을 때까지 반복 연습하는 것이 핵심입니다.

또한 수학은 꾸준함이 중요합니다. 하루에 많은 양을 한꺼번에 하는 것보다, 매일 조금씩 꾸준히 하는 것이 실력 향상에 효과적입니다. 시험 기간에만 벼락치기하면 금방 잊어버리게 됩니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
문제 풀이 과정을 함께 점검합니다. 정답뿐 아니라 풀이 과정의 논리성도 확인하여 서술형 문제에 대비합니다.
</div>

## 수업료 안내

{PRICING["middle_math"]}

수업료는 학생의 현재 수준, 목표, 수업 방식에 따라 달라질 수 있습니다. 정확한 수업료는 상담을 통해 안내드립니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
첫 상담에서 학생의 현재 상황과 목표를 파악합니다. 최적의 수업 계획과 예상 수업료를 안내드립니다.
</div>

{{{{< cta-dual type="final" >}}}}

## 부모님께 드리는 말씀

자녀의 수학 성적이 걱정되신다면, 지금이 바로 변화의 시작점입니다. 중학교 수학은 고등학교 수학의 기초가 됩니다. 이 시기에 탄탄한 기초를 다져야 고등학교에서 어려움을 겪지 않습니다.

수학은 한 번 놓치면 따라잡기가 어렵습니다. 지금 바로 시작하는 것이 가장 현명한 선택입니다.

1:1 과외는 학원과 달리 학생 개인에게 집중합니다. 어디서 막히는지 정확히 파악하고, 그 부분을 집중적으로 보완합니다. 학생의 성향과 학습 스타일에 맞춘 맞춤형 수업이 가능합니다.

상담은 부담 없이 받으실 수 있습니다. 현재 학생의 상황을 파악하고, 어떤 방향으로 학습을 진행하면 좋을지 함께 고민해드립니다.

학생에게 맞는 선생님을 연결해드리기 위해 학습 스타일과 성향도 함께 확인합니다.

## 자주 묻는 질문

**Q. 수학 기초가 많이 부족한데 따라갈 수 있을까요?**

기초부터 차근차근 다시 잡아드립니다. 학생의 현재 수준에서 시작해서 점차 실력을 끌어올립니다. 필요하다면 초등 연산부터 복습합니다.

**Q. 내신 시험 기간에는 어떻게 수업하나요?**

시험 2주 전부터 시험 범위 집중 대비로 전환합니다. 기출문제 풀이와 예상 문제 훈련을 합니다. 학교별 출제 경향에 맞춘 맞춤 대비를 진행합니다.

**Q. 숙제는 얼마나 나오나요?**

학생의 학습량과 일정에 맞춰 적절한 양을 내드립니다. 숙제 검사와 오답 분석도 철저히 합니다. 무리한 숙제로 학습 의욕이 떨어지지 않도록 조절합니다.

**Q. 수업은 어디서 하나요?**

학생 집 방문 수업 또는 온라인 수업 중 선택 가능합니다. 학생에게 편한 방식으로 진행합니다. 화상 수업도 대면 수업과 동일한 효과를 낼 수 있습니다.

**Q. 선생님은 어떤 분이신가요?**

수학 전공자 또는 수학 교육 경험이 풍부한 선생님으로 연결해 드립니다. 학생과의 궁합도 중요하게 고려합니다. 필요시 선생님 변경도 가능합니다.

**Q. 성적이 안 오르면 어떻게 하나요?**

정기적으로 학습 상황을 점검하고 필요시 수업 방식을 조정합니다. 목표 달성까지 함께 노력합니다. 성적 향상에는 시간이 필요하므로 꾸준함이 중요합니다.

**Q. 고등학교 수학 선행도 가능한가요?**

가능합니다. 중3 학생의 경우 고등학교 수학 내용을 미리 학습할 수 있습니다. 단, 현재 학년 내용이 완벽히 이해된 후에 진행합니다.

**Q. 수업 횟수는 어떻게 정하나요?**

학생의 현재 수준과 목표에 따라 상담 후 결정합니다. 보통 주1회 또는 주2회로 진행하며, 시험 기간에는 추가 수업도 가능합니다.

**Q. 학원과 과외를 병행해도 되나요?**

가능합니다. 다만 학습량이 과도해지지 않도록 조율이 필요합니다. 상담 시 현재 학습 상황을 말씀해주시면 적절한 방향을 안내드립니다.

## 마무리

{dong_name} 중학생 여러분, 수학은 포기할 과목이 아닙니다. {middle_schools} 내신에 맞춤 체계적인 수업으로 수학 실력을 키워보세요. {ending}
"""
    return content


def generate_middle_english_content(gu_name, dong_name, schools_middle, schools_high, image_path, variation_seed):
    """중등 영어 콘텐츠 생성"""
    random.seed(variation_seed + 1000)

    middle_schools = ", ".join(schools_middle)
    intro = random.choice(ENGLISH_INTROS)
    section_title = random.choice(SECTION_TITLES["middle_english"])
    ending = random.choice(ENDINGS)

    # 추가 문법 설명 변형
    grammar_desc_variants = [
        "영어 문법에서 가장 중요한 것은 시제입니다. 현재, 과거, 미래 시제뿐 아니라 현재완료, 과거완료까지 정확히 구분해야 합니다. 시제를 헷갈리면 문장의 의미가 완전히 달라지기 때문입니다.",
        "부정사와 동명사는 많은 학생들이 혼동하는 부분입니다. 어떤 동사 뒤에 to부정사가 오는지, 동명사가 오는지 정확히 알아야 합니다. 이 부분을 확실히 정리해두면 고등학교에서도 유용합니다.",
        "관계대명사는 문장을 연결하는 핵심 도구입니다. who, which, that의 쓰임을 정확히 이해하고, 관계대명사가 생략되는 경우도 알아야 합니다. 독해에서 긴 문장을 이해하려면 필수입니다.",
    ]
    grammar_desc = random.choice(grammar_desc_variants)

    # 학습 방법 변형
    study_tip_variants = [
        "영어 단어는 문맥 속에서 외워야 오래 기억됩니다. 단어장만 보고 외우는 것보다 문장 속에서 단어를 익히면 실제로 사용할 수 있는 어휘력이 됩니다.",
        "영어 독해력을 키우려면 매일 꾸준히 영어 지문을 읽어야 합니다. 처음에는 쉬운 지문부터 시작해서 점점 난이도를 높여가면 됩니다.",
        "영어 문법은 예문과 함께 공부해야 합니다. 규칙만 외우면 금방 잊어버리지만, 예문을 통해 익히면 자연스럽게 사용할 수 있습니다.",
    ]
    study_tip = random.choice(study_tip_variants)

    content = f"""---
aliases:
  - /middle/goyang-{dong_name.replace('동', '')}-middle-english/
title: "고양시 {gu_name} {dong_name} 중등 영어과외 | {middle_schools} 내신 완벽 대비"
date: 2025-01-15
categories:
  - 중등교육
regions:
  - 경기도
  - 고양시
cities:
  - {gu_name}
description: "고양시 {gu_name} {dong_name} 중학생 영어과외 전문. {middle_schools} 내신 맞춤 관리. 문법부터 독해까지 체계적 1:1 지도."
tags:
  - 고양시
  - {gu_name}
  - {dong_name}
  - 중등영어
  - 영어과외
  - 내신관리
{chr(10).join([f'  - {s}' for s in schools_middle])}
featured_image: "{image_path}"
---

{intro} 고양시 {gu_name} {dong_name}에서 중학교 영어 과외를 찾고 계시다면, 학교 내신에 맞춘 맞춤형 수업이 효과적입니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
첫 수업에서 학생의 영어 실력을 종합적으로 진단합니다. 문법, 어휘, 독해, 듣기 영역별로 강점과 약점을 파악한 후 맞춤 커리큘럼을 설계합니다.
</div>

## {section_title}

중학교 영어는 본격적인 문법 학습이 시작되는 시기입니다. 시제, 조동사, 부정사, 동명사, 관계대명사 등 복잡한 문법 개념들이 등장합니다. 이 시기에 문법 기초를 탄탄히 다져야 고등학교 영어에서 어려움을 겪지 않습니다.

{dong_name} 지역 {middle_schools} 학생들은 높은 내신 경쟁을 하고 있습니다. 영어 시험에서는 문법 문제뿐 아니라 긴 지문을 읽고 이해하는 독해 문제, 서술형 문제 비중도 높습니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
문법 개념을 설명한 후 다양한 문제를 통해 적용 연습을 합니다. 틀린 문제는 왜 틀렸는지 정확히 분석하여 같은 실수를 반복하지 않도록 합니다.
</div>

## {schools_middle[0]} 영어 시험의 특징

{schools_middle[0]}의 영어 시험은 교과서 본문에 대한 깊은 이해를 요구합니다. 단순 암기가 아니라 문장 구조를 파악하고, 어휘의 쓰임을 이해해야 합니다. 서술형 문제에서는 영작 능력도 평가합니다.

내신에서 좋은 성적을 받으려면 교과서 본문을 철저히 분석하고, 출제 가능한 문제 유형을 미리 연습해야 합니다. 학교별 출제 경향을 파악하는 것이 중요합니다.

{grammar_desc}

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
교과서 본문을 문장 단위로 분석합니다. 핵심 문법, 어휘, 표현을 정리하고 관련 문제를 풀어봅니다.
</div>

## 1:1 영어 과외의 효과

학원에서는 정해진 커리큘럼대로 수업이 진행됩니다. 이미 아는 내용도 다시 듣고, 모르는 내용은 충분히 이해하지 못한 채 넘어가기 쉽습니다. 1:1 과외는 학생의 수준에 맞춰 수업이 진행되므로 시간을 효율적으로 사용할 수 있습니다.

특히 영어는 듣기, 말하기, 읽기, 쓰기 네 가지 영역이 모두 중요합니다. 1:1 수업에서는 학생에게 부족한 영역을 집중적으로 보완할 수 있습니다.

{study_tip}

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
학생의 약점 영역을 파악하여 집중 훈련합니다. 문법이 약하면 문법을, 독해가 약하면 독해를 보강합니다.
</div>

## 학년별 학습 전략

중1은 기본 문법의 기초를 다지는 시기입니다. be동사, 일반동사, 시제, 조동사의 기본 개념을 확실히 이해해야 합니다. 어휘력도 중요하므로 매일 꾸준히 단어를 외우는 습관을 들여야 합니다. 하루 20개씩 꾸준히 외우면 1년이면 7,000개 이상의 단어를 익힐 수 있습니다.

중2는 문법이 복잡해지는 시기입니다. 부정사, 동명사, 분사, 접속사 등 고등학교 영어에서도 계속 나오는 핵심 문법을 배웁니다. 이 시기에 문법을 정확히 이해하지 못하면 고등학교에서 큰 어려움을 겪습니다. 특히 to부정사의 다양한 용법은 확실히 정리해야 합니다.

중3은 관계대명사, 가정법 등 복잡한 문장 구조를 배웁니다. 독해 지문도 길어지고 어려워집니다. 고등학교 영어를 미리 준비하는 마음으로 공부해야 합니다. 이 시기에 영어 독해 습관을 들여두면 고등학교에서 큰 도움이 됩니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
학년별 핵심 문법과 어휘를 체계적으로 정리합니다. 다음 학년 예습도 병행하여 선행 학습의 효과를 누릴 수 있습니다.
</div>

## 효과적인 영어 학습법

영어 실력은 하루아침에 오르지 않습니다. 매일 조금씩 꾸준히 공부하는 것이 가장 효과적입니다. 단어, 문법, 독해를 균형 있게 학습하고, 틀린 문제는 반드시 복습해야 합니다.

영어 지문을 읽을 때는 모르는 단어가 나와도 먼저 문맥으로 의미를 추측해보세요. 바로 사전을 찾는 것보다 추측하는 연습을 하면 실전에서 도움이 됩니다.

영어는 언어이기 때문에 반복 노출이 중요합니다. 같은 문법 개념도 여러 번 다른 예문으로 접하면 자연스럽게 체화됩니다. 시험 기간에만 공부하면 금방 잊어버리니 평소에 꾸준히 학습하는 것이 중요합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
독해 전략과 어휘 학습법을 가르쳐드립니다. 효율적으로 공부하는 방법을 알면 같은 시간에 더 많이 배울 수 있습니다.
</div>

## 수업료 안내

{PRICING["middle_english"]}

수업료는 학생의 현재 수준, 목표, 수업 방식에 따라 달라질 수 있습니다. 정확한 수업료는 상담을 통해 안내드립니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
첫 상담에서 학생의 현재 상황과 목표를 파악합니다. 최적의 수업 계획과 예상 수업료를 안내드립니다.
</div>

{{{{< cta-dual type="final" >}}}}

## 부모님께 드리는 말씀

자녀의 영어 성적이 걱정되신다면, 지금이 바로 변화의 시작점입니다. 중학교 영어는 고등학교 영어의 기초가 됩니다. 이 시기에 문법과 어휘의 기초를 다져야 고등학교에서 어려움을 겪지 않습니다.

영어는 언어이기 때문에 꾸준한 학습이 필수입니다. 지금 바로 시작하는 것이 가장 현명한 선택입니다.

1:1 과외는 학원과 달리 학생 개인에게 집중합니다. 어디서 막히는지 정확히 파악하고, 그 부분을 집중적으로 보완합니다. 학생의 성향과 학습 스타일에 맞춘 맞춤형 수업이 가능합니다.

상담은 부담 없이 받으실 수 있습니다. 현재 학생의 상황을 파악하고, 어떤 방향으로 학습을 진행하면 좋을지 함께 고민해드립니다.

학생에게 맞는 선생님을 연결해드리기 위해 학습 스타일과 성향도 함께 확인합니다.

## 자주 묻는 질문

**Q. 영어 기초가 많이 부족한데 따라갈 수 있을까요?**

기초부터 차근차근 다시 잡아드립니다. 알파벳과 파닉스부터 필요하다면 그 단계부터 시작합니다. 현재 수준에 맞춰 진도를 조절합니다.

**Q. 문법 암기가 너무 어려워요.**

단순 암기가 아니라 원리를 이해시켜드립니다. 왜 그런 규칙이 있는지 알면 기억에 오래 남습니다. 예문을 통해 자연스럽게 익히도록 합니다.

**Q. 듣기 실력도 향상시킬 수 있나요?**

물론입니다. 듣기 훈련 방법을 가르쳐드리고, 필요하면 수업 중 듣기 연습도 합니다. 쉐도잉, 딕테이션 등 효과적인 듣기 훈련법을 알려드립니다.

**Q. 영어 말하기 연습도 하나요?**

원하시면 수업 중 간단한 회화 연습도 진행합니다. 영어로 말하는 것에 자신감을 키워드립니다.

**Q. 내신 시험 대비는 어떻게 하나요?**

시험 2주 전부터 교과서 본문 완벽 분석과 예상 문제 풀이로 집중 대비합니다. 학교별 출제 경향을 파악하여 맞춤 대비를 합니다.

**Q. 고등학교 영어 선행도 가능한가요?**

가능합니다. 중3 학생의 경우 고등학교 영어 문법과 독해를 미리 준비할 수 있습니다.

**Q. 어휘력을 빠르게 키우는 방법이 있나요?**

매일 정해진 양을 꾸준히 외우는 것이 가장 효과적입니다. 어근, 접두사, 접미사를 활용하면 더 효율적으로 외울 수 있습니다.

**Q. 수업 횟수는 어떻게 정하나요?**

학생의 현재 수준과 목표에 따라 상담 후 결정합니다. 보통 주1회 또는 주2회로 진행하며, 시험 기간에는 추가 수업도 가능합니다.

**Q. 학원과 과외를 병행해도 되나요?**

가능합니다. 다만 학습량이 과도해지지 않도록 조율이 필요합니다. 상담 시 현재 학습 상황을 말씀해주시면 적절한 방향을 안내드립니다.

## 마무리

{dong_name} 중학생 여러분, 영어는 꾸준함이 답입니다. {middle_schools} 내신에 맞춘 체계적인 수업으로 영어 실력을 키워보세요. {ending}
"""
    return content


def generate_high_math_content(gu_name, dong_name, schools_middle, schools_high, image_path, variation_seed):
    """고등 수학 콘텐츠 생성"""
    random.seed(variation_seed + 2000)

    high_schools = ", ".join(schools_high)
    intro = random.choice(MATH_INTROS)
    section_title = random.choice(SECTION_TITLES["high_math"])
    ending = random.choice(ENDINGS)

    # 추가 단원 설명 변형
    subject_desc_variants = [
        "미적분은 고등학교 수학의 핵심입니다. 극한, 미분, 적분의 개념을 확실히 이해해야 수능에서 고득점을 받을 수 있습니다. 특히 미분과 적분의 관계, 적분의 활용 문제는 자주 출제됩니다.",
        "확률과 통계는 계산 실수가 많이 나오는 영역입니다. 순열, 조합, 확률의 기본 개념을 정확히 이해하고, 다양한 유형의 문제를 풀어봐야 합니다. 특히 조건부확률은 많은 학생이 어려워합니다.",
        "기하는 공간 감각이 필요한 영역입니다. 벡터의 개념, 평면과 직선의 방정식을 이해하고, 도형의 성질을 파악해야 합니다. 그림을 그려가며 문제를 푸는 연습이 중요합니다.",
    ]
    subject_desc = random.choice(subject_desc_variants)

    # 학습 조언 변형
    study_advice_variants = [
        "수학은 단순히 많은 문제를 푸는 것보다 한 문제를 깊이 이해하는 것이 중요합니다. 왜 이렇게 푸는지, 다른 방법은 없는지 생각하는 습관을 들이세요.",
        "오답 노트를 꼭 만드세요. 틀린 문제를 다시 풀어보고, 왜 틀렸는지 분석하면 같은 실수를 줄일 수 있습니다. 시험 직전에 오답 노트를 보면 효과적입니다.",
        "개념 공부와 문제 풀이의 균형이 중요합니다. 개념을 대충 알고 문제만 많이 풀면 비슷한 유형만 풀 수 있습니다. 새로운 유형이 나오면 막히게 됩니다.",
    ]
    study_advice = random.choice(study_advice_variants)

    content = f"""---
aliases:
  - /high/goyang-{dong_name.replace('동', '')}-high-math/
title: "고양시 {gu_name} {dong_name} 고등 수학과외 | {high_schools} 내신·수능 완벽 대비"
date: 2025-01-15
categories:
  - 고등교육
regions:
  - 경기도
  - 고양시
cities:
  - {gu_name}
description: "고양시 {gu_name} {dong_name} 고등학생 수학과외 전문. {high_schools} 내신과 수능 동시 대비. 개념부터 킬러문항까지 체계적 1:1 지도."
tags:
  - 고양시
  - {gu_name}
  - {dong_name}
  - 고등수학
  - 수학과외
  - 내신관리
  - 수능대비
{chr(10).join([f'  - {s}' for s in schools_high])}
featured_image: "{image_path}"
---

{intro} 고양시 {gu_name} {dong_name}에서 고등학교 수학 과외를 찾고 계시다면, 내신과 수능을 모두 대비할 수 있는 체계적인 수업이 필요합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
첫 수업에서 학생의 수학 실력을 정밀 진단합니다. 개념 이해도, 계산 정확도, 문제 해결 속도를 파악하고 부족한 부분부터 채워갑니다.
</div>

## {section_title}

고등학교 수학은 중학교와 차원이 다릅니다. 추상적인 개념이 많아지고, 함수, 미적분, 확률과 통계 등 새로운 영역이 등장합니다. 중학교 때 수학을 잘했던 학생도 고등학교에서 어려움을 겪는 경우가 많습니다.

{dong_name} 지역 {high_schools} 학생들은 높은 내신 경쟁과 수능 준비를 동시에 해야 합니다. 학교 시험은 학교별 특성에 맞춰 대비해야 하고, 수능은 전국 단위 경쟁이므로 또 다른 전략이 필요합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
내신과 수능의 차이를 명확히 알려드립니다. 두 가지를 효율적으로 병행할 수 있는 학습 전략을 세웁니다.
</div>

## {schools_high[0]} 수학 시험의 특징

{schools_high[0]}는 내신 시험 난이도가 높기로 유명합니다. 교과서 기본 문제는 물론, 심화 문제와 변형 문제가 많이 출제됩니다. 단순히 공식을 외워서는 좋은 점수를 받기 어렵고, 개념을 깊이 이해하고 다양한 유형에 적용할 수 있어야 합니다.

시험 시간 대비 문제 양이 많은 편이어서 시간 관리도 중요합니다. 평소 시간을 재고 문제를 푸는 연습을 해야 실전에서 당황하지 않습니다.

{subject_desc}

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{schools_high[0]} 기출문제를 철저히 분석합니다. 자주 출제되는 유형과 함정 문제 패턴을 파악하여 대비합니다.
</div>

## 수능 수학 대비

수능 수학은 내신과 출제 방식이 다릅니다. 킬러 문항이라 불리는 21번, 29번, 30번 문제는 여러 개념을 복합적으로 적용해야 풀 수 있습니다. 시간 압박 속에서 정확하게 문제를 푸는 능력이 필요합니다.

수능에서 1등급을 받으려면 킬러 문항 중 최소 1~2개는 맞혀야 합니다. 이를 위해서는 기본 개념이 완벽해야 하고, 다양한 심화 문제를 풀어본 경험이 있어야 합니다.

{study_advice}

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
기출문제 분석을 통해 수능 출제 패턴을 파악합니다. 킬러 문항 접근법을 체계적으로 훈련합니다.
</div>

## 1:1 과외의 장점

학원에서는 많은 학생을 한꺼번에 가르치다 보니 개인별 약점을 보완하기 어렵습니다. 1:1 과외는 학생의 현재 수준에서 출발하여 약한 부분을 집중적으로 보강합니다.

질문하기 어려운 학생도 1:1 수업에서는 편하게 물어볼 수 있습니다. 이해될 때까지 설명을 듣고, 스스로 문제를 풀어보며 실력을 키울 수 있습니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
매 수업 시작 전 지난 내용을 복습합니다. 숙제 검사와 오답 분석을 통해 실수를 줄여갑니다.
</div>

## 학년별 학습 전략

고1은 수학의 기초를 다시 점검하고, 고등 수학의 핵심인 함수 개념을 확실히 익혀야 합니다. 다항식, 방정식과 부등식, 도형의 방정식 등 수학(상), 수학(하) 내용을 탄탄히 해야 고2, 고3에서 수월합니다. 특히 함수의 그래프를 정확히 그리고 해석할 수 있어야 합니다.

고2는 수학I, 수학II를 배우며 지수, 로그, 삼각함수, 미분과 적분을 익힙니다. 이 시기에 배우는 내용이 수능 수학의 핵심이므로 확실히 이해하고 넘어가야 합니다. 미분과 적분의 개념은 특히 중요하므로 시간을 들여 완벽히 익혀야 합니다.

고3은 본격적인 수능 대비 시기입니다. 기출문제 분석, 모의고사 훈련, 약점 보완을 집중적으로 해야 합니다. 내신도 놓치지 말아야 하므로 효율적인 시간 관리가 중요합니다. 6월과 9월 모의고사를 기준으로 학습 계획을 세우는 것이 좋습니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
학년별 목표에 맞춰 커리큘럼을 구성합니다. 내신과 수능 비중을 조절하여 최적의 학습 계획을 세웁니다.
</div>

## 효과적인 수학 학습법

수학 실력을 키우려면 문제를 많이 푸는 것도 중요하지만, 한 문제를 깊이 이해하는 것이 더 중요합니다. 정답을 맞혔더라도 풀이 과정이 맞는지, 더 효율적인 방법은 없는지 생각해봐야 합니다.

모의고사 후에는 반드시 오답을 분석해야 합니다. 왜 틀렸는지, 어떤 개념이 부족했는지 파악하고 보완해야 다음 시험에서 같은 실수를 하지 않습니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
문제 풀이 과정을 함께 점검합니다. 더 효율적인 풀이 방법이 있으면 알려드리고, 시간 단축 전략도 훈련합니다.
</div>

## 수업료 안내

{PRICING["high_math"]}

수업료는 학생의 현재 수준, 목표, 수업 방식에 따라 달라질 수 있습니다. 정확한 수업료는 상담을 통해 안내드립니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
첫 상담에서 학생의 현재 상황과 목표를 파악합니다. 최적의 수업 계획과 예상 수업료를 안내드립니다.
</div>

{{{{< cta-dual type="final" >}}}}

## 부모님께 드리는 말씀

자녀의 수학 성적이 걱정되신다면, 지금이 바로 변화의 시작점입니다. 고등학교 수학은 대입에서 가장 중요한 과목입니다. 수학 성적에 따라 지원할 수 있는 대학이 달라집니다.

1:1 과외는 학원과 달리 학생 개인에게 집중합니다. 어디서 막히는지 정확히 파악하고, 그 부분을 집중적으로 보완합니다. 학생의 성향과 학습 스타일에 맞춘 맞춤형 수업이 가능합니다.

상담은 부담 없이 받으실 수 있습니다. 현재 학생의 상황을 파악하고, 어떤 방향으로 학습을 진행하면 좋을지 함께 고민해드립니다.

## 자주 묻는 질문

**Q. 내신과 수능 중 어떤 것을 먼저 준비해야 하나요?**

고1~2는 내신 위주로 공부하면서 수능 기초를 다지고, 고3은 내신과 수능을 병행합니다. 학생 상황에 따라 비중을 조절합니다.

**Q. 수학 기초가 많이 부족한데 따라갈 수 있을까요?**

중학교 내용부터 다시 점검하고 필요한 부분을 보강합니다. 기초를 확실히 다진 후 고등 내용을 진행합니다.

**Q. 킬러 문항은 어떻게 대비하나요?**

기본 개념을 완벽히 익힌 후, 고난도 문제 유형별 접근법을 체계적으로 훈련합니다. 최근 기출문제를 분석하여 출제 경향을 파악합니다.

**Q. 내신 시험 대비는 어떻게 하나요?**

시험 2~3주 전부터 학교 기출문제와 예상 문제 풀이로 집중 대비합니다. 학교 선생님의 출제 스타일도 분석합니다.

**Q. 온라인 수업도 가능한가요?**

가능합니다. 화상 수업으로 대면 수업과 동일한 효과를 낼 수 있습니다. 태블릿을 활용한 필기 공유도 가능합니다.

**Q. 성적이 안 오르면 어떻게 하나요?**

정기적으로 학습 상황을 점검하고 필요시 수업 방식을 조정합니다. 성적 향상에는 시간이 필요하므로 꾸준함이 중요합니다.

**Q. 수능 선택과목은 어떻게 정하나요?**

학생의 성향과 목표 대학에 따라 상담해드립니다. 각 선택과목의 특징과 유불리를 분석하여 조언드립니다.

**Q. 수업 횟수는 어떻게 정하나요?**

학생의 현재 수준과 목표에 따라 상담 후 결정합니다. 보통 주1회 또는 주2회로 진행하며, 시험 기간에는 추가 수업도 가능합니다.

**Q. 학원과 과외를 병행해도 되나요?**

가능합니다. 다만 학습량이 과도해지지 않도록 조율이 필요합니다. 상담 시 현재 학습 상황을 말씀해주시면 적절한 방향을 안내드립니다.

## 마무리

{dong_name} 고등학생 여러분, 수학은 포기할 과목이 아닙니다. {high_schools} 내신과 수능에 맞춘 체계적인 수업으로 수학 실력을 키워보세요. {ending}
"""
    return content


def generate_high_english_content(gu_name, dong_name, schools_middle, schools_high, image_path, variation_seed):
    """고등 영어 콘텐츠 생성"""
    random.seed(variation_seed + 3000)

    high_schools = ", ".join(schools_high)
    intro = random.choice(ENGLISH_INTROS)
    section_title = random.choice(SECTION_TITLES["high_english"])
    ending = random.choice(ENDINGS)

    # 추가 독해 설명 변형
    reading_desc_variants = [
        "수능 영어에서 가장 어려운 유형은 빈칸 추론입니다. 지문의 핵심 논리를 파악하고, 빈칸에 들어갈 내용을 추론해야 합니다. 이 유형을 잘 풀려면 다양한 주제의 지문을 읽어본 경험이 필요합니다.",
        "순서 배열과 문장 삽입 문제는 글의 논리적 흐름을 파악하는 능력이 필요합니다. 접속사와 지시어의 역할을 이해하고, 문장 간의 연결 관계를 파악해야 합니다.",
        "글의 요지나 주제를 파악하는 문제는 기본이지만 중요합니다. 지문 전체를 빠르게 읽고 핵심 내용을 파악하는 연습을 해야 합니다. 첫 문장과 마지막 문장에 집중하세요.",
    ]
    reading_desc = random.choice(reading_desc_variants)

    # 학습 조언 변형
    study_tip_variants = [
        "영어 실력 향상의 핵심은 꾸준함입니다. 매일 30분씩 영어 지문을 읽는 것이 일주일에 한 번 3시간 읽는 것보다 효과적입니다.",
        "모르는 단어가 나와도 바로 사전을 찾지 마세요. 먼저 문맥에서 의미를 추측해보고, 그 다음 확인하세요. 이 습관이 실전에서 도움이 됩니다.",
        "영어 듣기는 수능에서 비중이 높습니다. 매일 10분씩 영어 듣기 연습을 하면 큰 도움이 됩니다. 듣기 평가 만점은 1등급의 기본입니다.",
    ]
    study_tip = random.choice(study_tip_variants)

    content = f"""---
aliases:
  - /high/goyang-{dong_name.replace('동', '')}-high-english/
title: "고양시 {gu_name} {dong_name} 고등 영어과외 | {high_schools} 내신·수능 완벽 대비"
date: 2025-01-15
categories:
  - 고등교육
regions:
  - 경기도
  - 고양시
cities:
  - {gu_name}
description: "고양시 {gu_name} {dong_name} 고등학생 영어과외 전문. {high_schools} 내신과 수능 동시 대비. 독해부터 문법까지 체계적 1:1 지도."
tags:
  - 고양시
  - {gu_name}
  - {dong_name}
  - 고등영어
  - 영어과외
  - 내신관리
  - 수능대비
{chr(10).join([f'  - {s}' for s in schools_high])}
featured_image: "{image_path}"
---

{intro} 고양시 {gu_name} {dong_name}에서 고등학교 영어 과외를 찾고 계시다면, 내신과 수능을 모두 잡을 수 있는 맞춤형 수업이 필요합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
첫 수업에서 학생의 영어 실력을 종합 진단합니다. 문법, 어휘, 독해, 듣기 영역별 수준을 파악하고 맞춤 커리큘럼을 설계합니다.
</div>

## {section_title}

고등학교 영어는 중학교 때와 비교할 수 없이 어려워집니다. 지문의 길이와 난이도가 급격히 올라가고, 다루는 주제도 다양해집니다. 수능 영어에서는 추상적인 내용의 지문도 많이 출제됩니다.

{dong_name} 지역 {high_schools} 학생들은 내신과 수능을 모두 대비해야 합니다. 학교 시험은 교과서 위주로 출제되지만, 수능은 EBS 연계와 비연계 지문이 섞여 나옵니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
내신과 수능의 차이점을 명확히 알려드립니다. 두 가지를 효율적으로 병행하는 전략을 세웁니다.
</div>

## {schools_high[0]} 영어 시험의 특징

{schools_high[0]}의 영어 내신 시험은 교과서 지문에 대한 깊은 이해를 요구합니다. 단순 해석이 아니라 지문의 논리 구조, 필자의 의도, 어휘의 함축적 의미까지 파악해야 합니다.

서술형 문제에서는 영작 능력도 평가합니다. 문법적으로 정확하고 의미가 통하는 문장을 쓸 수 있어야 합니다. 내신에서 좋은 성적을 받으려면 교과서를 철저히 분석해야 합니다.

{reading_desc}

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
교과서 지문을 문장 단위로 분석합니다. 핵심 어휘, 문법 포인트, 논리 구조를 정리하고 관련 문제를 풀어봅니다.
</div>

## 수능 영어 대비

수능 영어는 2018년부터 절대평가로 바뀌었지만, 1등급 비율이 낮아 여전히 어렵습니다. 특히 빈칸 추론, 순서 배열, 문장 삽입 문제는 많은 학생들이 어려워합니다.

수능 영어 1등급을 받으려면 독해 속도와 정확도를 모두 갖춰야 합니다. 70분 안에 45문제를 풀어야 하므로 시간 관리 능력도 중요합니다.

{study_tip}

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
수능 기출문제를 유형별로 분석합니다. 각 유형별 접근법과 시간 배분 전략을 훈련합니다.
</div>

## 1:1 과외의 장점

학원에서는 정해진 진도에 맞춰 수업이 진행됩니다. 이미 아는 내용도 다시 듣고, 모르는 내용은 충분히 이해하지 못한 채 넘어가기 쉽습니다.

1:1 과외는 학생의 현재 수준에서 출발합니다. 부족한 부분을 집중적으로 보강하고, 이미 아는 내용은 빠르게 넘어갑니다. 시간을 효율적으로 사용할 수 있습니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
학생의 약점을 파악하여 집중 훈련합니다. 문법이 약하면 문법을, 독해가 약하면 독해를 보강합니다.
</div>

## 학년별 학습 전략

고1은 고등 영어의 기초를 다지는 시기입니다. 중학교 때 배운 문법을 복습하고, 고등 수준의 어휘를 확장해야 합니다. 독해 지문도 점점 길어지므로 읽기 속도를 높이는 연습이 필요합니다. 매일 영어 지문 1~2개를 읽는 습관을 들이면 좋습니다.

고2는 수능 영어의 핵심 유형을 익히는 시기입니다. 빈칸 추론, 순서 배열, 문장 삽입 등 어려운 유형의 접근법을 배워야 합니다. EBS 교재로 수능 대비를 본격화합니다. 모의고사를 통해 실전 감각도 키워야 합니다.

고3은 실전 감각을 키우는 시기입니다. 실제 시험처럼 시간을 재고 모의고사를 풀면서 시간 관리 능력을 키웁니다. 약점 유형은 집중 훈련합니다. 특히 6월과 9월 모의고사 결과를 분석하여 약점을 보완해야 합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
학년별 목표에 맞춰 커리큘럼을 구성합니다. 내신과 수능 비중을 조절하여 최적의 학습 계획을 세웁니다.
</div>

## 효과적인 영어 학습법

영어 실력은 단기간에 오르지 않습니다. 매일 꾸준히 공부하는 것이 가장 중요합니다. 단어, 문법, 독해를 균형 있게 학습하고, 취약 유형은 반복 훈련해야 합니다.

수능 영어에서 고득점을 받으려면 지문을 빠르고 정확하게 읽는 능력이 필수입니다. 매일 영어 지문을 읽으면서 읽기 속도를 높이세요.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
효율적인 독해 전략을 알려드립니다. 지문 유형별로 접근 방법이 다르므로 각각의 전략을 훈련합니다.
</div>

## 수업료 안내

{PRICING["high_english"]}

수업료는 학생의 현재 수준, 목표, 수업 방식에 따라 달라질 수 있습니다. 정확한 수업료는 상담을 통해 안내드립니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
첫 상담에서 학생의 현재 상황과 목표를 파악합니다. 최적의 수업 계획과 예상 수업료를 안내드립니다.
</div>

{{{{< cta-dual type="final" >}}}}

## 부모님께 드리는 말씀

자녀의 영어 성적이 걱정되신다면, 지금이 바로 변화의 시작점입니다. 영어는 대입에서 수학 다음으로 중요한 과목입니다. 영어 성적에 따라 지원할 수 있는 대학이 달라집니다.

1:1 과외는 학원과 달리 학생 개인에게 집중합니다. 어디서 막히는지 정확히 파악하고, 그 부분을 집중적으로 보완합니다. 학생의 성향과 학습 스타일에 맞춘 맞춤형 수업이 가능합니다.

상담은 부담 없이 받으실 수 있습니다. 현재 학생의 상황을 파악하고, 어떤 방향으로 학습을 진행하면 좋을지 함께 고민해드립니다.

## 자주 묻는 질문

**Q. 내신과 수능 중 어떤 것을 먼저 준비해야 하나요?**

고1~2는 내신 위주로 공부하면서 수능 기초를 다지고, 고3은 내신과 수능을 병행합니다. 학생 상황에 따라 비중을 조절합니다.

**Q. 영어 독해 속도가 너무 느려요.**

매일 꾸준히 영어 지문을 읽는 연습을 합니다. 처음에는 정확하게, 점차 빠르게 읽는 훈련을 합니다. 시간을 재고 읽는 연습도 필요합니다.

**Q. 어휘력이 부족한데 어떻게 해야 하나요?**

매일 일정량의 단어를 외우는 습관을 들입니다. 문맥에서 어휘를 익히면 오래 기억됩니다. 어근과 접두사를 활용하면 효율적입니다.

**Q. 수능 영어 1등급 받을 수 있을까요?**

현재 수준과 노력에 따라 다릅니다. 체계적으로 준비하면 충분히 가능합니다. 꾸준함이 가장 중요합니다.

**Q. 듣기 실력도 향상시킬 수 있나요?**

물론입니다. 듣기 훈련 방법을 알려드리고 필요시 수업에서 함께 연습합니다. 듣기 평가 만점은 1등급의 기본입니다.

**Q. 내신 시험 대비는 어떻게 하나요?**

시험 2~3주 전부터 교과서 완벽 분석과 예상 문제 풀이로 집중 대비합니다. 학교 선생님의 출제 스타일도 분석합니다.

**Q. EBS 연계율이 낮아졌는데 어떻게 대비하나요?**

EBS 교재의 주제와 소재를 익히는 것이 중요합니다. 비연계 지문에 대비한 독해력 향상도 병행합니다.

**Q. 수업 횟수는 어떻게 정하나요?**

학생의 현재 수준과 목표에 따라 상담 후 결정합니다. 보통 주1회 또는 주2회로 진행하며, 시험 기간에는 추가 수업도 가능합니다.

**Q. 학원과 과외를 병행해도 되나요?**

가능합니다. 다만 학습량이 과도해지지 않도록 조율이 필요합니다. 상담 시 현재 학습 상황을 말씀해주시면 적절한 방향을 안내드립니다.

## 마무리

{dong_name} 고등학생 여러분, 영어는 꾸준함이 답입니다. {high_schools} 내신과 수능에 맞춘 체계적인 수업으로 영어 실력을 키워보세요. {ending}
"""
    return content


def create_goyang_content():
    """고양시 전체 콘텐츠 생성"""
    base_dir = "/home/user/edu-guide/content/gyeonggi/goyang"

    # 기존 시 단위 파일 백업 경로 (필요시)
    file_count = 0
    variation_counter = 0

    for gu_key, gu_data in GOYANG_DATA.items():
        gu_name = gu_data["name_kr"]

        for dong_key, dong_data in gu_data["dongs"].items():
            dong_name = dong_data["name"]
            schools_middle = dong_data["middle"]
            schools_high = dong_data["high"]

            # 폴더 생성
            dong_dir = os.path.join(base_dir, dong_key)
            os.makedirs(dong_dir, exist_ok=True)

            # _index.md 생성
            index_content = f"""---
title: "고양시 {gu_name} {dong_name} 과외"
description: "고양시 {gu_name} {dong_name} 지역 중등/고등 수학·영어 과외 정보"
---

고양시 {gu_name} {dong_name} 지역의 과외 정보를 안내합니다.
"""
            with open(os.path.join(dong_dir, "_index.md"), 'w', encoding='utf-8') as f:
                f.write(index_content)

            # 4개 파일 생성 (중등수학, 중등영어, 고등수학, 고등영어)
            files_to_create = [
                ("middle-math.md", generate_middle_math_content),
                ("middle-english.md", generate_middle_english_content),
                ("high-math.md", generate_high_math_content),
                ("high-english.md", generate_high_english_content),
            ]

            for filename, generator in files_to_create:
                image_path = get_next_image()
                content = generator(gu_name, dong_name, schools_middle, schools_high, image_path, variation_counter)

                filepath = os.path.join(dong_dir, filename)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)

                file_count += 1
                variation_counter += 1

            print(f"Created: {dong_name} ({gu_name}) - 4 files")

    print(f"\nTotal files created: {file_count}")
    return file_count


if __name__ == "__main__":
    create_goyang_content()
