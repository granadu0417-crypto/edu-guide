#!/usr/bin/env python3
"""
기존 콘텐츠 파일에 CTA 쇼트코드를 자동으로 추가하는 스크립트
"""

import os
import re
from pathlib import Path

# 제외할 파일 목록 (이미 CTA가 있는 Phase 1 신규 글)
EXCLUDE_FILES = {
    'content/elementary/study-habits-formation.md',
    'content/middle/self-directed-learning-complete-guide.md',
    'content/high/suneung-d100-strategy.md',
    'content/subjects/korean-reading-improvement.md',
    'content/tutoring/private-tutor-selection-guide.md',
}

# CTA 쇼트코드
CTA_MIDDLE = '\n\n{{< cta-consultation message="맞춤 학습 전략이 필요하신가요?" >}}\n\n'
CTA_FINAL = '\n\n{{< cta-consultation-final >}}\n\n'

def should_process_file(file_path):
    """파일을 처리해야 하는지 확인"""
    # 상대 경로로 변환
    rel_path = str(file_path)

    # 제외 목록에 있는지 확인
    if any(rel_path.endswith(excluded) for excluded in EXCLUDE_FILES):
        return False

    # _index.md 파일은 제외
    if file_path.name == '_index.md':
        return False

    # consultation/_index.md도 제외
    if 'consultation' in str(file_path):
        return False

    return True

def already_has_cta(content):
    """이미 CTA 쇼트코드가 있는지 확인"""
    return 'cta-consultation' in content

def find_middle_position(lines):
    """글의 중간 지점 찾기 (본문의 50% 지점)"""
    # Front matter 이후 시작
    content_start = 0
    in_front_matter = False
    front_matter_count = 0

    for i, line in enumerate(lines):
        if line.strip() == '---':
            front_matter_count += 1
            if front_matter_count == 2:
                content_start = i + 1
                break

    # 본문만 카운트
    content_lines = lines[content_start:]

    # 이미지, 제목 등을 제외한 실제 본문 라인 찾기
    substantial_lines = []
    for i, line in enumerate(content_lines, start=content_start):
        line_stripped = line.strip()
        # 실질적인 본문 라인인지 확인
        if (line_stripped and
            not line_stripped.startswith('#') and
            not line_stripped.startswith('!') and
            not line_stripped.startswith('```') and
            not line_stripped.startswith('---') and
            not line_stripped.startswith('*') and
            len(line_stripped) > 50):  # 충분히 긴 라인만
            substantial_lines.append(i)

    if substantial_lines:
        # 중간 지점 반환
        middle_idx = len(substantial_lines) // 2
        return substantial_lines[middle_idx]

    # 대체: 전체 콘텐츠의 50% 지점
    total_lines = len(lines)
    return content_start + (total_lines - content_start) // 2

def find_end_position(lines):
    """글 끝 지점 찾기 (## 마무리 또는 --- 이전)"""
    # 뒤에서부터 검색
    for i in range(len(lines) - 1, -1, -1):
        line = lines[i].strip()

        # "마무리", "결론" 등의 섹션 찾기
        if line.startswith('##') and any(keyword in line for keyword in ['마무리', '결론', '정리', '요약']):
            return i

        # 맨 끝의 --- 또는 * 찾기
        if line == '---' or line.startswith('*본 글'):
            # 그 이전 위치 반환
            return i - 1

    # 못 찾으면 끝에서 10줄 전
    return max(0, len(lines) - 10)

def add_cta_to_file(file_path):
    """파일에 CTA 쇼트코드 추가"""
    try:
        # 파일 읽기
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 이미 CTA가 있으면 스킵
        if already_has_cta(content):
            print(f"⏭️  {file_path.name} - 이미 CTA 있음, 스킵")
            return False

        lines = content.split('\n')

        # 중간 위치와 끝 위치 찾기
        middle_pos = find_middle_position(lines)
        end_pos = find_end_position(lines)

        # CTA 삽입
        # 끝에 먼저 삽입 (인덱스가 변하지 않도록)
        lines.insert(end_pos, CTA_FINAL.strip())

        # 중간에 삽입
        lines.insert(middle_pos, CTA_MIDDLE.strip())

        # 파일 쓰기
        new_content = '\n'.join(lines)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print(f"✅ {file_path.name} - CTA 추가 완료 (중간: {middle_pos}줄, 끝: {end_pos}줄)")
        return True

    except Exception as e:
        print(f"❌ {file_path.name} - 에러: {e}")
        return False

def main():
    """메인 실행 함수"""
    print("=" * 60)
    print("기존 콘텐츠에 CTA 쇼트코드 자동 추가 시작")
    print("=" * 60)
    print()

    content_dir = Path('/mnt/c/Users/user/Desktop/edu-guide/content')

    # 모든 .md 파일 찾기
    all_md_files = list(content_dir.rglob('*.md'))

    processed = 0
    skipped = 0
    errors = 0

    for md_file in all_md_files:
        if should_process_file(md_file):
            result = add_cta_to_file(md_file)
            if result:
                processed += 1
            elif result is False and "이미 CTA" not in str(result):
                errors += 1
            else:
                skipped += 1
        else:
            print(f"⏭️  {md_file.name} - 제외 목록, 스킵")
            skipped += 1

    print()
    print("=" * 60)
    print("작업 완료")
    print("=" * 60)
    print(f"✅ 처리 완료: {processed}개")
    print(f"⏭️  스킵: {skipped}개")
    print(f"❌ 에러: {errors}개")
    print()

if __name__ == '__main__':
    main()
