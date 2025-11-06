#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
과목별 파일 350개 SEO 상태 분석
"""

from pathlib import Path
import re

def analyze_file(file_path):
    """파일 SEO 상태 분석"""
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

        # Description 길이
        desc_match = re.search(r'^description:\s*["\']?(.+?)["\']?(?=\n[a-z_]+:|$)', front_matter, re.MULTILINE | re.DOTALL)
        desc_length = len(desc_match.group(1).strip()) if desc_match else 0

        # Tags 개수
        tags_match = re.search(r'^tags:\s*(\[.+?\])', front_matter, re.MULTILINE | re.DOTALL)
        if tags_match:
            tags_str = tags_match.group(1)
            tags_count = len(re.findall(r'"[^"]+"|\'[^\']+\'|\w+', tags_str))
        else:
            tags_count = 0

        # Featured Image 존재
        has_image = bool(re.search(r'^featured_image:', front_matter, re.MULTILINE))

        # 콘텐츠 단어 수 (한글 공백 기준)
        words = len(body.split())

        # Reading time
        has_reading_time = bool(re.search(r'^reading_time:', front_matter, re.MULTILINE))

        return {
            'path': str(file_path.relative_to(Path('content'))),
            'desc_length': desc_length,
            'tags_count': tags_count,
            'has_image': has_image,
            'words': words,
            'has_reading_time': has_reading_time
        }
    except:
        return None

def main():
    content_dir = Path('content/subjects')

    print("🔍 과목별 파일 350개 SEO 상태 분석\n")

    results = []
    for md_file in sorted(content_dir.glob('**/*.md')):
        if md_file.name.startswith('_'):
            continue

        result = analyze_file(md_file)
        if result:
            results.append(result)

    print(f"총 파일 수: {len(results)}개\n")

    # 통계
    desc_short = [r for r in results if r['desc_length'] < 150]
    tags_low = [r for r in results if r['tags_count'] < 8]
    no_image = [r for r in results if not r['has_image']]
    short_content = [r for r in results if r['words'] < 500]
    no_reading_time = [r for r in results if not r['has_reading_time']]

    print("=" * 80)
    print("📊 SEO 현황")
    print("=" * 80)
    print(f"✅ Description 150자 이상: {len(results) - len(desc_short)}개 ({(len(results) - len(desc_short))/len(results)*100:.1f}%)")
    print(f"⚠️  Description 150자 미만: {len(desc_short)}개")
    print()
    print(f"✅ Tags 8개 이상: {len(results) - len(tags_low)}개 ({(len(results) - len(tags_low))/len(results)*100:.1f}%)")
    print(f"⚠️  Tags 8개 미만: {len(tags_low)}개")
    print()
    print(f"✅ Featured Image 있음: {len(results) - len(no_image)}개 ({(len(results) - len(no_image))/len(results)*100:.1f}%)")
    print(f"⚠️  Featured Image 없음: {len(no_image)}개")
    print()
    print(f"✅ 콘텐츠 500단어 이상: {len(results) - len(short_content)}개 ({(len(results) - len(short_content))/len(results)*100:.1f}%)")
    print(f"⚠️  콘텐츠 500단어 미만: {len(short_content)}개")
    print()
    print(f"✅ Reading Time 있음: {len(results) - len(no_reading_time)}개 ({(len(results) - len(no_reading_time))/len(results)*100:.1f}%)")
    print(f"⚠️  Reading Time 없음: {len(no_reading_time)}개")
    print("=" * 80)

    # 평균
    avg_desc = sum(r['desc_length'] for r in results) / len(results)
    avg_tags = sum(r['tags_count'] for r in results) / len(results)
    avg_words = sum(r['words'] for r in results) / len(results)

    print("\n📈 평균 수치")
    print(f"Description 평균: {avg_desc:.1f}자")
    print(f"Tags 평균: {avg_tags:.1f}개")
    print(f"콘텐츠 평균: {avg_words:.0f}단어")

    # 개선 필요 파일 목록
    needs_improvement = []
    for r in results:
        issues = []
        if r['desc_length'] < 150:
            issues.append('desc')
        if r['tags_count'] < 8:
            issues.append('tags')
        if not r['has_image']:
            issues.append('image')
        if r['words'] < 500:
            issues.append('content')
        if not r['has_reading_time']:
            issues.append('reading_time')

        if issues:
            needs_improvement.append({
                'path': r['path'],
                'issues': issues
            })

    if needs_improvement:
        print(f"\n\n⚠️  개선 필요 파일: {len(needs_improvement)}개")
        print("=" * 80)
        for item in needs_improvement[:10]:
            print(f"\n{item['path']}")
            print(f"  문제: {', '.join(item['issues'])}")

    print(f"\n\n💡 총 {len(needs_improvement)}개 파일이 개선 필요")

if __name__ == '__main__':
    main()
