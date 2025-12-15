#!/usr/bin/env python3
"""성동구 고등 수학/영어 과외 콘텐츠 생성 스크립트"""

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
    ("수학 성적이 안 오른다면", "고등학교 수학, 열심히 하는데도 성적이 오르지 않나요?"),
    ("수학이 갑자기 어려워졌다면", "중학교 때는 잘했는데 고등학교 와서 수학이 안 되기 시작했나요?"),
    ("내신이 걱정된다면", "학교 내신 수학 시험, 어떻게 준비해야 할지 막막하신가요?"),
    ("수능 수학이 두렵다면", "수능 수학 1등급, 어떻게 하면 받을 수 있을까요?"),
    ("킬러문항이 안 풀린다면", "21번, 29번, 30번 킬러 문항에서 막히시나요?"),
    ("개념이 헷갈린다면", "개념은 아는 것 같은데 문제가 안 풀리시나요?"),
    ("시간이 부족하다면", "문제 푸는 속도가 느려서 시험 시간이 부족하신가요?"),
    ("수학 때문에 대입이 걱정된다면", "수학 성적 때문에 원하는 대학에 못 갈까봐 걱정되시나요?"),
    ("기초가 흔들린다면", "고등학교 수학, 기초부터 다시 잡고 싶으신가요?"),
    ("실력이 정체되어 있다면", "수학 성적이 더 이상 오르지 않아 답답하신가요?"),
    ("학원에서 효과를 못 봤다면", "학원 다녔는데 성적이 그대로라면 1:1 맞춤이 답입니다."),
    ("수포자가 될 것 같다면", "수학을 포기하고 싶으신가요? 포기하기엔 아직 이릅니다."),
    ("고3인데 시간이 없다면", "입시까지 시간이 없다면 전략적으로 준비해야 합니다."),
    ("모의고사 등급이 안 나온다면", "모의고사 성적이 안 나와서 걱정이신가요?"),
    ("심화가 안 된다면", "기본은 되는데 심화 문제에서 막히시나요?"),
    ("서술형이 어렵다면", "내신 서술형 문제, 어떻게 접근해야 할지 모르겠다면"),
    ("등급이 오르락내리락한다면", "수학 성적이 들쭉날쭉해서 불안하신가요?"),
]

ENGLISH_INTROS = [
    ("영어 성적이 안 오른다면", "고등학교 영어, 열심히 하는데도 성적이 오르지 않나요?"),
    ("영어가 갑자기 어려워졌다면", "중학교 때는 잘했는데 고등학교 와서 영어가 안 되기 시작했나요?"),
    ("내신이 걱정된다면", "학교 내신 영어 시험, 어떻게 준비해야 할지 막막하신가요?"),
    ("수능 영어가 두렵다면", "수능 영어 1등급, 어떻게 하면 받을 수 있을까요?"),
    ("독해가 느리다면", "지문을 읽는 속도가 느려서 시간이 부족하신가요?"),
    ("문법이 헷갈린다면", "문법은 아는 것 같은데 문제에 적용이 안 되시나요?"),
    ("듣기가 안 된다면", "듣기 평가에서 점수가 잘 안 나오시나요?"),
    ("영어 때문에 대입이 걱정된다면", "영어 성적 때문에 원하는 대학에 못 갈까봐 걱정되시나요?"),
    ("어휘가 부족하다면", "단어를 외워도 금방 잊어버리시나요?"),
    ("실력이 정체되어 있다면", "영어 성적이 더 이상 오르지 않아 답답하신가요?"),
    ("학원에서 효과를 못 봤다면", "학원 다녔는데 성적이 그대로라면 1:1 맞춤이 답입니다."),
    ("영포자가 될 것 같다면", "영어를 포기하고 싶으신가요? 포기하기엔 아직 이릅니다."),
    ("고3인데 시간이 없다면", "입시까지 시간이 없다면 전략적으로 준비해야 합니다."),
    ("모의고사 등급이 안 나온다면", "모의고사 성적이 안 나와서 걱정이신가요?"),
    ("빈칸추론이 어렵다면", "빈칸 추론 문제에서 자주 틀리시나요?"),
    ("서술형이 어렵다면", "내신 서술형 문제, 어떻게 접근해야 할지 모르겠다면"),
    ("등급이 오르락내리락한다면", "영어 성적이 들쭉날쭉해서 불안하신가요?"),
]

# 성동구 17개 행정동 (고등학교 정보 포함)
SEONGDONG_DONGS = [
    {"id": "wangsimni-doseondong", "name": "왕십리도선동", "schools": ["무학여고", "한양대부고"], "math_suffix": "내신·수능 대비", "eng_suffix": "독해·문법 완성"},
    {"id": "wangsimni2", "name": "왕십리2동", "schools": ["무학여고", "한양대부고"], "math_suffix": "맞춤 커리큘럼", "eng_suffix": "1:1 맞춤 수업"},
    {"id": "majang", "name": "마장동", "schools": ["경일고", "성수고"], "math_suffix": "기초부터 심화까지", "eng_suffix": "체계적 학습 관리"},
    {"id": "sageun", "name": "사근동", "schools": ["한양대부고"], "math_suffix": "학교별 내신 특화", "eng_suffix": "실력 향상 수업"},
    {"id": "haengdang1", "name": "행당1동", "schools": ["무학여고", "한양대부고"], "math_suffix": "1:1 맞춤 수업", "eng_suffix": "내신·수능 대비"},
    {"id": "haengdang2", "name": "행당2동", "schools": ["무학여고", "한양대부고"], "math_suffix": "개념부터 실전까지", "eng_suffix": "맞춤 커리큘럼"},
    {"id": "eungbong", "name": "응봉동", "schools": ["경일고", "성수고"], "math_suffix": "실력 향상 수업", "eng_suffix": "기초부터 심화까지"},
    {"id": "geumho1ga", "name": "금호1가동", "schools": ["경일고", "성수고"], "math_suffix": "체계적 학습 관리", "eng_suffix": "학교별 내신 특화"},
    {"id": "geumho2-3ga", "name": "금호2·3가동", "schools": ["경일고", "성수고"], "math_suffix": "내신·수능 대비", "eng_suffix": "독해·문법 완성"},
    {"id": "geumho4ga", "name": "금호4가동", "schools": ["경일고", "성수고"], "math_suffix": "맞춤 커리큘럼", "eng_suffix": "1:1 맞춤 수업"},
    {"id": "oksu", "name": "옥수동", "schools": ["경일고", "성수고"], "math_suffix": "기초부터 심화까지", "eng_suffix": "체계적 학습 관리"},
    {"id": "seongsu1ga1", "name": "성수1가1동", "schools": ["경일고", "성수고"], "math_suffix": "학교별 내신 특화", "eng_suffix": "실력 향상 수업"},
    {"id": "seongsu1ga2", "name": "성수1가2동", "schools": ["경일고", "성수고"], "math_suffix": "1:1 맞춤 수업", "eng_suffix": "내신·수능 대비"},
    {"id": "seongsu2ga1", "name": "성수2가1동", "schools": ["성수고", "경일고"], "math_suffix": "개념부터 실전까지", "eng_suffix": "맞춤 커리큘럼"},
    {"id": "seongsu2ga3", "name": "성수2가3동", "schools": ["성수고", "경일고"], "math_suffix": "실력 향상 수업", "eng_suffix": "기초부터 심화까지"},
    {"id": "songjeong", "name": "송정동", "schools": ["성수고", "경일고"], "math_suffix": "체계적 학습 관리", "eng_suffix": "학교별 내신 특화"},
    {"id": "yongdap", "name": "용답동", "schools": ["성수고", "경일고"], "math_suffix": "내신·수능 대비", "eng_suffix": "독해·문법 완성"},
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
        if sch == "한양대부고":
            desc = f"{sch}는 한양대학교 사범대학 부속 고등학교입니다. 대학 부속 학교답게 교육 수준이 높고, 내신 시험 난이도도 상당합니다. 심화 개념과 고난도 문제가 출제되어 철저한 준비가 필요합니다."
        elif sch == "무학여고":
            desc = f"{sch}는 왕십리에 위치한 여자고등학교입니다. 교과서 중심의 출제 경향을 보이며, 기본 개념의 이해와 응용력을 함께 평가합니다. 서술형 비중이 높아 풀이 과정도 꼼꼼히 준비해야 합니다."
        elif sch == "경일고":
            desc = f"{sch}는 성동구에 위치한 남자고등학교입니다. 전통적인 명문고로 내신 시험의 변별력이 높습니다. 기본 문제와 심화 문제가 균형 있게 출제됩니다."
        elif sch == "성수고":
            desc = f"{sch}는 성수동에 위치한 남녀공학 고등학교입니다. 서울숲과 성수동 개발지역 인근에 위치하여 젊은 학부모가 많고 교육열이 높습니다. 내신 시험은 교과서 중심으로 출제됩니다."
        else:
            desc = f"{sch}은 성동구에 위치한 고등학교입니다. 내신 시험은 교과서 중심의 기본 문제와 응용 문제가 균형 있게 출제됩니다."

        school_section += f"""
### {sch} 수학 내신의 특징

{desc}

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{sch} 기출문제를 철저히 분석하여 출제 경향을 파악합니다. 자주 출제되는 유형과 고난도 문제를 집중적으로 연습합니다.
</div>
"""

    return f'''---
title: "성동구 {name} 고등 수학과외 | {school_list} {dong["math_suffix"]}"
date: 2025-01-29
categories:
  - 고등교육
regions:
  - 서울
cities:
  - 성동구
description: "성동구 {name} 고등학생 수학과외 전문. {school_list} 내신 및 수능 맞춤 관리. 개념부터 킬러문항까지 체계적 1:1 지도."
tags:
  - {name}
  - 성동구
  - 고등수학
  - 수학과외
  - 내신관리
  - 수능대비
{tags}
  - 수학개념
  - 킬러문항
  - 성동광진교육지원청
featured_image: "https://images.unsplash.com/{img}?w=1200&h=630&fit=crop"

---
## 성동구 {name} 고등학생, {intro_t}

{intro_d} {name}에서 고등학생 자녀의 수학 성적 때문에 고민하시는 학부모님이 많습니다. 학원에 보내도 성적이 오르지 않는 이유는 학생 개인의 취약점을 정확히 파악하지 못했기 때문입니다.

1:1 맞춤 과외는 학생의 현재 상태를 정확히 진단하는 것에서 시작합니다. 어떤 단원에서 막히는지, 어떤 유형에서 실수가 나오는지 파악합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
첫 수업에서 학생의 수학 실력을 꼼꼼히 진단합니다. 단원별로 개념 이해도를 체크하고, 최근 시험지를 분석하여 취약점을 파악합니다.
</div>

## 고등학교 수학이 어려운 이유

고등학교 수학은 중학교와 차원이 다릅니다. 추상적인 개념이 많아지고, 여러 개념을 복합적으로 적용해야 하는 문제가 출제됩니다.

성동구는 한양대학교가 위치한 교육 중심 지역입니다. 왕십리 부도심과 성수동 IT산업 밀집지역의 발전으로 젊은 학부모가 늘어나며 교육열이 높아지고 있습니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
현재 단원의 개념을 완벽히 이해했는지 확인한 후 다음으로 넘어갑니다. 학생이 직접 설명할 수 있어야 진짜 아는 것입니다.
</div>

## 내신과 수능, 두 마리 토끼 잡기

### 내신 대비 전략

학교 내신은 교과서와 프린트 중심으로 출제됩니다. 학교별로 출제 경향이 다르기 때문에 해당 학교의 기출문제 분석이 필수입니다.

### 수능 대비 전략

수능 수학은 사고력과 응용력이 핵심입니다. 킬러 문항인 21번, 29번, 30번을 풀 수 있느냐가 1등급과 2등급을 가릅니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
내신 기간에는 학교별 기출 분석에 집중하고, 평소에는 수능형 문제로 실력을 쌓아갑니다.
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

### 고등학교 1학년

수학의 기초를 다지는 가장 중요한 시기입니다. 다항식, 방정식과 부등식, 도형의 방정식의 개념을 완벽히 익혀야 합니다.

### 고등학교 2학년

수학의 핵심 시기입니다. 수학I, 수학II의 핵심인 지수함수, 로그함수, 삼각함수, 미적분의 기초를 확실히 잡아야 합니다.

### 고등학교 3학년

수능을 앞둔 마무리 시기입니다. 미적분, 기하, 확률과 통계 중 선택과목을 정하고 집중적으로 대비해야 합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
학년별 핵심 단원을 체계적으로 정리합니다. 다음 학년으로 연결되는 핵심 개념은 반드시 완벽히 마스터하고 넘어갑니다.
</div>

## 수업료 안내

성동구 {name} 고등학생 수학과외 수업료는 다음과 같습니다.

**고1~2**는 주1회 기준 25만원에서 35만원, 주2회 기준 42만원에서 58만원 선입니다.

**고3**은 주1회 기준 30만원에서 42만원, 주2회 기준 50만원에서 70만원이 일반적입니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
첫 상담에서 학생의 현재 수준과 목표를 파악하고, 적합한 수업 계획과 수업료를 안내드립니다.
</div>

{{{{< cta-dual type="final" >}}}}

## 자주 묻는 질문

**Q. 내신과 수능 중 어떤 것을 먼저 준비해야 하나요?**

학년에 따라 다릅니다. 고1~2는 내신에 집중하면서 수능 감각을 유지하고, 고3은 내신과 수능을 병행합니다.

**Q. 수학 기초가 많이 부족한데 따라갈 수 있을까요?**

기초가 부족한 학생일수록 1:1 과외가 효과적입니다. 어디서부터 막혔는지 정확히 진단하고, 그 부분부터 차근차근 다시 설명합니다.

**Q. 수업은 어디서 진행하나요?**

학생의 집으로 방문하거나, 스터디카페, 도서관 등 학생이 편한 장소에서 수업합니다. 온라인 수업도 가능합니다.

## 마무리

성동구 {name}에서 고등학생 수학과외를 찾고 계신다면, 지금 바로 상담받아보세요. {school_list} 내신과 수능에 맞춘 1:1 맞춤 수업으로 수학 실력을 확실히 올려드립니다.
'''

def create_english_content(dong, idx):
    name, schools = dong["name"], dong["schools"]
    school_list, tags = get_school_list(schools), get_school_tags(schools)
    img = ENGLISH_IMAGES[idx % len(ENGLISH_IMAGES)]
    intro_t, intro_d = ENGLISH_INTROS[idx % len(ENGLISH_INTROS)]

    school_section = ""
    for i, sch in enumerate(schools[:2]):
        if sch == "한양대부고":
            desc = f"{sch}는 한양대학교 사범대학 부속 고등학교입니다. 대학 부속 학교답게 영어 교육 수준이 높습니다. 심화 독해 지문이 출제되며, 서술형 비중이 높아 정확한 문법 지식과 작문 능력이 필요합니다."
        elif sch == "무학여고":
            desc = f"{sch}는 왕십리에 위치한 여자고등학교입니다. 교과서 본문과 부교재 중심의 출제 경향을 보입니다. 본문 암기가 핵심이며, 변형 문제에 대비해야 합니다."
        elif sch == "경일고":
            desc = f"{sch}는 성동구에 위치한 남자고등학교입니다. 전통적인 명문고로 영어 시험의 변별력이 높습니다. 교과서와 부교재를 꼼꼼히 학습해야 합니다."
        elif sch == "성수고":
            desc = f"{sch}는 성수동에 위치한 남녀공학 고등학교입니다. 내신 시험은 교과서 중심으로 출제되며, 본문 암기와 문법 문제가 핵심입니다."
        else:
            desc = f"{sch}은 성동구에 위치한 고등학교입니다. 교과서 본문 암기가 핵심이며, 본문에 나온 표현과 문법 사항이 그대로 시험에 출제됩니다."

        school_section += f"""
### {sch} 영어 내신의 특징

{desc}

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{sch} 영어 교과서와 부교재를 집중 분석합니다. 본문 암기, 핵심 문법 정리, 서술형 대비를 체계적으로 진행합니다.
</div>
"""

    return f'''---
title: "성동구 {name} 고등 영어과외 | {school_list} {dong["eng_suffix"]}"
date: 2025-01-29
categories:
  - 고등교육
regions:
  - 서울
cities:
  - 성동구
description: "성동구 {name} 고등학생 영어과외 전문. {school_list} 내신 및 수능 맞춤 관리. 독해·문법·어휘 체계적 1:1 지도."
tags:
  - {name}
  - 성동구
  - 고등영어
  - 영어과외
  - 내신관리
  - 수능대비
{tags}
  - 영어독해
  - 영어문법
  - 성동광진교육지원청
featured_image: "https://images.unsplash.com/{img}?w=1200&h=630&fit=crop"

---
## 성동구 {name} 고등학생, {intro_t}

{intro_d} {name}에서 고등학생 자녀의 영어 성적 때문에 고민하시는 학부모님이 많습니다. 단어도 외우고 문법책도 풀었는데 성적이 안 오르면 학습 방향이 잘못된 겁니다.

1:1 맞춤 과외는 학생의 현재 상태를 정확히 진단하는 것에서 시작합니다. 문법이 약한지, 독해가 약한지, 어휘가 부족한지를 파악합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
첫 수업에서 학생의 영어 실력을 영역별로 진단합니다. 문법, 독해, 어휘, 쓰기 중 어디가 약한지 파악하고, 맞춤 학습 계획을 세웁니다.
</div>

## 고등학교 영어가 어려운 이유

고등학교 영어는 중학교와 차원이 다릅니다. 지문의 길이가 길어지고, 추상적인 내용을 다루는 글이 많아집니다.

성동구는 한양대학교가 위치한 교육 중심 지역입니다. 대학가의 학구적인 분위기와 함께 영어 교육에 대한 관심도 높습니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
문법을 단순 암기가 아닌 원리로 접근합니다. 왜 그런 규칙이 있는지 이해하면 오래 기억되고 응용도 됩니다.
</div>

## 내신과 수능, 두 마리 토끼 잡기

### 내신 대비 전략

학교 내신은 교과서와 부교재 중심으로 출제됩니다. 본문 암기가 기본이고, 변형 문제에 대비해야 합니다.

### 수능 대비 전략

수능 영어는 독해력과 시간 관리가 핵심입니다. 다양한 유형의 지문을 빠르고 정확하게 읽는 훈련이 필요합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
내신 기간에는 학교별 기출 분석과 본문 암기에 집중하고, 평소에는 수능형 독해 문제로 실력을 쌓아갑니다.
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

### 고등학교 1학년

영어의 기초를 다지는 중요한 시기입니다. 복잡한 문장 구조를 분석하는 능력과 기본 어휘력을 탄탄히 쌓아야 합니다.

### 고등학교 2학년

영어 실력을 본격적으로 높이는 시기입니다. 수능 유형에 익숙해지고, 다양한 주제의 지문을 접해야 합니다.

### 고등학교 3학년

수능을 앞둔 마무리 시기입니다. EBS 연계 교재를 학습하고, 실전 감각을 키워야 합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
학년별 핵심 영역을 체계적으로 정리합니다. 빈틈없이 마무리한 후 다음 단계로 넘어갑니다.
</div>

## 수업료 안내

성동구 {name} 고등학생 영어과외 수업료는 다음과 같습니다.

**고1~2**는 주1회 기준 22만원에서 32만원, 주2회 기준 38만원에서 52만원 선입니다.

**고3**은 주1회 기준 28만원에서 38만원, 주2회 기준 45만원에서 62만원이 일반적입니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
첫 상담에서 학생의 현재 수준과 목표를 파악하고, 적합한 수업 계획과 수업료를 안내드립니다.
</div>

{{{{< cta-dual type="final" >}}}}

## 자주 묻는 질문

**Q. 내신과 수능 중 어떤 것을 먼저 준비해야 하나요?**

학년에 따라 다릅니다. 고1~2는 내신에 집중하면서 수능 감각을 유지하고, 고3은 내신과 수능을 병행합니다.

**Q. 영어 기초가 많이 부족한데 따라갈 수 있을까요?**

기초가 부족한 학생일수록 1:1 과외가 효과적입니다. 어디서부터 막혔는지 정확히 진단하고, 그 부분부터 차근차근 다시 설명합니다.

**Q. 수업은 어디서 진행하나요?**

학생의 집으로 방문하거나, 스터디카페, 도서관 등 학생이 편한 장소에서 수업합니다. 온라인 수업도 가능합니다.

## 마무리

성동구 {name}에서 고등학생 영어과외를 찾고 계신다면, 지금 바로 상담받아보세요. {school_list} 내신과 수능에 맞춘 1:1 맞춤 수업으로 영어 실력을 확실히 올려드립니다.
'''

def main():
    os.makedirs("content/high", exist_ok=True)
    files = []
    for i, dong in enumerate(SEONGDONG_DONGS):
        for subj, func in [("math", create_math_content), ("english", create_english_content)]:
            fn = f"seongdong-{dong['id']}-high-{subj}.md"
            with open(f"content/high/{fn}", 'w', encoding='utf-8') as f:
                f.write(func(dong, i))
            files.append(fn)
    print(f"성동구 고등: {len(files)}개 파일 생성 완료")

if __name__ == "__main__":
    main()
