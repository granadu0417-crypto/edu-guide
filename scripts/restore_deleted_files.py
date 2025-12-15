#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
삭제된 파일 복구 스크립트
ec4165e 커밋에서 삭제된 425개 파일을 복구
"""

import subprocess
import os
from pathlib import Path

def get_deleted_files(before_commit='ec4165e^', after_commit='ec4165e'):
    """삭제된 파일 목록 가져오기"""
    result = subprocess.run(
        ['git', 'diff', '--name-only', '--diff-filter=D', before_commit, after_commit],
        capture_output=True,
        text=True,
        encoding='utf-8'
    )

    deleted_files = [f.strip() for f in result.stdout.split('\n') if f.strip() and f.startswith('content/')]
    return deleted_files

def restore_file(file_path, commit='ec4165e^'):
    """Git에서 파일 복구"""
    try:
        # 디렉토리 생성
        dir_path = Path(file_path).parent
        dir_path.mkdir(parents=True, exist_ok=True)

        # Git에서 파일 내용 가져오기
        result = subprocess.run(
            ['git', 'show', f'{commit}:{file_path}'],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )

        if result.returncode == 0:
            # 파일 쓰기
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(result.stdout)
            return True
        else:
            print(f"  ⚠️ Git 조회 실패: {result.stderr}")
            return False

    except Exception as e:
        print(f"  ❌ 복구 실패: {e}")
        return False

def main():
    """메인 실행 함수"""
    print("🔍 삭제된 파일 목록 조회 중...\n")

    deleted_files = get_deleted_files()

    print(f"📊 총 {len(deleted_files)}개 파일이 삭제되었습니다.\n")

    # 카테고리별 분류
    from collections import defaultdict
    categories = defaultdict(list)

    for f in deleted_files:
        parts = f.split('/')
        if len(parts) >= 2:
            cat = parts[1]
            categories[cat].append(f)

    print("="*80)
    print("📁 카테고리별 삭제된 파일 수")
    print("="*80)
    for cat in sorted(categories.keys()):
        print(f"{cat}: {len(categories[cat])}개")

    print(f"\n{'='*80}")

    # 복구 시작
    answer = input("\n파일들을 복구하시겠습니까? (yes/no): ")

    if answer.lower() not in ['yes', 'y']:
        print("복구를 취소했습니다.")
        return

    print(f"\n{'='*80}")
    print("🔄 파일 복구 시작...")
    print("="*80 + "\n")

    restored_count = 0
    failed_count = 0

    for i, file_path in enumerate(deleted_files, 1):
        print(f"[{i}/{len(deleted_files)}] {file_path}")

        if restore_file(file_path):
            restored_count += 1
            print(f"  ✅ 복구 완료")
        else:
            failed_count += 1
            print(f"  ❌ 복구 실패")

        # 진행 상황 표시
        if i % 50 == 0:
            print(f"\n진행률: {i}/{len(deleted_files)} ({i/len(deleted_files)*100:.1f}%)\n")

    print(f"\n{'='*80}")
    print("✅ 파일 복구 완료!")
    print("="*80)
    print(f"성공: {restored_count}개")
    print(f"실패: {failed_count}개")
    print(f"총: {len(deleted_files)}개")
    print("="*80)

if __name__ == '__main__':
    main()
