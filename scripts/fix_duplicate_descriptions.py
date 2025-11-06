#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
중복된 Description 개별화 스크립트
"""

from pathlib import Path
import re

# 중복 description 패턴들
DUPLICATE_PATTERNS = [
    "초등학생의 발달 단계에 맞춘 체계적인 학습법과 실천 가능한 교육 가이드를 제공합니다.",
    "중학생의 발달 단계에 맞춘 체계적인 학습법과 실천 가능한 교육 가이드를 제공합니다.",
    "고등학생의 발달 단계에 맞춘 체계적인 학습법과 실천 가능한 교육 가이드를 제공합니다.",
]

# Title 기반 description 생성 매핑
DESCRIPTION_TEMPLATES = {
    # 초등 1학년
    "초1": "초등학교 1학년의 학교 적응과 기초 학습을 돕습니다. 한글, 숫자 학습부터 친구 사귀기까지 1학년 필수 가이드를 제공합니다.",
    "입학": "초등학교 입학을 앞둔 예비 초등생을 위한 완벽 준비 가이드. 학교 적응과 기초 학습 습관 형성을 도와드립니다.",

    # 초등 2학년
    "초2": "초등 2학년의 본격적인 학습 시작을 지원합니다. 받아쓰기, 구구단 등 핵심 학습 내용과 효과적인 공부 방법을 안내합니다.",

    # 초등 3학년
    "초3": "초등 3학년의 학습 습관 형성 시기를 집중 지원합니다. 예습과 복습 방법부터 노트 필기까지 평생 가는 공부 습관을 만듭니다.",

    # 초등 4학년
    "초4": "초등 4학년의 사고력 향상을 위한 학습 전략을 제시합니다. 수학 문장제, 국어 독해 등 논리적 사고력을 키우는 방법을 안내합니다.",

    # 초등 5학년
    "초5": "초등 5학년의 심화 학습과 중등 준비를 돕습니다. 응용력과 사고력을 키우는 학습법으로 중학교 입학을 대비하세요.",

    # 초등 6학년
    "초6": "초등 6학년의 마무리와 중학교 준비를 완벽 지원합니다. 초등 과정 총정리와 중등 선행 학습 전략을 제공합니다.",

    # 주제별
    "학습 습관": "평생 가는 학습 습관 형성을 돕는 실천 가능한 가이드. 자기주도 학습 능력을 키우는 구체적인 방법을 제시합니다.",
    "수학": "수학 학습의 기초를 탄탄히 다지는 학년별 맞춤 전략. 연산부터 문장제까지 체계적인 수학 공부법을 안내합니다.",
    "독해": "독해력 향상을 위한 체계적인 학습 전략. 글 이해 능력을 키우는 단계별 훈련 방법을 제공합니다.",
    "받아쓰기": "받아쓰기 실력을 향상시키는 효과적인 학습법. 맞춤법 정복과 쓰기 능력 향상을 위한 실천 전략을 안내합니다.",
    "영어": "초등 영어 학습의 기초를 다지는 실용적인 가이드. 파닉스부터 단어 암기까지 효과적인 영어 공부법을 제시합니다.",
    "독서": "평생 독서 습관 형성을 위한 단계별 전략. 책 읽기의 즐거움을 느끼며 사고력을 키우는 방법을 안내합니다.",
    "사고력": "논리적 사고력과 창의력을 키우는 학습 전략. 단순 암기를 넘어 생각하는 힘을 기르는 방법을 제시합니다.",
    "시험": "초등 시험 준비를 위한 효율적인 공부 계획. 시험 전 복습 전략과 실전 대비 방법을 구체적으로 안내합니다.",
}

def generate_custom_description(title, content):
    """Title과 content 기반으로 맞춤 description 생성"""

    # Title에서 키워드 찾기
    for keyword, template in DESCRIPTION_TEMPLATES.items():
        if keyword in title:
            return template

    # 기본 description (title 기반)
    if "초등" in title:
        grade_num = re.search(r'(\d)학년', title)
        if grade_num:
            grade = grade_num.group(1)
            return f"초등 {grade}학년 학습을 위한 맞춤형 가이드. 이 시기에 꼭 필요한 학습 전략과 효과적인 공부 방법을 제공합니다."

    # 그 외
    return f"{title.split('|')[0].strip()}을 위한 실용적인 학습 가이드. 효과적인 학습 전략과 구체적인 실천 방법을 제시합니다."

def fix_description(file_path):
    """파일의 중복 description 수정"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Front matter 파싱
        if not content.startswith('---'):
            return False, "front matter 없음"

        parts = content.split('---', 2)
        if len(parts) < 3:
            return False, "front matter 파싱 실패"

        front_matter = parts[1]
        body = parts[2]

        # Title 추출
        title_match = re.search(r'^title:\s*(.+)$', front_matter, re.MULTILINE)
        if not title_match:
            return False, "title 없음"

        title = title_match.group(1).strip()

        # Description 중복 체크
        has_duplicate = False
        for pattern in DUPLICATE_PATTERNS:
            if pattern in front_matter:
                has_duplicate = True
                break

        if not has_duplicate:
            return False, "중복 없음"

        # 새 description 생성
        new_desc = generate_custom_description(title, body)

        # Description 교체
        new_front_matter = re.sub(
            r'description:.*?(?=\n[a-z_]+:|$)',
            f'description: {new_desc}',
            front_matter,
            flags=re.DOTALL
        )

        # 파일 저장
        new_content = f"---{new_front_matter}---{body}"

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        rel_path = str(file_path.relative_to(Path('content')))
        return True, rel_path

    except Exception as e:
        return False, f"오류: {e}"

def main():
    content_dir = Path('content')

    fixed_count = 0
    fixed_files = []

    print("🔧 Description 중복 제거 시작...\n")

    # elementary 디렉토리만 처리
    for md_file in content_dir.glob('elementary/*.md'):
        success, result = fix_description(md_file)

        if success:
            fixed_count += 1
            fixed_files.append(result)

            if fixed_count <= 10 or fixed_count % 10 == 0:
                print(f"✅ [{fixed_count}] {result}")

    print("\n" + "=" * 80)
    print("📊 Description 개별화 완료")
    print("=" * 80)
    print(f"수정된 파일: {fixed_count}개")

    if fixed_files and len(fixed_files) <= 20:
        print("\n수정된 파일 목록:")
        for file in fixed_files:
            print(f"  - {file}")

    print("=" * 80)

if __name__ == '__main__':
    main()
