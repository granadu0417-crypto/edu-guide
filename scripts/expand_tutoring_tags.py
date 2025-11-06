#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tutoring 폴더 태그 8개 이상 확장
"""

from pathlib import Path
import re
from collections import Counter

# Tutoring 관련 태그 풀
TUTORING_TAG_POOLS = {
    'academy': [
        '학원', '학원찾기', '학원선택', '학원추천', '학원비교', '학원정보',
        '입시학원', '보습학원', '종합학원', '전문학원', '특목고학원', '강남학원',
        '수학학원', '영어학원', '과학학원', '대치동학원', '목동학원', '분당학원',
        '학원수업', '학원강사', '학원평가', '학원환경', '학원시스템', '학원관리',
        '자기주도학원', '관리형학원', '기숙학원', '온라인학원', '그룹학습', '소수정예'
    ],
    'private': [
        '과외', '1:1과외', '과외찾기', '과외선택', '과외추천', '개인과외',
        '수학과외', '영어과외', '과학과외', '국어과외', '과외선생님',
        '대학생과외', '의대생과외', '서울대과외', '연세대과외', '고려대과외',
        '전문과외', '재수과외', '검정고시과외', '영재과외', '특목고과외',
        '방문과외', '온라인과외', '화상과외', '그룹과외', '단기과외', '장기과외',
        '집중관리', '맞춤과외', '과외관리', '과외비용', '과외효과'
    ],
    'guide': [
        '선택가이드', '교육가이드', '학습가이드', '학부모가이드', '입시정보',
        '학원vs과외', '선택기준', '비교분석', '교육전략', '학습전략',
        '성적향상', '학습법', '공부법', '시험대비', '내신관리', '수능준비',
        '교육상담', '학습상담', '진로상담', '입시상담', '교육컨설팅',
        '학습플랜', '학습관리', '효율적학습', '자기주도학습', '학습동기'
    ]
}

# 학년별 태그
GRADE_TAGS = ['초등', '초등학생', '중등', '중학생', '고등', '고등학생', '재수생', '검정고시']

# 과목별 태그
SUBJECT_TAGS = ['수학', '영어', '국어', '과학', '사회', '역사', '한국사', '세계사', '물리', '화학', '생물', '지구과학']

# 지역별 태그
REGION_TAGS = ['강남', '서초', '송파', '강동', '대치동', '목동', '분당', '일산', '평촌', '중계동', '노원', '잠실']

# 공통 교육 태그
COMMON_TAGS = ['학습코칭', '교육정보', '입시전략', '맞춤학습', '검증된정보', '교육선택', '학습환경']

def extract_existing_tags(file_path):
    """기존 태그 추출"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        if not content.startswith('---'):
            return None

        parts = content.split('---', 2)
        if len(parts) < 3:
            return None

        front_matter = parts[1]
        body = parts[2]

        # Tags 추출
        tags_match = re.search(r'^tags:\s*\n((?:- .+\n)+)', front_matter, re.MULTILINE)
        if tags_match:
            tags_text = tags_match.group(1)
            existing_tags = [line.strip('- ').strip() for line in tags_text.split('\n') if line.strip()]
        else:
            tags_match = re.search(r'^tags:\s*\[(.+?)\]', front_matter, re.MULTILINE | re.DOTALL)
            if tags_match:
                tags_str = tags_match.group(1)
                existing_tags = []
                for tag in re.findall(r'["\']([^"\']+)["\']|([^,\[\]]+)', tags_str):
                    tag_value = tag[0] if tag[0] else tag[1]
                    tag_value = tag_value.strip()
                    if tag_value and tag_value not in existing_tags:
                        existing_tags.append(tag_value)
            else:
                existing_tags = []

        # Title 추출
        title_match = re.search(r'^title:\s*["\']?(.+?)["\']?$', front_matter, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else ""

        return {
            'tags': existing_tags,
            'title': title,
            'body': body,
            'content': content,
            'front_matter': front_matter
        }

    except Exception as e:
        return None

def generate_additional_tags(file_info, file_path, target_count=8):
    """추가 태그 생성"""
    existing_tags = file_info['tags']
    title = file_info['title']
    body = file_info['body'][:1000]

    if len(existing_tags) >= target_count:
        return []

    # 파일 경로에서 카테고리 추출
    rel_path = str(file_path.relative_to(Path('content/tutoring')))

    # 카테고리별 태그 풀 선택
    tag_pool = set()
    if 'academy' in rel_path:
        tag_pool.update(TUTORING_TAG_POOLS['academy'])
    elif 'private' in rel_path:
        tag_pool.update(TUTORING_TAG_POOLS['private'])
    elif 'guide' in rel_path:
        tag_pool.update(TUTORING_TAG_POOLS['guide'])
    else:
        # 일반 tutoring 파일
        tag_pool.update(TUTORING_TAG_POOLS['academy'])
        tag_pool.update(TUTORING_TAG_POOLS['private'])

    # 공통 태그 추가
    tag_pool.update(COMMON_TAGS)
    tag_pool.update(SUBJECT_TAGS)
    tag_pool.update(GRADE_TAGS)
    tag_pool.update(REGION_TAGS)

    # 제목/본문에서 키워드 매칭
    text = title + ' ' + body
    scored_tags = []

    for tag in tag_pool:
        # 기존 태그와 중복 체크
        if any(tag.lower() == existing.lower() for existing in existing_tags):
            continue

        score = 0
        if tag in title:
            score += 10
        if tag in body:
            score += 5

        scored_tags.append((tag, score))

    # 점수순 정렬
    scored_tags.sort(key=lambda x: x[1], reverse=True)

    # 필요한 수만큼 추가
    needed = target_count - len(existing_tags)
    additional_tags = [tag for tag, score in scored_tags[:needed] if score > 0]

    # 점수가 0인 경우도 일부 추가 (최소 8개 보장)
    if len(additional_tags) < needed:
        for tag, score in scored_tags[len(additional_tags):]:
            if len(additional_tags) >= needed:
                break
            if tag not in additional_tags:
                additional_tags.append(tag)

    return additional_tags[:needed]

def update_file_tags(file_path, additional_tags):
    """파일에 태그 추가"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        parts = content.split('---', 2)
        if len(parts) < 3:
            return False

        front_matter = parts[1]
        body = parts[2]

        # 기존 태그 섹션 찾기
        tags_match = re.search(r'^(tags:\s*\n(?:- .+\n)+)', front_matter, re.MULTILINE)

        if tags_match:
            old_tags = tags_match.group(1)
            new_tags_lines = old_tags.rstrip('\n')
            for tag in additional_tags:
                new_tags_lines += f"\n- {tag}"

            new_front_matter = front_matter.replace(old_tags, new_tags_lines + '\n')
        else:
            tags_match = re.search(r'^tags:\s*\[(.+?)\]', front_matter, re.MULTILINE | re.DOTALL)
            if tags_match:
                old_tags_section = tags_match.group(0)
                existing_tags = []
                for tag in re.findall(r'["\']([^"\']+)["\']|([^,\[\]]+)', tags_match.group(1)):
                    tag_value = tag[0] if tag[0] else tag[1]
                    tag_value = tag_value.strip()
                    if tag_value:
                        existing_tags.append(tag_value)

                new_tags_lines = "tags:\n"
                for tag in existing_tags + additional_tags:
                    new_tags_lines += f"- {tag}\n"

                new_front_matter = front_matter.replace(old_tags_section, new_tags_lines.rstrip('\n'))
            else:
                return False

        new_content = f"---{new_front_matter}---{body}"

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        return True

    except Exception as e:
        return False

def main():
    content_dir = Path('content/tutoring')

    print("🏷️  Tutoring 폴더 태그 확장 시작...\n")

    updated_count = 0
    skipped_count = 0
    error_count = 0
    category_stats = Counter()

    for md_file in sorted(content_dir.rglob('*.md')):
        file_info = extract_existing_tags(md_file)
        if not file_info:
            error_count += 1
            continue

        existing_count = len(file_info['tags'])

        if existing_count >= 8:
            skipped_count += 1
            continue

        additional_tags = generate_additional_tags(file_info, md_file)

        if not additional_tags:
            skipped_count += 1
            continue

        if update_file_tags(md_file, additional_tags):
            updated_count += 1
            rel_path = str(md_file.relative_to(content_dir))
            category = rel_path.split('/')[0] if '/' in rel_path else 'root'
            category_stats[category] += 1

            new_count = existing_count + len(additional_tags)
            print(f"✅ {rel_path}")
            print(f"   {existing_count}개 → {new_count}개 (추가: {', '.join(additional_tags[:3])}{'...' if len(additional_tags) > 3 else ''})")
        else:
            error_count += 1

    print("\n" + "=" * 80)
    print("📊 태그 확장 완료")
    print("=" * 80)
    print(f"확장 완료: {updated_count}개")
    print(f"스킵    : {skipped_count}개 (이미 8개 이상)")
    print(f"오류    : {error_count}개")

    if category_stats:
        print("\n📂 카테고리별 통계:")
        for category in sorted(category_stats.keys()):
            print(f"  {category:15s}: {category_stats[category]:3d}개 확장")

    print("=" * 80)

if __name__ == '__main__':
    main()
