#!/usr/bin/env python3
"""
중복된 description을 가진 마크다운 파일 찾기
SEO 최적화: 각 페이지는 고유한 description을 가져야 함
"""

import os
import re
from pathlib import Path
from collections import defaultdict

def extract_description(filepath):
    """파일의 description 필드 추출"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # frontmatter 추출
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                frontmatter = parts[1]

                # description 찾기 (여러 줄일 수 있음)
                desc_match = re.search(r'description:\s*(.+?)(?=\n[a-z_]+:|$)', frontmatter, re.DOTALL)
                if desc_match:
                    desc = desc_match.group(1).strip()
                    # 줄바꿈 제거하고 공백 정리
                    desc = ' '.join(desc.split())
                    # 따옴표 제거
                    desc = desc.strip('"\'')
                    return desc

        return None

    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return None

def main():
    """메인 함수"""
    content_path = Path("/mnt/c/Users/user/Desktop/클로드/에듀코리아/edu-guide/content")

    # description별로 파일 그룹화
    desc_to_files = defaultdict(list)

    print("마크다운 파일 검사 중...")

    # 모든 .md 파일 검사
    for md_file in content_path.rglob('*.md'):
        desc = extract_description(md_file)
        if desc:
            # 상대 경로로 변환
            rel_path = md_file.relative_to(content_path)
            desc_to_files[desc].append(str(rel_path))

    # 중복된 description 찾기
    duplicates = {desc: files for desc, files in desc_to_files.items() if len(files) > 1}

    if duplicates:
        print(f"\n🚨 중복된 description 발견: {len(duplicates)}개\n")

        total_files = 0
        for desc, files in sorted(duplicates.items(), key=lambda x: len(x[1]), reverse=True):
            print(f"📝 Description (길이: {len(desc)}자):")
            print(f"   '{desc[:100]}{'...' if len(desc) > 100 else ''}'")
            print(f"   사용 파일: {len(files)}개")
            for file in files[:5]:  # 처음 5개만 표시
                print(f"      - {file}")
            if len(files) > 5:
                print(f"      ... 외 {len(files) - 5}개")
            print()
            total_files += len(files)

        print(f"총 {total_files}개 파일이 중복된 description을 사용하고 있습니다.")
        print("\n💡 각 파일에 고유한 description을 작성해야 합니다.")

    else:
        print("✅ 중복된 description이 없습니다!")

if __name__ == "__main__":
    main()
