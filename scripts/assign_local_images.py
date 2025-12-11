#!/usr/bin/env python3
"""
로컬 이미지 분배 스크립트
- 1000개 이미지를 3001개 게시물에 분배
- 인접 게시물이 같은 이미지를 사용하지 않도록 함
"""

import os
import re
import glob

# 설정
CONTENT_DIR = "/home/user/edu-guide/content"
IMAGE_LIST_FILE = "/tmp/local_images.txt"

# 이미지 목록 로드
with open(IMAGE_LIST_FILE, 'r') as f:
    images = [line.strip() for line in f if line.strip().startswith('edu_')]

print(f"총 {len(images)}개 이미지 로드됨")

# 마크다운 파일 목록 (폴더별로 정렬)
md_files = sorted(glob.glob(f"{CONTENT_DIR}/**/*.md", recursive=True))
print(f"총 {len(md_files)}개 마크다운 파일")

# featured_image 패턴
pattern = re.compile(r'^featured_image:\s*["\']?https://images\.unsplash\.com/[^"\']*["\']?', re.MULTILINE)

updated_count = 0
error_count = 0

for i, filepath in enumerate(md_files):
    # 이미지 인덱스 (0~999 순환)
    img_index = i % len(images)
    image_filename = images[img_index]
    new_image_path = f"/images/{image_filename}"

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # featured_image가 있는지 확인
        if 'featured_image:' in content:
            # Unsplash URL을 로컬 경로로 변경
            new_content = pattern.sub(f'featured_image: "{new_image_path}"', content)

            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                updated_count += 1

                if updated_count <= 5 or updated_count % 500 == 0:
                    print(f"[{updated_count}] {os.path.basename(filepath)} → {image_filename}")
    except Exception as e:
        error_count += 1
        print(f"오류: {filepath} - {e}")

print(f"\n완료! 업데이트: {updated_count}개, 오류: {error_count}개")
