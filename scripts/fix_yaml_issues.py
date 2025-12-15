#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YAML 문법 오류 수정 스크립트
- 태그 배열 끝의 여분 ]" 제거
- 빈 keywords 배열 제거
"""

import os
import re
from pathlib import Path

def fix_yaml_issues(content):
    """YAML 문법 오류 수정"""
    lines = content.split('\n')
    fixed_lines = []
    modified = False
    in_front_matter = False
    front_matter_count = 0

    for i, line in enumerate(lines):
        # Front Matter 경계 확인
        if line.strip() == '---':
            front_matter_count += 1
            in_front_matter = front_matter_count == 1
            fixed_lines.append(line)
            continue

        # Front Matter 외부는 그대로 유지
        if not in_front_matter:
            fixed_lines.append(line)
            continue

        # tags 라인에서 여분의 ]" 제거
        if line.strip().startswith('tags:'):
            # ]"] 패턴을 ] 로 변경
            if '"]"]' in line:
                fixed_line = line.replace('"]"]', '"]')
                if fixed_line != line:
                    modified = True
                    print(f"  수정: tags 배열 끝 정리")
                fixed_lines.append(fixed_line)
            else:
                fixed_lines.append(line)
            continue

        # 빈 keywords 라인 제거
        if line.strip().startswith('keywords:'):
            if '[""]' in line or ': []' in line:
                modified = True
                print(f"  제거: 빈 keywords 배열")
                continue  # 이 라인 건너뛰기
            else:
                fixed_lines.append(line)
                continue

        # 나머지 라인은 그대로
        fixed_lines.append(line)

    return '\n'.join(fixed_lines), modified

def fix_file(file_path):
    """파일의 YAML 문제 수정"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        new_content, modified = fix_yaml_issues(content)

        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"✅ {file_path.relative_to(Path('content'))}")
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
    print(f"✅ YAML 문제 수정 완료!")
    print(f"📊 수정된 파일: {fixed_count}개")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
