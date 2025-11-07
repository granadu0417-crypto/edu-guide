#!/usr/bin/env python3
"""
섹션 이미지 중복 분석 및 수정 스크립트
"""

import os
import re
from pathlib import Path
from collections import defaultdict

# 섹션별 고유 이미지 매핑
SECTION_IMAGES = {
    # 메인 섹션
    '/content/tutoring/_index.md': {
        'title': '학원·과외 가이드',
        'image': 'https://images.unsplash.com/photo-1427504494785-3a9ca7044f45?w=1200&h=630&fit=crop',  # 교실/학습
    },
    '/content/tutoring/guide/_index.md': {
        'title': '선택 가이드',
        'image': 'https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=1200&h=630&fit=crop',  # 펜과 노트
    },
    '/content/tutoring/academy/_index.md': {
        'title': '학원 찾기',
        'image': 'https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=1200&h=630&fit=crop',  # 공부하는 학생들
    },
    '/content/tutoring/private/_index.md': {
        'title': '과외 찾기',
        'image': 'https://images.unsplash.com/photo-1509062522246-3755977927d7?w=1200&h=630&fit=crop',  # 1:1 과외
    },

    # 학년별
    '/content/elementary/_index.md': {
        'title': '초등 학습 가이드',
        'image': 'https://images.unsplash.com/photo-1503454537195-1dcabb73ffb9?w=1200&h=630&fit=crop',  # 초등학생
    },
    '/content/middle/_index.md': {
        'title': '중등 학습 가이드',
        'image': 'https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=1200&h=630&fit=crop',  # 중학생 그룹
    },
    '/content/high/_index.md': {
        'title': '고등 학습 가이드',
        'image': 'https://images.unsplash.com/photo-1488998427799-e3362cec87c3?w=1200&h=630&fit=crop',  # 고등학생
    },

    # 과목별
    '/content/subjects/_index.md': {
        'title': '과목별 학습 전략',
        'image': 'https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=1200&h=630&fit=crop',  # 책들
    },
    '/content/subjects/korean/_index.md': {
        'title': '국어',
        'image': 'https://images.unsplash.com/photo-1455390582262-044cdead277a?w=1200&h=630&fit=crop',  # 한글/책
    },
    '/content/subjects/english/_index.md': {
        'title': '영어',
        'image': 'https://images.unsplash.com/photo-1546410531-bb4caa6b424d?w=1200&h=630&fit=crop',  # 영어 알파벳
    },
    '/content/subjects/math/_index.md': {
        'title': '수학',
        'image': 'https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=1200&h=630&fit=crop',  # 수학 공식
    },
    '/content/subjects/science/_index.md': {
        'title': '과학',
        'image': 'https://images.unsplash.com/photo-1532094349884-543bc11b234d?w=1200&h=630&fit=crop',  # 과학 실험
    },
    '/content/subjects/social/_index.md': {
        'title': '사회',
        'image': 'https://images.unsplash.com/photo-1526666923127-b2970f64b422?w=1200&h=630&fit=crop',  # 지구본/지도
    },

    # 시험/상담
    '/content/exam/_index.md': {
        'title': '시험 대비 전략',
        'image': 'https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=1200&h=630&fit=crop',  # 시험
    },
    '/content/consultation/_index.md': {
        'title': '학습 상담',
        'image': 'https://images.unsplash.com/photo-1573164574230-db1d5e960238?w=1200&h=630&fit=crop',  # 상담
    },

    # 지역별
    '/content/local/_index.md': {
        'title': '지역별 교육 정보',
        'image': 'https://images.unsplash.com/photo-1524661135-423995f22d0b?w=1200&h=630&fit=crop',  # 도시
    },
    '/content/local/seoul/_index.md': {
        'title': '서울',
        'image': 'https://images.unsplash.com/photo-1505761671935-60b3a7427bad?w=1200&h=630&fit=crop',  # 서울 건물
    },
    '/content/local/gyeonggi/_index.md': {
        'title': '경기',
        'image': 'https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=1200&h=630&fit=crop',  # 경기 지역
    },
}

def extract_featured_image(filepath):
    """파일에서 featured_image 추출"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        if not content.startswith('---'):
            return None

        parts = content.split('---', 2)
        if len(parts) < 3:
            return None

        frontmatter = parts[1]
        match = re.search(r'featured_image:\s*(.+)', frontmatter)

        if match:
            return match.group(1).strip()
        return None

    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None

def update_featured_image(filepath, new_image):
    """featured_image 업데이트"""
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

        # 기존 featured_image 찾기
        old_match = re.search(r'featured_image:\s*.+', frontmatter)

        if old_match:
            # 교체
            new_frontmatter = frontmatter.replace(
                old_match.group(0),
                f'featured_image: {new_image}'
            )
        else:
            # 없으면 추가
            new_frontmatter = frontmatter + f'\nfeatured_image: {new_image}\n'

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
    base_path = Path("/mnt/c/Users/user/Desktop/클로드/에듀코리아/edu-guide")

    print("=" * 80)
    print("섹션 이미지 분석 및 중복 제거\n")

    # 현재 이미지 분석
    current_images = {}
    image_usage = defaultdict(list)

    for rel_path, info in SECTION_IMAGES.items():
        full_path = base_path / rel_path.lstrip('/')
        if full_path.exists():
            current_img = extract_featured_image(full_path)
            current_images[rel_path] = current_img
            if current_img:
                image_usage[current_img].append(rel_path)

    # 중복 이미지 확인
    print("📊 현재 상태:\n")
    duplicates_found = False
    for img, paths in image_usage.items():
        if len(paths) > 1:
            duplicates_found = True
            print(f"⚠️  중복 이미지 발견: {len(paths)}개 섹션에서 사용")
            print(f"   이미지: {img[:60]}...")
            for path in paths:
                title = SECTION_IMAGES.get(path, {}).get('title', 'Unknown')
                print(f"   - {title} ({path})")
            print()

    if not duplicates_found:
        print("✅ 중복 이미지 없음\n")

    # 이미지 업데이트
    print("\n" + "=" * 80)
    print("🔧 이미지 업데이트 중...\n")

    updated_count = 0
    skipped_count = 0

    for rel_path, info in SECTION_IMAGES.items():
        full_path = base_path / rel_path.lstrip('/')

        if not full_path.exists():
            print(f"⏭️  파일 없음: {info['title']}")
            skipped_count += 1
            continue

        current_img = current_images.get(rel_path)
        target_img = info['image']

        if current_img == target_img:
            print(f"✓  유지: {info['title']}")
            skipped_count += 1
        else:
            if update_featured_image(full_path, target_img):
                print(f"✅ 수정: {info['title']}")
                print(f"   {current_img[:50] if current_img else 'None'}...")
                print(f"   → {target_img[:50]}...")
                updated_count += 1
            else:
                print(f"❌ 실패: {info['title']}")

    # 결과 출력
    print("\n" + "=" * 80)
    print(f"\n📊 완료\n")
    print(f"✅ 수정됨: {updated_count}개")
    print(f"⏭️  건너뜀: {skipped_count}개")
    print(f"\n총 섹션: {len(SECTION_IMAGES)}개\n")

if __name__ == "__main__":
    main()
