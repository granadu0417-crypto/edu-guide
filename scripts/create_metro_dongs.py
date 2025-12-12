#!/usr/bin/env python3
"""
광역시 동 단위 콘텐츠 생성 스크립트
부산, 대구, 대전, 광주, 울산, 세종
"""

import os
import random
from datetime import datetime

# 광역시별 구/동 데이터
CITIES = {
    "busan": {
        "name_ko": "부산",
        "districts": {
            "haeundae": {
                "name_ko": "해운대구",
                "dongs": ["우동", "중동", "좌동", "송정동", "반여동", "반송동", "재송동", "석대동"]
            },
            "busanjin": {
                "name_ko": "부산진구",
                "dongs": ["부전동", "연지동", "초읍동", "양정동", "전포동", "범천동", "가야동", "당감동"]
            },
            "dongnae": {
                "name_ko": "동래구",
                "dongs": ["온천동", "명륜동", "안락동", "명장동", "복산동", "수안동", "사직동", "낙민동"]
            },
            "nam": {
                "name_ko": "남구",
                "dongs": ["대연동", "용호동", "용당동", "감만동", "우암동", "문현동"]
            },
            "buk": {
                "name_ko": "북구",
                "dongs": ["구포동", "덕천동", "만덕동", "금곡동", "화명동"]
            },
            "suyeong": {
                "name_ko": "수영구",
                "dongs": ["수영동", "망미동", "광안동", "민락동", "남천동"]
            },
            "yeonje": {
                "name_ko": "연제구",
                "dongs": ["거제동", "연산동", "연지동"]
            },
            "geumjeong": {
                "name_ko": "금정구",
                "dongs": ["장전동", "부곡동", "서동", "금사동", "회동동", "남산동", "구서동", "청룡동"]
            },
            "saha": {
                "name_ko": "사하구",
                "dongs": ["괴정동", "당리동", "하단동", "신평동", "장림동", "다대동", "구평동"]
            },
            "sasang": {
                "name_ko": "사상구",
                "dongs": ["삼락동", "모라동", "덕포동", "괘법동", "감전동", "주례동", "학장동"]
            },
            "seo": {
                "name_ko": "서구",
                "dongs": ["동대신동", "서대신동", "부민동", "아미동", "초장동", "충무동"]
            },
            "dong": {
                "name_ko": "동구",
                "dongs": ["초량동", "수정동", "좌천동", "범일동"]
            },
            "jung_bs": {
                "name_ko": "중구",
                "dongs": ["중앙동", "동광동", "대청동", "보수동", "부평동", "광복동", "남포동", "영주동"]
            },
            "yeongdo": {
                "name_ko": "영도구",
                "dongs": ["대교동", "남항동", "영선동", "신선동", "봉래동", "청학동", "동삼동"]
            },
            "gangseo_bs": {
                "name_ko": "강서구",
                "dongs": ["대저동", "강동동", "명지동", "신호동", "송정동", "화전동"]
            },
            "gijang": {
                "name_ko": "기장군",
                "dongs": ["기장읍", "장안읍", "정관읍", "일광읍", "철마면"]
            }
        }
    },
    "daegu": {
        "name_ko": "대구",
        "districts": {
            "jung_dg": {
                "name_ko": "중구",
                "dongs": ["동인동", "삼덕동", "성내동", "대신동", "남산동", "대봉동"]
            },
            "dong_dg": {
                "name_ko": "동구",
                "dongs": ["신암동", "신천동", "효목동", "도평동", "불로동", "지저동", "동촌동"]
            },
            "seo_dg": {
                "name_ko": "서구",
                "dongs": ["내당동", "비산동", "평리동", "상리동", "원대동", "이현동"]
            },
            "nam_dg": {
                "name_ko": "남구",
                "dongs": ["이천동", "봉덕동", "대명동"]
            },
            "buk_dg": {
                "name_ko": "북구",
                "dongs": ["침산동", "산격동", "대현동", "복현동", "검단동", "구암동", "태전동", "칠성동"]
            },
            "suseong": {
                "name_ko": "수성구",
                "dongs": ["범어동", "만촌동", "수성동", "황금동", "중동", "상동", "두산동", "지산동", "범물동", "신매동"]
            },
            "dalseo": {
                "name_ko": "달서구",
                "dongs": ["성당동", "두류동", "감삼동", "송현동", "본리동", "월성동", "진천동", "유천동", "상인동", "도원동"]
            },
            "dalseong": {
                "name_ko": "달성군",
                "dongs": ["화원읍", "논공읍", "다사읍", "유가읍", "옥포읍", "현풍읍", "가창면"]
            }
        }
    },
    "daejeon": {
        "name_ko": "대전",
        "districts": {
            "dong_dj": {
                "name_ko": "동구",
                "dongs": ["중앙동", "효동", "판암동", "신흥동", "삼성동", "홍도동", "용전동", "대동"]
            },
            "jung_dj": {
                "name_ko": "중구",
                "dongs": ["은행동", "목동", "중촌동", "대흥동", "문화동", "석교동", "대사동", "부사동", "용두동", "오류동", "태평동"]
            },
            "seo_dj": {
                "name_ko": "서구",
                "dongs": ["복수동", "도마동", "정림동", "변동", "용문동", "탄방동", "둔산동", "월평동", "갈마동", "내동", "만년동"]
            },
            "yuseong": {
                "name_ko": "유성구",
                "dongs": ["진잠동", "원신흥동", "온천동", "봉명동", "구암동", "노은동", "지족동", "관평동", "전민동", "문지동"]
            },
            "daedeok": {
                "name_ko": "대덕구",
                "dongs": ["오정동", "대화동", "읍내동", "신탄진동", "석봉동", "목상동", "법동", "송촌동", "중리동", "비래동"]
            }
        }
    },
    "gwangju": {
        "name_ko": "광주",
        "districts": {
            "dong_gj": {
                "name_ko": "동구",
                "dongs": ["충장동", "금남동", "산수동", "지산동", "서석동", "학동", "남동", "지원동", "계림동", "소태동"]
            },
            "seo_gj": {
                "name_ko": "서구",
                "dongs": ["양동", "농성동", "광천동", "유촌동", "치평동", "쌍촌동", "화정동", "내방동", "금호동"]
            },
            "nam_gj": {
                "name_ko": "남구",
                "dongs": ["양림동", "방림동", "봉선동", "주월동", "월산동", "백운동", "진월동", "대촌동"]
            },
            "buk_gj": {
                "name_ko": "북구",
                "dongs": ["중흥동", "유동", "누문동", "임동", "신안동", "용봉동", "운암동", "동림동", "삼각동", "일곡동", "매곡동", "오치동"]
            },
            "gwangsan": {
                "name_ko": "광산구",
                "dongs": ["송정동", "도산동", "신창동", "운남동", "수완동", "하남동", "첨단동", "월계동", "산월동", "비아동"]
            }
        }
    },
    "ulsan": {
        "name_ko": "울산",
        "districts": {
            "jung_us": {
                "name_ko": "중구",
                "dongs": ["학성동", "복산동", "우정동", "태화동", "성남동", "반구동", "유곡동", "다운동", "약사동"]
            },
            "nam_us": {
                "name_ko": "남구",
                "dongs": ["삼산동", "달동", "무거동", "옥동", "야음동", "신정동", "여천동"]
            },
            "dong_us": {
                "name_ko": "동구",
                "dongs": ["방어동", "일산동", "화정동", "전하동", "미포동", "주전동"]
            },
            "buk_us": {
                "name_ko": "북구",
                "dongs": ["양정동", "호계동", "염포동", "송정동", "명촌동", "진장동", "효문동", "달천동", "농소동"]
            },
            "ulju": {
                "name_ko": "울주군",
                "dongs": ["온양읍", "언양읍", "범서읍", "청량읍", "온산읍", "서생면", "웅촌면"]
            }
        }
    },
    "sejong": {
        "name_ko": "세종",
        "districts": {
            "sejong": {
                "name_ko": "세종시",
                "dongs": ["조치원읍", "한솔동", "새롬동", "도담동", "어진동", "아름동", "종촌동", "고운동", "보람동", "대평동", "소담동", "반곡동"]
            }
        }
    }
}

# 표현 풀
TITLE_SUFFIXES = [
    "내신·수능 맞춤 수업",
    "1:1 맞춤 커리큘럼",
    "개념부터 실전까지",
    "체계적 학습 관리",
    "실력 향상 프로그램",
    "기초부터 심화까지",
    "학교별 내신 특화",
    "맞춤형 학습 설계",
    "전문 과외 수업",
    "성적 향상 솔루션",
    "개인 맞춤 지도",
    "효과적인 학습법",
    "목표 달성 수업",
    "수준별 맞춤 과외",
    "꼼꼼한 1:1 수업"
]

INTROS = [
    "{city} {dong} 학생 여러분, {subject} 성적 때문에 스트레스받고 계신가요? 중학교 때는 잘했는데 고등학교에 와서 갑자기 어려워졌다는 말, 정말 많이 듣습니다.",
    "{city} {dong}에서 {subject} 때문에 고민이시라면 잘 찾아오셨습니다. 혼자 공부하면 어디가 문제인지 모를 수 있습니다.",
    "{subject} 성적이 오르지 않아 고민이신 {city} {dong} 학생 여러분, 공부 방법을 바꿔볼 때입니다.",
    "{city} {dong} 고등학생 여러분, {subject}은 포기 과목이 아닙니다. 제대로 된 방법으로 공부하면 반드시 성적이 오릅니다.",
    "{city} {dong}에서 {subject} 과외를 찾고 계신가요? 학원에서 따라가기 힘들다면 1:1 과외가 답입니다.",
    "{subject} 점수가 안 오르는 {city} {dong} 학생들, 지금 시작해도 늦지 않았습니다. 기초부터 차근차근 잡아드립니다.",
    "{city} {dong} 학부모님, 아이의 {subject} 실력이 걱정되시죠? 전문 과외로 확실하게 잡아드립니다.",
    "{subject}은 계단식 과목입니다. {city} {dong} 학생 여러분, 앞 단계를 완벽히 이해해야 다음 단계로 넘어갈 수 있습니다.",
    "{city} {dong}에서 {subject} 전문 과외를 찾으신다면 주목하세요. 학생 맞춤형 수업으로 실력을 키워드립니다.",
    "고등학교 {subject}, 어디서부터 잡아야 할지 모르겠다면 {city} {dong}에서 시작하세요.",
    "{city} {dong} 학생들의 {subject} 고민, 이해합니다. 실력 있는 선생님과 함께라면 달라질 수 있습니다.",
    "{subject}만 잘해도 대학이 달라집니다. {city} {dong} 고등학생 여러분, 지금 시작하세요.",
    "{city} {dong}에서 {subject} 과외 알아보시나요? 학생의 수준에 맞춘 1:1 맞춤 수업을 제공합니다.",
    "내신과 수능을 동시에 준비해야 하는 {city} {dong} 학생들, {subject}은 전략적으로 공부해야 합니다.",
    "{city} {dong} 고등학생 {subject} 성적 향상, 체계적인 과외로 가능합니다."
]

IVORY_BOXES = [
    "개념 설명 후 바로 문제 풀이로 연결합니다. 이해했는지 즉시 확인하고 넘어갑니다. 애매하게 넘어가지 않습니다.",
    "학생이 이해했는지 직접 설명해보게 합니다. 설명할 수 있어야 진짜 아는 겁니다.",
    "학생의 컨디션도 체크합니다. 공부만 잘한다고 되는 게 아닙니다. 전체적인 케어가 필요합니다.",
    "시험 후에는 함께 오답을 분석합니다. 왜 틀렸는지 파악하고 다음에 같은 실수를 안 하도록 합니다.",
    "매 수업 시작 전 지난 내용을 복습합니다. 까먹기 전에 다시 한번 확인합니다. 복습이 실력입니다.",
    "숙제는 적정량만 내드립니다. 무리하지 않으면서도 실력이 오르도록 합니다. 양보다 질입니다.",
    "학부모님께 주기적으로 학습 상황을 보고드립니다. 함께 아이를 케어합니다. 가정과 연계합니다.",
    "오답 노트를 함께 만들어갑니다. 틀린 문제는 반드시 다시 풀어봅니다. 왜 틀렸는지 분석합니다.",
    "모르는 건 바로 질문하게 합니다. 질문을 두려워하지 않도록 분위기를 만들어줍니다.",
    "첫 수업에서 학생의 현재 실력을 정확하게 진단합니다. 어디서 막히는지 파악한 후 맞춤 계획을 세웁니다.",
    "수업 중에 집중력이 떨어지면 잠시 쉬어갑니다. 억지로 붙잡아서 하는 공부는 효과가 없습니다.",
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
    "{city} {dong} 학생 여러분의 {subject} 성적 향상을 응원합니다. 상담 문의 주세요.",
    "{subject} 때문에 대학 못 가면 너무 억울합니다. {city} {dong}에서 지금 시작하세요.",
    "포기하기엔 아직 이릅니다. {city} {dong} 고등학생 {subject}, 함께 해결합시다.",
    "{city} {dong}에서 {subject} 성적을 올리고 싶다면, 지금 연락주세요.",
    "목표 대학을 향해, {city} {dong}에서 {subject} 실력을 키워가세요."
]

# 이미지 풀
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
    "photo-1521587760476-6c12a4b040da",
    "photo-1507842217343-583bb7270b66",
    "photo-1497633762265-9d179a990aa6",
    "photo-1516979187457-637abb4f9353",
    "photo-1512820790803-83ca734da794",
    "photo-1550399105-c4db5fb85c18",
    "photo-1491841573634-28140fc7ced7",
    "photo-1473186578172-c141e6798cf4",
    "photo-1510154221590-ff0b49f38f88",
    "photo-1481627834876-b7833e8f5570",
    "photo-1474932430478-367dbb6832c1"
]

def get_subject_info(subject_type):
    if subject_type == "math":
        return {
            "ko": "수학",
            "title_ko": "수학과외",
            "tag": "수학과외"
        }
    else:
        return {
            "ko": "영어",
            "title_ko": "영어과외",
            "tag": "영어과외"
        }

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

def generate_content(city_key, city_name, district_name, dong, level, subject, index):
    level_info = get_level_info(level)
    subject_info = get_subject_info(subject)

    # 다양한 표현 선택 (인덱스 기반으로 고르게 분포)
    title_suffix = TITLE_SUFFIXES[index % len(TITLE_SUFFIXES)]
    intro = INTROS[index % len(INTROS)]
    boxes = random.sample(IVORY_BOXES, 7)
    ending = ENDINGS[index % len(ENDINGS)]
    image = IMAGES[index % len(IMAGES)]

    title = f"{city_name} {dong} {level_info['title_ko']} {subject_info['title_ko']} | {title_suffix}"

    content = f'''---
title: "{title}"
date: {datetime.now().strftime("%Y-%m-%d")}
categories:
- {level_info["category"]}
- {subject_info["ko"]}
tags:
- {city_name}
- {dong}
- {level_info["ko"]}{subject_info["tag"]}
- {subject_info["tag"]}
- 내신대비
- 수능대비
description: "{city_name} {dong} 지역 {level_info['ko']} {subject_info['ko']} 과외 전문. 학생 맞춤 1:1 수업으로 내신과 수능을 동시에 준비합니다."
featured_image: "https://images.unsplash.com/{image}?w=1200&h=630&fit=crop"
---

{intro.format(city=city_name, dong=dong, subject=subject_info["ko"])}

{subject_info["ko"]}은 계단식 과목입니다. 앞 단계를 완벽히 이해해야 다음 단계로 넘어갈 수 있습니다. 기초에 빈틈이 있으면 점점 더 힘들어집니다.

혼자 공부하면 어디가 문제인지 모를 수 있습니다. 전문가의 도움을 받으면 효율적으로 문제를 해결할 수 있습니다.

학원에서 따라가기 힘들다면 1:1 과외가 답입니다. 본인의 속도에 맞춰 공부할 수 있습니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[0]}
</div>

## 1:1 과외가 효과적인 이유

1:1 과외의 가장 큰 장점은 맞춤 수업입니다. 학생의 수준에 맞춰 진도를 조절합니다. 이해가 안 되면 더 설명하고, 이해했으면 다음으로 넘어갑니다.

질문을 바로 할 수 있습니다. 모르는 게 생기면 그 자리에서 해결합니다. 학원에서는 질문하기가 어렵습니다.

학생의 약점을 정확히 파악할 수 있습니다. 어떤 유형에서 자주 틀리는지, 어떤 개념이 부족한지 선생님이 알고 있습니다.

학습 습관도 잡아드립니다. 혼자 공부할 때 어떻게 해야 하는지 알려드립니다. 진정한 실력 향상은 자기주도 학습에서 나옵니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[1]}
</div>

## 효과적인 학습 방법

{subject_info["ko"]} 공부의 핵심은 개념 이해입니다. 공식만 외워서는 응용 문제를 풀 수 없습니다. 왜 그런 공식이 나오는지 알아야 합니다.

문제 풀이는 양보다 질입니다. 많이 푸는 것보다 제대로 푸는 게 중요합니다. 한 문제를 풀더라도 풀이 과정을 깔끔하게 쓰세요.

오답 정리는 필수입니다. 틀린 문제는 반드시 다시 풀어봐야 합니다. 왜 틀렸는지 분석하세요.

복습을 습관화하세요. 한 번 배운 내용도 안 보면 잊어버립니다. 누적 복습이 실력 향상의 비결입니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[2]}
</div>

## 학년별 학습 전략

학년별로 전략이 다릅니다. {level_info["ko"]}1학년은 기초를 다지는 시기입니다. 이전 학년 내용에 빈틈이 있다면 먼저 메워야 합니다.

{level_info["ko"]}2학년은 심화 학습을 시작합니다. 핵심 개념들을 충실히 학습하세요. 여기서 배우는 개념들이 시험에 자주 출제됩니다.

{level_info["ko"]}3학년은 정리와 실전 연습의 시기입니다. 기출문제를 많이 풀어보세요. 자주 나오는 유형을 파악하고 풀이 시간을 단축하세요.

내신과 수능의 균형도 중요합니다. 둘 다 잘 봐야 원하는 결과를 얻을 수 있습니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[3]}
</div>


## 자주 하는 실수

학생들이 자주 하는 실수를 알려드립니다. 가장 흔한 건 계산 실수입니다. 급하게 풀다 보면 부호를 틀리거나 숫자를 잘못 쓰는 경우가 많습니다.

개념을 대충 알고 넘어가는 것도 문제입니다. 이해한 것 같아도 막상 문제에 적용하면 막힙니다. 개념은 완벽하게 이해한 후 넘어가야 합니다.

문제를 끝까지 읽지 않는 실수도 있습니다. 조건을 놓치거나, 묻는 것과 다른 답을 쓰는 경우가 있습니다.

검산을 안 하는 것도 실수입니다. 시간이 없어서 검산을 건너뛰는 학생이 많습니다. 하지만 검산으로 잡을 수 있는 실수가 많습니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[4]}
</div>


## 개념 학습의 중요성

{subject_info["ko"]}은 개념이 전부입니다. 공식만 외워서는 한계가 있습니다. 왜 이런 공식이 나오는지 알아야 합니다.

개념서를 꼼꼼히 읽으세요. 교과서도 좋고, 시중 개념서도 좋습니다. 중요한 건 꼼꼼히 읽는 것입니다.

예제를 충분히 풀어보세요. 개념을 읽었다고 다 아는 게 아닙니다. 예제를 직접 풀어봐야 진짜 이해한 것입니다.

개념은 반복해서 봐야 합니다. 한 번 봤다고 완벽히 아는 게 아닙니다. 주기적으로 다시 보세요.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[5]}
</div>


## 시험 대비 전략

시험 대비 방법을 알려드립니다. 시험 2주 전부터 본격적으로 준비하세요. 교과서와 수업 노트를 다시 읽고, 핵심 개념을 정리하세요.

기출문제를 풀어보세요. 학교 시험은 출제 경향이 있습니다. 기출을 분석하면 어떤 유형이 자주 나오는지 알 수 있습니다.

약한 단원을 집중 공략하세요. 모든 단원을 똑같이 공부하면 비효율적입니다.

시험 전날은 새로운 걸 하지 마세요. 이미 아는 내용을 다시 확인하는 정도로 하세요.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[6]}
</div>


## 수업료 안내

{city_name} {dong} 지역 {level_info['ko']} {subject_info['ko']} 과외 수업료입니다.

{level_info["cost"]}

정확한 비용은 학생의 현재 수준과 목표에 따라 달라질 수 있습니다. 상담을 통해 최적의 수업 횟수와 비용을 안내해 드리겠습니다.

{{{{< cta-dual type="final" >}}}}

## 자주 묻는 질문

**Q. 주 몇 회 수업이 좋나요?**

학생 상황에 따라 다릅니다. 기초가 부족하면 주 2-3회, 유지 목적이면 주 1회가 적당합니다.

**Q. 내신과 수능 중 뭘 먼저 해야 하나요?**

학년에 따라 다릅니다. {level_info["ko"]}1-2는 내신 중심으로, {level_info["ko"]}3은 수능 비중을 높여갑니다.

**Q. {subject_info["ko"]}은 언제부터 준비해야 하나요?**

빠를수록 좋습니다. 기초가 부족하다면 지금 바로 시작하세요.

**Q. 선행 학습이 필요한가요?**

무조건적인 선행보다 현재 단계의 완벽한 이해가 더 중요합니다.

## 마무리

{ending.format(city=city_name, dong=dong, subject=subject_info["ko"])}
'''
    return content

def main():
    base_path = "/home/user/edu-guide/content"
    total_files = 0
    index = 0

    for city_key, city_data in CITIES.items():
        city_name = city_data["name_ko"]

        for district_key, district_data in city_data["districts"].items():
            district_name = district_data["name_ko"]

            for dong in district_data["dongs"]:
                # 동 폴더 생성
                dong_path = os.path.join(base_path, city_key, district_key, dong)
                os.makedirs(dong_path, exist_ok=True)

                # _index.md 생성
                index_content = f'''---
title: "{city_name} {dong}"
---
'''
                with open(os.path.join(dong_path, "_index.md"), "w", encoding="utf-8") as f:
                    f.write(index_content)

                # 4개 파일 생성 (중등/고등 x 수학/영어)
                for level in ["middle", "high"]:
                    for subject in ["math", "english"]:
                        filename = f"{level}-{subject}.md"
                        filepath = os.path.join(dong_path, filename)

                        content = generate_content(
                            city_key, city_name, district_name, dong,
                            level, subject, index
                        )

                        with open(filepath, "w", encoding="utf-8") as f:
                            f.write(content)

                        total_files += 1
                        index += 1

                print(f"생성 완료: {city_name} {district_name} {dong} (4개 파일)")

    print(f"\n총 {total_files}개 파일 생성 완료")

if __name__ == "__main__":
    main()
