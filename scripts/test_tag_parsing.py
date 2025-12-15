#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
태그 파싱 테스트 스크립트
"""

from pathlib import Path
import re

def test_file(file_path):
    """파일의 태그 파싱 테스트"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Front matter 추출
    if not content.startswith('---'):
        print(f"❌ {file_path.name}: No front matter")
        return

    parts = content.split('---', 2)
    if len(parts) < 3:
        print(f"❌ {file_path.name}: Invalid front matter")
        return

    front_matter = parts[1]

    print(f"\n📄 {file_path.name}")
    print(f"   Front matter length: {len(front_matter)} chars")

    # tags 위치 찾기
    tags_pos = front_matter.find('tags:')
    if tags_pos == -1:
        print(f"   ❌ 'tags:' not found in front matter")
        return

    print(f"   'tags:' found at position {tags_pos}")
    print(f"   Context: {repr(front_matter[tags_pos:tags_pos+100])}")

    # 원본 방식 (문제 있음)
    tags_match = re.search(r'^tags:(.*?)(?=\n[a-z_]+:|$)', front_matter, re.MULTILINE | re.DOTALL)
    if tags_match:
        print(f"   [원본] Captured: {repr(tags_match.group(1)[:50])} (length: {len(tags_match.group(1))})")
    else:
        print(f"   [원본] ❌ No match")

    # 개선 방식 1: 다음 YAML 키까지 모두 캡처
    tags_match2 = re.search(r'^tags:\s*\n((?:- .+\n)+)', front_matter, re.MULTILINE)
    if tags_match2:
        print(f"   [방식1] Captured: {repr(tags_match2.group(1)[:50])} (length: {len(tags_match2.group(1))})")
    else:
        print(f"   [방식1] ❌ No match")

    # 개선 방식 2: featured_image가 나올 때까지
    tags_match3 = re.search(r'tags:\s*\n(.*?)\nfeatured_image:', front_matter, re.DOTALL)
    if tags_match3:
        tags_content = tags_match3.group(1)
        print(f"   [방식2] Captured: {repr(tags_content[:50])} (length: {len(tags_content)})")
    else:
        print(f"   [방식2] ❌ No match")

    # 방식2로 태그 카운트 (가장 정확)
    if tags_match3:
        tags_content = tags_match3.group(1)
        tag_count = len(re.findall(r'^-\s+', tags_content, re.MULTILINE))
        print(f"   [방식2] Tag count: {tag_count}")

        # 실제 태그 출력
        tags = re.findall(r'^-\s+(.+)$', tags_content, re.MULTILINE)
        print(f"   [방식2] Tags: {tags[:5]}")  # 처음 5개만

# 테스트 파일들
test_files = [
    Path('content/consultation/consultation-guide-1.md'),
    Path('content/elementary/elem-b9-1.md'),
    Path('content/elementary/_index.md'),
]

print("🔍 태그 파싱 테스트\n" + "=" * 60)

for file_path in test_files:
    if file_path.exists():
        test_file(file_path)
    else:
        print(f"⚠️  파일 없음: {file_path}")
