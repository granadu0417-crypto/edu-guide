#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
이미지가 없는 파일에 간단한 기본 이미지 추가
"""

from pathlib import Path
import yaml
import random

def extract_front_matter(content):
    """YAML front matter 추출"""
    if not content.startswith('---'):
        return None, content

    parts = content.split('---', 2)
    if len(parts) < 3:
        return None, content

    try:
        front_matter = yaml.safe_load(parts[1])
        body = parts[2]
        return front_matter, body
    except:
        return None, content

# 카테고리별 이미지 풀
CATEGORY_IMAGES = {
    'elementary': [
        'https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=1200&h=630&fit=crop',  # classroom
        'https://images.unsplash.com/photo-1427504494785-3a9ca7044f45?w=1200&h=630&fit=crop',  # students
        'https://images.unsplash.com/photo-1503454537195-1dcabb73ffb9?w=1200&h=630&fit=crop',  # books
        'https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=1200&h=630&fit=crop',  # study desk
        'https://images.unsplash.com/photo-1509062522246-3755977927d7?w=1200&h=630&fit=crop',  # library
    ],
    'middle': [
        'https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=1200&h=630&fit=crop',  # university
        'https://images.unsplash.com/photo-1491841651911-c44c30c34548?w=1200&h=630&fit=crop',  # books
        'https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=1200&h=630&fit=crop',  # desk
        'https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=1200&h=630&fit=crop',  # notebook
        'https://images.unsplash.com/photo-1513258496099-48168024aec0?w=1200&h=630&fit=crop',  # school
    ],
    'high': [
        'https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=1200&h=630&fit=crop',  # university
        'https://images.unsplash.com/photo-1523240795612-9a054b0db644?w=1200&h=630&fit=crop',  # campus
        'https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=1200&h=630&fit=crop',  # library
        'https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=1200&h=630&fit=crop',  # study
        'https://images.unsplash.com/photo-1517842645767-c639042777db?w=1200&h=630&fit=crop',  # books
    ],
    'subjects': [
        'https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=1200&h=630&fit=crop',  # books
        'https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=1200&h=630&fit=crop',  # desk
        'https://images.unsplash.com/photo-1509062522246-3755977927d7?w=1200&h=630&fit=crop',  # library
        'https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=1200&h=630&fit=crop',  # notebook
        'https://images.unsplash.com/photo-1455390582262-044cdead277a?w=1200&h=630&fit=crop',  # pencils
    ],
    'exam': [
        'https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=1200&h=630&fit=crop',  # writing
        'https://images.unsplash.com/photo-1455390582262-044cdead277a?w=1200&h=630&fit=crop',  # test
        'https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=1200&h=630&fit=crop',  # study
        'https://images.unsplash.com/photo-1606326608606-aa0b62935f2b?w=1200&h=630&fit=crop',  # checklist
        'https://images.unsplash.com/photo-1484480974693-6ca0a78fb36b?w=1200&h=630&fit=crop',  # planning
    ],
    'tutoring': [
        'https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=1200&h=630&fit=crop',  # tutoring
        'https://images.unsplash.com/photo-1524178232363-1fb2b075b655?w=1200&h=630&fit=crop',  # laptop
        'https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=1200&h=630&fit=crop',  # classroom
        'https://images.unsplash.com/photo-1427504494785-3a9ca7044f45?w=1200&h=630&fit=crop',  # teaching
        'https://images.unsplash.com/photo-1509062522246-3755977927d7?w=1200&h=630&fit=crop',  # learning
    ],
    'consultation': [
        'https://images.unsplash.com/photo-1450101499163-c8848c66ca85?w=1200&h=630&fit=crop',  # consulting
        'https://images.unsplash.com/photo-1542626991-cbc4e32524cc?w=1200&h=630&fit=crop',  # discussion
        'https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=1200&h=630&fit=crop',  # meeting
        'https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=1200&h=630&fit=crop',  # guidance
        'https://images.unsplash.com/photo-1497215842964-222b430dc094?w=1200&h=630&fit=crop',  # office
    ],
    'local': [
        'https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?w=1200&h=630&fit=crop',  # city
        'https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=1200&h=630&fit=crop',  # urban
        'https://images.unsplash.com/photo-1480714378408-67cf0d13bc1b?w=1200&h=630&fit=crop',  # buildings
        'https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=1200&h=630&fit=crop',  # architecture
        'https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?w=1200&h=630&fit=crop',  # location
    ]
}

def get_image_for_category(category):
    """카테고리에 맞는 랜덤 이미지 선택"""
    if category in CATEGORY_IMAGES:
        return random.choice(CATEGORY_IMAGES[category])
    else:
        # 기본 이미지
        return 'https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=1200&h=630&fit=crop'

def process_file(file_path):
    """파일 처리"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        front_matter, body = extract_front_matter(content)
        if not front_matter:
            return False, "front matter 없음"

        # 이미 이미지가 있으면 스킵
        if front_matter.get('featured_image'):
            return False, "이미 이미지 있음"

        rel_path = str(file_path.relative_to(Path('content')))
        category = rel_path.split('/')[0]

        # 이미지 선택
        image_url = get_image_for_category(category)
        front_matter['featured_image'] = image_url

        # YAML 직렬화
        yaml_str = yaml.dump(front_matter, allow_unicode=True, sort_keys=False, default_flow_style=False)

        # 새 콘텐츠 작성
        new_content = f"---\n{yaml_str}---{body}"

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        return True, f"{rel_path}"

    except Exception as e:
        return False, f"오류: {e}"

def main():
    content_dir = Path('content')

    success_count = 0
    skip_count = 0
    error_count = 0
    category_stats = {}

    print("🖼️  이미지 추가 시작...\n")

    for md_file in content_dir.rglob('*.md'):
        success, message = process_file(md_file)

        if success:
            success_count += 1
            category = str(md_file.relative_to(content_dir)).split('/')[0]
            category_stats[category] = category_stats.get(category, 0) + 1
            if success_count <= 10 or success_count % 50 == 0:
                print(f"✅ [{success_count}] {message}")
        elif "이미 이미지" in message:
            skip_count += 1
        else:
            error_count += 1
            if "front matter" not in message:
                print(f"❌ {message}")

    print("\n" + "=" * 80)
    print("📊 이미지 추가 완료")
    print("=" * 80)
    print(f"추가 완료: {success_count}개")
    print(f"스킵    : {skip_count}개")
    print(f"오류    : {error_count}개")

    if category_stats:
        print("\n📂 카테고리별 통계:")
        for category in sorted(category_stats.keys()):
            print(f"  {category:15s}: {category_stats[category]:3d}개 추가")

    print("=" * 80)

if __name__ == '__main__':
    main()
