#!/usr/bin/env python3
"""
경기도 전체 콘텐츠 재생성 스크립트
- 표현 풀 시스템 활용
- 중복률 10% 이하 목표
- 20개 도시 동단위 콘텐츠 생성
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from expression_pools import (
    INTRO_HIGH_MATH, INTRO_HIGH_ENG, INTRO_MID_MATH, INTRO_MID_ENG,
    H2_HIGH_MATH_WHY, H2_HIGH_MATH_EXAM, H2_HIGH_MATH_SUNEUNG,
    H2_HIGH_MATH_COMPARE, H2_HIGH_MATH_GRADE,
    H2_HIGH_ENG_WHY, H2_MID_MATH_WHY, H2_MID_ENG_WHY,
    IVORY_BOX_POOL, ENDING_POOL, IMAGE_POOL,
    BODY_HIGH_MATH_WHY, BODY_COMPARE, BODY_GRADE_STRATEGY,
    FAQ_Q1_VARIANTS, FAQ_A1_VARIANTS,
    FAQ_Q2_VARIANTS, FAQ_A2_VARIANTS,
    FAQ_Q3_VARIANTS, FAQ_A3_VARIANTS,
    FAQ_Q4_VARIANTS, FAQ_A4_VARIANTS,
    get_pool_item
)

# ============================================================
# 경기도 전체 도시 데이터
# ============================================================

GYEONGGI_DATA = {
    "suwon": {
        "name_ko": "수원시",
        "gus": {
            "jangan": {
                "name_ko": "장안구",
                "dongs": {
                    "jowon1": {"name": "조원1동", "schools_high": ["수원외고", "장안고", "수성고"], "schools_mid": ["조원중", "장안중", "천천중"]},
                    "jowon2": {"name": "조원2동", "schools_high": ["장안고", "수일여고", "천천고"], "schools_mid": ["수일여중", "장안중", "송원중"]},
                    "yeonghwa": {"name": "영화동", "schools_high": ["영생고", "천천고", "수원공고"], "schools_mid": ["영화중", "천천중", "수성중"]},
                    "songjuk": {"name": "송죽동", "schools_high": ["경기과학고", "수성고", "율전고"], "schools_mid": ["송죽중", "수성중", "율전중"]},
                    "jeongja1": {"name": "정자1동", "schools_high": ["정자고", "수원외고", "장안고"], "schools_mid": ["정자중", "장안중", "천천중"]},
                    "jeongja2": {"name": "정자2동", "schools_high": ["정자고", "천천고", "수성고"], "schools_mid": ["정자중", "천천중", "수성중"]},
                    "jeongja3": {"name": "정자3동", "schools_high": ["정자고", "율전고", "장안고"], "schools_mid": ["정자중", "율전중", "장안중"]},
                    "cheoncheon": {"name": "천천동", "schools_high": ["천천고", "수성고", "영생고"], "schools_mid": ["천천중", "수성중", "영화중"]},
                    "yeonmu": {"name": "연무동", "schools_high": ["수성고", "장안고", "삼일공고"], "schools_mid": ["수성중", "장안중", "연무중"]},
                    "pajang": {"name": "파장동", "schools_high": ["장안고", "수일여고", "천천고"], "schools_mid": ["파장중", "장안중", "수일여중"]},
                }
            },
            "gwonseon": {
                "name_ko": "권선구",
                "dongs": {
                    "gwonseon1": {"name": "권선1동", "schools_high": ["권선고", "곡선고", "세류고"], "schools_mid": ["권선중", "곡선중", "세류중"]},
                    "gwonseon2": {"name": "권선2동", "schools_high": ["권선고", "세류고", "칠보고"], "schools_mid": ["권선중", "세류중", "칠보중"]},
                    "homaesil": {"name": "호매실동", "schools_high": ["칠보고", "호매실고", "권선고"], "schools_mid": ["호매실중", "칠보중", "권선중"]},
                    "geumgok": {"name": "금곡동", "schools_high": ["금곡고", "호매실고", "칠보고"], "schools_mid": ["금곡중", "호매실중", "칠보중"]},
                    "chilbo": {"name": "칠보동", "schools_high": ["칠보고", "금곡고", "권선고"], "schools_mid": ["칠보중", "금곡중", "권선중"]},
                    "seryu1": {"name": "세류1동", "schools_high": ["세류고", "권선고", "수원공고"], "schools_mid": ["세류중", "권선중", "수원중"]},
                    "seryu2": {"name": "세류2동", "schools_high": ["세류고", "곡선고", "권선고"], "schools_mid": ["세류중", "곡선중", "권선중"]},
                    "seryu3": {"name": "세류3동", "schools_high": ["세류고", "고색고", "권선고"], "schools_mid": ["세류중", "고색중", "권선중"]},
                    "pyeong": {"name": "평동", "schools_high": ["고색고", "권선고", "곡선고"], "schools_mid": ["평중", "권선중", "곡선중"]},
                    "gosaek": {"name": "고색동", "schools_high": ["고색고", "권선고", "수원공고"], "schools_mid": ["고색중", "권선중", "수원중"]},
                }
            },
            "paldal": {
                "name_ko": "팔달구",
                "dongs": {
                    "uman1": {"name": "우만1동", "schools_high": ["유신고", "창현고", "수원고"], "schools_mid": ["우만중", "창현중", "수원중"]},
                    "uman2": {"name": "우만2동", "schools_high": ["창현고", "유신고", "동우여고"], "schools_mid": ["창현중", "우만중", "동우여중"]},
                    "ingye": {"name": "인계동", "schools_high": ["유신고", "창현고", "동우여고"], "schools_mid": ["인계중", "창현중", "동우여중"]},
                    "hwaseo1": {"name": "화서1동", "schools_high": ["수원고", "화홍고", "동우여고"], "schools_mid": ["화서중", "화홍중", "동우여중"]},
                    "hwaseo2": {"name": "화서2동", "schools_high": ["화홍고", "수원고", "유신고"], "schools_mid": ["화홍중", "화서중", "수원중"]},
                    "jidong": {"name": "지동", "schools_high": ["유신고", "수원고", "매향여고"], "schools_mid": ["지동중", "수원중", "매향여중"]},
                    "godeung": {"name": "고등동", "schools_high": ["유신고", "수원고", "매향여고"], "schools_mid": ["고등중", "수원중", "매향여중"]},
                    "maegyo": {"name": "매교동", "schools_high": ["수원고", "매향여고", "유신고"], "schools_mid": ["매교중", "매향여중", "수원중"]},
                }
            },
            "yeongtong": {
                "name_ko": "영통구",
                "dongs": {
                    "yeongtong1": {"name": "영통1동", "schools_high": ["영통고", "효원고", "청명고"], "schools_mid": ["영통중", "효원중", "청명중"]},
                    "yeongtong2": {"name": "영통2동", "schools_high": ["영통고", "효원고", "청명고"], "schools_mid": ["영통중", "효원중", "청명중"]},
                    "yeongtong3": {"name": "영통3동", "schools_high": ["청명고", "영통고", "효원고"], "schools_mid": ["청명중", "영통중", "효원중"]},
                    "maetan1": {"name": "매탄1동", "schools_high": ["매탄고", "영복여고", "효원고"], "schools_mid": ["매탄중", "영복여중", "효원중"]},
                    "maetan2": {"name": "매탄2동", "schools_high": ["매탄고", "영복여고", "청명고"], "schools_mid": ["매탄중", "영복여중", "청명중"]},
                    "maetan3": {"name": "매탄3동", "schools_high": ["매탄고", "효원고", "영통고"], "schools_mid": ["매탄중", "효원중", "영통중"]},
                    "maetan4": {"name": "매탄4동", "schools_high": ["매탄고", "영복여고", "청명고"], "schools_mid": ["매탄중", "영복여중", "청명중"]},
                    "woncheon": {"name": "원천동", "schools_high": ["아주대부고", "효원고", "영통고"], "schools_mid": ["원천중", "효원중", "영통중"]},
                    "gwanggyo1": {"name": "광교1동", "schools_high": ["광교고", "아주대부고", "영통고"], "schools_mid": ["광교중", "아주중", "영통중"]},
                    "gwanggyo2": {"name": "광교2동", "schools_high": ["광교고", "효원고", "청명고"], "schools_mid": ["광교중", "효원중", "청명중"]},
                    "mangpo1": {"name": "망포1동", "schools_high": ["망포고", "영통고", "효원고"], "schools_mid": ["망포중", "영통중", "효원중"]},
                    "mangpo2": {"name": "망포2동", "schools_high": ["망포고", "청명고", "영통고"], "schools_mid": ["망포중", "청명중", "영통중"]},
                }
            }
        }
    },
    "seongnam": {
        "name_ko": "성남시",
        "gus": {
            "sujeong": {
                "name_ko": "수정구",
                "dongs": {
                    "singheung1": {"name": "신흥1동", "schools_high": ["성남고", "신흥고", "성일정보고"], "schools_mid": ["신흥중", "성남중", "성일중"]},
                    "singheung2": {"name": "신흥2동", "schools_high": ["신흥고", "성남고", "복정고"], "schools_mid": ["신흥중", "복정중", "성남중"]},
                    "singheung3": {"name": "신흥3동", "schools_high": ["신흥고", "성일정보고", "성남고"], "schools_mid": ["신흥중", "성일중", "성남중"]},
                    "taepeong1": {"name": "태평1동", "schools_high": ["태평고", "성남고", "신흥고"], "schools_mid": ["태평중", "성남중", "신흥중"]},
                    "taepeong2": {"name": "태평2동", "schools_high": ["태평고", "성남고", "위례고"], "schools_mid": ["태평중", "위례중", "성남중"]},
                    "sujeong": {"name": "수진동", "schools_high": ["수진고", "성남고", "태평고"], "schools_mid": ["수진중", "성남중", "태평중"]},
                    "dandae": {"name": "단대동", "schools_high": ["단대고", "성남외고", "태평고"], "schools_mid": ["단대중", "성남중", "태평중"]},
                    "bokjeong": {"name": "복정동", "schools_high": ["복정고", "위례고", "성남고"], "schools_mid": ["복정중", "위례중", "성남중"]},
                    "sanseong": {"name": "산성동", "schools_high": ["성남고", "신흥고", "태평고"], "schools_mid": ["산성중", "신흥중", "태평중"]},
                }
            },
            "jungwon": {
                "name_ko": "중원구",
                "dongs": {
                    "seongnam": {"name": "성남동", "schools_high": ["성남고", "중원고", "풍생고"], "schools_mid": ["성남중", "중원중", "풍생중"]},
                    "geumgwang1": {"name": "금광1동", "schools_high": ["중원고", "풍생고", "성남고"], "schools_mid": ["금광중", "중원중", "풍생중"]},
                    "geumgwang2": {"name": "금광2동", "schools_high": ["풍생고", "중원고", "성남고"], "schools_mid": ["풍생중", "금광중", "중원중"]},
                    "eunhaeng1": {"name": "은행1동", "schools_high": ["중원고", "성남고", "풍생고"], "schools_mid": ["은행중", "성남중", "중원중"]},
                    "eunhaeng2": {"name": "은행2동", "schools_high": ["풍생고", "중원고", "성남고"], "schools_mid": ["은행중", "풍생중", "중원중"]},
                    "sangdaewon1": {"name": "상대원1동", "schools_high": ["상대원고", "중원고", "풍생고"], "schools_mid": ["상대원중", "중원중", "풍생중"]},
                    "sangdaewon2": {"name": "상대원2동", "schools_high": ["상대원고", "풍생고", "중원고"], "schools_mid": ["상대원중", "풍생중", "중원중"]},
                    "sangdaewon3": {"name": "상대원3동", "schools_high": ["상대원고", "중원고", "성남고"], "schools_mid": ["상대원중", "중원중", "성남중"]},
                    "hadaewon": {"name": "하대원동", "schools_high": ["중원고", "풍생고", "성남고"], "schools_mid": ["하대원중", "중원중", "풍생중"]},
                }
            },
            "bundang": {
                "name_ko": "분당구",
                "dongs": {
                    "seohyeon1": {"name": "서현1동", "schools_high": ["서현고", "분당고", "낙생고"], "schools_mid": ["서현중", "분당중", "낙생중"]},
                    "seohyeon2": {"name": "서현2동", "schools_high": ["서현고", "분당고", "이매고"], "schools_mid": ["서현중", "분당중", "이매중"]},
                    "imae1": {"name": "이매1동", "schools_high": ["이매고", "분당고", "서현고"], "schools_mid": ["이매중", "분당중", "서현중"]},
                    "imae2": {"name": "이매2동", "schools_high": ["이매고", "야탑고", "서현고"], "schools_mid": ["이매중", "야탑중", "서현중"]},
                    "yatap1": {"name": "야탑1동", "schools_high": ["야탑고", "분당고", "이매고"], "schools_mid": ["야탑중", "분당중", "이매중"]},
                    "yatap2": {"name": "야탑2동", "schools_high": ["야탑고", "이매고", "분당고"], "schools_mid": ["야탑중", "이매중", "분당중"]},
                    "yatap3": {"name": "야탑3동", "schools_high": ["야탑고", "분당고", "서현고"], "schools_mid": ["야탑중", "분당중", "서현중"]},
                    "sunae1": {"name": "수내1동", "schools_high": ["수내고", "분당고", "분당중앙고"], "schools_mid": ["수내중", "분당중", "분당중앙중"]},
                    "sunae2": {"name": "수내2동", "schools_high": ["수내고", "분당중앙고", "분당고"], "schools_mid": ["수내중", "분당중앙중", "분당중"]},
                    "sunae3": {"name": "수내3동", "schools_high": ["수내고", "분당고", "정자고"], "schools_mid": ["수내중", "분당중", "정자중"]},
                    "jeongja1": {"name": "정자1동", "schools_high": ["정자고", "분당고", "수내고"], "schools_mid": ["정자중", "분당중", "수내중"]},
                    "jeongja2": {"name": "정자2동", "schools_high": ["정자고", "수내고", "분당고"], "schools_mid": ["정자중", "수내중", "분당중"]},
                    "jeongja3": {"name": "정자3동", "schools_high": ["정자고", "분당고", "낙생고"], "schools_mid": ["정자중", "분당중", "낙생중"]},
                    "gumi1": {"name": "구미1동", "schools_high": ["구미고", "분당고", "낙생고"], "schools_mid": ["구미중", "분당중", "낙생중"]},
                    "gumi2": {"name": "구미2동", "schools_high": ["구미고", "낙생고", "분당고"], "schools_mid": ["구미중", "낙생중", "분당중"]},
                    "pangyo": {"name": "판교동", "schools_high": ["판교고", "낙생고", "분당고"], "schools_mid": ["판교중", "낙생중", "분당중"]},
                    "unjung1": {"name": "운중동", "schools_high": ["운중고", "판교고", "낙생고"], "schools_mid": ["운중중", "판교중", "낙생중"]},
                    "baekhyeon": {"name": "백현동", "schools_high": ["백현고", "판교고", "분당고"], "schools_mid": ["백현중", "판교중", "분당중"]},
                    "sampyeong": {"name": "삼평동", "schools_high": ["삼평고", "판교고", "백현고"], "schools_mid": ["삼평중", "판교중", "백현중"]},
                }
            }
        }
    },
    "yongin": {
        "name_ko": "용인시",
        "gus": {
            "suji": {
                "name_ko": "수지구",
                "dongs": {
                    "pungdeokcheon1": {"name": "풍덕천1동", "schools_high": ["풍덕고", "수지고", "손곡고"], "schools_mid": ["풍덕중", "수지중", "손곡중"]},
                    "pungdeokcheon2": {"name": "풍덕천2동", "schools_high": ["풍덕고", "손곡고", "수지고"], "schools_mid": ["풍덕중", "손곡중", "수지중"]},
                    "jukjeon1": {"name": "죽전1동", "schools_high": ["죽전고", "수지고", "신봉고"], "schools_mid": ["죽전중", "수지중", "신봉중"]},
                    "jukjeon2": {"name": "죽전2동", "schools_high": ["죽전고", "신봉고", "수지고"], "schools_mid": ["죽전중", "신봉중", "수지중"]},
                    "dongcheon": {"name": "동천동", "schools_high": ["동천고", "수지고", "신봉고"], "schools_mid": ["동천중", "수지중", "신봉중"]},
                    "sinbong": {"name": "신봉동", "schools_high": ["신봉고", "수지고", "죽전고"], "schools_mid": ["신봉중", "수지중", "죽전중"]},
                    "seongbok": {"name": "성복동", "schools_high": ["성복고", "수지고", "손곡고"], "schools_mid": ["성복중", "수지중", "손곡중"]},
                    "sangheondong": {"name": "상현1동", "schools_high": ["상현고", "수지고", "성복고"], "schools_mid": ["상현중", "수지중", "성복중"]},
                    "sangheondong2": {"name": "상현2동", "schools_high": ["상현고", "성복고", "수지고"], "schools_mid": ["상현중", "성복중", "수지중"]},
                }
            },
            "giheung": {
                "name_ko": "기흥구",
                "dongs": {
                    "giheung": {"name": "기흥동", "schools_high": ["기흥고", "용인고", "삼성고"], "schools_mid": ["기흥중", "용인중", "삼성중"]},
                    "sangha": {"name": "상하동", "schools_high": ["상하고", "기흥고", "용인고"], "schools_mid": ["상하중", "기흥중", "용인중"]},
                    "bojeong": {"name": "보정동", "schools_high": ["보정고", "기흥고", "죽전고"], "schools_mid": ["보정중", "기흥중", "죽전중"]},
                    "guseong": {"name": "구성동", "schools_high": ["구성고", "기흥고", "용인고"], "schools_mid": ["구성중", "기흥중", "용인중"]},
                    "sinjeong": {"name": "신갈동", "schools_high": ["신갈고", "기흥고", "용인고"], "schools_mid": ["신갈중", "기흥중", "용인중"]},
                    "yeongdeok1": {"name": "영덕1동", "schools_high": ["영덕고", "기흥고", "용인고"], "schools_mid": ["영덕중", "기흥중", "용인중"]},
                    "yeongdeok2": {"name": "영덕2동", "schools_high": ["영덕고", "용인고", "기흥고"], "schools_mid": ["영덕중", "용인중", "기흥중"]},
                    "donggak": {"name": "동백1동", "schools_high": ["동백고", "기흥고", "용인고"], "schools_mid": ["동백중", "기흥중", "용인중"]},
                    "donggak2": {"name": "동백2동", "schools_high": ["동백고", "용인고", "기흥고"], "schools_mid": ["동백중", "용인중", "기흥중"]},
                }
            },
            "cheoin": {
                "name_ko": "처인구",
                "dongs": {
                    "yeokbuk": {"name": "역북동", "schools_high": ["용인고", "처인고", "양지고"], "schools_mid": ["역북중", "처인중", "양지중"]},
                    "samga": {"name": "삼가동", "schools_high": ["처인고", "용인고", "양지고"], "schools_mid": ["삼가중", "처인중", "양지중"]},
                    "yuhyeon": {"name": "유림동", "schools_high": ["용인고", "처인고", "양지고"], "schools_mid": ["유림중", "처인중", "양지중"]},
                    "gimryang": {"name": "김량장동", "schools_high": ["처인고", "용인고", "양지고"], "schools_mid": ["김량장중", "처인중", "양지중"]},
                    "mohyeon": {"name": "모현동", "schools_high": ["모현고", "처인고", "용인고"], "schools_mid": ["모현중", "처인중", "용인중"]},
                }
            }
        }
    }
}

# 추가 도시 데이터 (간략화)
MORE_CITIES = {
    "bucheon": {"name_ko": "부천시", "schools_high": ["부천고", "부명고", "원미고", "상동고", "소사고"], "schools_mid": ["부천중", "부명중", "원미중", "상동중", "소사중"]},
    "anyang": {"name_ko": "안양시", "schools_high": ["안양고", "평촌고", "범계고", "관양고", "비산고"], "schools_mid": ["안양중", "평촌중", "범계중", "관양중", "비산중"]},
    "ansan": {"name_ko": "안산시", "schools_high": ["안산고", "단원고", "성포고", "원곡고", "광덕고"], "schools_mid": ["안산중", "단원중", "성포중", "원곡중", "광덕중"]},
    "namyangju": {"name_ko": "남양주시", "schools_high": ["남양주고", "호평고", "도농고", "진접고", "별내고"], "schools_mid": ["남양주중", "호평중", "도농중", "진접중", "별내중"]},
    "hwaseong": {"name_ko": "화성시", "schools_high": ["화성고", "동탄고", "병점고", "능동고", "반월고"], "schools_mid": ["화성중", "동탄중", "병점중", "능동중", "반월중"]},
    "pyeongtaek": {"name_ko": "평택시", "schools_high": ["평택고", "세교고", "비전고", "청북고", "한광고"], "schools_mid": ["평택중", "세교중", "비전중", "청북중", "한광중"]},
    "uijeongbu": {"name_ko": "의정부시", "schools_high": ["의정부고", "송양고", "호원고", "발곡고", "경민고"], "schools_mid": ["의정부중", "송양중", "호원중", "발곡중", "경민중"]},
    "siheung": {"name_ko": "시흥시", "schools_high": ["시흥고", "배곧고", "은행고", "함현고", "정왕고"], "schools_mid": ["시흥중", "배곧중", "은행중", "함현중", "정왕중"]},
    "paju": {"name_ko": "파주시", "schools_high": ["파주고", "금촌고", "교하고", "운정고", "한민고"], "schools_mid": ["파주중", "금촌중", "교하중", "운정중", "한민중"]},
    "gimpo": {"name_ko": "김포시", "schools_high": ["김포고", "양촌고", "장기고", "풍무고", "솔터고"], "schools_mid": ["김포중", "양촌중", "장기중", "풍무중", "솔터중"]},
    "gwangmyeong": {"name_ko": "광명시", "schools_high": ["광명고", "광명북고", "충현고", "진성고", "명문고"], "schools_mid": ["광명중", "광명북중", "충현중", "진성중", "명문중"]},
    "gunpo": {"name_ko": "군포시", "schools_high": ["군포고", "흥진고", "산본고", "당정고", "수리고"], "schools_mid": ["군포중", "흥진중", "산본중", "당정중", "수리중"]},
    "hanam": {"name_ko": "하남시", "schools_high": ["하남고", "위례고", "미사고", "창우고", "덕풍고"], "schools_mid": ["하남중", "위례중", "미사중", "창우중", "덕풍중"]},
    "osan": {"name_ko": "오산시", "schools_high": ["오산고", "세마고", "성호고", "운암고", "매홀고"], "schools_mid": ["오산중", "세마중", "성호중", "운암중", "매홀중"]},
    "icheon": {"name_ko": "이천시", "schools_high": ["이천고", "효양고", "증포고", "부발고", "대월고"], "schools_mid": ["이천중", "효양중", "증포중", "부발중", "대월중"]},
    "yangju": {"name_ko": "양주시", "schools_high": ["양주고", "덕정고", "회천고", "백석고", "고읍고"], "schools_mid": ["양주중", "덕정중", "회천중", "백석중", "고읍중"]},
    "guri": {"name_ko": "구리시", "schools_high": ["구리고", "인창고", "토평고", "갈매고", "동구고"], "schools_mid": ["구리중", "인창중", "토평중", "갈매중", "동구중"]},
}


def create_high_math_content(city_name, gu_name, dong_name, dong_name_en, schools_high, file_index):
    """고등 수학 콘텐츠 생성 - 표현 풀 활용"""
    school_str = "·".join(schools_high[:3])

    # 다양한 인덱스로 표현 풀에서 선택 (중복 최소화)
    idx = file_index
    intro = get_pool_item(INTRO_HIGH_MATH, idx)
    h2_why = get_pool_item(H2_HIGH_MATH_WHY, idx + 3)
    h2_exam = get_pool_item(H2_HIGH_MATH_EXAM, idx + 7)
    h2_suneung = get_pool_item(H2_HIGH_MATH_SUNEUNG, idx + 11)
    h2_compare = get_pool_item(H2_HIGH_MATH_COMPARE, idx + 13)
    h2_grade = get_pool_item(H2_HIGH_MATH_GRADE, idx + 17)

    body_why = get_pool_item(BODY_HIGH_MATH_WHY, idx + 5)
    body_compare = get_pool_item(BODY_COMPARE, idx + 9)
    body_grade = get_pool_item(BODY_GRADE_STRATEGY, idx + 15)

    boxes = [get_pool_item(IVORY_BOX_POOL, idx + i * 7) for i in range(7)]
    ending = get_pool_item(ENDING_POOL, idx + 19)
    image = get_pool_item(IMAGE_POOL, idx + 23)

    faq_q1 = get_pool_item(FAQ_Q1_VARIANTS, idx)
    faq_a1 = get_pool_item(FAQ_A1_VARIANTS, idx + 2)
    faq_q2 = get_pool_item(FAQ_Q2_VARIANTS, idx + 1)
    faq_a2 = get_pool_item(FAQ_A2_VARIANTS, idx + 3)
    faq_q3 = get_pool_item(FAQ_Q3_VARIANTS, idx + 4)
    faq_a3 = get_pool_item(FAQ_A3_VARIANTS, idx + 5)
    faq_q4 = get_pool_item(FAQ_Q4_VARIANTS, idx + 6)
    faq_a4 = get_pool_item(FAQ_A4_VARIANTS, idx + 7)

    content = f'''---
title: "{city_name} {gu_name} {dong_name} 고등 수학과외 | {school_str} 내신·수능 대비"
date: 2025-01-15
categories:
  - 고등교육
regions:
  - 경기도
  - {city_name}
cities:
  - {gu_name}
description: "{city_name} {gu_name} {dong_name} 고등학생 수학과외 전문. {schools_high[0]} 내신과 수능 동시 대비. 개념부터 킬러문항까지 체계적 1:1 지도."
tags:
  - {city_name}
  - {gu_name}
  - {dong_name}
  - 고등수학
  - 수학과외
  - 내신관리
  - 수능대비
  - {schools_high[0]}
featured_image: "https://images.unsplash.com/{image}?w=1200&h=630&fit=crop"
---
{intro}

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[0]}
</div>

## {h2_why}

{body_why}

{dong_name} 지역 {schools_high[0]} 학생들은 높은 내신 경쟁과 수능 준비를 동시에 해야 합니다. 학교 시험은 학교별 특성에 맞춰 대비해야 하고, 수능은 전국 단위 경쟁이므로 또 다른 전략이 필요합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[1]}
</div>

## {h2_exam}

{schools_high[0]}은 내신 시험 난이도가 높습니다. 교과서 기본 문제는 물론, 심화 문제와 변형 문제가 많이 출제됩니다. 단순히 공식을 외워서는 좋은 점수를 받기 어렵고, 개념을 깊이 이해하고 다양한 유형에 적용할 수 있어야 합니다.

시험 시간 대비 문제 양이 많은 편이어서 시간 관리도 중요합니다. 평소 시간을 재고 문제를 푸는 연습을 해야 실전에서 당황하지 않습니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[2]}
</div>

## {h2_suneung}

수능 수학은 내신과 출제 방식이 다릅니다. 킬러 문항이라 불리는 21번, 29번, 30번 문제는 여러 개념을 복합적으로 적용해야 풀 수 있습니다. 시간 압박 속에서 정확하게 문제를 푸는 능력이 필요합니다.

수능에서 1등급을 받으려면 킬러 문항 중 최소 1-2개는 맞혀야 합니다. 이를 위해서는 기본 개념이 완벽해야 하고, 다양한 심화 문제를 풀어본 경험이 있어야 합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[3]}
</div>

## {h2_compare}

{body_compare}

질문하기 어려운 학생도 1:1 수업에서는 편하게 물어볼 수 있습니다. 이해될 때까지 설명을 듣고, 스스로 문제를 풀어보며 실력을 키울 수 있습니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[4]}
</div>

## {h2_grade}

{body_grade}

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

**Q. {faq_q1}**

{faq_a1}

**Q. {faq_q2}**

{faq_a2}

**Q. {faq_q3}**

{faq_a3}

**Q. {faq_q4}**

{faq_a4}

## 마무리

{gu_name} {dong_name} 학생 여러분, {ending}
'''
    return content


def create_high_english_content(city_name, gu_name, dong_name, dong_name_en, schools_high, file_index):
    """고등 영어 콘텐츠 생성"""
    school_str = "·".join(schools_high[:3])
    idx = file_index + 100  # 수학과 다른 인덱스 사용

    intro = get_pool_item(INTRO_HIGH_ENG, idx)
    h2_why = get_pool_item(H2_HIGH_ENG_WHY, idx + 3)
    boxes = [get_pool_item(IVORY_BOX_POOL, idx + i * 7 + 50) for i in range(7)]
    ending = get_pool_item(ENDING_POOL, idx + 19)
    image = get_pool_item(IMAGE_POOL, idx + 30)

    faq_q1 = get_pool_item(FAQ_Q1_VARIANTS, idx + 1)
    faq_a1 = get_pool_item(FAQ_A1_VARIANTS, idx + 3)
    faq_q2 = get_pool_item(FAQ_Q2_VARIANTS, idx + 2)
    faq_a2 = get_pool_item(FAQ_A2_VARIANTS, idx + 4)

    content = f'''---
title: "{city_name} {gu_name} {dong_name} 고등 영어과외 | {school_str} 내신·수능 대비"
date: 2025-01-15
categories:
  - 고등교육
regions:
  - 경기도
  - {city_name}
cities:
  - {gu_name}
description: "{city_name} {gu_name} {dong_name} 고등학생 영어과외 전문. {schools_high[0]} 내신과 수능 동시 대비. 독해부터 문법까지 체계적 1:1 지도."
tags:
  - {city_name}
  - {gu_name}
  - {dong_name}
  - 고등영어
  - 영어과외
  - 내신관리
  - 수능대비
  - {schools_high[0]}
featured_image: "https://images.unsplash.com/{image}?w=1200&h=630&fit=crop"
---
{intro}

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[0]}
</div>

## {h2_why}

고등학교 영어는 중학교와 차원이 다릅니다. 지문의 길이가 길어지고, 어휘 수준이 높아지며, 문법적으로 복잡한 문장이 많아집니다. 단순히 단어를 많이 안다고 해서 좋은 성적을 받을 수 없습니다.

{dong_name} 지역 {schools_high[0]} 학생들은 내신과 수능을 동시에 준비해야 합니다. 학교 시험은 교과서와 부교재를 중심으로 출제되고, 수능은 처음 보는 지문을 빠르게 이해하는 능력이 필요합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[1]}
</div>

## 내신 영어 대비 전략

{schools_high[0]} 영어 시험은 교과서 본문의 완벽한 이해를 요구합니다. 단어, 숙어, 문법 포인트를 정리하고, 변형 문제에 대비해야 합니다. 서술형 문제도 출제되므로 영작 연습도 필요합니다.

시험 범위의 지문을 완벽히 분석하고, 예상 문제를 풀어보는 것이 효과적입니다. 기출문제 분석을 통해 출제 경향을 파악하면 대비가 수월해집니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[2]}
</div>

## 수능 영어의 핵심

수능 영어는 절대평가입니다. 90점 이상이면 1등급입니다. 하지만 쉽지 않습니다. 빈칸 추론, 순서 배열, 문장 삽입 등 고난도 유형이 있습니다.

독해 속도를 높이고, 글의 구조를 파악하는 능력이 필요합니다. 매일 꾸준히 영어 지문을 읽는 습관이 중요합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[3]}
</div>

## 1:1 영어 과외의 장점

학원에서는 많은 학생을 한꺼번에 가르치다 보니 개인별 약점을 보완하기 어렵습니다. 1:1 과외는 학생의 현재 수준에서 출발하여 약한 부분을 집중적으로 보강합니다.

문법이 약한 학생, 독해 속도가 느린 학생, 어휘력이 부족한 학생 각각 다른 접근이 필요합니다. 맞춤 수업이 효과적인 이유입니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[4]}
</div>

## 학년별 학습 전략

고1은 영어의 기초를 다지는 시기입니다. 기본 문법을 정리하고, 독해의 기본기를 익힙니다. 어휘력을 꾸준히 늘려가야 합니다.

고2는 실력을 쌓아가는 시기입니다. 다양한 유형의 지문을 접하고, 수능형 문제에 익숙해져야 합니다. 내신과 수능을 연결하는 학습이 필요합니다.

고3은 실전 대비의 시기입니다. 기출문제 분석, 모의고사 훈련, 약점 보완을 집중적으로 합니다.

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

**Q. {faq_q1}**

{faq_a1}

**Q. {faq_q2}**

{faq_a2}

**Q. 영어 단어는 어떻게 외워야 하나요?**

단순 암기보다 문맥 속에서 익히는 것이 효과적입니다. 예문과 함께 외우고, 반복적으로 접하면서 자연스럽게 익힙니다.

**Q. 독해 속도를 높이려면 어떻게 해야 하나요?**

매일 꾸준히 영어 지문을 읽는 것이 중요합니다. 직독직해 훈련과 함께 글의 구조를 파악하는 연습을 합니다.

## 마무리

{gu_name} {dong_name} 학생 여러분, {ending}
'''
    return content


def create_middle_math_content(city_name, gu_name, dong_name, dong_name_en, schools_mid, file_index):
    """중등 수학 콘텐츠 생성"""
    school_str = "·".join(schools_mid[:3])
    idx = file_index + 200

    intro = get_pool_item(INTRO_MID_MATH, idx)
    h2_why = get_pool_item(H2_MID_MATH_WHY, idx + 3)
    boxes = [get_pool_item(IVORY_BOX_POOL, idx + i * 7 + 25) for i in range(7)]
    ending = get_pool_item(ENDING_POOL, idx + 21)
    image = get_pool_item(IMAGE_POOL, idx + 40)

    content = f'''---
title: "{city_name} {gu_name} {dong_name} 중등 수학과외 | {school_str} 내신 완벽 대비"
date: 2025-01-15
categories:
  - 중등교육
regions:
  - 경기도
  - {city_name}
cities:
  - {gu_name}
description: "{city_name} {gu_name} {dong_name} 중학생 수학과외 전문. {schools_mid[0]} 내신 대비와 고등 선행까지. 개념부터 심화까지 체계적 1:1 지도."
tags:
  - {city_name}
  - {gu_name}
  - {dong_name}
  - 중등수학
  - 수학과외
  - 내신관리
  - 고등선행
  - {schools_mid[0]}
featured_image: "https://images.unsplash.com/{image}?w=1200&h=630&fit=crop"
---
{intro}

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[0]}
</div>

## {h2_why}

중학교 수학은 초등학교와 차원이 다릅니다. 음수, 문자식, 방정식 등 추상적인 개념이 등장합니다. 초등학교 때 산수를 잘했던 학생도 중학교에서 수학을 어려워하는 경우가 많습니다.

{dong_name} 지역 {schools_mid[0]} 학생들은 내신 관리와 함께 고등학교 진학을 준비해야 합니다. 중학교 수학을 확실히 잡아야 고등학교에서 수월합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[1]}
</div>

## 내신 시험 대비

{schools_mid[0]} 내신 시험은 교과서와 학교 프린트가 중심입니다. 기본 개념을 확실히 이해하고, 다양한 유형의 문제를 풀어보는 것이 중요합니다.

서술형 문제 비중이 높아지고 있습니다. 풀이 과정을 논리적으로 쓰는 연습이 필요합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[2]}
</div>

## 1:1 과외의 장점

학원에서는 많은 학생을 한꺼번에 가르치다 보니 개인별 약점을 보완하기 어렵습니다. 1:1 과외는 학생의 현재 수준에서 출발하여 약한 부분을 집중적으로 보강합니다.

질문하기 어려운 학생도 1:1 수업에서는 편하게 물어볼 수 있습니다. 이해될 때까지 설명을 듣고, 스스로 문제를 풀어보며 실력을 키울 수 있습니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[3]}
</div>

## 학년별 학습 전략

중1은 수학의 기초를 다지는 시기입니다. 정수와 유리수, 문자와 식, 방정식 등 기본 개념을 확실히 익혀야 합니다.

중2는 연립방정식, 함수, 도형의 성질 등을 배웁니다. 개념이 어려워지는 시기이므로 꼼꼼한 학습이 필요합니다.

중3은 고등학교 진학을 앞둔 중요한 시기입니다. 중학교 전체 내용을 정리하고, 고등 선행을 시작할 수 있습니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[4]}
</div>

## 수업료 안내

**중학생**은 주1회 22만원 - 32만원, 주2회 29만원 - 47만원 선입니다.

정확한 금액은 상담을 통해 안내드립니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[5]}
</div>

{{{{< cta-dual type="final" >}}}}

## 자주 묻는 질문

**Q. 수학 기초가 많이 부족한데 따라갈 수 있을까요?**

초등학교 내용부터 필요하면 다시 점검합니다. 기초를 확실히 다진 후 중학교 내용을 진행합니다.

**Q. 고등학교 선행은 언제부터 하나요?**

중학교 과정이 완성되면 시작합니다. 보통 중3 때 시작하지만 학생 상황에 따라 조절합니다.

**Q. 내신 시험 대비는 어떻게 하나요?**

시험 2-3주 전부터 학교 기출문제와 예상 문제 풀이로 집중 대비합니다.

## 마무리

{gu_name} {dong_name} 학생 여러분, {ending}
'''
    return content


def create_middle_english_content(city_name, gu_name, dong_name, dong_name_en, schools_mid, file_index):
    """중등 영어 콘텐츠 생성"""
    school_str = "·".join(schools_mid[:3])
    idx = file_index + 300

    intro = get_pool_item(INTRO_MID_ENG, idx)
    h2_why = get_pool_item(H2_MID_ENG_WHY, idx + 3)
    boxes = [get_pool_item(IVORY_BOX_POOL, idx + i * 7 + 75) for i in range(7)]
    ending = get_pool_item(ENDING_POOL, idx + 23)
    image = get_pool_item(IMAGE_POOL, idx + 50)

    content = f'''---
title: "{city_name} {gu_name} {dong_name} 중등 영어과외 | {school_str} 내신 완벽 대비"
date: 2025-01-15
categories:
  - 중등교육
regions:
  - 경기도
  - {city_name}
cities:
  - {gu_name}
description: "{city_name} {gu_name} {dong_name} 중학생 영어과외 전문. {schools_mid[0]} 내신 대비와 고등 선행까지. 문법부터 독해까지 체계적 1:1 지도."
tags:
  - {city_name}
  - {gu_name}
  - {dong_name}
  - 중등영어
  - 영어과외
  - 내신관리
  - 고등선행
  - {schools_mid[0]}
featured_image: "https://images.unsplash.com/{image}?w=1200&h=630&fit=crop"
---
{intro}

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[0]}
</div>

## {h2_why}

중학교 영어는 초등학교와 차원이 다릅니다. 문법이 본격적으로 등장하고, 독해 지문의 길이도 길어집니다. 초등학교 때 영어를 잘했던 학생도 중학교에서 어려움을 겪는 경우가 많습니다.

{dong_name} 지역 {schools_mid[0]} 학생들은 내신 관리와 함께 고등학교 영어를 준비해야 합니다. 중학교 때 기초를 확실히 잡아야 고등학교에서 수월합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[1]}
</div>

## 내신 영어 대비

{schools_mid[0]} 영어 시험은 교과서 본문이 중심입니다. 단어, 숙어, 문법 포인트를 정리하고, 본문 내용을 완벽히 이해해야 합니다.

서술형 문제 비중이 높아지고 있습니다. 영작 연습과 함께 문법 개념을 정확히 알아야 합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[2]}
</div>

## 1:1 과외의 장점

학원에서는 많은 학생을 한꺼번에 가르치다 보니 개인별 약점을 보완하기 어렵습니다. 1:1 과외는 학생의 현재 수준에서 출발하여 약한 부분을 집중적으로 보강합니다.

문법이 약한 학생, 독해가 느린 학생, 어휘력이 부족한 학생 각각 다른 접근이 필요합니다. 맞춤 수업이 효과적인 이유입니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[3]}
</div>

## 학년별 학습 전략

중1은 영어의 기초를 다지는 시기입니다. 기본 문법을 정리하고, 어휘력을 꾸준히 늘려가야 합니다.

중2는 문법이 어려워지는 시기입니다. 시제, 조동사, 수동태 등 핵심 문법을 확실히 익혀야 합니다.

중3은 고등학교 진학을 앞둔 중요한 시기입니다. 중학교 전체 문법을 정리하고, 고등 영어를 준비합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[4]}
</div>

## 수업료 안내

**중학생**은 주1회 22만원 - 32만원, 주2회 29만원 - 47만원 선입니다.

정확한 금액은 상담을 통해 안내드립니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[5]}
</div>

{{{{< cta-dual type="final" >}}}}

## 자주 묻는 질문

**Q. 영어 기초가 많이 부족한데 따라갈 수 있을까요?**

파닉스부터 필요하면 다시 시작합니다. 기초를 확실히 다진 후 중학교 내용을 진행합니다.

**Q. 문법이 너무 어려워요. 어떻게 해야 하나요?**

문법은 이해가 중요합니다. 암기보다 원리를 설명하고, 다양한 예문으로 연습합니다.

**Q. 내신 시험 대비는 어떻게 하나요?**

시험 2-3주 전부터 교과서 본문 분석과 예상 문제 풀이로 집중 대비합니다.

## 마무리

{gu_name} {dong_name} 학생 여러분, {ending}
'''
    return content


def create_index_content(city_name, gu_name):
    """목록 페이지 생성"""
    return f'''---
title: "{city_name} {gu_name} 과외"
date: 2025-01-15
---
{city_name} {gu_name} 지역 초중고 과외 정보입니다.
'''


def main():
    """메인 실행 함수"""
    base_path = "/home/user/edu-guide/content/gyeonggi"
    file_index = 0
    total_files = 0

    print("=" * 60)
    print("경기도 콘텐츠 재생성 시작")
    print("=" * 60)

    # 수원, 성남, 용인 처리
    for city_key, city_data in GYEONGGI_DATA.items():
        city_name = city_data["name_ko"]
        city_path = os.path.join(base_path, city_key)
        os.makedirs(city_path, exist_ok=True)

        print(f"\n{city_name} 처리 중...")

        for gu_key, gu_data in city_data["gus"].items():
            gu_name = gu_data["name_ko"]
            gu_path = os.path.join(city_path, gu_key)
            os.makedirs(gu_path, exist_ok=True)

            # 구 index 페이지
            with open(os.path.join(gu_path, "_index.md"), "w", encoding="utf-8") as f:
                f.write(create_index_content(city_name, gu_name))

            for dong_key, dong_data in gu_data["dongs"].items():
                dong_name = dong_data["name"]
                dong_path = os.path.join(gu_path, dong_key)
                os.makedirs(dong_path, exist_ok=True)

                schools_high = dong_data.get("schools_high", ["지역고"])
                schools_mid = dong_data.get("schools_mid", ["지역중"])

                # 동 index 페이지
                with open(os.path.join(dong_path, "_index.md"), "w", encoding="utf-8") as f:
                    f.write(f"---\ntitle: \"{dong_name} 과외\"\n---\n")

                # 4개 콘텐츠 파일 생성
                with open(os.path.join(dong_path, "high-math.md"), "w", encoding="utf-8") as f:
                    f.write(create_high_math_content(city_name, gu_name, dong_name, dong_key, schools_high, file_index))

                with open(os.path.join(dong_path, "high-english.md"), "w", encoding="utf-8") as f:
                    f.write(create_high_english_content(city_name, gu_name, dong_name, dong_key, schools_high, file_index))

                with open(os.path.join(dong_path, "middle-math.md"), "w", encoding="utf-8") as f:
                    f.write(create_middle_math_content(city_name, gu_name, dong_name, dong_key, schools_mid, file_index))

                with open(os.path.join(dong_path, "middle-english.md"), "w", encoding="utf-8") as f:
                    f.write(create_middle_english_content(city_name, gu_name, dong_name, dong_key, schools_mid, file_index))

                file_index += 1
                total_files += 4

        print(f"  {city_name} 완료")

    print(f"\n총 {total_files}개 파일 생성 완료")
    print("=" * 60)


if __name__ == "__main__":
    main()
