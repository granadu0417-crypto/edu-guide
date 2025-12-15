#!/usr/bin/env python3
"""
서울 법정동 콘텐츠 생성 스크립트
기존 행정동 콘텐츠에 법정동 콘텐츠 추가
"""

import os
import random
from datetime import datetime

# 서울 구별 법정동 데이터 (행정동과 중복되지 않는 것만)
SEOUL_DISTRICTS = {
    "gangnam": {
        "name_ko": "강남구",
        "legal_dongs": ["대치동", "도곡동", "개포동", "일원동", "수서동", "세곡동", "자곡동", "율현동", "삼성동", "청담동", "압구정동", "신사동", "논현동", "역삼동"]
    },
    "gangdong": {
        "name_ko": "강동구",
        "legal_dongs": ["강일동", "상일동", "명일동", "고덕동", "암사동", "천호동", "성내동", "길동", "둔촌동"]
    },
    "gangbuk": {
        "name_ko": "강북구",
        "legal_dongs": ["미아동", "번동", "수유동", "우이동", "삼양동", "송중동", "송천동", "삼각산동"]
    },
    "gangseo": {
        "name_ko": "강서구",
        "legal_dongs": ["가양동", "등촌동", "화곡동", "발산동", "내발산동", "외발산동", "공항동", "방화동"]
    },
    "gwanak": {
        "name_ko": "관악구",
        "legal_dongs": ["봉천동", "신림동", "남현동"]
    },
    "gwangjin": {
        "name_ko": "광진구",
        "legal_dongs": ["중곡동", "능동", "구의동", "광장동", "자양동", "화양동", "군자동"]
    },
    "guro": {
        "name_ko": "구로구",
        "legal_dongs": ["신도림동", "구로동", "가리봉동", "고척동", "개봉동", "오류동", "궁동", "온수동", "천왕동", "항동"]
    },
    "geumcheon": {
        "name_ko": "금천구",
        "legal_dongs": ["가산동", "독산동", "시흥동"]
    },
    "nowon": {
        "name_ko": "노원구",
        "legal_dongs": ["월계동", "공릉동", "하계동", "중계동", "상계동"]
    },
    "dobong": {
        "name_ko": "도봉구",
        "legal_dongs": ["쌍문동", "방학동", "창동", "도봉동"]
    },
    "dongdaemun": {
        "name_ko": "동대문구",
        "legal_dongs": ["신설동", "용두동", "제기동", "전농동", "답십리동", "장안동", "청량리동", "회기동", "휘경동", "이문동"]
    },
    "dongjak": {
        "name_ko": "동작구",
        "legal_dongs": ["노량진동", "상도동", "흑석동", "동작동", "사당동", "대방동", "신대방동"]
    },
    "mapo": {
        "name_ko": "마포구",
        "legal_dongs": ["공덕동", "아현동", "도화동", "용강동", "대흥동", "염리동", "신수동", "서강동", "서교동", "합정동", "망원동", "연남동", "성산동", "상암동"]
    },
    "seodaemun": {
        "name_ko": "서대문구",
        "legal_dongs": ["충정로", "합동", "미근동", "냉천동", "천연동", "옥천동", "영천동", "현저동", "북아현동", "홍제동", "대현동", "대신동", "신촌동", "봉원동", "창천동", "연희동", "홍은동", "북가좌동", "남가좌동"]
    },
    "seocho": {
        "name_ko": "서초구",
        "legal_dongs": ["방배동", "양재동", "우면동", "원지동", "잠원동", "반포동", "서초동", "내곡동", "염곡동", "신원동"]
    },
    "seongdong": {
        "name_ko": "성동구",
        "legal_dongs": ["상왕십리동", "하왕십리동", "홍익동", "도선동", "마장동", "사근동", "행당동", "응봉동", "금호동", "옥수동", "성수동", "송정동"]
    },
    "seongbuk": {
        "name_ko": "성북구",
        "legal_dongs": ["성북동", "돈암동", "동소문동", "삼선동", "동선동", "안암동", "보문동", "정릉동", "길음동", "종암동", "하월곡동", "상월곡동", "장위동", "석관동"]
    },
    "songpa": {
        "name_ko": "송파구",
        "legal_dongs": ["잠실동", "신천동", "풍납동", "거여동", "마천동", "방이동", "오금동", "가락동", "문정동", "장지동", "석촌동", "삼전동", "송파동"]
    },
    "yangcheon": {
        "name_ko": "양천구",
        "legal_dongs": ["목동", "신월동", "신정동"]
    },
    "yeongdeungpo": {
        "name_ko": "영등포구",
        "legal_dongs": ["영등포동", "여의도동", "당산동", "신길동", "대림동", "도림동", "문래동", "양평동"]
    },
    "yongsan": {
        "name_ko": "용산구",
        "legal_dongs": ["후암동", "용산동", "남영동", "청파동", "원효로", "효창동", "용문동", "한강로", "이촌동", "이태원동", "한남동", "서빙고동", "보광동"]
    },
    "eunpyeong": {
        "name_ko": "은평구",
        "legal_dongs": ["녹번동", "불광동", "갈현동", "구산동", "대조동", "응암동", "역촌동", "신사동", "증산동", "수색동", "진관동"]
    },
    "jongno": {
        "name_ko": "종로구",
        "legal_dongs": ["청운동", "신교동", "궁정동", "효자동", "창성동", "통의동", "적선동", "통인동", "누상동", "누하동", "옥인동", "체부동", "필운동", "내자동", "사직동", "도렴동", "당주동", "내수동", "세종로", "신문로", "청진동", "서린동", "수송동", "중학동", "종로", "공평동", "관훈동", "견지동", "와룡동", "권농동", "운니동", "익선동", "경운동", "관철동", "인사동", "낙원동", "봉익동", "돈의동", "묘동", "장사동", "삼일대로", "훈정동", "숭인동", "창신동", "원남동", "연건동", "충신동", "동숭동", "혜화동", "명륜동", "이화동"]
    },
    "jung": {
        "name_ko": "중구",
        "legal_dongs": ["무교동", "다동", "태평로", "을지로", "남대문로", "북창동", "삼각동", "수하동", "장교동", "수표동", "소공동", "회현동", "명동", "충무로", "을지로동", "신당동", "황학동", "중림동", "약수동", "청구동", "흥인동", "광희동", "장충동", "필동", "예관동", "묵정동", "동화동"]
    },
    "jungnang": {
        "name_ko": "중랑구",
        "legal_dongs": ["면목동", "상봉동", "중화동", "묵동", "망우동", "신내동"]
    }
}

# 표현 풀
TITLE_SUFFIXES = [
    "내신·수능 완벽 대비",
    "1:1 맞춤 수업",
    "개념부터 실전까지",
    "체계적 학습 관리",
    "실력 향상 보장",
    "기초부터 심화까지",
    "학교별 내신 특화",
    "맞춤형 커리큘럼",
    "전문 과외 수업",
    "성적 향상 솔루션",
    "개인 맞춤 지도",
    "효과적인 학습법",
    "목표 달성 수업",
    "수준별 맞춤 과외",
    "꼼꼼한 1:1 수업"
]

INTROS = [
    "{district} {dong} 학생 여러분, {subject} 성적 때문에 스트레스받고 계신가요? 중학교 때는 잘했는데 고등학교에 와서 갑자기 어려워졌다는 말, 정말 많이 듣습니다.",
    "{district} {dong}에서 {subject} 때문에 고민이시라면 잘 찾아오셨습니다. 혼자 공부하면 어디가 문제인지 모를 수 있습니다.",
    "{subject} 성적이 오르지 않아 고민이신 {district} {dong} 학생 여러분, 공부 방법을 바꿔볼 때입니다.",
    "{district} {dong} 고등학생 여러분, {subject}은 포기 과목이 아닙니다. 제대로 된 방법으로 공부하면 반드시 성적이 오릅니다.",
    "{district} {dong}에서 {subject} 과외를 찾고 계신가요? 학원에서 따라가기 힘들다면 1:1 과외가 답입니다.",
    "{subject} 점수가 안 오르는 {district} {dong} 학생들, 지금 시작해도 늦지 않았습니다.",
    "{district} {dong} 학부모님, 아이의 {subject} 실력이 걱정되시죠? 전문 과외로 확실하게 잡아드립니다.",
    "{subject}은 계단식 과목입니다. {district} {dong} 학생 여러분, 기초부터 탄탄히 쌓아가세요.",
    "{district} {dong}에서 {subject} 전문 과외를 찾으신다면 주목하세요.",
    "고등학교 {subject}, 어디서부터 잡아야 할지 모르겠다면 {district} {dong}에서 시작하세요.",
    "{district} {dong} 학생들의 {subject} 고민, 이해합니다. 함께라면 달라질 수 있습니다.",
    "{subject}만 잘해도 대학이 달라집니다. {district} {dong} 고등학생 여러분, 지금 시작하세요.",
    "{district} {dong}에서 {subject} 과외 알아보시나요? 학생의 수준에 맞춘 1:1 수업을 제공합니다.",
    "내신과 수능을 동시에 준비해야 하는 {district} {dong} 학생들, {subject}은 전략적으로 공부해야 합니다.",
    "{district} {dong} 고등학생 {subject} 성적 향상, 체계적인 과외로 가능합니다."
]

IVORY_BOXES = [
    "개념 설명 후 바로 문제 풀이로 연결합니다. 이해했는지 즉시 확인하고 넘어갑니다.",
    "학생이 이해했는지 직접 설명해보게 합니다. 설명할 수 있어야 진짜 아는 겁니다.",
    "학생의 컨디션도 체크합니다. 공부만 잘한다고 되는 게 아닙니다.",
    "시험 후에는 함께 오답을 분석합니다. 왜 틀렸는지 파악하고 다음에 같은 실수를 안 하도록 합니다.",
    "매 수업 시작 전 지난 내용을 복습합니다. 까먹기 전에 다시 한번 확인합니다.",
    "숙제는 적정량만 내드립니다. 무리하지 않으면서도 실력이 오르도록 합니다.",
    "학부모님께 주기적으로 학습 상황을 보고드립니다. 함께 아이를 케어합니다.",
    "오답 노트를 함께 만들어갑니다. 틀린 문제는 반드시 다시 풀어봅니다.",
    "모르는 건 바로 질문하게 합니다. 질문을 두려워하지 않도록 분위기를 만들어줍니다.",
    "첫 수업에서 학생의 현재 실력을 정확하게 진단합니다.",
    "수업 중에 집중력이 떨어지면 잠시 쉬어갑니다.",
    "학생의 학교 진도에 맞춰 수업합니다. 시험 범위에 맞게 집중적으로 대비합니다.",
    "단순 암기가 아닌 이해 중심으로 가르칩니다. 원리를 알면 응용이 됩니다.",
    "매 수업마다 작은 목표를 세우고 달성합니다. 성취감이 공부의 동력입니다.",
    "어려운 개념은 쉬운 예시로 설명합니다. 눈높이에 맞춘 설명이 이해를 돕습니다."
]

ENDINGS = [
    "{district} {dong} 고등 {subject}, 오늘 상담받고, 내일부터 달라지세요.",
    "지금이 바로 시작할 때입니다. {district} {dong}에서 {subject} 실력 향상을 시작하세요.",
    "{subject}은 시작이 반입니다. {district} {dong} 학생 여러분, 지금 바로 시작하세요.",
    "더 늦기 전에 시작하세요. {district} {dong}에서 {subject} 잘하는 학생, 여러분도 될 수 있습니다.",
    "고등학교 {subject}, 혼자 고민하지 마세요. {district} {dong}에서 함께하면 달라집니다.",
    "{district} {dong} 학생 여러분의 {subject} 성적 향상을 응원합니다.",
    "{subject} 때문에 대학 못 가면 너무 억울합니다. {district} {dong}에서 지금 시작하세요.",
    "포기하기엔 아직 이릅니다. {district} {dong} 고등학생 {subject}, 함께 해결합시다.",
    "{district} {dong}에서 {subject} 성적을 올리고 싶다면, 지금 연락주세요.",
    "목표 대학을 향해, {district} {dong}에서 {subject} 실력을 키워가세요."
]

IMAGES = [
    "photo-1523240795612-9a054b0db644",
    "photo-1522202176988-66273c2fd55f",
    "photo-1503676260728-1c00da094a0b",
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
    "photo-1516321497487-e288fb19713f",
    "photo-1501504905252-473c47e087f8",
    "photo-1509869175650-a1d97972541a",
    "photo-1457369804613-52c61a468e7d",
    "photo-1456513080510-7bf3a84b82f8",
    "photo-1546410531-bb4caa6b424d",
    "photo-1553877522-43269d4ea984",
    "photo-1515378791036-0648a3ef77b2",
    "photo-1519389950473-47ba0277781c",
    "photo-1488190211105-8b0e65b80b4e",
    "photo-1434030216411-0b793f4b4173",
    "photo-1455390582262-044cdead277a",
    "photo-1471107340929-a87cd0f5b5f3",
    "photo-1415369629372-26f2fe60c467",
    "photo-1447069387593-a5de0862481e",
    "photo-1476234251651-f353703a034d",
    "photo-1521587760476-6c12a4b040da"
]

def get_subject_info(subject_type):
    if subject_type == "math":
        return {"ko": "수학", "title_ko": "수학과외", "tag": "수학과외"}
    else:
        return {"ko": "영어", "title_ko": "영어과외", "tag": "영어과외"}

def get_level_info(level):
    if level == "middle":
        return {
            "ko": "중등",
            "title_ko": "중등",
            "category": "중등교육",
            "cost": "**중학생** 기준으로 주1회 22만원 - 32만원, 주2회 29만원 - 47만원 선입니다."
        }
    else:
        return {
            "ko": "고등",
            "title_ko": "고등",
            "category": "고등교육",
            "cost": "**고등학생** 기준으로 주1회 25만원 - 36만원, 주2회 33만원 - 53만원 선입니다."
        }

def generate_content(district_name, dong, level, subject, index):
    level_info = get_level_info(level)
    subject_info = get_subject_info(subject)

    title_suffix = TITLE_SUFFIXES[index % len(TITLE_SUFFIXES)]
    intro = INTROS[index % len(INTROS)]
    boxes = random.sample(IVORY_BOXES, 7)
    ending = ENDINGS[index % len(ENDINGS)]
    image = IMAGES[index % len(IMAGES)]

    title = f"서울 {district_name} {dong} {level_info['title_ko']} {subject_info['title_ko']} | {title_suffix}"

    content = f'''---
title: "{title}"
date: {datetime.now().strftime("%Y-%m-%d")}
categories:
- {level_info["category"]}
- {subject_info["ko"]}
tags:
- 서울
- {district_name}
- {dong}
- {level_info["ko"]}{subject_info["tag"]}
- {subject_info["tag"]}
- 내신대비
- 수능대비
description: "서울 {district_name} {dong} 지역 {level_info['ko']} {subject_info['ko']} 과외 전문. 학생 맞춤 1:1 수업으로 내신과 수능을 동시에 준비합니다."
featured_image: "https://images.unsplash.com/{image}?w=1200&h=630&fit=crop"
---

{intro.format(district=district_name, dong=dong, subject=subject_info["ko"])}

{subject_info["ko"]}은 계단식 과목입니다. 앞 단계를 완벽히 이해해야 다음 단계로 넘어갈 수 있습니다. 기초에 빈틈이 있으면 점점 더 힘들어집니다.

혼자 공부하면 어디가 문제인지 모를 수 있습니다. 전문가의 도움을 받으면 효율적으로 문제를 해결할 수 있습니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[0]}
</div>

## 1:1 과외가 효과적인 이유

1:1 과외의 가장 큰 장점은 맞춤 수업입니다. 학생의 수준에 맞춰 진도를 조절합니다. 이해가 안 되면 더 설명하고, 이해했으면 다음으로 넘어갑니다.

질문을 바로 할 수 있습니다. 모르는 게 생기면 그 자리에서 해결합니다. 학원에서는 질문하기가 어렵습니다.

학생의 약점을 정확히 파악할 수 있습니다. 어떤 유형에서 자주 틀리는지, 어떤 개념이 부족한지 선생님이 알고 있습니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[1]}
</div>

## 효과적인 학습 방법

{subject_info["ko"]} 공부의 핵심은 개념 이해입니다. 공식만 외워서는 응용 문제를 풀 수 없습니다. 왜 그런 공식이 나오는지 알아야 합니다.

문제 풀이는 양보다 질입니다. 많이 푸는 것보다 제대로 푸는 게 중요합니다.

오답 정리는 필수입니다. 틀린 문제는 반드시 다시 풀어봐야 합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[2]}
</div>

## 학년별 학습 전략

학년별로 전략이 다릅니다. {level_info["ko"]}1학년은 기초를 다지는 시기입니다. 이전 학년 내용에 빈틈이 있다면 먼저 메워야 합니다.

{level_info["ko"]}2학년은 심화 학습을 시작합니다. 핵심 개념들을 충실히 학습하세요.

{level_info["ko"]}3학년은 정리와 실전 연습의 시기입니다. 기출문제를 많이 풀어보세요.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[3]}
</div>

## 자주 하는 실수

학생들이 자주 하는 실수를 알려드립니다. 가장 흔한 건 계산 실수입니다. 급하게 풀다 보면 부호를 틀리거나 숫자를 잘못 쓰는 경우가 많습니다.

개념을 대충 알고 넘어가는 것도 문제입니다. 이해한 것 같아도 막상 문제에 적용하면 막힙니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[4]}
</div>

## 시험 대비 전략

시험 2주 전부터 본격적으로 준비하세요. 교과서와 수업 노트를 다시 읽고, 핵심 개념을 정리하세요.

기출문제를 풀어보세요. 학교 시험은 출제 경향이 있습니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[5]}
</div>

## 수업료 안내

서울 {district_name} {dong} 지역 {level_info['ko']} {subject_info['ko']} 과외 수업료입니다.

{level_info["cost"]}

정확한 비용은 학생의 현재 수준과 목표에 따라 달라질 수 있습니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[6]}
</div>

{{{{< cta-dual type="final" >}}}}

## 자주 묻는 질문

**Q. 주 몇 회 수업이 좋나요?**

학생 상황에 따라 다릅니다. 기초가 부족하면 주 2-3회, 유지 목적이면 주 1회가 적당합니다.

**Q. 내신과 수능 중 뭘 먼저 해야 하나요?**

학년에 따라 다릅니다. {level_info["ko"]}1-2는 내신 중심으로, {level_info["ko"]}3은 수능 비중을 높여갑니다.

**Q. {subject_info["ko"]}은 언제부터 준비해야 하나요?**

빠를수록 좋습니다. 기초가 부족하다면 지금 바로 시작하세요.

## 마무리

{ending.format(district=district_name, dong=dong, subject=subject_info["ko"])}
'''
    return content

def main():
    base_path = "/home/user/edu-guide/content/seoul"
    total_files = 0
    index = 0

    for district_key, district_data in SEOUL_DISTRICTS.items():
        district_name = district_data["name_ko"]
        district_path = os.path.join(base_path, district_key)

        for dong in district_data["legal_dongs"]:
            # 동 폴더 생성
            dong_folder = dong.replace(" ", "-")
            dong_path = os.path.join(district_path, dong_folder)
            os.makedirs(dong_path, exist_ok=True)

            # _index.md 생성
            index_content = f'''---
title: "서울 {district_name} {dong}"
---
'''
            with open(os.path.join(dong_path, "_index.md"), "w", encoding="utf-8") as f:
                f.write(index_content)

            # 4개 파일 생성
            for level in ["middle", "high"]:
                for subject in ["math", "english"]:
                    filename = f"{level}-{subject}.md"
                    filepath = os.path.join(dong_path, filename)

                    content = generate_content(district_name, dong, level, subject, index)

                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(content)

                    total_files += 1
                    index += 1

            print(f"생성 완료: 서울 {district_name} {dong} (4개 파일)")

    print(f"\n총 {total_files}개 파일 생성 완료")

if __name__ == "__main__":
    main()
