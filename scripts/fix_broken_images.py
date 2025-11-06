#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
깨진 이미지 찾아서 교체하는 스크립트
"""

from pathlib import Path
import re
import requests
from collections import defaultdict
import random
import time

# 검증된 고품질 교육 이미지 풀
VERIFIED_IMAGES = [
    "photo-1456513080510-7bf3a84b82f8", "photo-1434030216411-0b793f4b4173",
    "photo-1488190211105-8b0e65b80b4e", "photo-1516979187457-637abb4f9353",
    "photo-1522202176988-66273c2fd55f", "photo-1524995997946-a1c2e315a42f",
    "photo-1509062522246-3755977927d7", "photo-1503676260728-1c00da094a0b",
    "photo-1427504494785-3a9ca7044f45", "photo-1503454537195-1dcabb73ffb9",
    "photo-1524178232363-1fb2b075b655", "photo-1455390582262-044cdead277a",
    "photo-1450101499163-c8848c66ca85", "photo-1484480974693-6ca0a78fb36b",
    "photo-1454165804606-c3d57bc86b40", "photo-1542626991-cbc4e32524cc",
    "photo-1517842645767-c639042777db", "photo-1523240795612-9a054b0db644",
    "photo-1491841651911-c44c30c34548", "photo-1513258496099-48168024aec0",
    "photo-1497633762265-9d179a990aa6", "photo-1512820790803-83ca734da794",
    "photo-1506880018603-83d5b814b5a6", "photo-1495446815901-a7297e633e8d",
    "photo-1519682337058-a94d519337bc", "photo-1521587760476-6c12a4b040da",
    "photo-1526243741027-444d633d7365", "photo-1532012197267-da84d127e765",
    "photo-1481627834876-b7833e8f5570", "photo-1519337265831-281ec6cc8514",
    "photo-1546410531-bb4caa6b424d", "photo-1457369804613-52c61a468e7d",
    "photo-1523289333742-be1143f6b766", "photo-1523050854058-8df90110c9f1",
    "photo-1515378791036-0648a3ef77b2", "photo-1488190211105-8b0e65b80b4e",
    "photo-1529070538774-1843cb3265df", "photo-1516397281156-ca07cf9746fc",
    "photo-1531545514256-b1400bc00f31", "photo-1499750310107-5fef28a66643",
    "photo-1519389950473-47ba0277781c", "photo-1522071820081-009f0129c71c",
    "photo-1556761175-5973dc0f32e7", "photo-1486312338219-ce68d2c6f44d",
    "photo-1515378960530-7c0da6231fb1", "photo-1521737604893-d14cc237f11d",
    "photo-1522199755839-a2bacb67c546", "photo-1498050108023-c5249f4df085",
    "photo-1551434678-e076c223a692", "photo-1517048676732-d65bc937f952",
    "photo-1504384308090-c894fdcc538d", "photo-1542744173-8e7e53415bb0",
    "photo-1516321165247-4aa89a48be28", "photo-1487058792275-0ad4aaf24ca7",
    "photo-1511376777868-611b54f68947", "photo-1506784983877-45594efa4cbe",
    "photo-1525338078858-d762b5e32f2c", "photo-1507925921958-8a62f3d1a50d",
    "photo-1531346878377-a5be20888e57", "photo-1513151233558-d860c5398176",
    "photo-1513506003901-1e6a229e2d15", "photo-1497215842964-222b430dc094",
    "photo-1522881193457-37ae97c905bf", "photo-1523580494863-6f3031224c94",
    "photo-1528459801416-a9e53bbf4e17", "photo-1554048612-b6a482bc67e5",
    "photo-1556740758-90de374c12ad", "photo-1573164574230-db1d5e960238",
    "photo-1580894894513-541e068a3e2b", "photo-1587825140708-dfaf72ae4b04",
    "photo-1588072432836-e10032774350", "photo-1588702547919-26089e690ecc",
    "photo-1589829085413-56de8ae18c73", "photo-1590402494587-44b71d7772f6",
    "photo-1591123120675-6f7f1aae0e5b", "photo-1592280771190-3e2e4d571952",
    "photo-1593642532973-d31b6557fa68", "photo-1595152772835-219674b2a8a6",
    "photo-1596464716127-f2a82984de30", "photo-1596496181848-3091d4878b24",
    "photo-1596496181871-9681eacf9764", "photo-1598520106830-8c45c2035460",
    "photo-1606326608606-aa0b62935f2b", "photo-1610484826967-09c5720778c7",
    "photo-1611348586804-61bf6c080437", "photo-1616400619175-5beda3a17896",
    "photo-1622782914767-404fb9ab3f57", "photo-1635070041078-e363dbe005cb",
    "photo-1635070041409-bbec93146e3f", "photo-1472289065668-ce650ac443d2",
    "photo-1517694712202-14dd9538aa97", "photo-1472173148041-00294f0814a2",
    "photo-1485988412941-77a35537dae4", "photo-1521721839743-2e446fc17948",
]

def create_unsplash_url(photo_id):
    """Unsplash 사진 ID로 최적화된 URL 생성"""
    return f"https://images.unsplash.com/{photo_id}?w=1200&h=630&fit=crop"

def check_image_url(url, timeout=5):
    """이미지 URL이 유효한지 확인"""
    try:
        response = requests.head(url, timeout=timeout, allow_redirects=True)
        return response.status_code == 200
    except:
        return False

def extract_photo_id(url):
    """URL에서 photo ID 추출"""
    match = re.search(r'photo-[\w-]+', url)
    return match.group(0) if match else None

def find_all_images(content_dir):
    """모든 마크다운 파일에서 featured_image 추출"""
    images = {}

    for md_file in content_dir.glob('**/*.md'):
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()

            match = re.search(r'^featured_image:\s*(.+)$', content, re.MULTILINE)
            if match:
                image_url = match.group(1).strip()
                if image_url not in images:
                    images[image_url] = []
                images[image_url].append(str(md_file))
        except:
            continue

    return images

def replace_image_in_file(file_path, old_image, new_image):
    """파일의 이미지를 교체"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        new_content = re.sub(
            r'^featured_image:\s*' + re.escape(old_image) + r'\s*$',
            f'featured_image: {new_image}',
            content,
            flags=re.MULTILINE
        )

        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True
        return False
    except Exception as e:
        print(f"❌ 오류: {file_path} - {e}")
        return False

def main():
    content_dir = Path('content')

    print("🔍 이미지 체크 시작...\n")

    # 1. 모든 이미지 URL 수집
    print("📋 이미지 URL 수집 중...")
    all_images = find_all_images(content_dir)
    print(f"   총 {len(all_images)}개의 고유 이미지 발견\n")

    # 2. 각 이미지 URL 유효성 검사
    print("🧪 이미지 유효성 검사 중...\n")
    broken_images = {}
    checked = 0

    for image_url, file_list in all_images.items():
        checked += 1
        print(f"   [{checked}/{len(all_images)}] 체크 중...", end='\r')

        is_valid = check_image_url(image_url)

        if not is_valid:
            broken_images[image_url] = file_list
            print(f"\n❌ 깨진 이미지: {image_url[:60]}... ({len(file_list)}개 파일)")

        time.sleep(0.1)  # Rate limiting

    print(f"\n\n{'=' * 80}")
    print(f"📊 검사 완료")
    print(f"{'=' * 80}")
    print(f"전체 이미지: {len(all_images)}개")
    print(f"깨진 이미지: {len(broken_images)}개")
    print(f"정상 이미지: {len(all_images) - len(broken_images)}개")

    if not broken_images:
        print("\n✅ 모든 이미지가 정상입니다!")
        return

    # 3. 깨진 이미지 교체
    print(f"\n🔧 깨진 이미지 교체 시작...\n")

    random.shuffle(VERIFIED_IMAGES)
    image_index = 0
    replaced_count = 0
    total_files = sum(len(files) for files in broken_images.values())

    for broken_url, file_list in broken_images.items():
        for file_path in file_list:
            if image_index >= len(VERIFIED_IMAGES):
                print("\n⚠️  검증된 이미지 소진")
                break

            new_image = create_unsplash_url(VERIFIED_IMAGES[image_index])
            image_index += 1

            if replace_image_in_file(file_path, broken_url, new_image):
                replaced_count += 1
                rel_path = str(Path(file_path).relative_to(content_dir))
                if replaced_count <= 10:
                    print(f"✅ [{replaced_count}] {rel_path}")

        if image_index >= len(VERIFIED_IMAGES):
            break

    print(f"\n{'=' * 80}")
    print(f"📊 이미지 교체 완료")
    print(f"{'=' * 80}")
    print(f"교체된 파일: {replaced_count}개 / {total_files}개")
    print(f"사용된 이미지: {image_index}개")
    print(f"성공률: {replaced_count / total_files * 100:.1f}%")
    print(f"{'=' * 80}")

if __name__ == '__main__':
    main()
