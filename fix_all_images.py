#!/usr/bin/env python3
"""
전체 콘텐츠 폴더 이미지 경로 수정 스크립트 (서브폴더 포함)
- featured_image 필드
- 본문 마크다운 이미지 ![](url)
"""

import os
import re
import glob
from collections import Counter

IMAGES_DIR = "static/images"

# 사용 가능한 이미지 목록 로드
available_images = sorted([f for f in os.listdir(IMAGES_DIR) if f.startswith("edu_") and f.endswith(".jpg")])
print(f"사용 가능한 이미지: {len(available_images)}개")

# 이미지 번호별 실제 파일 매핑 생성
image_by_number = {}
for img in available_images:
    match = re.match(r'edu_(\d+)_', img)
    if match:
        num = match.group(1)
        image_by_number[num] = img

# 모든 마크다운 파일 찾기 (서브폴더 포함)
all_files = glob.glob("content/**/*.md", recursive=True)
print(f"총 파일 수: {len(all_files)}개")

# 이미지 사용 빈도 카운트
image_usage = Counter()

for filepath in all_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # featured_image 필드의 로컬 이미지
    match = re.search(r'featured_image:\s*["\']?/images/(edu_\d+_[^"\'?\s]+)', content)
    if match:
        img_name = match.group(1)
        if img_name in available_images:
            image_usage[img_name] += 1

print(f"로컬 이미지 사용 파일: {sum(image_usage.values())}개")

# 사용 빈도가 낮은 순으로 정렬
least_used_images = sorted(available_images, key=lambda x: image_usage.get(x, 0))

# 수정 카운터
fixed_featured = 0
fixed_inline = 0
fixed_mismatch = 0
least_used_idx = 0

for filepath in all_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # Case 1: featured_image 필드의 Unsplash URL
    if re.search(r'featured_image:\s*["\']?https://images\.unsplash\.com/', content):
        new_image = least_used_images[least_used_idx % len(least_used_images)]
        least_used_idx += 1

        content = re.sub(
            r'featured_image:\s*["\']?https://images\.unsplash\.com/[^"\'?\s]+(\?[^"\'\s]*)?["\']?',
            f'featured_image: "/images/{new_image}"',
            content
        )
        fixed_featured += 1
        image_usage[new_image] += 1

    # Case 2: 본문의 마크다운 이미지 ![alt](unsplash_url)
    inline_matches = re.findall(r'!\[([^\]]*)\]\(https://images\.unsplash\.com/[^)]+\)', content)
    for alt_text in inline_matches:
        new_image = least_used_images[least_used_idx % len(least_used_images)]
        least_used_idx += 1

        content = re.sub(
            r'!\[' + re.escape(alt_text) + r'\]\(https://images\.unsplash\.com/[^)]+\)',
            f'![{alt_text}](/images/{new_image})',
            content,
            count=1
        )
        fixed_inline += 1
        image_usage[new_image] += 1

    # Case 3: 로컬 이미지 경로가 실제 파일과 불일치하는 경우
    match = re.search(r'featured_image:\s*["\']?/images/(edu_(\d+)_[^"\'?\s]+)', content)
    if match:
        current_img = match.group(1)
        img_num = match.group(2)

        if current_img not in available_images:
            if img_num in image_by_number:
                correct_img = image_by_number[img_num]
                content = content.replace(
                    f'/images/{current_img}',
                    f'/images/{correct_img}'
                )
                fixed_mismatch += 1

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

print(f"\n=== 수정 완료 ===")
print(f"featured_image Unsplash 변경: {fixed_featured}개")
print(f"본문 이미지 Unsplash 변경: {fixed_inline}개")
print(f"로컬 경로 불일치 수정: {fixed_mismatch}개")
print(f"총 수정: {fixed_featured + fixed_inline + fixed_mismatch}개")

# 검증
remaining = 0
for filepath in all_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        if 'unsplash.com' in f.read():
            remaining += 1

print(f"\n남은 Unsplash URL: {remaining}개")
