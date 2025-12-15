#!/usr/bin/env python3
"""
인천 행정동 콘텐츠 추가 스크립트
기존 법정동에 행정동(숫자 붙은 동) 추가
"""

import os
import random
from datetime import datetime

# 인천 구별 행정동 데이터 (기존에 없는 것만)
INCHEON_ADMIN_DONGS = {
    "bupyeong": {
        "name_ko": "부평구",
        "admin_dongs": ["부평2동", "부평3동", "부평4동", "부평5동", "부평6동",
                       "산곡1동", "산곡2동", "산곡3동", "산곡4동",
                       "청천1동", "청천2동", "삼산1동", "삼산2동",
                       "부개1동", "부개2동", "부개3동", "일신동", "십정1동", "십정2동"]
    },
    "namdong": {
        "name_ko": "남동구",
        "admin_dongs": ["구월1동", "구월2동", "구월3동", "구월4동",
                       "간석1동", "간석2동", "간석3동", "간석4동",
                       "만수1동", "만수2동", "만수3동", "만수4동", "만수5동", "만수6동",
                       "장수서창동", "서창2동", "논현1동", "논현2동", "논현고잔동", "고잔동"]
    },
    "yeonsu": {
        "name_ko": "연수구",
        "admin_dongs": ["연수1동", "연수2동", "연수3동", "청학동", "동춘1동", "동춘2동", "동춘3동",
                       "옥련1동", "옥련2동", "선학동", "송도1동", "송도2동", "송도3동"]
    },
    "michuhol": {
        "name_ko": "미추홀구",
        "admin_dongs": ["숭의1동", "숭의2동", "숭의3동", "숭의4동", "용현1동", "용현2동", "용현3동", "용현4동", "용현5동",
                       "학익1동", "학익2동", "도화1동", "도화2동", "도화3동",
                       "주안1동", "주안2동", "주안3동", "주안4동", "주안5동", "주안6동", "주안7동", "주안8동",
                       "관교동", "문학동"]
    },
    "gyeyang": {
        "name_ko": "계양구",
        "admin_dongs": ["효성1동", "효성2동", "계산1동", "계산2동", "계산3동", "계산4동",
                       "작전1동", "작전2동", "작전서운동", "경서동", "임학동", "용종동",
                       "박촌동", "동양동", "귤현동", "목상동", "병방동"]
    },
    "seo_ic": {
        "name_ko": "서구",
        "admin_dongs": ["검암동", "연희동", "청라1동", "청라2동", "청라3동",
                       "경서동", "가정1동", "가정2동", "가정3동", "석남1동", "석남2동", "석남3동",
                       "신현동", "가좌1동", "가좌2동", "가좌3동", "가좌4동"]
    },
    "dong_ic": {
        "name_ko": "동구",
        "admin_dongs": ["만석동", "화수1동", "화수2동", "송현동", "송림1동", "송림2동",
                       "창영동", "금곡동", "화평동"]
    },
    "jung_ic": {
        "name_ko": "중구",
        "admin_dongs": ["영종동", "운서동", "중산동", "신포동", "연안동", "신흥동", "북성동"]
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
    "인천 {district} {dong} 학생 여러분, {subject} 성적 때문에 고민이신가요?",
    "인천 {district} {dong}에서 {subject} 과외를 찾고 계신가요? 1:1 과외가 답입니다.",
    "{subject} 성적이 오르지 않아 고민이신 인천 {district} {dong} 학생 여러분, 공부 방법을 바꿔볼 때입니다.",
    "인천 {district} {dong} 고등학생 여러분, {subject}은 포기 과목이 아닙니다.",
    "{subject} 점수가 안 오르는 인천 {district} {dong} 학생들, 지금 시작해도 늦지 않았습니다.",
    "인천 {district} {dong} 학부모님, 아이의 {subject} 실력이 걱정되시죠?",
    "{subject}은 계단식 과목입니다. 인천 {district} {dong} 학생 여러분, 기초부터 쌓아가세요.",
    "인천 {district} {dong}에서 {subject} 전문 과외를 찾으신다면 주목하세요.",
    "고등학교 {subject}, 어디서부터 잡아야 할지 모르겠다면 인천 {district} {dong}에서 시작하세요.",
    "인천 {district} {dong} 학생들의 {subject} 고민, 이해합니다.",
    "{subject}만 잘해도 대학이 달라집니다. 인천 {district} {dong} 고등학생 여러분, 지금 시작하세요.",
    "인천 {district} {dong}에서 {subject} 과외 알아보시나요?",
    "내신과 수능을 동시에 준비해야 하는 인천 {district} {dong} 학생들, {subject}은 전략적으로 공부해야 합니다.",
    "인천 {district} {dong} 고등학생 {subject} 성적 향상, 체계적인 과외로 가능합니다.",
    "중학교 때는 잘했는데 고등학교에서 갑자기 어려워졌다면, 인천 {district} {dong}에서 시작하세요."
]

IVORY_BOXES = [
    "개념 설명 후 바로 문제 풀이로 연결합니다.",
    "학생이 이해했는지 직접 설명해보게 합니다.",
    "학생의 컨디션도 체크합니다.",
    "시험 후에는 함께 오답을 분석합니다.",
    "매 수업 시작 전 지난 내용을 복습합니다.",
    "숙제는 적정량만 내드립니다.",
    "학부모님께 주기적으로 학습 상황을 보고드립니다.",
    "오답 노트를 함께 만들어갑니다.",
    "모르는 건 바로 질문하게 합니다.",
    "첫 수업에서 학생의 현재 실력을 정확하게 진단합니다.",
    "수업 중에 집중력이 떨어지면 잠시 쉬어갑니다.",
    "학생의 학교 진도에 맞춰 수업합니다.",
    "단순 암기가 아닌 이해 중심으로 가르칩니다.",
    "매 수업마다 작은 목표를 세우고 달성합니다.",
    "어려운 개념은 쉬운 예시로 설명합니다."
]

ENDINGS = [
    "인천 {district} {dong} 고등 {subject}, 오늘 상담받고, 내일부터 달라지세요.",
    "지금이 바로 시작할 때입니다. 인천 {district} {dong}에서 {subject} 실력 향상을 시작하세요.",
    "{subject}은 시작이 반입니다. 인천 {district} {dong} 학생 여러분, 지금 바로 시작하세요.",
    "더 늦기 전에 시작하세요. 인천 {district} {dong}에서 {subject} 잘하는 학생, 여러분도 될 수 있습니다.",
    "고등학교 {subject}, 혼자 고민하지 마세요. 인천 {district} {dong}에서 함께하면 달라집니다.",
    "인천 {district} {dong} 학생 여러분의 {subject} 성적 향상을 응원합니다.",
    "{subject} 때문에 대학 못 가면 너무 억울합니다. 인천 {district} {dong}에서 지금 시작하세요.",
    "포기하기엔 아직 이릅니다. 인천 {district} {dong} 고등학생 {subject}, 함께 해결합시다.",
    "인천 {district} {dong}에서 {subject} 성적을 올리고 싶다면, 지금 연락주세요.",
    "목표 대학을 향해, 인천 {district} {dong}에서 {subject} 실력을 키워가세요."
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
    "photo-1553877522-43269d4ea984"
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

    title = f"인천 {district_name} {dong} {level_info['title_ko']} {subject_info['title_ko']} | {title_suffix}"

    content = f'''---
title: "{title}"
date: {datetime.now().strftime("%Y-%m-%d")}
categories:
- {level_info["category"]}
- {subject_info["ko"]}
tags:
- 인천
- {district_name}
- {dong}
- {level_info["ko"]}{subject_info["tag"]}
- {subject_info["tag"]}
- 내신대비
- 수능대비
description: "인천 {district_name} {dong} 지역 {level_info['ko']} {subject_info['ko']} 과외 전문. 학생 맞춤 1:1 수업으로 내신과 수능을 동시에 준비합니다."
featured_image: "https://images.unsplash.com/{image}?w=1200&h=630&fit=crop"
---

{intro.format(district=district_name, dong=dong, subject=subject_info["ko"])}

{subject_info["ko"]}은 계단식 과목입니다. 앞 단계를 완벽히 이해해야 다음 단계로 넘어갈 수 있습니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[0]}
</div>

## 1:1 과외가 효과적인 이유

1:1 과외의 가장 큰 장점은 맞춤 수업입니다. 학생의 수준에 맞춰 진도를 조절합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[1]}
</div>

## 효과적인 학습 방법

{subject_info["ko"]} 공부의 핵심은 개념 이해입니다. 문제 풀이는 양보다 질입니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[2]}
</div>

## 학년별 학습 전략

{level_info["ko"]}1학년은 기초를 다지는 시기입니다. {level_info["ko"]}3학년은 실전 연습의 시기입니다.

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

시험 2주 전부터 본격적으로 준비하세요.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[5]}
</div>

## 수업료 안내

인천 {district_name} {dong} 지역 {level_info['ko']} {subject_info['ko']} 과외 수업료입니다.

{level_info["cost"]}

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[6]}
</div>

{{{{< cta-dual type="final" >}}}}

## 자주 묻는 질문

**Q. 주 몇 회 수업이 좋나요?**

학생 상황에 따라 다릅니다.

**Q. 내신과 수능 중 뭘 먼저 해야 하나요?**

학년에 따라 다릅니다.

## 마무리

{ending.format(district=district_name, dong=dong, subject=subject_info["ko"])}
'''
    return content

def main():
    base_path = "/home/user/edu-guide/content/incheon"
    total_files = 0
    index = 0

    for district_key, district_data in INCHEON_ADMIN_DONGS.items():
        district_name = district_data["name_ko"]
        district_path = os.path.join(base_path, district_key)

        for dong in district_data["admin_dongs"]:
            dong_folder = dong.replace(" ", "-")
            dong_path = os.path.join(district_path, dong_folder)
            os.makedirs(dong_path, exist_ok=True)

            index_content = f'''---
title: "인천 {district_name} {dong}"
---
'''
            with open(os.path.join(dong_path, "_index.md"), "w", encoding="utf-8") as f:
                f.write(index_content)

            for level in ["middle", "high"]:
                for subject in ["math", "english"]:
                    filename = f"{level}-{subject}.md"
                    filepath = os.path.join(dong_path, filename)

                    content = generate_content(district_name, dong, level, subject, index)

                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(content)

                    total_files += 1
                    index += 1

            print(f"생성 완료: 인천 {district_name} {dong} (4개 파일)")

    print(f"\n총 {total_files}개 파일 생성 완료")

if __name__ == "__main__":
    main()
