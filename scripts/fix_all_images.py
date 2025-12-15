#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
모든 깨진 이미지 일괄 수정
"""

from pathlib import Path
import re

# 카테고리별 기본 이미지
DEFAULT_IMAGES = {
    'subjects': 'https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=1200&h=630&fit=crop',
    'korean': 'https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=1200&h=630&fit=crop',
    'english': 'https://images.unsplash.com/photo-1546410531-bb4caa6b424d?w=1200&h=630&fit=crop',
    'math': 'https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=1200&h=630&fit=crop',
    'science': 'https://images.unsplash.com/photo-1532094349884-543bc11b234d?w=1200&h=630&fit=crop',
    'social': 'https://images.unsplash.com/photo-1526304640581-d334cdbbf45e?w=1200&h=630&fit=crop',
    'elementary': 'https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=1200&h=630&fit=crop',
    'exam': 'https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=1200&h=630&fit=crop',
    'local': 'https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?w=1200&h=630&fit=crop',
    'tutoring': 'https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=1200&h=630&fit=crop',
}

def fix_image_url(url):
    """Unsplash URL에 파라미터 추가"""
    if not url:
        return None

    # 이미 파라미터가 있는 경우
    if 'w=1200' in url and 'h=630' in url:
        return url

    # Unsplash URL인 경우 파라미터 추가
    if 'unsplash.com' in url:
        # 기존 파라미터 제거
        base_url = url.split('?')[0]
        # 새 파라미터 추가
        return f"{base_url}?w=1200&h=630&fit=crop"

    return url

def get_default_image(file_path):
    """파일 경로 기반으로 기본 이미지 반환"""
    rel_path = str(file_path)

    # subjects 카테고리 내 과목별
    if 'subjects/korean' in rel_path:
        return DEFAULT_IMAGES['korean']
    elif 'subjects/english' in rel_path:
        return DEFAULT_IMAGES['english']
    elif 'subjects/math' in rel_path:
        return DEFAULT_IMAGES['math']
    elif 'subjects/science' in rel_path:
        return DEFAULT_IMAGES['science']
    elif 'subjects/social' in rel_path:
        return DEFAULT_IMAGES['social']
    elif 'subjects' in rel_path:
        return DEFAULT_IMAGES['subjects']

    # 기타 카테고리
    for category in ['elementary', 'exam', 'local', 'tutoring']:
        if category in rel_path:
            return DEFAULT_IMAGES[category]

    return DEFAULT_IMAGES['subjects']

def fix_file_image(file_path):
    """파일의 이미지 수정"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        if not content.startswith('---'):
            return False, "front matter 없음"

        parts = content.split('---', 2)
        if len(parts) < 3:
            return False, "front matter 형식 오류"

        front_matter = parts[1]
        body = parts[2]

        # Featured Image 추출
        img_match = re.search(r'^featured_image:\s*(.+)', front_matter, re.MULTILINE)

        if img_match:
            # 기존 이미지 URL 수정
            old_url = img_match.group(1).strip()
            new_url = fix_image_url(old_url)

            if new_url and new_url != old_url:
                front_matter = front_matter.replace(
                    f"featured_image: {old_url}",
                    f"featured_image: {new_url}"
                )

                # 파일 저장
                new_content = f"---{front_matter}---{body}"
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)

                return True, f"URL 수정: {new_url}"
            else:
                return False, "수정 불필요"
        else:
            # featured_image 필드 없음 - 추가
            default_img = get_default_image(file_path)

            # author 필드 뒤에 추가 (없으면 categories 뒤에)
            if 'author:' in front_matter:
                front_matter = re.sub(
                    r'(author:.+)',
                    f'\\1\nfeatured_image: {default_img}',
                    front_matter,
                    count=1
                )
            elif 'categories:' in front_matter:
                # categories 블록 찾기
                categories_match = re.search(r'(categories:\s*\n(?:- .+\n)+)', front_matter)
                if categories_match:
                    categories_block = categories_match.group(1)
                    front_matter = front_matter.replace(
                        categories_block,
                        f"{categories_block}featured_image: {default_img}\n"
                    )
                else:
                    # 단일 라인 categories
                    front_matter = re.sub(
                        r'(categories:.+)',
                        f'\\1\nfeatured_image: {default_img}',
                        front_matter,
                        count=1
                    )
            else:
                # 맨 끝에 추가
                front_matter = front_matter.rstrip() + f"\nfeatured_image: {default_img}\n"

            # 파일 저장
            new_content = f"---{front_matter}---{body}"
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)

            return True, f"이미지 추가: {default_img}"

    except Exception as e:
        return False, f"오류: {e}"

def main():
    content_dir = Path('content')

    print("🔧 모든 깨진 이미지 일괄 수정 시작...\n")

    # 문제 파일 목록
    broken_files = [
        # elementary
        'elementary/elementary-math-study-guide/index.md',
        # exam
        'exam/_index.md',
        # local
        'local/after-school-program-guide.md',
        'local/community-learning-center-guide.md',
        'local/mapo-english-tutor.md',
        'local/online-education-platform-guide.md',
        'local/special-purpose-high-school-guide.md',
        'local/seoul/dobong-english-tutoring.md',
        'local/seoul/dobong-math-tutoring.md',
        'local/seoul/dongdaemun-math-tutoring.md',
        'local/seoul/dongjak-math-tutoring.md',
        'local/seoul/gangbuk-english-tutoring.md',
        'local/seoul/gangbuk-math-tutoring.md',
        'local/seoul/gangdong-english-tutoring.md',
        'local/seoul/gangdong-math-tutoring.md',
        'local/seoul/gangseo-english-tutoring.md',
        'local/seoul/gangseo-math-tutoring.md',
        'local/seoul/geumcheon-english-tutoring.md',
        'local/seoul/geumcheon-math-tutoring.md',
        'local/seoul/guro-english-tutoring.md',
        'local/seoul/guro-math-tutoring.md',
        'local/seoul/gwanak-english-tutoring.md',
        'local/seoul/gwanak-math-tutoring.md',
        'local/seoul/gwangjin-english-tutoring.md',
        'local/seoul/gwangjin-math-tutoring.md',
        'local/seoul/jongno-english-tutoring.md',
        'local/seoul/jongno-math-tutoring.md',
        'local/seoul/jung-english-tutoring.md',
        'local/seoul/jung-math-tutoring.md',
        'local/seoul/jungnang-english-tutoring.md',
        'local/seoul/jungnang-math-tutoring.md',
        'local/seoul/seodaemun-english-tutoring.md',
        'local/seoul/seodaemun-math-tutoring.md',
        'local/seoul/seongbuk-english-tutoring.md',
        'local/seoul/seongbuk-math-tutoring.md',
        # subjects
        'subjects/_index.md',
        'subjects/english/_index.md',
        'subjects/korean/_index.md',
        'subjects/math/_index.md',
        'subjects/science/_index.md',
        'subjects/social/_index.md',
        # tutoring
        'tutoring/_index.md',
        'tutoring/guide/academy-vs-private.md',
        'tutoring/guide/online-video-tutoring-guide.md',
    ]

    success_count = 0
    skip_count = 0
    error_count = 0

    category_stats = {}

    for rel_path in broken_files:
        file_path = content_dir / rel_path

        if not file_path.exists():
            print(f"⚠️  파일 없음: {rel_path}")
            error_count += 1
            continue

        success, message = fix_file_image(file_path)

        category = rel_path.split('/')[0]

        if success:
            success_count += 1
            category_stats[category] = category_stats.get(category, 0) + 1
            print(f"✅ {rel_path}")
            print(f"   {message}")
        elif "수정 불필요" in message:
            skip_count += 1
        else:
            error_count += 1
            print(f"❌ {rel_path}: {message}")

    print("\n" + "=" * 80)
    print("📊 이미지 수정 완료")
    print("=" * 80)
    print(f"수정 완료: {success_count}개")
    print(f"스킵    : {skip_count}개")
    print(f"오류    : {error_count}개")

    if category_stats:
        print("\n📂 카테고리별 통계:")
        for category in sorted(category_stats.keys()):
            print(f"  {category:15s}: {category_stats[category]:3d}개 수정")

    print("=" * 80)

if __name__ == '__main__':
    main()
