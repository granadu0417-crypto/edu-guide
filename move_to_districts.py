#!/usr/bin/env python3
"""
동별 콘텐츠를 각 구 폴더로 이동
/middle/gangnam-daechi1-middle-math.md → /seoul/gangnam/daechi1-middle-math.md
/high/gangnam-daechi1-high-math.md → /seoul/gangnam/daechi1-high-math.md
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

BASE_PATH = '/home/user/edu-guide/content'

def add_alias_to_file(filepath, old_url):
    """파일에 alias 추가 (기존 URL 리다이렉트용)"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 이미 aliases가 있는지 확인
    if 'aliases:' in content:
        # 이미 이 alias가 있는지 확인
        if old_url not in content:
            content = re.sub(
                r'(aliases:\n)',
                f'\\1  - {old_url}\n',
                content
            )
    else:
        # aliases 섹션 새로 추가
        content = re.sub(
            r'(---\n)',
            f'---\naliases:\n  - {old_url}\n',
            content,
            count=1
        )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def move_district_files(source_folder, folder_type):
    """
    source_folder: 'middle' or 'high'
    folder_type: 'middle' or 'high' (for URL)
    """
    source_path = os.path.join(BASE_PATH, source_folder)
    moved_count = 0
    skipped_count = 0

    for filename in os.listdir(source_path):
        if not filename.endswith('.md'):
            continue
        if filename == '_index.md':
            continue

        # 구 이름으로 시작하는 파일 찾기
        matched_district = None
        for district in DISTRICTS:
            if filename.startswith(f'{district}-'):
                matched_district = district
                break

        if not matched_district:
            skipped_count += 1
            continue

        # 새 파일명 (구 이름 제거)
        new_filename = filename[len(matched_district)+1:]  # "gangnam-" 제거

        # 목적지 경로
        dest_dir = os.path.join(BASE_PATH, 'seoul', matched_district)
        dest_path = os.path.join(dest_dir, new_filename)

        # 원본 경로
        source_file = os.path.join(source_path, filename)

        # 기존 URL (리다이렉트용)
        old_url = f'/{source_folder}/{filename[:-3]}/'

        # 파일 이동
        if os.path.exists(dest_path):
            # 이미 존재하면 alias만 추가
            add_alias_to_file(dest_path, old_url)
            os.remove(source_file)
        else:
            shutil.move(source_file, dest_path)
            # 새 위치에서 alias 추가
            add_alias_to_file(dest_path, old_url)

        moved_count += 1

    return moved_count, skipped_count

def main():
    print("=== 동별 콘텐츠 이동 시작 ===\n")

    # middle 폴더 처리
    print("Processing /middle/ folder...")
    moved, skipped = move_district_files('middle', 'middle')
    print(f"  이동: {moved}개, 스킵(일반 가이드): {skipped}개")

    # high 폴더 처리
    print("\nProcessing /high/ folder...")
    moved, skipped = move_district_files('high', 'high')
    print(f"  이동: {moved}개, 스킵(일반 가이드): {skipped}개")

    # 결과 확인
    print("\n=== 구별 파일 수 확인 ===")
    for district in sorted(DISTRICTS):
        district_path = os.path.join(BASE_PATH, 'seoul', district)
        if os.path.exists(district_path):
            count = len([f for f in os.listdir(district_path) if f.endswith('.md')])
            print(f"  {district}: {count}개")

    print("\n완료!")

if __name__ == '__main__':
    main()
