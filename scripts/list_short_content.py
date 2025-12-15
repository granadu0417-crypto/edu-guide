#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
짧은 콘텐츠 파일 목록 추출
"""

from pathlib import Path
import re

def count_words(content):
    """마크다운 콘텐츠의 단어 수 계산"""
    # Front matter 제거
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            content = parts[2]

    # 마크다운 문법 제거
    content = re.sub(r'#+ ', '', content)  # 헤딩
    content = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', content)  # 링크
    content = re.sub(r'[*_`]', '', content)  # 강조
    content = re.sub(r'{{<.*?>}}', '', content)  # Shortcodes

    # 단어 수 계산 (한글 + 영문)
    korean_chars = len(re.findall(r'[가-힣]', content))
    english_words = len(re.findall(r'\b[a-zA-Z]+\b', content))

    # 한글 2자 = 영문 1단어로 계산
    return (korean_chars // 2) + english_words

def main():
    content_dir = Path('content')
    short_files = []

    for md_file in content_dir.rglob('*.md'):
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()

            word_count = count_words(content)

            if word_count < 200:
                rel_path = str(md_file.relative_to(content_dir))
                short_files.append((rel_path, word_count))

        except Exception as e:
            pass

    # 정렬 및 출력
    short_files.sort(key=lambda x: x[1])  # 단어 수로 정렬

    print(f"📏 짧은 콘텐츠 파일 (< 200 단어): {len(short_files)}개\n")

    for file_path, word_count in short_files:
        print(f"{word_count:3d} 단어 - {file_path}")

    # 카테고리별 통계
    print("\n" + "="*80)
    print("📊 카테고리별 통계")
    print("="*80)

    categories = {}
    for file_path, _ in short_files:
        category = file_path.split('/')[0]
        categories[category] = categories.get(category, 0) + 1

    for category, count in sorted(categories.items()):
        print(f"{category:15s}: {count:3d}개")

    print("="*80)

if __name__ == '__main__':
    main()
