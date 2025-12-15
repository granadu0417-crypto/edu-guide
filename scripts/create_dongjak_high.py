#!/usr/bin/env python3
"""동작구 고등 수학/영어 과외 콘텐츠 생성 스크립트"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 이미지 풀
MATH_IMAGES = [
    "photo-1635070041078-e363dbe005cb",
    "photo-1596495578065-6e0763fa1178",
    "photo-1509228468518-180dd4864904",
    "photo-1635070041409-e63e783ce3b1",
    "photo-1518133910546-b6c2fb7d79e3",
    "photo-1453733190371-0a9bedd82893",
    "photo-1596495577886-d920f1fb7238",
    "photo-1611532736597-de2d4265fba3",
    "photo-1580894894513-541e068a3e2b",
    "photo-1613909207039-6b173b755cc1",
    "photo-1559494007-9f5847c49d94",
    "photo-1544383835-bda2bc66a55d",
    "photo-1518435579668-52e6c59a9c85",
    "photo-1611329857570-f02f340e7378",
    "photo-1512314889357-e157c22f938d",
]

ENGLISH_IMAGES = [
    "photo-1457369804613-52c61a468e7d",
    "photo-1456513080510-7bf3a84b82f8",
    "photo-1546410531-bb4caa6b424d",
    "photo-1553877522-43269d4ea984",
    "photo-1515378791036-0648a3ef77b2",
    "photo-1519389950473-47ba0277781c",
    "photo-1523240795612-9a054b0db644",
    "photo-1488190211105-8b0e65b80b4e",
    "photo-1434030216411-0b793f4b4173",
    "photo-1455390582262-044cdead277a",
    "photo-1471107340929-a87cd0f5b5f3",
    "photo-1415369629372-26f2fe60c467",
    "photo-1447069387593-a5de0862481e",
    "photo-1476234251651-f353703a034d",
    "photo-1516321497487-e288fb19713f",
]

# 서두 표현
MATH_INTROS = [
    ("수학 성적이 떨어졌다면", "고등학교에 올라온 후 수학이 어려워졌나요?"),
    ("수학 때문에 대학이 걱정이라면", "고등학교 수학, 제대로 잡아야 대학이 보입니다."),
    ("수포자가 되기 전에", "수학을 포기하기엔 아직 이릅니다."),
    ("고등 수학이 막막하다면", "어디서부터 시작해야 할지 모르겠다면 함께 시작해요."),
    ("수학 1등급을 원한다면", "상위권 진입을 위한 수학 학습 전략이 필요합니다."),
    ("내신과 수능 둘 다 잡으려면", "내신과 수능, 두 마리 토끼를 한꺼번에 잡는 방법이 있습니다."),
    ("수학 실력이 오르지 않는다면", "열심히 하는데 성적이 안 오르는 이유가 있습니다."),
    ("개념이 흔들린다면", "개념을 제대로 잡으면 문제는 저절로 풀립니다."),
    ("킬러 문항이 막힌다면", "킬러 문항, 접근법을 알면 풀 수 있습니다."),
    ("수학 자신감을 되찾고 싶다면", "수학에 대한 두려움을 자신감으로 바꿔드립니다."),
]

ENGLISH_INTROS = [
    ("영어 성적이 오르지 않는다면", "영어 공부를 하는데 성적이 제자리인가요?"),
    ("수능 영어 1등급을 원한다면", "영어 1등급, 체계적인 전략이 필요합니다."),
    ("영어 때문에 대학이 걱정이라면", "영어가 발목을 잡으면 안 됩니다."),
    ("독해가 안 되는 이유를 모르겠다면", "독해력을 키우는 방법이 따로 있습니다."),
    ("문법이 헷갈린다면", "문법을 체계적으로 정리하면 독해가 됩니다."),
    ("어휘가 부족하다면", "효율적인 어휘 학습법을 알려드립니다."),
    ("내신과 수능 영어가 다르게 느껴진다면", "내신과 수능, 접근법을 다르게 해야 합니다."),
    ("영어 학습 방향을 모르겠다면", "지금 해야 할 영어 공부를 정확히 짚어드립니다."),
    ("영어 자신감이 없다면", "영어에 대한 자신감을 다시 찾아드립니다."),
    ("EBS 연계가 어렵다면", "EBS 교재 활용법을 제대로 알려드립니다."),
]

# 동작구 동별 정보 (15개 행정동)
DONGJAK_DONGS = [
    {"id": "noryangjin1", "name": "노량진1동", "schools": ["동작고", "경문고"], "math_suffix": "내신·수능 대비", "eng_suffix": "독해·문법 완성"},
    {"id": "noryangjin2", "name": "노량진2동", "schools": ["동작고", "경문고"], "math_suffix": "맞춤 커리큘럼", "eng_suffix": "1:1 맞춤 수업"},
    {"id": "heukseok", "name": "흑석동", "schools": ["동작고", "경문고"], "math_suffix": "기초부터 심화까지", "eng_suffix": "체계적 학습 관리"},
    {"id": "sangdo1", "name": "상도1동", "schools": ["동작고", "경문고"], "math_suffix": "학교별 내신 특화", "eng_suffix": "실력 향상 수업"},
    {"id": "sangdo2", "name": "상도2동", "schools": ["동작고", "경문고"], "math_suffix": "1:1 맞춤 수업", "eng_suffix": "기초부터 심화까지"},
    {"id": "sangdo3", "name": "상도3동", "schools": ["성남고", "영등포고"], "math_suffix": "개념부터 실전까지", "eng_suffix": "맞춤 커리큘럼"},
    {"id": "sangdo4", "name": "상도4동", "schools": ["성남고", "영등포고"], "math_suffix": "실력 향상 수업", "eng_suffix": "학교별 내신 특화"},
    {"id": "sadang1", "name": "사당1동", "schools": ["동작고", "경문고"], "math_suffix": "체계적 학습 관리", "eng_suffix": "내신·수능 대비"},
    {"id": "sadang2", "name": "사당2동", "schools": ["동작고", "경문고"], "math_suffix": "내신 + 수능 병행", "eng_suffix": "독해·문법 완성"},
    {"id": "sadang3", "name": "사당3동", "schools": ["동작고", "경문고"], "math_suffix": "개념완성 수업", "eng_suffix": "1:1 맞춤 수업"},
    {"id": "sadang4", "name": "사당4동", "schools": ["동작고", "경문고"], "math_suffix": "맞춤 커리큘럼", "eng_suffix": "체계적 학습 관리"},
    {"id": "sadang5", "name": "사당5동", "schools": ["동작고", "경문고"], "math_suffix": "기초부터 심화까지", "eng_suffix": "실력 향상 수업"},
    {"id": "daebang", "name": "대방동", "schools": ["성남고", "영등포고", "서울공업고"], "math_suffix": "학교별 내신 특화", "eng_suffix": "내신·수능 대비"},
    {"id": "sindaebang1", "name": "신대방1동", "schools": ["수도여고", "숭의여고"], "math_suffix": "1:1 맞춤 수업", "eng_suffix": "독해·문법 완성"},
    {"id": "sindaebang2", "name": "신대방2동", "schools": ["수도여고", "숭의여고"], "math_suffix": "개념부터 실전까지", "eng_suffix": "맞춤 커리큘럼"},
]

def get_school_list_text(schools):
    if len(schools) == 1:
        return schools[0]
    elif len(schools) == 2:
        return f"{schools[0]}·{schools[1]}"
    else:
        return "·".join(schools[:3])

def get_school_tags(schools):
    return "\n".join([f"  - {school}" for school in schools])

def create_dongjak_math_content(dong_info, index):
    dong_name = dong_info["name"]
    schools = dong_info["schools"]
    school_list = get_school_list_text(schools)
    school_tags = get_school_tags(schools)
    title_suffix = dong_info["math_suffix"]
    image = MATH_IMAGES[index % len(MATH_IMAGES)]
    intro_title, intro_detail = MATH_INTROS[index % len(MATH_INTROS)]

    school_sections = ""
    for i, school in enumerate(schools[:2]):
        if i == 0:
            if school == "동작고":
                school_sections += f"""
### {school} 수학 내신의 특징

{school}은 동작구 사당동에 위치한 공립 고등학교입니다. 교과서 중심의 출제와 함께 응용 문제가 포함됩니다. 수학 내신에서는 기본 개념 이해와 문제 풀이력이 고르게 필요합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{school} 기출문제를 철저히 분석합니다. 자주 출제되는 유형과 선생님별 스타일을 파악하여 내신에 맞춰 준비합니다.
</div>
"""
            elif school == "성남고":
                school_sections += f"""
### {school} 수학 내신의 특징

{school}은 대방동에 위치한 사립 고등학교입니다. 내신 시험 난이도가 높은 편이며, 심화 문제가 출제됩니다. 개념 이해뿐만 아니라 고난도 문제 풀이 능력이 요구됩니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{school} 내신 대비는 심화 문제 풀이에 중점을 둡니다. 기본 개념은 빠르게 정리하고, 고난도 문제에 시간을 투자합니다.
</div>
"""
            elif school == "수도여고":
                school_sections += f"""
### {school} 수학 내신의 특징

{school}은 신대방동에 위치한 여자 고등학교입니다. 내신 경쟁이 치열하며, 서술형 비중이 높습니다. 풀이 과정을 논리적으로 쓰는 연습이 필수입니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{school} 내신은 서술형 대비가 핵심입니다. 풀이 과정을 체계적으로 쓰는 연습을 집중적으로 합니다.
</div>
"""
            else:
                school_sections += f"""
### {school} 수학 내신의 특징

{school}은 동작구에 위치한 고등학교입니다. 교과서 기본 문제와 응용 문제가 균형 있게 출제됩니다. 내신에서 좋은 성적을 받으려면 기본기와 응용력을 모두 갖춰야 합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{school} 기출문제를 분석하여 출제 경향을 파악합니다. 자주 나오는 유형을 집중 연습합니다.
</div>
"""
        elif i == 1:
            if school == "경문고":
                school_sections += f"""
### {school} 수학 내신의 특징

{school}은 사당동에 위치한 사립 고등학교입니다. 내신 시험에서 계산력과 응용력을 함께 평가합니다. 교과서 예제를 변형한 문제가 자주 출제됩니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{school} 기출 유형을 철저히 분석합니다. 변형 문제에 대비할 수 있도록 다양한 문제를 풀어봅니다.
</div>
"""
            elif school == "영등포고":
                school_sections += f"""
### {school} 수학 내신의 특징

{school}은 대방동에 위치한 고등학교입니다. 기본에 충실한 출제 경향을 보이며, 교과서와 익힘책을 완벽히 소화하면 좋은 성적을 받을 수 있습니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{school} 내신은 교과서 중심으로 철저히 준비합니다. 교과서 예제와 익힘책 문제를 완벽히 풀 수 있도록 지도합니다.
</div>
"""
            elif school == "숭의여고":
                school_sections += f"""
### {school} 수학 내신의 특징

{school}은 신대방동에 위치한 여자 고등학교입니다. 내신 경쟁이 치열하며, 꼼꼼한 준비가 필요합니다. 실수를 줄이는 것이 고득점의 핵심입니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{school} 내신은 실수 관리가 중요합니다. 자주 하는 실수 유형을 파악하고, 반복 훈련으로 실수를 줄입니다.
</div>
"""
            else:
                school_sections += f"""
### {school} 수학 내신의 특징

{school}은 동작구에 위치한 고등학교입니다. 내신에서 기본 문제와 응용 문제가 골고루 출제됩니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{school} 기출문제를 분석하고, 취약 유형을 집중 보완합니다.
</div>
"""

    content = f'''---
title: "동작구 {dong_name} 고등 수학과외 | {school_list} {title_suffix}"
date: 2025-01-29
categories:
  - 고등교육
regions:
  - 서울
cities:
  - 동작구
description: "동작구 {dong_name} 고등학생 수학과외 전문. {school_list} 내신과 수능 맞춤 관리. 개념부터 심화까지 체계적 1:1 지도."
tags:
  - {dong_name}
  - 동작구
  - 고등수학
  - 수학과외
  - 내신관리
  - 수능수학
{school_tags}
  - 수학개념
  - 수학심화
  - 동작관악교육지원청
featured_image: "https://images.unsplash.com/{image}?w=1200&h=630&fit=crop"

---
## 동작구 {dong_name} 고등학생, {intro_title}

{intro_detail} {dong_name}에서 고등학생 자녀의 수학 성적 때문에 고민하시는 학부모님이 많습니다. 중학교 때까지는 잘했는데 고등학교에서 갑자기 어려워진 경우도 있고, 계속 수학이 어려웠던 경우도 있습니다.

1:1 맞춤 과외는 학생의 현재 상태를 정확히 진단하는 것에서 시작합니다. 어떤 개념이 부족한지, 어떤 유형에서 막히는지, 시험 시간 관리는 어떤지 파악합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
첫 수업에서 학생의 수학 실력을 꼼꼼히 진단합니다. 모의고사 성적, 내신 시험지를 분석하여 취약점을 파악하고 맞춤 학습 계획을 세웁니다.
</div>

## 고등학교 수학이 어려운 이유

고등학교 수학은 중학교 수학과 차원이 다릅니다. 중학교 때는 열심히 외우고 문제 많이 풀면 어느 정도 성적이 나왔습니다. 고등학교 수학은 그렇게 해서는 한계가 있습니다.

추상적인 개념이 등장하고, 개념 간 연결이 복잡해지며, 문제 하나에 여러 개념이 복합적으로 적용됩니다. 단순 암기와 반복 풀이로는 고득점이 어렵습니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
개념을 단순히 외우는 것이 아니라, 왜 그런지 원리를 이해하게 합니다. 원리를 알면 응용이 되고, 처음 보는 문제도 풀 수 있습니다.
</div>

## 수능 수학의 특징

### 킬러 문항의 존재

수능 수학에서 21번, 29번, 30번은 킬러 문항으로 불립니다. 이 세 문제가 1등급과 2등급을 가릅니다. 킬러 문항은 여러 개념을 복합적으로 적용해야 하고, 사고력이 필요합니다.

### 시간 압박

수능 수학은 100분 동안 30문제를 풀어야 합니다. 문제당 평균 3분 남짓입니다. 빠르고 정확하게 푸는 연습이 필수입니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
실전 시간 배분 연습을 합니다. 어느 문제에 얼마나 시간을 쓸지 전략을 세우고, 모의고사를 통해 실전 감각을 익힙니다.
</div>

{school_sections}

## 1:1 과외가 효과적인 이유

### 맞춤형 커리큘럼

학원은 정해진 진도를 나갑니다. 1:1 과외는 학생에게 필요한 내용만 집중합니다. 이미 아는 내용은 빠르게 넘어가고, 모르는 부분은 완벽히 이해할 때까지 설명합니다.

### 학교 내신 맞춤 대비

같은 개념이라도 학교마다 출제 스타일이 다릅니다. 1:1 과외는 학생이 다니는 학교의 기출문제를 분석하고, 그 학교 시험에 맞춰 대비합니다.

### 즉각적인 피드백

모르는 게 생기면 바로 질문하고 바로 해결합니다. 학원에서는 질문하기 어렵지만, 1:1 과외에서는 궁금한 것을 바로 물어볼 수 있습니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
매 수업 오답 노트를 점검합니다. 틀린 문제를 다시 풀어보고, 같은 실수를 반복하지 않도록 합니다.
</div>

## 학년별 수학 학습 전략

### 고등학교 1학년

고등학교 수학의 기초를 다지는 시기입니다. 다항식, 방정식, 부등식, 함수의 기본 개념을 확실히 잡아야 합니다.

### 고등학교 2학년

심화 개념이 등장하는 시기입니다. 수학I, 수학II, 미적분, 확률과 통계 등 선택과목 개념을 체계적으로 학습해야 합니다.

### 고등학교 3학년

수능 실전 대비 시기입니다. 개념 정리는 마무리하고, 기출문제와 모의고사를 통해 문제 풀이력을 키워야 합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
학년별 학습 목표를 설정하고, 그에 맞는 커리큘럼을 진행합니다. 내신과 수능을 균형 있게 준비합니다.
</div>

## 수업료 안내

동작구 {dong_name} 고등학생 수학과외 수업료는 다음과 같습니다.

**고1~2**는 주1회 기준 25만원에서 35만원, 주2회 기준 42만원에서 58만원 선입니다.

**고3**은 주1회 기준 30만원에서 42만원, 주2회 기준 50만원에서 70만원이 일반적입니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
첫 상담에서 학생의 현재 수준과 목표를 파악하고, 적합한 수업 계획과 수업료를 안내드립니다.
</div>

{{{{< cta-dual type="final" >}}}}

## 자주 묻는 질문

**Q. 내신과 수능 중 어떤 것을 먼저 준비해야 하나요?**

고1~2는 내신 위주로, 고3은 내신과 수능을 병행합니다. 학생의 목표와 현재 상황에 따라 비중을 조절합니다.

**Q. 학원과 과외를 병행해도 되나요?**

가능합니다. 학원에서 진도를 나가고, 과외에서 부족한 부분을 보충하는 방식으로 병행하는 학생들이 있습니다.

**Q. 기초가 많이 부족한데 따라갈 수 있을까요?**

기초가 부족한 학생일수록 1:1 과외가 효과적입니다. 어디서부터 막혔는지 정확히 진단하고, 그 부분부터 차근차근 다시 채워나갑니다.

**Q. 수업은 어디서 진행하나요?**

학생의 집으로 방문하거나, 스터디카페, 도서관 등 학생이 편한 장소에서 수업합니다. 온라인 수업도 가능합니다.

**Q. 선생님은 어떤 분이 오시나요?**

수학 전공 또는 이공계열 전공의 경력 있는 선생님이 수업합니다.

## 마무리

동작구 {dong_name}에서 고등학생 수학과외를 찾고 계신다면, 지금 바로 상담받아보세요. {school_list} 내신과 수능에 맞춘 1:1 맞춤 수업으로 수학 실력을 확실히 올려드립니다.
'''
    return content


def create_dongjak_english_content(dong_info, index):
    dong_name = dong_info["name"]
    schools = dong_info["schools"]
    school_list = get_school_list_text(schools)
    school_tags = get_school_tags(schools)
    title_suffix = dong_info["eng_suffix"]
    image = ENGLISH_IMAGES[index % len(ENGLISH_IMAGES)]
    intro_title, intro_detail = ENGLISH_INTROS[index % len(ENGLISH_INTROS)]

    school_sections = ""
    for i, school in enumerate(schools[:2]):
        if i == 0:
            if school == "동작고":
                school_sections += f"""
### {school} 영어 내신의 특징

{school}은 동작구 사당동에 위치한 공립 고등학교입니다. 교과서 본문 암기가 핵심이며, 본문에 나온 문법과 표현이 시험에 출제됩니다. 서술형 비중도 있어 영작 연습이 필요합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{school} 교과서를 집중 분석합니다. 본문 암기, 핵심 문법 정리, 서술형 대비를 체계적으로 진행합니다.
</div>
"""
            elif school == "성남고":
                school_sections += f"""
### {school} 영어 내신의 특징

{school}은 대방동에 위치한 사립 고등학교입니다. 영어 시험 난이도가 높은 편이며, 교과서 외 지문도 출제됩니다. 독해 실력이 뒷받침되어야 고득점이 가능합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{school} 기출 경향을 분석하여 외부 지문 대비도 함께 합니다. 다양한 주제의 지문을 읽어 독해력을 키웁니다.
</div>
"""
            elif school == "수도여고":
                school_sections += f"""
### {school} 영어 내신의 특징

{school}은 신대방동에 위치한 여자 고등학교입니다. 내신 경쟁이 치열하며, 꼼꼼한 암기와 정확한 문법 지식이 요구됩니다. 서술형에서 실수를 줄이는 것이 중요합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{school} 내신은 정확성이 핵심입니다. 자주 틀리는 표현을 정리하고, 서술형 답안 작성 연습을 집중적으로 합니다.
</div>
"""
            else:
                school_sections += f"""
### {school} 영어 내신의 특징

{school}은 동작구에 위치한 고등학교입니다. 교과서 본문 중심의 출제가 이루어지며, 핵심 문법과 어휘를 확실히 익혀야 합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{school} 교과서를 집중 분석합니다. 본문 암기와 문법 정리를 체계적으로 진행합니다.
</div>
"""
        elif i == 1:
            if school == "경문고":
                school_sections += f"""
### {school} 영어 내신의 특징

{school}은 사당동에 위치한 사립 고등학교입니다. 교과서 본문을 완벽히 암기해야 하며, 어휘와 문법 문제가 고르게 출제됩니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{school} 기출을 분석하여 자주 나오는 유형을 파악합니다. 어휘 테스트와 문법 확인을 매 수업 진행합니다.
</div>
"""
            elif school == "영등포고":
                school_sections += f"""
### {school} 영어 내신의 특징

{school}은 대방동에 위치한 고등학교입니다. 기본에 충실한 출제 경향을 보이며, 교과서 내용을 확실히 숙지하면 좋은 성적을 받을 수 있습니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{school} 내신은 교과서 중심으로 준비합니다. 본문 내용과 핵심 표현을 완벽히 익히도록 합니다.
</div>
"""
            elif school == "숭의여고":
                school_sections += f"""
### {school} 영어 내신의 특징

{school}은 신대방동에 위치한 여자 고등학교입니다. 세심한 준비가 필요하며, 사소한 실수가 등급을 가릅니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{school} 내신은 디테일 관리가 중요합니다. 자주 틀리는 유형을 정리하고, 실수를 줄이는 훈련을 합니다.
</div>
"""
            else:
                school_sections += f"""
### {school} 영어 내신의 특징

{school}은 동작구에 위치한 고등학교입니다. 교과서 본문과 문법 중심으로 출제됩니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{school} 기출문제를 분석하고, 취약 유형을 집중 보완합니다.
</div>
"""

    content = f'''---
title: "동작구 {dong_name} 고등 영어과외 | {school_list} {title_suffix}"
date: 2025-01-29
categories:
  - 고등교육
regions:
  - 서울
cities:
  - 동작구
description: "동작구 {dong_name} 고등학생 영어과외 전문. {school_list} 내신과 수능 맞춤 관리. 문법·독해·어휘 체계적 1:1 지도."
tags:
  - {dong_name}
  - 동작구
  - 고등영어
  - 영어과외
  - 내신관리
  - 수능영어
{school_tags}
  - 영어문법
  - 영어독해
  - 동작관악교육지원청
featured_image: "https://images.unsplash.com/{image}?w=1200&h=630&fit=crop"

---
## 동작구 {dong_name} 고등학생, {intro_title}

{intro_detail} {dong_name}에서 고등학생 자녀의 영어 성적 때문에 고민하시는 학부모님이 많습니다. 단어도 외우고 문법도 공부했는데 성적이 안 오르면 학습 방법이 잘못된 겁니다.

1:1 맞춤 과외는 학생의 현재 상태를 정확히 진단하는 것에서 시작합니다. 문법이 약한지, 독해가 약한지, 어휘가 부족한지를 파악합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
첫 수업에서 학생의 영어 실력을 영역별로 진단합니다. 문법, 독해, 어휘 중 어디가 약한지 파악하고, 맞춤 학습 계획을 세웁니다.
</div>

## 고등학교 영어가 어려운 이유

고등학교 영어는 중학교 영어와 수준이 다릅니다. 문장이 길고 복잡해지고, 추상적인 주제의 지문이 등장합니다. 어휘도 전문적인 용어가 많아집니다.

수능 영어는 절대평가이지만, 1등급 비율이 낮아 사실상 상대평가입니다. 안정적인 1등급을 받으려면 체계적인 준비가 필요합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
문장 구조 분석 능력을 키웁니다. 복잡한 문장도 주어, 동사, 목적어를 찾아 해석할 수 있게 훈련합니다.
</div>

## 수능 영어의 특징

### 긴 지문과 복잡한 문장

수능 영어 지문은 길고, 문장 구조가 복잡합니다. 빈칸 추론, 순서 배열, 문장 삽입 등 사고력을 요구하는 문제가 많습니다.

### EBS 연계

수능 영어는 EBS 교재와 연계됩니다. EBS 지문의 주제와 소재가 변형되어 출제되므로, EBS 학습이 필수입니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
EBS 교재를 효과적으로 학습하는 방법을 지도합니다. 지문의 핵심 내용을 파악하고, 변형에 대비합니다.
</div>

{school_sections}

## 1:1 과외가 효과적인 이유

### 맞춤형 커리큘럼

학원은 정해진 진도를 나갑니다. 1:1 과외는 학생에게 필요한 내용만 집중합니다. 이미 아는 내용은 빠르게 넘어가고, 약한 부분은 집중 보강합니다.

### 학교 내신 맞춤 대비

같은 문법이라도 학교마다 출제 스타일이 다릅니다. 1:1 과외는 학생이 다니는 학교의 기출문제를 분석하고 맞춤 대비합니다.

### 즉각적인 피드백

모르는 게 생기면 바로 질문하고 바로 해결합니다. 이해 안 되는 부분을 그냥 넘어가지 않습니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
매 수업 어휘 테스트를 진행합니다. 영어는 어휘가 기본입니다. 꾸준히 암기하고 점검합니다.
</div>

## 학년별 영어 학습 전략

### 고등학교 1학년

고등 영어의 기초를 다지는 시기입니다. 기본 문법을 완벽히 정리하고, 독해 기초 체력을 키워야 합니다.

### 고등학교 2학년

본격적인 수능 대비 시기입니다. EBS 교재를 학습하고, 다양한 유형의 문제를 접해야 합니다.

### 고등학교 3학년

수능 실전 대비 시기입니다. 시간 내에 문제를 푸는 연습과 함께, 취약 유형을 집중 보완해야 합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
학년별 학습 목표를 설정하고, 그에 맞는 커리큘럼을 진행합니다. 내신과 수능을 균형 있게 준비합니다.
</div>

## 수업료 안내

동작구 {dong_name} 고등학생 영어과외 수업료는 다음과 같습니다.

**고1~2**는 주1회 기준 22만원에서 32만원, 주2회 기준 38만원에서 52만원 선입니다.

**고3**은 주1회 기준 28만원에서 38만원, 주2회 기준 45만원에서 62만원이 일반적입니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
첫 상담에서 학생의 현재 수준과 목표를 파악하고, 적합한 수업 계획과 수업료를 안내드립니다.
</div>

{{{{< cta-dual type="final" >}}}}

## 자주 묻는 질문

**Q. 내신과 수능 중 어떤 것을 먼저 준비해야 하나요?**

고1~2는 내신 위주로, 고3은 내신과 수능을 병행합니다. 학생의 목표와 현재 상황에 따라 비중을 조절합니다.

**Q. 학원과 과외를 병행해도 되나요?**

가능합니다. 학원에서 진도를 나가고, 과외에서 부족한 부분을 보충하는 방식으로 병행하는 학생들이 있습니다.

**Q. 기초가 많이 부족한데 따라갈 수 있을까요?**

기초가 부족한 학생일수록 1:1 과외가 효과적입니다. 어디서부터 막혔는지 정확히 진단하고, 그 부분부터 차근차근 다시 채워나갑니다.

**Q. 수업은 어디서 진행하나요?**

학생의 집으로 방문하거나, 스터디카페, 도서관 등 학생이 편한 장소에서 수업합니다. 온라인 수업도 가능합니다.

**Q. 선생님은 어떤 분이 오시나요?**

영어 전공 또는 관련 경력이 있는 선생님이 수업합니다.

## 마무리

동작구 {dong_name}에서 고등학생 영어과외를 찾고 계신다면, 지금 바로 상담받아보세요. {school_list} 내신과 수능에 맞춘 1:1 맞춤 수업으로 영어 실력을 확실히 올려드립니다.
'''
    return content


def main():
    output_dir = "content/high"
    created_files = []

    for i, dong in enumerate(DONGJAK_DONGS):
        # 수학 파일 생성
        math_filename = f"dongjak-{dong['id']}-high-math.md"
        math_filepath = os.path.join(output_dir, math_filename)
        math_content = create_dongjak_math_content(dong, i)

        with open(math_filepath, 'w', encoding='utf-8') as f:
            f.write(math_content)
        created_files.append(math_filename)

        # 영어 파일 생성
        english_filename = f"dongjak-{dong['id']}-high-english.md"
        english_filepath = os.path.join(output_dir, english_filename)
        english_content = create_dongjak_english_content(dong, i)

        with open(english_filepath, 'w', encoding='utf-8') as f:
            f.write(english_content)
        created_files.append(english_filename)

    print(f"동작구 고등: {len(created_files)}개 파일 생성 완료")
    for f in created_files[:5]:
        print(f"  - {f}")
    if len(created_files) > 5:
        print(f"  ... 외 {len(created_files) - 5}개")


if __name__ == "__main__":
    main()
