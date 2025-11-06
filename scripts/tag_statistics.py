#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
태그 통계 확인
"""

from pathlib import Path
import yaml
from collections import Counter

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

    all_tags = []
    files_with_tags = 0
    files_without_tags = 0
    tag_count_distribution = Counter()

    for md_file in content_dir.rglob('*.md'):
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()

            front_matter = extract_front_matter(content)
            if not front_matter:
                continue

            tags = front_matter.get('tags', [])
            if tags and len(tags) > 0:
                files_with_tags += 1
                all_tags.extend(tags)
                tag_count_distribution[len(tags)] += 1
            else:
                files_without_tags += 1

        except Exception as e:
            pass

    # 태그 빈도수 계산
    tag_frequency = Counter(all_tags)

    print("=" * 80)
    print("📊 태그 통계")
    print("=" * 80)
    print(f"총 파일 수         : {files_with_tags + files_without_tags}개")
    print(f"태그 있는 파일     : {files_with_tags}개")
    print(f"태그 없는 파일     : {files_without_tags}개")
    print(f"고유 태그 수       : {len(tag_frequency)}개")
    print(f"총 태그 사용 횟수  : {len(all_tags)}회")
    print(f"평균 태그 수/파일  : {len(all_tags)/files_with_tags:.1f}개" if files_with_tags > 0 else "N/A")

    print("\n" + "=" * 80)
    print("📈 파일당 태그 개수 분포")
    print("=" * 80)
    for count in sorted(tag_count_distribution.keys()):
        files = tag_count_distribution[count]
        print(f"{count}개 태그: {files:3d}개 파일")

    print("\n" + "=" * 80)
    print("🏆 가장 많이 사용된 태그 TOP 20")
    print("=" * 80)
    for tag, count in tag_frequency.most_common(20):
        print(f"{tag:20s}: {count:3d}회")

    print("=" * 80)

if __name__ == '__main__':
    main()
