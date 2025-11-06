#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
파일에 적절한 태그 자동 추가
"""

from pathlib import Path
import re
import yaml

# 카테고리별 기본 태그
CATEGORY_TAGS = {
    'elementary': ['초등교육', '초등학습'],
    'middle': ['중등교육', '중학교'],
    'high': ['고등교육', '고등학교', '대입'],
    'subjects': ['과목별학습'],
    'exam': ['시험대비', '시험전략'],
    'tutoring': ['과외', '학습코칭'],
    'consultation': ['교육상담', '학습전략'],
    'local': ['지역정보', '교육정보']
}

# 학년 태그 매핑
GRADE_TAGS = {
    'b9': '1학년', 'b10': '2학년', 'b11': '3학년',
    'b12': '4학년', 'b13': '5학년', 'b14': '6학년', 'b15': '전학년'
}

# 과목 태그
SUBJECT_TAGS = {
    'korean': '국어', 'english': '영어', 'math': '수학',
    'science': '과학', 'social': '사회', 'history': '역사'
}

# 키워드 기반 태그
KEYWORD_TAGS = {
    # 학습 방법
    '습관': '학습습관', '자기주도': '자기주도학습', '공부법': '학습방법',
    '시간관리': '시간관리', '집중력': '집중력',

    # 과목별
    '받아쓰기': '받아쓰기', '독해': '독해력', '어휘': '어휘력',
    '연산': '연산', '문장제': '문장제', '도형': '도형',
    '문법': '문법', '회화': '회화', '듣기': '듣기',

    # 시험
    '내신': '내신', '수능': '수능', '모의고사': '모의고사',
    '중간고사': '중간고사', '기말고사': '기말고사',

    # 입시
    '입시': '입시전략', '진로': '진로탐색', '진학': '진학정보',
    '학생부': '학생부', '수시': '수시', '정시': '정시',

    # 과외
    '과외': '1:1과외', '학원': '학원', '온라인': '온라인학습',
    '선생님': '교사선택', '그룹': '그룹과외',

    # 상담
    '상담': '학습상담', '컨설팅': '교육컨설팅', '전략': '학습전략',

    # 학습 영역
    '읽기': '읽기', '쓰기': '쓰기', '말하기': '말하기',
    '계산': '계산', '사고력': '사고력', '창의': '창의력',

    # 기타
    '학부모': '학부모가이드', '교재': '교재선택', '복습': '복습전략'
}

def extract_front_matter(content):
    """YAML front matter 추출"""
    if not content.startswith('---'):
        return None, content

    parts = content.split('---', 2)
    if len(parts) < 3:
        return None, content

    try:
        front_matter = yaml.safe_load(parts[1])
        body = parts[2]
        return front_matter, body
    except:
        return None, content

def generate_tags(file_path, front_matter, body):
    """파일에 적합한 태그 생성"""
    tags = set()

    rel_path = str(file_path.relative_to(Path('content')))
    category = rel_path.split('/')[0]
    filename = file_path.stem

    # 1. 카테고리 기본 태그
    if category in CATEGORY_TAGS:
        tags.update(CATEGORY_TAGS[category])

    # 2. 학년 태그 (파일명에서 추출)
    for code, grade in GRADE_TAGS.items():
        if code in filename:
            if category == 'elementary':
                tags.add(f'초등{grade}')
            elif category == 'middle':
                tags.add(f'중{grade}')
            elif category == 'high':
                tags.add(f'고{grade}')
            break

    # 3. 서브 카테고리 태그
    parts = rel_path.split('/')
    if len(parts) > 1:
        subcategory = parts[1].replace('_index.md', '').replace('.md', '')

        # 과목 태그
        if subcategory in SUBJECT_TAGS:
            tags.add(SUBJECT_TAGS[subcategory])

        # 과외 유형
        if category == 'tutoring':
            if 'academy' in subcategory:
                tags.add('학원')
            elif 'private' in subcategory or 'guide' in subcategory:
                tags.add('1:1과외')

        # 상담 유형
        if category == 'consultation':
            tags.add('교육컨설팅')

    # 4. 제목에서 키워드 추출
    title = front_matter.get('title', '')
    for keyword, tag in KEYWORD_TAGS.items():
        if keyword in title or keyword in body[:500]:
            tags.add(tag)

    # 5. 파일명 기반 특별 태그
    if 'batch' in filename:
        tags.add('학습가이드')
    if '_index' in filename:
        tags.add('가이드')
    if 'strategy' in filename or '전략' in title:
        tags.add('학습전략')
    if 'guide' in filename or '가이드' in title:
        tags.add('학습가이드')
    if 'preparation' in filename or '준비' in title:
        tags.add('시험준비')

    # 6. 중등/고등 특별 태그
    if category == 'middle':
        tags.add('내신관리')
    elif category == 'high':
        tags.add('대학입시')
        if '수능' in title or '수능' in body[:500]:
            tags.add('수능')

    # 7. 최소 태그 수 보장 (4-8개)
    if len(tags) < 4:
        # 기본 보충 태그
        if category in ['elementary', 'middle', 'high']:
            tags.add('학습방법')
            tags.add('성적향상')
        if category in ['exam']:
            tags.add('시험공부')
            tags.add('성적관리')
        if category in ['tutoring']:
            tags.add('과외선택')
            tags.add('학습코칭')

    # 태그 목록 정리 (최대 8개)
    return sorted(list(tags))[:8]

def add_tags_to_file(file_path):
    """파일에 태그 추가"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        front_matter, body = extract_front_matter(content)
        if not front_matter:
            return False, "front matter 없음"

        # 이미 태그가 있는 경우 스킵
        existing_tags = front_matter.get('tags', [])
        if existing_tags and len(existing_tags) > 0:
            return False, "이미 태그 있음"

        # 태그 생성
        tags = generate_tags(file_path, front_matter, body)

        # front matter에 태그 추가
        front_matter['tags'] = tags

        # YAML 직렬화
        yaml_str = yaml.dump(front_matter, allow_unicode=True, sort_keys=False, default_flow_style=False)

        # 새 콘텐츠 작성
        new_content = f"---\n{yaml_str}---{body}"

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        rel_path = str(file_path.relative_to(Path('content')))
        return True, f"{rel_path} ({len(tags)}개 태그)"

    except Exception as e:
        return False, f"오류: {e}"

def main():
    content_dir = Path('content')
    success_count = 0
    skip_count = 0
    error_count = 0

    category_stats = {}

    print("🏷️  태그 추가 시작...\n")

    for md_file in content_dir.rglob('*.md'):
        success, message = add_tags_to_file(md_file)

        if success:
            success_count += 1
            category = str(md_file.relative_to(content_dir)).split('/')[0]
            category_stats[category] = category_stats.get(category, 0) + 1
            print(f"✅ {message}")
        elif "이미 태그" in message:
            skip_count += 1
        else:
            error_count += 1
            print(f"❌ {md_file}: {message}")

    print("\n" + "=" * 80)
    print("📊 태그 추가 완료 통계")
    print("=" * 80)
    print(f"추가 완료: {success_count}")
    print(f"스킵    : {skip_count}")
    print(f"오류    : {error_count}")

    if category_stats:
        print("\n📂 카테고리별 통계:")
        for category in sorted(category_stats.keys()):
            print(f"  {category:15s}: {category_stats[category]:3d}개 추가")

    print("=" * 80)

if __name__ == '__main__':
    main()
