#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
카테고리별 깨진 featured_image 체크
"""

from pathlib import Path
import re
from collections import Counter

def extract_featured_image(file_path):
    """파일에서 featured_image URL 추출"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        if not content.startswith('---'):
            return None

        parts = content.split('---', 2)
        if len(parts) < 3:
            return None

        front_matter = parts[1]

        # Featured Image 추출
        img_match = re.search(r'^featured_image:\s*(.+)', front_matter, re.MULTILINE)
        if img_match:
            return img_match.group(1).strip()

        return None

    except Exception as e:
        return None

def check_image_url(url):
    """이미지 URL이 유효한지 체크 (기본 검증만)"""
    if not url or url == '':
        return False, "URL 없음"

    # 기본 URL 형식 체크
    if not url.startswith(('http://', 'https://', '/')):
        return False, f"잘못된 URL 형식: {url[:50]}"

    # Unsplash URL 형식 체크
    if 'unsplash.com' in url:
        if 'w=1200' not in url or 'h=630' not in url:
            return False, "Unsplash URL 파라미터 누락"

    return True, "정상"

def main():
    content_dir = Path('content')

    print("🖼️  카테고리별 이미지 상태 체크 시작...\n")

    category_stats = {}
    broken_files = {}

    categories = ['elementary', 'middle', 'high', 'exam', 'tutoring', 'consultation', 'local', 'subjects']

    for category in categories:
        category_path = content_dir / category
        if not category_path.exists():
            continue

        total = 0
        broken = 0
        no_image = 0
        broken_list = []

        for md_file in category_path.rglob('*.md'):
            total += 1

            img_url = extract_featured_image(md_file)

            if not img_url:
                no_image += 1
                broken += 1
                rel_path = str(md_file.relative_to(content_dir))
                broken_list.append((rel_path, "이미지 없음"))
                continue

            # URL 체크 (Unsplash만)
            is_valid, reason = check_image_url(img_url)

            if not is_valid:
                broken += 1
                rel_path = str(md_file.relative_to(content_dir))
                broken_list.append((rel_path, reason))

        category_stats[category] = {
            'total': total,
            'broken': broken,
            'no_image': no_image
        }

        if broken_list:
            broken_files[category] = broken_list

    # 출력
    print("=" * 80)
    print("📊 카테고리별 이미지 상태")
    print("=" * 80)

    total_files = 0
    total_broken = 0

    for category in sorted(category_stats.keys()):
        stats = category_stats[category]
        total_files += stats['total']
        total_broken += stats['broken']

        status = "✅" if stats['broken'] == 0 else "❌"
        print(f"{status} {category:15s}: 전체 {stats['total']:3d}개 | 깨진 이미지 {stats['broken']:3d}개 | 이미지 없음 {stats['no_image']:3d}개")

    print("=" * 80)
    print(f"합계: 전체 {total_files}개 | 깨진 이미지 {total_broken}개")
    print("=" * 80)

    # 깨진 파일 상세 출력
    if broken_files:
        print("\n❌ 깨진 이미지 파일 목록:\n")
        for category in sorted(broken_files.keys()):
            if broken_files[category]:
                print(f"\n📁 {category} ({len(broken_files[category])}개)")
                print("-" * 80)
                for file_path, reason in broken_files[category][:10]:  # 최대 10개만 표시
                    print(f"  - {file_path}")
                    print(f"    사유: {reason}")

                if len(broken_files[category]) > 10:
                    print(f"  ... 외 {len(broken_files[category]) - 10}개 더")

    print("\n" + "=" * 80)

if __name__ == '__main__':
    main()
