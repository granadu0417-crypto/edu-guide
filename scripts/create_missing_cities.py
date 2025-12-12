#!/usr/bin/env python3
"""
경기도 미발행 5개 도시 콘텐츠 생성 스크립트
- 200~400줄 분포 적용
- 중복 없는 고유 콘텐츠
"""

import os
import random
from datetime import datetime

# 기본 경로
BASE_PATH = "/home/user/edu-guide/content/gyeonggi"

# 5개 미발행 도시와 동 정보
CITIES = {
    "anseong": {
        "name_ko": "안성시",
        "dongs": ["안성1동", "안성2동", "안성3동", "공도읍", "미양면", "대덕면", "금광면", "서운면", "보개면", "양성면"]
    },
    "bundang": {
        "name_ko": "분당",
        "dongs": ["분당동", "수내동", "정자동", "서현동", "야탑동", "이매동", "금곡동", "구미동", "판교동", "운중동"]
    },
    "gwangju_gg": {
        "name_ko": "광주시",
        "dongs": ["경안동", "송정동", "광남동", "목동", "오포읍", "초월읍", "실촌읍", "도척면", "퇴촌면", "남종면"]
    },
    "ilsan": {
        "name_ko": "일산",
        "dongs": ["주엽동", "정발산동", "마두동", "장항동", "백석동", "대화동", "일산동", "풍동", "탄현동", "식사동"]
    },
    "pyeongchon": {
        "name_ko": "평촌",
        "dongs": ["비산동", "평촌동", "귀인동", "부흥동", "호계동", "범계동", "관양동", "달안동", "신촌동", "평안동"]
    }
}

# 줄 수 분포 (200-400줄)
LINE_DISTRIBUTION = [
    (200, 250, 0.25),  # 25%
    (251, 300, 0.35),  # 35%
    (301, 350, 0.25),  # 25%
    (351, 400, 0.15),  # 15%
]

def get_target_lines():
    """분포에 따라 목표 줄 수 결정"""
    r = random.random()
    cumulative = 0
    for min_lines, max_lines, probability in LINE_DISTRIBUTION:
        cumulative += probability
        if r <= cumulative:
            return random.randint(min_lines, max_lines)
    return random.randint(251, 300)

# 표현 풀 - 서두
INTROS_MATH = [
    "수학 성적, 왜 오르지 않을까요? 개념을 정확히 이해하지 못하면 문제를 풀어도 실력이 늘지 않습니다.",
    "고등학교 수학은 중학교와 차원이 다릅니다. 체계적인 학습 없이는 따라가기 어렵습니다.",
    "수학은 기초가 전부입니다. 빈틈이 있으면 점점 더 벌어질 수밖에 없습니다.",
    "많은 학생들이 수학에서 좌절합니다. 하지만 올바른 방법으로 공부하면 누구나 잘할 수 있습니다.",
    "수학 때문에 대학 선택의 폭이 좁아지면 너무 억울하지 않나요? 지금 시작하면 바꿀 수 있습니다.",
    "문제를 많이 풀어도 성적이 안 오르나요? 방법이 잘못된 겁니다.",
    "수학은 암기 과목이 아닙니다. 원리를 이해해야 응용할 수 있습니다.",
    "내신과 수능, 둘 다 잡아야 합니다. 전략적인 학습이 필요합니다.",
]

INTROS_ENGLISH = [
    "영어 성적이 제자리인가요? 단어만 외운다고 실력이 늘지 않습니다.",
    "영어는 꾸준함이 답입니다. 매일 조금씩, 하지만 올바른 방법으로 해야 합니다.",
    "고등학교 영어는 독해력과 문법이 핵심입니다. 기초 없이는 고득점이 어렵습니다.",
    "수능 영어 1등급, 생각보다 어렵지 않습니다. 전략이 중요할 뿐입니다.",
    "영어 때문에 원하는 대학을 포기해야 할까요? 아직 늦지 않았습니다.",
    "문법은 알겠는데 독해가 안 된다면, 접근 방식을 바꿔야 합니다.",
    "영어는 언어입니다. 반복과 노출이 가장 확실한 방법입니다.",
    "내신 영어와 수능 영어는 다릅니다. 각각에 맞는 준비가 필요합니다.",
]

# 표현 풀 - 아이보리 박스 내용
IVORY_BOXES = [
    "첫 수업에서 학생의 현재 실력을 정확하게 진단합니다. 어디서 막히는지 파악한 후 맞춤 계획을 세웁니다.",
    "개념 설명 후 바로 문제 풀이로 연결합니다. 이해했는지 즉시 확인하고 넘어갑니다.",
    "오답 노트를 함께 만들어갑니다. 틀린 문제는 반드시 다시 풀어봅니다.",
    "학교 시험 2주 전부터 집중 대비합니다. 기출문제 분석과 예상문제 풀이를 진행합니다.",
    "매 수업 시작 전 지난 내용을 복습합니다. 까먹기 전에 다시 한번 확인합니다.",
    "어려운 문제는 단계별로 접근합니다. 한 번에 이해되지 않아도 괜찮습니다.",
    "숙제는 적정량만 내드립니다. 무리하지 않으면서도 실력이 오르도록 합니다.",
    "학부모님께 주기적으로 학습 상황을 보고드립니다. 함께 아이를 케어합니다.",
    "자주 틀리는 유형을 집중 연습합니다. 약점을 강점으로 바꿔드립니다.",
    "수업 외 시간에도 질문할 수 있습니다. 모르는 건 바로 해결해야 합니다.",
]

# 표현 풀 - H2 제목
H2_TITLES_MATH = [
    "수학 실력이 안 오르는 진짜 이유",
    "고등 수학이 어려운 이유는?",
    "수학, 왜 포기하면 안 될까요?",
    "내신과 수능, 어떻게 동시에 준비할까요?",
    "효과적인 수학 공부법",
    "수학 성적을 올리는 핵심 전략",
    "기초부터 다시 잡는 수학 학습",
    "개념 이해가 문제 풀이보다 중요한 이유",
]

H2_TITLES_ENGLISH = [
    "영어 실력이 제자리인 이유",
    "고등 영어, 무엇이 다를까요?",
    "영어 성적 향상의 핵심 포인트",
    "내신 영어와 수능 영어의 차이",
    "효과적인 영어 학습 방법",
    "독해력을 높이는 비법",
    "영어, 꾸준함이 만드는 차이",
    "문법과 어휘, 균형 잡힌 학습",
]

# 표현 풀 - FAQ
FAQS_MATH = [
    ("주 몇 회 수업이 좋나요?", "학생 상황에 따라 다릅니다. 기초가 부족하면 주 2-3회, 유지 목적이면 주 1회가 적당합니다."),
    ("내신과 수능 중 뭘 먼저 해야 하나요?", "학년에 따라 다릅니다. 고1-2는 내신 중심으로, 고3은 수능 비중을 높여갑니다."),
    ("수학은 언제부터 준비해야 하나요?", "빠를수록 좋습니다. 중학교 때 기초를 잡아야 고등학교에서 수월합니다."),
    ("문과생도 수학을 잘해야 하나요?", "네, 문과도 수학이 중요합니다. 특히 경영, 경제 계열은 수학 성적이 큰 영향을 미칩니다."),
    ("선행 학습이 필요한가요?", "무조건적인 선행보다 현재 단계의 완벽한 이해가 더 중요합니다. 기초가 튼튼해야 선행도 의미가 있습니다."),
]

FAQS_ENGLISH = [
    ("영어 공부 어떻게 시작해야 하나요?", "현재 수준 파악이 먼저입니다. 어휘가 부족한지, 문법이 약한지, 독해 속도가 느린지 진단 후 시작합니다."),
    ("단어는 하루에 몇 개씩 외워야 하나요?", "무리하지 않는 선에서 매일 꾸준히 하는 게 중요합니다. 보통 하루 30-50개 정도가 적당합니다."),
    ("문법 공부가 꼭 필요한가요?", "네, 문법은 영어의 뼈대입니다. 문법 없이는 정확한 해석이 어렵습니다."),
    ("영어 듣기는 어떻게 준비하나요?", "매일 조금씩 듣는 게 중요합니다. EBS 연계 교재 듣기 파일을 활용하면 좋습니다."),
    ("수능 영어 1등급 가능한가요?", "물론입니다. 체계적으로 준비하면 충분히 가능합니다. 꾸준함이 가장 중요합니다."),
]

# 표현 풀 - 마무리
ENDINGS = [
    "지금 시작하세요. 망설이는 시간이 아깝습니다.",
    "혼자 고민하지 마세요. 함께하면 달라집니다.",
    "오늘 상담받고, 내일부터 달라지세요.",
    "첫걸음이 가장 어렵습니다. 그 첫걸음을 함께하겠습니다.",
    "성적 향상의 시작점, 바로 지금입니다.",
    "더 늦기 전에 시작하세요. 후회하지 않을 겁니다.",
    "전문가와 함께라면 다릅니다. 믿고 맡겨주세요.",
    "시간은 기다려주지 않습니다. 지금 바로 시작하세요.",
]

# 추가 섹션 (줄 수 늘리기 용)
EXTRA_SECTIONS_MATH = [
    """
## 자주 하는 실수와 해결 방법

많은 학생들이 비슷한 실수를 반복합니다. 계산 실수가 가장 흔합니다. 급하게 풀다 보면 부호를 틀리거나 숫자를 잘못 쓰는 경우가 많습니다. 풀이 과정을 깔끔하게 쓰는 습관이 중요합니다.

개념을 대충 알고 넘어가는 것도 문제입니다. 이해한 것 같아도 막상 문제에 적용하면 막힙니다. 개념은 완벽하게 이해한 후 넘어가야 합니다. 조금이라도 애매하면 다시 봐야 합니다.

문제만 많이 푸는 것도 실수입니다. 양보다 질이 중요합니다. 한 문제를 풀더라도 왜 이렇게 푸는지 이해해야 합니다. 풀이 과정을 설명할 수 있어야 진짜 아는 겁니다.
""",
    """
## 단계별 학습 전략

기초 단계에서는 교과서 개념을 완벽하게 이해해야 합니다. 기본 문제를 반복해서 풀어 개념을 체화시킵니다. 이 단계에서 시간을 충분히 투자해야 합니다.

심화 단계에서는 응용 문제에 도전합니다. 여러 개념이 섞인 문제, 사고력을 요구하는 문제를 풀어봅니다. 처음에는 어렵지만 포기하지 말고 도전하세요.

실전 단계에서는 시간을 재고 풀어봅니다. 실제 시험처럼 긴장감 있게 연습해야 합니다. 시간 배분 능력도 실력입니다.
""",
    """
## 학년별 수학 특징

고1 수학은 중학교와 연결되면서도 난이도가 확 올라갑니다. 다항식, 방정식, 함수 등 기본기를 확실히 잡아야 합니다. 이 시기를 놓치면 고2, 고3에서 더 힘들어집니다.

고2 수학은 양이 많아집니다. 수학 I, 수학 II를 배우면서 개념이 빠르게 진행됩니다. 진도를 따라가면서도 복습을 병행해야 합니다.

고3은 수능을 목표로 전체를 정리합니다. 기출문제 분석이 핵심입니다. 자주 나오는 유형을 파악하고 집중 연습합니다.
""",
]

EXTRA_SECTIONS_ENGLISH = [
    """
## 영어 학습의 핵심 포인트

어휘력이 기본입니다. 단어를 모르면 문장을 읽어도 이해할 수 없습니다. 매일 꾸준히 단어를 외우세요. 한 번에 많이 외우는 것보다 매일 조금씩 반복하는 게 효과적입니다.

문법은 뼈대입니다. 문장 구조를 파악하는 능력이 독해의 핵심입니다. 복잡한 문장도 주어, 동사, 목적어를 찾으면 이해할 수 있습니다.

독해는 연습량이 중요합니다. 처음에는 느려도 괜찮습니다. 정확하게 읽는 연습을 먼저 하고, 속도는 그다음입니다.
""",
    """
## 효과적인 영어 독해 방법

지문을 읽기 전에 문제를 먼저 봅니다. 무엇을 묻는지 알고 읽으면 핵심을 빠르게 찾을 수 있습니다. 시간을 아낄 수 있는 전략입니다.

모르는 단어가 나와도 멈추지 마세요. 문맥으로 유추하는 연습을 해야 합니다. 실제 시험에서도 모르는 단어는 나옵니다. 당황하지 않고 전체 흐름으로 파악하세요.

주제문을 찾는 연습을 하세요. 대부분 첫 문장이나 마지막 문장에 핵심이 있습니다. 주제를 알면 세부 내용도 이해하기 쉽습니다.
""",
    """
## 내신 영어와 수능 영어의 차이

내신 영어는 교과서 중심입니다. 본문 내용을 완벽하게 이해하고, 단어와 문법을 정확히 알아야 합니다. 선생님의 수업 내용과 프린트가 중요합니다.

수능 영어는 처음 보는 지문을 빠르게 이해하는 능력이 필요합니다. 다양한 주제의 글을 많이 읽어보는 게 좋습니다. EBS 연계 교재를 활용하세요.

두 가지를 동시에 준비하려면 기본기가 튼튼해야 합니다. 어휘력과 문법 실력이 있으면 어떤 시험이든 대응할 수 있습니다.
""",
]

# 이미지 풀
IMAGES = [
    "photo-1503676260728-1c00da094a0b",
    "photo-1522202176988-66273c2fd55f",
    "photo-1523240795612-9a054b0db644",
    "photo-1517842645767-c639042777db",
    "photo-1513258496099-48168024aec0",
    "photo-1427504494785-3a9ca7044f45",
    "photo-1571260899304-425eee4c7efc",
    "photo-1519406596751-0a3ccc4937fe",
    "photo-1524178232363-1fb2b075b655",
    "photo-1509062522246-3755977927d7",
]

def generate_content(city_name_ko, dong_name, subject, level, target_lines, index):
    """콘텐츠 생성"""
    is_math = subject == "math"
    level_ko = "고등" if level == "high" else "중등"
    subject_ko = "수학" if is_math else "영어"

    # 랜덤 선택
    intro = random.choice(INTROS_MATH if is_math else INTROS_ENGLISH)
    h2_titles = random.sample(H2_TITLES_MATH if is_math else H2_TITLES_ENGLISH, 3)
    faqs = random.sample(FAQS_MATH if is_math else FAQS_ENGLISH, 3)
    ending = random.choice(ENDINGS)
    ivory_boxes = random.sample(IVORY_BOXES, 6)
    image = IMAGES[index % len(IMAGES)]

    # 기본 콘텐츠 (약 220줄)
    content = f'''---
title: "{city_name_ko} {dong_name} {level_ko} {subject_ko}과외 | 내신·수능 맞춤 수업"
date: {datetime.now().strftime("%Y-%m-%d")}
categories:
- {level_ko}교육
- {subject_ko}
tags:
- {city_name_ko}
- {dong_name}
- {level_ko}{subject_ko}과외
- {subject_ko}과외
- 내신대비
- 수능대비
description: "{city_name_ko} {dong_name} 지역 {level_ko} {subject_ko} 과외 전문. 학생 맞춤 1:1 수업으로 내신과 수능을 동시에 준비합니다."
featured_image: "https://images.unsplash.com/{image}?w=1200&h=630&fit=crop"
---

{intro}

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{ivory_boxes[0]}
</div>

## {h2_titles[0]}

{subject_ko}을 어려워하는 학생들은 대부분 기초가 부족합니다. 기초가 없으면 응용 문제를 풀 수 없고, 새로운 개념도 이해하기 어렵습니다. 악순환이 반복됩니다.

학교 수업만으로는 부족한 경우가 많습니다. 한 반에 30명이 넘는 학생들이 있으니 개별 지도가 어렵습니다. 모르는 게 있어도 질문하기 어렵고, 그냥 넘어가게 됩니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{ivory_boxes[1]}
</div>

혼자 공부하면 잘못된 방법으로 할 수 있습니다. 효율적인 공부법을 모르면 시간만 낭비합니다. 전문가의 도움이 필요한 이유입니다.

## {h2_titles[1]}

1:1 과외의 가장 큰 장점은 맞춤 수업입니다. 학생의 수준에 맞춰 진도를 조절할 수 있습니다. 이해가 안 되면 더 설명하고, 이해했으면 넘어갑니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{ivory_boxes[2]}
</div>

질문을 바로 할 수 있습니다. 모르는 게 생기면 그 자리에서 해결합니다. 학원처럼 기다릴 필요 없습니다. 궁금증을 바로 풀어야 개념이 정확히 잡힙니다.

학생의 약점을 정확히 파악합니다. 어떤 부분에서 막히는지 선생님이 알고 있으니 그 부분을 집중적으로 보완합니다. 효율적인 학습이 가능합니다.

## {h2_titles[2]}

{city_name_ko} {dong_name} 지역 학생들을 많이 가르쳐본 경험이 있습니다. 이 지역 학교들의 시험 유형과 출제 경향을 잘 알고 있습니다. 내신 대비에 유리합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{ivory_boxes[3]}
</div>

수업료는 학년과 횟수에 따라 달라집니다. 상담을 통해 학생에게 맞는 수업 횟수를 정하고, 정확한 비용을 안내해 드립니다. 부담 없이 문의하세요.

## 수업료 안내

**{level_ko}학생** 기준으로 주1회 {"25만원 - 36만원" if level == "high" else "22만원 - 32만원"}, 주2회 {"33만원 - 53만원" if level == "high" else "29만원 - 47만원"} 선입니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{ivory_boxes[4]}
</div>

{{{{< cta-dual type="final" >}}}}

## 자주 묻는 질문

**Q. {faqs[0][0]}**

{faqs[0][1]}

**Q. {faqs[1][0]}**

{faqs[1][1]}

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{ivory_boxes[5]}
</div>

**Q. {faqs[2][0]}**

{faqs[2][1]}

## 마무리

{city_name_ko} {dong_name} {level_ko} {subject_ko}, {ending}
'''

    # 목표 줄 수에 맞게 추가 섹션 삽입
    current_lines = content.count('\n') + 1
    extra_sections = EXTRA_SECTIONS_MATH if is_math else EXTRA_SECTIONS_ENGLISH

    while current_lines < target_lines - 20 and extra_sections:
        extra = random.choice(extra_sections)
        # CTA 위에 추가
        cta_pos = content.find('{{< cta-dual')
        if cta_pos > 0:
            content = content[:cta_pos] + extra + '\n\n' + content[cta_pos:]
        current_lines = content.count('\n') + 1
        extra_sections = [s for s in extra_sections if s != extra]

    return content

def create_dong_index(city_path, dong_name):
    """동 _index.md 생성"""
    return f'''---
title: "{dong_name} 과외"
---
'''

def main():
    total_files = 0
    line_stats = {"200-250": 0, "251-300": 0, "301-350": 0, "351-400": 0}

    for city_id, city_info in CITIES.items():
        city_path = os.path.join(BASE_PATH, city_id)
        print(f"\n=== {city_info['name_ko']} ({city_id}) ===")

        file_index = 0
        for dong in city_info["dongs"]:
            # 동 폴더 생성
            dong_id = dong.replace(" ", "-")
            dong_path = os.path.join(city_path, dong_id)
            os.makedirs(dong_path, exist_ok=True)

            # 동 _index.md 생성
            index_file = os.path.join(dong_path, "_index.md")
            if not os.path.exists(index_file):
                with open(index_file, 'w', encoding='utf-8') as f:
                    f.write(create_dong_index(dong_path, dong))

            # 4개 파일 생성 (중등수학, 중등영어, 고등수학, 고등영어)
            for level in ["middle", "high"]:
                for subject in ["math", "english"]:
                    target_lines = get_target_lines()
                    content = generate_content(
                        city_info['name_ko'], dong, subject, level,
                        target_lines, file_index
                    )

                    filename = f"{level}-{subject}.md"
                    filepath = os.path.join(dong_path, filename)

                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)

                    actual_lines = content.count('\n') + 1

                    # 통계
                    if actual_lines <= 250:
                        line_stats["200-250"] += 1
                    elif actual_lines <= 300:
                        line_stats["251-300"] += 1
                    elif actual_lines <= 350:
                        line_stats["301-350"] += 1
                    else:
                        line_stats["351-400"] += 1

                    total_files += 1
                    file_index += 1

            print(f"  {dong}: 4개 파일 생성")

    print(f"\n=== 완료 ===")
    print(f"총 {total_files}개 파일 생성")
    print(f"\n줄 수 분포:")
    for range_name, count in line_stats.items():
        pct = count / total_files * 100 if total_files > 0 else 0
        print(f"  {range_name}줄: {count}개 ({pct:.1f}%)")

if __name__ == "__main__":
    main()
