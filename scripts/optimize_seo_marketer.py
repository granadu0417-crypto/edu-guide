#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
마케터 관점의 SEO 최적화 스크립트
- 불필요한 "지역" 접두사 제거
- 검색 친화적 제목 최적화
- 자연스러운 키워드 배치
"""

import os
import re
from pathlib import Path

def read_file(file_path):
    """파일 읽기"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"  ❌ 읽기 실패: {e}")
        return None

def write_file(file_path, content):
    """파일 쓰기"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"  ❌ 쓰기 실패: {e}")
        return False

def optimize_seo(file_path):
    """SEO 최적화"""
    content = read_file(file_path)
    if not content:
        return False

    lines = content.split('\n')
    modified = False
    new_lines = []
    in_front_matter = False
    front_matter_count = 0

    for line in lines:
        # Front Matter 경계 확인
        if line.strip() == '---':
            front_matter_count += 1
            in_front_matter = front_matter_count == 1
            new_lines.append(line)
            continue

        # Front Matter 외부는 그대로
        if not in_front_matter:
            new_lines.append(line)
            continue

        # Title 최적화
        if line.startswith('title:'):
            original_line = line

            # 제목 추출
            match = re.search(r'title:\s*["\'](.+)["\']', line)
            if match:
                title = match.group(1)
                original_title = title

                # 불필요한 "지역" 접두사 제거 (단, "지역아동센터", "지역정보" 같은 고유명사는 유지)
                if title.startswith('지역 '):
                    # "지역 " 다음이 실제 내용일 경우에만 제거
                    if not title.startswith('지역아동') and not title.startswith('지역정보'):
                        title = title.replace('지역 ', '', 1)
                        modified = True
                        print(f"  수정: 제목 '지역' 접두사 제거")
                        print(f"    변경 전: {original_title}")
                        print(f"    변경 후: {title}")

                # 새로운 title 라인 생성
                new_line = f'title: "{title}"'
                new_lines.append(new_line)
            else:
                new_lines.append(line)
            continue

        # keywords 필드 완전히 제거 (SEO 관점에서 불필요)
        if line.strip().startswith('keywords:'):
            modified = True
            print(f"  제거: keywords 필드")
            continue  # 이 라인을 건너뜀

        # tags 최적화: 불필요한 일반 키워드 제거
        if line.startswith('tags:'):
            original_line = line

            # 제거할 일반 키워드들 (너무 포괄적이어서 SEO 가치 낮음)
            remove_keywords = ['지역', '서울', '경기', '학원가', '교육특구']

            new_line = line
            for keyword in remove_keywords:
                # tags 배열에서 해당 키워드 제거
                new_line = re.sub(rf'["\'],?\s*"{keyword}"', '', new_line)
                new_line = re.sub(rf'"{keyword}"["\'],?\s*', '', new_line)

            # 빈 요소나 중복 쉼표 정리
            new_line = re.sub(r',\s*,', ',', new_line)
            new_line = re.sub(r'\[\s*,', '[', new_line)
            new_line = re.sub(r',\s*\]', ']', new_line)

            if new_line != line:
                modified = True
                print(f"  수정: tags에서 일반 키워드 제거")

            new_lines.append(new_line)
            continue

        # 나머지 라인은 그대로
        new_lines.append(line)

    if modified:
        new_content = '\n'.join(new_lines)
        return write_file(file_path, new_content)

    return False

def main():
    """메인 실행 함수"""
    content_dir = Path('content')

    if not content_dir.exists():
        print("❌ content 디렉토리를 찾을 수 없습니다.")
        return

    # 모든 마크다운 파일 찾기
    md_files = list(content_dir.rglob('*.md'))

    print(f"🔍 총 {len(md_files)}개 파일 SEO 최적화 시작...\n")

    optimized_count = 0
    skipped_count = 0

    # 카테고리별로 정리하여 처리
    from collections import defaultdict
    categories = defaultdict(list)

    for md_file in md_files:
        rel_path = md_file.relative_to(content_dir)
        category = rel_path.parts[0] if len(rel_path.parts) > 1 else 'root'
        categories[category].append(md_file)

    for category in sorted(categories.keys()):
        files = categories[category]
        print(f"\n📁 {category.upper()} ({len(files)}개 파일)")
        print("-" * 80)

        for md_file in files:
            print(f"처리: {md_file.name}")

            if optimize_seo(md_file):
                optimized_count += 1
                print(f"  ✅ 최적화 완료")
            else:
                skipped_count += 1
                print(f"  ⏭️  변경사항 없음")

    print(f"\n{'='*80}")
    print(f"✅ SEO 최적화 완료!")
    print(f"{'='*80}")
    print(f"최적화 완료: {optimized_count}개")
    print(f"변경 없음: {skipped_count}개")
    print(f"총: {len(md_files)}개")
    print(f"{'='*80}")

if __name__ == '__main__':
    main()
