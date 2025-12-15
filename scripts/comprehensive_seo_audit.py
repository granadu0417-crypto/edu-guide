#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
종합 SEO 감사 스크립트
모든 문제를 찾아냅니다
"""

from pathlib import Path
import re
from collections import defaultdict, Counter

class SEOAuditor:
    def __init__(self, content_dir='content'):
        self.content_dir = Path(content_dir)
        self.issues = defaultdict(list)
        self.stats = defaultdict(int)

    def audit_file(self, file_path):
        """파일별 SEO 감사"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Front matter 파싱
            if not content.startswith('---'):
                self.issues['no_frontmatter'].append(str(file_path))
                return

            parts = content.split('---', 2)
            if len(parts) < 3:
                self.issues['invalid_frontmatter'].append(str(file_path))
                return

            front_matter = parts[1]
            body = parts[2]

            rel_path = str(file_path.relative_to(self.content_dir))

            # 1. Title 체크
            title_match = re.search(r'^title:\s*(.+)$', front_matter, re.MULTILINE)
            if not title_match:
                self.issues['missing_title'].append(rel_path)
            else:
                title = title_match.group(1).strip()
                if len(title) < 10:
                    self.issues['title_too_short'].append(f"{rel_path} ({len(title)}자)")
                if len(title) > 60:
                    self.issues['title_too_long'].append(f"{rel_path} ({len(title)}자)")
                if title.count('|') > 2:
                    self.issues['title_too_many_separators'].append(rel_path)

            # 2. Description 체크
            desc_match = re.search(r'^description:\s*(.+?)(?=\n[a-z_]+:|$)', front_matter, re.MULTILINE | re.DOTALL)
            if not desc_match:
                self.issues['missing_description'].append(rel_path)
            else:
                desc = desc_match.group(1).strip()
                if len(desc) < 50:
                    self.issues['description_too_short'].append(f"{rel_path} ({len(desc)}자)")
                if len(desc) > 160:
                    self.issues['description_too_long'].append(f"{rel_path} ({len(desc)}자)")

            # 3. Featured Image 체크
            image_match = re.search(r'^featured_image:\s*(.+)$', front_matter, re.MULTILINE)
            if not image_match:
                self.issues['missing_featured_image'].append(rel_path)

            # 4. Tags 체크 (수정된 정규식)
            tags_match = re.search(r'^tags:\s*\n((?:- .+\n?)+)', front_matter, re.MULTILINE)
            if not tags_match:
                self.issues['missing_tags'].append(rel_path)
            else:
                tags_content = tags_match.group(1)
                tag_count = len(re.findall(r'^-\s+', tags_content, re.MULTILINE))
                if tag_count < 3:
                    self.issues['tags_too_few'].append(f"{rel_path} ({tag_count}개)")
                if tag_count > 15:
                    self.issues['tags_too_many'].append(f"{rel_path} ({tag_count}개)")

            # 5. Categories 체크 (수정된 정규식)
            cat_match = re.search(r'^categories:\s*\n((?:- .+\n?)+)', front_matter, re.MULTILINE)
            if not cat_match:
                self.issues['missing_categories'].append(rel_path)

            # 6. Body 콘텐츠 체크
            body_text = re.sub(r'#+\s+', '', body)  # 헤딩 제거
            body_text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', body_text)  # 링크 텍스트만
            body_text = re.sub(r'[*_`]', '', body_text)  # 마크다운 제거
            word_count = len(body_text.split())

            if word_count < 300:
                self.issues['content_too_short'].append(f"{rel_path} ({word_count}단어)")

            # 7. 헤딩 구조 체크
            headings = re.findall(r'^(#{1,6})\s+(.+)$', body, re.MULTILINE)
            if not headings:
                self.issues['no_headings'].append(rel_path)
            else:
                h1_count = sum(1 for h in headings if h[0] == '#')
                if h1_count > 1:
                    self.issues['multiple_h1'].append(f"{rel_path} ({h1_count}개)")

            # 8. 내부 링크 체크
            internal_links = re.findall(r'\[([^\]]+)\]\((/[^\)]+)\)', body)
            if len(internal_links) < 2:
                self.issues['few_internal_links'].append(f"{rel_path} ({len(internal_links)}개)")

            # 통계
            self.stats['total_files'] += 1
            self.stats['total_words'] += word_count

        except Exception as e:
            self.issues['file_read_error'].append(f"{rel_path}: {e}")

    def check_duplicates(self):
        """중복 콘텐츠 체크"""
        titles = defaultdict(list)
        descriptions = defaultdict(list)

        for md_file in self.content_dir.glob('**/*.md'):
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                title_match = re.search(r'^title:\s*(.+)$', content, re.MULTILINE)
                if title_match:
                    title = title_match.group(1).strip()
                    titles[title].append(str(md_file.relative_to(self.content_dir)))

                desc_match = re.search(r'^description:\s*(.+?)(?=\n[a-z_]+:|$)', content, re.MULTILINE | re.DOTALL)
                if desc_match:
                    desc = desc_match.group(1).strip()
                    descriptions[desc].append(str(md_file.relative_to(self.content_dir)))
            except:
                continue

        # 중복 발견
        for title, files in titles.items():
            if len(files) > 1:
                self.issues['duplicate_titles'].append(f"{title[:50]}... ({len(files)}개 파일)")

        for desc, files in descriptions.items():
            if len(files) > 1 and len(desc) > 50:  # 짧은 description은 무시
                self.issues['duplicate_descriptions'].append(f"{desc[:80]}... → {', '.join(files[:3])}")

    def run_audit(self):
        """전체 감사 실행"""
        print("🔍 종합 SEO 감사 시작...\n")

        # 1. 개별 파일 감사
        print("📄 파일별 감사 중...")
        for md_file in self.content_dir.glob('**/*.md'):
            if md_file.name.startswith('_'):
                continue
            self.audit_file(md_file)

        # 2. 중복 체크
        print("🔁 중복 콘텐츠 체크 중...")
        self.check_duplicates()

        # 3. 결과 출력
        self.print_report()

    def print_report(self):
        """감사 리포트 출력"""
        print("\n" + "=" * 80)
        print("📊 SEO 감사 결과")
        print("=" * 80)

        print(f"\n전체 파일: {self.stats['total_files']}개")
        print(f"전체 단어: {self.stats['total_words']:,}개")
        print(f"평균 단어: {self.stats['total_words'] // max(self.stats['total_files'], 1)}개/파일")

        if not self.issues:
            print("\n✅ 문제 없음! 완벽합니다!")
            return

        print(f"\n발견된 이슈 카테고리: {len(self.issues)}개")

        # 심각도별 분류
        critical = ['missing_title', 'missing_description', 'no_frontmatter']
        high = ['title_too_short', 'description_too_short', 'content_too_short', 'missing_featured_image']
        medium = ['title_too_long', 'description_too_long', 'missing_tags', 'tags_too_few']

        # Critical 이슈
        critical_issues = {k: v for k, v in self.issues.items() if k in critical}
        if critical_issues:
            print(f"\n🔴 CRITICAL 이슈 ({sum(len(v) for v in critical_issues.values())}개)")
            for issue_type, files in critical_issues.items():
                print(f"\n  [{issue_type}] {len(files)}개")
                for f in files[:3]:
                    print(f"    - {f}")
                if len(files) > 3:
                    print(f"    ... 외 {len(files) - 3}개")

        # High 이슈
        high_issues = {k: v for k, v in self.issues.items() if k in high}
        if high_issues:
            print(f"\n🟡 HIGH 이슈 ({sum(len(v) for v in high_issues.values())}개)")
            for issue_type, files in high_issues.items():
                print(f"\n  [{issue_type}] {len(files)}개")
                for f in files[:3]:
                    print(f"    - {f}")
                if len(files) > 3:
                    print(f"    ... 외 {len(files) - 3}개")

        # Medium 이슈
        medium_issues = {k: v for k, v in self.issues.items() if k in medium}
        if medium_issues:
            print(f"\n🟢 MEDIUM 이슈 ({sum(len(v) for v in medium_issues.values())}개)")
            for issue_type, files in medium_issues.items():
                print(f"\n  [{issue_type}] {len(files)}개")
                for f in files[:3]:
                    print(f"    - {f}")
                if len(files) > 3:
                    print(f"    ... 외 {len(files) - 3}개")

        # 기타 이슈
        other_issues = {k: v for k, v in self.issues.items()
                       if k not in critical and k not in high and k not in medium}
        if other_issues:
            print(f"\n⚪ 기타 이슈 ({sum(len(v) for v in other_issues.values())}개)")
            for issue_type, files in other_issues.items():
                print(f"\n  [{issue_type}] {len(files)}개")
                if issue_type == 'duplicate_descriptions':
                    # 중복 description 상세 출력
                    for item in files[:10]:  # 처음 10개만
                        print(f"    - {item}")
                    if len(files) > 10:
                        print(f"    ... 외 {len(files) - 10}개")

        print("\n" + "=" * 80)

if __name__ == '__main__':
    auditor = SEOAuditor()
    auditor.run_audit()
