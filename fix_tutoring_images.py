#!/usr/bin/env python3
"""
학원/과외 섹션 중복 이미지 교체 스크립트
"""

import os
import re
import random
from pathlib import Path

# 교육 관련 Unsplash 이미지 검색어
EDUCATION_KEYWORDS = [
    "classroom", "students studying", "teacher", "school", "education",
    "learning", "books", "study group", "homework", "notebook",
    "library", "desk study", "online learning", "tutoring",
    "math homework", "science class", "writing", "reading",
    "student laptop", "school supplies", "chalkboard",
    "whiteboard", "pencils", "graduation", "university",
    "college student", "exam", "test", "studying at home",
    "kids learning", "teenager studying", "computer learning"
]

# 중복 이미지 ID 목록
DUPLICATE_IMAGES = [
    "photo-1434030216411-0b793f4b4173",
    "photo-1427504494785-3a9ca7044f45",
    "photo-1522202176988-66273c2fd55f"
]

def generate_unique_image_url(seed):
    """고유한 Unsplash 이미지 URL 생성"""
    random.seed(seed)
    keyword = random.choice(EDUCATION_KEYWORDS)
    # Unsplash Source API 사용 - 각 키워드와 시드로 고유한 이미지 생성
    return f"https://source.unsplash.com/1200x630/?{keyword.replace(' ', '-')}&sig={seed}"

def fix_image_in_file(filepath):
    """파일 내 중복 이미지를 고유 이미지로 교체"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # featured_image 찾기
        original_content = content
        for old_image_id in DUPLICATE_IMAGES:
            if old_image_id in content:
                # 파일 경로를 시드로 사용하여 고유한 이미지 생성
                seed = abs(hash(str(filepath)))
                new_url = generate_unique_image_url(seed)

                # 이미지 URL 교체
                content = re.sub(
                    rf'featured_image:\s*https://images\.unsplash\.com/{re.escape(old_image_id)}\?[^\n]*',
                    f'featured_image: {new_url}',
                    content
                )

                if content != original_content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    return True

        return False
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def main():
    """메인 함수"""
    base_path = Path("/mnt/c/Users/user/Desktop/클로드/에듀코리아/edu-guide/content/tutoring")
    sections = ['guide', 'academy', 'private']

    total_fixed = 0

    for section in sections:
        section_path = base_path / section
        if not section_path.exists():
            continue

        print(f"\n처리 중: {section} 섹션...")
        fixed_count = 0

        # 모든 .md 파일 찾기
        for md_file in section_path.rglob('*.md'):
            if fix_image_in_file(md_file):
                fixed_count += 1
                print(f"  ✓ {md_file.name}")

        print(f"{section} 섹션: {fixed_count}개 파일 수정")
        total_fixed += fixed_count

    print(f"\n총 {total_fixed}개 파일의 이미지를 교체했습니다!")

if __name__ == "__main__":
    main()
