#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
콘텐츠 불일치 정확히 찾기
"""

from pathlib import Path
import re

def check_local_file(file_path):
    """지역 파일의 콘텐츠가 적절한지 체크"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Front matter 제거하고 본문만
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                body = parts[2]
            else:
                return False, "front matter 파싱 오류"
        else:
            body = content

        rel_path = str(file_path.relative_to(Path('content')))

        # 파일명에서 지역 추출
        filename = file_path.stem

        # 지역 과외 파일인데 일반적인 과목 학습법만 나열하는 경우 체크
        # 예: "## 📚 주요 과목 안내" 같은 섹션이 있으면 문제
        generic_subject_sections = [
            '## 📚 주요 과목 안내',
            '### 국어\n국어는 모든 학습의 기초',
            '### 수학\n수학은 논리적 사고력',
            '### 영어\n영어는 글로벌 시대',
            '### 과학\n과학은 자연 현상',
            '### 사회\n사회는 인간과 사회'
        ]

        has_generic = any(section in body for section in generic_subject_sections)

        if has_generic:
            return True, f"일반 과목 학습법 콘텐츠 발견 (지역 맞춤형 아님)"

        return False, "정상"

    except Exception as e:
        return False, f"오류: {e}"

def main():
    local_dir = Path('content/local')

    mismatched = []

    print("🔍 지역 파일 콘텐츠 불일치 검사...\n")

    for md_file in local_dir.rglob('*.md'):
        is_problem, message = check_local_file(md_file)

        if is_problem:
            rel_path = str(md_file.relative_to(Path('content')))
            mismatched.append((rel_path, message))
            print(f"⚠️  {rel_path}")
            print(f"    {message}\n")

    print("=" * 80)
    print(f"📊 총 {len(mismatched)}개 파일에 콘텐츠 불일치 발견")
    print("=" * 80)

    if mismatched:
        print("\n수정이 필요한 파일 목록:")
        for file_path, _ in mismatched:
            print(f"  - {file_path}")

if __name__ == '__main__':
    main()
