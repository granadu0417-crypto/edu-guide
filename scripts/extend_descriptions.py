#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Description을 150자 이상으로 확장
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

def extend_description(front_matter, rel_path, body):
    """Description 확장"""
    current_desc = front_matter.get('description', '')

    # 이미 150자 이상이면 유지
    if len(current_desc) >= 150:
        return current_desc

    title = front_matter.get('title', '')
    category = rel_path.split('/')[0]

    # 카테고리별 추가 문구
    extensions = {
        'elementary': ' 초등학생의 발달 단계에 맞춘 체계적인 학습법과 실천 가능한 교육 가이드를 제공합니다.',
        'middle': ' 중학생 내신 관리부터 자기주도 학습 능력 향상까지 단계별 학습 전략을 안내합니다.',
        'high': ' 대입 준비의 모든 것, 내신과 수능을 동시에 잡는 효율적인 학습 전략을 제시합니다.',
        'subjects': ' 과목별 특성을 고려한 맞춤형 학습법으로 성적 향상의 기초를 다져보세요.',
        'exam': ' 시험 준비부터 실전 응시까지, 체계적인 시험 전략으로 목표 달성을 돕겠습니다.',
        'tutoring': ' 과외 선택부터 효과적인 활용까지, 1:1 맞춤 지도의 모든 것을 알려드립니다.',
        'consultation': ' 전문가의 맞춤형 교육 컨설팅으로 학습 고민을 해결하고 명확한 방향을 설정하세요.',
        'local': ' 지역별 교육 환경과 학원 정보를 바탕으로 최적의 학습 환경을 찾아드립니다.'
    }

    # 기본 확장 문구
    base_extension = ' 체계적인 학습 전략과 실천 가능한 가이드로 목표 달성을 지원합니다.'

    # 카테고리에 맞는 확장 문구 선택
    extension = extensions.get(category, base_extension)

    # Description 확장
    extended_desc = current_desc.rstrip('.') + extension

    # 150자 이상 보장 - 더 강력한 확장
    while len(extended_desc) < 150:
        # 추가 보강 문구
        if '초등' in title or category == 'elementary':
            if len(extended_desc) < 150:
                extended_desc += ' 학부모님과 함께하는 효과적인 교육 방법을 안내합니다.'
            if len(extended_desc) < 150:
                extended_desc += ' 지금 바로 시작하세요.'
        elif '중등' in title or '중학' in title or category == 'middle':
            if len(extended_desc) < 150:
                extended_desc += ' 학년별 특성에 맞는 구체적인 학습 방법을 제시합니다.'
            if len(extended_desc) < 150:
                extended_desc += ' 내신 관리의 모든 것을 알려드립니다.'
        elif '고등' in title or category == 'high':
            if len(extended_desc) < 150:
                extended_desc += ' 입시 전문가의 노하우로 합격 전략을 설계합니다.'
            if len(extended_desc) < 150:
                extended_desc += ' 수능 대비 완벽 가이드를 제공합니다.'
        elif '과외' in title or category == 'tutoring':
            if len(extended_desc) < 150:
                extended_desc += ' 검증된 정보로 현명한 선택을 도와드립니다.'
            if len(extended_desc) < 150:
                extended_desc += ' 효과적인 1:1 맞춤 학습을 경험하세요.'
        elif '상담' in title or category == 'consultation':
            if len(extended_desc) < 150:
                extended_desc += ' 지금 바로 학습 고민을 해결하세요.'
            if len(extended_desc) < 150:
                extended_desc += ' 전문가의 상세한 가이드를 확인하세요.'
        elif category == 'local':
            if len(extended_desc) < 150:
                extended_desc += ' 우리 지역 최고의 교육 정보를 제공합니다.'
            if len(extended_desc) < 150:
                extended_desc += ' 학원 선택부터 관리까지 완벽 가이드를 드립니다.'
        else:
            if len(extended_desc) < 150:
                extended_desc += ' 단계별로 자세하게 안내드립니다.'
            if len(extended_desc) < 150:
                extended_desc += ' 효과적인 학습 방법을 지금 확인하세요.'

    return extended_desc

def process_file(file_path):
    """파일 처리"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        front_matter, body = extract_front_matter(content)
        if not front_matter:
            return False, "front matter 없음"

        rel_path = str(file_path.relative_to(Path('content')))
        current_desc = front_matter.get('description', '')

        # 이미 150자 이상이면 스킵
        if len(current_desc) >= 150:
            return False, f"이미 충분 ({len(current_desc)}자)"

        # Description 확장
        extended_desc = extend_description(front_matter, rel_path, body)

        # front matter 업데이트
        front_matter['description'] = extended_desc

        # YAML 직렬화
        yaml_str = yaml.dump(front_matter, allow_unicode=True, sort_keys=False, default_flow_style=False)

        # 새 콘텐츠 작성
        new_content = f"---\n{yaml_str}---{body}"

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        return True, f"{rel_path}: {len(current_desc)}자 → {len(extended_desc)}자"

    except Exception as e:
        return False, f"오류: {e}"

def main():
    content_dir = Path('content')

    success_count = 0
    skip_count = 0
    error_count = 0

    print("📝 Description 확장 시작...\n")

    for md_file in content_dir.rglob('*.md'):
        success, message = process_file(md_file)

        if success:
            success_count += 1
            print(f"✅ {message}")
        elif "이미 충분" in message:
            skip_count += 1
        else:
            error_count += 1
            if "front matter" not in message:
                print(f"❌ {md_file}: {message}")

    print("\n" + "=" * 80)
    print("📊 Description 확장 완료")
    print("=" * 80)
    print(f"확장 완료: {success_count}개")
    print(f"스킵    : {skip_count}개")
    print(f"오류    : {error_count}개")
    print("=" * 80)

if __name__ == '__main__':
    main()
