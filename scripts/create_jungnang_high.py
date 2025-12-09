#!/usr/bin/env python3
"""
중랑구 고등 수학/영어 과외 콘텐츠 생성 스크립트
16개 동 × 2과목 = 32개 파일 생성
"""

import os
from datetime import datetime

# 중랑구 16개 동 정보
JUNGNANG_DONGS = {
    "myeonmokbon": {
        "name": "면목본동",
        "schools": [],
        "high_schools": [],
        "nearby": "면목3·8동",
        "characteristics": "주거 밀집 지역으로 인근 면목고 이용"
    },
    "myeonmok2": {
        "name": "면목2동",
        "schools": [],
        "high_schools": [],
        "nearby": "면목3·8동",
        "characteristics": "주거 중심 지역으로 인근 고등학교 통학"
    },
    "myeonmok38": {
        "name": "면목3·8동",
        "schools": ["면목중", "중화중", "면목고"],
        "high_schools": ["면목고"],
        "nearby": "",
        "characteristics": "면목고가 위치한 중랑구 교육 중심지"
    },
    "myeonmok4": {
        "name": "면목4동",
        "schools": ["용마중"],
        "high_schools": [],
        "nearby": "면목3·8동",
        "characteristics": "용마중 학생들이 면목고 등으로 진학"
    },
    "myeonmok5": {
        "name": "면목5동",
        "schools": [],
        "high_schools": [],
        "nearby": "면목3·8동",
        "characteristics": "주거 환경이 좋은 지역, 인근 고교 통학"
    },
    "myeonmok7": {
        "name": "면목7동",
        "schools": [],
        "high_schools": [],
        "nearby": "면목3·8동",
        "characteristics": "면목역 인근, 교통 편리"
    },
    "sangbong1": {
        "name": "상봉1동",
        "schools": ["신현중", "신현고"],
        "high_schools": ["신현고"],
        "nearby": "",
        "characteristics": "혁신학교 신현고가 위치한 교육 특화 지역"
    },
    "sangbong2": {
        "name": "상봉2동",
        "schools": ["상봉중"],
        "high_schools": [],
        "nearby": "상봉1동",
        "characteristics": "상봉역 역세권, 신현고 통학 편리"
    },
    "junghwa1": {
        "name": "중화1동",
        "schools": ["장안중", "중화고"],
        "high_schools": ["중화고"],
        "nearby": "",
        "characteristics": "중화고가 위치한 학군 우수 지역"
    },
    "junghwa2": {
        "name": "중화2동",
        "schools": ["중랑중"],
        "high_schools": [],
        "nearby": "중화1동",
        "characteristics": "중화고 통학권, 주거 환경 안정적"
    },
    "muk1": {
        "name": "묵1동",
        "schools": ["원묵중", "태릉중", "원묵고", "태릉고"],
        "high_schools": ["원묵고", "태릉고"],
        "nearby": "",
        "characteristics": "중랑구 최대 학군 밀집 지역, 원묵고·태릉고 위치"
    },
    "muk2": {
        "name": "묵2동",
        "schools": [],
        "high_schools": [],
        "nearby": "묵1동",
        "characteristics": "태릉 인근 쾌적한 주거지, 묵1동 고교 이용"
    },
    "mangwubon": {
        "name": "망우본동",
        "schools": ["동원중", "봉화중"],
        "high_schools": [],
        "nearby": "망우3동",
        "characteristics": "전통 주거 지역, 망우3동 고교 통학"
    },
    "mangwu3": {
        "name": "망우3동",
        "schools": ["송곡여중", "혜원여중", "영란여중", "송곡고", "송곡여고", "혜원여고"],
        "high_schools": ["송곡고", "송곡여고", "혜원여고"],
        "nearby": "",
        "characteristics": "중랑구 최대 고교 밀집 지역, 체육중점고 송곡고 위치"
    },
    "sinnae1": {
        "name": "신내1동",
        "schools": [],
        "high_schools": [],
        "nearby": "묵1동, 망우3동",
        "characteristics": "신내역 역세권 신도시, 인근 고교 통학"
    },
    "sinnae2": {
        "name": "신내2동",
        "schools": [],
        "high_schools": [],
        "nearby": "묵1동, 망우3동",
        "characteristics": "신내 뉴타운, 젊은 가구 증가 지역"
    }
}

# 동별 서두 표현 (각각 다르게)
INTRO_VARIATIONS_MATH = {
    "myeonmokbon": "고등학교 수학, 중학교와는 차원이 다릅니다. 지금 시작해야 합니다.",
    "myeonmok2": "수학 성적이 갑자기 떨어졌나요? 고등학교에 와서 그런 학생이 많습니다.",
    "myeonmok38": "면목고 수학 내신, 어렵기로 유명합니다. 철저한 대비가 필요합니다.",
    "myeonmok4": "고등학교 수학이 막막하다면, 지금 바로 손을 잡아드립니다.",
    "myeonmok5": "수포자가 되기 전에, 지금 잡아야 합니다. 고등 수학은 시간이 생명입니다.",
    "myeonmok7": "고등학교 수학, 혼자 하기엔 너무 어렵습니다. 함께 시작하세요.",
    "sangbong1": "신현고 학생 여러분, 혁신학교라고 수학이 쉬운 건 아닙니다.",
    "sangbong2": "상봉2동 고등학생을 위한 맞춤 수학 과외를 소개합니다.",
    "junghwa1": "중화고 내신부터 수능까지, 체계적인 수학 학습이 필요합니다.",
    "junghwa2": "고등학교 수학, 개념이 무너지면 모든 게 무너집니다.",
    "muk1": "원묵고, 태릉고 학생들! 중랑구 최고 학군에서 수학 1등급 도전하세요.",
    "muk2": "묵2동에서 고등 수학 실력을 키워드립니다. 목표는 1등급입니다.",
    "mangwubon": "망우본동 고등학생 여러분, 수학 때문에 고민이시라면 읽어보세요.",
    "mangwu3": "송곡고, 송곡여고, 혜원여고 학생들의 수학 파트너가 되어드립니다.",
    "sinnae1": "신내1동 고등학생을 위한 프리미엄 수학 과외입니다.",
    "sinnae2": "신내2동에서 고등 수학 실력을 확실히 올려드립니다."
}

INTRO_VARIATIONS_ENGLISH = {
    "myeonmokbon": "수능 영어 1등급, 꾸준히 하면 가능합니다. 지금 시작하세요.",
    "myeonmok2": "영어 등급이 안 나온다면, 공부 방법을 바꿔야 합니다.",
    "myeonmok38": "면목고 영어 내신과 수능을 동시에 잡는 전략을 알려드립니다.",
    "myeonmok4": "고등학교 영어, 중학교와 다릅니다. 체계적인 학습이 필요합니다.",
    "myeonmok5": "영어는 꾸준함입니다. 매일 조금씩, 확실하게 실력을 올려드립니다.",
    "myeonmok7": "영어 때문에 대학 못 가면 너무 억울하지 않나요? 지금 시작하세요.",
    "sangbong1": "신현고 영어 내신, 까다롭습니다. 학교별 맞춤 대비가 필요합니다.",
    "sangbong2": "상봉2동 고등학생을 위한 1:1 맞춤 영어 과외입니다.",
    "junghwa1": "중화고 영어, 내신과 수능 모두 잡는 전략이 있습니다.",
    "junghwa2": "고등학교 영어 성적이 제자리라면, 방법을 바꿔보세요.",
    "muk1": "원묵고, 태릉고 영어 내신 1등급 도전! 체계적으로 준비합니다.",
    "muk2": "묵2동에서 영어 실력을 확실히 올려드립니다.",
    "mangwubon": "망우본동 고등학생을 위한 프리미엄 영어 과외입니다.",
    "mangwu3": "송곡고, 송곡여고, 혜원여고 영어 시험 패턴을 완벽 분석합니다.",
    "sinnae1": "신내1동에서 고등 영어 실력 향상을 도와드립니다.",
    "sinnae2": "신내2동 고등학생을 위한 맞춤형 영어 수업을 제안합니다."
}

# 이미지 풀 (수학, 영어 각각 - 중등과 다른 이미지 사용)
MATH_IMAGES = [
    "photo-1516979187457-637abb4f9353",
    "photo-1453733190371-0a9bedd82893",
    "photo-1503676260728-1c00da094a0b",
    "photo-1522202176988-66273c2fd55f",
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
    "photo-1501504905252-473c47e087f8",
    "photo-1509869175650-a1d97972541a"
]

ENGLISH_IMAGES = [
    "photo-1507842217343-583bb7270b66",
    "photo-1497633762265-9d179a990aa6",
    "photo-1512820790803-83ca734da794",
    "photo-1550399105-c4db5fb85c18",
    "photo-1491841573634-28140fc7ced7",
    "photo-1473186578172-c141e6798cf4",
    "photo-1510154221590-ff0b49f38f88",
    "photo-1481627834876-b7833e8f5570",
    "photo-1474932430478-367dbb6832c1",
    "photo-1532012197267-da84d127e765",
    "photo-1506880018603-83d5b814b5a6",
    "photo-1519682337058-a94d519337bc",
    "photo-1544716278-ca5e3f4abd8c",
    "photo-1515879218367-8466d910aaa4",
    "photo-1489533119213-66a5cd877091",
    "photo-1517842645767-c639042777db"
]

def get_high_school_text(dong_info):
    """고등학교 정보 텍스트 생성"""
    high_schools = dong_info.get("high_schools", [])

    if high_schools:
        return ", ".join(high_schools)
    elif dong_info["nearby"]:
        return f"인근 {dong_info['nearby']} 지역 고등학교"
    else:
        return "중랑구 관내 고등학교"

def generate_math_content(dong_key, dong_info, image_id):
    """수학 과외 콘텐츠 생성"""
    dong_name = dong_info["name"]
    high_schools = dong_info.get("high_schools", [])
    school_display = ", ".join(high_schools) if high_schools else "중랑구 관내 고등학교"
    intro = INTRO_VARIATIONS_MATH[dong_key]

    # 학교별 특화 섹션
    if high_schools:
        if "신현고" in high_schools:
            school_section = f"""## 신현고 수학 내신의 특징

신현고는 서울시 혁신학교입니다. 혁신학교라고 해서 시험이 쉬운 것은 아닙니다. 오히려 창의적 사고력을 요구하는 문제가 많이 출제됩니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
신현고의 출제 스타일에 맞춰 단순 계산보다 개념 이해와 응용력을 키웁니다. 서술형 문제 비중이 높으므로 풀이 과정 작성 연습을 철저히 합니다.
</div>

혁신학교 특성상 수행평가 비중도 높습니다. 수행평가와 지필고사를 균형 있게 준비해야 좋은 성적을 받을 수 있습니다."""

        elif "송곡고" in high_schools:
            school_section = f"""## 송곡고 수학 내신의 특징

송곡고는 국내 최초 체육중점고등학교입니다. 체육 특기생이 많지만, 일반 학생들도 함께 공부합니다. 수학 시험은 기본 개념 위주로 출제되는 편입니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
송곡고 기출문제를 분석하여 자주 나오는 유형을 집중 학습합니다. 기본 개념을 확실히 잡고, 계산 실수를 줄이는 훈련을 합니다.
</div>

체육중점고라는 특성상 진로가 다양합니다. 학생의 목표에 맞춰 내신 대비와 수능 대비의 비중을 조절합니다."""

        elif "원묵고" in high_schools or "태릉고" in high_schools:
            school_section = f"""## 원묵고·태릉고 수학 내신의 특징

묵1동은 중랑구에서 가장 학교가 많은 지역입니다. 원묵고와 태릉고 모두 내신 경쟁이 치열합니다. 시험 난이도가 높고 학생들의 학습 의지도 강합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
원묵고, 태릉고 각 학교별 기출문제를 철저히 분석합니다. 출제 교사의 스타일에 맞춰 예상 문제를 풀어보고, 고난도 문제 대비도 함께 진행합니다.
</div>

경쟁이 치열한 만큼, 철저한 준비가 필요합니다. 시험 범위 외에도 심화 문제까지 풀어봐야 상위권을 유지할 수 있습니다."""

        elif "중화고" in high_schools:
            school_section = f"""## 중화고 수학 내신의 특징

중화고는 중랑구 중화동에 위치한 일반고입니다. 수학 시험은 교과서 기본 개념과 응용 문제가 균형 있게 출제됩니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
중화고 기출문제를 분석하여 출제 패턴을 파악합니다. 교과서 예제부터 기출 변형 문제까지 단계별로 학습합니다.
</div>

서술형 비중이 높아지는 추세이므로 풀이 과정을 정확하게 쓰는 연습이 필수입니다."""

        elif "면목고" in high_schools:
            school_section = f"""## 면목고 수학 내신의 특징

면목고는 면목동에 위치한 일반고입니다. 수학 시험은 기본 개념 확인부터 심화 문제까지 다양한 난이도로 출제됩니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
면목고 기출문제를 철저히 분석합니다. 자주 출제되는 유형은 반복 학습하고, 킬러 문항에 대비한 심화 학습도 진행합니다.
</div>

내신과 수능을 균형 있게 준비해야 합니다. 학년별로 비중을 조절하며 학습 계획을 세웁니다."""
        else:
            school_section = f"""## {school_display} 수학 내신의 특징

{high_schools[0]}의 수학 시험은 교과서 기본 개념과 응용 문제가 균형 있게 출제됩니다. 서술형 비중이 높아 풀이 과정 작성 연습이 필수입니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{high_schools[0]} 기출문제를 분석하여 출제 패턴을 파악합니다. 자주 나오는 유형은 반복 학습하고, 서술형 답안 작성법을 훈련합니다.
</div>

시험 2주 전부터는 학교 프린트와 기출문제 위주로 집중 대비합니다."""

    else:
        nearby = dong_info["nearby"]
        school_section = f"""## 인근 학교 수학 내신 대비

{dong_name}에서는 {nearby} 지역 고등학교로 통학하는 학생들이 많습니다. 각 학교별 출제 경향이 다르므로 학교 맞춤형 대비가 중요합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
학생이 다니는 학교의 기출문제를 수집하고 분석합니다. 담당 선생님의 출제 스타일에 맞춰 예상 문제를 풀어보고, 서술형 대비도 함께 진행합니다.
</div>

중랑구에는 특목고나 자사고가 없지만, 노원구 학원가를 이용하는 학생도 많습니다. 하지만 이동 시간을 줄이고 집중 학습하는 것이 더 효율적일 수 있습니다."""

    content = f"""---
title: "중랑구 {dong_name} 고등 수학과외 | {school_display} 내신·수능 대비"
date: {datetime.now().strftime('%Y-%m-%d')}
categories:
  - 고등교육
  - 수학과외
regions:
  - 서울
  - 중랑구
tags:
  - 중랑구수학과외
  - {dong_name}수학과외
  - 고등수학
  - 고등학교수학과외
  - 수능수학
  - 내신대비
description: "중랑구 {dong_name} 고등학생을 위한 1:1 맞춤 수학과외. {school_display} 내신 완벽 대비, 수능 수학까지 체계적으로 지도합니다."
featured_image: "https://images.unsplash.com/{image_id}?w=1200&h=630&fit=crop"
---

{intro}

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
첫 수업에서 학생의 현재 수학 실력을 정확히 진단합니다. 개념 이해도, 계산 정확도, 문제 해결 속도를 파악하고, 부족한 부분부터 차근차근 채워갑니다.
</div>

중랑구는 서울 25개 구 중 유일하게 특목고와 자사고가 없는 지역입니다. 그래서 많은 학생들이 노원구 중계동 학원가를 이용합니다. 하지만 이동 시간을 생각하면, 집 근처에서 1:1 과외로 집중 학습하는 것이 더 효율적일 수 있습니다.

## 고등학교 수학이 중학교와 다른 점

고등학교 수학은 중학교 수학과 차원이 다릅니다. 추상적인 개념이 등장하고, 문제의 복잡도가 급격히 증가합니다. 중학교 때 수학을 잘했던 학생도 고등학교에서 어려움을 겪는 경우가 많습니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
고등학교 수학의 핵심은 개념 이해입니다. 공식을 암기하는 것이 아니라, 왜 이 공식이 나왔는지, 어떤 상황에서 적용하는지 원리를 이해시킵니다.
</div>

특히 수학 상(공통수학1)에서 배우는 다항식, 방정식, 부등식은 이후 모든 수학 단원의 기초가 됩니다. 이 부분이 흔들리면 수학1, 수학2, 미적분까지 모두 어려워집니다.

{school_section}

## 수능 수학의 특징과 대비 전략

수능 수학은 내신과 다릅니다. 사고력과 응용력, 시간 관리 능력이 모두 필요합니다. 킬러 문항이라 불리는 21번, 29번, 30번이 등급을 결정합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
수능 대비는 기본 개념 완성 → 유형별 문제 풀이 → 킬러 문항 공략 → 실전 모의고사 순서로 진행합니다. 시간 배분 전략도 함께 훈련합니다.
</div>

100분 안에 30문항을 풀어야 하므로, 쉬운 문제는 빠르게 풀고 어려운 문제에 시간을 할당하는 전략이 필요합니다. 실전 감각을 키우기 위해 정기적인 모의고사 풀이를 진행합니다.

## 고등학교 수학 핵심 단원별 학습법

### 수학 상·하 (공통수학1·2)

다항식의 연산, 방정식과 부등식, 도형의 방정식은 고등학교 수학의 기초입니다. 이 단원을 완벽히 이해해야 이후 학습이 수월합니다.

집합과 명제, 함수의 개념도 중요합니다. 특히 함수는 수학1, 수학2, 미적분에서 계속 등장하므로 확실히 이해해야 합니다.

### 수학I

지수함수와 로그함수, 삼각함수가 핵심입니다. 이 단원들은 수능에서 자주 출제되며, 킬러 문항의 소재가 되기도 합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
삼각함수는 공식이 많아 암기에 부담을 느끼는 학생이 많습니다. 공식의 유도 과정을 이해하면 암기량을 줄이고 응용력을 키울 수 있습니다.
</div>

수열은 등차수열, 등비수열의 기본 개념부터 여러 가지 수열의 합, 수학적 귀납법까지 체계적으로 학습합니다.

### 수학II

함수의 극한과 연속, 미분과 적분은 미적분의 기초입니다. 다항함수의 미분법과 적분법을 확실히 익혀야 합니다.

미분과 적분의 개념을 이해하면 물리, 경제학 등 다양한 분야에서 활용할 수 있습니다. 단순 계산이 아닌 의미를 이해하는 학습이 중요합니다.

### 미적분 (선택과목)

이공계 진학을 목표로 하는 학생들에게 미적분은 필수입니다. 여러 가지 함수의 미분법, 여러 가지 적분법, 급수 등 심화 내용을 다룹니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
미적분은 계산량이 많고 복잡합니다. 계산 실수를 줄이기 위한 체크 포인트를 정해두고, 검산 습관을 기릅니다.
</div>

## 학년별 학습 전략

### 고등학교 1학년

고1은 고등학교 수학의 기초를 다지는 시기입니다. 수학 상·하를 완벽히 이해해야 고2, 고3에서 무너지지 않습니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
고1 학생에게는 개념 이해와 내신 대비를 중심으로 수업합니다. 선행보다는 현재 배우는 내용을 확실히 이해하는 것이 우선입니다.
</div>

고1 때 수학에 자신감을 잃으면 고2, 고3에서 회복하기 어렵습니다. 성취감을 느낄 수 있도록 단계별로 학습을 진행합니다.

### 고등학교 2학년

고2는 내신과 수능 대비를 본격적으로 시작하는 시기입니다. 수학1, 수학2를 배우며, 선택과목(미적분, 확률과 통계, 기하)을 결정해야 합니다.

선택과목 결정은 진로와 밀접한 관련이 있습니다. 이공계는 미적분, 상경계는 확률과 통계를 선택하는 경우가 많습니다. 학생의 진로에 맞게 조언해드립니다.

### 고등학교 3학년

고3은 수능에 집중하는 시기입니다. 개념 정리는 1학기까지 마무리하고, 2학기부터는 문제 풀이와 실전 감각 훈련에 집중합니다.

킬러 문항 대비, 시간 배분 전략, 실전 모의고사 풀이 등 수능에 필요한 모든 것을 준비합니다.

## 내신 시험 대비 전략

### 시험 4주 전

시험 범위의 개념을 총정리합니다. 교과서와 프린트의 모든 문제를 풀어보고, 모르는 부분을 체크합니다.

### 시험 2주 전

기출문제와 학교 프린트를 집중적으로 풀이합니다. 오답노트를 만들어 자주 틀리는 유형을 파악합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
시험 2주 전부터는 실전 모의고사 형식으로 수업을 진행합니다. 시간 배분 연습과 서술형 답안 작성 요령을 집중 훈련합니다.
</div>

### 시험 1주 전

틀린 문제만 다시 풀어봅니다. 새로운 문제보다 기존 실수를 줄이는 데 집중합니다. 공식 정리와 계산 실수 체크 포인트를 최종 점검합니다.

## 오답노트 작성법

오답노트는 수학 실력 향상의 핵심입니다. 단순히 틀린 문제를 베끼는 것이 아니라, 왜 틀렸는지 원인을 분석하고 다시는 같은 실수를 하지 않도록 정리해야 합니다.

틀린 문제를 그대로 옮겨 적고, 내가 쓴 풀이와 정답 풀이를 비교합니다. 어디서 잘못 생각했는지, 어떤 개념이 부족했는지 명확히 적어둡니다. 시험 전에 오답노트만 봐도 약점을 효과적으로 보완할 수 있습니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
매 수업 시작 시 지난 시간에 틀린 문제를 다시 풀어봅니다. 같은 유형을 반복해서 틀리지 않도록 완벽하게 이해할 때까지 반복합니다.
</div>

## 좋은 학습 습관 만들기

수학 실력은 하루아침에 오르지 않습니다. 매일 꾸준히 공부하는 습관이 중요합니다. 하루 2시간 이상 수학을 공부하면 한 달 후에는 분명 달라진 실력을 느낄 수 있습니다.

문제를 풀 때는 시간을 정해놓고 푸는 습관을 들입니다. 수능에서는 시간이 제한되어 있기 때문에 평소에도 시간 압박 속에서 문제를 푸는 연습을 해야 합니다. 또한, 풀이 과정을 깔끔하게 쓰는 습관도 중요합니다.

## 수업료 안내

고등 수학과외 수업료는 다음과 같습니다.

**고1~2**는 주1회 기준 25만원에서 35만원, 주2회 기준 42만원에서 58만원 선입니다.

**고3**은 주1회 기준 30만원에서 42만원, 주2회 기준 50만원에서 70만원이 일반적입니다.

수업료는 선생님 경력, 수업 시간, 학생 수준에 따라 달라질 수 있습니다. 정확한 금액은 상담을 통해 안내드립니다.

{{{{< cta-dual type="final" >}}}}

## 자주 묻는 질문

**Q. 수학 기초가 너무 약한데 따라갈 수 있을까요?**

물론입니다. 첫 수업에서 학생의 현재 수준을 정확히 파악하고, 부족한 부분부터 차근차근 채워나갑니다. 필요하다면 중학교 내용까지 복습합니다.

**Q. 내신과 수능 중 어느 쪽에 집중해야 하나요?**

학년에 따라 다릅니다. 고1~2는 내신 위주로, 고3은 수능에 더 집중합니다. 하지만 둘은 별개가 아니므로 균형 있게 준비합니다.

**Q. 노원구 학원 대신 과외를 선택하는 이유가 있나요?**

이동 시간을 아낄 수 있고, 학생 수준에 맞춘 1:1 맞춤 수업이 가능합니다. 학원에서는 질문하기 어려운 부분도 과외에서는 바로 해결할 수 있습니다.

**Q. 선택과목은 어떻게 정하나요?**

진로에 따라 결정합니다. 이공계는 미적분, 상경계는 확률과 통계를 권장합니다. 학생의 목표와 적성에 맞게 조언해드립니다.

**Q. 온라인 수업도 가능한가요?**

가능합니다. 다만 수학은 풀이 과정을 직접 보면서 피드백하는 것이 효과적이므로 대면 수업을 권장합니다. 필요시 화상 수업도 진행 가능합니다.

**Q. 성적이 얼마나 빨리 오르나요?**

학생의 기초 상태와 노력에 따라 다릅니다. 보통 3개월 정도 꾸준히 수업을 받으면 한 등급 이상 향상되는 경우가 많습니다. 기초가 부족한 학생은 조금 더 시간이 필요할 수 있습니다.

**Q. 수능 수학 1등급 받으려면 어떻게 해야 하나요?**

기본 개념을 완벽히 이해하고, 유형별 문제 풀이를 충분히 연습한 후, 킬러 문항까지 공략해야 합니다. 시간 관리 능력도 중요합니다. 꾸준한 모의고사 풀이로 실전 감각을 키워야 합니다.

**Q. 부모님과의 소통은 어떻게 하나요?**

정기적으로 학습 상황을 보고드립니다. 매 수업 후 간단한 피드백을 전달하고, 한 달에 한 번 이상 자세한 학습 보고서를 제공합니다. 모의고사 결과와 향후 학습 방향에 대해서도 상담해드립니다.

## 과외 선생님 선택 기준

좋은 과외 선생님을 선택하는 것은 매우 중요합니다. 단순히 경력이 오래되었다고 좋은 것이 아닙니다. 학생과의 소통 능력, 수업 준비 정도, 학습 관리 시스템을 종합적으로 고려해야 합니다.

고등학교 수학은 특히 선생님의 역량이 중요합니다. 개념을 명확하게 설명할 수 있는지, 다양한 문제 유형에 대응할 수 있는지, 학생의 약점을 정확히 파악하고 보완해줄 수 있는지 확인하세요.

## 마무리

중랑구 {dong_name} 고등학생 여러분, 수학 때문에 고민이라면 지금 시작하세요. 고등학교 수학은 어렵지만, 제대로 된 방법으로 공부하면 반드시 오릅니다. 함께 시작해보시겠습니까?
"""
    return content


def generate_english_content(dong_key, dong_info, image_id):
    """영어 과외 콘텐츠 생성"""
    dong_name = dong_info["name"]
    high_schools = dong_info.get("high_schools", [])
    school_display = ", ".join(high_schools) if high_schools else "중랑구 관내 고등학교"
    intro = INTRO_VARIATIONS_ENGLISH[dong_key]

    # 학교별 특화 섹션
    if high_schools:
        if "신현고" in high_schools:
            school_section = f"""## 신현고 영어 내신의 특징

신현고는 혁신학교로서 창의적 사고력을 강조합니다. 영어 시험에서도 단순 암기보다 독해력과 응용력을 요구하는 문제가 많이 출제됩니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
신현고 영어 기출을 분석하여 출제 패턴을 파악합니다. 교과서 본문 암기뿐 아니라 변형 문제와 응용 문제에도 대비합니다.
</div>

수행평가 비중도 높으므로 발표, 에세이 작성 등도 함께 준비합니다."""

        elif "송곡고" in high_schools or "송곡여고" in high_schools or "혜원여고" in high_schools:
            school_names = [s for s in high_schools if "고" in s]
            school_section = f"""## {', '.join(school_names)} 영어 내신의 특징

망우3동은 중랑구에서 고등학교가 가장 많은 지역입니다. {', '.join(school_names)} 각각 영어 시험 스타일이 다르므로 학교별 맞춤 대비가 중요합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
각 학교의 기출문제를 수집하고 분석합니다. 담당 선생님의 출제 스타일에 맞춰 예상 문제를 준비하고 서술형 대비도 함께 진행합니다.
</div>

여학교가 많은 지역 특성상 꼼꼼한 준비가 필요합니다. 체계적인 학습 계획으로 내신 상위권을 목표로 합니다."""

        elif "원묵고" in high_schools or "태릉고" in high_schools:
            school_section = f"""## 원묵고·태릉고 영어 내신의 특징

묵1동은 중랑구 최대 학군 밀집 지역입니다. 원묵고와 태릉고 모두 영어 내신 경쟁이 치열합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
원묵고, 태릉고 각 학교별 영어 기출문제를 철저히 분석합니다. 교과서 본문 암기, 문법 정리, 서술형 대비를 체계적으로 진행합니다.
</div>

경쟁이 치열한 만큼 완벽한 준비가 필요합니다. 시험 범위 본문을 100% 암기하고, 변형 문제까지 대비합니다."""

        elif "중화고" in high_schools:
            school_section = f"""## 중화고 영어 내신의 특징

중화고 영어 시험은 교과서 본문 암기와 문법 문제가 중심입니다. 서술형에서는 영작문과 문장 전환 문제가 출제됩니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
중화고 기출문제를 분석하여 자주 나오는 문법 포인트를 정리합니다. 교과서 본문은 암기뿐 아니라 응용 문제까지 대비합니다.
</div>

듣기평가 비중도 있으므로 정기적인 듣기 훈련으로 실전 감각을 유지합니다."""

        elif "면목고" in high_schools:
            school_section = f"""## 면목고 영어 내신의 특징

면목고 영어 시험은 기본 개념 확인부터 심화 문제까지 다양한 난이도로 출제됩니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
면목고 영어 기출을 철저히 분석합니다. 자주 출제되는 문법 유형은 반복 학습하고, 서술형 답안 작성법을 훈련합니다.
</div>

내신과 수능을 균형 있게 준비해야 합니다. 학년별로 비중을 조절하며 학습합니다."""
        else:
            school_section = f"""## {school_display} 영어 내신의 특징

{high_schools[0]}의 영어 시험은 교과서 본문 암기와 문법 문제가 주를 이룹니다. 서술형에서는 영작문과 문장 전환 문제가 자주 출제됩니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{high_schools[0]} 영어 기출문제를 분석하여 자주 나오는 문법 포인트를 정리합니다. 교과서 본문은 암기뿐 아니라 응용 문제까지 대비합니다.
</div>

듣기평가 비중도 무시할 수 없습니다. 정기적인 듣기 훈련으로 실전 감각을 유지합니다."""

    else:
        nearby = dong_info["nearby"]
        school_section = f"""## 인근 학교 영어 내신 대비

{dong_name}에서는 {nearby} 지역 고등학교로 통학하는 학생들이 많습니다. 학교마다 영어 시험 스타일이 다르므로 맞춤 대비가 중요합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
학생이 다니는 학교의 영어 기출문제를 수집하여 출제 패턴을 분석합니다. 교과서 본문 학습과 문법 정리를 병행하여 내신에 대비합니다.
</div>

중랑구에는 특목고나 자사고가 없지만, 노원구 학원가를 이용하는 학생도 많습니다. 하지만 이동 시간을 줄이고 집중 학습하는 것이 더 효율적일 수 있습니다."""

    content = f"""---
title: "중랑구 {dong_name} 고등 영어과외 | {school_display} 내신·수능 대비"
date: {datetime.now().strftime('%Y-%m-%d')}
categories:
  - 고등교육
  - 영어과외
regions:
  - 서울
  - 중랑구
tags:
  - 중랑구영어과외
  - {dong_name}영어과외
  - 고등영어
  - 고등학교영어과외
  - 수능영어
  - 영어내신
description: "중랑구 {dong_name} 고등학생을 위한 1:1 맞춤 영어과외. {school_display} 내신 완벽 대비, 수능 영어까지 체계적으로 지도합니다."
featured_image: "https://images.unsplash.com/{image_id}?w=1200&h=630&fit=crop"
---

{intro}

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
첫 수업에서 학생의 영어 실력을 종합 진단합니다. 문법, 어휘, 독해, 듣기 각 영역의 수준을 파악하고 약점부터 집중 보완합니다.
</div>

중랑구는 서울 25개 구 중 유일하게 특목고와 자사고가 없는 지역입니다. 그래서 많은 학생들이 노원구 중계동 학원가를 이용합니다. 하지만 영어는 매일 꾸준히 공부하는 것이 중요합니다. 이동 시간을 줄이고 집중 학습하는 것이 더 효과적일 수 있습니다.

## 고등학교 영어가 중학교와 다른 점

고등학교 영어는 중학교와 차원이 다릅니다. 어휘 수준이 높아지고, 문장 구조가 복잡해지며, 독해 지문이 길어집니다. 수능 영어는 독해 속도와 정확성이 모두 요구됩니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
고등학교 영어의 핵심은 구문 분석 능력입니다. 긴 문장을 끊어 읽고, 주어와 동사를 찾고, 문장 구조를 파악하는 연습을 합니다.
</div>

특히 관계사절, 분사구문, 가정법 등 복잡한 문법 구조가 등장합니다. 이런 구문을 정확히 해석할 수 있어야 독해 속도가 빨라집니다.

{school_section}

## 수능 영어의 특징과 대비 전략

수능 영어는 2018학년도부터 절대평가로 전환되었습니다. 90점 이상이면 1등급이지만, 결코 쉽지 않습니다. 빈칸 추론, 순서 배열, 문장 삽입 등 고난도 유형이 등급을 결정합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
수능 영어 대비는 어휘 완성 → 구문 분석 → 유형별 풀이 → 실전 모의고사 순서로 진행합니다. 70분 안에 45문항을 풀어야 하므로 시간 배분 전략도 훈련합니다.
</div>

듣기는 17문항으로 비중이 크지만, 꾸준히 연습하면 만점을 받을 수 있는 영역입니다. 독해 영역에서 실수를 줄이는 것이 1등급의 열쇠입니다.

## 고등학교 영어 핵심 영역별 학습법

### 어휘 영역

수능에 나오는 어휘 수준은 중학교보다 훨씬 높습니다. 필수 어휘 약 3,500개를 체계적으로 암기해야 합니다.

어휘는 단순 암기보다 문맥 속에서 익히는 것이 효과적입니다. 독해 지문에서 모르는 단어를 정리하고, 예문과 함께 암기합니다. 단어장을 만들어 매일 복습하고, 틀린 단어는 표시해두어 반복 학습합니다.

### 문법 영역

고등학교 문법은 중학교 문법의 심화입니다. 관계대명사, 분사구문, 가정법, 도치 구문 등 복잡한 문법이 등장합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
문법은 암기가 아닌 이해가 중요합니다. 왜 이런 문법 규칙이 있는지, 어떤 상황에서 사용하는지 원리를 설명합니다.
</div>

내신 시험에서는 문법 문제 비중이 높습니다. 수능에서는 직접 출제되지 않지만, 독해의 기초가 되므로 확실히 익혀야 합니다.

### 독해 영역

독해는 어휘와 문법의 종합입니다. 글의 주제, 요지, 제목을 파악하고, 빈칸 추론, 순서 배열, 문장 삽입 등 유형별 풀이 전략을 익혀야 합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
독해 수업에서는 끊어 읽기, 구문 분석, 핵심 문장 찾기를 연습합니다. 유형별 접근법을 익히고, 실전에서 적용할 수 있도록 훈련합니다.
</div>

### 듣기 영역

수능 듣기는 17문항, 25분입니다. 꾸준히 연습하면 만점을 받을 수 있는 영역입니다.

매일 15~20분씩 듣기 연습을 하면 한 학기 만에도 눈에 띄는 향상을 볼 수 있습니다. EBS 연계 교재 듣기 파일을 활용합니다.

## 학년별 학습 전략

### 고등학교 1학년

고1은 고등학교 영어의 기초를 다지는 시기입니다. 어휘력을 키우고, 문법을 정리하며, 독해 기초를 쌓습니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
고1 학생에게는 내신 대비와 함께 영어 기초 체력을 키우는 데 집중합니다. 어휘 암기 습관과 독해 루틴을 만들어줍니다.
</div>

고1 때 영어 습관이 고등학교 3년을 결정합니다. 매일 영어 공부 시간을 확보하고, 꾸준히 하는 습관을 들입니다.

### 고등학교 2학년

고2는 내신과 수능 대비를 본격적으로 시작하는 시기입니다. 수능 유형에 익숙해지고, 고난도 문제에 대비합니다.

EBS 연계 교재 학습을 시작합니다. 수능에서 EBS 연계율이 높으므로 EBS 교재를 꼼꼼히 공부해야 합니다.

### 고등학교 3학년

고3은 수능에 집중하는 시기입니다. 기본 개념 정리는 1학기까지 마무리하고, 2학기부터는 실전 감각 훈련에 집중합니다.

모의고사 풀이와 오답 분석을 반복합니다. 실수를 줄이고, 시간 배분 전략을 세웁니다.

## 내신 시험 대비 전략

### 시험 4주 전

시험 범위 교과서 본문을 완벽히 암기합니다. 본문 속 문법 포인트와 주요 표현을 정리합니다.

### 시험 2주 전

학교 프린트와 기출문제를 집중 풀이합니다. 서술형 문제 유형을 파악하고 영작 연습을 합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
시험 2주 전부터는 실전 모의고사를 통해 시간 배분을 연습합니다. 서술형 답안 작성 요령과 부분 점수 받는 방법을 집중 훈련합니다.
</div>

### 시험 1주 전

틀린 문제만 다시 풀고, 교과서 본문을 다시 한번 점검합니다. 새로운 문제보다 기존 실수를 줄이는 데 집중합니다. 본문 암기가 완벽한지, 핵심 문법 정리가 되어 있는지 최종 점검합니다.

## 효과적인 영어 학습 습관

영어 실력은 하루아침에 오르지 않습니다. 매일 꾸준히 공부하는 습관이 가장 중요합니다. 하루 1시간 이상 영어를 공부하면 한 달 후에는 분명 달라집니다.

단어는 하루에 30~50개씩 꾸준히 외웁니다. 수능 필수 어휘 약 3,500개를 고3이 되기 전에 마스터하는 것이 목표입니다. 외운 단어는 다음 날, 일주일 후, 한 달 후에 다시 확인하는 복습 주기를 지킵니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
매 수업 시작 시 단어 테스트를 진행합니다. 암기가 잘 안 되는 단어는 예문과 함께 다시 학습하고, 다음 시간에 재테스트합니다.
</div>

## EBS 연계 학습법

수능 영어는 EBS 연계율이 높습니다. EBS 수능특강, 수능완성 교재를 꼼꼼히 공부해야 합니다. 본문을 읽고 해석하는 것에서 그치지 않고, 변형 문제까지 대비해야 합니다.

고3이 되기 전에 기본 어휘와 문법을 완성하고, 고3 때는 EBS 교재와 기출문제에 집중하는 것이 효율적입니다. 연계 지문을 정확히 이해하고 있으면 시험장에서 시간을 크게 절약할 수 있습니다.

## 수업료 안내

고등 영어과외 수업료는 다음과 같습니다.

**고1~2**는 주1회 기준 22만원에서 32만원, 주2회 기준 38만원에서 52만원 선입니다.

**고3**은 주1회 기준 28만원에서 38만원, 주2회 기준 45만원에서 62만원이 일반적입니다.

수업료는 선생님 경력, 수업 시간, 학생 수준에 따라 달라질 수 있습니다. 정확한 금액은 상담을 통해 안내드립니다.

{{{{< cta-dual type="final" >}}}}

## 자주 묻는 질문

**Q. 영어 기초가 너무 약한데 따라갈 수 있을까요?**

물론입니다. 학생의 현재 수준에서 시작합니다. 필요하다면 중학교 문법까지 복습합니다. 기초가 약한 학생일수록 1:1 과외의 효과가 큽니다.

**Q. 내신과 수능 중 어느 쪽에 집중해야 하나요?**

학년과 목표에 따라 다릅니다. 고1~2는 내신 위주로, 고3은 수능에 더 집중합니다. 둘은 별개가 아니므로 균형 있게 준비합니다.

**Q. 노원구 학원 대신 과외를 선택하는 이유가 있나요?**

이동 시간을 아낄 수 있고, 학생 수준에 맞춘 1:1 맞춤 수업이 가능합니다. 학원에서는 질문하기 어려운 부분도 과외에서는 바로 해결할 수 있습니다.

**Q. 수능 영어 1등급 받으려면 어떻게 해야 하나요?**

90점 이상이면 1등급입니다. 듣기에서 실수하지 않고, 독해 고난도 유형(빈칸, 순서, 삽입)을 정확히 풀어야 합니다. 꾸준한 연습이 답입니다.

**Q. 온라인 수업도 가능한가요?**

가능합니다. 다만 영어는 발음과 문장 흐름을 실시간으로 교정하는 것이 중요하므로 대면 수업을 권장합니다. 필요시 화상 수업도 진행 가능합니다.

**Q. 영어 성적이 얼마나 빨리 오르나요?**

학생의 기초 상태와 노력에 따라 다릅니다. 꾸준히 수업을 받고 과제를 수행하면 보통 한 학기 안에 한 등급 이상 향상되는 경우가 많습니다. 단어와 문법 기초가 잡히면 성적 향상 속도가 빨라집니다.

**Q. EBS 연계 교재는 언제부터 공부하나요?**

고2 겨울방학부터 시작하는 것이 좋습니다. 고3 때 나오는 EBS 수능특강, 수능완성을 꼼꼼히 공부하면 수능에서 유리합니다. 연계 지문을 미리 학습해두면 시험장에서 시간을 절약할 수 있습니다.

**Q. 부모님과의 소통은 어떻게 하나요?**

정기적으로 학습 상황을 보고드립니다. 매 수업 후 간단한 피드백을 전달하고, 한 달에 한 번 이상 자세한 학습 보고서를 제공합니다. 모의고사 결과와 향후 학습 방향에 대해서도 상담해드립니다.

## 과외 선생님 선택 기준

좋은 과외 선생님을 선택하는 것은 매우 중요합니다. 단순히 영어를 잘한다고 좋은 선생님이 아닙니다. 학생의 수준에 맞게 설명할 수 있는 능력, 학습 동기를 부여하는 능력이 중요합니다.

고등학교 영어는 특히 수능 유형에 대한 이해가 있는 선생님을 선택하는 것이 좋습니다. 최신 출제 경향을 파악하고 있는지, 고난도 문제 해결 전략을 알고 있는지 확인하세요.

## 마무리

중랑구 {dong_name} 고등학생 여러분, 영어 때문에 고민이라면 지금 시작하세요. 영어는 꾸준히 하면 반드시 늡니다. 내신도 수능도 체계적인 준비가 답입니다. 함께 시작해보시겠습니까?
"""
    return content


def main():
    # 출력 디렉토리 확인
    output_dir = "content/high"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    file_count = 0

    for idx, (dong_key, dong_info) in enumerate(JUNGNANG_DONGS.items()):
        # 수학 콘텐츠 생성
        math_image = MATH_IMAGES[idx % len(MATH_IMAGES)]
        math_content = generate_math_content(dong_key, dong_info, math_image)
        math_filename = f"jungnang-{dong_key}-high-math.md"
        math_filepath = os.path.join(output_dir, math_filename)

        with open(math_filepath, 'w', encoding='utf-8') as f:
            f.write(math_content)

        print(f"Created: {math_filename}")
        file_count += 1

        # 영어 콘텐츠 생성
        english_image = ENGLISH_IMAGES[idx % len(ENGLISH_IMAGES)]
        english_content = generate_english_content(dong_key, dong_info, english_image)
        english_filename = f"jungnang-{dong_key}-high-english.md"
        english_filepath = os.path.join(output_dir, english_filename)

        with open(english_filepath, 'w', encoding='utf-8') as f:
            f.write(english_content)

        print(f"Created: {english_filename}")
        file_count += 1

    print(f"\n총 {file_count}개 파일 생성 완료!")


if __name__ == "__main__":
    main()
