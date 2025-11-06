#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YAML Tags 배열 수정 스크립트
SEO 최적화 스크립트로 인한 중복 따옴표 제거
"""

import os
import re
from pathlib import Path

def fix_tags_line(line):
    """tags 라인의 중복 따옴표 수정"""
    if not line.startswith('tags:'):
        return line

    # 패턴: tags: ["["tag1"", ""tag2"", ...]", "other", ...]
    # 목표: tags: ["tag1", "tag2", ..., "other", ...]

    # 모든 이중 따옴표 제거
    fixed = line.replace('""', '"')

    # ["[ 패턴 제거
    fixed = re.sub(r'\["\[', '[', fixed)

    # ]" 패턴 제거 (배열 끝이 아닌 경우)
    fixed = re.sub(r'\]",\s*"', ', "', fixed)

    # 추가적인 정리
    fixed = re.sub(r'",\s*",', '", "', fixed)

    return fixed

def fix_file(file_path):
    """파일의 tags 라인 수정"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        modified = False
        new_lines = []

        for line in lines:
            if line.strip().startswith('tags:'):
                fixed_line = fix_tags_line(line)
                if fixed_line != line:
                    modified = True
                    print(f"  수정: {file_path.name}")
                    print(f"    이전: {line.strip()}")
                    print(f"    이후: {fixed_line.strip()}")
                new_lines.append(fixed_line)
            else:
                new_lines.append(line)

        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            return True

        return False

    except Exception as e:
        print(f"❌ {file_path.name} 처리 중 오류: {e}")
        return False

def main():
    """메인 실행 함수"""
    content_dir = Path('content')

    if not content_dir.exists():
        print("❌ content 디렉토리를 찾을 수 없습니다.")
        return

    md_files = list(content_dir.rglob('*.md'))

    print(f"📁 총 {len(md_files)}개 파일 검사 시작...\n")

    fixed_count = 0

    for md_file in md_files:
        if fix_file(md_file):
            fixed_count += 1

    print(f"\n{'='*60}")
    print(f"✅ Tags 배열 수정 완료!")
    print(f"📊 수정된 파일: {fixed_count}개")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
