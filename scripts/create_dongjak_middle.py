#!/usr/bin/env python3
"""동작구 중등 수학/영어 과외 콘텐츠 생성 스크립트"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from create_middle_content import MATH_IMAGES, ENGLISH_IMAGES, MATH_INTROS, ENGLISH_INTROS

# 동작구 동별 정보 (15개 행정동)
DONGJAK_DONGS = [
    {"id": "noryangjin1", "name": "노량진1동", "schools": ["대방중", "강남중"], "math_suffix": "내신 완벽 대비", "eng_suffix": "독해·문법 완성"},
    {"id": "noryangjin2", "name": "노량진2동", "schools": ["대방중", "강남중"], "math_suffix": "맞춤 커리큘럼", "eng_suffix": "1:1 맞춤 수업"},
    {"id": "heukseok", "name": "흑석동", "schools": ["중앙대부속중"], "math_suffix": "기초부터 심화까지", "eng_suffix": "체계적 학습 관리"},
    {"id": "sangdo1", "name": "상도1동", "schools": ["강현중", "상현중"], "math_suffix": "학교별 내신 특화", "eng_suffix": "실력 향상 수업"},
    {"id": "sangdo2", "name": "상도2동", "schools": ["강현중", "상현중"], "math_suffix": "1:1 맞춤 수업", "eng_suffix": "기초부터 심화까지"},
    {"id": "sangdo3", "name": "상도3동", "schools": ["국사봉중", "장승중"], "math_suffix": "개념부터 실전까지", "eng_suffix": "맞춤 커리큘럼"},
    {"id": "sangdo4", "name": "상도4동", "schools": ["국사봉중", "장승중"], "math_suffix": "실력 향상 수업", "eng_suffix": "학교별 내신 특화"},
    {"id": "sadang1", "name": "사당1동", "schools": ["상도중", "동작중"], "math_suffix": "체계적 학습 관리", "eng_suffix": "내신 완벽 대비"},
    {"id": "sadang2", "name": "사당2동", "schools": ["상도중", "동작중"], "math_suffix": "맞춤 커리큘럼", "eng_suffix": "독해·문법 완성"},
    {"id": "sadang3", "name": "사당3동", "schools": ["상도중", "동작중"], "math_suffix": "기초부터 심화까지", "eng_suffix": "1:1 맞춤 수업"},
    {"id": "sadang4", "name": "사당4동", "schools": ["상도중", "동작중"], "math_suffix": "학교별 내신 특화", "eng_suffix": "체계적 학습 관리"},
    {"id": "sadang5", "name": "사당5동", "schools": ["상도중", "동작중"], "math_suffix": "개념부터 실전까지", "eng_suffix": "실력 향상 수업"},
    {"id": "daebang", "name": "대방동", "schools": ["대방중", "강남중"], "math_suffix": "1:1 맞춤 수업", "eng_suffix": "맞춤 커리큘럼"},
    {"id": "sindaebang1", "name": "신대방1동", "schools": ["문창중"], "math_suffix": "실력 향상 수업", "eng_suffix": "기초부터 심화까지"},
    {"id": "sindaebang2", "name": "신대방2동", "schools": ["문창중"], "math_suffix": "체계적 학습 관리", "eng_suffix": "학교별 내신 특화"},
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
            if school == "중앙대부속중":
                school_sections += f"""
### {school} 수학 내신의 특징

{school}은 중앙대학교 사범대학 부속 중학교로, 교육에 대한 전문성이 높습니다. 교과서 기본 개념을 충실히 다루면서도 응용력을 요구하는 문제가 출제됩니다. 서술형 비중이 높아 풀이 과정을 논리적으로 작성하는 연습이 필요합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{school} 기출문제를 철저히 분석합니다. 대학 부속 중학교 특성에 맞춘 심화 학습도 병행합니다.
</div>
"""
            else:
                school_sections += f"""
### {school} 수학 내신의 특징

{school}은 교과서 중심의 기본 문제와 응용 문제를 균형 있게 출제합니다. 교과서 예제를 완벽히 이해하고, 익힘책 문제까지 풀어두면 기본 점수는 확보할 수 있습니다.

서술형 문제에서는 풀이 과정을 논리적으로 쓰는 것이 중요합니다. 답만 맞아도 풀이 과정이 부실하면 감점됩니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{school} 기출문제를 분석하여 자주 나오는 유형을 파악합니다. 선생님별 출제 스타일까지 고려한 맞춤 대비를 합니다.
</div>
"""
        elif i == 1:
            school_sections += f"""
### {school} 수학 내신의 특징

{school}은 응용 문제와 서술형 비중이 높습니다. 기본 개념만 알아서는 고득점이 어렵고, 개념을 응용하는 능력이 필요합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{school}의 고난도 기출문제를 집중 분석합니다. 시간 내에 푸는 연습과 부분 점수 전략까지 훈련합니다.
</div>
"""

    content = f'''---
title: "동작구 {dong_name} 중등 수학과외 | {school_list} {title_suffix}"
date: 2025-01-29
categories:
  - 중등교육
regions:
  - 서울
cities:
  - 동작구
description: "동작구 {dong_name} 중학생 수학과외 전문. {school_list} 내신 맞춤 관리. 개념부터 심화까지 체계적 1:1 지도."
tags:
  - {dong_name}
  - 동작구
  - 중등수학
  - 수학과외
  - 내신관리
{school_tags}
  - 수학개념
  - 수학심화
  - 동작관악교육지원청
featured_image: "https://images.unsplash.com/{image}?w=1200&h=630&fit=crop"

---
## 동작구 {dong_name} 중학생, {intro_title}

{intro_detail} {dong_name}에서 중학생 자녀의 수학 성적 때문에 고민하시는 학부모님이 많습니다. 학원을 보내도, 문제집을 풀려도 성적이 오르지 않는 이유는 학생 개인의 취약점을 정확히 파악하지 못했기 때문입니다.

1:1 맞춤 과외는 학생의 현재 상태를 정확히 진단하는 것에서 시작합니다. 어떤 단원에서 막히는지, 어떤 유형에서 실수가 나오는지 파악합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
첫 수업에서 학생의 수학 실력을 꼼꼼히 진단합니다. 단원별로 개념 이해도를 체크하고, 최근 시험지를 분석하여 취약점을 파악합니다.
</div>

## 중학교 수학이 중요한 이유

중학교 수학은 고등학교 수학의 기초입니다. 중학교 때 개념에 구멍이 생기면 고등학교 가서 메우기 어렵습니다. 중1 정수와 유리수 연산이 안 되면 중2 다항식 계산이 안 되고, 중2가 안 되면 중3 이차방정식이 안 됩니다.

동작구는 중앙대, 숭실대 등 대학가가 형성된 교육 중심 지역입니다. 노량진 학원가가 있어 교육열이 높고, 중앙대부속중 같은 명문 중학교도 있습니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
현재 단원의 개념을 완벽히 이해했는지 확인한 후 다음으로 넘어갑니다. 학생이 직접 설명할 수 있어야 진짜 아는 것입니다.
</div>

## 중학교 수학, 어떤 점이 어려운가

### 추상적 개념의 등장

초등학교 수학은 구체적인 숫자를 다뤘습니다. 중학교는 문자가 등장합니다. x, y라는 문자로 미지수를 표현하고, 이 문자들로 식을 세우고 풀어야 합니다.

### 개념 간 연결

중학교 수학은 개념이 서로 연결되어 있습니다. 일차방정식을 알아야 연립방정식을 풀고, 함수를 알아야 그래프를 그립니다.

### 사고력 요구

단순 계산이 아니라 생각을 해야 합니다. 문제를 읽고 무엇을 구해야 하는지 파악하고, 어떤 개념을 적용해야 하는지 판단해야 합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
개념을 단순히 설명하는 것이 아니라, 왜 그런지 이유를 함께 설명합니다. 원리를 이해하면 응용이 됩니다.
</div>

{school_sections}

## 1:1 과외가 효과적인 이유

### 맞춤형 진단과 처방

학원은 정해진 커리큘럼대로 진도를 나갑니다. 1:1 과외는 학생 한 명에게만 집중합니다. 이해가 될 때까지 설명하고, 완전히 소화한 후 다음으로 넘어갑니다.

### 즉각적인 피드백

모르는 게 생기면 바로 질문할 수 있습니다. 학원에서는 수업 중에 질문하기 어렵습니다. 1:1 과외에서는 궁금한 것을 바로 물어보고 바로 해결합니다.

### 학교 시험 맞춤 대비

같은 개념이라도 학교마다 출제 스타일이 다릅니다. 1:1 과외는 학생이 다니는 학교의 기출문제를 분석하고, 그 학교 시험에 맞춰 대비합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
매 수업 학생이 배운 내용을 직접 설명해보게 합니다. 설명할 수 있어야 진짜 아는 것입니다.
</div>

## 학년별 수학 학습 전략

### 중학교 1학년

수학의 기초를 다지는 가장 중요한 시기입니다. 정수와 유리수의 연산, 문자와 식, 일차방정식의 개념을 완벽히 익혀야 합니다.

### 중학교 2학년

중학교 수학의 핵심 시기입니다. 연립방정식과 일차함수가 등장합니다. 함수의 개념을 확실히 잡고, 그래프 해석 능력을 키워야 합니다.

### 중학교 3학년

고등학교 준비 시기입니다. 이차방정식, 이차함수, 피타고라스 정리, 삼각비를 마스터해야 합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
학년별 핵심 단원을 체계적으로 정리합니다. 다음 학년으로 연결되는 핵심 개념은 반드시 완벽히 마스터하고 넘어갑니다.
</div>

## 내신 대비 전략

### 2주 전부터 시작

시험 2주 전부터 본격적인 시험 대비를 시작합니다. 시험 범위를 확인하고, 개념 정리와 문제 풀이를 병행합니다.

### 교과서와 익힘책 완벽 정리

학교 시험은 교과서에서 출제됩니다. 교과서 예제, 익힘 문제를 완벽히 풀 수 있어야 합니다.

### 기출문제 분석

이전 시험 기출문제를 분석합니다. 선생님마다 출제 스타일이 있습니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
시험 2주 전부터 시험 대비 모드로 전환합니다. 시험 범위를 집중 복습하고, 예상 문제를 풀어봅니다.
</div>

## 수업료 안내

동작구 {dong_name} 중학생 수학과외 수업료는 다음과 같습니다.

**중1~2**는 주1회 기준 18만원에서 25만원, 주2회 기준 32만원에서 45만원 선입니다.

**중3**은 주1회 기준 20만원에서 28만원, 주2회 기준 36만원에서 50만원이 일반적입니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
첫 상담에서 학생의 현재 수준과 목표를 파악하고, 적합한 수업 계획과 수업료를 안내드립니다.
</div>

{{{{< cta-dual type="final" >}}}}

## 자주 묻는 질문

**Q. 수학 기초가 많이 부족한데 따라갈 수 있을까요?**

기초가 부족한 학생일수록 1:1 과외가 효과적입니다. 어디서부터 막혔는지 정확히 진단하고, 그 부분부터 차근차근 다시 설명합니다.

**Q. 학원과 과외를 병행해도 되나요?**

가능합니다. 학원에서 진도를 나가고, 과외에서 부족한 부분을 보충하는 방식으로 병행하는 학생들이 많습니다.

**Q. 내신 대비와 선행을 같이 할 수 있나요?**

가능합니다. 시험 기간에는 내신 대비에 집중하고, 시험이 끝나면 선행을 진행합니다.

**Q. 수업은 어디서 진행하나요?**

학생의 집으로 방문하거나, 스터디카페, 도서관 등 학생이 편한 장소에서 수업합니다. 온라인 수업도 가능합니다.

**Q. 선생님은 어떤 분이 오시나요?**

수학 전공 또는 이공계열 전공의 경력 있는 선생님이 수업합니다.

## 마무리

동작구 {dong_name}에서 중학생 수학과외를 찾고 계신다면, 지금 바로 상담받아보세요. {school_list} 내신에 맞춘 1:1 맞춤 수업으로 수학 실력을 확실히 올려드립니다.
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
            if school == "중앙대부속중":
                school_sections += f"""
### {school} 영어 내신의 특징

{school}은 중앙대학교 사범대학 부속 중학교로, 영어 교육 수준이 높습니다. 교과서 본문 암기는 기본이고, 심화 독해 지문도 출제됩니다. 서술형 비중이 높아 영작 실력도 필요합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{school} 영어 교과서를 집중 분석합니다. 본문 암기, 핵심 문법 정리, 서술형 대비를 체계적으로 진행합니다.
</div>
"""
            else:
                school_sections += f"""
### {school} 영어 내신의 특징

{school}은 교과서 본문 암기가 핵심입니다. 본문에 나온 표현과 문법 사항이 그대로 시험에 출제됩니다. 본문을 통째로 외우고, 핵심 문법을 정확히 이해해야 합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{school} 영어 교과서를 집중 분석합니다. 본문 암기, 핵심 문법 정리, 서술형 대비를 체계적으로 진행합니다.
</div>
"""
        elif i == 1:
            school_sections += f"""
### {school} 영어 내신의 특징

{school}은 독해 지문의 난이도가 있는 편입니다. 교과서 외 지문도 출제되어 다양한 글을 읽어본 학생이 유리합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{school}의 기출 문제를 분석하여 출제 경향을 파악합니다. 교과서 외 지문 독해 연습도 병행합니다.
</div>
"""

    content = f'''---
title: "동작구 {dong_name} 중등 영어과외 | {school_list} {title_suffix}"
date: 2025-01-29
categories:
  - 중등교육
regions:
  - 서울
cities:
  - 동작구
description: "동작구 {dong_name} 중학생 영어과외 전문. {school_list} 내신 맞춤 관리. 문법·독해·어휘 체계적 1:1 지도."
tags:
  - {dong_name}
  - 동작구
  - 중등영어
  - 영어과외
  - 내신관리
{school_tags}
  - 영어문법
  - 영어독해
  - 동작관악교육지원청
featured_image: "https://images.unsplash.com/{image}?w=1200&h=630&fit=crop"

---
## 동작구 {dong_name} 중학생, {intro_title}

{intro_detail} {dong_name}에서 중학생 자녀의 영어 성적 때문에 고민하시는 학부모님이 많습니다. 단어도 외우고 문법책도 풀었는데 성적이 안 오르면 학습 방향이 잘못된 겁니다.

1:1 맞춤 과외는 학생의 현재 상태를 정확히 진단하는 것에서 시작합니다. 문법이 약한지, 독해가 약한지, 어휘가 부족한지를 파악합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
첫 수업에서 학생의 영어 실력을 영역별로 진단합니다. 문법, 독해, 어휘, 쓰기 중 어디가 약한지 파악하고, 맞춤 학습 계획을 세웁니다.
</div>

## 중학교 영어가 중요한 이유

중학교 영어는 고등학교 영어의 기초입니다. 중학교 때 문법이 흔들리면 고등학교 독해가 어려워집니다. 수능 영어까지 이어지는 긴 싸움의 시작점이 바로 중학교 영어입니다.

동작구는 중앙대, 숭실대 등 대학가가 형성된 지역입니다. 노량진 학원가가 있어 교육열이 높고, 영어 실력 향상에 적극적인 학생들이 많습니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
문법을 단순 암기가 아닌 원리로 접근합니다. 왜 그런 규칙이 있는지 이해하면 오래 기억되고 응용도 됩니다.
</div>

## 중학교 영어, 어떤 점이 어려운가

### 문법의 복잡화

초등학교 영어는 간단한 문장과 회화 중심이었습니다. 중학교는 본격적인 문법이 등장합니다. 시제, 조동사, 부정사, 동명사, 분사, 관계대명사 등 배워야 할 문법이 많아집니다.

### 문장의 복잡화

중학교로 올라갈수록 문장이 길고 복잡해집니다. 주어와 동사를 찾기도 어려워지고, 수식 구조가 복잡해집니다.

### 어휘량 증가

외워야 할 단어가 급격히 늘어납니다. 단순 암기로는 한계가 있고, 효율적인 어휘 학습 전략이 필요합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
복잡한 문장을 분석하는 방법을 체계적으로 가르칩니다. 주어, 동사를 찾고, 수식 관계를 파악하는 연습을 합니다.
</div>

{school_sections}

## 1:1 과외가 효과적인 이유

### 개인별 맞춤 지도

학원은 여러 학생을 한꺼번에 가르칩니다. 1:1 과외는 학생 한 명에게만 집중합니다. 문법이 약하면 문법을, 독해가 약하면 독해를 집중적으로 보완합니다.

### 즉각적인 질문과 해결

모르는 게 생기면 바로 질문할 수 있습니다. 학원에서는 질문하기 어렵습니다. 1:1 과외에서는 이해 안 되는 부분을 그냥 넘어가지 않습니다.

### 학교 시험 맞춤 대비

같은 문법이라도 학교마다 출제 스타일이 다릅니다. 1:1 과외는 학생이 다니는 학교의 기출문제를 분석하고 맞춤 대비합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
매 수업 배운 문법을 활용해 직접 문장을 만들어보게 합니다. 직접 써봐야 내 것이 됩니다.
</div>

## 학년별 영어 학습 전략

### 중학교 1학년

영어 기초를 다지는 중요한 시기입니다. be동사, 일반동사, 시제, 조동사 등 기본 문법을 확실히 익혀야 합니다.

### 중학교 2학년

중학교 영어의 핵심 시기입니다. to부정사, 동명사, 분사 등 준동사 개념이 등장합니다. 관계대명사도 배웁니다.

### 중학교 3학년

고등학교 준비 시기입니다. 복합 문장 구조를 이해하고, 긴 지문 독해 연습을 해야 합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
학년별 핵심 문법을 체계적으로 정리합니다. 빈틈없이 마무리한 후 다음 단계로 넘어갑니다.
</div>

## 내신 대비 전략

### 교과서 완벽 분석

학교 시험은 교과서에서 출제됩니다. 본문 내용을 완벽히 이해하고, 핵심 표현과 문법을 정리합니다.

### 단어 암기

교과서 단어와 추가 어휘를 매일 암기합니다. 영어는 어휘가 기본입니다.

### 서술형 대비

서술형 문제 유형을 분석하고, 작문 연습을 합니다. 문법에 맞게 쓰는 연습이 중요합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
시험 2주 전부터 시험 대비 모드로 전환합니다. 시험 범위를 집중 복습하고, 예상 문제를 풀어봅니다.
</div>

## 수업료 안내

동작구 {dong_name} 중학생 영어과외 수업료는 다음과 같습니다.

**중1~2**는 주1회 기준 17만원에서 24만원, 주2회 기준 30만원에서 42만원 선입니다.

**중3**은 주1회 기준 19만원에서 26만원, 주2회 기준 34만원에서 48만원이 일반적입니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
첫 상담에서 학생의 현재 수준과 목표를 파악하고, 적합한 수업 계획과 수업료를 안내드립니다.
</div>

{{{{< cta-dual type="final" >}}}}

## 자주 묻는 질문

**Q. 영어 기초가 많이 부족한데 따라갈 수 있을까요?**

기초가 부족한 학생일수록 1:1 과외가 효과적입니다. 어디서부터 막혔는지 정확히 진단하고, 그 부분부터 차근차근 다시 설명합니다.

**Q. 학원과 과외를 병행해도 되나요?**

가능합니다. 학원에서 진도를 나가고, 과외에서 부족한 부분을 보충하는 방식으로 병행하는 학생들이 많습니다.

**Q. 내신 대비와 회화를 같이 할 수 있나요?**

가능합니다. 다만 내신 시험 대비가 우선이라면 내신에 집중하는 것을 권장합니다.

**Q. 수업은 어디서 진행하나요?**

학생의 집으로 방문하거나, 스터디카페, 도서관 등 편한 장소에서 수업합니다. 온라인 수업도 가능합니다.

**Q. 선생님은 어떤 분이 오시나요?**

영어 전공 또는 관련 경력이 있는 선생님이 수업합니다.

## 마무리

동작구 {dong_name}에서 중학생 영어과외를 찾고 계신다면, 지금 바로 상담받아보세요. {school_list} 내신에 맞춘 1:1 맞춤 수업으로 영어 실력을 확실히 올려드립니다.
'''
    return content


def main():
    output_dir = "content/middle"
    created_files = []

    for i, dong in enumerate(DONGJAK_DONGS):
        # 수학 파일 생성
        math_filename = f"dongjak-{dong['id']}-middle-math.md"
        math_filepath = os.path.join(output_dir, math_filename)
        math_content = create_dongjak_math_content(dong, i)

        with open(math_filepath, 'w', encoding='utf-8') as f:
            f.write(math_content)
        created_files.append(math_filename)

        # 영어 파일 생성
        english_filename = f"dongjak-{dong['id']}-middle-english.md"
        english_filepath = os.path.join(output_dir, english_filename)
        english_content = create_dongjak_english_content(dong, i)

        with open(english_filepath, 'w', encoding='utf-8') as f:
            f.write(english_content)
        created_files.append(english_filename)

    print(f"동작구 중등: {len(created_files)}개 파일 생성 완료")
    for f in created_files[:5]:
        print(f"  - {f}")
    if len(created_files) > 5:
        print(f"  ... 외 {len(created_files) - 5}개")


if __name__ == "__main__":
    main()
