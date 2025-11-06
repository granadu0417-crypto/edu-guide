#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
가격 정보 자동 제거 스크립트
모든 마크다운 파일에서 가격 관련 정보를 찾아 제거합니다.
"""

import os
import re
from pathlib import Path

# 가격 관련 패턴들
PRICE_PATTERNS = [
    # 숫자 + 원/만원
    r'\d+[\.,]?\d*\s*원',
    r'\d+[\.,]?\d*\s*만\s*원',
    r'월\s*\d+[\.,]?\d*\s*원',
    r'시간당\s*\d+[\.,]?\d*\s*원',
    r'회당\s*\d+[\.,]?\d*\s*원',

    # 달러 표기
    r'\$\s*\d+[\.,]?\d*',

    # 한글로 된 가격 표현
    r'[일이삼사오육칠팔구십백천만억]+\s*원',

    # 가격 범위
    r'\d+[\.,]?\d*\s*~\s*\d+[\.,]?\d*\s*원',
    r'\d+[\.,]?\d*\s*-\s*\d+[\.,]?\d*\s*원',

    # 비용/요금 관련
    r'비용[:\s]*\d+[\.,]?\d*\s*원',
    r'요금[:\s]*\d+[\.,]?\d*\s*원',
    r'수강료[:\s]*\d+[\.,]?\d*\s*원',
    r'등록비[:\s]*\d+[\.,]?\d*\s*원',
    r'수업료[:\s]*\d+[\.,]?\d*\s*원',

    # 가격대 언급
    r'[저중고]가[\s]*\(\d+[\.,]?\d*\s*원\)',
    r'약\s*\d+[\.,]?\d*\s*원',
    r'대략\s*\d+[\.,]?\d*\s*원',
    r'평균\s*\d+[\.,]?\d*\s*원',
]

# 가격 관련 문장 패턴 (전체 문장 제거)
PRICE_SENTENCE_PATTERNS = [
    r'.*가격은.*원.*\n?',
    r'.*비용은.*원.*\n?',
    r'.*요금은.*원.*\n?',
    r'.*\d+만원.*부터.*\n?',
    r'.*월\s*\d+.*정도.*\n?',
]

def remove_price_info(content):
    """가격 정보를 제거하고 개선된 텍스트 반환"""
    original_content = content
    removed_count = 0

    # 패턴별로 제거
    for pattern in PRICE_PATTERNS:
        matches = re.findall(pattern, content, re.IGNORECASE)
        if matches:
            removed_count += len(matches)
            content = re.sub(pattern, '[개별 문의 필요]', content, flags=re.IGNORECASE)

    # 가격 관련 문장 전체 제거
    for pattern in PRICE_SENTENCE_PATTERNS:
        matches = re.findall(pattern, content, re.MULTILINE | re.IGNORECASE)
        if matches:
            removed_count += len(matches)
            content = re.sub(pattern, '', content, flags=re.MULTILINE | re.IGNORECASE)

    # 연속된 빈 줄 정리
    content = re.sub(r'\n{3,}', '\n\n', content)

    return content, removed_count

def process_markdown_file(file_path):
    """마크다운 파일 처리"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        new_content, removed_count = remove_price_info(content)

        if removed_count > 0:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"✅ {file_path.name}: {removed_count}개 가격 정보 제거")
            return removed_count
        else:
            return 0

    except Exception as e:
        print(f"❌ {file_path.name} 처리 중 오류: {e}")
        return 0

def main():
    """메인 실행 함수"""
    content_dir = Path('content')

    if not content_dir.exists():
        print("❌ content 디렉토리를 찾을 수 없습니다.")
        return

    # 모든 마크다운 파일 찾기
    md_files = list(content_dir.rglob('*.md'))

    print(f"📁 총 {len(md_files)}개 파일 검사 시작...\n")

    total_removed = 0
    processed_files = 0

    for md_file in md_files:
        removed = process_markdown_file(md_file)
        if removed > 0:
            processed_files += 1
            total_removed += removed

    print(f"\n{'='*60}")
    print(f"✅ 작업 완료!")
    print(f"📊 처리된 파일: {processed_files}개")
    print(f"🗑️  제거된 가격 정보: {total_removed}개")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
