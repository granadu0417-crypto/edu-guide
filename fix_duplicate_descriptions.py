#!/usr/bin/env python3
"""
중복된 description을 제목 기반으로 고유하게 변경하는 스크립트
SEO 최적화: 각 페이지는 고유한 description을 가져야 함
"""

import os
import re
from pathlib import Path

def extract_title(content):
    """frontmatter에서 title 추출"""
    title_match = re.search(r'title:\s*(.+)', content)
    if title_match:
        return title_match.group(1).strip()
    return None

def extract_description(content):
    """frontmatter에서 description 추출"""
    desc_match = re.search(r'description:\s*(.+?)(?=\n[a-z_]+:|$)', content, re.DOTALL)
    if desc_match:
        desc = desc_match.group(1).strip()
        desc = ' '.join(desc.split())
        desc = desc.strip('"\'')
        return desc
    return None

def generate_unique_description(filepath, title, old_desc):
    """파일 경로와 제목을 기반으로 고유한 description 생성"""

    path_str = str(filepath)

    # 카테고리별 맞춤 description 생성

    # 1. 과외 찾기 (private tutoring)
    if 'tutoring/private/' in path_str:
        # 과목 이름 추출
        subject = title.split('과외')[0].split('1:1')[0].split('온라인')[0].split('방문')[0].strip()

        endings = [
            "전문 선생님 매칭과 효과적인 학습 관리 전략을 제공합니다.",
            "맞춤형 커리큘럼과 체계적인 학습 관리로 목표를 달성하세요.",
            "우수한 선생님 선택과 효율적인 과외 활용법을 안내합니다.",
            "검증된 선생님과 함께하는 1:1 맞춤 학습으로 실력을 향상시키세요.",
            "개인별 학습 진단과 맞춤형 지도로 빠른 성과를 만들어보세요."
        ]

        hash_val = abs(hash(filepath)) % len(endings)
        return f"{subject} 1:1 과외의 모든 것. 선택 기준, 시세, 효과적 활용법을 상세히 안내합니다. {endings[hash_val]}"

    # 2. 학원 찾기 (academy)
    elif 'tutoring/academy/' in path_str:
        subject = title.split('학원')[0].strip()

        endings = [
            "우수 학원 추천과 효과적인 학습 전략을 제시합니다.",
            "학년별 맞춤 커리큘럼과 체계적인 관리 시스템을 소개합니다.",
            "검증된 학원 정보와 1:1 과외 병행 전략을 안내합니다.",
            "전문 강사진과 함께하는 체계적인 학습으로 실력을 키우세요.",
            "학원 선택 기준과 효율적인 활용법을 상세히 설명합니다."
        ]

        hash_val = abs(hash(filepath)) % len(endings)
        return f"{subject} 학원 완벽 가이드. 유형별 특징, 선택 기준, 비용 정보를 제공합니다. {endings[hash_val]}"

    # 3. 지역별 과외 (local)
    elif 'local/' in path_str:
        area_match = re.search(r'local/seoul/([^/]+)', path_str)
        if area_match:
            area_name = area_match.group(1).replace('-', ' ')

            endings = [
                "지역 맞춤 학습 전략과 우수 선생님 정보를 제공합니다.",
                "지역 특성을 반영한 효과적인 과외 선택 가이드입니다.",
                "검증된 지역 선생님과 학원 정보를 상세히 안내합니다.",
                "지역별 교육 환경 분석과 최적의 학습 전략을 제시합니다.",
                "우리 동네 최고의 과외와 학원 선택 노하우를 공개합니다."
            ]

            hash_val = abs(hash(filepath)) % len(endings)
            return f"{title}. 지역 교육 환경, 우수 학원, 과외 시세 정보를 제공합니다. {endings[hash_val]}"

    # 4. 고등학교 학습 (high)
    elif 'high/' in path_str:
        endings = [
            "대학 입시를 위한 실전 전략과 공부법을 제시합니다.",
            "내신과 수능을 동시에 준비하는 효율적인 학습법을 안내합니다.",
            "상위권 진입을 위한 과목별 학습 전략을 상세히 설명합니다.",
            "체계적인 시간 관리와 효과적인 공부법으로 목표를 달성하세요.",
            "입시 성공을 위한 학년별 맞춤 전략과 실천 방법을 제공합니다."
        ]

        hash_val = abs(hash(filepath)) % len(endings)
        return f"{title}. 고등학생 필수 학습 전략과 공부법을 안내합니다. {endings[hash_val]}"

    # 5. 중학교 학습 (middle)
    elif 'middle/' in path_str:
        endings = [
            "중학생 맞춤 학습법과 성적 향상 전략을 제시합니다.",
            "초등과는 다른 중등 학습 전략과 시험 대비법을 안내합니다.",
            "자기주도 학습 습관 형성과 효율적인 공부법을 설명합니다.",
            "내신 관리부터 고교 준비까지 체계적인 전략을 제공합니다.",
            "학교 적응과 성적 향상을 위한 실전 노하우를 공개합니다."
        ]

        hash_val = abs(hash(filepath)) % len(endings)
        return f"{title}. {endings[hash_val]}"

    # 6. 시험 대비 (exam)
    elif 'exam/' in path_str:
        endings = [
            "효과적인 시험 준비 전략과 과목별 공부법을 안내합니다.",
            "시험 2주 전부터 당일까지 완벽 대비 플랜을 제시합니다.",
            "핵심 개념 정리부터 실전 문제 풀이까지 체계적으로 준비하세요.",
            "시험 기간 시간 관리와 멘탈 관리 노하우를 공유합니다.",
            "과목별 출제 경향 분석과 효율적인 학습법을 제공합니다."
        ]

        hash_val = abs(hash(filepath)) % len(endings)
        return f"{title}. {endings[hash_val]}"

    # 7. 학습 상담 (consultation)
    elif 'consultation/' in path_str:
        endings = [
            "전문가의 1:1 학습 진단과 맞춤형 솔루션을 제공합니다.",
            "학습 문제 분석부터 해결 전략까지 체계적으로 안내합니다.",
            "성적 향상을 위한 실질적인 상담과 코칭을 받아보세요.",
            "맞춤형 학습 설계와 효과적인 관리 전략을 제시합니다.",
            "전문 컨설턴트의 심층 분석과 실행 가능한 플랜을 받으세요."
        ]

        hash_val = abs(hash(filepath)) % len(endings)
        return f"{title}. {endings[hash_val]}"

    # 8. 과외 가이드 (tutoring guide)
    elif 'tutoring/guide/' in path_str or 'tutoring/tutoring-guide' in path_str:
        endings = [
            "성공적인 과외를 위한 선택부터 활용까지 완벽 가이드입니다.",
            "효과적인 과외 활용 전략과 학습 관리 노하우를 제공합니다.",
            "과외 선생님 선택부터 학습 목표 달성까지 상세히 안내합니다.",
            "1:1 맞춤 학습의 모든 것을 체계적으로 설명합니다.",
            "과외 효과 극대화를 위한 실전 전략과 팁을 공개합니다."
        ]

        hash_val = abs(hash(filepath)) % len(endings)
        return f"{title}. {endings[hash_val]}"

    # 기본값: 제목 + 다양한 마무리
    else:
        endings = [
            "효과적인 학습 전략과 실천 방법을 상세히 안내합니다.",
            "체계적인 준비와 맞춤형 전략으로 목표를 달성하세요.",
            "전문가의 노하우와 검증된 방법을 제공합니다.",
            "실전에서 바로 적용 가능한 구체적인 팁을 공유합니다.",
            "성공적인 학습을 위한 완벽 가이드입니다."
        ]

        hash_val = abs(hash(filepath)) % len(endings)
        return f"{title}. {endings[hash_val]}"

def fix_description_in_file(filepath):
    """파일의 description을 고유하게 변경"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        title = extract_title(content)
        old_desc = extract_description(content)

        if not title or not old_desc:
            return False

        # 새로운 고유 description 생성
        new_desc = generate_unique_description(filepath, title, old_desc)

        # description 교체 (여러 줄일 수 있으므로 정규식 사용)
        new_content = re.sub(
            r'(description:\s*)(.+?)(?=\n[a-z_]+:|featured_image:)',
            f'\\1{new_desc}\n',
            content,
            flags=re.DOTALL
        )

        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True

        return False

    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def main():
    """메인 함수"""
    content_path = Path("/mnt/c/Users/user/Desktop/클로드/에듀코리아/edu-guide/content")

    # 중복된 파일 리스트 (앞서 분석 결과 기반)
    duplicate_files = [
        # consultation
        "consultation/consultation-guide-11.md",
        "consultation/consultation-guide-3.md",
        "consultation/consultation-guide-31.md",
        "consultation/consultation-guide-43.md",
        "consultation/consultation-guide-25.md",
        "consultation/consultation-guide-45.md",
        "consultation/consultation-guide-47.md",
        "consultation/consultation-guide-7.md",

        # exam
        "exam/exam-preparation-11.md",
        "exam/exam-preparation-6.md",
        "exam/exam-preparation-46.md",
        "exam/exam-preparation-56.md",

        # high
        "high/admissions-strategy.md",
        "high/high-batch8-1.md",
        "high/mental-management.md",
        "high/high-b13-1.md",
        "high/high-final-1.md",
        "high/online-lecture-guide.md",
        "high/high-b10-2.md",
        "high/high-batch8-2.md",
        "high/high-b11-2.md",
        "high/high-b14-2.md",
        "high/high-b12-1.md",
        "high/high-b15-1.md",
        "high/high-b13-2.md",
        "high/high-b15-2.md",
        "high/high-b14-1.md",
        "high/korean-reading-strategy.md",
        "high/high-b14-3.md",
        "high/high-batch7-3.md",
        "high/high-b9-1.md",
        "high/high-final-11.md",
        "high/high-batch7-2.md",
        "high/high-final-2.md",
        "high/high-final-4.md",
        "high/high-final-9.md",
        "high/math-strategy.md",
        "high/school-record-management.md",

        # middle
        "middle/descriptive-assessment-strategy.md",
        "middle/math-geometry-functions.md",
        "middle/mid-b9-1.md",
        "middle/mid-b10-2.md",
        "middle/mid-b13-2.md",
        "middle/mid-b15-2.md",
        "middle/mid-b13-1.md",
        "middle/science-lab-notebook.md",
        "middle/time-management-planning.md",
        "middle/mid-b10-1.md",
        "middle/mid-b15-1.md",
        "middle/mid-b11-3.md",
        "middle/mid-b9-3.md",
        "middle/middle-final-1.md",
        "middle/self-directed-learning-complete-guide.md",

        # local
        "local/seoul/gangbuk-math-tutoring.md",
        "local/seoul/gangseo-english-tutoring.md",
        "local/seoul/seocho-math-tutoring.md",
        "local/seoul/dobong-math-tutoring.md",
        "local/seoul/geumcheon-math-tutoring.md",
        "local/seoul/geumcheon-english-tutoring.md",
        "local/seoul/gwangjin-english-tutoring.md",

        # tutoring/academy
        "tutoring/academy/high-english-academy.md",
        "tutoring/academy/high-math-academy.md",
        "tutoring/academy/science-academy.md",
        "tutoring/academy/boarding-academy.md",
        "tutoring/academy/naesin-specialized-academy.md",
        "tutoring/academy/dankwa-vs-jonghap-academy.md",
        "tutoring/academy/managed-academy.md",
        "tutoring/academy/elementary-academy-guide.md",
        "tutoring/academy/jaejong-academy.md",
        "tutoring/academy/essay-academy.md",
        "tutoring/academy/middle-math-academy.md",
        "tutoring/academy/japanese-academy.md",
        "tutoring/academy/special-highschool-academy.md",
        "tutoring/academy/korean-academy.md",
        "tutoring/academy/social-studies-academy.md",

        # tutoring/private
        "tutoring/private/elementary-math-tutoring.md",
        "tutoring/private/english-conversation-tutoring.md",
        "tutoring/private/suneung-math-tutoring.md",
        "tutoring/private/toeic-tutoring.md",
        "tutoring/private/art-tutoring.md",
        "tutoring/private/biology-tutoring.md",
        "tutoring/private/chemistry-tutoring.md",
        "tutoring/private/chinese-tutoring.md",
        "tutoring/private/korean-history-tutoring.md",
        "tutoring/private/middle-math-tutoring.md",
        "tutoring/private/gifted-tutoring.md",
        "tutoring/private/high-math-tutoring.md",
        "tutoring/private/korean-tutoring.md",
        "tutoring/private/bundang-visiting-tutoring.md",
        "tutoring/private/mokdong-visiting-tutoring.md",
        "tutoring/private/earth-science-tutoring.md",
        "tutoring/private/toefl-tutoring.md",
        "tutoring/private/economics-tutoring.md",
        "tutoring/private/thinking-skills-tutoring.md",
        "tutoring/private/elementary-english-tutoring.md",
        "tutoring/private/social-culture-tutoring.md",
        "tutoring/private/elementary-tutoring-guide.md",
        "tutoring/private/high-tutoring-guide.md",
        "tutoring/private/essay-tutoring.md",
        "tutoring/private/japanese-tutoring.md",
        "tutoring/private/group-tutoring.md",
        "tutoring/private/visiting-home-tutoring.md",
        "tutoring/private/high-english-tutoring.md",
        "tutoring/private/music-tutoring.md",
        "tutoring/private/korea-student-tutoring.md",
        "tutoring/private/medical-student-tutoring.md",
        "tutoring/private/middle-english-tutoring.md",
        "tutoring/private/world-history-tutoring.md",
        "tutoring/private/one-on-one-intensive-tutoring.md",
        "tutoring/private/online-video-tutoring.md",

        # tutoring guide
        "tutoring/tutoring-guide-10.md",
        "tutoring/tutoring-guide-20.md",
        "tutoring/tutoring-guide-11.md",
        "tutoring/tutoring-guide-16.md",
        "tutoring/tutoring-guide-13.md",
        "tutoring/tutoring-guide-3.md",
        "tutoring/tutoring-guide-30.md",
        "tutoring/tutoring-guide-35.md",
        "tutoring/tutoring-guide-46.md",
        "tutoring/tutoring-guide-56.md",
    ]

    total_fixed = 0

    print("중복 description 수정 중...")

    for file_rel_path in duplicate_files:
        filepath = content_path / file_rel_path
        if filepath.exists():
            if fix_description_in_file(filepath):
                total_fixed += 1
                # 진행 상황 표시 (20개마다)
                if total_fixed % 20 == 0:
                    print(f"  진행: {total_fixed}개 파일 수정...")

    print(f"\n완료! 총 {total_fixed}개 파일의 description을 고유하게 변경했습니다.")
    print("이제 각 페이지는 고유한 description을 가지게 됩니다. (SEO 최적화)")

if __name__ == "__main__":
    main()
