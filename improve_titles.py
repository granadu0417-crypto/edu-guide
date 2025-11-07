#!/usr/bin/env python3
"""
제목 길이 개선 스크립트
SEO 최적화: 40자 미만 제목에 카테고리별 적절한 suffix 추가
"""

import os
import re
from pathlib import Path

# 카테고리별 suffix 템플릿
CATEGORY_SUFFIXES = {
    'tutoring': [
        ' - 효과적인 1:1 맞춤 학습 전략',
        ' 완벽 가이드 - 학원비 절약하는 선택 방법',
        ' 상세 안내 - 성공적인 과외 활용법',
    ],
    'academy': [
        ' 완벽 가이드 - 성공적인 학원 선택과 활용법',
        ' - 효과적인 학원 활용 전략',
        ' 상세 안내 - 학원 선택부터 성적 향상까지',
    ],
    'guide': [
        ' 상세 가이드 - 체계적인 학습 전략과 실전 팁',
        ' 완벽 안내 - 성공적인 학습법과 노하우',
        ' - 효과적인 공부법과 성적 향상 비법',
    ],
    'exam': [
        ' 완벽 대비 가이드 - 합격을 위한 전략과 공부법',
        ' - 효과적인 시험 준비 전략',
        ' 상세 안내 - 고득점을 위한 학습법',
    ],
    'subject': [
        ' 학습 전략 - 효과적인 공부법과 성적 향상 비법',
        ' 완벽 가이드 - 성공적인 학습법과 활용 전략',
        ' - 체계적인 학습 방법과 실전 노하우',
    ],
}

# 기본 suffix
DEFAULT_SUFFIXES = [
    ' - 전문가가 알려주는 효과적인 방법',
    ' 완벽 가이드 - 성공적인 전략과 노하우',
    ' 상세 안내 - 체계적인 접근법과 실전 팁',
]

def get_category_from_path(filepath):
    """파일 경로에서 카테고리 추출"""
    path_str = str(filepath)

    if '/tutoring/' in path_str:
        return 'tutoring'
    elif '/academy/' in path_str:
        return 'academy'
    elif '/guide/' in path_str:
        return 'guide'
    elif '/exam/' in path_str or '/test/' in path_str:
        return 'exam'
    elif '/subject/' in path_str or '/korean/' in path_str or '/english/' in path_str or '/math/' in path_str:
        return 'subject'

    return 'default'

def get_suffix_for_title(title, category, title_length):
    """제목과 카테고리에 맞는 suffix 선택"""
    suffixes = CATEGORY_SUFFIXES.get(category, DEFAULT_SUFFIXES)

    # 제목 길이에 따라 suffix 선택
    if title_length < 20:
        # 매우 짧은 제목 - 긴 suffix
        return suffixes[0]
    elif title_length < 30:
        # 중간 길이 - 중간 suffix
        return suffixes[1] if len(suffixes) > 1 else suffixes[0]
    else:
        # 비교적 긴 제목 - 짧은 suffix
        return suffixes[2] if len(suffixes) > 2 else suffixes[0]

def improve_title(title, filepath):
    """제목 개선"""
    title_length = len(title)

    # 이미 충분히 긴 제목은 건너뛰기
    if title_length >= 40:
        return None

    category = get_category_from_path(filepath)
    suffix = get_suffix_for_title(title, category, title_length)

    # 새 제목 생성
    new_title = title + suffix

    # 60자를 넘지 않도록 조정
    if len(new_title) > 60:
        # suffix를 짧게 조정
        available_length = 60 - title_length
        suffix = suffix[:available_length]
        new_title = title + suffix

    return new_title

def update_file_title(filepath, new_title):
    """파일의 제목 업데이트"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        if not content.startswith('---'):
            return False

        parts = content.split('---', 2)
        if len(parts) < 3:
            return False

        frontmatter = parts[1]
        body = parts[2]

        # 기존 title 찾기
        title_match = re.search(r'title:\s*(.+)', frontmatter)
        if not title_match:
            return False

        old_title_line = title_match.group(0)
        new_title_line = f'title: {new_title}'

        # frontmatter 업데이트
        new_frontmatter = frontmatter.replace(old_title_line, new_title_line)

        # 파일 쓰기
        new_content = f'---{new_frontmatter}---{body}'
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

        return True

    except Exception as e:
        print(f"Error updating {filepath}: {e}")
        return False

def main():
    """메인 함수"""
    content_path = Path("/mnt/c/Users/user/Desktop/클로드/에듀코리아/edu-guide/content")

    print("제목 길이 개선 중...\n")

    updated_count = 0
    skipped_count = 0
    error_count = 0

    for md_file in content_path.rglob('*.md'):
        if md_file.name == '_index.md':
            continue

        try:
            # 현재 제목 추출
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()

            if not content.startswith('---'):
                skipped_count += 1
                continue

            parts = content.split('---', 2)
            if len(parts) < 3:
                skipped_count += 1
                continue

            frontmatter = parts[1]
            title_match = re.search(r'title:\s*(.+)', frontmatter)

            if not title_match:
                skipped_count += 1
                continue

            title = title_match.group(1).strip().strip('"\'')
            title_length = len(title)

            # 제목 개선 필요 여부 확인
            if title_length >= 40:
                skipped_count += 1
                continue

            # 새 제목 생성
            new_title = improve_title(title, md_file)

            if new_title and new_title != title:
                # 파일 업데이트
                if update_file_title(md_file, new_title):
                    updated_count += 1
                    print(f"✅ {md_file.name}")
                    print(f"   원본: {title} ({title_length}자)")
                    print(f"   개선: {new_title} ({len(new_title)}자)\n")
                else:
                    error_count += 1
            else:
                skipped_count += 1

        except Exception as e:
            print(f"❌ Error processing {md_file}: {e}")
            error_count += 1

    # 결과 출력
    print("\n" + "=" * 80)
    print(f"\n📊 제목 개선 완료\n")
    print(f"✅ 업데이트됨: {updated_count}개")
    print(f"⏭️  건너뜀: {skipped_count}개")
    print(f"❌ 오류: {error_count}개")
    print(f"\n총 처리: {updated_count + skipped_count + error_count}개\n")

if __name__ == "__main__":
    main()
