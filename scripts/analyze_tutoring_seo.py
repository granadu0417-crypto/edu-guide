#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tutoring 폴더 SEO 상태 분석
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

        # 콘텐츠 단어 수
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
    content_dir = Path('content/tutoring')

    print("🔍 Tutoring 폴더 SEO 상태 분석\n")

    files_data = []
    for md_file in content_dir.rglob('*.md'):
        data = analyze_file(md_file)
        if data:
            files_data.append(data)

    if not files_data:
        print("❌ 분석할 파일이 없습니다.")
        return

    print(f"총 파일 수: {len(files_data)}개\n")

    # 통계
    desc_150_plus = sum(1 for f in files_data if f['desc_length'] >= 150)
    desc_under_150 = len(files_data) - desc_150_plus

    tags_8_plus = sum(1 for f in files_data if f['tags_count'] >= 8)
    tags_under_8 = len(files_data) - tags_8_plus

    has_image = sum(1 for f in files_data if f['has_image'])
    no_image = len(files_data) - has_image

    words_500_plus = sum(1 for f in files_data if f['words'] >= 500)
    words_under_500 = len(files_data) - words_500_plus

    has_reading = sum(1 for f in files_data if f['has_reading_time'])
    no_reading = len(files_data) - has_reading

    # 평균
    avg_desc = sum(f['desc_length'] for f in files_data) / len(files_data)
    avg_tags = sum(f['tags_count'] for f in files_data) / len(files_data)
    avg_words = sum(f['words'] for f in files_data) / len(files_data)

    print("=" * 80)
    print("📊 SEO 현황")
    print("=" * 80)
    print(f"✅ Description 150자 이상: {desc_150_plus}개 ({desc_150_plus/len(files_data)*100:.1f}%)")
    print(f"⚠️  Description 150자 미만: {desc_under_150}개")
    print()
    print(f"✅ Tags 8개 이상: {tags_8_plus}개 ({tags_8_plus/len(files_data)*100:.1f}%)")
    print(f"⚠️  Tags 8개 미만: {tags_under_8}개")
    print()
    print(f"✅ Featured Image 있음: {has_image}개 ({has_image/len(files_data)*100:.1f}%)")
    print(f"⚠️  Featured Image 없음: {no_image}개")
    print()
    print(f"✅ 콘텐츠 500단어 이상: {words_500_plus}개 ({words_500_plus/len(files_data)*100:.1f}%)")
    print(f"⚠️  콘텐츠 500단어 미만: {words_under_500}개")
    print()
    print(f"✅ Reading Time 있음: {has_reading}개 ({has_reading/len(files_data)*100:.1f}%)")
    print(f"⚠️  Reading Time 없음: {no_reading}개")
    print("=" * 80)
    print()
    print("📈 평균 수치")
    print(f"Description 평균: {avg_desc:.1f}자")
    print(f"Tags 평균: {avg_tags:.1f}개")
    print(f"콘텐츠 평균: {avg_words:.0f}단어")
    print()

    # 개선 필요 파일 목록
    needs_improvement = []
    for f in files_data:
        issues = []
        if f['desc_length'] < 150:
            issues.append('desc')
        if f['tags_count'] < 8:
            issues.append('tags')
        if not f['has_image']:
            issues.append('image')
        if f['words'] < 500:
            issues.append('words')
        if not f['has_reading_time']:
            issues.append('reading')

        if issues:
            needs_improvement.append((f['path'], issues))

    if needs_improvement:
        print("⚠️  개선 필요 파일:", len(needs_improvement), "개")
        print("=" * 80)
        print()
        for path, issues in needs_improvement[:10]:
            print(f"{path}")
            print(f"  문제: {', '.join(issues)}")
            print()

        if len(needs_improvement) > 10:
            print(f"... 외 {len(needs_improvement) - 10}개 더")

    print(f"\n💡 총 {len(needs_improvement)}개 파일이 개선 필요")
    print("=" * 80)

if __name__ == '__main__':
    main()
