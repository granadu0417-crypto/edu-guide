#!/usr/bin/env python3
"""용산구 고등 수학/영어 과외 콘텐츠 생성 스크립트"""

import os

# 용산구 16개 동 정보 (고등학교)
YONGSAN_DONGS = [
    {"id": "yongsan2ga", "name": "용산2가동", "schools": ["용산고", "보성여고"], "math_suffix": "내신·수능 완벽 대비", "eng_suffix": "내신·수능 병행"},
    {"id": "hangang-ro", "name": "한강로동", "schools": ["용산고", "보성여고"], "math_suffix": "수학 실력 완성", "eng_suffix": "영어 등급 향상"},
    {"id": "ichon1", "name": "이촌1동", "schools": ["중경고"], "math_suffix": "1:1 맞춤 커리큘럼", "eng_suffix": "독해·문법 마스터"},
    {"id": "ichon2", "name": "이촌2동", "schools": ["중경고"], "math_suffix": "개념부터 심화까지", "eng_suffix": "내신 고득점 전략"},
    {"id": "itaewon1", "name": "이태원1동", "schools": ["오산고", "배문고"], "math_suffix": "학교별 맞춤 수업", "eng_suffix": "수능 영어 1등급"},
    {"id": "itaewon2", "name": "이태원2동", "schools": ["오산고", "배문고"], "math_suffix": "내신 1등급 목표", "eng_suffix": "체계적 영어 학습"},
    {"id": "hannam", "name": "한남동", "schools": ["오산고", "중경고"], "math_suffix": "수능형 문제 완성", "eng_suffix": "영어 실력 도약"},
    {"id": "bogwang", "name": "보광동", "schools": ["오산고"], "math_suffix": "민족학교 전통 계승", "eng_suffix": "내신·수능 특화"},
    {"id": "seobinggo", "name": "서빙고동", "schools": ["중경고", "용산고"], "math_suffix": "체계적 학습 관리", "eng_suffix": "기초부터 실전까지"},
    {"id": "hyochang", "name": "효창동", "schools": ["배문고"], "math_suffix": "수학 자신감 향상", "eng_suffix": "영어 내신 집중"},
    {"id": "cheongpa", "name": "청파동", "schools": ["신광여고"], "math_suffix": "학교 시험 완벽 대비", "eng_suffix": "문법·독해 완성"},
    {"id": "namyeong", "name": "남영동", "schools": ["신광여고", "배문고"], "math_suffix": "맞춤형 진도 관리", "eng_suffix": "수능 대비 특강"},
    {"id": "wonhyoro1", "name": "원효로1동", "schools": ["성심여고", "배문고"], "math_suffix": "개념 완성 수업", "eng_suffix": "독해력 강화"},
    {"id": "wonhyoro2", "name": "원효로2동", "schools": ["성심여고"], "math_suffix": "기초 개념 강화", "eng_suffix": "내신 만점 전략"},
    {"id": "yongmun", "name": "용문동", "schools": ["성심여고", "배문고"], "math_suffix": "단계별 실력 향상", "eng_suffix": "어휘·문법 완성"},
    {"id": "huam", "name": "후암동", "schools": ["용산고", "보성여고"], "math_suffix": "개별 맞춤 지도", "eng_suffix": "체계적 수능 대비"},
]

# 16개 고유한 수학 인트로
MATH_INTROS = [
    ("고등학교 수학, 중학교와 차원이 다릅니다", "개념의 깊이가 달라지고, 문제의 복잡도도 급격히 올라갑니다."),
    ("수학 성적이 떨어졌다면 이유가 있습니다", "고등학교 수학은 중학교 방식으로는 한계가 있습니다."),
    ("수학, 개념이 흔들리면 수능까지 영향 미칩니다", "지금 기초를 확실히 다져야 합니다."),
    ("고등학교 수학, 어디서부터 손대야 할지 막막하다면", "정확한 진단으로 부족한 부분만 집중 공략합니다."),
    ("수학 때문에 대학이 걱정되시나요?", "지금 시작하면 충분히 바꿀 수 있습니다."),
    ("내 아이 수학 실력, 한계에 부딪혔다면", "1:1 맞춤 수업으로 돌파구를 찾아드립니다."),
    ("수학, 공식만 외워서는 수능 못 봅니다", "원리를 이해해야 응용이 됩니다."),
    ("고등학교 수학이 어렵다고요?", "맞습니다. 그래서 제대로 된 도움이 필요합니다."),
    ("수학 자신감이 사라졌나요?", "다시 찾을 수 있습니다. 방법이 중요합니다."),
    ("수학, 혼자 하기엔 한계가 있습니다", "전문가의 도움으로 효율적으로 올려보세요."),
    ("수학 성적 정체기를 겪고 계신가요?", "새로운 접근법이 필요할 때입니다."),
    ("고등학교 수학, 기초부터 다시 시작해도 됩니다", "늦은 게 아닙니다. 제대로 하면 됩니다."),
    ("수학 때문에 밤잠 설치시나요?", "함께 해결책을 찾아드립니다."),
    ("수학, 학원만으로 부족하다면", "1:1 과외가 확실히 다릅니다."),
    ("내신과 수능, 둘 다 잡아야 합니다", "전략적인 학습 계획이 필요합니다."),
    ("수학 포기는 아직 이릅니다", "지금 제대로 시작하면 대학이 달라집니다."),
]

# 16개 고유한 영어 인트로
ENG_INTROS = [
    ("고등학교 영어, 중학교와 완전히 다릅니다", "독해 지문의 난이도가 급격히 올라갑니다."),
    ("영어 성적이 정체되어 있나요?", "방법을 바꾸면 결과도 달라집니다."),
    ("수능 영어 1등급, 전략이 필요합니다", "무작정 공부해서는 한계가 있습니다."),
    ("영어 때문에 대학이 걱정되시나요?", "지금 시작하면 충분히 바꿀 수 있습니다."),
    ("영어 독해가 너무 어렵다면", "문장 구조를 이해하면 길이 보입니다."),
    ("내 아이 영어 실력, 한계에 부딪혔다면", "1:1 맞춤 수업으로 돌파구를 찾아드립니다."),
    ("영어, 단어만 외워서는 수능 못 봅니다", "독해력을 키워야 진짜 실력입니다."),
    ("고등학교 영어가 버겁다고요?", "맞습니다. 그래서 전략적인 학습이 필요합니다."),
    ("영어 자신감이 사라졌나요?", "다시 찾을 수 있습니다. 함께 시작해요."),
    ("영어, 혼자 하기엔 한계가 있습니다", "전문가의 도움으로 효율적으로 올려보세요."),
    ("영어 성적 정체기를 겪고 계신가요?", "새로운 접근법이 필요할 때입니다."),
    ("고등학교 영어, 기초부터 다시 해도 됩니다", "늦은 게 아닙니다. 제대로 하면 됩니다."),
    ("수능 영어, 막막하게 느껴지신다면", "체계적인 학습으로 길을 열어드립니다."),
    ("영어, 학원만으로 부족하다면", "1:1 과외가 확실히 다릅니다."),
    ("내신과 수능 영어, 둘 다 잡아야 합니다", "전략적인 학습 계획이 필요합니다."),
    ("영어 포기는 아직 이릅니다", "지금 제대로 시작하면 등급이 달라집니다."),
]

# 이미지 풀 (용산구 고등용 - 중등과 다른 이미지)
IMAGES = [
    "photo-1503676260728-1c00da094a0b",
    "photo-1427504494785-3a9ca7044f45",
    "photo-1519406596751-0a3ccc4937fe",
    "photo-1524178232363-1fb2b075b655",
    "photo-1509062522246-3755977927d7",
    "photo-1544717305-2782549b5136",
    "photo-1501504905252-473c47e087f8",
    "photo-1509869175650-a1d97972541a",
    "photo-1528980917907-8df7f48f6f2a",
    "photo-1525921429624-479b6a26d84d",
    "photo-1588072432836-e10032774350",
    "photo-1577896851231-70ef18881754",
    "photo-1578574577315-3fbeb0cecdc2",
    "photo-1580582932707-520aed937b7b",
    "photo-1580894732444-8ecded7900cd",
    "photo-1581078426770-6d336e5de7bf",
    "photo-1584697964358-3e14ca57658b",
    "photo-1588196749597-9ff075ee6b5b",
    "photo-1588345921523-c2dcdb7f1dcd",
    "photo-1531482615713-2afd69097998",
    "photo-1515187029135-18ee286d815b",
    "photo-1600195077077-7c815f540a3d",
    "photo-1604134967494-8a9ed3adea0d",
    "photo-1611162617474-5b21e879e113",
    "photo-1594608661623-aa0bd3a69d98",
    "photo-1599687351724-dfa3c4ff81b5",
    "photo-1610484826967-09c5720778c7",
    "photo-1622556498246-755f44ca76f3",
    "photo-1603354350317-6f7aaa5911c5",
    "photo-1607990281513-2c110a25bd8c",
    "photo-1593642632823-8f785ba67e45",
    "photo-1598025678451-af5c59b29c40",
]


def generate_math_content(dong, idx):
    """수학 콘텐츠 생성"""
    intro_title, intro_text = MATH_INTROS[idx % len(MATH_INTROS)]
    schools = "·".join(dong["schools"])
    image = IMAGES[idx % len(IMAGES)]

    content = f'''---
title: "용산구 {dong["name"]} 고등 수학과외 | {schools} {dong["math_suffix"]}"
date: 2025-05-15
categories:
  - 고등교육
  - 수학
regions:
  - 서울
  - 용산구
  - {dong["name"]}
tags:
  - 용산구수학과외
  - {dong["name"]}수학과외
  - 고등수학
  - {dong["schools"][0]}
  - 수능수학
  - 고등수학과외
description: "용산구 {dong["name"]} 고등학생을 위한 수학과외입니다. {schools} 내신 대비와 수능 수학 준비를 위한 1:1 맞춤 수업을 제공합니다."
featured_image: "https://images.unsplash.com/{image}?w=1200&h=630&fit=crop"
---

## {intro_title}

{intro_text} 용산구 {dong["name"]} 고등학생들을 위한 맞춤형 수학 과외를 소개합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
첫 수업에서 학생의 수학 실력을 정밀하게 진단합니다. 개념 이해도, 문제 풀이 속도, 취약 유형을 파악한 후 맞춤 학습 계획을 수립합니다.
</div>

## 고등학교 수학, 무엇이 다른가요?

고등학교 수학은 중학교와 차원이 다릅니다. 수학(상), 수학(하)에서 다항식, 방정식, 함수의 깊이가 확 깊어지고, 수학I, 수학II에서는 지수, 로그, 삼각함수, 미적분까지 등장합니다.

특히 {dong["name"]} 학생들이 다니는 {schools} 등의 학교에서는 내신 경쟁이 치열합니다. 중간·기말고사 한 문제 차이로 등급이 갈리기 때문에 철저한 준비가 필요합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
학교별 시험 출제 경향을 분석하여 맞춤 대비합니다. 기출문제 분석, 예상 문제 풀이, 실전 모의고사로 완벽하게 준비합니다.
</div>

## {dong["name"]} 지역 고등학교 수학 특징

### {dong["schools"][0]} 수학 내신

{dong["schools"][0]}은 용산구 내에서도 수학 시험 난이도가 있는 학교입니다. 기본 개념 문제부터 심화 응용 문제까지 골고루 출제되어, 개념과 응용력을 모두 갖춰야 합니다.

시험 전 2주간은 기출 분석과 실전 연습에 집중합니다. 시간 내에 문제를 정확히 푸는 훈련을 통해 실전에서 실력을 발휘할 수 있도록 합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
학교 선생님별 출제 스타일을 파악합니다. 자주 나오는 유형, 킬러 문제 패턴을 분석하여 시험에 완벽히 대비합니다.
</div>

## 수능 수학 대비 전략

수능 수학은 내신과 다릅니다. 정해진 범위 없이 수학 전체를 다루고, 킬러 문항(21번, 29번, 30번)은 여러 개념을 복합적으로 묻습니다.

100분 안에 30문제를 풀어야 하므로 시간 관리가 중요합니다. 쉬운 문제는 빠르게 해결하고, 어려운 문제에 충분한 시간을 쏟는 전략이 필요합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
수능 기출문제를 철저히 분석합니다. 자주 출제되는 유형, 킬러 문항 공략법을 체계적으로 훈련합니다.
</div>

## 학년별 수학 학습 전략

### 고1 수학

고1은 고등 수학의 기초를 다지는 시기입니다. 수학(상)의 다항식, 방정식, 부등식과 수학(하)의 집합, 명제, 함수가 이후 수학의 기초가 됩니다. 이 시기에 개념을 확실히 잡아야 합니다.

### 고2 수학

고2는 수능 수학의 핵심 내용을 배우는 시기입니다. 수학I의 지수, 로그, 삼각함수와 수학II의 미분, 적분은 수능의 핵심입니다. 이 개념들이 흔들리면 수능에서 좋은 점수를 받기 어렵습니다.

### 고3 수학

고3은 배운 내용을 정리하고 실전 감각을 키우는 시기입니다. 개념을 총정리하고, 수능 기출과 모의고사를 통해 실전 연습을 합니다. 시간 관리, 킬러 문항 대응력을 키웁니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
학년별 학습 로드맵을 제시합니다. 현재 학년에 맞는 목표를 설정하고, 단계적으로 실력을 쌓아갑니다.
</div>

## 용산구 {dong["name"]} 고등 수학 과외 비용

수학 과외 비용은 수업 횟수와 시간에 따라 달라집니다.

**고1~2**는 주1회 기준 25만원에서 35만원, 주2회 기준 42만원에서 58만원 선입니다.

**고3**은 주1회 기준 30만원에서 42만원, 주2회 기준 50만원에서 70만원이 일반적입니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
상담에서 학생의 목표와 현재 실력을 파악한 후, 최적의 수업 계획을 함께 수립합니다.
</div>

## 자주 묻는 질문

**Q. 수학 기초가 많이 부족한데 고등학교 수학을 따라갈 수 있을까요?**

기초가 부족하면 먼저 중학교 핵심 개념부터 빠르게 정리합니다. 부족한 부분만 선별적으로 보완하면 고등학교 수학도 충분히 따라갈 수 있습니다. 1:1 수업이라 개인 속도에 맞춰 진행합니다.

**Q. 내신과 수능 중 어떤 것을 먼저 준비해야 하나요?**

고1~2는 내신에 집중하면서 개념을 탄탄히 쌓습니다. 내신을 준비하면 자연스럽게 수능 기초도 다져집니다. 고3이 되면 내신과 수능을 병행하되, 학기 중에는 내신, 방학에는 수능에 집중합니다.

**Q. 일주일에 몇 번 수업이 적당한가요?**

학생 상황에 따라 다르지만, 보통 주2회를 권장합니다. 수학은 꾸준한 연습이 중요해서 주1회는 복습 간격이 길어질 수 있습니다.

{{< cta-dual type="final" >}}

## 마무리

용산구 {dong["name"]} 고등학생 여러분, 수학은 올바른 방법으로 꾸준히 하면 반드시 성적이 오릅니다. 지금 시작해서 내신과 수능 모두 잡으세요. 함께 목표를 이뤄나가겠습니다.
'''
    return content


def generate_english_content(dong, idx):
    """영어 콘텐츠 생성"""
    intro_title, intro_text = ENG_INTROS[idx % len(ENG_INTROS)]
    schools = "·".join(dong["schools"])
    image = IMAGES[(idx + 16) % len(IMAGES)]

    content = f'''---
title: "용산구 {dong["name"]} 고등 영어과외 | {schools} {dong["eng_suffix"]}"
date: 2025-05-15
categories:
  - 고등교육
  - 영어
regions:
  - 서울
  - 용산구
  - {dong["name"]}
tags:
  - 용산구영어과외
  - {dong["name"]}영어과외
  - 고등영어
  - {dong["schools"][0]}
  - 수능영어
  - 고등영어과외
description: "용산구 {dong["name"]} 고등학생을 위한 영어과외입니다. {schools} 내신 대비와 수능 영어 준비를 위한 1:1 맞춤 수업을 제공합니다."
featured_image: "https://images.unsplash.com/{image}?w=1200&h=630&fit=crop"
---

## {intro_title}

{intro_text} 용산구 {dong["name"]} 고등학생들을 위한 맞춤형 영어 과외를 소개합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
첫 수업에서 문법, 독해, 어휘력을 종합적으로 진단합니다. 현재 실력과 목표를 파악한 후 맞춤형 학습 계획을 수립합니다.
</div>

## 고등학교 영어, 무엇이 다른가요?

고등학교 영어는 중학교와 차원이 다릅니다. 독해 지문의 길이가 길어지고, 어휘 수준이 급격히 올라갑니다. 빈칸 추론, 문장 삽입, 순서 배열 등 고난도 유형이 본격적으로 등장합니다.

특히 {dong["name"]} 학생들이 다니는 {schools} 등의 학교에서는 영어 내신 경쟁이 치열합니다. 교과서 본문 이해는 기본이고, 변형 문제와 외부 지문까지 대비해야 합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
학교별 영어 시험 출제 경향을 분석합니다. 교과서 본문 완벽 이해, 변형 문제 대비, 서술형 영작 연습까지 철저히 준비합니다.
</div>

## {dong["name"]} 지역 고등학교 영어 특징

### {dong["schools"][0]} 영어 내신

{dong["schools"][0]}의 영어 시험은 교과서 본문에 대한 깊은 이해를 요구합니다. 본문의 주제, 요지, 세부 정보를 정확히 파악해야 하고, 문법 변형 문제에도 대응해야 합니다.

서술형 평가에서는 문장 완성, 영작 문제가 출제됩니다. 문법 지식을 바탕으로 정확한 영작이 가능해야 좋은 점수를 받을 수 있습니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
학교 기출문제를 철저히 분석합니다. 자주 출제되는 유형, 서술형 패턴을 파악하여 시험에 완벽히 대비합니다.
</div>

## 수능 영어 대비 전략

수능 영어는 2018학년도부터 절대평가입니다. 90점 이상이면 1등급을 받을 수 있어 상대적으로 안정적인 과목입니다. 하지만 독해력이 부족하면 70점대에 머물 수 있습니다.

수능 영어의 핵심은 빈칸 추론, 문장 삽입, 순서 배열 같은 고난도 유형입니다. 글의 논리적 구조를 파악하는 훈련이 필요합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
수능 기출을 철저히 분석합니다. 고난도 유형별 풀이 전략을 체계적으로 훈련하여 1등급을 목표로 합니다.
</div>

## 학년별 영어 학습 전략

### 고1 영어

고1은 고등 영어의 기초를 다지는 시기입니다. 중학교 문법을 완벽히 정리하고, 고등 수준의 독해에 적응해야 합니다. 어휘력도 본격적으로 늘려가야 할 때입니다.

### 고2 영어

고2는 수능 유형에 익숙해지는 시기입니다. 내신 대비와 함께 수능 기출을 풀어보며 유형별 접근법을 익힙니다. 독해 속도와 정확도를 모두 높여야 합니다.

### 고3 영어

고3은 실전 감각을 완성하는 시기입니다. 수능 형식의 모의고사를 꾸준히 풀며 시간 배분을 연습합니다. 취약 유형을 집중 보완하여 안정적인 점수대를 확보합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
학년별 맞춤 전략을 제시합니다. 현재 학년에 맞는 목표를 설정하고 단계적으로 실력을 쌓아갑니다.
</div>

## 용산구 {dong["name"]} 고등 영어 과외 비용

영어 과외 비용은 수업 횟수와 시간에 따라 달라집니다.

**고1~2**는 주1회 기준 22만원에서 32만원, 주2회 기준 38만원에서 52만원 선입니다.

**고3**은 주1회 기준 28만원에서 38만원, 주2회 기준 45만원에서 62만원이 일반적입니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
상담에서 학생의 목표와 현재 실력을 파악한 후, 최적의 수업 계획을 함께 수립합니다.
</div>

## 자주 묻는 질문

**Q. 영어 독해가 너무 느린데 어떻게 해야 하나요?**

독해 속도는 훈련으로 빨라집니다. 문장 구조 파악 훈련, 끊어 읽기 연습을 통해 점차 속도를 높여갑니다. 구문 분석 능력이 쌓이면 자연스럽게 빨라집니다.

**Q. 내신과 수능 영어, 공부법이 다른가요?**

기본적인 영어 실력(어휘, 문법, 독해력)은 같습니다. 다만 내신은 교과서 중심, 수능은 다양한 지문 독해력이 중요합니다. 내신 기간에는 내신에 집중하고, 방학에는 수능 유형 연습을 합니다.

**Q. 일주일에 몇 번 수업이 적당한가요?**

학생 상황에 따라 다르지만, 보통 주2회를 권장합니다. 영어는 꾸준한 노출이 중요해서 주1회는 간격이 길어질 수 있습니다.

{{< cta-dual type="final" >}}

## 마무리

용산구 {dong["name"]} 고등학생 여러분, 영어는 꾸준히 하면 반드시 성적이 오릅니다. 내신과 수능, 두 마리 토끼를 함께 잡을 수 있습니다. 지금 시작해서 목표를 이뤄나가요.
'''
    return content


def main():
    base_dir = "/home/user/edu-guide/content/high"
    os.makedirs(base_dir, exist_ok=True)

    created_files = []

    for idx, dong in enumerate(YONGSAN_DONGS):
        # 수학 파일 생성
        math_filename = f"yongsan-{dong['id']}-high-math.md"
        math_path = os.path.join(base_dir, math_filename)
        math_content = generate_math_content(dong, idx)
        with open(math_path, 'w', encoding='utf-8') as f:
            f.write(math_content)
        created_files.append(math_filename)

        # 영어 파일 생성
        eng_filename = f"yongsan-{dong['id']}-high-english.md"
        eng_path = os.path.join(base_dir, eng_filename)
        eng_content = generate_english_content(dong, idx)
        with open(eng_path, 'w', encoding='utf-8') as f:
            f.write(eng_content)
        created_files.append(eng_filename)

    print(f"총 {len(created_files)}개 파일 생성 완료!")
    for f in created_files:
        print(f"  - {f}")


if __name__ == "__main__":
    main()
