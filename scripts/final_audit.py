#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
최종 사이트 감사 - 모든 이슈 종합 점검
"""

from pathlib import Path
import re
import yaml
from collections import Counter

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

def count_words(content):
    """단어 수 계산"""
    # Front matter 제거
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            content = parts[2]

    # 마크다운 문법 제거
    content = re.sub(r'#+ ', '', content)
    content = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', content)
    content = re.sub(r'[*_`]', '', content)
    content = re.sub(r'{{<.*?>}}', '', content)

    # 단어 수 계산
    korean_chars = len(re.findall(r'[가-힣]', content))
    english_words = len(re.findall(r'\b[a-zA-Z]+\b', content))

    return (korean_chars // 2) + english_words

def main():
    content_dir = Path('content')

    # 통계 변수
    total_files = 0
    issues = {
        'duplicate_titles': [],
        'duplicate_descriptions': [],
        'short_descriptions': [],
        'missing_tags': [],
        'short_content': [],
        'missing_featured_image': [],
        'duplicate_images': []
    }

    # 중복 검사용
    titles = Counter()
    descriptions = Counter()
    images = Counter()

    # 모든 파일 검사
    for md_file in content_dir.rglob('*.md'):
        total_files += 1

        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()

            front_matter, body = extract_front_matter(content)
            if not front_matter:
                continue

            rel_path = str(md_file.relative_to(content_dir))

            # 1. 제목 중복 검사
            title = front_matter.get('title', '')
            if title:
                titles[title] += 1

            # 2. Description 중복 검사
            description = front_matter.get('description', '')
            if description:
                descriptions[description] += 1

                # 짧은 description 검사 (150자 미만)
                if len(description) < 150:
                    issues['short_descriptions'].append((rel_path, len(description)))

            # 3. Tags 검사
            tags = front_matter.get('tags', [])
            if not tags or len(tags) == 0:
                issues['missing_tags'].append(rel_path)

            # 4. 이미지 중복 검사
            featured_image = front_matter.get('featured_image', '')
            if featured_image:
                images[featured_image] += 1
            else:
                issues['missing_featured_image'].append(rel_path)

            # 5. 콘텐츠 길이 검사
            word_count = count_words(content)
            if word_count < 200:
                issues['short_content'].append((rel_path, word_count))

        except Exception as e:
            print(f"❌ 오류: {md_file} - {e}")

    # 중복 항목 식별
    for title, count in titles.items():
        if count > 1:
            issues['duplicate_titles'].append((title, count))

    for desc, count in descriptions.items():
        if count > 1:
            issues['duplicate_descriptions'].append((desc[:50] + '...', count))

    for img, count in images.items():
        if count > 1:
            issues['duplicate_images'].append((img, count))

    # 결과 출력
    print("=" * 80)
    print("📋 최종 사이트 감사 보고서")
    print("=" * 80)
    print(f"총 파일 수: {total_files}개\n")

    # 이슈 요약
    total_issues = sum(len(v) for v in issues.values())

    if total_issues == 0:
        print("✅ 모든 검사 항목 통과! 이슈 없음\n")
    else:
        print(f"⚠️  발견된 이슈: {total_issues}개\n")

    # 상세 이슈 보고
    print("=" * 80)
    print("🔍 상세 검사 결과")
    print("=" * 80)

    print(f"\n1. 중복 제목: {len(issues['duplicate_titles'])}개")
    if issues['duplicate_titles']:
        for title, count in issues['duplicate_titles'][:5]:
            print(f"   - '{title}' ({count}회)")
        if len(issues['duplicate_titles']) > 5:
            print(f"   ... 외 {len(issues['duplicate_titles']) - 5}개")

    print(f"\n2. 중복 Description: {len(issues['duplicate_descriptions'])}개")
    if issues['duplicate_descriptions']:
        for desc, count in issues['duplicate_descriptions'][:5]:
            print(f"   - '{desc}' ({count}회)")
        if len(issues['duplicate_descriptions']) > 5:
            print(f"   ... 외 {len(issues['duplicate_descriptions']) - 5}개")

    print(f"\n3. 짧은 Description (<150자): {len(issues['short_descriptions'])}개")
    if issues['short_descriptions']:
        for path, length in issues['short_descriptions'][:5]:
            print(f"   - {path} ({length}자)")
        if len(issues['short_descriptions']) > 5:
            print(f"   ... 외 {len(issues['short_descriptions']) - 5}개")

    print(f"\n4. 태그 없음: {len(issues['missing_tags'])}개")
    if issues['missing_tags']:
        for path in issues['missing_tags'][:5]:
            print(f"   - {path}")
        if len(issues['missing_tags']) > 5:
            print(f"   ... 외 {len(issues['missing_tags']) - 5}개")

    print(f"\n5. 짧은 콘텐츠 (<200단어): {len(issues['short_content'])}개")
    if issues['short_content']:
        for path, words in issues['short_content'][:5]:
            print(f"   - {path} ({words}단어)")
        if len(issues['short_content']) > 5:
            print(f"   ... 외 {len(issues['short_content']) - 5}개")

    print(f"\n6. 이미지 없음: {len(issues['missing_featured_image'])}개")
    if issues['missing_featured_image']:
        for path in issues['missing_featured_image'][:5]:
            print(f"   - {path}")
        if len(issues['missing_featured_image']) > 5:
            print(f"   ... 외 {len(issues['missing_featured_image']) - 5}개")

    print(f"\n7. 중복 이미지: {len(issues['duplicate_images'])}개")
    if issues['duplicate_images']:
        for img, count in issues['duplicate_images'][:5]:
            print(f"   - {img} ({count}회)")
        if len(issues['duplicate_images']) > 5:
            print(f"   ... 외 {len(issues['duplicate_images']) - 5}개")

    print("\n" + "=" * 80)

    # 품질 점수 계산
    max_score = 100
    deductions = {
        'duplicate_titles': len(issues['duplicate_titles']) * 5,
        'duplicate_descriptions': len(issues['duplicate_descriptions']) * 3,
        'short_descriptions': len(issues['short_descriptions']) * 2,
        'missing_tags': len(issues['missing_tags']) * 3,
        'short_content': len(issues['short_content']) * 4,
        'missing_featured_image': len(issues['missing_featured_image']) * 2,
        'duplicate_images': len(issues['duplicate_images']) * 1
    }

    total_deduction = sum(deductions.values())
    quality_score = max(0, max_score - total_deduction)

    print(f"📊 사이트 품질 점수: {quality_score}/100")
    if quality_score >= 95:
        print("✅ 우수 - 배포 준비 완료")
    elif quality_score >= 80:
        print("⚠️  양호 - 일부 개선 권장")
    else:
        print("❌ 불량 - 개선 필요")

    print("=" * 80)

if __name__ == '__main__':
    main()
