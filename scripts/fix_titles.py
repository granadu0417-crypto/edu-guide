#!/usr/bin/env python3
"""제목 중복 수정 스크립트 - 동마다 다른 제목 표현 적용"""

import os
import re

# 고등 수학 제목 표현
HIGH_MATH_SUFFIXES = [
    "내신·수능 대비",
    "맞춤 커리큘럼",
    "개념부터 실전까지",
    "학교별 내신 특화",
    "기초부터 심화까지",
    "1:1 맞춤 수업",
    "실력 향상 수업",
    "체계적 학습 관리",
    "내신 + 수능 병행",
    "개념완성 수업",
]

# 고등 영어 제목 표현
HIGH_ENGLISH_SUFFIXES = [
    "내신·수능 대비",
    "독해·문법 완성",
    "맞춤 커리큘럼",
    "체계적 학습 관리",
    "실력 향상 수업",
    "기초부터 심화까지",
    "1:1 맞춤 수업",
    "학교별 내신 특화",
    "내신 + 수능 병행",
    "어휘·독해 집중",
]

# 중등 수학 제목 표현
MIDDLE_MATH_SUFFIXES = [
    "내신 완벽 대비",
    "맞춤 커리큘럼",
    "개념부터 실전까지",
    "학교별 내신 특화",
    "기초부터 심화까지",
    "1:1 맞춤 수업",
    "실력 향상 수업",
    "체계적 학습 관리",
    "개념완성 수업",
    "내신 집중 관리",
]

# 중등 영어 제목 표현
MIDDLE_ENGLISH_SUFFIXES = [
    "내신 완벽 대비",
    "독해·문법 완성",
    "맞춤 커리큘럼",
    "체계적 학습 관리",
    "실력 향상 수업",
    "기초부터 심화까지",
    "1:1 맞춤 수업",
    "학교별 내신 특화",
    "어휘·문법 집중",
    "내신 집중 관리",
]

def fix_title_in_file(filepath, suffix):
    """파일의 title을 수정"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # title 라인 찾아서 수정
    # 패턴: title: "... | 학교명 기존표현"
    pattern = r'(title: "[^|]+\| [^"]+) (내신·수능 대비|내신 완벽 대비|내신\+수능 대비)"'
    replacement = rf'\1 {suffix}"'

    new_content = re.sub(pattern, replacement, content)

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def fix_district_titles(district, folder, dong_list):
    """구별로 제목 수정"""
    fixed_count = 0

    for i, dong_id in enumerate(dong_list):
        # 수학 파일
        math_file = f"content/{folder}/{district}-{dong_id}-{folder}-math.md"
        if os.path.exists(math_file):
            if folder == "high":
                suffix = HIGH_MATH_SUFFIXES[i % len(HIGH_MATH_SUFFIXES)]
            else:
                suffix = MIDDLE_MATH_SUFFIXES[i % len(MIDDLE_MATH_SUFFIXES)]
            if fix_title_in_file(math_file, suffix):
                fixed_count += 1

        # 영어 파일
        english_file = f"content/{folder}/{district}-{dong_id}-{folder}-english.md"
        if os.path.exists(english_file):
            if folder == "high":
                suffix = HIGH_ENGLISH_SUFFIXES[i % len(HIGH_ENGLISH_SUFFIXES)]
            else:
                suffix = MIDDLE_ENGLISH_SUFFIXES[i % len(MIDDLE_ENGLISH_SUFFIXES)]
            if fix_title_in_file(english_file, suffix):
                fixed_count += 1

    return fixed_count

# 도봉구 동 리스트
DOBONG_DONGS = [
    "ssangmun1", "ssangmun2", "ssangmun3", "ssangmun4",
    "chang1", "chang2", "chang3", "chang4", "chang5",
    "banghak1", "banghak2", "banghak3",
    "dobong1", "dobong2"
]

# 동대문구 동 리스트
DONGDAEMUN_DONGS = [
    "yongsin", "jegi", "cheongnyangni", "hoegi",
    "hwigyeong1", "hwigyeong2", "imun1", "imun2",
    "jeonnong1", "jeonnong2", "dapsimni1", "dapsimni2",
    "jangan1", "jangan2"
]

# 금천구 동 리스트
GEUMCHEON_DONGS = [
    "gasan", "doksan1", "doksan2", "doksan3", "doksan4",
    "siheung1", "siheung2", "siheung3", "siheung4", "siheung5"
]

# 강북구 동 리스트
GANGBUK_DONGS = [
    "beon1", "beon2", "beon3",
    "suyu1", "suyu2", "suyu3",
    "ui", "samyang", "songbuk", "samgaksan",
    "mia", "songjung", "wolgok"
]

# 구로구 동 리스트
GURO_DONGS = [
    "gaebong1", "gaebong2", "gaebong3",
    "gocheok1", "gocheok2",
    "guro1", "guro2", "guro3", "guro4", "guro5",
    "sindorim", "oryu1", "oryu2",
    "hangdong", "sugung", "cheonwang"
]

def main():
    total_fixed = 0

    # 도봉구 고등 + 중등
    print("도봉구 수정 중...")
    total_fixed += fix_district_titles("dobong", "high", DOBONG_DONGS)
    total_fixed += fix_district_titles("dobong", "middle", DOBONG_DONGS)

    # 동대문구 고등 + 중등
    print("동대문구 수정 중...")
    total_fixed += fix_district_titles("dongdaemun", "high", DONGDAEMUN_DONGS)
    total_fixed += fix_district_titles("dongdaemun", "middle", DONGDAEMUN_DONGS)

    # 금천구 중등만
    print("금천구 중등 수정 중...")
    total_fixed += fix_district_titles("geumcheon", "middle", GEUMCHEON_DONGS)

    # 강북구 중등만
    print("강북구 중등 수정 중...")
    total_fixed += fix_district_titles("gangbuk", "middle", GANGBUK_DONGS)

    # 구로구 중등만
    print("구로구 중등 수정 중...")
    total_fixed += fix_district_titles("guro", "middle", GURO_DONGS)

    print(f"\n총 {total_fixed}개 파일 수정 완료")

if __name__ == "__main__":
    main()
