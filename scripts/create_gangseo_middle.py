#!/usr/bin/env python3
"""강서구 중등 수학/영어 과외 콘텐츠 생성 스크립트"""

import os

# 강서구 동별 정보
GANGSEO_DONGS = [
    {"id": "yeomchang", "name": "염창동", "schools": ["염경중", "염창중"]},
    {"id": "deungchon1", "name": "등촌1동", "schools": ["등촌중", "등명중", "등원중", "백석중"]},
    {"id": "deungchon2", "name": "등촌2동", "schools": ["등촌중", "등명중", "등원중", "백석중"]},
    {"id": "deungchon3", "name": "등촌3동", "schools": ["등촌중", "등명중", "등원중", "백석중"]},
    {"id": "hwagokbon", "name": "화곡본동", "schools": ["화곡중", "화원중"]},
    {"id": "hwagok1", "name": "화곡1동", "schools": ["화곡중", "화원중"]},
    {"id": "hwagok2", "name": "화곡2동", "schools": ["화곡중", "화원중"]},
    {"id": "hwagok3", "name": "화곡3동", "schools": ["화곡중", "화원중"]},
    {"id": "hwagok4", "name": "화곡4동", "schools": ["화곡중", "화원중"]},
    {"id": "hwagok5", "name": "화곡5동", "schools": ["화곡중", "화원중"]},
    {"id": "hwagok6", "name": "화곡6동", "schools": ["화곡중", "화원중"]},
    {"id": "hwagok7", "name": "화곡7동", "schools": ["화곡중", "화원중"]},
    {"id": "hwagok8", "name": "화곡8동", "schools": ["화곡중", "화원중"]},
    {"id": "ujangsan", "name": "우장산동", "schools": ["덕원중", "수명중"]},
    {"id": "balsan1", "name": "발산1동", "schools": ["덕원중", "수명중"]},
    {"id": "gonghang", "name": "공항동", "schools": ["공항중", "송정중", "마곡하늬중"]},
    {"id": "banghwa1", "name": "방화1동", "schools": ["방화중", "방원중", "삼정중"]},
    {"id": "banghwa2", "name": "방화2동", "schools": ["방화중", "방원중", "삼정중"]},
    {"id": "banghwa3", "name": "방화3동", "schools": ["방화중", "방원중", "삼정중"]},
    {"id": "gayang1", "name": "가양1동", "schools": ["마포중"]},
    {"id": "gayang2", "name": "가양2동", "schools": ["마포중"]},
    {"id": "gayang3", "name": "가양3동", "schools": ["마포중"]},
    {"id": "magok", "name": "마곡동", "schools": ["마곡중", "마곡하늬중"]},
]

# 이미지 풀 (중복 방지용)
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
    "photo-1518435579668-52e6c59a85",
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
    "photo-1507842217343-583bb7270b66",
    "photo-1497633762265-9d179a990aa6",
    "photo-1516979187457-637abb4f9353",
    "photo-1512820790803-83ca734da794",
    "photo-1550399105-c4db5fb85c18",
    "photo-1491841573634-28140fc7ced7",
    "photo-1473186578172-c141e6798cf4",
]

# 서두 변형 (수학)
MATH_INTROS = [
    "수학 성적이 오르락내리락 불안정한가요?",
    "중학교 수학, 어디서부터 잡아야 할지 모르겠나요?",
    "수학 개념은 아는 것 같은데 문제만 보면 막히나요?",
    "시험만 보면 실수가 나와서 속상하신가요?",
    "수학 때문에 학원을 여러 번 바꿔봤지만 효과가 없나요?",
    "아이가 수학을 싫어해서 걱정되시나요?",
    "중학교 올라오니 갑자기 수학이 어려워졌나요?",
    "선행은 했는데 정작 내신 성적이 안 나오나요?",
    "수학 공부 시간은 많은데 성적은 제자리인가요?",
    "서술형 문제에서 점수를 많이 잃고 있나요?",
    "수학 자신감이 점점 떨어지고 있나요?",
    "기초가 부족한 것 같아 걱정되시나요?",
    "문제 풀이 속도가 너무 느려서 시간이 부족한가요?",
    "개념은 외웠는데 응용이 안 되나요?",
    "수학 학원 숙제만 하다가 지쳐가나요?",
    "중2 수학부터 갑자기 어려워졌나요?",
    "함수가 나오면서 수학이 싫어졌나요?",
    "내신 수학 90점의 벽을 못 넘고 있나요?",
    "수학 때문에 전체 등급이 떨어지고 있나요?",
    "혼자 공부하려니 어디서부터 시작해야 할지 모르겠나요?",
    "수학 과외를 해도 성적이 그대로인가요?",
    "학원에서는 이해가 됐는데 집에 오면 까먹나요?",
    "수학 문제집만 쌓여가고 실력은 제자리인가요?",
]

# 서두 변형 (영어)
ENGLISH_INTROS = [
    "영어 성적이 좀처럼 오르지 않나요?",
    "영어 단어는 외우는데 독해가 안 되나요?",
    "문법은 아는 것 같은데 문제를 풀면 틀리나요?",
    "영어 시험만 보면 시간이 부족한가요?",
    "리스닝은 되는데 독해에서 점수를 잃나요?",
    "영어 학원을 다녀도 성적 변화가 없나요?",
    "중학교 영어가 갑자기 어려워졌나요?",
    "영어 내신 90점의 벽을 넘지 못하고 있나요?",
    "영어 서술형에서 감점이 많이 되나요?",
    "영어 공부 방법을 모르겠다고 하나요?",
    "단어 암기가 너무 힘들어하나요?",
    "영어 지문이 길어지니 읽기 싫어하나요?",
    "문법 개념이 헷갈려서 실수가 많나요?",
    "영어 자신감이 점점 없어지고 있나요?",
    "중2 영어부터 성적이 떨어지기 시작했나요?",
    "영어 공부 시간은 많은데 성적은 안 오르나요?",
    "학원 진도는 나가는데 실력이 안 느나요?",
    "영어 때문에 전체 내신이 떨어지고 있나요?",
    "영어 독해 지문을 읽어도 무슨 말인지 모르겠나요?",
    "문법책은 여러 권 풀었는데 실전에서 안 되나요?",
    "영어 듣기는 잘하는데 필기 시험이 약하나요?",
    "영어 어휘력이 부족해서 독해가 안 되나요?",
    "영어 에세이 쓰는 게 너무 어렵나요?",
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
            school_features.append(f"{school}은 기본 개념을 충실히 묻는 편입니다. 교과서 예제와 익힘책 문제를 꼼꼼히 풀어두면 좋은 점수를 받을 수 있습니다. 서술형에서는 풀이 과정을 논리적으로 쓰는 연습이 필요합니다.")
        else:
            school_features.append(f"{school}은 응용 문제 비중이 높습니다. 개념을 정확히 이해하고 다양한 유형의 문제를 풀어본 학생이 유리합니다. 시간 관리 연습도 필수입니다.")

    school_feature_text = "\n\n".join(school_features)

    content = f'''---
title: "강서구 {dong_name} 중등 수학과외 | {school_list} 내신 완벽 대비"
date: 2025-01-29
categories:
  - 중등교육
regions:
  - 서울
cities:
  - 강서구
description: "강서구 {dong_name} 중학생 수학과외 전문. {school_list} 내신 맞춤 관리. 개념부터 심화까지 체계적 1:1 지도."
tags:
  - {dong_name}
  - 강서구
  - 중등수학
  - 수학과외
  - 내신관리
{school_tags}
  - 수학개념
  - 수학심화
  - 강서양천교육지원청
featured_image: "https://images.unsplash.com/{image}?w=1200&h=630&fit=crop"

---
## 강서구 {dong_name} 중학생, {intro}

{dong_name}에서 중학생 자녀의 수학 성적 때문에 고민하시는 학부모님이 많습니다. 학원을 보내도, 문제집을 풀려도 성적이 오르지 않는 이유는 학생 개인의 취약점을 정확히 파악하지 못했기 때문입니다. 1:1 맞춤 과외로 정확한 진단부터 시작해야 합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
첫 수업에서 학생의 수학 실력을 꼼꼼히 진단합니다. 어떤 개념이 부족한지, 어떤 유형에서 실수가 나오는지 파악하고 맞춤 학습 계획을 세웁니다.
</div>

## 중학교 수학이 중요한 이유

중학교 수학은 고등학교 수학의 기초입니다. 중학교 때 개념에 구멍이 생기면 고등학교 가서 메우기 어렵습니다. 지금 제대로 잡아야 나중에 고생하지 않습니다.

중1의 정수와 유리수 연산, 중2의 연립방정식과 일차함수, 중3의 이차방정식과 이차함수는 모두 고등학교 수학의 필수 선행 개념입니다. 지금 완벽히 이해해두지 않으면 고등학교에서 큰 어려움을 겪게 됩니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
현재 학년의 개념을 완벽히 이해했는지 확인한 후 다음 단원으로 넘어갑니다. 진도보다 완성도를 중시합니다.
</div>

## {school_list} 수학 시험의 특징

{school_feature_text}

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{school_list} 기출문제를 분석하여 출제 경향을 파악합니다. 학교별 맞춤 대비로 내신 성적을 올립니다.
</div>

## 1:1 과외가 학원보다 효과적인 경우

학원은 정해진 커리큘럼대로 진도를 나갑니다. 학생이 이해하지 못해도 다음으로 넘어가는 경우가 많습니다. 1:1 과외는 학생의 이해도에 맞춰 수업 속도를 조절합니다.

특히 기초가 부족한 학생, 특정 단원에서 막히는 학생, 상위권으로 도약하고 싶은 학생에게 1:1 맞춤 지도가 효과적입니다. 모르는 것을 그냥 넘어가지 않습니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
매 수업 학생이 스스로 설명할 수 있는지 확인합니다. 설명할 수 있어야 진짜 아는 것입니다.
</div>

## 학년별 학습 전략

중1은 수학의 기초를 다지는 시기입니다. 정수와 유리수의 연산을 완벽히 익히고, 문자와 식의 표현에 익숙해져야 합니다. 일차방정식의 풀이 원리를 정확히 이해하는 것이 중요합니다.

중2는 수학의 핵심 시기입니다. 연립방정식과 일차함수는 고등학교 수학의 기초가 됩니다. 그래프를 해석하는 능력을 키우고, 함수 개념을 확실히 잡아야 합니다.

중3은 고등학교 준비 시기입니다. 이차방정식과 이차함수를 마스터해야 합니다. 피타고라스 정리를 활용한 문제를 많이 풀고, 내신 마무리와 고등 선행을 병행합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
학년별 핵심 단원을 체계적으로 정리합니다. 다음 학년으로 넘어가기 전 빈틈없이 점검합니다.
</div>

## 수업료 안내

중학생 수학과외 수업료는 다음과 같습니다.

**중1~2**는 주1회 기준 18만원에서 25만원, 주2회 기준 32만원에서 45만원 선입니다.

**중3**은 주1회 기준 20만원에서 28만원, 주2회 기준 36만원에서 50만원이 일반적입니다.

수업 횟수, 시간, 선생님 경력에 따라 달라질 수 있습니다. 정확한 수업료는 상담을 통해 안내드립니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
첫 상담에서 학생의 현재 실력과 목표를 파악하고, 적합한 수업 계획과 수업료를 안내드립니다.
</div>

{{{{< cta-dual type="final" >}}}}

## 자주 묻는 질문

**Q. 수학 기초가 많이 부족한데 따라갈 수 있을까요?**

기초가 부족한 학생일수록 1:1 과외가 효과적입니다. 어디서부터 막혔는지 정확히 진단하고, 그 부분부터 차근차근 다시 설명합니다. 학원에서는 불가능한 맞춤 지도가 가능합니다.

**Q. 내신 대비와 선행을 같이 할 수 있나요?**

가능합니다. 시험 기간에는 내신 대비에 집중하고, 시험이 끝나면 선행을 진행합니다. 학생의 상황에 맞게 유연하게 운영합니다.

**Q. 수업은 어디서 진행하나요?**

학생의 집으로 방문하거나, 스터디카페, 도서관 등 학생이 편한 장소에서 수업합니다. 온라인 수업도 가능합니다.

## 마무리

강서구 {dong_name}에서 중학생 수학과외를 찾고 계신다면, 지금 바로 상담받아보세요. {school_list} 내신에 맞춘 1:1 맞춤 수업으로 수학 실력을 확실히 올려드립니다.
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
            school_features.append(f"{school}은 교과서 본문 내용을 충실히 출제합니다. 본문 암기와 문법 정리가 잘 되어 있으면 좋은 점수를 받을 수 있습니다. 서술형에서는 문장 구조를 정확히 쓰는 연습이 필요합니다.")
        else:
            school_features.append(f"{school}은 독해 지문의 난이도가 높은 편입니다. 교과서 외 지문도 출제되므로 다양한 글을 읽어보는 연습이 필요합니다. 어휘력 확장도 중요합니다.")

    school_feature_text = "\n\n".join(school_features)

    content = f'''---
title: "강서구 {dong_name} 중등 영어과외 | {school_list} 내신 완벽 대비"
date: 2025-01-29
categories:
  - 중등교육
regions:
  - 서울
cities:
  - 강서구
description: "강서구 {dong_name} 중학생 영어과외 전문. {school_list} 내신 맞춤 관리. 문법·독해·어휘 체계적 1:1 지도."
tags:
  - {dong_name}
  - 강서구
  - 중등영어
  - 영어과외
  - 내신관리
{school_tags}
  - 영어문법
  - 영어독해
  - 강서양천교육지원청
featured_image: "https://images.unsplash.com/{image}?w=1200&h=630&fit=crop"

---
## 강서구 {dong_name} 중학생, {intro}

{dong_name}에서 중학생 자녀의 영어 성적 때문에 고민하시는 학부모님이 많습니다. 단어도 외우고 문법책도 풀었는데 성적이 안 오르는 이유는 학생 개인의 약점을 정확히 파악하지 못했기 때문입니다. 1:1 맞춤 과외로 정확한 진단부터 시작해야 합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
첫 수업에서 학생의 영어 실력을 영역별로 진단합니다. 문법, 독해, 어휘 중 어디가 약한지 파악하고 맞춤 학습 계획을 세웁니다.
</div>

## 중학교 영어가 중요한 이유

중학교 영어는 고등학교 영어의 기초입니다. 중학교 때 문법 개념이 흔들리면 고등학교 독해가 어려워집니다. 지금 제대로 잡아야 나중에 고생하지 않습니다.

중1의 기초 문법, 중2의 준동사와 관계대명사, 중3의 복합 문장 구조는 모두 고등학교 영어의 필수 선행 개념입니다. 지금 완벽히 이해해두지 않으면 수능 영어에서 큰 어려움을 겪게 됩니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
문법 개념을 단순 암기가 아닌 원리 이해로 접근합니다. 왜 그런 문법 규칙이 있는지 설명하면 오래 기억됩니다.
</div>

## {school_list} 영어 시험의 특징

{school_feature_text}

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{school_list} 기출문제를 분석하여 출제 경향을 파악합니다. 학교별 맞춤 대비로 내신 성적을 올립니다.
</div>

## 1:1 과외가 학원보다 효과적인 경우

학원은 정해진 커리큘럼대로 진도를 나갑니다. 학생이 이해하지 못해도 다음으로 넘어가는 경우가 많습니다. 1:1 과외는 학생의 이해도에 맞춰 수업 속도를 조절합니다.

특히 문법이 약한 학생, 독해가 안 되는 학생, 상위권으로 도약하고 싶은 학생에게 1:1 맞춤 지도가 효과적입니다. 모르는 것을 그냥 넘어가지 않습니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
매 수업 학생이 배운 문법을 직접 활용해 문장을 만들어보게 합니다. 직접 써봐야 진짜 아는 것입니다.
</div>

## 학년별 학습 전략

중1은 영어의 기초를 다지는 시기입니다. 기본 문법 개념을 정확히 이해하고, 기초 어휘를 탄탄히 쌓아야 합니다. 짧은 문장 독해부터 시작해 점점 긴 문장으로 확장합니다.

중2는 영어의 핵심 시기입니다. to부정사, 동명사, 분사 등 준동사 개념이 등장합니다. 관계대명사도 배우게 됩니다. 이 개념들이 고등학교 독해의 기초가 됩니다.

중3은 고등학교 준비 시기입니다. 복합 문장 구조를 이해하고, 긴 지문 독해 연습을 해야 합니다. 내신 마무리와 고등 선행을 병행합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
학년별 핵심 문법을 체계적으로 정리합니다. 다음 학년으로 넘어가기 전 빈틈없이 점검합니다.
</div>

## 수업료 안내

중학생 영어과외 수업료는 다음과 같습니다.

**중1~2**는 주1회 기준 17만원에서 24만원, 주2회 기준 30만원에서 42만원 선입니다.

**중3**은 주1회 기준 19만원에서 26만원, 주2회 기준 34만원에서 48만원이 일반적입니다.

수업 횟수, 시간, 선생님 경력에 따라 달라질 수 있습니다. 정확한 수업료는 상담을 통해 안내드립니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
첫 상담에서 학생의 현재 실력과 목표를 파악하고, 적합한 수업 계획과 수업료를 안내드립니다.
</div>

{{{{< cta-dual type="final" >}}}}

## 자주 묻는 질문

**Q. 영어 기초가 많이 부족한데 따라갈 수 있을까요?**

기초가 부족한 학생일수록 1:1 과외가 효과적입니다. 어디서부터 막혔는지 정확히 진단하고, 그 부분부터 차근차근 다시 설명합니다. 학원에서는 불가능한 맞춤 지도가 가능합니다.

**Q. 내신 대비와 선행을 같이 할 수 있나요?**

가능합니다. 시험 기간에는 내신 대비에 집중하고, 시험이 끝나면 선행을 진행합니다. 학생의 상황에 맞게 유연하게 운영합니다.

**Q. 수업은 어디서 진행하나요?**

학생의 집으로 방문하거나, 스터디카페, 도서관 등 학생이 편한 장소에서 수업합니다. 온라인 수업도 가능합니다.

## 마무리

강서구 {dong_name}에서 중학생 영어과외를 찾고 계신다면, 지금 바로 상담받아보세요. {school_list} 내신에 맞춘 1:1 맞춤 수업으로 영어 실력을 확실히 올려드립니다.
'''
    return content

def main():
    output_dir = "content/middle"

    created_files = []

    for i, dong in enumerate(GANGSEO_DONGS):
        # 수학 파일 생성
        math_filename = f"gangseo-{dong['id']}-middle-math.md"
        math_filepath = os.path.join(output_dir, math_filename)
        math_content = create_math_content(dong, i)

        with open(math_filepath, 'w', encoding='utf-8') as f:
            f.write(math_content)
        created_files.append(math_filename)

        # 영어 파일 생성
        english_filename = f"gangseo-{dong['id']}-middle-english.md"
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
