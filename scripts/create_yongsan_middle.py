#!/usr/bin/env python3
"""용산구 중등 수학/영어 과외 콘텐츠 생성 스크립트"""

import os

# 용산구 16개 동 정보
YONGSAN_DONGS = [
    {"id": "yongsan2ga", "name": "용산2가동", "schools": ["용산중", "보성여중"], "math_suffix": "내신 완벽 대비", "eng_suffix": "독해·문법 완성"},
    {"id": "hangang-ro", "name": "한강로동", "schools": ["용산중", "보성여중"], "math_suffix": "기초부터 심화까지", "eng_suffix": "영어 실력 향상"},
    {"id": "ichon1", "name": "이촌1동", "schools": ["용강중"], "math_suffix": "1:1 맞춤 수업", "eng_suffix": "내신·회화 병행"},
    {"id": "ichon2", "name": "이촌2동", "schools": ["용강중"], "math_suffix": "개념부터 실전까지", "eng_suffix": "체계적 영어 학습"},
    {"id": "itaewon1", "name": "이태원1동", "schools": ["오산중", "한강중"], "math_suffix": "학교별 맞춤 전략", "eng_suffix": "내신 집중 관리"},
    {"id": "itaewon2", "name": "이태원2동", "schools": ["오산중", "한강중"], "math_suffix": "수학 실력 완성", "eng_suffix": "독해력 강화"},
    {"id": "hannam", "name": "한남동", "schools": ["오산중", "한강중"], "math_suffix": "개인 맞춤 커리큘럼", "eng_suffix": "문법·어휘 완성"},
    {"id": "bogwang", "name": "보광동", "schools": ["오산중"], "math_suffix": "내신 1등급 목표", "eng_suffix": "영어 내신 특화"},
    {"id": "seobinggo", "name": "서빙고동", "schools": ["한강중"], "math_suffix": "체계적 학습 관리", "eng_suffix": "기초부터 탄탄하게"},
    {"id": "hyochang", "name": "효창동", "schools": ["선린중", "성심여중"], "math_suffix": "개념 완성 수업", "eng_suffix": "내신 만점 전략"},
    {"id": "cheongpa", "name": "청파동", "schools": ["신광여중"], "math_suffix": "학교 시험 완벽 대비", "eng_suffix": "독해·문법 마스터"},
    {"id": "namyeong", "name": "남영동", "schools": ["신광여중", "선린중"], "math_suffix": "맞춤형 진도 관리", "eng_suffix": "영어 기초 완성"},
    {"id": "wonhyoro1", "name": "원효로1동", "schools": ["선린중"], "math_suffix": "수학 자신감 향상", "eng_suffix": "회화·문법 병행"},
    {"id": "wonhyoro2", "name": "원효로2동", "schools": ["성심여중"], "math_suffix": "기초 개념 강화", "eng_suffix": "내신 고득점 비결"},
    {"id": "yongmun", "name": "용문동", "schools": ["선린중", "성심여중"], "math_suffix": "단계별 실력 향상", "eng_suffix": "체계적 문법 학습"},
    {"id": "huam", "name": "후암동", "schools": ["용산중", "보성여중"], "math_suffix": "개별 맞춤 지도", "eng_suffix": "영어 실력 도약"},
]

# 16개 고유한 수학 인트로
MATH_INTROS = [
    ("수학, 개념이 흔들리면 다 무너집니다", "중학교 수학은 고등 수학의 기초입니다. 지금 개념을 확실히 잡아야 합니다."),
    ("수학 성적, 왜 제자리일까요?", "열심히 하는데 성적이 안 오른다면, 방법이 잘못된 겁니다."),
    ("중학교 수학, 공식 암기로는 부족합니다", "진짜 수학 실력은 원리 이해에서 시작됩니다."),
    ("수학을 포기하기엔 아직 이릅니다", "중학교 때 잡으면 고등학교 수학이 쉬워집니다."),
    ("수학, 기초부터 다시 시작해볼까요?", "어디서부터 막히는지 정확히 찾아 해결해 드립니다."),
    ("내 아이 수학, 왜 안 오를까요?", "문제는 공부량이 아니라 공부법에 있습니다."),
    ("수학 자신감, 되찾을 수 있습니다", "작은 성공 경험이 쌓이면 수학이 재밌어집니다."),
    ("중학교 수학이 어렵다고요?", "사실 중학교 수학은 패턴만 익히면 쉬워집니다."),
    ("수학 때문에 고민이신가요?", "지금 제대로 잡으면 고등학교 가서 빛을 봅니다."),
    ("수학, 개념 없이 문제만 풀면 한계가 옵니다", "개념부터 차근차근 쌓아가는 수업을 합니다."),
    ("수학 점수, 더 올릴 수 있습니다", "학생에게 맞는 전략으로 효율적으로 올려드립니다."),
    ("수학, 어디서부터 손대야 할지 모르겠다면", "정확한 진단으로 부족한 부분만 집중 보완합니다."),
    ("중학교 수학, 지금이 골든타임입니다", "고등학교 가기 전에 반드시 완성해야 합니다."),
    ("수학, 학원만 다녀서는 안 됩니다", "1:1 맞춤 수업이 확실히 다릅니다."),
    ("수학 기초가 부족하다고 느끼신다면", "처음부터 다시, 확실하게 잡아드립니다."),
    ("수학 성적 향상의 비결이 있습니다", "학생별 취약점을 정확히 파악하는 것이 시작입니다."),
]

# 16개 고유한 영어 인트로
ENG_INTROS = [
    ("영어, 문법이 약하면 독해도 안 됩니다", "기초 문법부터 확실히 잡아야 영어가 늡니다."),
    ("영어 성적이 정체되어 있나요?", "방법을 바꾸면 결과도 달라집니다."),
    ("중학교 영어, 지금 잡아야 합니다", "고등학교 영어는 중학교의 연장선입니다."),
    ("영어 단어만 외워서는 한계가 있습니다", "문장 속에서 단어를 익혀야 진짜 실력입니다."),
    ("영어, 어디서부터 시작해야 할지 모르겠다면", "실력에 맞는 커리큘럼으로 시작합니다."),
    ("영어 독해가 어렵다고요?", "문장 구조를 이해하면 독해가 쉬워집니다."),
    ("영어 자신감을 키워드립니다", "작은 성취가 쌓여 큰 실력이 됩니다."),
    ("중학교 영어, 내신이 중요합니다", "학교별 출제 경향을 정확히 파악해 대비합니다."),
    ("영어, 기초부터 다시 해볼까요?", "부족한 부분만 정확히 채워드립니다."),
    ("영어 문법, 어렵지 않습니다", "원리를 이해하면 쉽게 적용할 수 있습니다."),
    ("영어 점수 향상, 방법이 있습니다", "학생에게 맞는 전략으로 접근합니다."),
    ("내 아이 영어, 왜 늘지 않을까요?", "공부량보다 공부법이 중요합니다."),
    ("영어, 학원만으로 부족하다면", "1:1 맞춤 수업이 확실히 다릅니다."),
    ("중학교 영어 내신, 확실히 잡아드립니다", "시험 유형별 완벽 대비가 가능합니다."),
    ("영어 실력, 지금 바꿀 수 있습니다", "체계적인 학습으로 한 단계 업그레이드합니다."),
    ("영어, 포기하기엔 아직 이릅니다", "중학교 때 잡으면 고등학교가 편해집니다."),
]

# 이미지 풀 (용산구용 - 중복 최소화)
IMAGES = [
    "photo-1522202176988-66273c2fd55f",
    "photo-1523240795612-9a054b0db644",
    "photo-1517842645767-c639042777db",
    "photo-1513258496099-48168024aec0",
    "photo-1427504494785-3a9ca7044f45",
    "photo-1571260899304-425eee4c7efc",
    "photo-1519406596751-0a3ccc4937fe",
    "photo-1524178232363-1fb2b075b655",
    "photo-1509062522246-3755977927d7",
    "photo-1544717305-2782549b5136",
    "photo-1544717301-9cdcb1f5940f",
    "photo-1529390079861-591de354faf5",
    "photo-1501504905252-473c47e087f8",
    "photo-1509869175650-a1d97972541a",
    "photo-1528980917907-8df7f48f6f2a",
    "photo-1525921429624-479b6a26d84d",
    "photo-1588072432836-e10032774350",
    "photo-1588702547923-7093a6c3ba33",
    "photo-1587691592099-24045742c181",
    "photo-1580894906475-403935091be2",
    "photo-1573497019940-1c28c88b4f3e",
    "photo-1573496359142-b8d87734a5a2",
    "photo-1573497019236-17f8177b81e8",
    "photo-1573497161161-c3e73707e25c",
    "photo-1577896851231-70ef18881754",
    "photo-1578574577315-3fbeb0cecdc2",
    "photo-1580582932707-520aed937b7b",
    "photo-1580894732444-8ecded7900cd",
    "photo-1580894908361-967195033215",
    "photo-1581078426770-6d336e5de7bf",
    "photo-1582719478250-c89cae4dc85b",
    "photo-1584697964358-3e14ca57658b",
]


def generate_math_content(dong, idx):
    """수학 콘텐츠 생성"""
    intro_title, intro_text = MATH_INTROS[idx % len(MATH_INTROS)]
    schools = "·".join(dong["schools"])
    image = IMAGES[idx % len(IMAGES)]

    content = f'''---
title: "용산구 {dong["name"]} 중등 수학과외 | {schools} {dong["math_suffix"]}"
date: 2025-05-15
categories:
  - 중등교육
  - 수학
regions:
  - 서울
  - 용산구
  - {dong["name"]}
tags:
  - 용산구수학과외
  - {dong["name"]}수학과외
  - 중학교수학
  - {dong["schools"][0]}
  - 수학내신
  - 중등수학과외
description: "용산구 {dong["name"]} 중학생을 위한 수학과외입니다. {schools} 내신 대비와 수학 실력 향상을 위한 1:1 맞춤 수업을 제공합니다."
featured_image: "https://images.unsplash.com/{image}?w=1200&h=630&fit=crop"
---

## {intro_title}

{intro_text} 용산구 {dong["name"]} 중학생들을 위한 맞춤형 수학 과외를 소개합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
첫 수업에서 학생의 현재 실력을 정밀하게 파악합니다. 어떤 개념이 약하고, 어떤 유형에서 실수가 나는지 진단한 후 맞춤 커리큘럼을 설계합니다.
</div>

## 중학교 수학, 왜 어려워질까요?

중학교 수학은 초등학교와 확실히 다릅니다. 문자와 식, 함수, 기하 등 추상적 개념이 본격적으로 등장합니다. 단순 계산에서 논리적 사고로의 전환이 필요한 시기입니다.

특히 {dong["name"]} 학생들이 다니는 {schools} 등의 학교에서는 서술형 평가 비중이 높아지고 있습니다. 단순히 답만 맞히는 것이 아니라, 풀이 과정을 논리적으로 서술하는 능력이 필요합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
서술형 문제 대비를 위해 풀이 과정 작성법을 체계적으로 지도합니다. 논리적으로 글을 쓰는 훈련이 수학 실력 향상의 핵심입니다.
</div>

## {dong["name"]} 지역 중학교 수학 특징

### {dong["schools"][0]} 수학 내신

{dong["schools"][0]}은 용산구 내에서도 내신 관리가 중요한 학교입니다. 중간·기말고사 출제 경향을 파악하고, 기출 유형을 분석하여 시험에 완벽히 대비합니다.

시험 2주 전부터는 실전 모의고사를 통해 시간 관리 능력과 실전 감각을 키웁니다. 자주 출제되는 유형을 반복 학습하여 실수를 최소화합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
학교별 기출문제를 철저히 분석합니다. 선생님별 출제 스타일까지 파악하여 시험에 나올 문제를 예측하고 대비합니다.
</div>

## 수학 과외가 필요한 이유

학원 수업은 정해진 커리큘럼으로 진행됩니다. 내가 이미 아는 내용도 듣고, 모르는 부분은 빠르게 지나갈 수 있습니다. 1:1 과외는 다릅니다.

학생이 모르는 부분만 집중적으로 공략합니다. 이미 아는 내용은 빠르게 확인만 하고, 취약한 단원에 시간을 투자합니다. 이것이 효율적인 공부법입니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
매 수업마다 오답 노트를 함께 정리합니다. 틀린 문제의 유형과 실수 패턴을 분석하여 같은 실수를 반복하지 않도록 훈련합니다.
</div>

## 학년별 수학 학습 전략

### 중1 수학

중1은 수학적 사고의 기초를 다지는 시기입니다. 정수와 유리수, 문자와 식, 방정식의 개념을 확실히 잡아야 합니다. 이 개념들이 중2, 중3 수학의 기초가 됩니다.

### 중2 수학

중2는 수학이 본격적으로 어려워지는 시기입니다. 일차함수, 연립방정식, 도형의 성질 등 추상적 개념이 많아집니다. 이 시기에 흔들리면 중3, 고등학교 수학까지 영향을 미칩니다.

### 중3 수학

중3은 고등학교 수학을 준비하는 시기입니다. 이차함수, 피타고라스 정리, 삼각비 등 고등학교 수학과 직결되는 개념을 배웁니다. 특히 이차함수는 고등학교 수학의 핵심이므로 완벽히 이해해야 합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
학년별, 단원별 핵심 개념을 명확히 정리합니다. 개념 이해 후에는 다양한 유형의 문제를 풀며 응용력을 키웁니다.
</div>

## 용산구 {dong["name"]} 중등 수학 과외 비용

수학 과외 비용은 수업 횟수와 시간에 따라 달라집니다.

**중1~2**는 주1회 기준 18만원에서 25만원, 주2회 기준 32만원에서 45만원 선입니다.

**중3**은 주1회 기준 20만원에서 28만원, 주2회 기준 36만원에서 50만원이 일반적입니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
첫 상담에서 학생의 목표와 현재 실력을 파악한 후, 최적의 수업 횟수와 시간을 제안해 드립니다. 무리한 스케줄보다 효율적인 학습이 중요합니다.
</div>

## 자주 묻는 질문

**Q. 수학 기초가 많이 부족한데 따라갈 수 있을까요?**

기초가 부족할수록 1:1 과외가 효과적입니다. 어디서부터 막히는지 정확히 진단하고, 그 부분부터 차근차근 다시 시작합니다. 기초를 탄탄히 쌓으면 이후 진도도 빨라집니다.

**Q. 내신 대비와 선행 학습 중 뭐가 더 중요한가요?**

현재 학년 내신이 우선입니다. 내신이 불안정한 상태에서 선행을 하면 오히려 둘 다 놓칠 수 있습니다. 내신을 확실히 잡은 후에 선행을 진행하는 것이 효율적입니다.

**Q. 일주일에 몇 번 수업이 적당한가요?**

학생 상황에 따라 다르지만, 보통 주2회를 권장합니다. 주1회는 복습 기간이 길어져 학습 효과가 떨어질 수 있고, 주3회 이상은 학생 부담이 클 수 있습니다.

{{< cta-dual type="final" >}}

## 마무리

용산구 {dong["name"]} 중학생 여러분, 수학은 올바른 방법으로 공부하면 반드시 성적이 오릅니다. 지금 시작하면 늦지 않았습니다. 함께 수학 실력을 키워나가요.
'''
    return content


def generate_english_content(dong, idx):
    """영어 콘텐츠 생성"""
    intro_title, intro_text = ENG_INTROS[idx % len(ENG_INTROS)]
    schools = "·".join(dong["schools"])
    image = IMAGES[(idx + 16) % len(IMAGES)]

    content = f'''---
title: "용산구 {dong["name"]} 중등 영어과외 | {schools} {dong["eng_suffix"]}"
date: 2025-05-15
categories:
  - 중등교육
  - 영어
regions:
  - 서울
  - 용산구
  - {dong["name"]}
tags:
  - 용산구영어과외
  - {dong["name"]}영어과외
  - 중학교영어
  - {dong["schools"][0]}
  - 영어내신
  - 중등영어과외
description: "용산구 {dong["name"]} 중학생을 위한 영어과외입니다. {schools} 내신 대비와 영어 실력 향상을 위한 1:1 맞춤 수업을 제공합니다."
featured_image: "https://images.unsplash.com/{image}?w=1200&h=630&fit=crop"
---

## {intro_title}

{intro_text} 용산구 {dong["name"]} 중학생들을 위한 맞춤형 영어 과외를 소개합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
첫 수업에서 문법, 독해, 어휘력을 종합적으로 진단합니다. 어떤 부분이 약한지 파악한 후 맞춤형 학습 계획을 세웁니다.
</div>

## 중학교 영어, 무엇이 달라지나요?

중학교 영어는 초등학교와 차원이 다릅니다. 문법이 본격적으로 등장하고, 독해 지문의 길이와 난이도가 급격히 올라갑니다. 어휘량도 크게 늘어나 체계적인 학습이 필요합니다.

특히 {dong["name"]} 학생들이 다니는 {schools} 등에서는 영어 서술형 평가 비중이 높습니다. 문법 지식을 바탕으로 영작까지 할 수 있어야 좋은 성적을 받을 수 있습니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
서술형 대비를 위해 영작 연습을 체계적으로 진행합니다. 문법 규칙을 단순히 외우는 것이 아니라, 실제 문장에 적용하는 훈련을 합니다.
</div>

## {dong["name"]} 지역 중학교 영어 특징

### {dong["schools"][0]} 영어 내신

{dong["schools"][0]}의 영어 시험은 교과서 본문 이해와 문법 적용 능력을 중점적으로 평가합니다. 교과서 지문을 완벽히 이해하고, 변형 문제에도 대응할 수 있어야 합니다.

시험 전에는 교과서 본문 암기와 함께 다양한 변형 문제를 풀어봅니다. 예상 문제를 통해 실전 감각을 키우고, 시간 배분 연습도 함께 합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
학교별 기출문제를 분석하여 자주 나오는 유형을 파악합니다. 출제 경향에 맞춘 예상 문제로 시험에 완벽히 대비합니다.
</div>

## 영어 과외가 효과적인 이유

학원 수업은 여러 학생이 함께 듣기 때문에, 내 수준에 맞지 않을 수 있습니다. 이미 아는 내용을 반복하거나, 이해가 안 되는 부분을 그냥 넘어갈 수 있습니다.

1:1 과외는 오직 나만을 위한 수업입니다. 내가 모르는 부분만 집중적으로 배울 수 있어 시간 대비 효율이 높습니다. 질문도 편하게 할 수 있어 이해도가 높아집니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
매 수업 후 그날 배운 내용을 정리하고, 다음 수업 전까지 복습할 과제를 드립니다. 꾸준한 복습이 영어 실력 향상의 핵심입니다.
</div>

## 학년별 영어 학습 전략

### 중1 영어

중1은 영어 문법의 기초를 다지는 시기입니다. 8품사, 문장의 형식, 시제 등 핵심 문법을 확실히 잡아야 합니다. 이 기초가 탄탄해야 중2, 중3 문법을 소화할 수 있습니다.

### 중2 영어

중2는 문법이 본격적으로 복잡해지는 시기입니다. 준동사(to부정사, 동명사, 분사), 관계대명사, 비교급·최상급 등 중요한 문법이 쏟아집니다. 이 시기에 놓치면 고등학교까지 영향을 미칩니다.

### 중3 영어

중3은 고등학교 영어를 준비하는 시기입니다. 중학교 문법을 완벽히 정리하고, 고등학교 수준의 독해를 미리 연습합니다. 어휘력도 고등학교 수준으로 끌어올려야 합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
학년별 필수 문법을 체계적으로 정리합니다. 문법을 배운 후에는 실제 문장과 지문에서 적용하는 연습을 하여 진짜 실력으로 만듭니다.
</div>

## 용산구 {dong["name"]} 중등 영어 과외 비용

영어 과외 비용은 수업 횟수와 시간에 따라 달라집니다.

**중1~2**는 주1회 기준 17만원에서 24만원, 주2회 기준 30만원에서 42만원 선입니다.

**중3**은 주1회 기준 19만원에서 26만원, 주2회 기준 34만원에서 48만원이 일반적입니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
상담을 통해 학생의 현재 실력과 목표를 파악합니다. 그에 맞는 최적의 수업 횟수와 시간을 함께 결정합니다.
</div>

## 자주 묻는 질문

**Q. 영어 문법이 너무 약한데 따라갈 수 있을까요?**

문법이 약할수록 1:1 수업이 효과적입니다. 어디서부터 이해가 안 되는지 파악하고, 그 부분부터 차근차근 설명합니다. 기초 문법이 잡히면 이후 학습 속도도 빨라집니다.

**Q. 단어 암기가 안 되는데 어떻게 해야 하나요?**

단어를 문장 속에서 익히는 것이 효과적입니다. 예문과 함께 단어를 학습하면 기억에 오래 남고, 실제로 활용할 수 있는 어휘력이 됩니다.

**Q. 독해 지문을 읽는데 시간이 너무 오래 걸려요.**

독해 속도는 훈련으로 빨라집니다. 문장 구조를 파악하는 연습, 끊어 읽기 연습을 통해 점차 속도를 높여갑니다. 꾸준히 연습하면 반드시 빨라집니다.

{{< cta-dual type="final" >}}

## 마무리

용산구 {dong["name"]} 중학생 여러분, 영어는 꾸준함이 답입니다. 지금 시작해서 기초를 탄탄히 다지면 고등학교 영어도 두렵지 않습니다. 함께 영어 실력을 키워나가요.
'''
    return content


def main():
    base_dir = "/home/user/edu-guide/content/middle"
    os.makedirs(base_dir, exist_ok=True)

    created_files = []

    for idx, dong in enumerate(YONGSAN_DONGS):
        # 수학 파일 생성
        math_filename = f"yongsan-{dong['id']}-middle-math.md"
        math_path = os.path.join(base_dir, math_filename)
        math_content = generate_math_content(dong, idx)
        with open(math_path, 'w', encoding='utf-8') as f:
            f.write(math_content)
        created_files.append(math_filename)

        # 영어 파일 생성
        eng_filename = f"yongsan-{dong['id']}-middle-english.md"
        eng_path = os.path.join(base_dir, eng_filename)
        eng_content = generate_english_content(dong, idx)
        with open(eng_path, 'w', encoding='utf-8') as f:
            f.write(eng_content)
        created_files.append(eng_filename)

    print(f"총 {len(created_files)}개 파일 생성 완료!")
    for f in created_files:
        print(f"  - {f}")


if __name__ == "__main__":
    main()
