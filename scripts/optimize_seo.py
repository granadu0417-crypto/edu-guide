#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SEO 최적화 스크립트
제목, 메타 설명, 키워드를 검색 최적화
"""

import os
import re
from pathlib import Path

# SEO 키워드 데이터베이스
SEO_KEYWORDS = {
    'elementary': {
        'primary': ['초등학생', '초등', '초등교육', '초등학교'],
        'secondary': ['공부법', '학습법', '학습전략', '교육', '학원', '과외']
    },
    'middle': {
        'primary': ['중학생', '중학교', '중등', '중등교육'],
        'secondary': ['내신', '공부법', '학습법', '시험대비', '학원', '과외']
    },
    'high': {
        'primary': ['고등학생', '고등학교', '고등', '수능'],
        'secondary': ['입시', '내신', '대학', '공부법', '학원', '과외']
    },
    'subjects': {
        'korean': ['국어', '국어공부', '국어학습', '독해', '문법', '작문'],
        'english': ['영어', '영어공부', '영어학습', '영문법', '영어회화', '영어독해'],
        'math': ['수학', '수학공부', '수학학습', '수학문제', '연산', '도형'],
        'science': ['과학', '과학공부', '과학학습', '실험', '탐구'],
        'social': ['사회', '사회공부', '지리', '역사', '일반사회']
    },
    'exam': {
        'primary': ['시험', '시험대비', '중간고사', '기말고사', '모의고사'],
        'secondary': ['공부법', '학습전략', '오답노트', '시험준비']
    },
    'tutoring': {
        'primary': ['과외', '학원', '개인과외', '그룹과외', '화상과외'],
        'secondary': ['선생님', '교사', '강사', '1대1', '맞춤학습']
    },
    'local': {
        'primary': ['지역', '서울', '경기', '강남', '강동', '강북', '강서'],
        'secondary': ['학원가', '교육특구', '대치동', '목동', '중계동']
    }
}

# 검색 최적화 제목 패턴
TITLE_PATTERNS = {
    'guide': '{keyword} 완벽 가이드 | {detail}',
    'strategy': '{keyword} {detail} 전략',
    'method': '{keyword} {detail} 방법',
    'tips': '{keyword} {detail} 꿀팁',
    'comparison': '{keyword} vs {keyword2} | 선택 가이드'
}

def extract_front_matter(content):
    """Front Matter 추출"""
    match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if match:
        return match.group(1), match.end()
    return None, 0

def parse_front_matter(front_matter):
    """Front Matter 파싱"""
    data = {}
    for line in front_matter.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip().strip('"')
            data[key] = value
    return data

def get_category_from_path(file_path):
    """파일 경로에서 카테고리 추출"""
    parts = file_path.parts
    for part in parts:
        if part in SEO_KEYWORDS:
            return part

    # subjects 하위 카테고리 확인
    if 'subjects' in parts:
        for i, part in enumerate(parts):
            if part == 'subjects' and i + 1 < len(parts):
                subject = parts[i + 1]
                if subject in SEO_KEYWORDS['subjects']:
                    return f'subjects.{subject}'

    return 'general'

def get_seo_keywords(category):
    """카테고리별 SEO 키워드 반환"""
    if '.' in category:
        main, sub = category.split('.')
        keywords = SEO_KEYWORDS.get(main, {}).get(sub, [])
    else:
        cat_data = SEO_KEYWORDS.get(category, {})
        keywords = cat_data.get('primary', []) + cat_data.get('secondary', [])

    return keywords

def optimize_title(title, category_keywords):
    """제목 SEO 최적화"""
    # 이미 키워드가 앞에 있으면 그대로 유지
    for keyword in category_keywords[:3]:
        if title.startswith(keyword):
            return title

    # 제목이 너무 길면 압축
    if len(title) > 60:
        title = title[:57] + '...'

    # 주요 키워드가 없으면 추가
    has_keyword = any(kw in title for kw in category_keywords[:5])
    if not has_keyword and category_keywords:
        title = f"{category_keywords[0]} {title}"

    return title

def optimize_description(description, category_keywords):
    """메타 설명 SEO 최적화"""
    if not description or len(description) < 80:
        # 짧으면 키워드 추가
        if category_keywords:
            prefix = ', '.join(category_keywords[:3])
            description = f"{prefix}에 대한 완벽 가이드. {description}"

    # 너무 길면 잘라내기
    if len(description) > 160:
        description = description[:157] + '...'

    return description

def optimize_tags(tags, category_keywords):
    """태그 최적화"""
    if not tags:
        tags = []
    else:
        tags = [t.strip() for t in tags.split(',')]

    # 주요 키워드 추가
    for keyword in category_keywords[:10]:
        if keyword not in tags:
            tags.append(keyword)

    # 중복 제거 및 정렬
    tags = list(dict.fromkeys(tags))

    return tags[:15]  # 최대 15개

def update_front_matter(content, optimized_data):
    """Front Matter 업데이트"""
    front_matter, end_pos = extract_front_matter(content)
    if not front_matter:
        return content, False

    # 각 필드 업데이트
    new_front_matter = front_matter

    if 'title' in optimized_data:
        new_front_matter = re.sub(
            r'title:\s*"?([^"\n]+)"?',
            f'title: "{optimized_data["title"]}"',
            new_front_matter
        )

    if 'description' in optimized_data:
        new_front_matter = re.sub(
            r'description:\s*"?([^"\n]+)"?',
            f'description: "{optimized_data["description"]}"',
            new_front_matter
        )

    if 'tags' in optimized_data:
        tags_str = '", "'.join(optimized_data['tags'])
        new_front_matter = re.sub(
            r'tags:\s*\[.*?\]',
            f'tags: ["{tags_str}"]',
            new_front_matter
        )

    if 'keywords' in optimized_data:
        keywords_str = '", "'.join(optimized_data['keywords'])
        if 'keywords:' in new_front_matter:
            new_front_matter = re.sub(
                r'keywords:\s*\[.*?\]',
                f'keywords: ["{keywords_str}"]',
                new_front_matter
            )
        else:
            new_front_matter += f'\nkeywords: ["{keywords_str}"]'

    # 전체 콘텐츠 재구성
    new_content = f"---\n{new_front_matter}\n---\n" + content[end_pos:]
    return new_content, True

def process_markdown_file(file_path):
    """마크다운 파일 SEO 최적화"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Front Matter 추출
        front_matter, _ = extract_front_matter(content)
        if not front_matter:
            return False

        # Front Matter 파싱
        fm_data = parse_front_matter(front_matter)

        # 카테고리별 키워드
        category = get_category_from_path(file_path)
        category_keywords = get_seo_keywords(category)

        # 최적화 데이터 생성
        optimized_data = {}

        # 제목 최적화
        if 'title' in fm_data:
            optimized_data['title'] = optimize_title(fm_data['title'], category_keywords)

        # 설명 최적화
        if 'description' in fm_data:
            optimized_data['description'] = optimize_description(fm_data['description'], category_keywords)

        # 태그 최적화
        if 'tags' in fm_data:
            optimized_data['tags'] = optimize_tags(fm_data['tags'], category_keywords)

        # 키워드 최적화
        optimized_data['keywords'] = category_keywords[:10]

        # Front Matter 업데이트
        new_content, updated = update_front_matter(content, optimized_data)

        if updated:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)

            print(f"✅ {file_path.name}: SEO 최적화 완료")
            return True
        else:
            return False

    except Exception as e:
        print(f"❌ {file_path.name} 처리 중 오류: {e}")
        return False

def main():
    """메인 실행 함수"""
    content_dir = Path('content')

    if not content_dir.exists():
        print("❌ content 디렉토리를 찾을 수 없습니다.")
        return

    # 모든 마크다운 파일 찾기
    md_files = list(content_dir.rglob('*.md'))

    print(f"📁 총 {len(md_files)}개 파일 SEO 최적화 시작...\n")

    processed_files = 0

    for md_file in md_files:
        if process_markdown_file(md_file):
            processed_files += 1

    print(f"\n{'='*60}")
    print(f"✅ SEO 최적화 완료!")
    print(f"📊 최적화된 파일: {processed_files}개")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
