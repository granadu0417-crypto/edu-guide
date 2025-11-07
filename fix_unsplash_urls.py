#!/usr/bin/env python3
"""
Unsplash Source API URL 수정 스크립트
폐기된 source.unsplash.com을 images.unsplash.com으로 교체
"""

import os
import re
from pathlib import Path

# 대체할 이미지 풀
REPLACEMENT_IMAGES = [
    "https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=1200&h=630&fit=crop",  # 공부하는 학생
    "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=1200&h=630&fit=crop",  # 책상과 노트
    "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=1200&h=630&fit=crop",  # 펜과 노트
    "https://images.unsplash.com/photo-1427504494785-3a9ca7044f45?w=1200&h=630&fit=crop",  # 교실
    "https://images.unsplash.com/photo-1509062522246-3755977927d7?w=1200&h=630&fit=crop",  # 학습 자료
    "https://images.unsplash.com/photo-1497215842964-222b430dc094?w=1200&h=630&fit=crop",  # 컴퓨터와 학습
    "https://images.unsplash.com/photo-1488998427799-e3362cec87c3?w=1200&h=630&fit=crop",  # 노트북
    "https://images.unsplash.com/photo-1513001900722-370f803f498d?w=1200&h=630&fit=crop",  # 책과 공부
    "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=1200&h=630&fit=crop",  # 그룹 학습
    "https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=1200&h=630&fit=crop",  # 회의/토론
]

def fix_unsplash_url(filepath):
    """파일의 source.unsplash.com URL을 images.unsplash.com으로 교체"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # source.unsplash.com URL 패턴 찾기
        pattern = r'https://source\.unsplash\.com/[^\s"\')]+'
        matches = re.findall(pattern, content)

        if not matches:
            return False

        # 각 매치에 대해 대체 이미지 할당 (파일 경로 기반 해시로 일관성 유지)
        import hashlib
        file_hash = int(hashlib.md5(str(filepath).encode()).hexdigest(), 16)

        for i, match in enumerate(matches):
            # 파일별로 일관된 이미지 선택
            img_index = (file_hash + i) % len(REPLACEMENT_IMAGES)
            replacement = REPLACEMENT_IMAGES[img_index]
            content = content.replace(match, replacement)

        # 변경사항이 있으면 파일 쓰기
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
    content_path = Path("/mnt/c/Users/user/Desktop/클로드/에듀코리아/edu-guide/content")

    print("Unsplash Source API URL 수정 중...\n")

    fixed_count = 0
    skipped_count = 0
    error_count = 0

    for md_file in content_path.rglob('*.md'):
        try:
            if fix_unsplash_url(md_file):
                fixed_count += 1
                print(f"✅ {md_file.name}")
            else:
                skipped_count += 1
        except Exception as e:
            print(f"❌ Error: {md_file.name} - {e}")
            error_count += 1

    # 결과 출력
    print("\n" + "=" * 80)
    print(f"\n📊 URL 수정 완료\n")
    print(f"✅ 수정됨: {fixed_count}개")
    print(f"⏭️  건너뜀: {skipped_count}개")
    print(f"❌ 오류: {error_count}개")
    print(f"\n총 처리: {fixed_count + skipped_count + error_count}개\n")

if __name__ == "__main__":
    main()
