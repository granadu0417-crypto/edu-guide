#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
전체 파일 구조 및 제목 분석 스크립트
Git 히스토리와 현재 파일 비교
"""

import subprocess
import re
from pathlib import Path
from collections import defaultdict

def get_title_from_content(content):
    """콘텐츠에서 title 추출"""
    match = re.search(r'title:\s*["\']([^"\']+)["\']', content)
    return match.group(1) if match else None

def get_original_title(file_path, commit='862fc5b'):
    """Git에서 원본 제목 가져오기"""
    try:
        result = subprocess.run(
            ['git', 'show', f'{commit}:{file_path}'],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        if result.returncode == 0:
            return get_title_from_content(result.stdout)
    except:
        pass
    return None

def get_current_title(file_path):
    """현재 제목 가져오기"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            return get_title_from_content(content)
    except:
        pass
    return None

def main():
    content_dir = Path('content')

    # 카테고리별 분류
    categories = defaultdict(list)

    print("📁 전체 파일 구조 분석 중...\n")

    for md_file in sorted(content_dir.rglob('*.md')):
        # 상대 경로
        rel_path = md_file.relative_to(Path('.'))

        # 카테고리 추출
        parts = md_file.parts
        if len(parts) >= 2:
            category = parts[1]

            # 원본 제목
            original_title = get_original_title(str(rel_path))

            # 현재 제목
            current_title = get_current_title(md_file)

            # 변경 여부
            changed = original_title != current_title if original_title else False

            categories[category].append({
                'file': md_file.name,
                'path': str(rel_path),
                'original': original_title,
                'current': current_title,
                'changed': changed
            })

    # 카테고리별 출력
    print("="*80)
    print("📊 카테고리별 파일 분석 결과")
    print("="*80)

    total_files = 0
    total_changed = 0

    for category in sorted(categories.keys()):
        files = categories[category]
        changed_count = sum(1 for f in files if f['changed'])
        total_files += len(files)
        total_changed += changed_count

        print(f"\n### {category.upper()} ({len(files)}개 파일, {changed_count}개 변경)")
        print("-" * 80)

        for i, file_info in enumerate(files[:5], 1):  # 각 카테고리당 처음 5개만
            print(f"{i}. {file_info['file']}")
            if file_info['original']:
                print(f"   원본: {file_info['original']}")
            if file_info['current']:
                print(f"   현재: {file_info['current']}")
            if file_info['changed']:
                print(f"   ⚠️  제목 변경됨!")
            print()

        if len(files) > 5:
            print(f"   ... 외 {len(files) - 5}개 파일")

    print("\n" + "="*80)
    print(f"📊 전체 요약")
    print("="*80)
    print(f"총 파일: {total_files}개")
    print(f"제목 변경된 파일: {total_changed}개")
    print(f"변경 비율: {total_changed/total_files*100:.1f}%")

    # 상세 분석 파일 저장
    print("\n💾 상세 분석 결과를 analysis_report.txt에 저장 중...")

    with open('analysis_report.txt', 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("전체 파일 제목 분석 리포트\n")
        f.write("="*80 + "\n\n")

        for category in sorted(categories.keys()):
            files = categories[category]
            f.write(f"\n### {category.upper()} ({len(files)}개)\n")
            f.write("-" * 80 + "\n")

            for file_info in files:
                f.write(f"\n파일: {file_info['path']}\n")
                if file_info['original']:
                    f.write(f"원본 제목: {file_info['original']}\n")
                if file_info['current']:
                    f.write(f"현재 제목: {file_info['current']}\n")
                if file_info['changed']:
                    f.write(f"상태: ⚠️ 제목 변경됨\n")
                f.write("\n")

    print("✅ 분석 완료! analysis_report.txt 확인하세요.")

if __name__ == '__main__':
    main()
