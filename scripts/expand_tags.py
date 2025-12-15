#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
과목별 파일 태그 8개 이상 확장
"""

from pathlib import Path
import re
from collections import Counter

# 과목별 관련 태그 풀
SUBJECT_TAG_POOLS = {
    'korean': [
        '국어', '독해', '문학', '비문학', '문법', '어휘', '작문', '화법',
        '고전문학', '현대문학', '시', '소설', '수필', '희곡', '시나리오',
        '국어교육', '언어능력', '읽기', '쓰기', '말하기', '듣기',
        '문장구조', '품사', '맞춤법', '표현', '이해력', '분석력'
    ],
    'english': [
        '영어', '영어회화', '영문법', '영어듣기', '영어독해', '영어작문',
        '어휘', '단어', 'vocabulary', 'grammar', 'listening', 'reading', 'writing', 'speaking',
        '영어교육', '영어학습', '영어시험', '영어능력', '영어실력',
        '문법', '회화', '듣기', '독해', '작문', '발음', '억양'
    ],
    'math': [
        '수학', '산수', '연산', '계산', '수식', '공식', '문제풀이',
        '대수', '기하', '함수', '방정식', '부등식', '통계', '확률',
        '도형', '그래프', '좌표', '벡터', '행렬', '미적분', '삼각함수',
        '수학교육', '수학학습', '수학사고력', '논리', '추론', '증명'
    ],
    'science': [
        '과학', '물리', '화학', '생물', '지구과학', '실험', '관찰',
        '과학교육', '과학학습', '탐구', '과학적사고', '과학원리',
        '자연현상', '과학지식', '과학이론', '과학실습', '과학탐구',
        '에너지', '물질', '생명', '지구', '우주', '환경'
    ],
    'social': [
        '사회', '역사', '지리', '일반사회', '윤리', '정치', '경제',
        '사회교육', '사회학습', '역사이해', '지리탐구', '사회현상',
        '문화', '사회구조', '사회문제', '시사', '세계사', '한국사',
        '인문', '사회과학', '공동체', '시민', '민주주의', '인권'
    ]
}

# 공통 교육 태그 풀
COMMON_TAGS = [
    '학습방법', '학습전략', '학습가이드', '1:1과외', '과외', '교육',
    '시험대비', '내신', '수능', '성적향상', '학습코칭', '맞춤학습',
    '기초', '심화', '실력향상', '학습능력', '학습효과', '학습관리',
    '학습습관', '자기주도학습', '효율적학습', '학습계획', '학습목표',
    '초등교육', '중등교육', '고등교육', '교과학습', '과목학습'
]

# 레벨 태그
LEVEL_TAGS = {
    'basic': ['기초', '입문', '초급'],
    'intermediate': ['중급', '표준'],
    'advanced': ['심화', '고급', '상급']
}

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
            # 리스트 형식이 아닌 경우
            tags_match = re.search(r'^tags:\s*\[(.+?)\]', front_matter, re.MULTILINE | re.DOTALL)
            if tags_match:
                tags_str = tags_match.group(1)
                # 쉼표로 구분된 태그 파싱
                existing_tags = []
                for tag in re.findall(r'["\']([^"\']+)["\']|([^,\[\]]+)', tags_str):
                    tag_value = tag[0] if tag[0] else tag[1]
                    tag_value = tag_value.strip()
                    if tag_value and tag_value not in existing_tags:
                        existing_tags.append(tag_value)
            else:
                existing_tags = []

        # Title 추출
        title_match = re.search(r'^title:\s*(.+)', front_matter, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else ""

        return {
            'tags': existing_tags,
            'title': title,
            'body': body,
            'content': content,
            'front_matter': front_matter
        }

    except Exception as e:
        print(f"❌ 오류 ({file_path.name}): {e}")
        return None

def generate_additional_tags(file_info, file_path, target_count=8):
    """추가 태그 생성"""
    existing_tags = file_info['tags']
    title = file_info['title']
    body = file_info['body'][:1000]  # 앞부분 1000자만 분석

    # 이미 충분한 태그가 있으면 스킵
    if len(existing_tags) >= target_count:
        return []

    # 파일 경로에서 과목 추출
    rel_path = str(file_path.relative_to(Path('content')))
    parts = rel_path.split('/')

    subject = None
    if len(parts) >= 2:
        subject = parts[1]  # subjects/korean → korean

    # 후보 태그 풀 생성
    candidate_tags = set()

    # 1. 과목 특화 태그
    if subject and subject in SUBJECT_TAG_POOLS:
        candidate_tags.update(SUBJECT_TAG_POOLS[subject])

    # 2. 공통 교육 태그
    candidate_tags.update(COMMON_TAGS)

    # 3. 레벨 태그 (제목/본문에 키워드가 있는 경우)
    for level, tags in LEVEL_TAGS.items():
        if any(keyword in title.lower() or keyword in body.lower()
               for keyword in ['기초', '입문', '초급', '중급', '심화', '고급']):
            candidate_tags.update(tags)

    # 4. 제목/본문에서 키워드 기반 필터링
    text = title + ' ' + body

    # 키워드가 포함된 태그 우선순위 부여
    scored_tags = []
    for tag in candidate_tags:
        # 기존 태그와 중복 체크 (대소문자 구분 없이)
        if any(tag.lower() == existing.lower() for existing in existing_tags):
            continue

        score = 0
        # 제목에 포함되면 높은 점수
        if tag in title:
            score += 10
        # 본문에 포함되면 중간 점수
        if tag in body:
            score += 5
        # 과목 특화 태그에 보너스
        if subject and subject in SUBJECT_TAG_POOLS and tag in SUBJECT_TAG_POOLS[subject]:
            score += 3
        # 너무 짧은 태그는 감점 (오탐 방지)
        if len(tag) < 2:
            score -= 5

        scored_tags.append((tag, score))

    # 점수순 정렬 후 상위 태그 선택
    scored_tags.sort(key=lambda x: x[1], reverse=True)

    # 필요한 수만큼 추가 (target_count - 기존 태그 수)
    needed = target_count - len(existing_tags)
    additional_tags = [tag for tag, score in scored_tags[:needed] if score > 0]

    # 점수가 0 이하인 경우 일반 추천 태그 사용
    if len(additional_tags) < needed:
        # 과목별 기본 태그 추가
        if subject and subject in SUBJECT_TAG_POOLS:
            for tag in SUBJECT_TAG_POOLS[subject][:needed - len(additional_tags)]:
                if not any(tag.lower() == t.lower() for t in existing_tags + additional_tags):
                    additional_tags.append(tag)

    return additional_tags

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
            # 리스트 형식
            old_tags = tags_match.group(1)
            new_tags_lines = old_tags.rstrip('\n')
            for tag in additional_tags:
                new_tags_lines += f"\n- {tag}"

            new_front_matter = front_matter.replace(old_tags, new_tags_lines + '\n')
        else:
            # 다른 형식 (배열 등) - 단순히 끝에 추가
            tags_match = re.search(r'^tags:\s*\[(.+?)\]', front_matter, re.MULTILINE | re.DOTALL)
            if tags_match:
                old_tags_section = tags_match.group(0)
                # 배열 형식을 리스트 형식으로 변환
                existing_tags = []
                for tag in re.findall(r'["\']([^"\']+)["\']|([^,\[\]]+)', tags_match.group(1)):
                    tag_value = tag[0] if tag[0] else tag[1]
                    tag_value = tag_value.strip()
                    if tag_value:
                        existing_tags.append(tag_value)

                # 새로운 리스트 형식 생성
                new_tags_lines = "tags:\n"
                for tag in existing_tags + additional_tags:
                    new_tags_lines += f"- {tag}\n"

                new_front_matter = front_matter.replace(old_tags_section, new_tags_lines.rstrip('\n'))
            else:
                return False

        # 파일 저장
        new_content = f"---{new_front_matter}---{body}"

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        return True

    except Exception as e:
        print(f"❌ 저장 오류 ({file_path.name}): {e}")
        return False

def main():
    content_dir = Path('content/subjects')

    print("🏷️  과목별 파일 태그 확장 시작...\n")

    updated_count = 0
    skipped_count = 0
    error_count = 0

    subject_stats = Counter()

    for md_file in sorted(content_dir.glob('**/*.md')):
        if md_file.name.startswith('_'):
            continue

        file_info = extract_existing_tags(md_file)
        if not file_info:
            error_count += 1
            continue

        existing_count = len(file_info['tags'])

        # 8개 미만인 경우만 처리
        if existing_count >= 8:
            skipped_count += 1
            continue

        # 추가 태그 생성
        additional_tags = generate_additional_tags(file_info, md_file)

        if not additional_tags:
            skipped_count += 1
            continue

        # 파일 업데이트
        if update_file_tags(md_file, additional_tags):
            updated_count += 1
            rel_path = str(md_file.relative_to(content_dir))
            subject = rel_path.split('/')[0]
            subject_stats[subject] += 1

            new_count = existing_count + len(additional_tags)
            print(f"✅ {rel_path}")
            print(f"   {existing_count}개 → {new_count}개 (추가: {', '.join(additional_tags)})")
        else:
            error_count += 1

    print("\n" + "=" * 80)
    print("📊 태그 확장 완료")
    print("=" * 80)
    print(f"확장 완료: {updated_count}개")
    print(f"스킵    : {skipped_count}개 (이미 8개 이상)")
    print(f"오류    : {error_count}개")

    if subject_stats:
        print("\n📂 과목별 통계:")
        for subject in sorted(subject_stats.keys()):
            print(f"  {subject:15s}: {subject_stats[subject]:3d}개 확장")

    print("=" * 80)

if __name__ == '__main__':
    main()
