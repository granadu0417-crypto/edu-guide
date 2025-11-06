#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hugo Shortcode 문법 오류 일괄 수정
{< shortcode >} → {{< shortcode >}}
"""

from pathlib import Path
import re

def fix_shortcodes(file_path):
    """파일의 shortcode 문법 수정"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # 먼저 잘못된 삼중/다중 괄호 수정: {{{< >}}} → {{< >}}
        content = re.sub(r'\{{3,}<\s*([^>]+?)\s*>\}{3,}', r'{{< \1 >}}', content)

        # 그 다음 단일 괄호 수정: {< >} → {{< >}} (이미 {{<는 제외)
        content = re.sub(r'(?<!\{)\{<\s*([^>]+?)\s*>\}(?!\})', r'{{< \1 >}}', content)

        # 변경사항이 있으면 저장
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            rel_path = str(file_path.relative_to(Path('content')))
            # 몇 개 수정되었는지 카운트
            count = len(re.findall(r'\{<\s*([^>]+)\s*>\}', original_content))
            return True, rel_path, count
        else:
            return False, None, 0

    except Exception as e:
        return False, None, 0

def main():
    content_dir = Path('content')

    fixed_count = 0
    total_shortcodes = 0
    fixed_files = []

    print("🔧 Shortcode 문법 수정 시작...\n")

    for md_file in content_dir.rglob('*.md'):
        success, file_path, count = fix_shortcodes(md_file)

        if success:
            fixed_count += 1
            total_shortcodes += count
            fixed_files.append((file_path, count))

            if fixed_count <= 10 or fixed_count % 50 == 0:
                print(f"✅ [{fixed_count}] {file_path} ({count}개 수정)")

    print("\n" + "=" * 80)
    print("📊 Shortcode 문법 수정 완료")
    print("=" * 80)
    print(f"수정된 파일  : {fixed_count}개")
    print(f"수정된 Shortcode: {total_shortcodes}개")

    # 카테고리별 통계
    category_stats = {}
    for file_path, count in fixed_files:
        category = file_path.split('/')[0]
        category_stats[category] = category_stats.get(category, 0) + count

    if category_stats:
        print("\n📂 카테고리별 통계:")
        for category in sorted(category_stats.keys()):
            print(f"  {category:15s}: {category_stats[category]:3d}개 수정")

    print("=" * 80)

if __name__ == '__main__':
    main()
