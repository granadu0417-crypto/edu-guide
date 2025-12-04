#!/usr/bin/env python3
"""동대문구 고등 수학/영어 과외 콘텐츠 생성 스크립트"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from create_middle_content import MATH_IMAGES, ENGLISH_IMAGES, MATH_INTROS, ENGLISH_INTROS

# 동대문구 동별 정보 (14개 행정동)
# 고등학교: 대광고, 청량고, 경희고(자사고), 경희여고, 휘경여고, 휘봉고, 해성여고, 서울정화고, 동국대사범대부속고
DONGDAEMUN_DONGS = [
    {"id": "yongsin", "name": "용신동", "schools": ["대광고"]},
    {"id": "jegi", "name": "제기동", "schools": ["대광고", "청량고"]},
    {"id": "cheongnyangni", "name": "청량리동", "schools": ["청량고"]},
    {"id": "hoegi", "name": "회기동", "schools": ["경희고", "경희여고"]},
    {"id": "hwigyeong1", "name": "휘경1동", "schools": ["휘경여고", "휘봉고"]},
    {"id": "hwigyeong2", "name": "휘경2동", "schools": ["휘경여고", "휘봉고"]},
    {"id": "imun1", "name": "이문1동", "schools": ["경희고", "경희여고"]},
    {"id": "imun2", "name": "이문2동", "schools": ["경희고", "경희여고"]},
    {"id": "jeonnong1", "name": "전농1동", "schools": ["해성여고", "청량고"]},
    {"id": "jeonnong2", "name": "전농2동", "schools": ["해성여고", "청량고"]},
    {"id": "dapsimni1", "name": "답십리1동", "schools": ["서울정화고"]},
    {"id": "dapsimni2", "name": "답십리2동", "schools": ["서울정화고"]},
    {"id": "jangan1", "name": "장안1동", "schools": ["동국대사범대부속고"]},
    {"id": "jangan2", "name": "장안2동", "schools": ["동국대사범대부속고"]},
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

def create_dongdaemun_high_math_content(dong_info, index):
    dong_name = dong_info["name"]
    schools = dong_info["schools"]
    school_list = get_school_list_text(schools)
    school_tags = get_school_tags(schools)
    image = MATH_IMAGES[index % len(MATH_IMAGES)]
    intro_title, intro_detail = MATH_INTROS[index % len(MATH_INTROS)]

    school_sections = ""
    for i, school in enumerate(schools[:2]):
        if i == 0:
            if school == "경희고":
                school_sections += f"""
### {school} 수학 내신의 특징

{school}는 서울 동북권 대표 자율형사립고입니다. 자사고 특성상 내신 경쟁이 매우 치열합니다. 최상위권 변별을 위해 경시 수준의 고난도 문제가 출제되며, 서술형 비중이 높고 채점이 엄격합니다.

경희대 병설학교로서 이과 중심의 심화 교육이 이루어집니다. 수학 내신에서 고득점을 받으려면 기본 개념은 물론 최고난도 심화 문제까지 대비해야 합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{school} 기출문제를 철저히 분석합니다. 자사고 수준의 고난도 문제에 대비하여 경시 유형 훈련도 병행합니다.
</div>
"""
            elif school == "대광고":
                school_sections += f"""
### {school} 수학 내신의 특징

{school}는 기독교 명문 사학입니다. 대광중에서 올라온 학생들의 학력 수준이 높아 내신 경쟁이 치열합니다. 교과서 개념을 충실히 다루면서도 응용 문제의 비중이 높습니다.

서술형 문제에서 풀이 과정의 논리성을 꼼꼼히 채점합니다. 답만 맞아도 풀이가 부실하면 감점될 수 있습니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{school} 기출문제를 철저히 분석합니다. 선생님별 출제 스타일을 파악하여 효과적으로 대비합니다.
</div>
"""
            elif school == "동국대사범대부속고":
                school_sections += f"""
### {school} 수학 내신의 특징

{school}는 동국대 재단의 불교 종립학교입니다. 사범대 부속고 특성상 교육에 대한 전문성이 높고, 체계적인 내신 관리가 이루어집니다.

교과서 중심의 기본 문제와 응용 문제가 균형 있게 출제됩니다. 서술형 비중이 있어 풀이 과정을 정확히 쓰는 연습이 필요합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{school} 기출문제를 철저히 분석합니다. 학교 특성에 맞는 맞춤 내신 대비를 진행합니다.
</div>
"""
            else:
                school_sections += f"""
### {school} 수학 내신의 특징

{school}은 동대문구의 대표적인 고등학교입니다. 교과서 개념을 충실히 다루면서도 응용력을 요구하는 문제가 출제됩니다. 서술형 비중이 있어 풀이 과정을 논리적으로 작성하는 연습이 필요합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{school} 기출문제를 철저히 분석합니다. 선생님별 출제 스타일을 파악하여 효과적으로 대비합니다.
</div>
"""
        elif i == 1:
            school_sections += f"""
### {school} 수학 내신의 특징

{school}은 기본 개념과 함께 심화 문제도 출제됩니다. 시간 배분이 중요하며, 계산 실수를 줄이는 훈련이 필요합니다. 내신 등급 경쟁이 치열하여 꼼꼼한 준비가 필수입니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{school}의 고난도 문제 유형을 집중 분석합니다. 실전처럼 시간을 재며 푸는 연습을 반복합니다.
</div>
"""

    content = f'''---
title: "동대문구 {dong_name} 고등 수학과외 | {school_list} 내신·수능 대비"
date: 2025-01-29
categories:
  - 고등교육
regions:
  - 서울
cities:
  - 동대문구
description: "동대문구 {dong_name} 고등학생 수학과외 전문. {school_list} 내신 및 수능 동시 대비. 개념부터 킬러 문항까지 체계적 1:1 지도."
tags:
  - {dong_name}
  - 동대문구
  - 고등수학
  - 수학과외
  - 내신관리
  - 수능대비
{school_tags}
  - 동부교육지원청
featured_image: "https://images.unsplash.com/{image}?w=1200&h=630&fit=crop"

---
## 동대문구 {dong_name} 고등학생, {intro_title}

{intro_detail} {dong_name}에서 고등학생 자녀의 수학 때문에 고민하시는 학부모님이 많습니다. 고등학교 수학은 중학교와 완전히 다른 수준입니다. 개념의 깊이, 문제의 난이도가 확 올라갑니다.

동대문구는 경희대, 한국외대 등 대학가가 형성된 교육 중심 지역입니다. 경희고 같은 자사고, 대광고 같은 명문 사학이 있어 내신 경쟁이 치열합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
첫 수업에서 학생의 수학 실력을 정확하게 진단합니다. 단원별 개념 이해도, 문제 풀이 능력, 시간 관리 능력까지 파악하여 맞춤 학습 계획을 세웁니다.
</div>

## 고등학교 수학, 무엇이 달라질까요?

### 개념의 고도화

중학교가 기초였다면, 고등학교는 본격적인 수학입니다. 함수의 극한과 연속, 미분과 적분, 지수함수와 로그함수, 삼각함수와 벡터, 확률과 통계의 심화까지 다룹니다. 개념 자체가 어렵고, 이해 없이는 한 발짝도 나갈 수 없습니다.

### 내신 수학의 치열한 경쟁

고등학교 내신은 1~2문제로 등급이 결정됩니다. 상위권 변별 문제, 시간 부족하게 출제되는 시험, 계산 실수 유발 문제, 복합 개념 응용 문제 등 100점 맞기가 매우 어렵습니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{school_list} 기출 문제를 철저히 분석합니다. 학교별로 출제 경향이 다르기 때문에, 해당 학교에 맞는 맞춤 내신 대비를 진행합니다.
</div>

### 수능 수학의 난이도

수능 수학은 가장 변별력 높은 영역입니다. 킬러 문항(21번, 29번, 30번), 시간 압박(100분 30문항), 한 문제로 등급 변동이 있습니다. 수학 1등급은 상위 4%만 받을 수 있습니다.

{school_sections}

## 고등학교 수학과외, 왜 필요한가요?

### 내신과 수능 동시 대비

고등학교는 내신과 수능 모두 중요합니다. 내신은 학교 기출 분석이, 수능은 평가원 기출 분석이 핵심입니다. 둘 다 잡아야 좋은 대학에 갈 수 있습니다.

### 개념 완벽 이해

고등 수학은 개념이 생명입니다. 공식 유도 과정을 이해하고 왜 그런지 설명할 수 있어야 합니다. 개념 없이는 응용 문제를 풀 수 없습니다.

### 약점 집중 보완

학생마다 약한 부분이 다릅니다. 1:1 과외는 미적분이 약하면 미적분 집중, 확률이 어려우면 확률 훈련, 계산 실수가 많으면 연산 강화, 시간이 부족하면 속도 훈련을 합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
오답 노트를 함께 작성하고 분석합니다. 왜 틀렸는지, 어떤 개념이 부족했는지 파악하여 같은 실수를 반복하지 않도록 훈련합니다.
</div>

## 효과적인 고등 수학 학습법

### 1단계: 개념 완벽 이해

고등 수학의 핵심은 개념입니다. 공식을 외우지 말고 유도하세요. 정의와 정리를 정확히 알고, 예제로 개념을 확인합니다.

### 2단계: 유형 문제 정복

개념을 익혔다면 유형 문제로 확인합니다. 유형별로 분류하며 정리하고, 대표 문제를 완벽히 풀어봅니다.

### 3단계: 킬러 문항 도전

기본이 탄탄하면 킬러 문항에 도전합니다. 수능 고난도 문제, 평가원 기출 킬러, 복합 개념 응용 문제를 다룹니다.

### 4단계: 시간 관리 훈련

수능은 시간과의 싸움입니다. 문제당 시간 배분, 쉬운 문제 먼저, 막히면 넘어가기, 실전처럼 연습합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
4단계 학습법을 체계적으로 진행합니다. 학생의 현재 수준에 맞춰 단계별로 밟아갑니다.
</div>

{{{{< cta-dual type="final" >}}}}

## {dong_name} 고등학생 수학, 학년별 전략

### 고1 - 기초 확립기

목표는 고등 수학 기초 완성입니다. 다항식과 방정식, 부등식을 완벽히 익히고, 도형의 방정식을 이해합니다. 고1 수학이 고2, 고3의 토대입니다.

### 고2 - 실력 향상기

목표는 본격적인 수학 실력 쌓기입니다. 수학I, II 개념을 완성하고 미적분 기초를 다집니다. 확률과 통계를 시작하고 수능 기출도 시작합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
학년별로 적정 학습량과 진도를 계획합니다. 무리한 선행보다 현재 학년 개념을 완벽하게 숙달한 후 다음 단계로 넘어갑니다.
</div>

### 고3 - 수능 완성기

목표는 내신 마무리와 수능 완성입니다. 약점을 집중 보완하고 킬러 문항을 정복합니다. 실전 모의고사를 반복하고 시간 관리를 완벽히 합니다.

## {dong_name} 고등 수학과외 비용 안내

동대문구 {dong_name} 고등 수학과외 비용입니다.

**고1~2**는 주1회 기준 25만원에서 35만원, 주2회 기준 42만원에서 58만원 선입니다.

**고3**은 주1회 기준 30만원에서 42만원, 주2회 기준 50만원에서 70만원이 일반적입니다.

수업 횟수, 시간, 선생님 경력에 따라 달라질 수 있습니다. 정확한 수업료는 상담을 통해 안내드립니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
수업료는 학생 상황에 맞춰 합리적으로 책정합니다. 무료 상담을 통해 학생 수준을 파악한 후, 필요한 수업 횟수와 시간을 제안드립니다.
</div>

## 자주 묻는 질문

**Q. 고등 수학은 선행이 필수인가요?**

반드시 그렇지는 않습니다. 무리한 선행보다 현재 학년 개념을 완벽히 이해하는 것이 더 중요합니다. 다만 기초가 탄탄한 학생은 적정 선행이 도움됩니다.

**Q. 내신과 수능 중 어떤 것을 먼저 준비해야 하나요?**

고1~2는 내신 위주로, 고3은 내신과 수능을 병행합니다. 학기 중에는 내신에 집중하고, 방학에는 수능 개념과 기출 분석에 집중합니다.

**Q. 학원과 과외 중 어떤 것이 좋나요?**

기초가 있고 자기주도가 가능하면 학원, 개별 관리가 필요하면 과외를 추천합니다. 병행도 효과적입니다.

**Q. 수학 1등급을 받으려면 어떻게 해야 하나요?**

개념 완벽 이해, 기출 문제 반복, 오답노트 필수, 시간 관리 훈련, 계산 실수 줄이기가 핵심입니다.

**Q. 수업은 어디서 진행하나요?**

학생의 집으로 방문하거나, 스터디카페, 도서관 등 편한 장소에서 수업합니다. 온라인 수업도 가능합니다.

## 마무리

동대문구 {dong_name}에서 고등학생 수학과외를 찾고 계신다면, 지금 바로 상담받아보세요. {school_list} 내신과 수능에 맞춘 1:1 맞춤 수업으로 수학 실력을 확실히 끌어올립니다. 고등학교 수학은 대입의 핵심입니다. 지금 시작하면 달라집니다.
'''
    return content


def create_dongdaemun_high_english_content(dong_info, index):
    dong_name = dong_info["name"]
    schools = dong_info["schools"]
    school_list = get_school_list_text(schools)
    school_tags = get_school_tags(schools)
    image = ENGLISH_IMAGES[index % len(ENGLISH_IMAGES)]
    intro_title, intro_detail = ENGLISH_INTROS[index % len(ENGLISH_INTROS)]

    school_sections = ""
    for i, school in enumerate(schools[:2]):
        if i == 0:
            if school == "경희고":
                school_sections += f"""
### {school} 영어 내신의 특징

{school}는 자율형사립고로서 영어 내신의 난이도가 매우 높습니다. 교과서 외 지문이 다수 출제되고, 고급 어휘와 복잡한 구문에 대한 이해가 필수입니다. 서술형 비중이 높아 작문 실력도 필요합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{school} 영어 기출을 철저히 분석합니다. 자사고 수준의 고난도 독해와 어휘를 집중 훈련합니다.
</div>
"""
            elif school == "대광고":
                school_sections += f"""
### {school} 영어 내신의 특징

{school}는 기독교 명문 사학으로 영어 교육에 강점이 있습니다. 교과서 본문 암기가 기본이며, 본문에서 핵심 표현과 문법이 출제됩니다. 서술형에서는 정확한 영작 실력이 요구됩니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{school} 영어 기출을 철저히 분석합니다. 본문 암기, 문법 정리, 서술형 대비를 체계적으로 진행합니다.
</div>
"""
            else:
                school_sections += f"""
### {school} 영어 내신의 특징

{school}은 교과서 본문 암기가 기본입니다. 본문에서 핵심 표현과 문법이 그대로 출제됩니다. 본문을 완벽히 숙지하고, 변형 문제에 대비해야 합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{school} 영어 기출을 철저히 분석합니다. 본문 암기, 문법 정리, 서술형 대비를 체계적으로 진행합니다.
</div>
"""
        elif i == 1:
            school_sections += f"""
### {school} 영어 내신의 특징

{school}은 독해 지문의 난이도가 높은 편입니다. 교과서 외 지문도 출제되며, 심화 문법 문제도 나옵니다. 다양한 유형의 문제에 대비해야 합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{school} 기출을 분석하여 출제 패턴을 파악합니다. 교과서 외 지문 독해 연습도 병행합니다.
</div>
"""

    content = f'''---
title: "동대문구 {dong_name} 고등 영어과외 | {school_list} 내신·수능 대비"
date: 2025-01-29
categories:
  - 고등교육
regions:
  - 서울
cities:
  - 동대문구
description: "동대문구 {dong_name} 고등학생 영어과외 전문. {school_list} 내신 및 수능 동시 대비. 독해·문법·어휘 체계적 1:1 지도."
tags:
  - {dong_name}
  - 동대문구
  - 고등영어
  - 영어과외
  - 내신관리
  - 수능대비
{school_tags}
  - 동부교육지원청
featured_image: "https://images.unsplash.com/{image}?w=1200&h=630&fit=crop"

---
## 동대문구 {dong_name} 고등학생, {intro_title}

{intro_detail} {dong_name}에서 고등학생 자녀의 영어 성적 때문에 고민하시는 학부모님이 많습니다. 고등학교 영어는 중학교와 차원이 다릅니다. 지문이 길어지고, 어휘 수준이 올라가며, 수능형 문제 유형에 적응해야 합니다.

동대문구는 한국외대가 있어 외국어 교육에 대한 관심이 높습니다. 경희대 캠퍼스와 함께 대학가가 형성되어 있고, 경희고, 대광고 등 명문고가 있어 영어 내신 경쟁이 치열합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
첫 수업에서 학생의 영어 실력을 영역별로 진단합니다. 문법, 독해, 어휘, 듣기 중 어디가 약한지 파악하고 맞춤 학습 계획을 세웁니다.
</div>

## 고등학교 영어, 무엇이 달라질까요?

### 지문의 고도화

중학교 영어는 짧고 쉬운 지문이었습니다. 고등학교는 지문이 길고 복잡해집니다. 추상적인 주제, 복잡한 문장 구조, 고급 어휘가 등장합니다.

### 수능 영어의 특수성

수능 영어는 절대평가이지만 1등급 받기는 쉽지 않습니다. 빈칸 추론, 순서 배열, 문장 삽입 등 고난도 유형에 대한 훈련이 필수입니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{school_list} 기출 문제를 철저히 분석합니다. 학교별 출제 경향에 맞춘 맞춤 내신 대비를 진행합니다.
</div>

### 내신과 수능의 간극

내신은 교과서 중심, 수능은 EBS 중심입니다. 둘 다 잡으려면 효율적인 학습 전략이 필요합니다.

{school_sections}

## 고등학교 영어과외, 왜 필요한가요?

### 내신과 수능 동시 대비

고등학교는 내신과 수능 모두 중요합니다. 내신은 학교 교과서와 기출 분석이, 수능은 EBS와 평가원 기출 분석이 핵심입니다.

### 영역별 약점 보완

학생마다 약한 영역이 다릅니다. 1:1 과외는 독해가 약하면 독해 집중, 문법이 어려우면 문법 훈련, 어휘가 부족하면 어휘 암기를 집중적으로 진행합니다.

### 수능 유형 완벽 대비

수능 영어는 유형별 접근이 중요합니다. 빈칸 추론, 순서 배열, 문장 삽입 등 고난도 유형을 집중 훈련합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
오답 노트를 함께 작성하고 분석합니다. 왜 틀렸는지, 어떤 부분이 부족했는지 파악하여 같은 실수를 반복하지 않도록 합니다.
</div>

## 효과적인 고등 영어 학습법

### 1단계: 어휘력 확장

고등 영어의 기본은 어휘입니다. 수능 필수 어휘, 교과서 어휘를 매일 꾸준히 암기합니다.

### 2단계: 문법 완성

고등 문법을 체계적으로 정리합니다. 문장 구조 분석 능력을 키워야 복잡한 문장도 읽을 수 있습니다.

### 3단계: 독해력 강화

다양한 유형의 지문을 읽으며 독해력을 키웁니다. 주제 파악, 요지 추론, 빈칸 추론 등 유형별 접근법을 익힙니다.

### 4단계: 실전 훈련

실전처럼 시간을 재며 문제를 풉니다. 수능은 70분 안에 45문항을 풀어야 합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
4단계 학습법을 체계적으로 진행합니다. 학생의 현재 수준에 맞춰 단계별로 밟아갑니다.
</div>

{{{{< cta-dual type="final" >}}}}

## {dong_name} 고등학생 영어, 학년별 전략

### 고1 - 기초 확립기

목표는 고등 영어 기초 완성입니다. 수능 필수 어휘를 시작하고, 고등 문법을 정리합니다. 긴 지문 읽기에 익숙해지는 것이 중요합니다.

### 고2 - 실력 향상기

목표는 본격적인 영어 실력 쌓기입니다. 수능 유형별 접근법을 익히고, EBS 연계 교재를 시작합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
학년별로 적정 학습량과 진도를 계획합니다. 내신 기간에는 내신에 집중, 방학에는 수능 대비에 집중합니다.
</div>

### 고3 - 수능 완성기

목표는 내신 마무리와 수능 완성입니다. EBS 연계 교재를 완벽히 분석하고, 실전 모의고사를 반복합니다.

## {dong_name} 고등 영어과외 비용 안내

동대문구 {dong_name} 고등 영어과외 비용입니다.

**고1~2**는 주1회 기준 22만원에서 32만원, 주2회 기준 38만원에서 52만원 선입니다.

**고3**은 주1회 기준 28만원에서 38만원, 주2회 기준 45만원에서 62만원이 일반적입니다.

수업 횟수, 시간, 선생님 경력에 따라 달라질 수 있습니다. 정확한 수업료는 상담을 통해 안내드립니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
수업료는 학생 상황에 맞춰 합리적으로 책정합니다. 무료 상담을 통해 학생 수준을 파악한 후, 필요한 수업 횟수와 시간을 제안드립니다.
</div>

## 자주 묻는 질문

**Q. 수능 영어 1등급 받으려면 어떻게 해야 하나요?**

어휘력이 기본입니다. 수능 필수 어휘를 완벽히 암기하고, 유형별 접근법을 익혀야 합니다.

**Q. 내신과 수능 중 어떤 것을 먼저 준비해야 하나요?**

고1~2는 내신 위주로, 고3은 내신과 수능을 병행합니다. 학기 중에는 내신, 방학에는 수능에 집중합니다.

**Q. 학원과 과외 중 어떤 것이 좋나요?**

기초가 있고 자기주도가 가능하면 학원, 개별 관리가 필요하면 과외를 추천합니다. 병행도 효과적입니다.

**Q. 듣기도 같이 준비할 수 있나요?**

가능합니다. 듣기는 매일 꾸준히 연습하는 것이 중요합니다. 수업에서 듣기 훈련법도 안내드립니다.

**Q. 수업은 어디서 진행하나요?**

학생의 집으로 방문하거나, 스터디카페, 도서관 등 편한 장소에서 수업합니다. 온라인 수업도 가능합니다.

## 마무리

동대문구 {dong_name}에서 고등학생 영어과외를 찾고 계신다면, 지금 바로 상담받아보세요. {school_list} 내신과 수능에 맞춘 1:1 맞춤 수업으로 영어 실력을 확실히 끌어올립니다. 고등학교 영어는 대입의 핵심입니다. 지금 시작하면 달라집니다.
'''
    return content


def main():
    output_dir = "content/high"
    created_files = []

    for i, dong in enumerate(DONGDAEMUN_DONGS):
        # 수학 파일 생성
        math_filename = f"dongdaemun-{dong['id']}-high-math.md"
        math_filepath = os.path.join(output_dir, math_filename)
        math_content = create_dongdaemun_high_math_content(dong, i)

        with open(math_filepath, 'w', encoding='utf-8') as f:
            f.write(math_content)
        created_files.append(math_filename)

        # 영어 파일 생성
        english_filename = f"dongdaemun-{dong['id']}-high-english.md"
        english_filepath = os.path.join(output_dir, english_filename)
        english_content = create_dongdaemun_high_english_content(dong, i)

        with open(english_filepath, 'w', encoding='utf-8') as f:
            f.write(english_content)
        created_files.append(english_filename)

    print(f"동대문구 고등: {len(created_files)}개 파일 생성 완료")
    for f in created_files[:5]:
        print(f"  - {f}")
    if len(created_files) > 5:
        print(f"  ... 외 {len(created_files) - 5}개")


if __name__ == "__main__":
    main()
