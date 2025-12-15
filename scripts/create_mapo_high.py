#!/usr/bin/env python3
"""마포구 고등 수학/영어 과외 콘텐츠 생성 스크립트"""

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
    "photo-1516796181074-bf453fbfa3e6",
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
    "photo-1521587760476-6c12a4b040da",
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
    ("모의고사 등급이 안 오른다면", "모의고사 성적, 전략적으로 올릴 수 있습니다."),
    ("미적분이 어렵다면", "미적분, 개념부터 차근차근 잡아드립니다."),
    ("내신 등급이 떨어졌다면", "내신 성적 하락, 원인을 찾아 해결합니다."),
    ("수능 준비가 막막하다면", "수능까지 남은 시간, 효율적으로 활용하세요."),
    ("기출 분석이 안 된다면", "기출문제 분석법을 알려드립니다."),
    ("시간이 부족하다면", "시간 관리 전략이 필요합니다."),
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
    ("빈칸 추론이 어렵다면", "빈칸 추론, 접근 전략을 알면 풀립니다."),
    ("모의고사 등급이 불안정하다면", "안정적인 등급을 위한 학습법이 있습니다."),
    ("내신 영어가 어렵다면", "학교 시험에 맞춘 전략이 필요합니다."),
    ("영어 포기를 고민한다면", "포기하기엔 아직 이릅니다."),
    ("듣기가 불안하다면", "듣기 안정권 확보 전략을 알려드립니다."),
    ("서술형이 어렵다면", "서술형 대비, 체계적으로 준비합니다."),
]

# 마포구 동별 정보 (16개 행정동)
MAPO_DONGS = [
    {"id": "gongdeok", "name": "공덕동", "schools": ["숭문고", "광성고"], "math_suffix": "내신·수능 대비", "eng_suffix": "독해·문법 완성"},
    {"id": "ahyeon", "name": "아현동", "schools": ["숭문고", "서울여고"], "math_suffix": "맞춤 커리큘럼", "eng_suffix": "1:1 맞춤 수업"},
    {"id": "dohwa", "name": "도화동", "schools": ["광성고", "숭문고"], "math_suffix": "기초부터 심화까지", "eng_suffix": "체계적 학습 관리"},
    {"id": "yonggang", "name": "용강동", "schools": ["광성고", "경성고"], "math_suffix": "학교별 내신 특화", "eng_suffix": "실력 향상 수업"},
    {"id": "daeheung", "name": "대흥동", "schools": ["숭문고"], "math_suffix": "1:1 맞춤 수업", "eng_suffix": "내신·수능 대비"},
    {"id": "yeomni", "name": "염리동", "schools": ["서울여고"], "math_suffix": "개념부터 실전까지", "eng_suffix": "맞춤 커리큘럼"},
    {"id": "sinsu", "name": "신수동", "schools": ["광성고"], "math_suffix": "실력 향상 수업", "eng_suffix": "기초부터 심화까지"},
    {"id": "seogang", "name": "서강동", "schools": ["광성고", "경성고"], "math_suffix": "체계적 학습 관리", "eng_suffix": "학교별 내신 특화"},
    {"id": "seogyo", "name": "서교동", "schools": ["경성고", "홍익대부속여고"], "math_suffix": "내신 + 수능 병행", "eng_suffix": "독해·문법 완성"},
    {"id": "hapjeong", "name": "합정동", "schools": ["경성고", "홍익대부속여고"], "math_suffix": "개념완성 수업", "eng_suffix": "1:1 맞춤 수업"},
    {"id": "mangwon1", "name": "망원1동", "schools": ["경성고", "상암고"], "math_suffix": "내신·수능 대비", "eng_suffix": "체계적 학습 관리"},
    {"id": "mangwon2", "name": "망원2동", "schools": ["경성고", "상암고"], "math_suffix": "맞춤 커리큘럼", "eng_suffix": "실력 향상 수업"},
    {"id": "yeonnam", "name": "연남동", "schools": ["경성고"], "math_suffix": "기초부터 심화까지", "eng_suffix": "내신·수능 대비"},
    {"id": "seongsan1", "name": "성산1동", "schools": ["홍익대부속여고", "상암고"], "math_suffix": "학교별 내신 특화", "eng_suffix": "맞춤 커리큘럼"},
    {"id": "seongsan2", "name": "성산2동", "schools": ["홍익대부속여고", "상암고"], "math_suffix": "1:1 맞춤 수업", "eng_suffix": "기초부터 심화까지"},
    {"id": "sangam", "name": "상암동", "schools": ["상암고"], "math_suffix": "개념부터 실전까지", "eng_suffix": "학교별 내신 특화"},
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

def create_mapo_math_content(dong_info, index):
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
            if school == "숭문고":
                school_sections += f"""
### {school} 수학 내신의 특징

{school}은 1906년 개교한 마포구의 전통 있는 사립 고등학교입니다. 오랜 역사만큼 내신 시험의 체계가 잘 잡혀 있습니다. 기본 개념 문제와 심화 문제가 균형 있게 출제되며, 서술형 비중이 높은 편입니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{school} 기출문제를 철저히 분석합니다. 전통 사학의 출제 경향을 파악하여 내신에 맞춘 준비를 합니다.
</div>
"""
            elif school == "광성고":
                school_sections += f"""
### {school} 수학 내신의 특징

{school}은 신수동에 위치한 사립 고등학교입니다. 서강대학교 인근에 위치하여 학구적인 분위기가 있습니다. 내신 시험에서 개념 이해와 응용력을 함께 평가합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{school} 기출문제를 분석하여 출제 경향을 파악합니다. 개념 정리와 응용 문제 풀이를 병행합니다.
</div>
"""
            elif school == "서울여고":
                school_sections += f"""
### {school} 수학 내신의 특징

{school}은 염리동에 위치한 여자 사립 고등학교입니다. 내신 경쟁이 치열하며, 꼼꼼한 준비가 필요합니다. 서술형 비중이 높아 풀이 과정을 논리적으로 쓰는 연습이 필수입니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{school} 내신은 서술형 대비가 핵심입니다. 풀이 과정을 체계적으로 쓰는 연습을 집중적으로 합니다.
</div>
"""
            elif school == "경성고":
                school_sections += f"""
### {school} 수학 내신의 특징

{school}은 연남동에 위치한 사립 고등학교입니다. 홍대 인근의 문화적 분위기와 함께 학업에도 충실한 학교입니다. 내신에서 기본 문제와 응용 문제가 균형 있게 출제됩니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{school} 기출문제를 철저히 분석합니다. 자주 출제되는 유형을 파악하고 집중 연습합니다.
</div>
"""
            elif school == "홍익대부속여고":
                school_sections += f"""
### {school} 수학 내신의 특징

{school}은 홍익대학교 사범대학 부속 여자 고등학교입니다. 대학 부속 학교답게 교육의 질이 높고, 내신 시험도 체계적입니다. 심화 문제가 출제되어 깊이 있는 이해가 필요합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{school} 기출문제를 철저히 분석합니다. 사대부속 특성에 맞춘 심화 학습도 병행합니다.
</div>
"""
            elif school == "상암고":
                school_sections += f"""
### {school} 수학 내신의 특징

{school}은 상암동 디지털미디어시티 인근에 위치한 마포구 유일의 공립 일반고입니다. 남녀공학으로 다양한 학생들이 있습니다. 내신에서 기본 개념 문제와 응용 문제가 균형 있게 출제됩니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{school} 기출문제를 분석하여 출제 경향을 파악합니다. 교과서 완벽 이해를 기본으로 응용력을 키웁니다.
</div>
"""
            else:
                school_sections += f"""
### {school} 수학 내신의 특징

{school}은 마포구에 위치한 고등학교입니다. 내신 시험에서 기본 개념 문제와 응용 문제가 균형 있게 출제됩니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{school} 기출문제를 분석하여 자주 나오는 유형을 파악합니다. 선생님별 출제 스타일까지 고려한 맞춤 대비를 합니다.
</div>
"""
        elif i == 1:
            school_sections += f"""
### {school} 수학 내신의 특징

{school}은 마포구에 위치한 고등학교입니다. 내신 시험에서 기본 개념 문제와 응용 문제가 출제됩니다. 개념을 정확히 이해하고 다양한 문제를 풀어보는 것이 중요합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{school}의 기출문제를 집중 분석합니다. 취약 유형을 파악하고 반복 훈련으로 실력을 키웁니다.
</div>
"""

    content = f'''---
title: "마포구 {dong_name} 고등 수학과외 | {school_list} {title_suffix}"
date: 2025-01-29
categories:
  - 고등교육
regions:
  - 서울
cities:
  - 마포구
description: "마포구 {dong_name} 고등학생 수학과외 전문. {school_list} 내신과 수능 맞춤 관리. 개념부터 심화까지 체계적 1:1 지도."
tags:
  - {dong_name}
  - 마포구
  - 고등수학
  - 수학과외
  - 내신관리
  - 수능수학
{school_tags}
  - 수학개념
  - 수학심화
  - 서부교육지원청
featured_image: "https://images.unsplash.com/{image}?w=1200&h=630&fit=crop"

---
## 마포구 {dong_name} 고등학생, {intro_title}

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

마포구 {dong_name} 고등학생 수학과외 수업료는 다음과 같습니다.

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

마포구 {dong_name}에서 고등학생 수학과외를 찾고 계신다면, 지금 바로 상담받아보세요. {school_list} 내신과 수능에 맞춘 1:1 맞춤 수업으로 수학 실력을 확실히 올려드립니다.
'''
    return content


def create_mapo_english_content(dong_info, index):
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
            if school == "숭문고":
                school_sections += f"""
### {school} 영어 내신의 특징

{school}은 1906년 개교한 마포구의 전통 있는 사립 고등학교입니다. 영어 교육에서도 체계적인 시스템을 갖추고 있습니다. 교과서 본문 암기가 기본이며, 문법과 독해 문제가 균형 있게 출제됩니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{school} 영어 교과서를 집중 분석합니다. 본문 암기, 핵심 문법 정리, 서술형 대비를 체계적으로 진행합니다.
</div>
"""
            elif school == "광성고":
                school_sections += f"""
### {school} 영어 내신의 특징

{school}은 신수동에 위치한 사립 고등학교입니다. 서강대학교 인근에 위치하여 학구적인 분위기가 있습니다. 영어 내신에서 교과서 본문 암기와 문법 이해가 핵심입니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{school} 기출문제를 분석하여 출제 경향을 파악합니다. 본문 완벽 정리와 핵심 문법 학습을 병행합니다.
</div>
"""
            elif school == "서울여고":
                school_sections += f"""
### {school} 영어 내신의 특징

{school}은 염리동에 위치한 여자 사립 고등학교입니다. 영어 내신 경쟁이 치열하며, 꼼꼼한 암기와 정확한 문법 지식이 요구됩니다. 서술형에서 실수를 줄이는 것이 중요합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{school} 내신은 정확성이 핵심입니다. 자주 틀리는 표현을 정리하고, 서술형 답안 작성 연습을 집중적으로 합니다.
</div>
"""
            elif school == "경성고":
                school_sections += f"""
### {school} 영어 내신의 특징

{school}은 연남동에 위치한 사립 고등학교입니다. 홍대 인근의 문화적 분위기와 함께 학업에도 충실한 학교입니다. 교과서 본문 중심의 출제가 이루어집니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{school} 기출문제를 철저히 분석합니다. 본문 암기와 핵심 문법을 체계적으로 정리합니다.
</div>
"""
            elif school == "홍익대부속여고":
                school_sections += f"""
### {school} 영어 내신의 특징

{school}은 홍익대학교 사범대학 부속 여자 고등학교입니다. 대학 부속 학교답게 영어 교육 수준이 높습니다. 교과서 본문뿐 아니라 심화 독해 지문도 출제됩니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{school} 영어는 심화 학습이 필요합니다. 교과서 완벽 정리와 함께 추가 독해 연습을 병행합니다.
</div>
"""
            elif school == "상암고":
                school_sections += f"""
### {school} 영어 내신의 특징

{school}은 상암동 디지털미디어시티 인근에 위치한 마포구 유일의 공립 일반고입니다. 교과서 본문 암기가 핵심이며, 본문에 나온 문법과 표현이 시험에 출제됩니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{school} 영어 교과서를 집중 분석합니다. 본문 암기와 핵심 문법 정리를 체계적으로 진행합니다.
</div>
"""
            else:
                school_sections += f"""
### {school} 영어 내신의 특징

{school}은 마포구에 위치한 고등학교입니다. 교과서 본문 암기가 핵심이며, 본문에 나온 표현과 문법 사항이 그대로 시험에 출제됩니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{school} 영어 교과서를 집중 분석합니다. 본문 암기, 핵심 문법 정리, 서술형 대비를 체계적으로 진행합니다.
</div>
"""
        elif i == 1:
            school_sections += f"""
### {school} 영어 내신의 특징

{school}은 마포구에 위치한 고등학교입니다. 교과서 본문 중심으로 출제되며, 핵심 문법과 어휘를 확실히 익혀야 합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{school}의 기출 문제를 분석하여 출제 경향을 파악합니다. 취약 유형을 집중 보완합니다.
</div>
"""

    content = f'''---
title: "마포구 {dong_name} 고등 영어과외 | {school_list} {title_suffix}"
date: 2025-01-29
categories:
  - 고등교육
regions:
  - 서울
cities:
  - 마포구
description: "마포구 {dong_name} 고등학생 영어과외 전문. {school_list} 내신과 수능 맞춤 관리. 문법·독해·어휘 체계적 1:1 지도."
tags:
  - {dong_name}
  - 마포구
  - 고등영어
  - 영어과외
  - 내신관리
  - 수능영어
{school_tags}
  - 영어문법
  - 영어독해
  - 서부교육지원청
featured_image: "https://images.unsplash.com/{image}?w=1200&h=630&fit=crop"

---
## 마포구 {dong_name} 고등학생, {intro_title}

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

마포구 {dong_name} 고등학생 영어과외 수업료는 다음과 같습니다.

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

마포구 {dong_name}에서 고등학생 영어과외를 찾고 계신다면, 지금 바로 상담받아보세요. {school_list} 내신과 수능에 맞춘 1:1 맞춤 수업으로 영어 실력을 확실히 올려드립니다.
'''
    return content


def main():
    output_dir = "content/high"
    created_files = []

    for i, dong in enumerate(MAPO_DONGS):
        # 수학 파일 생성
        math_filename = f"mapo-{dong['id']}-high-math.md"
        math_filepath = os.path.join(output_dir, math_filename)
        math_content = create_mapo_math_content(dong, i)

        with open(math_filepath, 'w', encoding='utf-8') as f:
            f.write(math_content)
        created_files.append(math_filename)

        # 영어 파일 생성
        english_filename = f"mapo-{dong['id']}-high-english.md"
        english_filepath = os.path.join(output_dir, english_filename)
        english_content = create_mapo_english_content(dong, i)

        with open(english_filepath, 'w', encoding='utf-8') as f:
            f.write(english_content)
        created_files.append(english_filename)

    print(f"마포구 고등: {len(created_files)}개 파일 생성 완료")
    for f in created_files[:5]:
        print(f"  - {f}")
    if len(created_files) > 5:
        print(f"  ... 외 {len(created_files) - 5}개")


if __name__ == "__main__":
    main()
