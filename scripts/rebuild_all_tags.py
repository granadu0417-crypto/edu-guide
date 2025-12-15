#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
모든 파일의 tags 배열 재구성
"""

import os
import re
from pathlib import Path

def rebuild_tags(content):
    """tags 배열 완전히 재구성"""
    lines = content.split('\n')
    fixed_lines = []
    modified = False

    for line in lines:
        if line.strip().startswith('tags:'):
            # 모든 따옴표로 둘러싸인 텍스트 추출
            all_matches = re.findall(r'"([^"]+)"', line)

            if all_matches:
                # 빈 문자열 제거
                valid_tags = [tag.strip() for tag in all_matches if tag.strip() and tag.strip() != '"]']

                # 새로운 tags 라인 생성
                new_tags_str = ', '.join([f'"{tag}"' for tag in valid_tags])
                new_line = f'tags: [{new_tags_str}]'

                if new_line != line:
                    fixed_lines.append(new_line)
                    modified = True
                else:
                    fixed_lines.append(line)
            else:
                fixed_lines.append(line)
        else:
            fixed_lines.append(line)

    return '\n'.join(fixed_lines), modified

def fix_file(file_path):
    """파일 수정"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        new_content, modified = rebuild_tags(content)

        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True

        return False

    except Exception as e:
        print(f"  ❌ 처리 실패: {e}")
        return False

def main():
    """메인 실행 함수"""
    content_dir = Path('content')

    if not content_dir.exists():
        print("❌ content 디렉토리를 찾을 수 없습니다.")
        return

    md_files = list(content_dir.rglob('*.md'))

    print(f"🔍 총 {len(md_files)}개 파일 tags 재구성 시작...\n")

    fixed_count = 0

    for md_file in md_files:
        if fix_file(md_file):
            fixed_count += 1
            print(f"✅ {md_file.name}")

    print(f"\n{'='*60}")
    print(f"✅ tags 배열 재구성 완료!")
    print(f"{'='*60}")
    print(f"수정된 파일: {fixed_count}개")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
