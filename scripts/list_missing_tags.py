#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
태그가 없는 파일 목록 확인
"""

from pathlib import Path
import re
import yaml

def extract_front_matter(content):
    """YAML front matter 추출"""
    if not content.startswith('---'):
        return None

    parts = content.split('---', 2)
    if len(parts) < 3:
        return None

    try:
        return yaml.safe_load(parts[1])
    except:
        return None

def main():
    content_dir = Path('content')
    missing_tags = []

    for md_file in content_dir.rglob('*.md'):
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()

            front_matter = extract_front_matter(content)
            if not front_matter:
                continue

            # tags 필드가 없거나 비어있는 경우
            tags = front_matter.get('tags', [])
            if not tags or len(tags) == 0:
                rel_path = str(md_file.relative_to(content_dir))
                category = rel_path.split('/')[0]
                missing_tags.append((rel_path, category))

        except Exception as e:
            pass

    # 정렬 및 출력
    missing_tags.sort()

    print(f"🏷️  태그 없는 파일: {len(missing_tags)}개\n")

    # 카테고리별 분류
    categories = {}
    for file_path, category in missing_tags:
        if category not in categories:
            categories[category] = []
        categories[category].append(file_path)

    # 카테고리별 통계
    print("=" * 80)
    print("📊 카테고리별 통계")
    print("=" * 80)

    for category in sorted(categories.keys()):
        files = categories[category]
        print(f"{category:15s}: {len(files):3d}개")
        # 처음 3개만 샘플로 표시
        for file_path in files[:3]:
            print(f"  - {file_path}")
        if len(files) > 3:
            print(f"  ... 외 {len(files) - 3}개")

    print("=" * 80)

if __name__ == '__main__':
    main()
