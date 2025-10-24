#!/usr/bin/env python3
"""
Front matter 안에 잘못 들어간 CTA 쇼트코드를 제거하는 스크립트
"""

import os
import re
from pathlib import Path

def fix_yaml_in_file(file_path):
    """파일의 front matter에서 CTA 쇼트코드 제거"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        lines = content.split('\n')

        # Front matter 범위 찾기
        front_matter_end = -1
        dash_count = 0

        for i, line in enumerate(lines):
            if line.strip() == '---':
                dash_count += 1
                if dash_count == 2:
                    front_matter_end = i
                    break

        if front_matter_end == -1:
            print(f"⏭️  {file_path.name} - front matter를 찾을 수 없음")
            return False

        # Front matter 내에 CTA가 있는지 확인
        has_cta_in_front_matter = False
        fixed_lines = []

        for i, line in enumerate(lines):
            if i < front_matter_end:
                # Front matter 안
                if '{{<' in line and 'cta-consultation' in line:
                    # CTA 쇼트코드 라인은 제거
                    has_cta_in_front_matter = True
                    continue
            fixed_lines.append(line)

        if has_cta_in_front_matter:
            # 파일 다시 쓰기
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(fixed_lines))
            print(f"✅ {file_path.name} - front matter에서 CTA 제거")
            return True
        else:
            print(f"⏭️  {file_path.name} - 문제 없음")
            return False

    except Exception as e:
        print(f"❌ {file_path.name} - 에러: {e}")
        return False

def main():
    """메인 실행 함수"""
    print("=" * 60)
    print("Front matter YAML 에러 수정 시작")
    print("=" * 60)
    print()

    content_dir = Path('/mnt/c/Users/user/Desktop/edu-guide/content')

    # 모든 .md 파일 찾기
    all_md_files = list(content_dir.rglob('*.md'))

    fixed = 0
    skipped = 0

    for md_file in all_md_files:
        result = fix_yaml_in_file(md_file)
        if result:
            fixed += 1
        else:
            skipped += 1

    print()
    print("=" * 60)
    print("작업 완료")
    print("=" * 60)
    print(f"✅ 수정 완료: {fixed}개")
    print(f"⏭️  스킵: {skipped}개")
    print()

if __name__ == '__main__':
    main()
