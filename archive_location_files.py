#!/usr/bin/env python3
"""
지역 기반 콘텐츠 파일을 아카이브 폴더로 이동
새 URL 구조의 aliases와 충돌 방지
"""

import os
import shutil
import re

# 서울 25개 구 영문명
DISTRICTS = [
    'gangnam', 'gangdong', 'gangbuk', 'gangseo', 'gwanak', 'gwangjin',
    'guro', 'geumcheon', 'nowon', 'dobong', 'dongdaemun', 'dongjak',
    'mapo', 'seodaemun', 'seocho', 'seongdong', 'seongbuk', 'songpa',
    'yangcheon', 'yeongdeungpo', 'yongsan', 'eunpyeong', 'jongno', 'jung', 'jungnang'
]

def is_location_file(filename):
    """지역 기반 파일인지 확인"""
    # _index.md는 제외
    if filename == '_index.md':
        return False

    # 구 이름으로 시작하는 파일 확인
    for district in DISTRICTS:
        if filename.startswith(f'{district}-'):
            return True
    return False

def move_location_files(source_folder, archive_folder):
    """지역 기반 파일들을 아카이브로 이동"""
    moved = 0
    kept = 0

    for filename in os.listdir(source_folder):
        if not filename.endswith('.md'):
            continue

        source_path = os.path.join(source_folder, filename)

        if is_location_file(filename):
            archive_path = os.path.join(archive_folder, filename)
            shutil.move(source_path, archive_path)
            moved += 1
        else:
            kept += 1

    return moved, kept

def main():
    base = '/home/user/edu-guide/content'

    # middle 폴더 처리
    print("=== /middle/ 폴더 처리 ===")
    moved, kept = move_location_files(
        f'{base}/middle',
        f'{base}/_archive/middle'
    )
    print(f"이동: {moved}개, 유지: {kept}개")

    # high 폴더 처리
    print("\n=== /high/ 폴더 처리 ===")
    moved, kept = move_location_files(
        f'{base}/high',
        f'{base}/_archive/high'
    )
    print(f"이동: {moved}개, 유지: {kept}개")

    print("\n완료!")

if __name__ == '__main__':
    main()
