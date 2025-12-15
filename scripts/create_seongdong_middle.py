#!/usr/bin/env python3
"""성동구 중등 수학/영어 과외 콘텐츠 생성 스크립트"""

import os

MATH_IMAGES = [
    "photo-1635070041078-e363dbe005cb", "photo-1596495578065-6e0763fa1178",
    "photo-1509228468518-180dd4864904", "photo-1635070041409-e63e783ce3b1",
    "photo-1518133910546-b6c2fb7d79e3", "photo-1453733190371-0a9bedd82893",
    "photo-1596495577886-d920f1fb7238", "photo-1611532736597-de2d4265fba3",
    "photo-1580894894513-541e068a3e2b", "photo-1613909207039-6b173b755cc1",
    "photo-1559494007-9f5847c49d94", "photo-1544383835-bda2bc66a55d",
    "photo-1518435579668-52e6c59a9c85", "photo-1611329857570-f02f340e7378",
    "photo-1512314889357-e157c22f938d", "photo-1516796181074-bf453fbfa3e6",
    "photo-1515879218367-8466d910aaa4",
]

ENGLISH_IMAGES = [
    "photo-1457369804613-52c61a468e7d", "photo-1456513080510-7bf3a84b82f8",
    "photo-1546410531-bb4caa6b424d", "photo-1553877522-43269d4ea984",
    "photo-1515378791036-0648a3ef77b2", "photo-1519389950473-47ba0277781c",
    "photo-1523240795612-9a054b0db644", "photo-1488190211105-8b0e65b80b4e",
    "photo-1434030216411-0b793f4b4173", "photo-1455390582262-044cdead277a",
    "photo-1471107340929-a87cd0f5b5f3", "photo-1415369629372-26f2fe60c467",
    "photo-1447069387593-a5de0862481e", "photo-1476234251651-f353703a034d",
    "photo-1516321497487-e288fb19713f", "photo-1521587760476-6c12a4b040da",
    "photo-1507842217343-583bb7270b66",
]

MATH_INTROS = [
    ("수학 성적이 고민이라면", "중학교 수학, 어디서부터 손대야 할지 막막하신가요?"),
    ("수학 자신감이 필요하다면", "수학에 대한 두려움, 이제 떨쳐버릴 때입니다."),
    ("내신 성적을 올리고 싶다면", "학교 시험에서 좋은 성적을 받고 싶으시죠?"),
    ("수학 기초가 흔들린다면", "기초가 부족하면 다음 단계로 넘어갈 수 없습니다."),
    ("선행보다 현행이 중요하다면", "지금 배우는 내용을 확실히 잡는 게 먼저입니다."),
    ("수학 공부법을 모르겠다면", "어떻게 공부해야 할지 방향을 잡아드립니다."),
    ("개념이 헷갈린다면", "개념을 제대로 이해하면 문제가 풀립니다."),
    ("서술형이 어렵다면", "서술형 문제, 접근법을 알면 어렵지 않습니다."),
    ("수학 때문에 스트레스라면", "수학 스트레스, 함께 해결해 드립니다."),
    ("실력이 제자리라면", "열심히 하는데 성적이 안 오르는 이유가 있습니다."),
    ("학원이 안 맞는다면", "학원에서 효과를 못 봤다면 1:1 맞춤이 답입니다."),
    ("수학을 포기하고 싶다면", "포기하기엔 아직 이릅니다. 다시 시작해봐요."),
    ("고등 준비가 걱정이라면", "중학교 수학이 고등학교의 기초입니다."),
    ("시험만 보면 긴장된다면", "시험 불안, 충분한 준비로 극복할 수 있습니다."),
    ("계산 실수가 잦다면", "실수를 줄이는 것도 실력입니다."),
    ("응용문제가 안 풀린다면", "응용력은 개념 이해에서 시작됩니다."),
    ("문제 풀이가 느리다면", "속도와 정확성, 둘 다 잡을 수 있습니다."),
]

ENGLISH_INTROS = [
    ("영어 성적이 오르지 않는다면", "영어 공부를 하는데 성적이 제자리인가요?"),
    ("영어가 어렵게 느껴진다면", "영어, 제대로 된 방법으로 시작하면 달라집니다."),
    ("문법이 헷갈린다면", "문법을 체계적으로 정리하면 독해가 됩니다."),
    ("단어 암기가 안 된다면", "효율적인 어휘 학습법이 있습니다."),
    ("독해가 느리다면", "독해 속도를 높이는 방법을 알려드립니다."),
    ("내신 영어가 어렵다면", "학교 시험에 맞춘 영어 공부가 필요합니다."),
    ("영어 자신감이 없다면", "영어에 대한 자신감을 다시 찾아드립니다."),
    ("학원 영어가 안 맞다면", "1:1 맞춤 수업으로 효과를 느껴보세요."),
    ("서술형이 두렵다면", "서술형 영작, 연습하면 할 수 있습니다."),
    ("듣기가 안 들린다면", "듣기 실력도 훈련으로 향상됩니다."),
    ("영어 공부법을 모르겠다면", "어떻게 공부해야 할지 방향을 잡아드립니다."),
    ("고등 영어가 걱정된다면", "중학 영어가 고등 영어의 기초입니다."),
    ("영어 기초가 부족하다면", "기초부터 차근차근 다시 시작합니다."),
    ("시험 점수가 들쭉날쭉하다면", "안정적인 성적을 위한 학습법이 있습니다."),
    ("영어 포기를 고민한다면", "포기하기엔 이릅니다. 함께 해봐요."),
    ("본문 암기가 안 된다면", "효과적인 암기 전략을 알려드립니다."),
    ("문장 해석이 안 된다면", "문장 구조 분석법을 알려드립니다."),
]

# 성동구 17개 행정동
SEONGDONG_DONGS = [
    {"id": "wangsimni-doseondong", "name": "왕십리도선동", "schools": ["무학중", "행당중"], "math_suffix": "내신 완벽 대비", "eng_suffix": "독해·문법 완성"},
    {"id": "wangsimni2", "name": "왕십리2동", "schools": ["무학중", "행당중"], "math_suffix": "맞춤 커리큘럼", "eng_suffix": "1:1 맞춤 수업"},
    {"id": "majang", "name": "마장동", "schools": ["동마중", "마장중"], "math_suffix": "기초부터 심화까지", "eng_suffix": "체계적 학습 관리"},
    {"id": "sageun", "name": "사근동", "schools": ["한양대부중"], "math_suffix": "학교별 내신 특화", "eng_suffix": "실력 향상 수업"},
    {"id": "haengdang1", "name": "행당1동", "schools": ["무학중", "행당중"], "math_suffix": "1:1 맞춤 수업", "eng_suffix": "내신 완벽 대비"},
    {"id": "haengdang2", "name": "행당2동", "schools": ["무학중", "행당중"], "math_suffix": "개념부터 실전까지", "eng_suffix": "맞춤 커리큘럼"},
    {"id": "eungbong", "name": "응봉동", "schools": ["광희중"], "math_suffix": "실력 향상 수업", "eng_suffix": "기초부터 심화까지"},
    {"id": "geumho1ga", "name": "금호1가동", "schools": ["광희중", "옥정중"], "math_suffix": "체계적 학습 관리", "eng_suffix": "학교별 내신 특화"},
    {"id": "geumho2-3ga", "name": "금호2·3가동", "schools": ["광희중", "옥정중"], "math_suffix": "내신 완벽 대비", "eng_suffix": "독해·문법 완성"},
    {"id": "geumho4ga", "name": "금호4가동", "schools": ["옥정중"], "math_suffix": "맞춤 커리큘럼", "eng_suffix": "1:1 맞춤 수업"},
    {"id": "oksu", "name": "옥수동", "schools": ["옥정중"], "math_suffix": "기초부터 심화까지", "eng_suffix": "체계적 학습 관리"},
    {"id": "seongsu1ga1", "name": "성수1가1동", "schools": ["성수중"], "math_suffix": "학교별 내신 특화", "eng_suffix": "실력 향상 수업"},
    {"id": "seongsu1ga2", "name": "성수1가2동", "schools": ["성수중"], "math_suffix": "1:1 맞춤 수업", "eng_suffix": "내신 완벽 대비"},
    {"id": "seongsu2ga1", "name": "성수2가1동", "schools": ["성원중"], "math_suffix": "개념부터 실전까지", "eng_suffix": "맞춤 커리큘럼"},
    {"id": "seongsu2ga3", "name": "성수2가3동", "schools": ["성원중"], "math_suffix": "실력 향상 수업", "eng_suffix": "기초부터 심화까지"},
    {"id": "songjeong", "name": "송정동", "schools": ["성원중", "성수중"], "math_suffix": "체계적 학습 관리", "eng_suffix": "학교별 내신 특화"},
    {"id": "yongdap", "name": "용답동", "schools": ["성원중", "성수중"], "math_suffix": "내신 완벽 대비", "eng_suffix": "독해·문법 완성"},
]

def get_school_list(schools):
    return "·".join(schools) if len(schools) > 1 else schools[0]

def get_school_tags(schools):
    return "\n".join([f"  - {s}" for s in schools])

def create_math_content(dong, idx):
    name, schools = dong["name"], dong["schools"]
    school_list, tags = get_school_list(schools), get_school_tags(schools)
    img = MATH_IMAGES[idx % len(MATH_IMAGES)]
    intro_t, intro_d = MATH_INTROS[idx % len(MATH_INTROS)]

    school_section = ""
    for i, sch in enumerate(schools[:2]):
        if sch == "한양대부중":
            desc = f"{sch}은 한양대학교 사범대학 부속 중학교입니다. 대학 부속 학교답게 교육의 질이 높고, 내신 시험도 체계적입니다. 심화 문제가 출제되어 깊이 있는 이해가 필요합니다."
        elif sch in ["무학중", "행당중"]:
            desc = f"{sch}은 행당동에 위치한 공립 중학교입니다. 왕십리역 인근의 교육 중심지에 위치하여 학부모의 교육열이 높습니다. 교과서 중심의 기본 문제와 응용 문제가 균형 있게 출제됩니다."
        elif sch == "광희중":
            desc = f"{sch}은 응봉동에 위치한 공립 중학교입니다. 응봉산 인근의 주거지역에 위치하여 안정적인 학습 환경을 갖추고 있습니다."
        elif sch == "옥정중":
            desc = f"{sch}은 옥수동에 위치한 공립 중학교입니다. 한강 인근의 주거지역에 위치하여 쾌적한 교육 환경을 갖추고 있습니다."
        elif sch in ["성수중", "성원중"]:
            desc = f"{sch}은 성수동에 위치한 공립 중학교입니다. 서울숲과 성수동 IT산업 밀집지역 인근에 위치하여 젊은 학부모가 많고 교육열이 높습니다."
        elif sch in ["동마중", "마장중"]:
            desc = f"{sch}은 마장동에 위치한 공립 중학교입니다. 교과서 중심의 기본 문제와 응용 문제가 균형 있게 출제됩니다."
        else:
            desc = f"{sch}은 성동구에 위치한 중학교입니다. 교과서 중심의 기본 문제와 응용 문제가 균형 있게 출제됩니다."

        school_section += f"""
### {sch} 수학 내신의 특징

{desc}

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{sch} 기출문제를 분석하여 출제 경향을 파악합니다. 자주 나오는 유형을 집중 연습합니다.
</div>
"""

    return f'''---
title: "성동구 {name} 중등 수학과외 | {school_list} {dong["math_suffix"]}"
date: 2025-01-29
categories:
  - 중등교육
regions:
  - 서울
cities:
  - 성동구
description: "성동구 {name} 중학생 수학과외 전문. {school_list} 내신 맞춤 관리. 개념부터 심화까지 체계적 1:1 지도."
tags:
  - {name}
  - 성동구
  - 중등수학
  - 수학과외
  - 내신관리
{tags}
  - 수학개념
  - 수학심화
  - 성동광진교육지원청
featured_image: "https://images.unsplash.com/{img}?w=1200&h=630&fit=crop"

---
## 성동구 {name} 중학생, {intro_t}

{intro_d} {name}에서 중학생 자녀의 수학 성적 때문에 고민하시는 학부모님이 많습니다. 학원을 보내도 성적이 오르지 않는 이유는 학생 개인의 취약점을 정확히 파악하지 못했기 때문입니다.

1:1 맞춤 과외는 학생의 현재 상태를 정확히 진단하는 것에서 시작합니다. 어떤 단원에서 막히는지, 어떤 유형에서 실수가 나오는지 파악합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
첫 수업에서 학생의 수학 실력을 꼼꼼히 진단합니다. 단원별로 개념 이해도를 체크하고, 최근 시험지를 분석하여 취약점을 파악합니다.
</div>

## 중학교 수학이 중요한 이유

중학교 수학은 고등학교 수학의 기초입니다. 중학교 때 개념에 구멍이 생기면 고등학교 가서 메우기 어렵습니다.

성동구는 한양대학교가 위치한 교육 중심 지역입니다. 왕십리 부도심과 성수동 IT산업 밀집지역의 발전으로 젊은 학부모가 늘어나며 교육열이 높아지고 있습니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
현재 단원의 개념을 완벽히 이해했는지 확인한 후 다음으로 넘어갑니다. 학생이 직접 설명할 수 있어야 진짜 아는 것입니다.
</div>

## 중학교 수학, 어떤 점이 어려운가

### 추상적 개념의 등장

초등학교 수학은 구체적인 숫자를 다뤘습니다. 중학교는 문자가 등장합니다. x, y라는 문자로 미지수를 표현하고, 이 문자들로 식을 세우고 풀어야 합니다.

### 개념 간 연결

중학교 수학은 개념이 서로 연결되어 있습니다. 일차방정식을 알아야 연립방정식을 풀고, 함수를 알아야 그래프를 그립니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
개념을 단순히 설명하는 것이 아니라, 왜 그런지 이유를 함께 설명합니다. 원리를 이해하면 응용이 됩니다.
</div>

{school_section}

## 1:1 과외가 효과적인 이유

### 맞춤형 진단과 처방

학원은 정해진 커리큘럼대로 진도를 나갑니다. 1:1 과외는 학생 한 명에게만 집중합니다. 이해가 될 때까지 설명하고, 완전히 소화한 후 다음으로 넘어갑니다.

### 즉각적인 피드백

모르는 게 생기면 바로 질문할 수 있습니다. 1:1 과외에서는 궁금한 것을 바로 물어보고 바로 해결합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
매 수업 학생이 배운 내용을 직접 설명해보게 합니다. 설명할 수 있어야 진짜 아는 것입니다.
</div>

## 학년별 수학 학습 전략

### 중학교 1학년

수학의 기초를 다지는 가장 중요한 시기입니다. 정수와 유리수의 연산, 문자와 식, 일차방정식의 개념을 완벽히 익혀야 합니다.

### 중학교 2학년

중학교 수학의 핵심 시기입니다. 연립방정식과 일차함수가 등장합니다. 함수의 개념을 확실히 잡아야 합니다.

### 중학교 3학년

고등학교 준비 시기입니다. 이차방정식, 이차함수, 피타고라스 정리, 삼각비를 마스터해야 합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
학년별 핵심 단원을 체계적으로 정리합니다. 다음 학년으로 연결되는 핵심 개념은 반드시 완벽히 마스터하고 넘어갑니다.
</div>

## 수업료 안내

성동구 {name} 중학생 수학과외 수업료는 다음과 같습니다.

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

**Q. 수업은 어디서 진행하나요?**

학생의 집으로 방문하거나, 스터디카페, 도서관 등 학생이 편한 장소에서 수업합니다. 온라인 수업도 가능합니다.

## 마무리

성동구 {name}에서 중학생 수학과외를 찾고 계신다면, 지금 바로 상담받아보세요. {school_list} 내신에 맞춘 1:1 맞춤 수업으로 수학 실력을 확실히 올려드립니다.
'''

def create_english_content(dong, idx):
    name, schools = dong["name"], dong["schools"]
    school_list, tags = get_school_list(schools), get_school_tags(schools)
    img = ENGLISH_IMAGES[idx % len(ENGLISH_IMAGES)]
    intro_t, intro_d = ENGLISH_INTROS[idx % len(ENGLISH_INTROS)]

    school_section = ""
    for i, sch in enumerate(schools[:2]):
        if sch == "한양대부중":
            desc = f"{sch}은 한양대학교 사범대학 부속 중학교입니다. 대학 부속 학교답게 영어 교육 수준이 높습니다. 교과서 본문뿐 아니라 심화 독해 지문도 출제됩니다."
        else:
            desc = f"{sch}은 성동구에 위치한 중학교입니다. 교과서 본문 암기가 핵심이며, 본문에 나온 표현과 문법 사항이 그대로 시험에 출제됩니다."

        school_section += f"""
### {sch} 영어 내신의 특징

{desc}

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{sch} 영어 교과서를 집중 분석합니다. 본문 암기, 핵심 문법 정리, 서술형 대비를 체계적으로 진행합니다.
</div>
"""

    return f'''---
title: "성동구 {name} 중등 영어과외 | {school_list} {dong["eng_suffix"]}"
date: 2025-01-29
categories:
  - 중등교육
regions:
  - 서울
cities:
  - 성동구
description: "성동구 {name} 중학생 영어과외 전문. {school_list} 내신 맞춤 관리. 문법·독해·어휘 체계적 1:1 지도."
tags:
  - {name}
  - 성동구
  - 중등영어
  - 영어과외
  - 내신관리
{tags}
  - 영어문법
  - 영어독해
  - 성동광진교육지원청
featured_image: "https://images.unsplash.com/{img}?w=1200&h=630&fit=crop"

---
## 성동구 {name} 중학생, {intro_t}

{intro_d} {name}에서 중학생 자녀의 영어 성적 때문에 고민하시는 학부모님이 많습니다. 단어도 외우고 문법책도 풀었는데 성적이 안 오르면 학습 방향이 잘못된 겁니다.

1:1 맞춤 과외는 학생의 현재 상태를 정확히 진단하는 것에서 시작합니다. 문법이 약한지, 독해가 약한지, 어휘가 부족한지를 파악합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
첫 수업에서 학생의 영어 실력을 영역별로 진단합니다. 문법, 독해, 어휘, 쓰기 중 어디가 약한지 파악하고, 맞춤 학습 계획을 세웁니다.
</div>

## 중학교 영어가 중요한 이유

중학교 영어는 고등학교 영어의 기초입니다. 중학교 때 문법이 흔들리면 고등학교 독해가 어려워집니다.

성동구는 한양대학교가 위치한 교육 중심 지역입니다. 대학가의 학구적인 분위기와 함께 영어 교육에 대한 관심도 높습니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
문법을 단순 암기가 아닌 원리로 접근합니다. 왜 그런 규칙이 있는지 이해하면 오래 기억되고 응용도 됩니다.
</div>

## 중학교 영어, 어떤 점이 어려운가

### 문법의 복잡화

초등학교 영어는 간단한 문장과 회화 중심이었습니다. 중학교는 본격적인 문법이 등장합니다. 시제, 조동사, 부정사, 동명사, 분사, 관계대명사 등 배워야 할 문법이 많아집니다.

### 어휘량 증가

외워야 할 단어가 급격히 늘어납니다. 효율적인 어휘 학습 전략이 필요합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
복잡한 문장을 분석하는 방법을 체계적으로 가르칩니다. 주어, 동사를 찾고, 수식 관계를 파악하는 연습을 합니다.
</div>

{school_section}

## 1:1 과외가 효과적인 이유

### 개인별 맞춤 지도

학원은 여러 학생을 한꺼번에 가르칩니다. 1:1 과외는 학생 한 명에게만 집중합니다. 문법이 약하면 문법을, 독해가 약하면 독해를 집중적으로 보완합니다.

### 즉각적인 질문과 해결

모르는 게 생기면 바로 질문할 수 있습니다. 1:1 과외에서는 이해 안 되는 부분을 그냥 넘어가지 않습니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
매 수업 배운 문법을 활용해 직접 문장을 만들어보게 합니다. 직접 써봐야 내 것이 됩니다.
</div>

## 학년별 영어 학습 전략

### 중학교 1학년

영어 기초를 다지는 중요한 시기입니다. be동사, 일반동사, 시제, 조동사 등 기본 문법을 확실히 익혀야 합니다.

### 중학교 2학년

중학교 영어의 핵심 시기입니다. to부정사, 동명사, 분사 등 준동사 개념이 등장합니다.

### 중학교 3학년

고등학교 준비 시기입니다. 복합 문장 구조를 이해하고, 긴 지문 독해 연습을 해야 합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
학년별 핵심 문법을 체계적으로 정리합니다. 빈틈없이 마무리한 후 다음 단계로 넘어갑니다.
</div>

## 수업료 안내

성동구 {name} 중학생 영어과외 수업료는 다음과 같습니다.

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

**Q. 수업은 어디서 진행하나요?**

학생의 집으로 방문하거나, 스터디카페, 도서관 등 편한 장소에서 수업합니다. 온라인 수업도 가능합니다.

## 마무리

성동구 {name}에서 중학생 영어과외를 찾고 계신다면, 지금 바로 상담받아보세요. {school_list} 내신에 맞춘 1:1 맞춤 수업으로 영어 실력을 확실히 올려드립니다.
'''

def main():
    os.makedirs("content/middle", exist_ok=True)
    files = []
    for i, dong in enumerate(SEONGDONG_DONGS):
        for subj, func in [("math", create_math_content), ("english", create_english_content)]:
            fn = f"seongdong-{dong['id']}-middle-{subj}.md"
            with open(f"content/middle/{fn}", 'w', encoding='utf-8') as f:
                f.write(func(dong, i))
            files.append(fn)
    print(f"성동구 중등: {len(files)}개 파일 생성 완료")

if __name__ == "__main__":
    main()
