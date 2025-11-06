#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
잘못된 tags 배열 수정 스크립트
"""

import os
import re
from pathlib import Path

def fix_tags_array(content):
    """tags 배열 수정"""
    lines = content.split('\n')
    fixed_lines = []
    modified = False

    for i, line in enumerate(lines):
        if line.startswith('tags:'):
            # 잘못된 패턴 찾기: 닫히지 않은 따옴표
            if ', "' in line and not line.endswith(']'):
                # tags 라인이 malformed되어 있음
                # 모든 키워드를 추출하고 재구성
                match = re.search(r'tags:\s*\[(.+)', line)
                if match:
                    tags_content = match.group(1)

                    # 모든 따옴표로 둘러싸인 텍스트 추출
                    all_tags = re.findall(r'"([^"]+)"', tags_content)

                    # 유효한 tags만 필터링
                    valid_tags = [tag for tag in all_tags if tag and not tag.endswith(',')]

                    # 새로운 tags 라인 생성
                    new_tags_str = ', '.join([f'"{tag}"' for tag in valid_tags])
                    new_line = f'tags: [{new_tags_str}]'

                    fixed_lines.append(new_line)
                    modified = True
                    print(f"  수정: tags 배열 재구성")
                    print(f"    {len(valid_tags)}개 태그")
                    continue

        fixed_lines.append(line)

    return '\n'.join(fixed_lines), modified

def fix_file(file_path):
    """파일 수정"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        new_content, modified = fix_tags_array(content)

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

    print(f"🔍 총 {len(md_files)}개 파일 검사 시작...\n")

    fixed_count = 0

    for md_file in md_files:
        print(f"검사: {md_file.name}")

        if fix_file(md_file):
            fixed_count += 1
            print(f"  ✅ 수정 완료")
        else:
            print(f"  ⏭️  변경 없음")

    print(f"\n{'='*60}")
    print(f"✅ tags 배열 수정 완료!")
    print(f"{'='*60}")
    print(f"수정된 파일: {fixed_count}개")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
