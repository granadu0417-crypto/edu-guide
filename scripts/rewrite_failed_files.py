#!/usr/bin/env python3
"""실패한 파일 리라이팅 스크립트 (은평구, 중랑구, 용산구)"""

import os
import re
import glob

# 수학용 표현 풀 - 서두 (30개)
MATH_INTRO_POOL = [
    "중학교 수학이 갑자기 어려워졌나요? 초등학교 때와 달라서 당황스러우실 겁니다.",
    "수학 성적이 예전 같지 않다면, 개념부터 다시 잡아야 할 때입니다.",
    "중학교 수학, 어디서부터 손을 대야 할지 막막하시죠?",
    "수학 때문에 스트레스 받는 아이, 이제 해결책을 찾아드립니다.",
    "중학교 들어와서 수학이 안 되기 시작했다면, 기초가 흔들리고 있다는 신호입니다.",
    "수학 실력, 지금 잡지 않으면 고등학교 가서 더 힘들어집니다.",
    "우리 아이 수학, 왜 갑자기 어려워졌을까요?",
    "중학 수학의 벽, 함께 넘어봅시다.",
    "수학 자신감을 되찾을 수 있습니다. 지금 시작하세요.",
    "중학교 수학, 개념만 잡으면 문제가 풀립니다.",
    "수학 포기하기엔 아직 이릅니다. 방법을 알면 달라집니다.",
    "내 아이 수학 실력, 지금 어디쯤일까요?",
    "수학 때문에 고민이라면, 혼자 끙끙대지 마세요.",
    "중학교 수학, 체계적으로 잡으면 고등학교 준비까지 됩니다.",
    "수학이 어려운 게 아니라, 배우는 방법이 안 맞았던 거예요.",
    "중학교 수학 성적, 올릴 수 있습니다.",
    "수학 기초가 탄탄해야 응용이 됩니다.",
    "우리 아이에게 맞는 수학 공부법을 찾아드립니다.",
    "수학 점수 올리고 싶으시죠? 방법이 있습니다.",
    "중학 수학, 지금 놓치면 고등학교 때 두 배로 힘들어요.",
    "수학을 싫어하는 아이도 재미있게 배울 수 있습니다.",
    "개념을 알면 수학이 쉬워집니다.",
    "중학교 수학, 막막하다면 전문가와 함께하세요.",
    "수학 실력은 하루아침에 생기지 않습니다. 꾸준함이 답입니다.",
    "내신 수학, 지금부터 준비하면 충분합니다.",
    "수학 공부, 효율적으로 하는 방법을 알려드립니다.",
    "중학생 수학, 어떻게 해야 잘할 수 있을까요?",
    "수학이 재미없다면, 배우는 방식을 바꿔야 합니다.",
    "중학교 수학, 기초부터 탄탄히 쌓아보세요.",
    "수학 성적 향상의 비결, 알려드립니다."
]

# 영어용 표현 풀 - 서두 (30개)
ENG_INTRO_POOL = [
    "중학교 영어, 갑자기 어려워졌나요? 문법이 본격적으로 시작되면서 많은 학생들이 어려움을 느낍니다.",
    "영어 성적이 떨어지고 있다면, 지금이 잡아야 할 때입니다.",
    "중학교 영어, 어디서부터 손을 대야 할지 모르겠다면 도움을 받으세요.",
    "영어 때문에 스트레스받는 아이, 방법을 바꿔야 합니다.",
    "초등학교 때 잘했는데 중학교 영어가 안 된다면, 문법 기초가 흔들린 겁니다.",
    "영어 실력, 지금 잡지 않으면 고등학교 가서 더 힘들어요.",
    "우리 아이 영어, 왜 점수가 안 나올까요?",
    "중학 영어의 벽, 함께 넘어봅시다.",
    "영어 자신감을 되찾을 수 있습니다. 체계적으로 시작하세요.",
    "중학교 영어, 문법만 잡으면 독해가 됩니다.",
    "영어 포기하기엔 너무 이릅니다. 방법이 있어요.",
    "내 아이 영어 실력, 지금 어디쯤일까요?",
    "영어 때문에 고민이라면, 혼자 끙끙대지 마세요.",
    "중학교 영어, 체계적으로 잡으면 고등학교도 문제없습니다.",
    "영어가 어려운 게 아니라, 배우는 순서가 잘못된 거예요.",
    "중학교 영어 성적, 충분히 올릴 수 있습니다.",
    "문법 기초가 탄탄해야 독해가 됩니다.",
    "우리 아이에게 맞는 영어 공부법을 찾아드립니다.",
    "영어 점수 올리고 싶으시죠? 방법이 있습니다.",
    "중학 영어, 지금 놓치면 고등학교 때 두 배로 힘들어요.",
    "영어를 싫어하는 아이도 재미있게 배울 수 있어요.",
    "문법을 알면 영어가 쉬워집니다.",
    "중학교 영어, 막막하다면 전문가와 함께하세요.",
    "영어 실력은 하루아침에 생기지 않습니다. 꾸준함이 답입니다.",
    "내신 영어, 지금부터 준비하면 충분합니다.",
    "영어 공부, 효율적으로 하는 방법을 알려드립니다.",
    "중학생 영어, 어떻게 해야 잘할 수 있을까요?",
    "영어가 재미없다면, 배우는 방식을 바꿔야 합니다.",
    "중학교 영어, 기초부터 탄탄히 쌓아보세요.",
    "영어 성적 향상의 비결, 알려드립니다."
]

# 고등 수학용 서두 (30개)
HIGH_MATH_INTRO_POOL = [
    "고등학교 수학, 중학교 때와 완전히 다르네요.",
    "수학 성적이 갑자기 떨어졌나요? 고등학교 수학은 차원이 다릅니다.",
    "고등학교 수학, 왜 이렇게 어려운 걸까요?",
    "내 아이 수학, 왜 이렇게 안 오르는 걸까요?",
    "수포자가 되기 전에, 지금 바로 잡아야 합니다.",
    "수학만 잘해도 대학이 달라집니다.",
    "고등학교 수학, 어디서부터 잡아야 할지 모르겠다면",
    "수능 수학, 지금 시작해도 늦지 않습니다.",
    "고등 수학의 벽, 함께 넘어봅시다.",
    "수학 자신감을 되찾을 수 있습니다.",
    "수학 때문에 대학 못 가면 너무 억울하지 않나요?",
    "고등학교 수학, 개념부터 다시 잡아야 합니다.",
    "수학 성적 올리고 싶으시죠? 방법이 있습니다.",
    "고등학교 올라와서 수학이 안 되기 시작했다면",
    "수학 기초가 흔들리면 모든 게 어려워집니다.",
    "내신과 수능, 둘 다 잡아야 합니다.",
    "수학 때문에 고민이라면, 이제 해결책을 찾아보세요.",
    "고등학교 수학, 체계적으로 공부하면 됩니다.",
    "수학 실력, 지금 잡지 않으면 늦습니다.",
    "개념이 되어야 문제가 풀립니다.",
    "고등 수학, 막막하다면 전문가와 함께하세요.",
    "수학 공부법을 바꾸면 성적이 바뀝니다.",
    "지금 시작하면 충분히 따라갈 수 있습니다.",
    "수학은 꾸준함이 답입니다.",
    "고등학교 수학, 기초부터 다시 해도 됩니다.",
    "수학 성적 향상, 불가능하지 않습니다.",
    "개념을 알면 수학이 쉬워집니다.",
    "고등 수학, 제대로 된 방법으로 공부하세요.",
    "수학 때문에 스트레스 받지 마세요.",
    "지금 시작해서 수능까지 가봅시다."
]

# 고등 영어용 서두 (30개)
HIGH_ENG_INTRO_POOL = [
    "수능 영어 1등급, 전략이 필요합니다.",
    "영어 성적이 오르지 않아 고민이신가요?",
    "고등학교 영어, 중학교 때와 완전히 다릅니다.",
    "영어 때문에 대학이 걱정되시나요?",
    "지금 시작하면 충분히 바꿀 수 있습니다.",
    "영어 독해가 너무 어렵다면, 문장 구조를 이해해야 합니다.",
    "수능 영어, 절대평가라고 쉬운 게 아닙니다.",
    "내 아이 영어 실력, 한계에 부딪혔다면",
    "1:1 맞춤 수업으로 돌파구를 찾아드립니다.",
    "영어 자신감을 되찾을 수 있습니다.",
    "고등학교 영어, 기초부터 다시 해도 됩니다.",
    "영어 성적 올리고 싶으시죠? 방법이 있습니다.",
    "내신과 수능 영어, 둘 다 잡아야 합니다.",
    "영어 때문에 고민이라면, 이제 해결책을 찾아보세요.",
    "고등학교 영어, 체계적으로 공부하면 됩니다.",
    "문법과 독해, 균형 잡힌 학습이 필요합니다.",
    "영어 실력, 지금 잡지 않으면 늦습니다.",
    "고등 영어, 막막하다면 전문가와 함께하세요.",
    "영어 공부법을 바꾸면 성적이 바뀝니다.",
    "수능 영어 1등급, 불가능하지 않습니다.",
    "영어는 꾸준함이 답입니다.",
    "지금 시작하면 충분히 따라갈 수 있습니다.",
    "영어 성적 향상의 비결, 알려드립니다.",
    "고등학교 영어, 제대로 된 방법으로 공부하세요.",
    "영어 때문에 스트레스 받지 마세요.",
    "내신 영어도, 수능 영어도 잡을 수 있습니다.",
    "영어 독해 속도, 훈련으로 빨라집니다.",
    "문법이 되면 독해가 됩니다.",
    "영어 실력 향상, 지금 시작하세요.",
    "수능까지 함께 가봅시다."
]

# 아이보리 박스 내용 풀
IVORY_BOX_POOL = [
    "첫 수업에서 학생의 실력을 정확하게 파악합니다. 어떤 개념이 부족한지 확인하고, 맞춤 학습 계획을 세웁니다.",
    "수업 시작 전, 현재 실력을 꼼꼼히 체크합니다. 무작정 진도를 나가지 않습니다.",
    "어디서 막히는지 먼저 알아야 합니다. 진단 후 학생에게 맞는 수업을 설계합니다.",
    "학생마다 부족한 부분이 다릅니다. 정확한 진단 후 맞춤 지도를 시작합니다.",
    "첫 시간에 개념 이해도와 문제 풀이력을 확인합니다. 이를 바탕으로 수업 방향을 정합니다.",
    "무엇을 알고 무엇을 모르는지 파악하는 것이 첫 번째입니다.",
    "레벨 테스트로 현재 위치를 확인하고, 목표까지의 로드맵을 그립니다.",
    "학생의 학습 습관과 실력을 함께 분석합니다. 효과적인 학습법을 제안합니다.",
    "진도보다 진단이 우선입니다. 학생 상태를 정확히 파악한 후 시작합니다.",
    "처음 만나면 학생의 강점과 약점을 파악합니다. 맞춤 전략을 세웁니다."
]

# FAQ 풀
FAQ_POOL = [
    {"q": "기초가 부족한데 따라갈 수 있을까요?", "a": "학생 수준에 맞춰 시작합니다. 부족한 기초부터 차근차근 채워나갑니다."},
    {"q": "학원이랑 과외 중 뭐가 더 좋아요?", "a": "학생 성향에 따라 다릅니다. 맞춤 지도가 필요하면 과외가 효과적입니다."},
    {"q": "선행 학습도 해주시나요?", "a": "현재 학년 내용이 확실하면 선행을 진행합니다. 기초 없는 선행은 권하지 않습니다."},
    {"q": "수업은 어떤 방식으로 진행되나요?", "a": "개념 설명, 문제 풀이, 오답 분석 순서로 진행됩니다. 학생에 맞게 조정합니다."},
    {"q": "얼마나 해야 성적이 오르나요?", "a": "보통 2-3개월이면 변화가 보입니다. 꾸준히 하면 확실히 오릅니다."},
    {"q": "과외 선생님은 어떤 분인가요?", "a": "검증된 실력의 대학생이나 전문 강사입니다. 학생과의 소통을 중시하는 분들입니다."},
    {"q": "숙제가 많이 나오나요?", "a": "학생 상황에 맞게 적절히 부여합니다. 무리하지 않게 조절합니다."},
    {"q": "온라인 수업도 가능한가요?", "a": "가능합니다. 대면과 비슷한 효과를 냅니다."},
    {"q": "수업 시간은 어떻게 되나요?", "a": "보통 2시간입니다. 학생 집중력에 따라 조정 가능합니다."},
    {"q": "방학 때 수업은 어떻게 하나요?", "a": "방학에는 부족한 부분 보충이나 선행에 집중합니다. 횟수 조정도 가능합니다."}
]

# 마무리 풀
CLOSING_POOL = [
    "지금 시작하면 충분히 따라갈 수 있습니다. 함께 해요.",
    "실력은 노력하면 반드시 오릅니다. 시작이 반입니다.",
    "혼자 고민하지 마세요. 도움받으면 달라집니다.",
    "자신감을 되찾을 수 있습니다. 지금 상담받아보세요.",
    "체계적으로 관리해보세요. 결과가 달라집니다.",
    "기초를 탄탄히 쌓으면 다음 단계도 문제없습니다.",
    "스트레스 받지 마세요. 해결책이 있습니다.",
    "꾸준함이 실력의 비결입니다. 함께 시작해요.",
    "성적 향상, 생각보다 어렵지 않습니다.",
    "지금 시작하면 됩니다. 도와드릴게요."
]


def extract_info_from_file(filepath):
    """파일에서 지역 및 학교 정보 추출 (개선된 버전)"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # regions에서 구 이름 추출 (두 번째 항목이 구)
    regions_match = re.search(r'regions:\s*\n\s*-\s*서울\s*\n\s*-\s*(\S+)', content)
    if regions_match:
        gu = regions_match.group(1)
    else:
        gu = ""

    # regions에서 동 이름 추출 (세 번째 항목)
    dong_match = re.search(r'regions:\s*\n\s*-\s*서울\s*\n\s*-\s*\S+\s*\n\s*-\s*(\S+)', content)
    if dong_match:
        dong = dong_match.group(1)
    else:
        # title에서 추출 시도
        title_dong_match = re.search(r'title:\s*["\']?(\S+구)\s+(\S+)\s+(중등|고등)', content)
        if title_dong_match:
            dong = title_dong_match.group(2)
        else:
            dong = ""

    # 학교 이름 추출 (title에서 | 뒤의 내용)
    school_match = re.search(r'title:\s*["\'][^|]+\|\s*([^"\']+)', content)
    if school_match:
        schools = school_match.group(1).strip()
    else:
        schools = ""

    # 과목 판별
    if 'middle-math' in filepath or '수학과외' in content:
        subject = 'math'
    elif 'middle-english' in filepath or '영어과외' in content:
        subject = 'english'
    elif 'high-math' in filepath:
        subject = 'high-math'
    elif 'high-english' in filepath:
        subject = 'high-english'
    else:
        subject = 'unknown'

    # 학교급 판별
    if 'middle' in filepath or '중등' in content:
        level = 'middle'
    elif 'high' in filepath or '고등' in content:
        level = 'high'
    else:
        level = 'unknown'

    return {
        "gu": gu,
        "dong": dong,
        "schools": schools,
        "subject": subject,
        "level": level,
        "original_content": content
    }


def generate_middle_math_content(info, pool_index, yaml_part):
    """중등 수학 콘텐츠 생성"""
    gu = info["gu"]
    dong = info["dong"]
    schools = info["schools"]

    idx = pool_index % 30
    idx2 = (pool_index + 3) % 10

    intro = MATH_INTRO_POOL[idx]
    box1 = IVORY_BOX_POOL[idx2]
    box2 = IVORY_BOX_POOL[(idx2 + 2) % 10]
    box3 = IVORY_BOX_POOL[(idx2 + 4) % 10]
    box4 = IVORY_BOX_POOL[(idx2 + 6) % 10]
    box5 = IVORY_BOX_POOL[(idx2 + 8) % 10]
    box6 = IVORY_BOX_POOL[(idx2 + 1) % 10]

    faq_indices = [(idx + i*2) % len(FAQ_POOL) for i in range(5)]
    selected_faqs = [FAQ_POOL[i] for i in faq_indices]

    closing = CLOSING_POOL[idx % 10]

    school_intro = f"{schools} 학생들이 내신 경쟁을 하며 공부하고 있습니다." if schools else ""

    content = f"""{yaml_part}

## {gu} {dong} 중학생, 수학이 어렵다면

{intro}

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{box1}
</div>

## 중학교 수학이 어려운 이유

중학교 수학은 초등학교와 달리 추상적인 개념이 많아집니다. 문자와 식, 함수, 방정식 등 눈에 보이지 않는 것들을 다루기 시작합니다. 이 단계에서 개념을 확실히 잡지 않으면 점점 어려워집니다.

계산만 잘한다고 되는 게 아닙니다. 왜 그렇게 되는지, 어떻게 적용하는지 이해해야 합니다. 이해 없이 공식만 외우면 응용 문제에서 막힙니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{box2}
</div>

## {dong} 지역 학교 수학 특징

{gu}의 중학교들은 내신 경쟁이 치열합니다. 기본 문제부터 심화 문제까지 다양하게 출제되며, 서술형 비중도 높습니다.

{school_intro} 학교별 출제 경향을 파악하고 대비하는 것이 중요합니다. 기출문제 분석을 통해 어떤 유형이 자주 나오는지 확인합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{box3}
</div>

## 1:1 과외가 필요한 이유

학원에서는 여러 학생을 함께 가르치기 때문에 개인별 맞춤 지도가 어렵습니다. 모르는 부분이 있어도 질문하기 어렵고, 진도에 맞춰 넘어가야 합니다.

1:1 과외는 학생 수준에 맞춰 수업합니다. 모르는 부분은 확실히 짚고 넘어갑니다. 약한 부분은 더 시간을 들이고, 잘하는 부분은 빠르게 넘어갑니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{box4}
</div>

## 학년별 수학 학습 전략

### 중1 수학

중1은 수학적 사고의 기초를 닦는 시기입니다. 정수, 유리수 계산부터 문자와 식, 일차방정식까지 배웁니다. 이 단계에서 기초가 흔들리면 중2, 중3에서 어려워집니다.

### 중2 수학

중2는 난이도가 확 올라가는 시기입니다. 연립방정식, 일차함수, 확률 등 중요한 단원이 많습니다. 특히 일차함수는 고등학교 수학의 기초가 되므로 확실히 잡아야 합니다.

### 중3 수학

중3은 고등학교를 준비하는 시기입니다. 이차방정식, 이차함수, 삼각비, 원의 성질 등을 배웁니다. 고등학교 수학과 직접 연결되는 내용이 많아 확실히 이해하고 넘어가야 합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{box5}
</div>

## 수업료 안내

**중학생**은 주1회 22만원 - 32만원, 주2회 29만원 - 47만원 선입니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{box6}
</div>

{{{{< cta-dual type="final" >}}}}

## 자주 묻는 질문

"""

    for faq in selected_faqs:
        content += f"""**Q. {faq['q']}**

{faq['a']}

"""

    content += f"""## 마무리

{gu} {dong} 중학생 여러분, {closing}
"""

    return content


def generate_middle_english_content(info, pool_index, yaml_part):
    """중등 영어 콘텐츠 생성"""
    gu = info["gu"]
    dong = info["dong"]
    schools = info["schools"]

    idx = (pool_index + 5) % 30
    idx2 = (pool_index + 1) % 10

    intro = ENG_INTRO_POOL[idx]
    box1 = IVORY_BOX_POOL[idx2]
    box2 = IVORY_BOX_POOL[(idx2 + 3) % 10]
    box3 = IVORY_BOX_POOL[(idx2 + 5) % 10]
    box4 = IVORY_BOX_POOL[(idx2 + 7) % 10]
    box5 = IVORY_BOX_POOL[(idx2 + 9) % 10]
    box6 = IVORY_BOX_POOL[(idx2 + 2) % 10]

    faq_indices = [(idx + i*2) % len(FAQ_POOL) for i in range(5)]
    selected_faqs = [FAQ_POOL[i] for i in faq_indices]

    closing = CLOSING_POOL[idx % 10]

    school_intro = f"{schools} 학생들이 내신 경쟁을 하며 공부하고 있습니다." if schools else ""

    content = f"""{yaml_part}

## {gu} {dong} 중학생, 영어가 어렵다면

{intro}

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{box1}
</div>

## 중학교 영어가 어려운 이유

중학교 영어는 초등학교와 달리 본격적인 문법이 시작됩니다. 시제, 조동사, 관계대명사 등 복잡한 문법이 등장합니다. 문법 없이는 독해가 안 되고, 영작은 더더욱 어렵습니다.

단어만 알아도 되던 시절이 끝났습니다. 문장 구조를 이해하고, 문법 규칙을 적용해야 합니다. 이 단계에서 문법 기초가 흔들리면 고등학교 영어가 매우 어려워집니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{box2}
</div>

## {dong} 지역 학교 영어 특징

{gu}의 중학교들은 영어 내신 경쟁이 치열합니다. 교과서 본문 암기는 기본이고, 문법 응용 문제와 서술형까지 대비해야 합니다.

{school_intro} 학교별 출제 경향을 파악하고 대비하는 것이 중요합니다. 기출문제 분석을 통해 어떤 유형이 자주 나오는지 확인합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{box3}
</div>

## 1:1 과외가 필요한 이유

학원에서는 여러 학생을 함께 가르치기 때문에 개인별 맞춤 지도가 어렵습니다. 모르는 부분이 있어도 질문하기 어렵고, 진도에 맞춰 넘어가야 합니다.

1:1 과외는 학생 수준에 맞춰 수업합니다. 모르는 문법은 확실히 짚고 넘어갑니다. 약한 부분은 더 시간을 들이고, 잘하는 부분은 빠르게 넘어갑니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{box4}
</div>

## 학년별 영어 학습 전략

### 중1 영어

중1은 영어 문법의 기초를 다지는 시기입니다. be동사, 일반동사, 시제의 기본을 배웁니다. 이 단계에서 문법 개념이 흔들리면 중2, 중3에서 어려워집니다.

### 중2 영어

중2는 문법 난이도가 확 올라가는 시기입니다. 부정사, 동명사, 비교급, 접속사 등 중요한 문법이 많습니다. 독해 지문도 길어지고 복잡해집니다.

### 중3 영어

중3은 고등학교를 준비하는 시기입니다. 관계대명사, 분사, 가정법 등 고급 문법을 배웁니다. 수능 유형의 독해 지문도 접하기 시작합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{box5}
</div>

## 수업료 안내

**중학생**은 주1회 22만원 - 32만원, 주2회 29만원 - 47만원 선입니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{box6}
</div>

{{{{< cta-dual type="final" >}}}}

## 자주 묻는 질문

"""

    for faq in selected_faqs:
        content += f"""**Q. {faq['q']}**

{faq['a']}

"""

    content += f"""## 마무리

{gu} {dong} 중학생 여러분, {closing}
"""

    return content


def generate_high_math_content(info, pool_index, yaml_part):
    """고등 수학 콘텐츠 생성"""
    gu = info["gu"]
    dong = info["dong"]
    schools = info["schools"]

    idx = pool_index % 30
    idx2 = (pool_index + 3) % 10

    intro = HIGH_MATH_INTRO_POOL[idx]
    box1 = IVORY_BOX_POOL[idx2]
    box2 = IVORY_BOX_POOL[(idx2 + 2) % 10]
    box3 = IVORY_BOX_POOL[(idx2 + 4) % 10]
    box4 = IVORY_BOX_POOL[(idx2 + 6) % 10]
    box5 = IVORY_BOX_POOL[(idx2 + 8) % 10]
    box6 = IVORY_BOX_POOL[(idx2 + 1) % 10]

    faq_indices = [(idx + i*2) % len(FAQ_POOL) for i in range(5)]
    selected_faqs = [FAQ_POOL[i] for i in faq_indices]

    closing = CLOSING_POOL[idx % 10]

    school_intro = f"{schools} 학생들의 내신 경쟁이 치열합니다." if schools else ""

    content = f"""{yaml_part}

## {gu} {dong} 고등학생, 수학 성적 올리고 싶다면

{intro}

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{box1}
</div>

## 고등학교 수학이 어려운 이유

고등학교 수학은 중학교와 차원이 다릅니다. 추상적인 개념, 복잡한 계산, 논리적 사고력이 모두 필요합니다. 중학교 때 기초가 흔들렸다면 고등학교에서 더 어려움을 겪습니다.

특히 수능 수학은 사고력과 응용력이 핵심입니다. 킬러 문항이라 불리는 고난도 문제들은 여러 개념을 복합적으로 적용해야 풀립니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{box2}
</div>

## {dong} 지역 학교 수학 특징

{gu}의 고등학교들은 내신 경쟁이 치열합니다. {school_intro}

학교별 출제 경향을 파악하고 대비하는 것이 중요합니다. 기출문제 분석을 통해 어떤 유형이 자주 나오는지 확인합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{box3}
</div>

## 1:1 과외가 필요한 이유

학원에서는 정해진 진도로 수업합니다. 모르는 부분이 있어도 질문하기 어렵고, 이미 아는 내용도 다시 들어야 합니다.

1:1 과외는 학생 수준에 맞춰 수업합니다. 취약한 부분에 집중하고, 강한 부분은 빠르게 넘어갑니다. 시간 효율이 높습니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{box4}
</div>

## 학년별 수학 학습 전략

### 고1 수학

고1은 고등 수학의 기초를 다지는 시기입니다. 수학(상), 수학(하)를 배우며 다항식, 방정식, 함수의 기본 개념을 익힙니다.

### 고2 수학

고2는 선택과목을 시작하는 시기입니다. 수학I, 수학II, 확률과 통계 등 자신의 진로에 맞는 과목을 선택해야 합니다.

### 고3 수학

고3은 수능 대비에 집중하는 시기입니다. 기출 분석, 모의고사 연습, 취약 유형 보완이 핵심입니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{box5}
</div>

## 수업료 안내

**고1-2**는 주1회 25만원 - 36만원, 주2회 33만원 - 53만원 선입니다.

**고3**은 주1회 28만원 - 40만원, 주2회 37만원 - 59만원이 일반적입니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{box6}
</div>

{{{{< cta-dual type="final" >}}}}

## 자주 묻는 질문

"""

    for faq in selected_faqs:
        content += f"""**Q. {faq['q']}**

{faq['a']}

"""

    content += f"""## 마무리

{gu} {dong} 고등학생 여러분, {closing}
"""

    return content


def generate_high_english_content(info, pool_index, yaml_part):
    """고등 영어 콘텐츠 생성"""
    gu = info["gu"]
    dong = info["dong"]
    schools = info["schools"]

    idx = (pool_index + 5) % 30
    idx2 = (pool_index + 1) % 10

    intro = HIGH_ENG_INTRO_POOL[idx]
    box1 = IVORY_BOX_POOL[idx2]
    box2 = IVORY_BOX_POOL[(idx2 + 3) % 10]
    box3 = IVORY_BOX_POOL[(idx2 + 5) % 10]
    box4 = IVORY_BOX_POOL[(idx2 + 7) % 10]
    box5 = IVORY_BOX_POOL[(idx2 + 9) % 10]
    box6 = IVORY_BOX_POOL[(idx2 + 2) % 10]

    faq_indices = [(idx + i*2) % len(FAQ_POOL) for i in range(5)]
    selected_faqs = [FAQ_POOL[i] for i in faq_indices]

    closing = CLOSING_POOL[idx % 10]

    school_intro = f"{schools} 학생들의 내신 경쟁이 치열합니다." if schools else ""

    content = f"""{yaml_part}

## {gu} {dong} 고등학생, 영어 성적 올리고 싶다면

{intro}

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{box1}
</div>

## 고등학교 영어가 어려운 이유

고등학교 영어는 중학교와 차원이 다릅니다. 독해 지문이 길어지고, 어휘 수준이 높아집니다. 빈칸 추론, 문장 삽입, 순서 배열 등 고난도 유형이 등장합니다.

수능 영어는 절대평가지만, 90점 이상을 받아야 1등급입니다. 독해력이 부족하면 70점대에 머물 수 있습니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{box2}
</div>

## {dong} 지역 학교 영어 특징

{gu}의 고등학교들은 영어 내신 경쟁이 치열합니다. {school_intro}

교과서 본문 이해는 기본이고, 변형 문제와 외부 지문까지 대비해야 합니다. 학교별 출제 경향을 파악하는 것이 중요합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{box3}
</div>

## 1:1 과외가 필요한 이유

학원에서는 정해진 진도로 수업합니다. 개인별 약점을 집중 보완하기 어렵습니다.

1:1 과외는 학생 수준에 맞춰 수업합니다. 문법이 약하면 문법에, 독해가 약하면 독해에 집중합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{box4}
</div>

## 학년별 영어 학습 전략

### 고1 영어

고1은 고등 영어의 기초를 다지는 시기입니다. 중학교 문법을 정리하고, 고등 수준의 독해에 적응해야 합니다.

### 고2 영어

고2는 수능 유형에 익숙해지는 시기입니다. 내신 대비와 함께 수능 기출을 풀어보며 유형별 접근법을 익힙니다.

### 고3 영어

고3은 실전 감각을 완성하는 시기입니다. 모의고사를 꾸준히 풀며 시간 배분을 연습합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{box5}
</div>

## 수업료 안내

**고1-2**는 주1회 25만원 - 36만원, 주2회 33만원 - 53만원 선입니다.

**고3**은 주1회 28만원 - 40만원, 주2회 37만원 - 59만원이 일반적입니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{box6}
</div>

{{{{< cta-dual type="final" >}}}}

## 자주 묻는 질문

"""

    for faq in selected_faqs:
        content += f"""**Q. {faq['q']}**

{faq['a']}

"""

    content += f"""## 마무리

{gu} {dong} 고등학생 여러분, {closing}
"""

    return content


def rewrite_failed_files():
    """실패한 파일들 리라이팅"""
    base_path = "/home/user/edu-guide/content/seoul"

    # 실패한 구 목록
    failed_gus = ["eunpyeong", "jungnang", "yongsan"]

    files = []
    for gu in failed_gus:
        gu_path = os.path.join(base_path, gu)
        if os.path.exists(gu_path):
            files.extend(glob.glob(f"{gu_path}/*-middle-math.md"))
            files.extend(glob.glob(f"{gu_path}/*-middle-english.md"))
            files.extend(glob.glob(f"{gu_path}/*-high-math.md"))
            files.extend(glob.glob(f"{gu_path}/*-high-english.md"))

    print(f"총 {len(files)}개 파일 발견")

    success_count = 0
    fail_count = 0

    for i, filepath in enumerate(files):
        try:
            info = extract_info_from_file(filepath)

            if not info["gu"]:
                print(f"건너뜀 (구 정보 추출 실패): {filepath}")
                fail_count += 1
                continue

            # YAML 추출
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            yaml_match = re.match(r'(---\n.*?\n---)\n', content, re.DOTALL)
            if not yaml_match:
                print(f"건너뜀 (YAML 추출 실패): {filepath}")
                fail_count += 1
                continue

            yaml_part = yaml_match.group(1)

            # 파일 유형에 따라 콘텐츠 생성
            if 'middle-math' in filepath:
                new_content = generate_middle_math_content(info, i, yaml_part)
            elif 'middle-english' in filepath:
                new_content = generate_middle_english_content(info, i, yaml_part)
            elif 'high-math' in filepath:
                new_content = generate_high_math_content(info, i, yaml_part)
            elif 'high-english' in filepath:
                new_content = generate_high_english_content(info, i, yaml_part)
            else:
                print(f"건너뜀 (알 수 없는 유형): {filepath}")
                fail_count += 1
                continue

            if new_content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                success_count += 1
            else:
                fail_count += 1

        except Exception as e:
            print(f"오류: {filepath} - {e}")
            fail_count += 1

    print(f"\n리라이팅 완료!")
    print(f"성공: {success_count}개, 실패: {fail_count}개")


if __name__ == "__main__":
    rewrite_failed_files()
