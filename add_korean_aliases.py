#!/usr/bin/env python3
"""
한글 URL을 영문 URL로 리다이렉트하기 위한 aliases 추가 스크립트
/cities/강남구/ → /seoul/gangnam/ 등
"""

import os
import re

# 한글 → 영문 매핑
DISTRICT_MAP = {
    '강남구': 'gangnam',
    '강동구': 'gangdong',
    '강북구': 'gangbuk',
    '강서구': 'gangseo',
    '관악구': 'gwanak',
    '광진구': 'gwangjin',
    '구로구': 'guro',
    '금천구': 'geumcheon',
    '노원구': 'nowon',
    '도봉구': 'dobong',
    '동대문구': 'dongdaemun',
    '동작구': 'dongjak',
    '마포구': 'mapo',
    '서대문구': 'seodaemun',
    '서초구': 'seocho',
    '성동구': 'seongdong',
    '성북구': 'seongbuk',
    '송파구': 'songpa',
    '양천구': 'yangcheon',
    '영등포구': 'yeongdeungpo',
    '용산구': 'yongsan',
    '은평구': 'eunpyeong',
    '종로구': 'jongno',
    '중구': 'jung',
    '중랑구': 'jungnang',
}

def add_alias_to_file(filepath, alias):
    """파일에 alias 추가"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 이미 aliases가 있는지 확인
    if 'aliases:' in content:
        # aliases 섹션에 추가
        if alias not in content:
            content = re.sub(
                r'(aliases:\n)',
                f'\\1  - {alias}\n',
                content
            )
    else:
        # aliases 섹션 새로 추가 (date: 다음 줄에)
        content = re.sub(
            r'(date: [^\n]+\n)',
            f'\\1aliases:\n  - {alias}\n',
            content
        )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return True

def main():
    base_path = '/home/user/edu-guide/content/seoul'
    updated = 0

    for korean, english in DISTRICT_MAP.items():
        index_file = os.path.join(base_path, english, '_index.md')
        alias = f'/cities/{korean}/'

        if os.path.exists(index_file):
            if add_alias_to_file(index_file, alias):
                print(f"✓ {english}/_index.md: alias {alias} 추가됨")
                updated += 1
        else:
            print(f"✗ {index_file} 파일 없음")

    print(f"\n총 {updated}개 파일 업데이트 완료")

if __name__ == '__main__':
    main()
