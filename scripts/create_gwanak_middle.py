#!/usr/bin/env python3
"""관악구 중등 수학/영어 과외 콘텐츠 생성 스크립트"""

import os

# 관악구 동별 정보
GWANAK_DONGS = [
    {"id": "boramae", "name": "보라매동", "schools": ["당곡중"]},
    {"id": "euncheon", "name": "은천동", "schools": ["구암중", "봉원중"]},
    {"id": "seonghyeon", "name": "성현동", "schools": ["구암중", "봉원중"]},
    {"id": "cheongnyong", "name": "청룡동", "schools": ["봉림중"]},
    {"id": "haengun", "name": "행운동", "schools": ["관악중"]},
    {"id": "nakseongdae", "name": "낙성대동", "schools": ["인헌중"]},
    {"id": "inheon", "name": "인헌동", "schools": ["인헌중"]},
    {"id": "jungang", "name": "중앙동", "schools": ["서울문영여자중"]},
    {"id": "sillim", "name": "신림동", "schools": ["신림중"]},
    {"id": "sinsa", "name": "신사동", "schools": ["신관중"]},
    {"id": "jowon", "name": "조원동", "schools": ["남강중"]},
    {"id": "daehak", "name": "대학동", "schools": ["삼성중"]},
    {"id": "miseong", "name": "미성동", "schools": ["남서울중", "미성중", "성보중"]},
    {"id": "nangok", "name": "난곡동", "schools": ["난우중", "남강중"]},
    {"id": "nanhyang", "name": "난향동", "schools": ["난우중"]},
    {"id": "seowon", "name": "서원동", "schools": ["신림중", "삼성중"]},
    {"id": "sinwon", "name": "신원동", "schools": ["신림중", "삼성중"]},
    {"id": "seorim", "name": "서림동", "schools": ["신림중", "삼성중"]},
    {"id": "samseong", "name": "삼성동", "schools": ["삼성중"]},
    {"id": "namhyeon", "name": "남현동", "schools": ["인헌중", "봉림중"]},
]

# 이미지 풀 (중복 방지용)
MATH_IMAGES = [
    "photo-1596495578065-6e0763fa1178",
    "photo-1509228468518-180dd4864904",
    "photo-1518133910546-b6c2fb7d79e3",
    "photo-1453733190371-0a9bedd82893",
    "photo-1596495577886-d920f1fb7238",
    "photo-1611532736597-de2d4265fba3",
    "photo-1580894894513-541e068a3e2b",
    "photo-1613909207039-6b173b755cc1",
    "photo-1559494007-9f5847c49d94",
    "photo-1544383835-bda2bc66a55d",
    "photo-1611329857570-f02f340e7378",
    "photo-1512314889357-e157c22f938d",
    "photo-1516796181074-bf453fbfa3e6",
    "photo-1515879218367-8466d910aaa4",
    "photo-1554475901-4538ddfbccc2",
    "photo-1581078426770-6d336e5de7bf",
    "photo-1611348586804-61bf6c080437",
    "photo-1611348524140-53c9a25263d6",
    "photo-1611351888222-c5797b8b5c2f",
    "photo-1596495577933-6c64e3a7d20a",
]

ENGLISH_IMAGES = [
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
    "photo-1507842217343-583bb7270b66",
    "photo-1497633762265-9d179a990aa6",
    "photo-1516979187457-637abb4f9353",
    "photo-1512820790803-83ca734da794",
    "photo-1550399105-c4db5fb85c18",
]

# 서두 변형 (수학) - 관악구용 새로운 변형
MATH_INTROS = [
    "수학 문제만 보면 머리가 하얘지나요?",
    "개념은 알겠는데 응용이 안 되나요?",
    "학원 진도는 빠른데 성적이 안 따라오나요?",
    "시험 때만 되면 아는 문제도 틀리나요?",
    "수학 공부에 투자하는 시간 대비 성과가 없나요?",
    "수학 자신감이 바닥을 치고 있나요?",
    "중학교 수학이 갑자기 어려워졌나요?",
    "수학 때문에 전체 성적이 발목 잡히나요?",
    "문제집은 많이 풀었는데 실력이 안 느나요?",
    "계산 실수가 너무 잦아서 걱정되나요?",
    "서술형 문제에서 점수를 많이 깎이나요?",
    "수학 포기를 생각해본 적 있나요?",
    "학원에서는 이해가 됐는데 혼자 풀면 모르겠나요?",
    "수학 성적이 항상 제자리걸음인가요?",
    "기초부터 다시 잡아야 할 것 같나요?",
    "수학 때문에 고등학교 진학이 걱정되나요?",
    "방정식이 나오면서 수학이 싫어졌나요?",
    "그래프 문제만 나오면 막막한가요?",
    "수학 학원을 여러 번 옮겨봤지만 소용없나요?",
    "수학 점수가 80점의 벽을 못 넘나요?",
]

# 서두 변형 (영어) - 관악구용 새로운 변형
ENGLISH_INTROS = [
    "영어 지문이 길어지니 읽기 싫어하나요?",
    "단어는 외워도 문장이 해석이 안 되나요?",
    "문법 규칙이 너무 많아 헷갈리나요?",
    "영어 시험 시간이 항상 부족한가요?",
    "영어 성적이 오르락내리락 불안정한가요?",
    "영어 공부 방법을 몰라 답답한가요?",
    "영어 때문에 전체 등급이 낮아지고 있나요?",
    "학원 수업을 따라가기 버거워하나요?",
    "영어 자신감이 점점 사라지고 있나요?",
    "중학교 영어가 생각보다 어려운가요?",
    "문법은 외웠는데 적용이 안 되나요?",
    "영어 서술형에서 감점이 많나요?",
    "독해 지문을 읽어도 내용 파악이 안 되나요?",
    "영어 단어 암기가 너무 힘드나요?",
    "영어 때문에 고등학교 준비가 걱정되나요?",
    "관계대명사가 나오면서 포기하고 싶어졌나요?",
    "영어 학원 숙제만 하다가 시간이 다 가나요?",
    "영어 점수가 좀처럼 오르지 않나요?",
    "영어 공부를 어디서부터 시작해야 할지 모르겠나요?",
    "문장 구조 파악이 안 돼서 해석이 어려운가요?",
]

def get_school_list_text(schools):
    """학교 목록을 텍스트로 변환"""
    if len(schools) == 1:
        return schools[0]
    elif len(schools) == 2:
        return f"{schools[0]}·{schools[1]}"
    else:
        return "·".join(schools[:3])

def get_school_tags(schools):
    """학교명을 태그 형식으로 변환"""
    return "\n".join([f"  - {school}" for school in schools])

def create_math_content(dong_info, index):
    """수학 과외 콘텐츠 생성"""
    dong_id = dong_info["id"]
    dong_name = dong_info["name"]
    schools = dong_info["schools"]
    school_list = get_school_list_text(schools)
    school_tags = get_school_tags(schools)
    image = MATH_IMAGES[index % len(MATH_IMAGES)]
    intro = MATH_INTROS[index % len(MATH_INTROS)]

    # 학교별 특징 생성
    school_features = []
    for i, school in enumerate(schools[:2]):
        if i == 0:
            school_features.append(f"{school}은 교과서 중심의 기본 문제와 응용 문제를 균형 있게 출제합니다. 개념을 정확히 이해하고 다양한 유형을 연습하면 좋은 성적을 받을 수 있습니다.")
        else:
            school_features.append(f"{school}은 서술형 비중이 높은 편입니다. 풀이 과정을 논리적으로 작성하는 연습이 필요합니다. 계산 과정도 꼼꼼히 채점합니다.")

    school_feature_text = "\n\n".join(school_features)

    content = f'''---
title: "관악구 {dong_name} 중등 수학과외 | {school_list} 내신 완벽 대비"
date: 2025-01-29
categories:
  - 중등교육
regions:
  - 서울
cities:
  - 관악구
description: "관악구 {dong_name} 중학생 수학과외 전문. {school_list} 내신 맞춤 관리. 개념부터 심화까지 체계적 1:1 지도."
tags:
  - {dong_name}
  - 관악구
  - 중등수학
  - 수학과외
  - 내신관리
{school_tags}
  - 수학개념
  - 수학심화
  - 동작관악교육지원청
featured_image: "https://images.unsplash.com/{image}?w=1200&h=630&fit=crop"

---
## 관악구 {dong_name} 중학생, {intro}

{dong_name}에서 중학생 자녀의 수학 때문에 고민이 많으시죠. 학원도 보내보고 문제집도 풀려봤지만 성적이 오르지 않는다면, 학생 개인의 약점을 제대로 파악하지 못한 것일 수 있습니다. 1:1 맞춤 과외로 정확한 진단부터 시작해보세요.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
첫 수업에서 학생이 어느 단원에서 막히는지, 어떤 유형에서 실수하는지 정확히 진단합니다. 진단 결과를 바탕으로 맞춤 학습 계획을 세웁니다.
</div>

## 중학교 수학, 왜 중요한가

중학교 수학은 고등학교 수학의 뿌리입니다. 중학교 때 개념이 흔들리면 고등학교에서 바로잡기 어렵습니다. 특히 방정식, 함수, 도형의 기초가 완벽해야 고등학교 진도를 따라갈 수 있습니다.

관악구는 서울대학교 캠퍼스가 있는 교육 중심 지역입니다. 주변 학생들의 학업 수준이 높고 경쟁이 치열합니다. 내신에서 좋은 성적을 받으려면 탄탄한 기본기가 필수입니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
현재 배우는 단원의 개념을 완벽히 이해했는지 확인합니다. 빈틈이 있으면 바로 메우고 넘어갑니다.
</div>

## {school_list} 수학 시험의 특징

{school_feature_text}

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{school_list} 기출문제를 분석하여 자주 나오는 유형을 파악합니다. 학교 시험에 맞춘 전략적 대비를 합니다.
</div>

## 1:1 과외의 장점

학원은 정해진 진도대로 나갑니다. 학생이 이해하지 못해도 기다려주지 않습니다. 1:1 과외는 학생의 속도에 맞춥니다. 이해가 될 때까지 설명하고, 완전히 소화한 후 다음으로 넘어갑니다.

특히 기초가 부족하거나 특정 단원에서 막힌 학생에게 효과적입니다. 학원에서 놓친 부분을 1:1로 꼼꼼히 채워갈 수 있습니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
매 수업 학생이 배운 내용을 직접 설명해보게 합니다. 설명할 수 있어야 진짜 이해한 것입니다.
</div>

## 학년별 수학 공부법

중1은 정수와 유리수 연산, 문자와 식, 일차방정식의 기초를 다지는 시기입니다. 이 기초가 흔들리면 중2, 중3 수학이 어려워집니다.

중2는 연립방정식과 일차함수가 핵심입니다. 함수의 개념을 확실히 잡고, 그래프 해석 능력을 키워야 합니다. 고등학교 수학으로 연결되는 중요한 시기입니다.

중3은 이차방정식, 이차함수, 피타고라스 정리를 마스터해야 합니다. 내신 마무리와 함께 고등 수학 선행도 시작합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
학년별 핵심 단원을 체계적으로 정리합니다. 다음 학년 진도를 나가기 전에 현재 단원을 완벽히 마무리합니다.
</div>

## 수업료 안내

중학생 수학과외 수업료는 다음과 같습니다.

**중1~2**는 주1회 기준 18만원에서 25만원, 주2회 기준 32만원에서 45만원 선입니다.

**중3**은 주1회 기준 20만원에서 28만원, 주2회 기준 36만원에서 50만원이 일반적입니다.

수업 횟수, 시간, 선생님 경력에 따라 달라질 수 있습니다. 정확한 수업료는 상담을 통해 안내드립니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
첫 상담에서 학생의 현재 수준과 목표를 파악하고, 그에 맞는 수업 계획을 제안드립니다.
</div>

{{{{< cta-dual type="final" >}}}}

## 자주 묻는 질문

**Q. 수학 기초가 많이 약한데 따라갈 수 있나요?**

기초가 약한 학생일수록 1:1 과외가 효과적입니다. 어디서부터 막혔는지 진단하고, 그 부분부터 차근차근 다시 잡아드립니다. 학원에서는 불가능한 맞춤 지도입니다.

**Q. 시험 기간에만 수업을 늘릴 수 있나요?**

가능합니다. 평소에는 주1회로 개념을 잡고, 시험 2주 전부터 주2~3회로 늘려 집중 대비하는 방식도 많이 활용합니다.

**Q. 수업 장소는 어떻게 되나요?**

학생의 집, 스터디카페, 도서관 등 학생이 편한 곳에서 수업합니다. 온라인 수업도 가능합니다.

## 마무리

관악구 {dong_name}에서 중학생 수학과외를 찾고 계신다면, 지금 상담받아보세요. {school_list} 내신에 맞춘 1:1 맞춤 수업으로 수학 실력을 확실히 끌어올려 드립니다.
'''
    return content

def create_english_content(dong_info, index):
    """영어 과외 콘텐츠 생성"""
    dong_id = dong_info["id"]
    dong_name = dong_info["name"]
    schools = dong_info["schools"]
    school_list = get_school_list_text(schools)
    school_tags = get_school_tags(schools)
    image = ENGLISH_IMAGES[index % len(ENGLISH_IMAGES)]
    intro = ENGLISH_INTROS[index % len(ENGLISH_INTROS)]

    # 학교별 특징 생성
    school_features = []
    for i, school in enumerate(schools[:2]):
        if i == 0:
            school_features.append(f"{school}은 교과서 본문 암기와 문법 적용을 중시합니다. 본문에 나온 핵심 표현과 문법 규칙을 정확히 익히면 좋은 성적을 받을 수 있습니다.")
        else:
            school_features.append(f"{school}은 독해 지문의 난이도가 있는 편입니다. 교과서 외 지문도 연습하고, 다양한 유형의 문제에 익숙해지는 것이 중요합니다.")

    school_feature_text = "\n\n".join(school_features)

    content = f'''---
title: "관악구 {dong_name} 중등 영어과외 | {school_list} 내신 완벽 대비"
date: 2025-01-29
categories:
  - 중등교육
regions:
  - 서울
cities:
  - 관악구
description: "관악구 {dong_name} 중학생 영어과외 전문. {school_list} 내신 맞춤 관리. 문법·독해·어휘 체계적 1:1 지도."
tags:
  - {dong_name}
  - 관악구
  - 중등영어
  - 영어과외
  - 내신관리
{school_tags}
  - 영어문법
  - 영어독해
  - 동작관악교육지원청
featured_image: "https://images.unsplash.com/{image}?w=1200&h=630&fit=crop"

---
## 관악구 {dong_name} 중학생, {intro}

{dong_name}에서 중학생 자녀의 영어 성적 때문에 고민이시죠. 단어도 열심히 외우고 문법책도 풀었는데 성적이 안 오른다면, 학생의 약점을 정확히 파악하지 못한 것일 수 있습니다. 1:1 맞춤 과외로 영역별 진단부터 시작해보세요.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
첫 수업에서 문법, 독해, 어휘 영역별로 어디가 약한지 진단합니다. 약점을 파악한 후 집중 보완 계획을 세웁니다.
</div>

## 중학교 영어, 왜 중요한가

중학교 영어는 고등학교 영어의 기초입니다. 중학교 때 문법이 흔들리면 고등학교 독해가 어려워집니다. 수능 영어까지 이어지는 긴 싸움의 시작점이 바로 중학교 영어입니다.

관악구는 서울대학교가 있는 교육 중심 지역입니다. 주변 학생들의 영어 수준이 높고 경쟁이 치열합니다. 내신에서 좋은 성적을 받으려면 탄탄한 기본기가 필수입니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
문법을 단순 암기가 아닌 원리로 이해하게 합니다. 왜 그런 규칙이 있는지 알면 오래 기억됩니다.
</div>

## {school_list} 영어 시험의 특징

{school_feature_text}

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{school_list} 기출문제를 분석하여 출제 경향을 파악합니다. 학교 시험에 맞춘 전략적 대비를 합니다.
</div>

## 1:1 과외의 장점

학원은 정해진 커리큘럼대로 진도를 나갑니다. 학생이 이해하지 못해도 기다려주지 않습니다. 1:1 과외는 학생의 이해도에 맞춰 속도를 조절합니다.

특히 문법이 약하거나 독해에서 막히는 학생에게 효과적입니다. 어디서 막혔는지 정확히 찾아서 그 부분부터 다시 설명합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
매 수업 배운 문법을 활용해 직접 문장을 만들어보게 합니다. 직접 써봐야 내 것이 됩니다.
</div>

## 학년별 영어 공부법

중1은 기초 문법과 어휘를 다지는 시기입니다. 문장의 기본 구조를 이해하고, 핵심 어휘를 탄탄히 쌓아야 합니다.

중2는 준동사(to부정사, 동명사)와 관계대명사가 핵심입니다. 이 개념들이 고등학교 독해의 기초가 됩니다. 확실히 이해하고 넘어가야 합니다.

중3은 복합 문장 구조를 익히고 긴 지문 독해를 연습합니다. 내신 마무리와 함께 고등 영어 선행도 시작합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
학년별 핵심 문법을 체계적으로 정리합니다. 빈틈없이 마무리한 후 다음 단계로 넘어갑니다.
</div>

## 수업료 안내

중학생 영어과외 수업료는 다음과 같습니다.

**중1~2**는 주1회 기준 17만원에서 24만원, 주2회 기준 30만원에서 42만원 선입니다.

**중3**은 주1회 기준 19만원에서 26만원, 주2회 기준 34만원에서 48만원이 일반적입니다.

수업 횟수, 시간, 선생님 경력에 따라 달라질 수 있습니다. 정확한 수업료는 상담을 통해 안내드립니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
첫 상담에서 학생의 현재 수준과 목표를 파악하고, 그에 맞는 수업 계획을 제안드립니다.
</div>

{{{{< cta-dual type="final" >}}}}

## 자주 묻는 질문

**Q. 영어 기초가 많이 약한데 따라갈 수 있나요?**

기초가 약한 학생일수록 1:1 과외가 효과적입니다. 어디서부터 막혔는지 진단하고, 그 부분부터 차근차근 다시 잡아드립니다.

**Q. 시험 기간에만 수업을 늘릴 수 있나요?**

가능합니다. 평소에는 주1회로 기본을 잡고, 시험 전에 집중 대비하는 방식으로 운영할 수 있습니다.

**Q. 수업 장소는 어떻게 되나요?**

학생의 집, 스터디카페, 도서관 등 편한 곳에서 수업합니다. 온라인 수업도 가능합니다.

## 마무리

관악구 {dong_name}에서 중학생 영어과외를 찾고 계신다면, 지금 상담받아보세요. {school_list} 내신에 맞춘 1:1 맞춤 수업으로 영어 실력을 확실히 끌어올려 드립니다.
'''
    return content

def main():
    output_dir = "content/middle"

    created_files = []

    for i, dong in enumerate(GWANAK_DONGS):
        # 수학 파일 생성
        math_filename = f"gwanak-{dong['id']}-middle-math.md"
        math_filepath = os.path.join(output_dir, math_filename)
        math_content = create_math_content(dong, i)

        with open(math_filepath, 'w', encoding='utf-8') as f:
            f.write(math_content)
        created_files.append(math_filename)

        # 영어 파일 생성
        english_filename = f"gwanak-{dong['id']}-middle-english.md"
        english_filepath = os.path.join(output_dir, english_filename)
        english_content = create_english_content(dong, i)

        with open(english_filepath, 'w', encoding='utf-8') as f:
            f.write(english_content)
        created_files.append(english_filename)

    print(f"생성 완료: {len(created_files)}개 파일")
    for f in created_files:
        print(f"  - {f}")

if __name__ == "__main__":
    main()
