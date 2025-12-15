#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
이미지 URL 실제 접근 가능 여부 검사
- HTTP HEAD 요청으로 실제 확인
- 깨진 이미지 목록 출력
"""

import re
import urllib.request
import urllib.error
import ssl
from pathlib import Path
from collections import defaultdict
import concurrent.futures

# SSL 인증서 검증 비활성화 (일부 환경에서 필요)
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

def extract_image_urls():
    """모든 md 파일에서 featured_image URL 추출"""
    content_dir = Path('/home/user/edu-guide/content')
    folders = ['high', 'middle', 'local', 'tutoring', 'subjects', 'elementary', 'exam', 'consultation']

    url_to_files = defaultdict(list)

    for folder in folders:
        folder_path = content_dir / folder
        if not folder_path.exists():
            continue

        for md_file in folder_path.glob('*.md'):
            if md_file.stem == '_index':
                continue
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                match = re.search(r'featured_image:\s*["\']?(https://[^"\'\n]+)', content)
                if match:
                    url = match.group(1).strip()
                    url_to_files[url].append(str(md_file))
            except Exception as e:
                print(f"Error reading {md_file}: {e}")

    return url_to_files

def check_url(url, timeout=15):
    """URL이 유효한지 확인"""
    try:
        req = urllib.request.Request(url, method='HEAD')
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        with urllib.request.urlopen(req, timeout=timeout, context=ssl_context) as response:
            return response.status == 200, response.status
    except urllib.error.HTTPError as e:
        return False, e.code
    except urllib.error.URLError as e:
        return False, str(e.reason)[:30]
    except Exception as e:
        return False, str(e)[:30]

def check_single_url(args):
    """단일 URL 검사 (병렬 처리용)"""
    url, files = args
    is_valid, status = check_url(url)
    photo_match = re.search(r'photo-[\w-]+', url)
    photo_id = photo_match.group(0) if photo_match else "unknown"
    return url, files, is_valid, status, photo_id

def main():
    print("이미지 URL 추출 중...")
    url_to_files = extract_image_urls()

    print(f"총 {len(url_to_files)}개의 고유 이미지 URL 발견")
    print("=" * 60)

    broken_images = []
    valid_count = 0

    print("\n이미지 URL 유효성 검사 중... (시간이 걸릴 수 있습니다)")

    # 병렬로 URL 검사
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(check_single_url, (url, files)): url
                   for url, files in url_to_files.items()}

        for i, future in enumerate(concurrent.futures.as_completed(futures)):
            url, files, is_valid, status, photo_id = future.result()

            if is_valid:
                valid_count += 1
            else:
                broken_images.append((url, files, photo_id, status))

            # 진행 상황 (20개마다)
            if (i + 1) % 20 == 0:
                print(f"  진행: {i + 1}/{len(url_to_files)}")

    print("\n" + "=" * 60)
    print(f"검사 완료: 유효 {valid_count}개, 깨진 이미지 {len(broken_images)}개")

    if broken_images:
        print("\n=== 깨진 이미지 목록 ===")
        for url, files, photo_id, status in sorted(broken_images, key=lambda x: len(x[1]), reverse=True):
            print(f"\n❌ {photo_id} (상태: {status})")
            print(f"   URL: {url}")
            print(f"   사용 파일 ({len(files)}개):")
            for f in files[:5]:
                rel_path = f.replace('/home/user/edu-guide/', '')
                print(f"     - {rel_path}")
            if len(files) > 5:
                print(f"     ... 외 {len(files) - 5}개")

        # 총 영향받는 파일 수
        total_affected = sum(len(files) for _, files, _, _ in broken_images)
        print(f"\n총 영향받는 파일: {total_affected}개")
    else:
        print("\n✅ 모든 이미지가 유효합니다!")

if __name__ == '__main__':
    main()
