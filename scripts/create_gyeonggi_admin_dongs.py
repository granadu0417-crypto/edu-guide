#!/usr/bin/env python3
"""
경기도 행정동 콘텐츠 생성 스크립트
기존 법정동에 행정동(숫자 붙은 동) 추가
"""

import os
import random
from datetime import datetime

# 경기도 주요 지역 행정동 데이터 (법정동에서 분리된 행정동만)
GYEONGGI_ADMIN_DONGS = {
    "bundang": {
        "name_ko": "분당구",
        "city_ko": "성남시",
        "admin_dongs": ["서현1동", "서현2동", "수내1동", "수내2동", "수내3동", "정자1동", "정자2동", "정자3동",
                       "야탑1동", "야탑2동", "야탑3동", "이매1동", "이매2동", "분당동", "구미1동", "금곡동",
                       "판교동", "운중동", "삼평동", "백현동"]
    },
    "ilsan": {
        "name_ko": "일산",
        "city_ko": "고양시",
        "admin_dongs": ["주엽1동", "주엽2동", "대화동", "장항1동", "장항2동", "백석1동", "백석2동",
                       "마두1동", "마두2동", "정발산동", "풍산동", "일산1동", "일산2동", "일산3동",
                       "탄현동", "식사동", "중산동", "산황동"]
    },
    "suwon": {
        "name_ko": "수원시",
        "city_ko": "수원시",
        "admin_dongs": ["영통1동", "영통2동", "영통3동", "매탄1동", "매탄2동", "매탄3동", "매탄4동",
                       "원천동", "광교1동", "광교2동", "권선1동", "권선2동", "세류1동", "세류2동", "세류3동",
                       "팔달문동", "행궁동", "매산동", "고등동", "화서1동", "화서2동", "인계동", "율전동"]
    },
    "yongin": {
        "name_ko": "용인시",
        "city_ko": "용인시",
        "admin_dongs": ["수지1동", "수지2동", "죽전1동", "죽전2동", "동천동", "풍덕천1동", "풍덕천2동",
                       "상현1동", "상현2동", "성복동", "신봉동", "기흥동", "구갈동", "상갈동", "보라동",
                       "영덕동", "신갈동", "동백1동", "동백2동", "동백3동"]
    },
    "anyang": {
        "name_ko": "안양시",
        "city_ko": "안양시",
        "admin_dongs": ["비산1동", "비산2동", "비산3동", "관양1동", "관양2동", "부림동", "달안동",
                       "평촌동", "귀인동", "평안동", "부흥동", "범계동", "호계1동", "호계2동", "호계3동"]
    },
    "pyeongchon": {
        "name_ko": "평촌",
        "city_ko": "안양시",
        "admin_dongs": ["평촌동", "귀인동", "평안동", "부흥동", "범계동", "호계1동", "호계2동", "호계3동",
                       "관양1동", "관양2동", "달안동", "비산1동", "비산2동"]
    },
    "bucheon": {
        "name_ko": "부천시",
        "city_ko": "부천시",
        "admin_dongs": ["원미1동", "원미2동", "소사본동", "소사본1동", "소사본2동", "심곡1동", "심곡2동", "심곡3동", "심곡본동",
                       "역곡1동", "역곡2동", "역곡3동", "중동", "상동", "상1동", "상2동", "상3동",
                       "송내1동", "송내2동", "오정동", "약대동", "고강본동", "신흥동", "도당동"]
    },
    "goyang": {
        "name_ko": "고양시",
        "city_ko": "고양시",
        "admin_dongs": ["화정1동", "화정2동", "행신1동", "행신2동", "행신3동", "흥도동", "능곡동",
                       "대덕동", "화전동", "행주동", "신원동", "원당동", "성사1동", "성사2동"]
    },
    "namyangju": {
        "name_ko": "남양주시",
        "city_ko": "남양주시",
        "admin_dongs": ["호평동", "평내동", "금곡동", "다산1동", "다산2동", "별내동", "퇴계원읍",
                       "와부읍", "진접읍", "오남읍", "진건읍", "화도읍"]
    },
    "uijeongbu": {
        "name_ko": "의정부시",
        "city_ko": "의정부시",
        "admin_dongs": ["의정부1동", "의정부2동", "의정부3동", "호원1동", "호원2동", "장암동",
                       "신곡1동", "신곡2동", "송산1동", "송산2동", "자금동", "가능1동", "가능2동", "가능3동",
                       "녹양동", "흥선동"]
    },
    "hwaseong": {
        "name_ko": "화성시",
        "city_ko": "화성시",
        "admin_dongs": ["동탄1동", "동탄2동", "동탄3동", "동탄4동", "동탄5동", "동탄6동", "동탄7동", "동탄8동",
                       "병점1동", "병점2동", "진안동", "기배동", "반월동", "능동", "화산동"]
    },
    "siheung": {
        "name_ko": "시흥시",
        "city_ko": "시흥시",
        "admin_dongs": ["대야동", "신천동", "은행동", "매화동", "목감동", "정왕1동", "정왕2동", "정왕3동", "정왕4동",
                       "거모동", "신현동", "능곡동", "과림동", "연성동", "장곡동", "배곧1동", "배곧2동"]
    },
    "gimpo": {
        "name_ko": "김포시",
        "city_ko": "김포시",
        "admin_dongs": ["장기동", "마산동", "걸포동", "북변동", "풍무동", "사우동", "운양동", "구래동",
                       "장기본동", "고촌읍", "통진읍", "양촌읍", "대곶면", "월곶면", "하성면"]
    },
    "hanam": {
        "name_ko": "하남시",
        "city_ko": "하남시",
        "admin_dongs": ["천현동", "신장1동", "신장2동", "덕풍1동", "덕풍2동", "덕풍3동", "풍산동", "위례동",
                       "미사1동", "미사2동", "감일동", "춘궁동", "초이동"]
    },
    "gwangmyeong": {
        "name_ko": "광명시",
        "city_ko": "광명시",
        "admin_dongs": ["광명1동", "광명2동", "광명3동", "광명4동", "광명5동", "광명6동", "광명7동",
                       "철산1동", "철산2동", "철산3동", "철산4동", "하안1동", "하안2동", "하안3동", "하안4동",
                       "소하1동", "소하2동"]
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
    "{city} {dong} 학생 여러분, {subject} 성적 때문에 고민이신가요? 혼자 공부하면 어디가 문제인지 파악하기 어렵습니다.",
    "{city} {dong}에서 {subject} 과외를 찾고 계신가요? 학원에서 따라가기 힘들다면 1:1 과외가 답입니다.",
    "{subject} 성적이 오르지 않아 고민이신 {city} {dong} 학생 여러분, 공부 방법을 바꿔볼 때입니다.",
    "{city} {dong} 고등학생 여러분, {subject}은 포기 과목이 아닙니다. 제대로 된 방법으로 공부하면 성적이 오릅니다.",
    "{subject} 점수가 안 오르는 {city} {dong} 학생들, 지금 시작해도 늦지 않았습니다.",
    "{city} {dong} 학부모님, 아이의 {subject} 실력이 걱정되시죠? 전문 과외로 확실하게 잡아드립니다.",
    "{subject}은 계단식 과목입니다. {city} {dong} 학생 여러분, 기초부터 탄탄히 쌓아가세요.",
    "{city} {dong}에서 {subject} 전문 과외를 찾으신다면 주목하세요.",
    "고등학교 {subject}, 어디서부터 잡아야 할지 모르겠다면 {city} {dong}에서 시작하세요.",
    "{city} {dong} 학생들의 {subject} 고민, 이해합니다. 함께라면 달라질 수 있습니다.",
    "{subject}만 잘해도 대학이 달라집니다. {city} {dong} 고등학생 여러분, 지금 시작하세요.",
    "{city} {dong}에서 {subject} 과외 알아보시나요? 학생의 수준에 맞춘 1:1 수업을 제공합니다.",
    "내신과 수능을 동시에 준비해야 하는 {city} {dong} 학생들, {subject}은 전략적으로 공부해야 합니다.",
    "{city} {dong} 고등학생 {subject} 성적 향상, 체계적인 과외로 가능합니다.",
    "중학교 때는 잘했는데 고등학교에서 갑자기 어려워졌다면, {city} {dong}에서 시작하세요."
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
    "{city} {dong} 고등 {subject}, 오늘 상담받고, 내일부터 달라지세요.",
    "지금이 바로 시작할 때입니다. {city} {dong}에서 {subject} 실력 향상을 시작하세요.",
    "{subject}은 시작이 반입니다. {city} {dong} 학생 여러분, 지금 바로 시작하세요.",
    "더 늦기 전에 시작하세요. {city} {dong}에서 {subject} 잘하는 학생, 여러분도 될 수 있습니다.",
    "고등학교 {subject}, 혼자 고민하지 마세요. {city} {dong}에서 함께하면 달라집니다.",
    "{city} {dong} 학생 여러분의 {subject} 성적 향상을 응원합니다.",
    "{subject} 때문에 대학 못 가면 너무 억울합니다. {city} {dong}에서 지금 시작하세요.",
    "포기하기엔 아직 이릅니다. {city} {dong} 고등학생 {subject}, 함께 해결합시다.",
    "{city} {dong}에서 {subject} 성적을 올리고 싶다면, 지금 연락주세요.",
    "목표 대학을 향해, {city} {dong}에서 {subject} 실력을 키워가세요."
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

def generate_content(city_name, dong, level, subject, index):
    level_info = get_level_info(level)
    subject_info = get_subject_info(subject)

    title_suffix = TITLE_SUFFIXES[index % len(TITLE_SUFFIXES)]
    intro = INTROS[index % len(INTROS)]
    boxes = random.sample(IVORY_BOXES, 7)
    ending = ENDINGS[index % len(ENDINGS)]
    image = IMAGES[index % len(IMAGES)]

    title = f"경기 {city_name} {dong} {level_info['title_ko']} {subject_info['title_ko']} | {title_suffix}"

    content = f'''---
title: "{title}"
date: {datetime.now().strftime("%Y-%m-%d")}
categories:
- {level_info["category"]}
- {subject_info["ko"]}
tags:
- 경기도
- {city_name}
- {dong}
- {level_info["ko"]}{subject_info["tag"]}
- {subject_info["tag"]}
- 내신대비
- 수능대비
description: "경기 {city_name} {dong} 지역 {level_info['ko']} {subject_info['ko']} 과외 전문. 학생 맞춤 1:1 수업으로 내신과 수능을 동시에 준비합니다."
featured_image: "https://images.unsplash.com/{image}?w=1200&h=630&fit=crop"
---

{intro.format(city=city_name, dong=dong, subject=subject_info["ko"])}

{subject_info["ko"]}은 계단식 과목입니다. 앞 단계를 완벽히 이해해야 다음 단계로 넘어갈 수 있습니다.

혼자 공부하면 어디가 문제인지 모를 수 있습니다. 전문가의 도움으로 효율적으로 해결하세요.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[0]}
</div>

## 1:1 과외가 효과적인 이유

1:1 과외의 가장 큰 장점은 맞춤 수업입니다. 학생의 수준에 맞춰 진도를 조절합니다.

질문을 바로 할 수 있습니다. 모르는 게 생기면 그 자리에서 해결합니다.

학생의 약점을 정확히 파악할 수 있습니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[1]}
</div>

## 효과적인 학습 방법

{subject_info["ko"]} 공부의 핵심은 개념 이해입니다. 공식만 외워서는 응용 문제를 풀 수 없습니다.

문제 풀이는 양보다 질입니다. 오답 정리는 필수입니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[2]}
</div>

## 학년별 학습 전략

{level_info["ko"]}1학년은 기초를 다지는 시기입니다. {level_info["ko"]}2학년은 심화 학습을 시작합니다.

{level_info["ko"]}3학년은 정리와 실전 연습의 시기입니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[3]}
</div>

## 자주 하는 실수

가장 흔한 건 계산 실수입니다. 개념을 대충 알고 넘어가는 것도 문제입니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[4]}
</div>

## 시험 대비 전략

시험 2주 전부터 본격적으로 준비하세요. 기출문제를 풀어보세요.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[5]}
</div>

## 수업료 안내

경기 {city_name} {dong} 지역 {level_info['ko']} {subject_info['ko']} 과외 수업료입니다.

{level_info["cost"]}

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

## 마무리

{ending.format(city=city_name, dong=dong, subject=subject_info["ko"])}
'''
    return content

def main():
    base_path = "/home/user/edu-guide/content/gyeonggi"
    total_files = 0
    index = 0

    for region_key, region_data in GYEONGGI_ADMIN_DONGS.items():
        city_name = region_data["city_ko"]
        region_path = os.path.join(base_path, region_key)

        for dong in region_data["admin_dongs"]:
            # 동 폴더 생성
            dong_folder = dong.replace(" ", "-")
            dong_path = os.path.join(region_path, dong_folder)
            os.makedirs(dong_path, exist_ok=True)

            # _index.md 생성
            index_content = f'''---
title: "경기 {city_name} {dong}"
---
'''
            with open(os.path.join(dong_path, "_index.md"), "w", encoding="utf-8") as f:
                f.write(index_content)

            # 4개 파일 생성
            for level in ["middle", "high"]:
                for subject in ["math", "english"]:
                    filename = f"{level}-{subject}.md"
                    filepath = os.path.join(dong_path, filename)

                    content = generate_content(city_name, dong, level, subject, index)

                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(content)

                    total_files += 1
                    index += 1

            print(f"생성 완료: 경기 {city_name} {dong} (4개 파일)")

    print(f"\n총 {total_files}개 파일 생성 완료")

if __name__ == "__main__":
    main()
