#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
중복 이미지 다양화 스크립트
카테고리별로 다양한 이미지 할당
"""

import os
import re
from pathlib import Path

# 카테고리별 이미지 풀 (Unsplash - 교육 관련 고품질 이미지)
IMAGE_POOLS = {
    'consultation': [
        "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=1200&h=630&fit=crop",  # 상담
        "https://images.unsplash.com/photo-1551836022-deb4988cc6c0?w=1200&h=630&fit=crop",  # 비즈니스 미팅
        "https://images.unsplash.com/photo-1552664730-d307ca884978?w=1200&h=630&fit=crop",  # 팀워크
        "https://images.unsplash.com/photo-1531538606174-0f90ff5dce83?w=1200&h=630&fit=crop",  # 1:1 상담
        "https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?w=1200&h=630&fit=crop",  # 워크숍
        "https://images.unsplash.com/photo-1560439514-4e9645039924?w=1200&h=630&fit=crop",  # 회의실
        "https://images.unsplash.com/photo-1523240795612-9a054b0db644?w=1200&h=630&fit=crop",  # 팀 협업
        "https://images.unsplash.com/photo-1542626991-cbc4e32524cc?w=1200&h=630&fit=crop",  # 멘토링
        "https://images.unsplash.com/photo-1507537297725-24a1c029d3ca?w=1200&h=630&fit=crop",  # 컨설팅
        "https://images.unsplash.com/photo-1521737711867-e3b97375f902?w=1200&h=630&fit=crop",  # 코칭
        "https://images.unsplash.com/photo-1521737852567-6949f3f9f2b5?w=1200&h=630&fit=crop",  # 상담 장면
        "https://images.unsplash.com/photo-1600880292203-757bb62b4baf?w=1200&h=630&fit=crop",  # 온라인 미팅
        "https://images.unsplash.com/photo-1513128034602-7814ccaddd4e?w=1200&h=630&fit=crop",  # 교육 세미나
        "https://images.unsplash.com/photo-1516321497487-e288fb19713f?w=1200&h=630&fit=crop",  # 전문가 대화
        "https://images.unsplash.com/photo-1557804506-669a67965ba0?w=1200&h=630&fit=crop",  # 팀 미팅
    ],
    'exam': [
        "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=1200&h=630&fit=crop",  # 시험 공부
        "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=1200&h=630&fit=crop",  # 노트 필기
        "https://images.unsplash.com/photo-1546410531-bb4caa6b424d?w=1200&h=630&fit=crop",  # 시험지
        "https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=1200&h=630&fit=crop",  # 학습 도구
        "https://images.unsplash.com/photo-1516534775068-ba3e7458af70?w=1200&h=630&fit=crop",  # 책상 공부
        "https://images.unsplash.com/photo-1455390582262-044cdead277a?w=1200&h=630&fit=crop",  # 필기도구
        "https://images.unsplash.com/photo-1488190211105-8b0e65b80b4e?w=1200&h=630&fit=crop",  # 책과 노트
        "https://images.unsplash.com/photo-1471107340929-a87cd0f5b5f3?w=1200&h=630&fit=crop",  # 도서관
        "https://images.unsplash.com/photo-1519406596751-0a3ccc4937fe?w=1200&h=630&fit=crop",  # 집중 학습
        "https://images.unsplash.com/photo-1513001900722-370f803f498d?w=1200&h=630&fit=crop",  # 시험 준비
        "https://images.unsplash.com/photo-1509228468518-180dd4864904?w=1200&h=630&fit=crop",  # 공부 자료
        "https://images.unsplash.com/photo-1461749280684-dccba630e2f6?w=1200&h=630&fit=crop",  # 컴퓨터 학습
        "https://images.unsplash.com/photo-1505682634904-d7c8d95cdc50?w=1200&h=630&fit=crop",  # 수험서
        "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=1200&h=630&fit=crop",  # 책더미
        "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=1200&h=630&fit=crop",  # 노트북 학습
    ],
    'tutoring': [
        "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=1200&h=630&fit=crop",  # 1:1 과외
        "https://images.unsplash.com/photo-1509062522246-3755977927d7?w=1200&h=630&fit=crop",  # 개인 지도
        "https://images.unsplash.com/photo-1524178232363-1fb2b075b655?w=1200&h=630&fit=crop",  # 교실 수업
        "https://images.unsplash.com/photo-1427504494785-3a9ca7044f45?w=1200&h=630&fit=crop",  # 선생님과 학생
        "https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?w=1200&h=630&fit=crop",  # 그룹 학습
        "https://images.unsplash.com/photo-1556911220-e15b29be8c8f?w=1200&h=630&fit=crop",  # 수업 장면
        "https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=1200&h=630&fit=crop",  # 팀 학습
        "https://images.unsplash.com/photo-1509228468518-180dd4864904?w=1200&h=630&fit=crop",  # 학습 자료
        "https://images.unsplash.com/photo-1513258496099-48168024aec0?w=1200&h=630&fit=crop",  # 화이트보드
        "https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=1200&h=630&fit=crop",  # 온라인 과외
        "https://images.unsplash.com/photo-1546410531-bb4caa6b424d?w=1200&h=630&fit=crop",  # 수학 공부
        "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=1200&h=630&fit=crop",  # 대학 캠퍼스
        "https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=1200&h=630&fit=crop",  # 컴퓨터 교육
        "https://images.unsplash.com/photo-1488190211105-8b0e65b80b4e?w=1200&h=630&fit=crop",  # 학습 도서
        "https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=1200&h=630&fit=crop",  # 학습 준비
    ],
    'elementary': [
        "https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=1200&h=630&fit=crop",  # 초등 학습
        "https://images.unsplash.com/photo-1588072432836-e10032774350?w=1200&h=630&fit=crop",  # 어린이 독서
        "https://images.unsplash.com/photo-1503454537195-1dcabb73ffb9?w=1200&h=630&fit=crop",  # 초등학생
        "https://images.unsplash.com/photo-1516627145497-ae6968895b74?w=1200&h=630&fit=crop",  # 학교 수업
        "https://images.unsplash.com/photo-1553729459-efe14ef6055d?w=1200&h=630&fit=crop",  # 어린이 활동
        "https://images.unsplash.com/photo-1587825140708-dfaf72ae4b04?w=1200&h=630&fit=crop",  # 그림 그리기
        "https://images.unsplash.com/photo-1596496181848-3091d4878b24?w=1200&h=630&fit=crop",  # 초등 교실
        "https://images.unsplash.com/photo-1503454537195-1dcabb73ffb9?w=1200&h=630&fit=crop",  # 어린이 학습
        "https://images.unsplash.com/photo-1455390582262-044cdead277a?w=1200&h=630&fit=crop",  # 학용품
        "https://images.unsplash.com/photo-1509062522246-3755977927d7?w=1200&h=630&fit=crop",  # 선생님과 학생
        "https://images.unsplash.com/photo-1488190211105-8b0e65b80b4e?w=1200&h=630&fit=crop",  # 초등 도서
        "https://images.unsplash.com/photo-1546410531-bb4caa6b424d?w=1200&h=630&fit=crop",  # 공부 시간
        "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=1200&h=630&fit=crop",  # 어린이 책
        "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=1200&h=630&fit=crop",  # 노트 작성
        "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=1200&h=630&fit=crop",  # 학습 활동
    ],
    'middle': [
        "https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=1200&h=630&fit=crop",  # 중등 학습
        "https://images.unsplash.com/photo-1427504494785-3a9ca7044f45?w=1200&h=630&fit=crop",  # 학생들
        "https://images.unsplash.com/photo-1509062522246-3755977927d7?w=1200&h=630&fit=crop",  # 중학교 수업
        "https://images.unsplash.com/photo-1524178232363-1fb2b075b655?w=1200&h=630&fit=crop",  # 교실 장면
        "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=1200&h=630&fit=crop",  # 개별 학습
        "https://images.unsplash.com/photo-1488190211105-8b0e65b80b4e?w=1200&h=630&fit=crop",  # 학습 자료
        "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=1200&h=630&fit=crop",  # 필기 노트
        "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=1200&h=630&fit=crop",  # 집중 학습
        "https://images.unsplash.com/photo-1546410531-bb4caa6b424d?w=1200&h=630&fit=crop",  # 시험 준비
        "https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=1200&h=630&fit=crop",  # 학습 도구
        "https://images.unsplash.com/photo-1455390582262-044cdead277a?w=1200&h=630&fit=crop",  # 필기구
        "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=1200&h=630&fit=crop",  # 교과서
        "https://images.unsplash.com/photo-1509228468518-180dd4864904?w=1200&h=630&fit=crop",  # 학습 공간
        "https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=1200&h=630&fit=crop",  # 컴퓨터 활용
        "https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=1200&h=630&fit=crop",  # 온라인 학습
    ],
    'high': [
        "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=1200&h=630&fit=crop",  # 고등학생
        "https://images.unsplash.com/photo-1427504494785-3a9ca7044f45?w=1200&h=630&fit=crop",  # 대학 준비
        "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=1200&h=630&fit=crop",  # 수험 공부
        "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=1200&h=630&fit=crop",  # 집중 필기
        "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=1200&h=630&fit=crop",  # 개별 학습
        "https://images.unsplash.com/photo-1488190211105-8b0e65b80b4e?w=1200&h=630&fit=crop",  # 수능 교재
        "https://images.unsplash.com/photo-1546410531-bb4caa6b424d?w=1200&h=630&fit=crop",  # 수학 공부
        "https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=1200&h=630&fit=crop",  # 시험 대비
        "https://images.unsplash.com/photo-1509062522246-3755977927d7?w=1200&h=630&fit=crop",  # 멘토링
        "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=1200&h=630&fit=crop",  # 참고서
        "https://images.unsplash.com/photo-1455390582262-044cdead277a?w=1200&h=630&fit=crop",  # 학습 도구
        "https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=1200&h=630&fit=crop",  # 디지털 학습
        "https://images.unsplash.com/photo-1509228468518-180dd4864904?w=1200&h=630&fit=crop",  # 입시 자료
        "https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=1200&h=630&fit=crop",  # 온라인 강의
        "https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=1200&h=630&fit=crop",  # 스터디 그룹
    ]
}

def parse_front_matter(content):
    """Front matter 파싱"""
    if not content.startswith('---'):
        return None, content, content

    parts = content.split('---', 2)
    if len(parts) < 3:
        return None, content, content

    return parts[1].strip(), parts[2].strip(), content

def get_new_image(file_path, category):
    """파일 경로를 기반으로 새로운 이미지 URL 선택"""
    filename = Path(file_path).stem

    # 파일명에서 번호 추출
    number_match = re.search(r'-(\d+)$', filename)
    if not number_match:
        number_match = re.search(r'(\d+)', filename)

    if number_match:
        num = int(number_match.group(1))
    else:
        # 번호가 없으면 파일명 해시 사용
        num = hash(filename) % 100

    # 이미지 풀에서 순환 선택
    if category in IMAGE_POOLS:
        images = IMAGE_POOLS[category]
        image_idx = (num - 1) % len(images)
        return images[image_idx]

    return None

def fix_file(file_path):
    """파일의 중복 이미지 교체"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        front_matter, body, original = parse_front_matter(content)

        if not front_matter:
            return False

        # 현재 이미지 추출
        image_match = re.search(r'featured_image:\s*["\']?(.+?)["\']?\s*$', front_matter, re.MULTILINE)

        if not image_match:
            return False

        current_image = image_match.group(1).strip('"\'')

        # 카테고리 판단
        rel_path = Path(file_path).relative_to(Path('content'))
        category = rel_path.parts[0] if len(rel_path.parts) > 0 else None

        # 새로운 이미지 선택
        new_image = get_new_image(file_path, category)

        if not new_image or new_image == current_image:
            return False

        # 이미지 교체
        new_front_matter = re.sub(
            r'featured_image:\s*["\']?(.+?)["\']?\s*$',
            f'featured_image: "{new_image}"',
            front_matter,
            flags=re.MULTILINE
        )

        new_content = f"---\n{new_front_matter}\n---\n{body}"

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        return True

    except Exception as e:
        print(f"  ❌ {file_path}: {e}")
        return False

def main():
    """메인 실행"""
    content_dir = Path('content')

    if not content_dir.exists():
        print("❌ content 디렉토리를 찾을 수 없습니다.")
        return

    # 중복 이미지가 있는 카테고리만 처리
    target_dirs = [
        'consultation',
        'exam',
        'tutoring',
        'elementary',
        'middle',
        'high'
    ]

    total_fixed = 0

    for category in target_dirs:
        category_path = content_dir / category

        if not category_path.exists():
            continue

        md_files = list(category_path.glob('*.md'))
        md_files = [f for f in md_files if f.stem != '_index']

        print(f"\n📁 {category.upper()} ({len(md_files)}개 파일)")
        print("-" * 80)

        fixed_count = 0

        for md_file in sorted(md_files):
            if fix_file(md_file):
                fixed_count += 1
                # print(f"  ✅ {md_file.name}")

        total_fixed += fixed_count
        print(f"수정 완료: {fixed_count}개")

    print(f"\n{'='*80}")
    print(f"✅ 중복 이미지 다양화 완료!")
    print(f"{'='*80}")
    print(f"총 수정된 파일: {total_fixed}개")
    print(f"{'='*80}")

if __name__ == '__main__':
    main()
