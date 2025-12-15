#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
이미지 자동 할당 스크립트
Pexels와 Unsplash API를 사용하여 각 콘텐츠에 고유한 이미지 할당
"""

import os
import re
import time
import random
import requests
from pathlib import Path

# API 키
PEXELS_API_KEY = "1ZNOIZ70f0oMswRVoLVRWHeqioIxxRQr3CEAH4ZHhOr9E0q9rAEXBsJA"
UNSPLASH_ACCESS_KEY = "mARHwUbfiB7nMDACQgbKAKV0Guy_cmWAtsumV2htpJ4"

# 카테고리별 검색 키워드 매핑
CATEGORY_KEYWORDS = {
    'elementary': ['elementary student studying', 'child learning', 'primary school education', 'young student homework'],
    'middle': ['middle school student', 'teenager studying', 'junior high education', 'teen homework'],
    'high': ['high school student', 'teenager books', 'university entrance exam', 'advanced studying'],
    'subjects': {
        'korean': ['korean language book', 'reading comprehension', 'writing student', 'literature study'],
        'english': ['english learning', 'vocabulary book', 'foreign language student', 'english textbook'],
        'math': ['mathematics student', 'math problem solving', 'geometry study', 'calculator notebook'],
        'science': ['science experiment', 'laboratory student', 'microscope learning', 'chemistry education'],
        'social': ['geography student', 'history textbook', 'social studies map', 'world globe education']
    },
    'exam': ['student taking test', 'exam preparation', 'study schedule', 'test review notes'],
    'tutoring': ['one on one tutoring', 'private teacher student', 'personalized learning', 'tutor teaching'],
    'local': ['seoul cityscape', 'korean city education', 'urban school district', 'neighborhood learning center'],
    'consultation': ['counseling session', 'education consultation', 'parent teacher meeting', 'academic advice']
}

def get_pexels_image(query, page=1):
    """Pexels API로 이미지 검색"""
    url = "https://api.pexels.com/v1/search"
    headers = {"Authorization": PEXELS_API_KEY}
    params = {
        "query": query,
        "per_page": 15,
        "page": page,
        "orientation": "landscape"
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data['photos']:
                photo = random.choice(data['photos'])
                return photo['src']['large2x']
    except Exception as e:
        print(f"⚠️  Pexels API 오류: {e}")

    return None

def get_unsplash_image(query, page=1):
    """Unsplash API로 이미지 검색"""
    url = "https://api.unsplash.com/search/photos"
    headers = {"Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"}
    params = {
        "query": query,
        "per_page": 15,
        "page": page,
        "orientation": "landscape"
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data['results']:
                photo = random.choice(data['results'])
                return f"{photo['urls']['regular']}&w=1200&q=80"
    except Exception as e:
        print(f"⚠️  Unsplash API 오류: {e}")

    return None

def get_category_from_path(file_path):
    """파일 경로에서 카테고리 추출"""
    parts = file_path.parts
    for part in parts:
        if part in CATEGORY_KEYWORDS:
            return part

    # subjects 하위 카테고리 확인
    if 'subjects' in parts:
        for i, part in enumerate(parts):
            if part == 'subjects' and i + 1 < len(parts):
                subject = parts[i + 1]
                if subject in CATEGORY_KEYWORDS['subjects']:
                    return f'subjects.{subject}'

    return 'general'

def get_search_keywords(category):
    """카테고리에 맞는 검색 키워드 반환"""
    if '.' in category:
        main, sub = category.split('.')
        return CATEGORY_KEYWORDS.get(main, {}).get(sub, ['education student studying'])

    keywords = CATEGORY_KEYWORDS.get(category, ['korean education student studying'])
    return keywords

def extract_front_matter(content):
    """Front Matter 추출"""
    match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if match:
        return match.group(1), match.end()
    return None, 0

def update_featured_image(content, new_image_url):
    """featured_image 필드 업데이트"""
    # Front Matter 추출
    front_matter, end_pos = extract_front_matter(content)
    if not front_matter:
        return content, False

    # featured_image 필드 확인
    if 'featured_image:' in front_matter:
        # 기존 이미지 URL 추출
        old_match = re.search(r'featured_image:\s*"([^"]+)"', front_matter)
        if old_match:
            old_url = old_match.group(1)
            # 같은 URL이면 변경 안 함
            if old_url == new_image_url:
                return content, False

            # 새 이미지로 교체
            new_front_matter = re.sub(
                r'featured_image:\s*"[^"]+"',
                f'featured_image: "{new_image_url}"',
                front_matter
            )
        else:
            return content, False
    else:
        # featured_image 필드 추가
        new_front_matter = front_matter + f'\nfeatured_image: "{new_image_url}"'

    # 전체 콘텐츠 재구성
    new_content = f"---\n{new_front_matter}\n---\n" + content[end_pos:]
    return new_content, True

def process_markdown_file(file_path, used_images):
    """마크다운 파일 처리"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 카테고리 확인
        category = get_category_from_path(file_path)
        keywords = get_search_keywords(category)

        # 랜덤 키워드 선택
        query = random.choice(keywords)

        # API 선택 (번갈아가며 사용)
        use_pexels = random.choice([True, False])

        new_image = None
        max_attempts = 5

        for attempt in range(max_attempts):
            if use_pexels:
                new_image = get_pexels_image(query, page=attempt+1)
            else:
                new_image = get_unsplash_image(query, page=attempt+1)

            # 중복 확인
            if new_image and new_image not in used_images:
                break

            # API 전환
            use_pexels = not use_pexels
            time.sleep(0.5)  # Rate limit 방지

        if not new_image:
            print(f"⚠️  {file_path.name}: 이미지를 찾지 못했습니다.")
            return False

        # 이미지 업데이트
        new_content, updated = update_featured_image(content, new_image)

        if updated:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)

            used_images.add(new_image)
            source = "Pexels" if use_pexels else "Unsplash"
            print(f"✅ {file_path.name}: {source} 이미지 할당")
            return True
        else:
            return False

    except Exception as e:
        print(f"❌ {file_path.name} 처리 중 오류: {e}")
        return False

def main():
    """메인 실행 함수"""
    content_dir = Path('content')

    if not content_dir.exists():
        print("❌ content 디렉토리를 찾을 수 없습니다.")
        return

    # 모든 마크다운 파일 찾기
    md_files = list(content_dir.rglob('*.md'))

    print(f"📁 총 {len(md_files)}개 파일에 이미지 할당 시작...\n")

    used_images = set()
    processed_files = 0

    for i, md_file in enumerate(md_files, 1):
        print(f"[{i}/{len(md_files)}] 처리 중...", end=" ")

        if process_markdown_file(md_file, used_images):
            processed_files += 1

        # Rate limit 방지 (API 호출 제한)
        if i % 20 == 0:
            print("\n⏸️  20개 처리마다 3초 대기 (API Rate Limit 방지)...")
            time.sleep(3)

    print(f"\n{'='*60}")
    print(f"✅ 작업 완료!")
    print(f"📊 이미지 할당 완료: {processed_files}개 파일")
    print(f"🖼️  사용된 고유 이미지: {len(used_images)}개")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
