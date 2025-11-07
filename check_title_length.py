#!/usr/bin/env python3
"""
제목 길이 확인 스크립트
SEO 최적화: 40-60자 이상의 제목 찾기
"""

import os
import re
from pathlib import Path

def extract_title(filepath):
    """파일에서 title 추출"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        if not content.startswith('---'):
            return None

        parts = content.split('---', 2)
        if len(parts) < 3:
            return None

        frontmatter = parts[1]

        # Title 추출
        title_match = re.search(r'title:\s*(.+)', frontmatter)
        if title_match:
            title = title_match.group(1).strip().strip('"\'')
            return title

        return None

    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None

def main():
    """메인 함수"""
    content_path = Path("/mnt/c/Users/user/Desktop/클로드/에듀코리아/edu-guide/content")

    print("제목 길이 분석 중...\n")

    short_titles = []  # 40자 미만
    long_titles = []   # 60자 초과
    good_titles = []   # 40-60자

    for md_file in content_path.rglob('*.md'):
        if md_file.name == '_index.md':
            continue

        title = extract_title(md_file)
        if title:
            title_len = len(title)

            if title_len < 40:
                short_titles.append((str(md_file), title, title_len))
            elif title_len > 60:
                long_titles.append((str(md_file), title, title_len))
            else:
                good_titles.append((str(md_file), title, title_len))

    # 결과 출력
    print(f"📊 제목 길이 분석 결과\n")
    print(f"✅ 적절한 길이 (40-60자): {len(good_titles)}개")
    print(f"⚠️  너무 짧음 (<40자): {len(short_titles)}개")
    print(f"⚠️  너무 길음 (>60자): {len(long_titles)}개")
    print(f"\n총 페이지: {len(short_titles) + len(long_titles) + len(good_titles)}개\n")

    # 너무 짧은 제목 출력
    if short_titles:
        print("=" * 80)
        print(f"\n⚠️  너무 짧은 제목 ({len(short_titles)}개):\n")
        for filepath, title, length in sorted(short_titles, key=lambda x: x[2]):
            print(f"{length:2}자 | {title}")
            print(f"      파일: {filepath}\n")

    # 너무 긴 제목 출력
    if long_titles:
        print("=" * 80)
        print(f"\n⚠️  너무 긴 제목 ({len(long_titles)}개):\n")
        for filepath, title, length in sorted(long_titles, key=lambda x: -x[2]):
            print(f"{length:2}자 | {title}")
            print(f"      파일: {filepath}\n")

if __name__ == "__main__":
    main()
