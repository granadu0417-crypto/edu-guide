#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SEO 및 개발 품질 종합 검사
"""

from pathlib import Path
import re
import yaml

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

def check_file(file_path):
    """파일별 SEO 이슈 체크"""
    issues = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        front_matter, body = extract_front_matter(content)
        if not front_matter:
            return issues

        rel_path = str(file_path.relative_to(Path('content')))

        # 1. Description 중복 텍스트 체크
        description = front_matter.get('description', '')
        if description:
            # 같은 문장이 반복되는지 체크
            sentences = description.split('.')
            seen = set()
            for sentence in sentences:
                cleaned = sentence.strip()
                if cleaned and cleaned in seen:
                    issues.append({
                        'file': rel_path,
                        'type': 'description_duplicate',
                        'severity': 'high',
                        'message': f'Description에 중복 문장: "{cleaned}"'
                    })
                seen.add(cleaned)

        # 2. 제목과 콘텐츠 일치성 체크
        title = front_matter.get('title', '')
        first_heading = re.search(r'^#\s+(.+)$', body, re.MULTILINE)
        if first_heading and title:
            title_clean = title.split('|')[0].strip()
            heading_clean = first_heading.group(1).strip()
            if title_clean != heading_clean:
                issues.append({
                    'file': rel_path,
                    'type': 'title_mismatch',
                    'severity': 'medium',
                    'message': f'제목 불일치: title="{title_clean}" vs h1="{heading_clean}"'
                })

        # 3. Shortcode 문법 오류
        # 단일 괄호 패턴 체크: {< >} ({{<는 제외)
        single_brace = re.findall(r'(?<!\{)\{<\s*([^>]+?)\s*>\}(?!\})', body)
        # 삼중 이상 괄호 패턴 체크: {{{< >}}} 이상
        multi_brace = re.findall(r'\{{3,}<\s*([^>]+?)\s*>\}{3,}', body)

        wrong_shortcodes = single_brace + multi_brace
        if wrong_shortcodes:
            issues.append({
                'file': rel_path,
                'type': 'shortcode_syntax',
                'severity': 'critical',
                'message': f'잘못된 shortcode 문법: {wrong_shortcodes} ({{{{< >}}}}로 수정 필요)'
            })

        # 4. 깨진 내부 링크 체크
        internal_links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', body)
        for link_text, link_url in internal_links:
            if link_url.startswith('../') or link_url.startswith('./'):
                # 상대 경로 링크
                target_path = file_path.parent / link_url
                if not target_path.exists():
                    issues.append({
                        'file': rel_path,
                        'type': 'broken_link',
                        'severity': 'medium',
                        'message': f'깨진 링크: [{link_text}]({link_url})'
                    })

        # 5. 이미지 Alt 텍스트 누락
        images = re.findall(r'!\[([^\]]*)\]\(([^)]+)\)', body)
        for alt_text, img_url in images:
            if not alt_text or len(alt_text.strip()) == 0:
                issues.append({
                    'file': rel_path,
                    'type': 'missing_alt_text',
                    'severity': 'medium',
                    'message': f'이미지 Alt 누락: {img_url}'
                })

        # 6. Heading 계층 구조 체크
        headings = re.findall(r'^(#{1,6})\s+(.+)$', body, re.MULTILINE)
        prev_level = 0
        for heading_marks, heading_text in headings:
            level = len(heading_marks)
            if prev_level > 0 and level - prev_level > 1:
                issues.append({
                    'file': rel_path,
                    'type': 'heading_hierarchy',
                    'severity': 'low',
                    'message': f'Heading 계층 건너뜀: h{prev_level} → h{level}'
                })
            prev_level = level

        # 7. Keywords 밀도 체크 (제목 키워드가 본문에 적절히 사용되는지)
        title_words = set(re.findall(r'[가-힣]{2,}', title))
        body_text = re.sub(r'[^가-힣\s]', ' ', body)
        body_words = re.findall(r'[가-힣]{2,}', body_text)

        for keyword in title_words:
            if keyword not in ['지역', '정보', '가이드', '학습', '교육']:  # 일반적인 단어 제외
                count = body_words.count(keyword)
                if count < 2:
                    issues.append({
                        'file': rel_path,
                        'type': 'low_keyword_density',
                        'severity': 'low',
                        'message': f'제목 키워드 "{keyword}"가 본문에 {count}회만 등장'
                    })

        # 8. 콘텐츠와 카테고리 일치성 (일반 과목 학습법 패턴만 체크)
        if 'local' in rel_path:
            # 명확한 일반 과목 학습법 패턴만 체크
            generic_subject_patterns = [
                '## 📚 주요 과목 안내',
                '### 국어\n국어는 모든 학습의 기초',
                '### 수학\n수학은 논리적 사고력',
                '### 영어\n영어는 글로벌 시대',
                '### 과학\n과학은 자연 현상',
                '### 사회\n사회는 인간과 사회'
            ]

            has_generic_pattern = any(pattern in body for pattern in generic_subject_patterns)
            if has_generic_pattern:
                issues.append({
                    'file': rel_path,
                    'type': 'content_category_mismatch',
                    'severity': 'high',
                    'message': '지역 페이지인데 일반 과목 학습법 콘텐츠가 들어있음 (카테고리 불일치)'
                })

    except Exception as e:
        pass

    return issues

def main():
    content_dir = Path('content')
    all_issues = []

    for md_file in content_dir.rglob('*.md'):
        issues = check_file(md_file)
        all_issues.extend(issues)

    # 심각도별 분류
    critical = [i for i in all_issues if i['severity'] == 'critical']
    high = [i for i in all_issues if i['severity'] == 'high']
    medium = [i for i in all_issues if i['severity'] == 'medium']
    low = [i for i in all_issues if i['severity'] == 'low']

    print("=" * 80)
    print("🔍 SEO 및 개발 품질 검사 보고서")
    print("=" * 80)
    print(f"\n총 이슈: {len(all_issues)}개")
    print(f"  🚨 Critical: {len(critical)}개")
    print(f"  ⚠️  High    : {len(high)}개")
    print(f"  ⚡ Medium  : {len(medium)}개")
    print(f"  ℹ️  Low     : {len(low)}개")

    # Critical 이슈 출력
    if critical:
        print("\n" + "=" * 80)
        print("🚨 CRITICAL 이슈 (즉시 수정 필요)")
        print("=" * 80)
        for issue in critical[:10]:
            print(f"\n📄 {issue['file']}")
            print(f"   유형: {issue['type']}")
            print(f"   내용: {issue['message']}")
        if len(critical) > 10:
            print(f"\n... 외 {len(critical) - 10}개")

    # High 이슈 출력
    if high:
        print("\n" + "=" * 80)
        print("⚠️  HIGH 이슈 (우선 수정 권장)")
        print("=" * 80)
        for issue in high[:10]:
            print(f"\n📄 {issue['file']}")
            print(f"   유형: {issue['type']}")
            print(f"   내용: {issue['message']}")
        if len(high) > 10:
            print(f"\n... 외 {len(high) - 10}개")

    # Medium 이슈 출력
    if medium:
        print("\n" + "=" * 80)
        print("⚡ MEDIUM 이슈 (개선 권장)")
        print("=" * 80)
        for issue in medium[:5]:
            print(f"\n📄 {issue['file']}")
            print(f"   유형: {issue['type']}")
            print(f"   내용: {issue['message']}")
        if len(medium) > 5:
            print(f"\n... 외 {len(medium) - 5}개")

    print("\n" + "=" * 80)

if __name__ == '__main__':
    main()
