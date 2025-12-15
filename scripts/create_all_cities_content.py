#!/usr/bin/env python3
"""경기도 모든 도시 동단위 콘텐츠 생성 스크립트"""

import os
import sys
import shutil
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from create_suwon_content import (
    INTRO_POOL_HIGH_MATH, INTRO_POOL_HIGH_ENG,
    INTRO_POOL_MID_MATH, INTRO_POOL_MID_ENG,
    BOX_POOL, ENDING_POOL, IMAGE_POOL, get_expression
)

# 모든 도시 데이터
ALL_CITIES = {
    "yongin": {
        "name_ko": "용인시",
        "gus": {
            "suji": {
                "name_ko": "수지구",
                "dongs": {
                    "pungdeokcheon1": {"name": "풍덕천1동", "schools": ["수지고", "풍덕고", "죽전고"]},
                    "pungdeokcheon2": {"name": "풍덕천2동", "schools": ["풍덕고", "수지고", "현암고"]},
                    "jukjeon1": {"name": "죽전1동", "schools": ["죽전고", "수지고", "풍덕고"]},
                    "jukjeon2": {"name": "죽전2동", "schools": ["죽전고", "현암고", "수지고"]},
                    "dongan": {"name": "동안동", "schools": ["현암고", "수지고", "죽전고"]},
                    "sangdeok1": {"name": "상덕1동", "schools": ["수지고", "상현고", "풍덕고"]},
                    "sangdeok2": {"name": "상덕2동", "schools": ["상현고", "수지고", "현암고"]},
                    "sanghyeon1": {"name": "상현1동", "schools": ["상현고", "수지고", "죽전고"]},
                    "sanghyeon2": {"name": "상현2동", "schools": ["상현고", "풍덕고", "현암고"]},
                    "sanghyeon3": {"name": "상현3동", "schools": ["상현고", "수지고", "죽전고"]},
                    "seongnae": {"name": "성복동", "schools": ["현암고", "수지고", "상현고"]},
                }
            },
            "giheung": {
                "name_ko": "기흥구",
                "dongs": {
                    "sinjeong": {"name": "신갈동", "schools": ["기흥고", "용인삼계고", "용인고"]},
                    "giheung": {"name": "기흥동", "schools": ["기흥고", "용인고", "용인삼계고"]},
                    "guseong": {"name": "구성동", "schools": ["구성고", "기흥고", "용인고"]},
                    "dongin": {"name": "동인동", "schools": ["용인고", "기흥고", "구성고"]},
                    "sanggal": {"name": "상갈동", "schools": ["기흥고", "용인고", "구성고"]},
                    "yeonghee": {"name": "영덕동", "schools": ["용인삼계고", "기흥고", "용인고"]},
                    "maruk": {"name": "마북동", "schools": ["구성고", "용인삼계고", "기흥고"]},
                    "jungok": {"name": "중동", "schools": ["용인고", "기흥고", "용인삼계고"]},
                    "bohang": {"name": "보라동", "schools": ["보라고", "기흥고", "용인고"]},
                    "dongbaek": {"name": "동백동", "schools": ["동백고", "기흥고", "용인고"]},
                }
            },
            "cheoin": {
                "name_ko": "처인구",
                "dongs": {
                    "yeoksam": {"name": "역삼동", "schools": ["용인고", "처인고", "양지고"]},
                    "samga": {"name": "삼가동", "schools": ["처인고", "용인고", "양지고"]},
                    "yutang": {"name": "유방동", "schools": ["용인고", "처인고", "양지고"]},
                    "haeung": {"name": "해곡동", "schools": ["처인고", "용인고", "양지고"]},
                    "mohyeon": {"name": "모현면", "schools": ["용인고", "처인고", "양지고"]},
                }
            }
        }
    },
    "bucheon": {
        "name_ko": "부천시",
        "gus": {
            "bucheon": {
                "name_ko": "",
                "dongs": {
                    "wonmi1": {"name": "원미1동", "schools": ["부천고", "부천여고", "부흥고"]},
                    "wonmi2": {"name": "원미2동", "schools": ["부천여고", "부천고", "부흥고"]},
                    "simgok": {"name": "심곡동", "schools": ["심원고", "부천고", "부천여고"]},
                    "wonjonng": {"name": "원종동", "schools": ["부천고", "부명고", "부천여고"]},
                    "junghang": {"name": "중동", "schools": ["중원고", "부천고", "부천여고"]},
                    "sangdong": {"name": "상동", "schools": ["상동고", "중원고", "부천고"]},
                    "sosa": {"name": "소사동", "schools": ["소사고", "부천고", "부천여고"]},
                    "yakdae": {"name": "약대동", "schools": ["부명고", "부천고", "소사고"]},
                    "yeogwol": {"name": "역곡동", "schools": ["역곡고", "부천고", "부천여고"]},
                    "goeoe": {"name": "괴안동", "schools": ["부천고", "부명고", "역곡고"]},
                    "chunui": {"name": "춘의동", "schools": ["부천여고", "부천고", "부흥고"]},
                    "dosan": {"name": "도당동", "schools": ["부흥고", "부천고", "부천여고"]},
                    "sang": {"name": "성곡동", "schools": ["송내고", "부천고", "부천여고"]},
                    "songnae": {"name": "송내동", "schools": ["송내고", "부천고", "중원고"]},
                    "oka": {"name": "오정동", "schools": ["정명고", "부천고", "부천여고"]},
                }
            }
        }
    },
    "anyang": {
        "name_ko": "안양시",
        "gus": {
            "manan": {
                "name_ko": "만안구",
                "dongs": {
                    "anan1": {"name": "안양1동", "schools": ["안양고", "백영고", "신성고"]},
                    "anan2": {"name": "안양2동", "schools": ["백영고", "안양고", "신성고"]},
                    "anan3": {"name": "안양3동", "schools": ["안양고", "안양여고", "백영고"]},
                    "anan4": {"name": "안양4동", "schools": ["안양여고", "안양고", "신성고"]},
                    "anan5": {"name": "안양5동", "schools": ["신성고", "안양고", "백영고"]},
                    "anan6": {"name": "안양6동", "schools": ["안양고", "백영고", "안양여고"]},
                    "bakdal1": {"name": "박달1동", "schools": ["백영고", "안양고", "신성고"]},
                    "bakdal2": {"name": "박달2동", "schools": ["안양고", "백영고", "안양여고"]},
                    "seoksu1": {"name": "석수1동", "schools": ["안양고", "신성고", "백영고"]},
                    "seoksu2": {"name": "석수2동", "schools": ["신성고", "안양고", "안양여고"]},
                }
            },
            "dongan": {
                "name_ko": "동안구",
                "dongs": {
                    "bishan1": {"name": "비산1동", "schools": ["평촌고", "안양외고", "범계고"]},
                    "bishan2": {"name": "비산2동", "schools": ["범계고", "평촌고", "안양외고"]},
                    "bishan3": {"name": "비산3동", "schools": ["평촌고", "범계고", "부흥고"]},
                    "pyeongchon": {"name": "평촌동", "schools": ["평촌고", "안양외고", "범계고"]},
                    "hogye1": {"name": "호계1동", "schools": ["평촌고", "범계고", "안양외고"]},
                    "hogye2": {"name": "호계2동", "schools": ["범계고", "평촌고", "안양외고"]},
                    "hogye3": {"name": "호계3동", "schools": ["안양외고", "평촌고", "범계고"]},
                    "buheung": {"name": "부흥동", "schools": ["평촌고", "범계고", "부흥고"]},
                    "dalsan": {"name": "달산동", "schools": ["평촌고", "범계고", "안양외고"]},
                    "gwanyng": {"name": "관양1동", "schools": ["평촌고", "안양외고", "범계고"]},
                    "gwanyang2": {"name": "관양2동", "schools": ["범계고", "평촌고", "안양외고"]},
                }
            }
        }
    },
    "ansan": {
        "name_ko": "안산시",
        "gus": {
            "sangnok": {
                "name_ko": "상록구",
                "dongs": {
                    "wolpi1": {"name": "월피동", "schools": ["안산고", "상록고", "성포고"]},
                    "bonggok": {"name": "본오1동", "schools": ["상록고", "안산고", "성포고"]},
                    "bono2": {"name": "본오2동", "schools": ["안산고", "상록고", "성포고"]},
                    "bono3": {"name": "본오3동", "schools": ["성포고", "안산고", "상록고"]},
                    "saeong": {"name": "사동", "schools": ["안산고", "성포고", "상록고"]},
                    "ildeok": {"name": "일동", "schools": ["상록고", "안산고", "성포고"]},
                    "gong": {"name": "장상동", "schools": ["안산고", "상록고", "안산강서고"]},
                    "buyok": {"name": "부곡동", "schools": ["부곡고", "안산고", "상록고"]},
                }
            },
            "danwon": {
                "name_ko": "단원구",
                "dongs": {
                    "hogok": {"name": "호곡동", "schools": ["단원고", "성안고", "안산공고"]},
                    "seonbu1": {"name": "선부1동", "schools": ["단원고", "안산공고", "성안고"]},
                    "seonbu2": {"name": "선부2동", "schools": ["성안고", "단원고", "안산공고"]},
                    "seonbu3": {"name": "선부3동", "schools": ["단원고", "성안고", "안산공고"]},
                    "chodo": {"name": "초지동", "schools": ["성안고", "단원고", "안산공고"]},
                    "won": {"name": "원곡동", "schools": ["단원고", "성안고", "원곡고"]},
                    "daea": {"name": "대부동", "schools": ["단원고", "안산공고", "성안고"]},
                    "gozan": {"name": "고잔동", "schools": ["고잔고", "단원고", "성안고"]},
                }
            }
        }
    },
    "namyangju": {
        "name_ko": "남양주시",
        "gus": {
            "namyangju": {
                "name_ko": "",
                "dongs": {
                    "hopyeong": {"name": "호평동", "schools": ["호평고", "남양주고", "동화고"]},
                    "pyeongnae": {"name": "평내동", "schools": ["동화고", "남양주고", "호평고"]},
                    "geumgok": {"name": "금곡동", "schools": ["남양주고", "동화고", "호평고"]},
                    "yangjeong": {"name": "양정동", "schools": ["동화고", "남양주고", "호평고"]},
                    "dasan1": {"name": "다산1동", "schools": ["다산고", "남양주고", "동화고"]},
                    "dasan2": {"name": "다산2동", "schools": ["다산고", "동화고", "남양주고"]},
                    "byeollae": {"name": "별내동", "schools": ["별내고", "남양주고", "동화고"]},
                    "jinjeob": {"name": "진접읍", "schools": ["남양주고", "동화고", "진접고"]},
                    "onam": {"name": "오남읍", "schools": ["오남고", "남양주고", "동화고"]},
                    "jingeon": {"name": "진건읍", "schools": ["남양주고", "동화고", "호평고"]},
                    "hwadeo": {"name": "화도읍", "schools": ["화도고", "남양주고", "동화고"]},
                }
            }
        }
    },
    "hwaseong": {
        "name_ko": "화성시",
        "gus": {
            "hwaseong": {
                "name_ko": "",
                "dongs": {
                    "dongtan1": {"name": "동탄1동", "schools": ["동탄고", "능동고", "반송고"]},
                    "dongtan2": {"name": "동탄2동", "schools": ["능동고", "동탄고", "반송고"]},
                    "dongtan3": {"name": "동탄3동", "schools": ["반송고", "동탄고", "능동고"]},
                    "dongtan4": {"name": "동탄4동", "schools": ["동탄고", "능동고", "청명고"]},
                    "dongtan5": {"name": "동탄5동", "schools": ["동탄고", "청명고", "능동고"]},
                    "dongtan6": {"name": "동탄6동", "schools": ["청명고", "동탄고", "반송고"]},
                    "byungnam": {"name": "병점1동", "schools": ["병점고", "화성고", "동탄고"]},
                    "byungnam2": {"name": "병점2동", "schools": ["화성고", "병점고", "동탄고"]},
                    "donghwa": {"name": "봉담읍", "schools": ["봉담고", "화성고", "동탄고"]},
                    "hwangang": {"name": "향남읍", "schools": ["향남고", "화성고", "봉담고"]},
                    "jangdan": {"name": "정남면", "schools": ["화성고", "봉담고", "향남고"]},
                }
            }
        }
    },
    "pyeongtaek": {
        "name_ko": "평택시",
        "gus": {
            "pyeongtaek": {
                "name_ko": "",
                "dongs": {
                    "junang": {"name": "중앙동", "schools": ["평택고", "평택여고", "세교고"]},
                    "seojeong": {"name": "서정동", "schools": ["평택여고", "평택고", "세교고"]},
                    "songtan": {"name": "송탄동", "schools": ["송탄고", "평택고", "평택여고"]},
                    "shinpyeong": {"name": "신평동", "schools": ["평택고", "송탄고", "평택여고"]},
                    "paeksan": {"name": "비전1동", "schools": ["세교고", "평택고", "송탄고"]},
                    "paeksan2": {"name": "비전2동", "schools": ["평택고", "세교고", "송탄고"]},
                    "jije": {"name": "지제동", "schools": ["세교고", "평택고", "평택여고"]},
                    "sinjan": {"name": "신장동", "schools": ["평택고", "평택여고", "세교고"]},
                    "tongbok": {"name": "통복동", "schools": ["평택여고", "평택고", "송탄고"]},
                    "paengsung": {"name": "팽성읍", "schools": ["평택고", "송탄고", "세교고"]},
                    "anjung": {"name": "안중읍", "schools": ["안중고", "평택고", "평택여고"]},
                }
            }
        }
    },
    "uijeongbu": {
        "name_ko": "의정부시",
        "gus": {
            "uijeongbu": {
                "name_ko": "",
                "dongs": {
                    "uijeongbu1": {"name": "의정부1동", "schools": ["의정부고", "경민고", "효자고"]},
                    "uijeongbu2": {"name": "의정부2동", "schools": ["경민고", "의정부고", "효자고"]},
                    "uijeongbu3": {"name": "의정부3동", "schools": ["의정부고", "효자고", "경민고"]},
                    "hoewon1": {"name": "호원1동", "schools": ["효자고", "의정부고", "경민고"]},
                    "hoewon2": {"name": "호원2동", "schools": ["의정부고", "경민고", "효자고"]},
                    "sinheung": {"name": "신곡1동", "schools": ["경민고", "의정부고", "효자고"]},
                    "sinheung2": {"name": "신곡2동", "schools": ["의정부고", "효자고", "경민고"]},
                    "sonhwa": {"name": "송산1동", "schools": ["효자고", "경민고", "의정부고"]},
                    "sonhwa2": {"name": "송산2동", "schools": ["의정부고", "경민고", "효자고"]},
                    "jageung": {"name": "자금동", "schools": ["경민고", "의정부고", "효자고"]},
                    "ganeung": {"name": "가능동", "schools": ["의정부고", "효자고", "경민고"]},
                    "janghang": {"name": "장암동", "schools": ["효자고", "의정부고", "경민고"]},
                }
            }
        }
    },
    "siheung": {
        "name_ko": "시흥시",
        "gus": {
            "siheung": {
                "name_ko": "",
                "dongs": {
                    "daeya": {"name": "대야동", "schools": ["시흥고", "능곡고", "소래고"]},
                    "sincheon": {"name": "신천동", "schools": ["능곡고", "시흥고", "소래고"]},
                    "mogam": {"name": "목감동", "schools": ["소래고", "시흥고", "능곡고"]},
                    "jeongwang1": {"name": "정왕1동", "schools": ["정왕고", "시흥고", "능곡고"]},
                    "jeongwang2": {"name": "정왕2동", "schools": ["시흥고", "정왕고", "소래고"]},
                    "jeongwang3": {"name": "정왕3동", "schools": ["능곡고", "정왕고", "시흥고"]},
                    "jeongwang4": {"name": "정왕4동", "schools": ["정왕고", "능곡고", "시흥고"]},
                    "geumohyeon": {"name": "거모동", "schools": ["시흥고", "능곡고", "정왕고"]},
                    "eunhae": {"name": "은행동", "schools": ["능곡고", "시흥고", "소래고"]},
                    "baeugot": {"name": "배곧동", "schools": ["배곧고", "시흥고", "능곡고"]},
                }
            }
        }
    },
    "paju": {
        "name_ko": "파주시",
        "gus": {
            "paju": {
                "name_ko": "",
                "dongs": {
                    "geumchon1": {"name": "금촌1동", "schools": ["파주고", "금촌고", "문산고"]},
                    "geumchon2": {"name": "금촌2동", "schools": ["금촌고", "파주고", "문산고"]},
                    "geumchon3": {"name": "금촌3동", "schools": ["파주고", "금촌고", "문산고"]},
                    "yodam": {"name": "교하동", "schools": ["운정고", "파주고", "금촌고"]},
                    "unjeong1": {"name": "운정1동", "schools": ["운정고", "파주고", "금촌고"]},
                    "unjeong2": {"name": "운정2동", "schools": ["파주고", "운정고", "금촌고"]},
                    "unjeong3": {"name": "운정3동", "schools": ["운정고", "금촌고", "파주고"]},
                    "munsan": {"name": "문산읍", "schools": ["문산고", "파주고", "금촌고"]},
                    "papyeong": {"name": "파평면", "schools": ["파주고", "문산고", "금촌고"]},
                    "jeokseong": {"name": "적성면", "schools": ["파주고", "금촌고", "문산고"]},
                }
            }
        }
    },
    "gimpo": {
        "name_ko": "김포시",
        "gus": {
            "gimpo": {
                "name_ko": "",
                "dongs": {
                    "gimpo1": {"name": "김포1동", "schools": ["김포고", "김포제일고", "양곡고"]},
                    "gimpo2": {"name": "김포2동", "schools": ["김포제일고", "김포고", "양곡고"]},
                    "janggi": {"name": "장기동", "schools": ["양곡고", "김포고", "김포제일고"]},
                    "gurae": {"name": "구래동", "schools": ["김포고", "김포제일고", "풍무고"]},
                    "majeon": {"name": "마산동", "schools": ["풍무고", "김포고", "김포제일고"]},
                    "gochon": {"name": "고촌읍", "schools": ["김포고", "김포제일고", "양곡고"]},
                    "yangchon": {"name": "양촌읍", "schools": ["양곡고", "김포고", "김포제일고"]},
                    "tongjin": {"name": "통진읍", "schools": ["김포고", "양곡고", "김포제일고"]},
                    "hangang": {"name": "한강로", "schools": ["김포제일고", "김포고", "양곡고"]},
                    "pungmu": {"name": "풍무동", "schools": ["풍무고", "김포고", "김포제일고"]},
                }
            }
        }
    },
    "gwangmyeong": {
        "name_ko": "광명시",
        "gus": {
            "gwangmyeong": {
                "name_ko": "",
                "dongs": {
                    "gwangmyeong1": {"name": "광명1동", "schools": ["광명고", "광명북고", "진성고"]},
                    "gwangmyeong2": {"name": "광명2동", "schools": ["광명북고", "광명고", "진성고"]},
                    "gwangmyeong3": {"name": "광명3동", "schools": ["광명고", "진성고", "광명북고"]},
                    "gwangmyeong4": {"name": "광명4동", "schools": ["진성고", "광명고", "광명북고"]},
                    "gwangmyeong5": {"name": "광명5동", "schools": ["광명고", "광명북고", "진성고"]},
                    "gwangmyeong6": {"name": "광명6동", "schools": ["광명북고", "진성고", "광명고"]},
                    "gwangmyeong7": {"name": "광명7동", "schools": ["광명고", "진성고", "광명북고"]},
                    "choldong": {"name": "철산1동", "schools": ["진성고", "광명고", "광명북고"]},
                    "choldong2": {"name": "철산2동", "schools": ["광명고", "광명북고", "진성고"]},
                    "choldong3": {"name": "철산3동", "schools": ["광명북고", "광명고", "진성고"]},
                    "choldong4": {"name": "철산4동", "schools": ["진성고", "광명북고", "광명고"]},
                    "soha1": {"name": "소하1동", "schools": ["소하고", "광명고", "진성고"]},
                    "soha2": {"name": "소하2동", "schools": ["광명고", "소하고", "광명북고"]},
                    "haan": {"name": "하안1동", "schools": ["광명고", "진성고", "소하고"]},
                    "haan2": {"name": "하안2동", "schools": ["진성고", "광명고", "소하고"]},
                    "haan3": {"name": "하안3동", "schools": ["광명고", "소하고", "진성고"]},
                    "haan4": {"name": "하안4동", "schools": ["소하고", "광명고", "진성고"]},
                }
            }
        }
    },
    "gunpo": {
        "name_ko": "군포시",
        "gus": {
            "gunpo": {
                "name_ko": "",
                "dongs": {
                    "gunpo1": {"name": "군포1동", "schools": ["군포고", "흥진고", "수리고"]},
                    "gunpo2": {"name": "군포2동", "schools": ["흥진고", "군포고", "수리고"]},
                    "sanbon1": {"name": "산본1동", "schools": ["수리고", "군포고", "흥진고"]},
                    "sanbon2": {"name": "산본2동", "schools": ["군포고", "수리고", "흥진고"]},
                    "gumjung": {"name": "금정동", "schools": ["흥진고", "수리고", "군포고"]},
                    "dangan": {"name": "당정동", "schools": ["군포고", "흥진고", "수리고"]},
                    "daeya": {"name": "대야동", "schools": ["수리고", "흥진고", "군포고"]},
                    "sueom": {"name": "수리동", "schools": ["수리고", "군포고", "흥진고"]},
                }
            }
        }
    },
    "hanam": {
        "name_ko": "하남시",
        "gus": {
            "hanam": {
                "name_ko": "",
                "dongs": {
                    "sinjan1": {"name": "신장1동", "schools": ["하남고", "미사고", "위례고"]},
                    "sinjan2": {"name": "신장2동", "schools": ["미사고", "하남고", "위례고"]},
                    "deogsong1": {"name": "덕풍1동", "schools": ["하남고", "위례고", "미사고"]},
                    "deogsong2": {"name": "덕풍2동", "schools": ["위례고", "하남고", "미사고"]},
                    "deogsong3": {"name": "덕풍3동", "schools": ["미사고", "위례고", "하남고"]},
                    "misa1": {"name": "미사1동", "schools": ["미사고", "하남고", "위례고"]},
                    "misa2": {"name": "미사2동", "schools": ["하남고", "미사고", "위례고"]},
                    "wirye": {"name": "위례동", "schools": ["위례고", "미사고", "하남고"]},
                    "chuncheong": {"name": "춘궁동", "schools": ["하남고", "미사고", "위례고"]},
                }
            }
        }
    },
    "osan": {
        "name_ko": "오산시",
        "gus": {
            "osan": {
                "name_ko": "",
                "dongs": {
                    "junang": {"name": "중앙동", "schools": ["오산고", "세마고", "운천고"]},
                    "daewon": {"name": "대원동", "schools": ["세마고", "오산고", "운천고"]},
                    "namchon": {"name": "남촌동", "schools": ["오산고", "운천고", "세마고"]},
                    "sinjan": {"name": "신장동", "schools": ["운천고", "오산고", "세마고"]},
                    "sema": {"name": "세마동", "schools": ["세마고", "운천고", "오산고"]},
                    "chowon": {"name": "초평동", "schools": ["오산고", "세마고", "운천고"]},
                }
            }
        }
    },
    "icheon": {
        "name_ko": "이천시",
        "gus": {
            "icheon": {
                "name_ko": "",
                "dongs": {
                    "junang": {"name": "중앙동", "schools": ["이천고", "이천제일고", "이현고"]},
                    "gwan": {"name": "관고동", "schools": ["이천제일고", "이천고", "이현고"]},
                    "jeung": {"name": "증포동", "schools": ["이현고", "이천고", "이천제일고"]},
                    "changjeon": {"name": "창전동", "schools": ["이천고", "이현고", "이천제일고"]},
                    "sindun": {"name": "신둔면", "schools": ["이천제일고", "이현고", "이천고"]},
                    "bubal": {"name": "부발읍", "schools": ["이천고", "이천제일고", "이현고"]},
                }
            }
        }
    },
    "yangju": {
        "name_ko": "양주시",
        "gus": {
            "yangju": {
                "name_ko": "",
                "dongs": {
                    "yangju1": {"name": "양주1동", "schools": ["양주고", "양주백석고", "덕정고"]},
                    "yangju2": {"name": "양주2동", "schools": ["양주백석고", "양주고", "덕정고"]},
                    "hwedok": {"name": "회천1동", "schools": ["덕정고", "양주고", "양주백석고"]},
                    "hwedok2": {"name": "회천2동", "schools": ["양주고", "덕정고", "양주백석고"]},
                    "hwedok3": {"name": "회천3동", "schools": ["양주백석고", "덕정고", "양주고"]},
                    "hwedok4": {"name": "회천4동", "schools": ["덕정고", "양주백석고", "양주고"]},
                    "goesan": {"name": "고읍동", "schools": ["양주고", "양주백석고", "덕정고"]},
                    "baekseok": {"name": "백석읍", "schools": ["양주백석고", "양주고", "덕정고"]},
                    "eunhyun": {"name": "은현면", "schools": ["양주고", "덕정고", "양주백석고"]},
                }
            }
        }
    },
    "guri": {
        "name_ko": "구리시",
        "gus": {
            "guri": {
                "name_ko": "",
                "dongs": {
                    "galmaok": {"name": "갈매동", "schools": ["구리고", "인창고", "동구고"]},
                    "inchang": {"name": "인창동", "schools": ["인창고", "구리고", "동구고"]},
                    "gyomun1": {"name": "교문1동", "schools": ["동구고", "구리고", "인창고"]},
                    "gyomun2": {"name": "교문2동", "schools": ["구리고", "동구고", "인창고"]},
                    "sueok1": {"name": "수택1동", "schools": ["인창고", "동구고", "구리고"]},
                    "sueok2": {"name": "수택2동", "schools": ["구리고", "인창고", "동구고"]},
                    "sueok3": {"name": "수택3동", "schools": ["동구고", "구리고", "인창고"]},
                }
            }
        }
    },
}

def create_content(city_name_ko, city_name_en, gu_name_ko, dong_name, dong_name_en, schools, file_type, file_index, city_index):
    """콘텐츠 생성 함수"""
    school_str = "·".join(schools[:3])
    offset = city_index * 100 + file_index

    if file_type == "high-math":
        intro = get_expression(INTRO_POOL_HIGH_MATH, offset)
        boxes = [get_expression(BOX_POOL, offset + i * 7) for i in range(7)]
        ending = get_expression(ENDING_POOL, offset)
        image = get_expression(IMAGE_POOL, offset)
        category = "고등교육"
        subject = "수학"
        subject_tags = ["고등수학", "수학과외", "내신관리", "수능대비"]

        if gu_name_ko:
            title = f"{city_name_ko} {gu_name_ko} {dong_name} 고등 수학과외 | {school_str} 내신·수능 대비"
            desc = f"{city_name_ko} {gu_name_ko} {dong_name} 고등학생 수학과외 전문. {schools[0]} 내신과 수능 동시 대비."
        else:
            title = f"{city_name_ko} {dong_name} 고등 수학과외 | {school_str} 내신·수능 대비"
            desc = f"{city_name_ko} {dong_name} 고등학생 수학과외 전문. {schools[0]} 내신과 수능 동시 대비."

    elif file_type == "high-english":
        intro = get_expression(INTRO_POOL_HIGH_ENG, offset + 1)
        boxes = [get_expression(BOX_POOL, offset + i * 5 + 3) for i in range(7)]
        ending = get_expression(ENDING_POOL, offset + 1)
        image = get_expression(IMAGE_POOL, offset + 1)
        category = "고등교육"
        subject = "영어"
        subject_tags = ["고등영어", "영어과외", "내신관리", "수능대비"]

        if gu_name_ko:
            title = f"{city_name_ko} {gu_name_ko} {dong_name} 고등 영어과외 | {school_str} 내신·수능 대비"
            desc = f"{city_name_ko} {gu_name_ko} {dong_name} 고등학생 영어과외 전문. {schools[0]} 내신과 수능 동시 대비."
        else:
            title = f"{city_name_ko} {dong_name} 고등 영어과외 | {school_str} 내신·수능 대비"
            desc = f"{city_name_ko} {dong_name} 고등학생 영어과외 전문. {schools[0]} 내신과 수능 동시 대비."

    elif file_type == "middle-math":
        intro = get_expression(INTRO_POOL_MID_MATH, offset + 2)
        boxes = [get_expression(BOX_POOL, offset + i * 4 + 2) for i in range(7)]
        ending = get_expression(ENDING_POOL, offset + 2)
        image = get_expression(IMAGE_POOL, offset + 2)
        category = "중등교육"
        subject = "수학"
        subject_tags = ["중등수학", "수학과외", "내신관리", "고등선행"]
        school_str = "·".join([s.replace("고", "중") for s in schools[:3]])

        if gu_name_ko:
            title = f"{city_name_ko} {gu_name_ko} {dong_name} 중등 수학과외 | {school_str} 내신 완벽 대비"
            desc = f"{city_name_ko} {gu_name_ko} {dong_name} 중학생 수학과외 전문. 내신 대비와 고등 선행까지."
        else:
            title = f"{city_name_ko} {dong_name} 중등 수학과외 | {school_str} 내신 완벽 대비"
            desc = f"{city_name_ko} {dong_name} 중학생 수학과외 전문. 내신 대비와 고등 선행까지."

    else:  # middle-english
        intro = get_expression(INTRO_POOL_MID_ENG, offset + 3)
        boxes = [get_expression(BOX_POOL, offset + i * 6 + 1) for i in range(7)]
        ending = get_expression(ENDING_POOL, offset + 3)
        image = get_expression(IMAGE_POOL, offset + 3)
        category = "중등교육"
        subject = "영어"
        subject_tags = ["중등영어", "영어과외", "내신관리", "고등선행"]
        school_str = "·".join([s.replace("고", "중") for s in schools[:3]])

        if gu_name_ko:
            title = f"{city_name_ko} {gu_name_ko} {dong_name} 중등 영어과외 | {school_str} 내신 완벽 대비"
            desc = f"{city_name_ko} {gu_name_ko} {dong_name} 중학생 영어과외 전문. 내신 대비와 고등 선행까지."
        else:
            title = f"{city_name_ko} {dong_name} 중등 영어과외 | {school_str} 내신 완벽 대비"
            desc = f"{city_name_ko} {dong_name} 중학생 영어과외 전문. 내신 대비와 고등 선행까지."

    # 수업료 정보
    if category == "고등교육":
        fee_info = """**고1-2**는 주1회 25만원 - 36만원, 주2회 33만원 - 53만원 선입니다.

**고3**은 주1회 28만원 - 40만원, 주2회 37만원 - 59만원이 일반적입니다."""
    else:
        fee_info = """**중학생**은 주1회 22만원 - 32만원, 주2회 29만원 - 47만원 선입니다."""

    location = f"{gu_name_ko} {dong_name}" if gu_name_ko else dong_name

    content = f'''---
aliases:
  - /{file_type.split('-')[0]}/{city_name_en}-{dong_name_en}-{file_type}/
title: "{title}"
date: 2025-01-15
categories:
  - {category}
regions:
  - 경기도
  - {city_name_ko}
description: "{desc}"
tags:
  - {city_name_ko}
  - {dong_name}
  - {subject_tags[0]}
  - {subject_tags[1]}
  - {subject_tags[2]}
  - {subject_tags[3]}
featured_image: "https://images.unsplash.com/{image}?w=1200&h=630&fit=crop"
---
{intro}

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[0]}
</div>

## {subject} 실력, 왜 중요할까요?

{dong_name} 지역 학생들은 내신 경쟁과 상위 학교 진학을 위해 체계적인 학습이 필요합니다. 학교 시험은 학교별 특성에 맞춰 대비해야 하고, 상위권 성적을 유지하려면 꾸준한 노력이 필요합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[1]}
</div>

## {schools[0]} 내신 시험 분석

{schools[0]}은 내신 시험 난이도가 높습니다. 교과서 기본 문제는 물론, 심화 문제와 변형 문제가 출제됩니다. 개념을 깊이 이해하고 다양한 유형에 적용할 수 있어야 합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[2]}
</div>

## 학원과 과외의 차이

학원에서는 많은 학생을 한꺼번에 가르치다 보니 개인별 약점을 보완하기 어렵습니다. 1:1 과외는 학생의 현재 수준에서 출발하여 약한 부분을 집중적으로 보강합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[3]}
</div>

## 학년별 학습 전략

학년에 따라 학습 전략이 달라져야 합니다. 기초를 다지는 시기와 심화 학습이 필요한 시기, 실전 대비가 필요한 시기를 구분하여 효율적으로 학습해야 합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[4]}
</div>

## 수업료 안내

{fee_info}

정확한 금액은 상담을 통해 안내드립니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[5]}
</div>

{{{{< cta-dual type="final" >}}}}

## 자주 묻는 질문

**Q. 기초가 많이 부족한데 따라갈 수 있을까요?**

기초부터 다시 점검하고 필요한 부분을 보강합니다. 기초를 확실히 다진 후 진행합니다.

**Q. 내신 시험 대비는 어떻게 하나요?**

시험 2-3주 전부터 학교 기출문제와 예상 문제 풀이로 집중 대비합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
{boxes[6]}
</div>

## 마무리

{location} 학생 여러분, {ending}
'''
    return content

def main():
    base_path = "/home/user/edu-guide/content/gyeonggi"

    city_index = 0
    total_files = 0

    for city_key, city_data in ALL_CITIES.items():
        city_name_ko = city_data["name_ko"]
        city_path = f"{base_path}/{city_key}"

        # 기존 폴더 삭제 후 재생성
        if os.path.exists(city_path):
            shutil.rmtree(city_path)
        os.makedirs(city_path, exist_ok=True)

        # 도시 인덱스
        with open(f"{city_path}/_index.md", "w", encoding="utf-8") as f:
            f.write(f'''---
title: "{city_name_ko} 과외"
date: 2025-01-15
description: "{city_name_ko} 전 지역 초중고 과외 정보."
---
{city_name_ko} 전 지역 과외 정보를 안내합니다.
''')

        file_index = 0
        city_files = 0

        for gu_key, gu_data in city_data["gus"].items():
            gu_name_ko = gu_data["name_ko"]

            if gu_name_ko:  # 구가 있는 경우
                gu_path = f"{city_path}/{gu_key}"
                os.makedirs(gu_path, exist_ok=True)

                with open(f"{gu_path}/_index.md", "w", encoding="utf-8") as f:
                    f.write(f'''---
title: "{city_name_ko} {gu_name_ko} 과외"
date: 2025-01-15
description: "{city_name_ko} {gu_name_ko} 지역 과외 정보."
---
{gu_name_ko} 지역 과외 정보를 안내합니다.
''')
                dong_base_path = gu_path
            else:
                dong_base_path = city_path

            for dong_key, dong_data in gu_data["dongs"].items():
                dong_name = dong_data["name"]
                schools = dong_data["schools"]
                dong_path = f"{dong_base_path}/{dong_key}"
                os.makedirs(dong_path, exist_ok=True)

                # 동 인덱스
                with open(f"{dong_path}/_index.md", "w", encoding="utf-8") as f:
                    if gu_name_ko:
                        f.write(f'''---
title: "{city_name_ko} {gu_name_ko} {dong_name} 과외"
date: 2025-01-15
description: "{city_name_ko} {gu_name_ko} {dong_name} 지역 과외 정보."
---
{dong_name} 지역 과외 정보를 안내합니다.
''')
                    else:
                        f.write(f'''---
title: "{city_name_ko} {dong_name} 과외"
date: 2025-01-15
description: "{city_name_ko} {dong_name} 지역 과외 정보."
---
{dong_name} 지역 과외 정보를 안내합니다.
''')

                # 4개 파일 생성
                for file_type in ["high-math", "high-english", "middle-math", "middle-english"]:
                    content = create_content(
                        city_name_ko, city_key, gu_name_ko,
                        dong_name, dong_key, schools,
                        file_type, file_index, city_index
                    )
                    with open(f"{dong_path}/{file_type}.md", "w", encoding="utf-8") as f:
                        f.write(content)

                file_index += 1
                city_files += 4

        print(f"Created: {city_name_ko} ({city_files} files)")
        total_files += city_files
        city_index += 1

    print(f"\n총 {total_files}개 파일 생성 완료!")

if __name__ == "__main__":
    main()
