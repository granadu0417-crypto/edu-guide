#!/usr/bin/env python3
"""수원시 동단위 콘텐츠 생성 스크립트"""

import os
import random

# 수원시 4개 구별 행정동 및 학교 정보
SUWON_DATA = {
    "jangan": {  # 장안구
        "name_ko": "장안구",
        "dongs": {
            "jowon1": {"name": "조원1동", "schools": ["수원외고", "경기과학고", "삼일공고"]},
            "jowon2": {"name": "조원2동", "schools": ["수원외고", "장안고", "수일여고"]},
            "yeonghwa": {"name": "영화동", "schools": ["영생고", "천천고", "수원공고"]},
            "songjuk": {"name": "송죽동", "schools": ["경기과학고", "수성고", "율전고"]},
            "yeonmu": {"name": "연무동", "schools": ["수성고", "장안고", "삼일공고"]},
            "pajang": {"name": "파장동", "schools": ["장안고", "수일여고", "천천고"]},
            "yuljeon": {"name": "율전동", "schools": ["율전고", "아주대부고", "경기과학고"]},
            "jeongja1": {"name": "정자1동", "schools": ["정자고", "수원외고", "장안고"]},
            "jeongja2": {"name": "정자2동", "schools": ["정자고", "천천고", "수성고"]},
            "jeongja3": {"name": "정자3동", "schools": ["정자고", "율전고", "장안고"]},
            "cheoncheon": {"name": "천천동", "schools": ["천천고", "수성고", "영생고"]},
        }
    },
    "gwonseon": {  # 권선구
        "name_ko": "권선구",
        "dongs": {
            "pyeong": {"name": "평동", "schools": ["고색고", "권선고", "곡선고"]},
            "guun": {"name": "구운동", "schools": ["곡선고", "권선고", "수원공고"]},
            "seodun": {"name": "서둔동", "schools": ["농생명고", "권선고", "고색고"]},
            "ibuk": {"name": "입북동", "schools": ["권선고", "칠보고", "고색고"]},
            "gosaek": {"name": "고색동", "schools": ["고색고", "권선고", "수원공고"]},
            "gwonseon1": {"name": "권선1동", "schools": ["권선고", "곡선고", "세류고"]},
            "gwonseon2": {"name": "권선2동", "schools": ["권선고", "세류고", "칠보고"]},
            "homaesil": {"name": "호매실동", "schools": ["칠보고", "호매실고", "권선고"]},
            "geumgok": {"name": "금곡동", "schools": ["금곡고", "호매실고", "칠보고"]},
            "chilbo": {"name": "칠보동", "schools": ["칠보고", "금곡고", "권선고"]},
            "seryu1": {"name": "세류1동", "schools": ["세류고", "권선고", "수원공고"]},
            "seryu2": {"name": "세류2동", "schools": ["세류고", "곡선고", "권선고"]},
            "seryu3": {"name": "세류3동", "schools": ["세류고", "고색고", "권선고"]},
        }
    },
    "paldal": {  # 팔달구
        "name_ko": "팔달구",
        "dongs": {
            "paldal": {"name": "팔달동", "schools": ["수원고", "삼일상고", "매향여고"]},
            "namhyang": {"name": "남향동", "schools": ["수원고", "유신고", "매향여고"]},
            "sinan": {"name": "신안동", "schools": ["수원고", "동우여고", "삼일상고"]},
            "maegyo": {"name": "매교동", "schools": ["수원고", "매향여고", "유신고"]},
            "maesan": {"name": "매산동", "schools": ["수원고", "삼일상고", "동우여고"]},
            "godeung": {"name": "고등동", "schools": ["유신고", "수원고", "매향여고"]},
            "hwaseo1": {"name": "화서1동", "schools": ["수원고", "화홍고", "동우여고"]},
            "hwaseo2": {"name": "화서2동", "schools": ["화홍고", "수원고", "유신고"]},
            "jidong": {"name": "지동", "schools": ["유신고", "수원고", "매향여고"]},
            "uman1": {"name": "우만1동", "schools": ["유신고", "창현고", "수원고"]},
            "uman2": {"name": "우만2동", "schools": ["창현고", "유신고", "동우여고"]},
            "ingye": {"name": "인계동", "schools": ["유신고", "창현고", "동우여고"]},
        }
    },
    "yeongtong": {  # 영통구
        "name_ko": "영통구",
        "dongs": {
            "yeongtong1": {"name": "영통1동", "schools": ["영통고", "효원고", "청명고"]},
            "yeongtong2": {"name": "영통2동", "schools": ["영통고", "수원칠보고", "효원고"]},
            "yeongtong3": {"name": "영통3동", "schools": ["청명고", "영통고", "효원고"]},
            "maetan1": {"name": "매탄1동", "schools": ["매탄고", "영복여고", "효원고"]},
            "maetan2": {"name": "매탄2동", "schools": ["매탄고", "영복여고", "청명고"]},
            "maetan3": {"name": "매탄3동", "schools": ["매탄고", "효원고", "영통고"]},
            "maetan4": {"name": "매탄4동", "schools": ["매탄고", "영복여고", "청명고"]},
            "woncheon": {"name": "원천동", "schools": ["아주대부고", "효원고", "영통고"]},
            "uui": {"name": "이의동", "schools": ["광교고", "아주대부고", "효원고"]},
            "gwanggyo1": {"name": "광교1동", "schools": ["광교고", "아주대부고", "영통고"]},
            "gwanggyo2": {"name": "광교2동", "schools": ["광교고", "효원고", "청명고"]},
            "mangpo1": {"name": "망포1동", "schools": ["망포고", "영통고", "효원고"]},
            "mangpo2": {"name": "망포2동", "schools": ["망포고", "청명고", "영통고"]},
            "taejang": {"name": "태장동", "schools": ["태장고", "영통고", "효원고"]},
        }
    }
}

# 표현 풀 - 서두
INTRO_POOL_HIGH_MATH = [
    "고등학교 수학, 중학교 때와 완전히 다릅니다.",
    "수학 성적이 갑자기 떨어졌다면 이유가 있습니다.",
    "고등학교에 올라오면 수학이 어려워지는 건 당연합니다.",
    "수포자가 되기 전에, 지금 잡아야 합니다.",
    "내신과 수능, 둘 다 잡는 방법이 있습니다.",
    "수학은 한 번 놓치면 따라잡기 어렵습니다.",
    "개념이 흔들리면 문제가 안 풀립니다.",
    "수학 때문에 대학을 포기하지 마세요.",
    "1등급과 3등급의 차이는 생각보다 작습니다.",
    "수학, 제대로 배우면 어렵지 않습니다.",
    "고등 수학의 벽, 넘을 수 있습니다.",
    "혼자 공부하는 수학은 한계가 있습니다.",
    "지금 시작하면 아직 늦지 않았습니다.",
    "수학 실력, 3개월이면 달라집니다.",
    "개념부터 다시 잡으면 성적이 오릅니다.",
    "수학을 잘하는 학생들의 비결이 있습니다.",
    "문제 풀이 시간이 부족하다면 방법이 있습니다.",
    "킬러 문항도 풀 수 있습니다.",
    "등급을 올리고 싶다면 지금 시작하세요.",
    "수학, 어디서부터 시작해야 할지 모르겠다면",
    "기초부터 심화까지, 체계적으로 잡아드립니다.",
    "내신 1등급, 불가능하지 않습니다.",
    "수능 수학 1등급의 비결을 알려드립니다.",
    "수학은 노력만으로 되지 않습니다. 방법이 필요합니다.",
    "같은 시간을 공부해도 성적 차이가 나는 이유.",
    "수학 과외, 제대로 받으면 달라집니다.",
    "고등학교 수학, 막막하다면 함께 시작해요.",
    "성적이 안 오르는 데는 이유가 있습니다.",
    "수학 공부법을 바꾸면 결과가 바뀝니다.",
    "이제 혼자 고민하지 마세요.",
]

INTRO_POOL_HIGH_ENG = [
    "고등학교 영어, 중학교와 차원이 다릅니다.",
    "영어 성적이 오르지 않아 고민이신가요?",
    "수능 영어 1등급, 생각보다 어렵지 않습니다.",
    "영어는 꾸준함이 답입니다.",
    "내신과 수능, 둘 다 잡는 전략이 있습니다.",
    "영어 때문에 대학 못 가면 억울합니다.",
    "독해 속도가 느리다면 방법이 있습니다.",
    "문법이 약하면 독해도 어렵습니다.",
    "영어, 제대로 배우면 오릅니다.",
    "1등급 학생들의 공부법은 다릅니다.",
    "영어 성적, 3개월이면 달라질 수 있습니다.",
    "지금 시작하면 충분히 따라잡을 수 있습니다.",
    "수능 영어, 절대평가라고 쉬운 게 아닙니다.",
    "영어는 혼자 하면 늘지 않습니다.",
    "내신 영어와 수능 영어, 둘 다 잡아야 합니다.",
    "영어 공부, 방향이 중요합니다.",
    "단어만 외운다고 성적이 오르지 않습니다.",
    "구문 분석 능력이 핵심입니다.",
    "영어 지문이 길어지면 시간이 부족해집니다.",
    "등급을 올리고 싶다면 전략이 필요합니다.",
    "영어, 어디서부터 시작해야 할지 모르겠다면",
    "기초부터 심화까지 체계적으로 잡아드립니다.",
    "내신 1등급, 방법만 알면 됩니다.",
    "같은 시간 공부해도 결과가 다른 이유.",
    "영어 과외, 제대로 받으면 달라집니다.",
    "고등학교 영어, 막막하다면 함께해요.",
    "성적이 정체되어 있다면 방법을 바꿔야 합니다.",
    "영어 실력, 확실히 올려드립니다.",
    "이제 혼자 고민하지 마세요.",
    "영어, 포기하기엔 너무 중요한 과목입니다.",
]

INTRO_POOL_MID_MATH = [
    "중학교 수학, 초등학교와 완전히 다릅니다.",
    "수학이 갑자기 어려워졌다면 이유가 있습니다.",
    "지금 기초를 잡아야 고등학교가 편합니다.",
    "수포자가 되기 전에 잡아야 합니다.",
    "중학교 수학은 고등학교의 기초입니다.",
    "수학은 한 번 놓치면 따라잡기 어렵습니다.",
    "개념이 흔들리면 문제가 안 풀립니다.",
    "내신 성적, 지금 잡아야 합니다.",
    "중학교 수학, 제대로 배우면 어렵지 않습니다.",
    "혼자 공부하는 수학은 한계가 있습니다.",
    "지금 시작하면 아직 늦지 않았습니다.",
    "수학 실력, 3개월이면 달라집니다.",
    "개념부터 다시 잡으면 성적이 오릅니다.",
    "문제 풀이가 느리다면 방법이 있습니다.",
    "내신 성적을 올리고 싶다면 지금 시작하세요.",
    "기초부터 심화까지 체계적으로 잡아드립니다.",
    "수학은 노력만으로 되지 않습니다.",
    "같은 시간을 공부해도 차이가 나는 이유.",
    "수학 과외, 제대로 받으면 달라집니다.",
    "중학교 수학, 막막하다면 함께 시작해요.",
    "성적이 안 오르는 데는 이유가 있습니다.",
    "수학 공부법을 바꾸면 결과가 바뀝니다.",
    "이제 혼자 고민하지 마세요.",
    "수학, 어디서부터 시작해야 할지 모르겠다면",
    "고등학교 선행, 지금 시작해야 합니다.",
    "내신 1등급, 방법만 알면 됩니다.",
    "수학의 기초를 확실히 잡아드립니다.",
    "중학교 때 기초가 부실하면 고등학교에서 고생합니다.",
    "지금이 가장 중요한 시기입니다.",
    "수학, 포기하기엔 너무 중요한 과목입니다.",
]

INTRO_POOL_MID_ENG = [
    "중학교 영어, 초등학교와 차원이 다릅니다.",
    "영어 성적이 오르지 않아 고민이신가요?",
    "지금 기초를 잡아야 고등학교가 편합니다.",
    "영어는 꾸준함이 답입니다.",
    "내신 성적, 지금 잡아야 합니다.",
    "영어 때문에 성적이 떨어지면 억울합니다.",
    "문법이 약하면 독해도 어렵습니다.",
    "영어, 제대로 배우면 오릅니다.",
    "영어 성적, 3개월이면 달라질 수 있습니다.",
    "지금 시작하면 충분히 따라잡을 수 있습니다.",
    "영어는 혼자 하면 늘지 않습니다.",
    "영어 공부, 방향이 중요합니다.",
    "단어만 외운다고 성적이 오르지 않습니다.",
    "기초 문법이 핵심입니다.",
    "등급을 올리고 싶다면 전략이 필요합니다.",
    "영어, 어디서부터 시작해야 할지 모르겠다면",
    "기초부터 심화까지 체계적으로 잡아드립니다.",
    "내신 1등급, 방법만 알면 됩니다.",
    "같은 시간 공부해도 결과가 다른 이유.",
    "영어 과외, 제대로 받으면 달라집니다.",
    "중학교 영어, 막막하다면 함께해요.",
    "성적이 정체되어 있다면 방법을 바꿔야 합니다.",
    "영어 실력, 확실히 올려드립니다.",
    "이제 혼자 고민하지 마세요.",
    "영어, 포기하기엔 너무 중요한 과목입니다.",
    "고등학교 선행, 지금 준비해야 합니다.",
    "독해력은 문법에서 시작됩니다.",
    "중학교 때 영어 기초를 확실히 잡아야 합니다.",
    "영어 실력의 기반을 만들어 드립니다.",
    "지금이 영어 실력을 키울 최적의 시기입니다.",
]

# 아이보리 박스 표현 풀
BOX_POOL = [
    "첫 수업에서 학생의 실력을 정확하게 진단합니다. 개념 이해도, 문제 풀이력, 시간 관리 능력을 파악합니다.",
    "수업 시작 전, 학생이 어디서 막히는지 정확히 파악합니다. 무작정 진도를 나가지 않습니다.",
    "먼저 학생의 현재 실력을 꼼꼼히 체크합니다. 어떤 개념이 부족한지 진단합니다.",
    "진도보다 진단이 먼저입니다. 학생이 무엇을 알고 무엇을 모르는지 정확히 파악한 후 수업을 시작합니다.",
    "학생마다 부족한 부분이 다릅니다. 정확한 진단 후 맞춤 지도를 시작합니다.",
    "처음 만나면 학생의 강점과 약점을 파악합니다. 맞춤 전략을 세웁니다.",
    "어디서 막히는지 먼저 알아야 합니다. 진단 후 학생에게 맞는 수업을 설계합니다.",
    "레벨 테스트로 현재 위치를 확인하고, 목표까지의 로드맵을 그립니다.",
    "실력은 숫자로만 평가할 수 없습니다. 개념 이해도, 문제 접근법, 시간 관리까지 종합 진단합니다.",
    "기초가 부족한지, 응용이 약한지, 시간 관리가 문제인지 정확히 진단합니다.",
    "문제를 풀기 전에 그림을 그려봅니다. 시각화하면 이해가 쉬워집니다.",
    "개념을 완벽히 이해한 후, 다양한 유형의 문제를 훈련합니다.",
    "학교별로 시험 난이도와 유형이 다릅니다. 맞춤 대비를 해드립니다.",
    "학교 시험 범위에 맞춰 집중 대비합니다. 범위 외 내용으로 시간 낭비하지 않습니다.",
    "내신과 수능의 차이를 명확히 알려드립니다. 두 가지를 효율적으로 병행할 수 있습니다.",
    "내신 공부가 수능에 도움이 되도록 합니다. 두 번 공부하는 비효율을 없앱니다.",
    "비슷한 유형을 반복해서 풀며 패턴을 익힙니다. 새로운 문제도 익숙한 유형으로 변환할 수 있습니다.",
    "오답노트를 활용합니다. 같은 실수를 반복하지 않도록 합니다.",
    "풀이 과정을 꼼꼼히 점검합니다. 어디서 실수했는지 정확히 파악합니다.",
    "시간을 재고 문제를 풉니다. 실전 감각을 기릅니다.",
    "기출문제를 분석합니다. 출제 경향을 파악하면 대비가 쉬워집니다.",
    "학년별로 중점이 다릅니다. 학년에 맞는 최적의 전략을 세웁니다.",
    "기초가 부실하면 나중에 고생합니다. 지금 확실히 잡아야 합니다.",
    "첫 상담에서 학생의 현재 상황과 목표를 파악합니다. 최적의 수업 계획을 안내드립니다.",
    "정기적으로 학습 상황을 점검합니다. 필요시 수업 방식을 조정합니다.",
    "학부모님과 정기적으로 소통합니다. 학생의 학습 상황을 공유합니다.",
    "단순 암기가 아닌 이해 중심으로 수업합니다. 오래 기억에 남습니다.",
    "개념 설명 후 바로 문제에 적용합니다. 이론과 실전을 연결합니다.",
    "어려운 개념은 쉬운 예시로 설명합니다. 이해가 빠릅니다.",
    "질문을 많이 하도록 유도합니다. 질문해야 배웁니다.",
]

# 마무리 표현 풀
ENDING_POOL = [
    "지금 시작하세요. 늦었다고 생각할 때가 가장 빠른 때입니다.",
    "시작이 반입니다. 오늘 연락 주세요.",
    "더 늦기 전에 시작하세요. 함께하면 달라집니다.",
    "고민만 하지 마세요. 상담은 무료입니다.",
    "지금이 가장 좋은 시작점입니다.",
    "변화는 결심에서 시작됩니다. 지금 연락 주세요.",
    "함께하면 가능합니다. 기다리고 있겠습니다.",
    "포기하지 마세요. 방법이 있습니다.",
    "성적 향상의 시작, 지금입니다.",
    "혼자 고민하지 마세요. 도와드리겠습니다.",
    "결과로 보여드리겠습니다. 연락 주세요.",
    "첫 상담이 시작입니다. 부담 없이 연락 주세요.",
    "학생의 가능성을 믿습니다. 함께 만들어가요.",
    "성적은 바뀔 수 있습니다. 지금 시작하세요.",
    "시간은 기다려주지 않습니다. 오늘 시작하세요.",
    "노력은 배신하지 않습니다. 함께 노력해요.",
    "목표를 향해 함께 가겠습니다.",
    "변화의 시작을 응원합니다.",
    "가능성은 누구에게나 있습니다.",
    "시작만 하면 절반은 온 겁니다.",
    "기다리지 마세요. 지금이 적기입니다.",
    "상담 한 번으로 방향이 잡힙니다.",
    "작은 시작이 큰 변화를 만듭니다.",
    "함께라면 어렵지 않습니다.",
    "성공의 비결은 시작에 있습니다.",
    "준비된 선생님이 기다리고 있습니다.",
    "학생의 성장을 함께하고 싶습니다.",
    "믿고 맡겨주세요. 결과로 보답하겠습니다.",
    "지금 결정이 미래를 바꿉니다.",
    "연락 주시면 친절히 상담해 드리겠습니다.",
]

# 이미지 풀
IMAGE_POOL = [
    "photo-1503676260728-1c00da094a0b",
    "photo-1522202176988-66273c2fd55f",
    "photo-1523240795612-9a054b0db644",
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
    "photo-1456513080510-7bf3a84b82f8",
    "photo-1457369804613-52c61a468e7d",
    "photo-1546410531-bb4caa6b424d",
    "photo-1553877522-43269d4ea984",
    "photo-1515378791036-0648a3ef77b2",
    "photo-1519389950473-47ba0277781c",
    "photo-1488190211105-8b0e65b80b4e",
    "photo-1434030216411-0b793f4b4173",
    "photo-1455390582262-044cdead277a",
    "photo-1471107340929-a87cd0f5b5f3",
    "photo-1447069387593-a5de0862481e",
    "photo-1476234251651-f353703a034d",
    "photo-1507842217343-583bb7270b66",
    "photo-1497633762265-9d179a990aa6",
]

def get_expression(pool, index):
    """인덱스 기반으로 표현 선택 (순환)"""
    return pool[index % len(pool)]

def create_high_math_content(gu_name, dong_name, dong_name_en, schools, file_index):
    """고등 수학 콘텐츠 생성"""
    school_str = "·".join(schools[:3])
    intro = get_expression(INTRO_POOL_HIGH_MATH, file_index)
    boxes = [get_expression(BOX_POOL, file_index + i * 7) for i in range(7)]
    ending = get_expression(ENDING_POOL, file_index)
    image = get_expression(IMAGE_POOL, file_index)

    content = f'''---
aliases:
  - /high/suwon-{dong_name_en}-high-math/
title: "수원시 {gu_name} {dong_name} 고등 수학과외 | {school_str} 내신·수능 대비"
date: 2025-01-15
categories:
  - 고등교육
regions:
  - 경기도
  - 수원시
cities:
  - {gu_name}
description: "수원시 {gu_name} {dong_name} 고등학생 수학과외 전문. {schools[0]} 내신과 수능 동시 대비. 개념부터 킬러문항까지 체계적 1:1 지도."
tags:
  - 수원시
  - {gu_name}
  - {dong_name}
  - 고등수학
  - 수학과외
  - 내신관리
  - 수능대비
  - {schools[0]}
featured_image: "https://images.unsplash.com/{image}?w=1200&h=630&fit=crop"
---
{intro}

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[0]}
</div>

## 고등학교 수학, 왜 어려워질까요?

고등학교 수학은 중학교와 차원이 다릅니다. 추상적인 개념이 많아지고, 함수, 미적분, 확률과 통계 등 새로운 영역이 등장합니다. 중학교 때 수학을 잘했던 학생도 고등학교에서 어려움을 겪는 경우가 많습니다.

{dong_name} 지역 {schools[0]} 학생들은 높은 내신 경쟁과 수능 준비를 동시에 해야 합니다. 학교 시험은 학교별 특성에 맞춰 대비해야 하고, 수능은 전국 단위 경쟁이므로 또 다른 전략이 필요합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[1]}
</div>

## {schools[0]} 내신 시험 분석

{schools[0]}은 내신 시험 난이도가 높습니다. 교과서 기본 문제는 물론, 심화 문제와 변형 문제가 많이 출제됩니다. 단순히 공식을 외워서는 좋은 점수를 받기 어렵고, 개념을 깊이 이해하고 다양한 유형에 적용할 수 있어야 합니다.

시험 시간 대비 문제 양이 많은 편이어서 시간 관리도 중요합니다. 평소 시간을 재고 문제를 푸는 연습을 해야 실전에서 당황하지 않습니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[2]}
</div>

## 수능 수학의 핵심

수능 수학은 내신과 출제 방식이 다릅니다. 킬러 문항이라 불리는 21번, 29번, 30번 문제는 여러 개념을 복합적으로 적용해야 풀 수 있습니다. 시간 압박 속에서 정확하게 문제를 푸는 능력이 필요합니다.

수능에서 1등급을 받으려면 킬러 문항 중 최소 1-2개는 맞혀야 합니다. 이를 위해서는 기본 개념이 완벽해야 하고, 다양한 심화 문제를 풀어본 경험이 있어야 합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[3]}
</div>

## 학원과 과외의 차이

학원에서는 많은 학생을 한꺼번에 가르치다 보니 개인별 약점을 보완하기 어렵습니다. 1:1 과외는 학생의 현재 수준에서 출발하여 약한 부분을 집중적으로 보강합니다.

질문하기 어려운 학생도 1:1 수업에서는 편하게 물어볼 수 있습니다. 이해될 때까지 설명을 듣고, 스스로 문제를 풀어보며 실력을 키울 수 있습니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[4]}
</div>

## 학년별 학습 전략

고1은 수학의 기초를 다시 점검하고, 고등 수학의 핵심인 함수 개념을 확실히 익혀야 합니다. 다항식, 방정식과 부등식, 도형의 방정식 등 수학(상), 수학(하) 내용을 탄탄히 해야 고2, 고3에서 수월합니다.

고2는 수학I, 수학II를 배우며 지수, 로그, 삼각함수, 미분과 적분을 익힙니다. 이 시기에 배우는 내용이 수능 수학의 핵심이므로 확실히 이해하고 넘어가야 합니다.

고3은 본격적인 수능 대비 시기입니다. 기출문제 분석, 모의고사 훈련, 약점 보완을 집중적으로 해야 합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[5]}
</div>

## 수업료 안내

**고1-2**는 주1회 25만원 - 36만원, 주2회 33만원 - 53만원 선입니다.

**고3**은 주1회 28만원 - 40만원, 주2회 37만원 - 59만원이 일반적입니다.

정확한 금액은 상담을 통해 안내드립니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[6]}
</div>

{{{{< cta-dual type="final" >}}}}

## 자주 묻는 질문

**Q. 내신과 수능 중 어떤 것을 먼저 준비해야 하나요?**

고1-2는 내신 위주로 공부하면서 수능 기초를 다지고, 고3은 내신과 수능을 병행합니다. 학생 상황에 따라 비중을 조절합니다.

**Q. 수학 기초가 많이 부족한데 따라갈 수 있을까요?**

중학교 내용부터 다시 점검하고 필요한 부분을 보강합니다. 기초를 확실히 다진 후 고등 내용을 진행합니다.

**Q. 킬러 문항은 어떻게 대비하나요?**

기본 개념을 완벽히 익힌 후, 고난도 문제 유형별 접근법을 체계적으로 훈련합니다.

**Q. 내신 시험 대비는 어떻게 하나요?**

시험 2-3주 전부터 학교 기출문제와 예상 문제 풀이로 집중 대비합니다.

## 마무리

{gu_name} {dong_name} 학생 여러분, {ending}
'''
    return content

def create_high_english_content(gu_name, dong_name, dong_name_en, schools, file_index):
    """고등 영어 콘텐츠 생성"""
    school_str = "·".join(schools[:3])
    intro = get_expression(INTRO_POOL_HIGH_ENG, file_index)
    boxes = [get_expression(BOX_POOL, file_index + i * 5 + 3) for i in range(7)]
    ending = get_expression(ENDING_POOL, file_index + 1)
    image = get_expression(IMAGE_POOL, file_index + 1)

    content = f'''---
aliases:
  - /high/suwon-{dong_name_en}-high-english/
title: "수원시 {gu_name} {dong_name} 고등 영어과외 | {school_str} 내신·수능 대비"
date: 2025-01-15
categories:
  - 고등교육
regions:
  - 경기도
  - 수원시
cities:
  - {gu_name}
description: "수원시 {gu_name} {dong_name} 고등학생 영어과외 전문. {schools[0]} 내신과 수능 동시 대비. 독해부터 문법까지 체계적 1:1 지도."
tags:
  - 수원시
  - {gu_name}
  - {dong_name}
  - 고등영어
  - 영어과외
  - 내신관리
  - 수능대비
  - {schools[0]}
featured_image: "https://images.unsplash.com/{image}?w=1200&h=630&fit=crop"
---
{intro}

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[0]}
</div>

## 고등학교 영어, 왜 어려워질까요?

고등학교 영어는 중학교와 차원이 다릅니다. 지문 길이가 길어지고, 어휘 수준이 높아지며, 복잡한 구문이 등장합니다. 중학교 때 영어를 잘했던 학생도 고등학교에서 어려움을 겪는 경우가 많습니다.

{dong_name} 지역 {schools[0]} 학생들은 높은 내신 경쟁과 수능 준비를 동시에 해야 합니다. 학교 시험은 학교별 특성에 맞춰 대비해야 하고, 수능은 전국 단위 경쟁이므로 또 다른 전략이 필요합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[1]}
</div>

## {schools[0]} 내신 시험 분석

{schools[0]}은 영어 내신 시험 난이도가 높습니다. 교과서 본문 암기는 기본이고, 변형 문제와 외부 지문이 출제되기도 합니다. 문법, 어휘, 독해를 균형 있게 준비해야 합니다.

시험 시간 대비 문제 양이 많은 편이어서 시간 관리도 중요합니다. 평소 시간을 재고 문제를 푸는 연습을 해야 실전에서 당황하지 않습니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[2]}
</div>

## 수능 영어의 핵심

수능 영어는 절대평가이지만 1등급을 받기는 쉽지 않습니다. 빈칸 추론, 순서 배열, 문장 삽입 등 고난도 문제 유형에서 실수하면 등급이 떨어집니다.

독해 속도와 정확성을 동시에 갖춰야 합니다. 이를 위해서는 구문 분석 능력과 충분한 어휘력이 필수입니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[3]}
</div>

## 학원과 과외의 차이

학원에서는 많은 학생을 한꺼번에 가르치다 보니 개인별 약점을 보완하기 어렵습니다. 1:1 과외는 학생의 현재 수준에서 출발하여 약한 부분을 집중적으로 보강합니다.

질문하기 어려운 학생도 1:1 수업에서는 편하게 물어볼 수 있습니다. 이해될 때까지 설명을 듣고, 스스로 문제를 풀어보며 실력을 키울 수 있습니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[4]}
</div>

## 학년별 학습 전략

고1은 영어의 기초를 다시 점검하고, 기본 문법과 구문 분석 능력을 확실히 익혀야 합니다. 어휘력도 꾸준히 쌓아야 합니다.

고2는 독해 실력을 본격적으로 키우는 시기입니다. 다양한 주제의 지문을 읽으며 배경지식을 쌓고, 고난도 문제 유형에 익숙해져야 합니다.

고3은 본격적인 수능 대비 시기입니다. 기출문제 분석, 모의고사 훈련, 약점 보완을 집중적으로 해야 합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[5]}
</div>

## 수업료 안내

**고1-2**는 주1회 25만원 - 36만원, 주2회 33만원 - 53만원 선입니다.

**고3**은 주1회 28만원 - 40만원, 주2회 37만원 - 59만원이 일반적입니다.

정확한 금액은 상담을 통해 안내드립니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[6]}
</div>

{{{{< cta-dual type="final" >}}}}

## 자주 묻는 질문

**Q. 내신과 수능 중 어떤 것을 먼저 준비해야 하나요?**

고1-2는 내신 위주로 공부하면서 수능 기초를 다지고, 고3은 내신과 수능을 병행합니다. 학생 상황에 따라 비중을 조절합니다.

**Q. 영어 기초가 많이 부족한데 따라갈 수 있을까요?**

중학교 문법부터 다시 점검하고 필요한 부분을 보강합니다. 기초를 확실히 다진 후 고등 내용을 진행합니다.

**Q. 단어 암기는 어떻게 해야 하나요?**

문맥 속에서 단어를 익히는 것이 효과적입니다. 단어장과 독해를 병행합니다.

**Q. 내신 시험 대비는 어떻게 하나요?**

시험 2-3주 전부터 학교 기출문제와 예상 문제 풀이로 집중 대비합니다.

## 마무리

{gu_name} {dong_name} 학생 여러분, {ending}
'''
    return content

def create_middle_math_content(gu_name, dong_name, dong_name_en, schools, file_index):
    """중등 수학 콘텐츠 생성"""
    school_str = "·".join([s.replace("고", "중") for s in schools[:3]])
    intro = get_expression(INTRO_POOL_MID_MATH, file_index)
    boxes = [get_expression(BOX_POOL, file_index + i * 4 + 2) for i in range(7)]
    ending = get_expression(ENDING_POOL, file_index + 2)
    image = get_expression(IMAGE_POOL, file_index + 2)

    content = f'''---
aliases:
  - /middle/suwon-{dong_name_en}-middle-math/
title: "수원시 {gu_name} {dong_name} 중등 수학과외 | {school_str} 내신 완벽 대비"
date: 2025-01-15
categories:
  - 중등교육
regions:
  - 경기도
  - 수원시
cities:
  - {gu_name}
description: "수원시 {gu_name} {dong_name} 중학생 수학과외 전문. {school_str.split('·')[0]} 내신 대비와 고등 선행까지. 개념부터 심화까지 체계적 1:1 지도."
tags:
  - 수원시
  - {gu_name}
  - {dong_name}
  - 중등수학
  - 수학과외
  - 내신관리
  - 고등선행
featured_image: "https://images.unsplash.com/{image}?w=1200&h=630&fit=crop"
---
{intro}

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[0]}
</div>

## 중학교 수학, 왜 중요할까요?

중학교 수학은 초등학교와 차원이 다릅니다. 음수, 문자식, 방정식 등 추상적인 개념이 등장합니다. 초등학교 때 수학을 잘했던 학생도 중학교에서 어려움을 겪는 경우가 많습니다.

{dong_name} 지역 중학생들은 내신 경쟁과 고등학교 준비를 동시에 해야 합니다. 중학교 수학이 고등학교의 기초이므로 지금 확실히 잡아야 합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[1]}
</div>

## 내신 시험 완벽 분석

{dong_name} 지역 중학교들은 내신 시험 난이도가 높습니다. 교과서 기본 문제는 물론, 심화 문제와 변형 문제가 많이 출제됩니다. 단순히 공식을 외워서는 좋은 점수를 받기 어렵고, 개념을 깊이 이해하고 다양한 유형에 적용할 수 있어야 합니다.

시험 시간 대비 문제 양이 많은 편이어서 시간 관리도 중요합니다. 평소 시간을 재고 문제를 푸는 연습을 해야 실전에서 당황하지 않습니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[2]}
</div>

## 고등학교 수학의 기초

중학교 수학은 고등학교의 기초입니다. 중학교에서 배우는 방정식, 함수, 도형 개념이 고등학교에서 더 어렵게 확장됩니다. 중학교 때 기초가 부실하면 고등학교에서 큰 어려움을 겪습니다.

중3 때부터는 고등 수학을 미리 맛보는 선행 학습이 필요합니다. 고등학교 수학1의 기초 내용을 미리 접해두면 고등학교에 가서 훨씬 수월합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[3]}
</div>

## 학원과 과외의 차이

학원에서는 많은 학생을 한꺼번에 가르치다 보니 개인별 약점을 보완하기 어렵습니다. 1:1 과외는 학생의 현재 수준에서 출발하여 약한 부분을 집중적으로 보강합니다.

질문하기 어려운 학생도 1:1 수업에서는 편하게 물어볼 수 있습니다. 이해될 때까지 설명을 듣고, 스스로 문제를 풀어보며 실력을 키울 수 있습니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[4]}
</div>

## 학년별 학습 전략

중1은 수학의 기초를 다시 점검하고, 중학 수학의 핵심인 방정식과 함수 개념을 확실히 익혀야 합니다. 정수와 유리수 연산, 일차방정식의 기초를 탄탄히 해야 합니다.

중2는 일차함수, 연립방정식, 도형의 성질을 배우며 수학적 사고력을 키웁니다. 이 시기에 배우는 내용이 고등 수학의 기초입니다.

중3은 이차방정식, 이차함수, 피타고라스 정리 등 중학 수학의 정점을 찍는 시기입니다. 동시에 고등학교 선행도 시작해야 합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[5]}
</div>

## 수업료 안내

**중학생**은 주1회 22만원 - 32만원, 주2회 29만원 - 47만원 선입니다.

정확한 금액은 상담을 통해 안내드립니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[6]}
</div>

{{{{< cta-dual type="final" >}}}}

## 자주 묻는 질문

**Q. 내신과 선행 중 어떤 것을 먼저 해야 하나요?**

학년에 따라 다릅니다. 중1-2는 내신에 집중하고, 중3부터는 내신과 고등 선행을 병행합니다.

**Q. 수학 기초가 많이 부족한데 따라갈 수 있을까요?**

초등 내용부터 다시 점검하고 필요한 부분을 보강합니다. 기초를 확실히 다진 후 진행합니다.

**Q. 고등 선행은 언제부터 시작하나요?**

보통 중3 여름방학부터 시작합니다. 학생 상황에 따라 조절할 수 있습니다.

**Q. 내신 시험 대비는 어떻게 하나요?**

시험 2-3주 전부터 학교 기출문제와 예상 문제 풀이로 집중 대비합니다.

## 마무리

{gu_name} {dong_name} 학생 여러분, {ending}
'''
    return content

def create_middle_english_content(gu_name, dong_name, dong_name_en, schools, file_index):
    """중등 영어 콘텐츠 생성"""
    school_str = "·".join([s.replace("고", "중") for s in schools[:3]])
    intro = get_expression(INTRO_POOL_MID_ENG, file_index)
    boxes = [get_expression(BOX_POOL, file_index + i * 6 + 1) for i in range(7)]
    ending = get_expression(ENDING_POOL, file_index + 3)
    image = get_expression(IMAGE_POOL, file_index + 3)

    content = f'''---
aliases:
  - /middle/suwon-{dong_name_en}-middle-english/
title: "수원시 {gu_name} {dong_name} 중등 영어과외 | {school_str} 내신 완벽 대비"
date: 2025-01-15
categories:
  - 중등교육
regions:
  - 경기도
  - 수원시
cities:
  - {gu_name}
description: "수원시 {gu_name} {dong_name} 중학생 영어과외 전문. {school_str.split('·')[0]} 내신 대비와 고등 선행까지. 문법부터 독해까지 체계적 1:1 지도."
tags:
  - 수원시
  - {gu_name}
  - {dong_name}
  - 중등영어
  - 영어과외
  - 내신관리
  - 고등선행
featured_image: "https://images.unsplash.com/{image}?w=1200&h=630&fit=crop"
---
{intro}

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[0]}
</div>

## 중학교 영어, 왜 중요할까요?

중학교 영어는 초등학교와 차원이 다릅니다. 문법이 본격적으로 등장하고, 독해 지문도 길어집니다. 초등학교 때 영어를 잘했던 학생도 중학교에서 어려움을 겪는 경우가 많습니다.

{dong_name} 지역 중학생들은 내신 경쟁과 고등학교 준비를 동시에 해야 합니다. 중학교 영어가 고등학교의 기초이므로 지금 확실히 잡아야 합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[1]}
</div>

## 내신 시험 완벽 분석

{dong_name} 지역 중학교들은 영어 내신 시험 난이도가 높습니다. 교과서 본문 암기는 기본이고, 문법 문제와 독해 문제가 균형 있게 출제됩니다.

시험 시간 대비 문제 양이 많은 편이어서 시간 관리도 중요합니다. 평소 시간을 재고 문제를 푸는 연습을 해야 실전에서 당황하지 않습니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[2]}
</div>

## 고등학교 영어의 기초

중학교 영어는 고등학교의 기초입니다. 중학교에서 배우는 문법과 독해 능력이 고등학교에서 더 높은 수준으로 요구됩니다. 중학교 때 기초가 부실하면 고등학교에서 큰 어려움을 겪습니다.

중3 때부터는 고등 영어를 미리 맛보는 선행 학습이 필요합니다. 고등학교 수준의 문법과 구문을 미리 접해두면 고등학교에 가서 훨씬 수월합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[3]}
</div>

## 학원과 과외의 차이

학원에서는 많은 학생을 한꺼번에 가르치다 보니 개인별 약점을 보완하기 어렵습니다. 1:1 과외는 학생의 현재 수준에서 출발하여 약한 부분을 집중적으로 보강합니다.

질문하기 어려운 학생도 1:1 수업에서는 편하게 물어볼 수 있습니다. 이해될 때까지 설명을 듣고, 스스로 문제를 풀어보며 실력을 키울 수 있습니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[4]}
</div>

## 학년별 학습 전략

중1은 영어의 기초를 다시 점검하고, 기본 문법을 확실히 익혀야 합니다. 어휘력도 꾸준히 쌓아야 합니다.

중2는 문법 실력을 본격적으로 키우는 시기입니다. 다양한 문장 구조를 익히고, 독해 연습을 시작합니다.

중3은 고등학교 진학을 앞두고 선행 학습을 시작해야 합니다. 고등 수준의 독해와 문법을 미리 접해둡니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[5]}
</div>

## 수업료 안내

**중학생**은 주1회 22만원 - 32만원, 주2회 29만원 - 47만원 선입니다.

정확한 금액은 상담을 통해 안내드립니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[6]}
</div>

{{{{< cta-dual type="final" >}}}}

## 자주 묻는 질문

**Q. 내신과 선행 중 어떤 것을 먼저 해야 하나요?**

학년에 따라 다릅니다. 중1-2는 내신에 집중하고, 중3부터는 내신과 고등 선행을 병행합니다.

**Q. 영어 기초가 많이 부족한데 따라갈 수 있을까요?**

초등 문법부터 다시 점검하고 필요한 부분을 보강합니다. 기초를 확실히 다진 후 진행합니다.

**Q. 고등 선행은 언제부터 시작하나요?**

보통 중3 여름방학부터 시작합니다. 학생 상황에 따라 조절할 수 있습니다.

**Q. 내신 시험 대비는 어떻게 하나요?**

시험 2-3주 전부터 학교 기출문제와 예상 문제 풀이로 집중 대비합니다.

## 마무리

{gu_name} {dong_name} 학생 여러분, {ending}
'''
    return content

def create_index_content(path_type, gu_name=None, dong_name=None, dong_name_en=None):
    """인덱스 파일 생성"""
    if path_type == "city":
        return f'''---
title: "수원시 과외"
date: 2025-01-15
description: "수원시 전 지역 초중고 과외 정보. 장안구, 권선구, 팔달구, 영통구 지역별 맞춤 과외."
---
수원시 전 지역 과외 정보를 안내합니다.
'''
    elif path_type == "gu":
        return f'''---
title: "수원시 {gu_name} 과외"
date: 2025-01-15
description: "수원시 {gu_name} 지역 초중고 과외 정보. 동별 맞춤 과외 안내."
---
수원시 {gu_name} 지역 과외 정보를 안내합니다.
'''
    elif path_type == "dong":
        return f'''---
title: "수원시 {gu_name} {dong_name} 과외"
date: 2025-01-15
description: "수원시 {gu_name} {dong_name} 지역 초중고 과외 정보."
---
{dong_name} 지역 과외 정보를 안내합니다.
'''

def main():
    base_path = "/home/user/edu-guide/content/gyeonggi/suwon"

    # 기존 suwon 폴더 삭제 후 재생성
    if os.path.exists(base_path):
        import shutil
        shutil.rmtree(base_path)

    os.makedirs(base_path, exist_ok=True)

    # 수원시 인덱스
    with open(f"{base_path}/_index.md", "w", encoding="utf-8") as f:
        f.write(create_index_content("city"))

    file_index = 0
    total_files = 0

    for gu_key, gu_data in SUWON_DATA.items():
        gu_name = gu_data["name_ko"]
        gu_path = f"{base_path}/{gu_key}"
        os.makedirs(gu_path, exist_ok=True)

        # 구 인덱스
        with open(f"{gu_path}/_index.md", "w", encoding="utf-8") as f:
            f.write(create_index_content("gu", gu_name=gu_name))

        for dong_key, dong_data in gu_data["dongs"].items():
            dong_name = dong_data["name"]
            schools = dong_data["schools"]
            dong_path = f"{gu_path}/{dong_key}"
            os.makedirs(dong_path, exist_ok=True)

            # 동 인덱스
            with open(f"{dong_path}/_index.md", "w", encoding="utf-8") as f:
                f.write(create_index_content("dong", gu_name=gu_name, dong_name=dong_name, dong_name_en=dong_key))

            # 4개 파일 생성
            with open(f"{dong_path}/high-math.md", "w", encoding="utf-8") as f:
                f.write(create_high_math_content(gu_name, dong_name, dong_key, schools, file_index))

            with open(f"{dong_path}/high-english.md", "w", encoding="utf-8") as f:
                f.write(create_high_english_content(gu_name, dong_name, dong_key, schools, file_index))

            with open(f"{dong_path}/middle-math.md", "w", encoding="utf-8") as f:
                f.write(create_middle_math_content(gu_name, dong_name, dong_key, schools, file_index))

            with open(f"{dong_path}/middle-english.md", "w", encoding="utf-8") as f:
                f.write(create_middle_english_content(gu_name, dong_name, dong_key, schools, file_index))

            file_index += 1
            total_files += 4
            print(f"Created: {gu_name} {dong_name} (4 files)")

    print(f"\n총 {total_files}개 파일 생성 완료!")

if __name__ == "__main__":
    main()
