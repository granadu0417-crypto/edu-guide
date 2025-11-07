#!/usr/bin/env python3
"""
마크다운 파일의 본문 첫 번째 # 제목을 ## 로 변경하는 스크립트
SEO 최적화: 페이지당 H1 태그는 1개만 있어야 함 (템플릿에서 제공)
"""

import os
import re
from pathlib import Path

def fix_h1_in_file(filepath):
    """파일의 본문 첫 번째 # 제목을 ## 로 변경"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # frontmatter와 본문 분리
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                frontmatter = parts[1]
                body = parts[2]

                # 본문에서 첫 번째 # 제목 찾기 (줄 시작에 있는 것만)
                # ^# 로 시작하는 첫 번째 라인만 변경
                lines = body.split('\n')
                modified = False

                for i, line in enumerate(lines):
                    # 빈 줄이나 공백만 있는 줄은 건너뛰기
                    if line.strip() and line.startswith('# '):
                        lines[i] = '##' + line[1:]  # # 를 ## 로 변경
                        modified = True
                        break  # 첫 번째 것만 변경

                if modified:
                    new_content = '---' + frontmatter + '---' + '\n'.join(lines)

                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    return True

        return False

    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def main():
    """메인 함수"""
    content_path = Path("/mnt/c/Users/user/Desktop/클로드/에듀코리아/edu-guide/content")

    total_fixed = 0

    print("마크다운 파일 검사 중...")

    # 모든 .md 파일 찾기
    for md_file in content_path.rglob('*.md'):
        if fix_h1_in_file(md_file):
            total_fixed += 1
            # 진행 상황 표시 (100개마다)
            if total_fixed % 100 == 0:
                print(f"  진행: {total_fixed}개 파일 수정...")

    print(f"\n완료! 총 {total_fixed}개 파일의 H1 태그를 H2로 변경했습니다.")
    print("이제 각 페이지는 템플릿의 H1 태그만 가지게 됩니다. (SEO 최적화)")

if __name__ == "__main__":
    main()
