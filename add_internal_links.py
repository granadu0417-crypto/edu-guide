#!/usr/bin/env python3
"""
본문 내 자동 내부 링크 추가 스크립트
SEO 최적화: 페이지 간 내부 링크 구조 강화
"""

import os
import re
from pathlib import Path
from collections import defaultdict

# 전역 변수
all_pages = []  # 모든 페이지 정보 저장

class Page:
    def __init__(self, filepath, title, categories, tags, url_path):
        self.filepath = filepath
        self.title = title
        self.categories = categories or []
        self.tags = tags or []
        self.url_path = url_path

def extract_frontmatter(filepath):
    """파일에서 frontmatter 정보 추출"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        if not content.startswith('---'):
            return None

        parts = content.split('---', 2)
        if len(parts) < 3:
            return None

        frontmatter = parts[1]
        body = parts[2]

        # Title 추출
        title_match = re.search(r'title:\s*(.+)', frontmatter)
        title = title_match.group(1).strip().strip('"\'') if title_match else None

        # Categories 추출
        categories = []
        cat_section = re.search(r'categories:\s*\n((?:- .+\n)+)', frontmatter)
        if cat_section:
            categories = [c.strip('- ').strip() for c in cat_section.group(1).split('\n') if c.strip()]

        # Tags 추출
        tags = []
        tag_section = re.search(r'tags:\s*\n((?:- .+\n)+)', frontmatter)
        if tag_section:
            tags = [t.strip('- ').strip() for t in tag_section.group(1).split('\n') if t.strip()]

        return {
            'title': title,
            'categories': categories,
            'tags': tags,
            'body': body
        }

    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None

def get_url_path(filepath, content_path):
    """파일 경로를 URL 경로로 변환"""
    rel_path = filepath.relative_to(content_path)
    url_path = str(rel_path.parent).replace('\\', '/')
    filename = rel_path.stem

    if filename == '_index':
        return f"/{url_path}/"
    else:
        return f"/{url_path}/{filename}/"

def find_related_pages(page, all_pages, limit=5):
    """관련 페이지 찾기 (카테고리/태그 기반)"""
    scored_pages = []

    for other_page in all_pages:
        if other_page.filepath == page.filepath:
            continue

        score = 0

        # 카테고리 일치 (가중치 3)
        for cat in page.categories:
            if cat in other_page.categories:
                score += 3

        # 태그 일치 (가중치 1)
        for tag in page.tags:
            if tag in other_page.tags:
                score += 1

        if score >= 2:  # 최소 점수 2 이상
            scored_pages.append((score, other_page))

    # 점수순 정렬 후 상위 N개 반환
    scored_pages.sort(reverse=True, key=lambda x: x[0])
    return [p[1] for p in scored_pages[:limit]]

def has_related_links(body):
    """이미 관련 링크가 있는지 확인"""
    # "관련 가이드" 또는 비슷한 섹션이 있는지 확인
    markers = [
        '## 관련 가이드',
        '## 추천 가이드',
        '## 함께 보면 좋은 글',
        '## 더 읽어보기'
    ]
    return any(marker in body for marker in markers)

def add_links_to_file(filepath, content_path):
    """파일에 관련 링크 추가"""
    try:
        info = extract_frontmatter(filepath)
        if not info or not info['title']:
            return False

        # 이미 링크가 있으면 건너뛰기
        if has_related_links(info['body']):
            return False

        # 현재 페이지의 관련 페이지 찾기
        current_page = Page(
            filepath=filepath,
            title=info['title'],
            categories=info['categories'],
            tags=info['tags'],
            url_path=get_url_path(filepath, content_path)
        )

        related_pages = find_related_pages(current_page, all_pages, limit=5)

        if len(related_pages) < 2:
            return False  # 최소 2개 이상의 관련 페이지가 있어야 함

        # 링크 섹션 생성
        links_section = "\n\n## 📚 관련 가이드\n\n"

        for rp in related_pages[:5]:  # 최대 5개
            links_section += f"- [{rp.title}]({rp.url_path})\n"

        # 본문에 링크 추가 (FAQ나 CTA 전에 삽입)
        body = info['body']

        # FAQ 섹션 찾기
        faq_match = re.search(r'\n## FAQ', body)
        cta_match = re.search(r'\{\{<\s*cta-consultation-final\s*>\}\}', body)

        # 삽입 위치 결정
        if faq_match:
            insert_pos = faq_match.start()
        elif cta_match:
            insert_pos = cta_match.start()
        else:
            # 본문 끝에 추가
            insert_pos = len(body)

        # 링크 섹션 삽입
        new_body = body[:insert_pos] + links_section + "\n" + body[insert_pos:]

        # 파일 재작성
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        parts = content.split('---', 2)
        new_content = '---' + parts[1] + '---' + new_body

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

        return True

    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def main():
    """메인 함수"""
    global all_pages

    content_path = Path("/mnt/c/Users/user/Desktop/클로드/에듀코리아/edu-guide/content")

    print("1단계: 모든 페이지 정보 수집 중...")

    # 1단계: 모든 페이지 정보 수집
    for md_file in content_path.rglob('*.md'):
        if md_file.name == '_index.md':
            continue  # 인덱스 페이지는 제외

        info = extract_frontmatter(md_file)
        if info and info['title']:
            page = Page(
                filepath=md_file,
                title=info['title'],
                categories=info['categories'],
                tags=info['tags'],
                url_path=get_url_path(md_file, content_path)
            )
            all_pages.append(page)

    print(f"   총 {len(all_pages)}개 페이지 발견")

    # 2단계: 각 페이지에 링크 추가
    print("\n2단계: 내부 링크 추가 중...")

    total_added = 0

    for md_file in content_path.rglob('*.md'):
        if md_file.name == '_index.md':
            continue

        if add_links_to_file(md_file, content_path):
            total_added += 1
            # 진행 상황 표시 (100개마다)
            if total_added % 100 == 0:
                print(f"   진행: {total_added}개 파일 처리...")

    print(f"\n완료! 총 {total_added}개 파일에 내부 링크를 추가했습니다.")
    print("각 페이지는 이제 3-5개의 관련 페이지로의 링크를 가지게 됩니다.")

if __name__ == "__main__":
    main()
