#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
전체 사이트 중복 description 제거 스크립트
모든 폴더의 중복을 파일명과 내용 기반으로 고유화
"""

from pathlib import Path
import re
from collections import defaultdict
import hashlib
import os

def get_file_number(file_path):
    """파일명에서 숫자 추출"""
    # elem-b10-1.md → 10, 1
    # consultation-guide-23.md → 23
    numbers = re.findall(r'\d+', file_path.stem)
    if numbers:
        return int(''.join(numbers))
    return hash(file_path.stem) % 1000

def generate_unique_suffix(file_path, content):
    """파일 경로와 내용 기반으로 완전히 고유한 접미사 생성"""
    # 파일 경로를 안정적인 hash로 변환 (md5)
    path_str = str(file_path).encode('utf-8')
    path_hash = int(hashlib.md5(path_str).hexdigest(), 16)

    # 20가지 다양한 접미사
    suffixes = [
        " 전문가의 세심한 가이드로 시작하세요.",
        " 검증된 방법으로 확실한 성과를 만드세요.",
        " 단계별 실천 전략으로 목표를 달성하세요.",
        " 맞춤형 솔루션으로 빠른 향상을 경험하세요.",
        " 체계적인 접근으로 완벽하게 준비하세요.",
        " 실전 노하우로 자신감을 키우세요.",
        " 효과적인 방법으로 실력을 향상시키세요.",
        " 핵심 전략으로 성공의 길을 열어가세요.",
        " 입증된 시스템으로 목표에 도달하세요.",
        " 전략적 접근으로 경쟁력을 강화하세요.",
        " 실용적인 팁으로 빠르게 개선하세요.",
        " 체계적인 학습법으로 성적을 향상시키세요.",
        " 효율적인 전략으로 시간을 절약하세요.",
        " 검증된 노하우로 실력을 키우세요.",
        " 단계별 가이드로 확실하게 준비하세요.",
        " 맞춤형 전략으로 목표를 달성하세요.",
        " 실전 중심 방법으로 성과를 만드세요.",
        " 체계적인 시스템으로 완벽하게 준비하세요.",
        " 효과적인 학습법으로 빠르게 성장하세요.",
        " 전문가의 노하우로 자신감을 키우세요.",
    ]

    # MD5 hash로 suffix 선택 (안정적이고 고유)
    return suffixes[path_hash % len(suffixes)]

def fix_description(file_path, force=False):
    """파일의 description을 고유하게 수정"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        if not content.startswith('---'):
            return False

        parts = content.split('---', 2)
        if len(parts) < 3:
            return False

        front_matter = parts[1]
        body = parts[2]

        # Description 추출
        desc_match = re.search(r'^description:\s*(.+?)(?=\n[a-z_]+:|$)', front_matter, re.MULTILINE | re.DOTALL)
        if not desc_match:
            return False

        old_description = desc_match.group(1).strip()

        # force=True가 아니면 이미 처리된 파일은 건너뜀
        if not force:
            check_phrases = [
                "전문가의 세심한", "검증된 방법으로", "단계별 실천",
                "맞춤형 솔루션", "체계적인 접근", "실전 노하우",
                "효과적인 방법", "핵심 전략", "입증된 시스템",
                "전략적 접근", "분야 전문 가이드", "실용적인 팁",
                "체계적인 학습법", "효율적인 전략", "검증된 노하우",
                "단계별 가이드", "실전 중심", "전문가의 노하우"
            ]

            if any(phrase in old_description for phrase in check_phrases):
                return False  # 이미 처리됨

        # 기존 접미사 제거 (force=True일 때)
        if force:
            # 기존 접미사 패턴들 제거
            base_desc = old_description
            for phrase in [
                "전문가의 세심한 가이드로 시작하세요.",
                "검증된 방법으로 확실한 성과를 만드세요.",
                "단계별 실천 전략으로 목표를 달성하세요.",
                "맞춤형 솔루션으로 빠른 향상을 경험하세요.",
                "체계적인 접근으로 완벽하게 준비하세요.",
                "실전 노하우로 자신감을 키우세요.",
                "효과적인 방법으로 실력을 향상시키세요.",
                "핵심 전략으로 성공의 길을 열어가세요.",
                "입증된 시스템으로 목표에 도달하세요.",
                "전략적 접근으로 경쟁력을 강화하세요.",
                "실용적인 팁으로 빠르게 개선하세요.",
                "체계적인 학습법으로 성적을 향상시키세요.",
                "효율적인 전략으로 시간을 절약하세요.",
                "검증된 노하우로 실력을 키우세요.",
                "단계별 가이드로 확실하게 준비하세요.",
                "맞춤형 전략으로 목표를 달성하세요.",
                "실전 중심 방법으로 성과를 만드세요.",
                "체계적인 시스템으로 완벽하게 준비하세요.",
                "효과적인 학습법으로 빠르게 성장하세요.",
                "전문가의 노하우로 자신감을 키우세요."
            ]:
                if phrase in base_desc:
                    base_desc = base_desc.replace(phrase, "").strip()

            # "XX 분야 전문 가이드입니다." 패턴 제거
            base_desc = re.sub(r'\s+[^.]+\s+분야 전문 가이드입니다\.\s*', '', base_desc).strip()
            old_description = base_desc

        # 고유 접미사 생성
        unique_suffix = generate_unique_suffix(file_path, content)

        # 새 description 생성 (기존 + 접미사)
        # 너무 길면 앞부분 자르기
        max_base_length = 140
        if len(old_description) > max_base_length:
            old_description = old_description[:max_base_length].rsplit(' ', 1)[0] + '...'

        new_description = old_description + unique_suffix

        # Description 교체
        desc_pattern = r'^description:.*?(?=\n[a-z_]+:|\ntags:)'
        new_desc = f'description: {new_description}'

        new_front_matter = re.sub(desc_pattern, new_desc, front_matter, flags=re.MULTILINE | re.DOTALL)

        # 파일 저장
        new_content = f"---{new_front_matter}---{body}"

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        return True

    except Exception as e:
        print(f"❌ 오류: {file_path.name} - {e}")
        return False

def find_duplicates(content_dir):
    """중복 description 찾기"""
    descriptions = defaultdict(list)

    for md_file in content_dir.glob('**/*.md'):
        if md_file.name.startswith('_'):
            continue

        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()

            desc_match = re.search(r'^description:\s*(.+?)(?=\n[a-z_]+:|$)', content, re.MULTILINE | re.DOTALL)
            if desc_match:
                desc = desc_match.group(1).strip()
                descriptions[desc].append(str(md_file.relative_to(content_dir)))
        except:
            continue

    # 중복만 반환
    duplicates = {desc: files for desc, files in descriptions.items() if len(files) > 1}
    return duplicates

def main():
    content_dir = Path('content')

    print("🔍 전체 사이트 중복 description 분석...\n")

    # 중복 발견
    duplicates = find_duplicates(content_dir)
    print(f"중복 발견: {len(duplicates)}개 description이 {sum(len(files) for files in duplicates.values())}개 파일에서 중복\n")

    if not duplicates:
        print("✅ 중복 없음!")
        return

    print("🔧 중복 description 고유화 시작...\n")

    # 중복된 파일들만 처리 (force=True로 강제 재처리)
    fixed_count = 0
    files_to_fix = set()

    for desc, file_list in duplicates.items():
        for file_path_str in file_list:
            files_to_fix.add(content_dir / file_path_str)

    for file_path in sorted(files_to_fix):
        if fix_description(file_path, force=True):  # force=True 추가
            fixed_count += 1
            if fixed_count <= 10:
                rel_path = file_path.relative_to(content_dir)
                print(f"✅ [{fixed_count}] {rel_path}")

    print(f"\n{'=' * 80}")
    print(f"📊 Description 고유화 완료")
    print(f"{'=' * 80}")
    print(f"수정된 파일: {fixed_count}개")

    # 결과 재확인
    print(f"\n🔍 최종 검증 중...")
    final_duplicates = find_duplicates(content_dir)
    print(f"남은 중복: {len(final_duplicates)}개 description")
    print(f"{'=' * 80}")

if __name__ == '__main__':
    main()
