#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
전체 사이트 종합 분석 스크립트
- SEO 전문가 관점
- 마케터 관점
- 프로그래머 관점
"""

import os
import re
from pathlib import Path
from collections import defaultdict, Counter
import json

def parse_front_matter(content):
    """Front matter 파싱"""
    if not content.startswith('---'):
        return None, content

    parts = content.split('---', 2)
    if len(parts) < 3:
        return None, content

    return parts[1].strip(), parts[2].strip()

def extract_field(front_matter, field_name):
    """Front matter에서 특정 필드 추출"""
    pattern = rf'{field_name}:\s*["\']?(.+?)["\']?\s*$'
    match = re.search(pattern, front_matter, re.MULTILINE)
    return match.group(1).strip('"\'') if match else None

def extract_tags(front_matter):
    """tags 배열 추출"""
    pattern = r'tags:\s*\[(.+?)\]'
    match = re.search(pattern, front_matter, re.DOTALL)
    if match:
        tags_str = match.group(1)
        tags = re.findall(r'"([^"]+)"', tags_str)
        return tags
    return []

def extract_categories(front_matter):
    """categories 배열 추출"""
    pattern = r'categories:\s*\[(.+?)\]'
    match = re.search(pattern, front_matter, re.DOTALL)
    if match:
        cats_str = match.group(1)
        cats = re.findall(r'"([^"]+)"', cats_str)
        return cats
    return []

def analyze_site():
    """전체 사이트 분석"""
    content_dir = Path('content')

    if not content_dir.exists():
        print("❌ content 디렉토리를 찾을 수 없습니다.")
        return

    # 데이터 수집 구조
    data = {
        'files': [],
        'images': defaultdict(list),  # image_url -> [file_paths]
        'titles': defaultdict(list),  # title -> [file_paths]
        'descriptions': defaultdict(list),  # description -> [file_paths]
        'tags': Counter(),
        'categories': Counter(),
        'issues': {
            'seo': [],
            'content': [],
            'technical': []
        },
        'stats': {
            'total_files': 0,
            'by_category': defaultdict(int),
            'avg_content_length': 0,
            'min_content_length': float('inf'),
            'max_content_length': 0,
            'files_without_images': [],
            'files_without_description': [],
            'files_without_tags': [],
            'empty_content': [],
            'short_content': [],  # < 500 words
            'duplicate_slugs': defaultdict(list)
        }
    }

    md_files = list(content_dir.rglob('*.md'))
    print(f"🔍 총 {len(md_files)}개 파일 분석 시작...\n")

    for md_file in md_files:
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()

            front_matter, body = parse_front_matter(content)

            if not front_matter:
                data['issues']['technical'].append({
                    'file': str(md_file),
                    'issue': 'No front matter found'
                })
                continue

            # 기본 정보 추출
            title = extract_field(front_matter, 'title')
            description = extract_field(front_matter, 'description')
            featured_image = extract_field(front_matter, 'featured_image')
            tags = extract_tags(front_matter)
            categories = extract_categories(front_matter)

            # 파일 정보 저장
            file_info = {
                'path': str(md_file.relative_to(content_dir)),
                'title': title,
                'description': description,
                'image': featured_image,
                'tags': tags,
                'categories': categories,
                'content_length': len(body.strip()),
                'word_count': len(body.split())
            }

            data['files'].append(file_info)
            data['stats']['total_files'] += 1

            # 중복 검사
            if featured_image:
                data['images'][featured_image].append(str(md_file.relative_to(content_dir)))
            else:
                data['stats']['files_without_images'].append(str(md_file.relative_to(content_dir)))

            if title:
                data['titles'][title].append(str(md_file.relative_to(content_dir)))

            if description:
                data['descriptions'][description].append(str(md_file.relative_to(content_dir)))
            else:
                data['stats']['files_without_description'].append(str(md_file.relative_to(content_dir)))

            if not tags:
                data['stats']['files_without_tags'].append(str(md_file.relative_to(content_dir)))

            # 태그/카테고리 통계
            for tag in tags:
                data['tags'][tag] += 1
            for cat in categories:
                data['categories'][cat] += 1
                data['stats']['by_category'][cat] += 1

            # 콘텐츠 길이 통계
            content_len = len(body.strip())
            data['stats']['min_content_length'] = min(data['stats']['min_content_length'], content_len)
            data['stats']['max_content_length'] = max(data['stats']['max_content_length'], content_len)

            if content_len == 0:
                data['stats']['empty_content'].append(str(md_file.relative_to(content_dir)))
            elif len(body.split()) < 200:  # 200 단어 미만
                data['stats']['short_content'].append(str(md_file.relative_to(content_dir)))

            # 슬러그 중복 검사 (같은 디렉토리 내)
            slug = md_file.stem
            parent = str(md_file.parent.relative_to(content_dir))
            data['stats']['duplicate_slugs'][f"{parent}/{slug}"].append(str(md_file.relative_to(content_dir)))

            # SEO 문제 검사
            if title and len(title) > 60:
                data['issues']['seo'].append({
                    'file': str(md_file.relative_to(content_dir)),
                    'issue': f'Title too long ({len(title)} chars): {title[:60]}...'
                })

            if description and len(description) > 160:
                data['issues']['seo'].append({
                    'file': str(md_file.relative_to(content_dir)),
                    'issue': f'Description too long ({len(description)} chars)'
                })

            if description and len(description) < 50:
                data['issues']['seo'].append({
                    'file': str(md_file.relative_to(content_dir)),
                    'issue': f'Description too short ({len(description)} chars)'
                })

            # 콘텐츠 품질 검사
            if 'Lorem ipsum' in body or 'TODO' in body or 'FIXME' in body:
                data['issues']['content'].append({
                    'file': str(md_file.relative_to(content_dir)),
                    'issue': 'Contains placeholder text (Lorem ipsum/TODO/FIXME)'
                })

            # 링크 검사
            broken_links = re.findall(r'\[([^\]]+)\]\(([^\)]+)\)', body)
            for link_text, link_url in broken_links:
                if link_url.startswith('/') and not link_url.startswith('http'):
                    # 내부 링크 - 나중에 검증 가능
                    pass

        except Exception as e:
            data['issues']['technical'].append({
                'file': str(md_file.relative_to(content_dir)),
                'issue': f'Error parsing file: {str(e)}'
            })

    # 평균 콘텐츠 길이 계산
    if data['stats']['total_files'] > 0:
        total_length = sum(f['content_length'] for f in data['files'])
        data['stats']['avg_content_length'] = total_length // data['stats']['total_files']

    return data

def print_report(data):
    """분석 결과 리포트 출력"""
    print("\n" + "="*80)
    print("📊 전체 사이트 종합 분석 리포트")
    print("="*80)

    # 1. 기본 통계
    print("\n【1. 기본 통계】")
    print(f"총 파일 수: {data['stats']['total_files']}개")
    print(f"\n카테고리별 파일 수:")
    for cat, count in sorted(data['stats']['by_category'].items(), key=lambda x: x[1], reverse=True):
        print(f"  - {cat}: {count}개")

    print(f"\n콘텐츠 길이:")
    print(f"  - 평균: {data['stats']['avg_content_length']:,} bytes")
    print(f"  - 최소: {data['stats']['min_content_length']:,} bytes")
    print(f"  - 최대: {data['stats']['max_content_length']:,} bytes")

    # 2. 중복 검사
    print("\n" + "="*80)
    print("【2. 중복 검사】")

    # 중복 이미지
    duplicate_images = {img: files for img, files in data['images'].items() if len(files) > 1}
    print(f"\n🖼️  중복 이미지: {len(duplicate_images)}개")
    if duplicate_images:
        for img, files in sorted(duplicate_images.items(), key=lambda x: len(x[1]), reverse=True)[:10]:
            print(f"\n  📌 {img}")
            print(f"  사용된 파일 ({len(files)}개):")
            for f in files[:5]:
                print(f"    - {f}")
            if len(files) > 5:
                print(f"    ... 외 {len(files)-5}개")

    # 중복 제목
    duplicate_titles = {title: files for title, files in data['titles'].items() if len(files) > 1}
    print(f"\n📝 중복 제목: {len(duplicate_titles)}개")
    if duplicate_titles:
        for title, files in sorted(duplicate_titles.items(), key=lambda x: len(x[1]), reverse=True)[:10]:
            print(f"\n  📌 \"{title}\"")
            print(f"  사용된 파일 ({len(files)}개):")
            for f in files:
                print(f"    - {f}")

    # 중복 description
    duplicate_descriptions = {desc: files for desc, files in data['descriptions'].items() if len(files) > 1}
    print(f"\n📄 중복 Description: {len(duplicate_descriptions)}개")
    if duplicate_descriptions:
        for desc, files in sorted(duplicate_descriptions.items(), key=lambda x: len(x[1]), reverse=True)[:10]:
            print(f"\n  📌 \"{desc[:80]}...\"")
            print(f"  사용된 파일 ({len(files)}개):")
            for f in files[:5]:
                print(f"    - {f}")
            if len(files) > 5:
                print(f"    ... 외 {len(files)-5}개")

    # 3. SEO 문제점
    print("\n" + "="*80)
    print("【3. SEO 문제점】")

    print(f"\n🔍 이미지 없는 파일: {len(data['stats']['files_without_images'])}개")
    if data['stats']['files_without_images']:
        for f in data['stats']['files_without_images'][:10]:
            print(f"  - {f}")
        if len(data['stats']['files_without_images']) > 10:
            print(f"  ... 외 {len(data['stats']['files_without_images'])-10}개")

    print(f"\n📋 Description 없는 파일: {len(data['stats']['files_without_description'])}개")
    if data['stats']['files_without_description']:
        for f in data['stats']['files_without_description'][:10]:
            print(f"  - {f}")
        if len(data['stats']['files_without_description']) > 10:
            print(f"  ... 외 {len(data['stats']['files_without_description'])-10}개")

    print(f"\n🏷️  Tags 없는 파일: {len(data['stats']['files_without_tags'])}개")
    if data['stats']['files_without_tags']:
        for f in data['stats']['files_without_tags'][:10]:
            print(f"  - {f}")
        if len(data['stats']['files_without_tags']) > 10:
            print(f"  ... 외 {len(data['stats']['files_without_tags'])-10}개")

    print(f"\n⚠️  SEO 이슈: {len(data['issues']['seo'])}개")
    if data['issues']['seo']:
        for issue in data['issues']['seo'][:20]:
            print(f"  - {issue['file']}: {issue['issue']}")
        if len(data['issues']['seo']) > 20:
            print(f"  ... 외 {len(data['issues']['seo'])-20}개")

    # 4. 콘텐츠 품질
    print("\n" + "="*80)
    print("【4. 콘텐츠 품질】")

    print(f"\n📭 빈 콘텐츠: {len(data['stats']['empty_content'])}개")
    if data['stats']['empty_content']:
        for f in data['stats']['empty_content']:
            print(f"  - {f}")

    print(f"\n📏 짧은 콘텐츠 (< 200 단어): {len(data['stats']['short_content'])}개")
    if data['stats']['short_content']:
        for f in data['stats']['short_content'][:10]:
            print(f"  - {f}")
        if len(data['stats']['short_content']) > 10:
            print(f"  ... 외 {len(data['stats']['short_content'])-10}개")

    print(f"\n⚠️  콘텐츠 이슈: {len(data['issues']['content'])}개")
    if data['issues']['content']:
        for issue in data['issues']['content'][:10]:
            print(f"  - {issue['file']}: {issue['issue']}")
        if len(data['issues']['content']) > 10:
            print(f"  ... 외 {len(data['issues']['content'])-10}개")

    # 5. 기술적 문제
    print("\n" + "="*80)
    print("【5. 기술적 문제】")

    print(f"\n🔧 기술 이슈: {len(data['issues']['technical'])}개")
    if data['issues']['technical']:
        for issue in data['issues']['technical']:
            print(f"  - {issue['file']}: {issue['issue']}")

    # 6. 태그 통계
    print("\n" + "="*80)
    print("【6. 태그 통계 (상위 20개)】")
    for tag, count in data['tags'].most_common(20):
        print(f"  - {tag}: {count}회")

    # 7. 종합 점수
    print("\n" + "="*80)
    print("【7. 종합 평가】")

    total_issues = (
        len(duplicate_images) * 2 +
        len(duplicate_titles) * 3 +
        len(duplicate_descriptions) * 2 +
        len(data['stats']['files_without_images']) * 1 +
        len(data['stats']['files_without_description']) * 2 +
        len(data['stats']['files_without_tags']) * 1 +
        len(data['stats']['empty_content']) * 5 +
        len(data['stats']['short_content']) * 1 +
        len(data['issues']['seo']) * 2 +
        len(data['issues']['content']) * 3 +
        len(data['issues']['technical']) * 4
    )

    max_score = 100
    penalty = min(total_issues, max_score)
    score = max(0, max_score - penalty)

    print(f"\n📊 종합 점수: {score}/100")
    print(f"총 문제점: {total_issues}개")

    if score >= 90:
        grade = "🌟 우수"
    elif score >= 80:
        grade = "✅ 양호"
    elif score >= 70:
        grade = "⚠️  보통"
    elif score >= 60:
        grade = "🔧 개선 필요"
    else:
        grade = "❌ 심각한 문제"

    print(f"등급: {grade}")

    # 우선순위 개선사항
    print("\n" + "="*80)
    print("【8. 우선순위 개선사항】")

    priority_fixes = []

    if data['stats']['empty_content']:
        priority_fixes.append(f"🔴 긴급: {len(data['stats']['empty_content'])}개 빈 콘텐츠 파일")

    if len(duplicate_titles) > 10:
        priority_fixes.append(f"🟠 높음: {len(duplicate_titles)}개 중복 제목 수정")

    if len(data['stats']['files_without_description']) > 20:
        priority_fixes.append(f"🟡 중간: {len(data['stats']['files_without_description'])}개 파일에 Description 추가")

    if len(duplicate_images) > 20:
        priority_fixes.append(f"🟢 낮음: {len(duplicate_images)}개 중복 이미지 다양화")

    if len(data['stats']['short_content']) > 50:
        priority_fixes.append(f"🟡 중간: {len(data['stats']['short_content'])}개 짧은 콘텐츠 보강")

    for i, fix in enumerate(priority_fixes, 1):
        print(f"{i}. {fix}")

    print("\n" + "="*80)

def save_detailed_report(data):
    """상세 리포트 JSON 저장"""
    output_file = 'site_audit_report.json'

    # JSON 직렬화를 위해 데이터 변환
    report = {
        'total_files': data['stats']['total_files'],
        'duplicate_images': {img: files for img, files in data['images'].items() if len(files) > 1},
        'duplicate_titles': {title: files for title, files in data['titles'].items() if len(files) > 1},
        'duplicate_descriptions': {desc: files for desc, files in data['descriptions'].items() if len(files) > 1},
        'files_without_images': data['stats']['files_without_images'],
        'files_without_description': data['stats']['files_without_description'],
        'files_without_tags': data['stats']['files_without_tags'],
        'empty_content': data['stats']['empty_content'],
        'short_content': data['stats']['short_content'],
        'seo_issues': data['issues']['seo'],
        'content_issues': data['issues']['content'],
        'technical_issues': data['issues']['technical'],
        'top_tags': dict(data['tags'].most_common(50)),
        'category_stats': dict(data['stats']['by_category'])
    }

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"\n💾 상세 리포트 저장: {output_file}")

def main():
    """메인 실행"""
    data = analyze_site()
    if data:
        print_report(data)
        save_detailed_report(data)

if __name__ == '__main__':
    main()
