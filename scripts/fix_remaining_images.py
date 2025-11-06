#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
남은 깨진 이미지 수정
"""

from pathlib import Path
import re

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
            return False, "이미지 없음"

    except Exception as e:
        return False, f"오류: {e}"

def main():
    content_dir = Path('content')

    print("🔧 남은 깨진 이미지 수정 시작...\n")

    # 남은 문제 파일 목록
    remaining_files = [
        'local/seoul/gangnam-english-tutoring.md',
        'local/seoul/gangnam-math-tutoring-REWRITE.md',
        'local/seoul/gangnam-math-tutoring.md',
        'local/seoul/mapo-english-tutoring.md',
        'local/seoul/mapo-math-tutoring.md',
        'local/seoul/nowon-math-tutoring.md',
        'local/seoul/seocho-english-tutoring.md',
        'local/seoul/seongdong-english-tutoring.md',
        'local/seoul/songpa-math-tutoring.md',
        'local/seoul/yangcheon-english-tutoring.md',
        'local/seoul/yangcheon-math-tutoring.md',
        'local/seoul/yeongdeungpo-math-tutoring.md',
    ]

    success_count = 0
    skip_count = 0
    error_count = 0

    for rel_path in remaining_files:
        file_path = content_dir / rel_path

        if not file_path.exists():
            print(f"⚠️  파일 없음: {rel_path}")
            error_count += 1
            continue

        success, message = fix_file_image(file_path)

        if success:
            success_count += 1
            print(f"✅ {rel_path}")
            print(f"   {message}")
        elif "수정 불필요" in message:
            skip_count += 1
            print(f"⏭️  {rel_path}: {message}")
        else:
            error_count += 1
            print(f"❌ {rel_path}: {message}")

    print("\n" + "=" * 80)
    print("📊 이미지 수정 완료")
    print("=" * 80)
    print(f"수정 완료: {success_count}개")
    print(f"스킵    : {skip_count}개")
    print(f"오류    : {error_count}개")
    print("=" * 80)

if __name__ == '__main__':
    main()
