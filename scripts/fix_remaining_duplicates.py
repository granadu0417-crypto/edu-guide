#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
남은 중복 제목 수정 스크립트
파일명 기반으로 고유한 제목 생성
"""

from pathlib import Path
import re

# 파일명 → 고유 제목 매핑
TITLE_MAP = {
    # Middle school files
    'middle/descriptive-assessment-strategy.md': '서술형 평가 전략 | 고득점 비법',
    'middle/english-grammar-guide.md': '중등 영어 문법 완벽 가이드 | 체계적 학습',
    'middle/english-listening-skills.md': '영어 듣기 실력 향상법 | 청해 마스터',
    'middle/history-study-methods.md': '역사 공부법 가이드 | 암기와 이해',
    'middle/internal-grade-management.md': '중등 내신 관리 전략 | 학년별 대비법',
    'middle/math-difficult-problems.md': '중등 수학 고난도 문제 풀이 | 심화 학습',
    'middle/math-geometry-functions.md': '도형과 함수 완벽 정복 | 중등 핵심 단원',
    'middle/memory-note-taking.md': '효과적인 암기법과 노트필기 | 학습 효율화',
    'middle/mid-b10-1.md': '중2 학습 전략 가이드 | 사춘기 극복 공부법',
    'middle/mid-b11-1.md': '중3 입시 준비 완벽 가이드 | 고교 진학 로드맵',
    'middle/mid-b12-1.md': '중등 학습 심화 전략 | 자기주도학습',
    'middle/mid-b13-1.md': '중등 성적 향상 비법 | 과목별 전략',
    'middle/mid-b14-1.md': '중학생 공부습관 완성 | 효율적 학습',
    'middle/mid-b15-1.md': '중등 진로 탐색 가이드 | 미래 설계',
    'middle/mid-b9-1.md': '중1 학교 적응 전략 | 중학 생활 시작',
    'middle/middle-batch7-1.md': '중등 종합 학습 전략 | 전 과목 완성',
    'middle/middle-batch8-1.md': '중학교 성공 로드맵 | 내신부터 진로까지',
    'middle/middle-final-1.md': '중등 교육 완벽 마스터 | 학업 성취',
    'middle/reading-comprehension-advanced.md': '중등 심화 독해 전략 | 비문학 정복',
    'middle/science-lab-notebook.md': '과학 실험 노트 작성법 | 탐구 활동 가이드',
    'middle/self-directed-learning-complete-guide.md': '자기주도학습 완벽 가이드 | 스스로 공부하기',
    'middle/time-management-planning.md': '중학생 시간 관리법 | 효율적 계획 수립',

    # High school -1 batch files
    'high/high-b10-1.md': '고1 학습 시작 전략 | 고교 적응',
    'high/high-b11-1.md': '고1 내신 관리법 | 첫 시험 대비',
    'high/high-b12-1.md': '고1 학습 습관 형성 | 효율적 공부',
    'high/high-b13-1.md': '고1 과목별 전략 | 균형 학습',
    'high/high-b14-1.md': '고1 비교과 시작 | 생기부 관리',
    'high/high-b15-1.md': '고1 진로 탐색 | 학과 선택',
    'high/high-b9-1.md': '고1 연간 계획 | 학습 로드맵',
    'high/high-batch7-1.md': '고1 종합 전략 | 성공적 시작',
    'high/high-batch8-1.md': '고1 완벽 가이드 | 고교 생활',
    'high/high-final-1.md': '고1 마스터 가이드 | 학습부터 생활까지',
    'high/high-final-12.md': '모의고사 완벽 활용 | 수능 실전 대비',

    # High school -2, -3, batch, final files
    'high/admissions-strategy.md': '대학 입시 전략 가이드 | 전형별 대비법',
    'high/career-major-guide.md': '진로와 학과 선택 가이드 | 미래 설계',
    'high/english-strategy.md': '고등 영어 학습 전략 | 수능 완벽 대비',
    'high/korean-reading-strategy.md': '고등 국어 독해 전략 | 비문학 정복',
    'high/math-strategy.md': '고등 수학 학습 전략 | 수능 수학 완성',
    'high/mental-management.md': '입시 멘탈 관리 가이드 | 스트레스 극복',
    'high/mock-exam-strategy.md': '모의고사 활용 전략 | 실전 감각 유지',
    'high/online-lecture-guide.md': '온라인 강의 활용법 | 효과적 학습',
    'high/parent-support-guide.md': '학부모 지원 가이드 | 입시 도움',
    'high/school-record-management.md': '학생부 관리 전략 | 생기부 완성',
    'high/high-b10-2.md': '고2 진로 확정 전략 | 학과 선택',
    'high/high-b11-2.md': '고2 학습 집중 전략 | 내신과 수능',
    'high/high-b12-2.md': '고2 심화 학습 가이드 | 실력 완성',
    'high/high-b13-2.md': '고2 비교과 활동 | 생기부 관리',
    'high/high-b14-2.md': '고2 모의고사 대비 | 수능 준비',
    'high/high-b15-2.md': '고2 입시 준비 시작 | 전략 수립',
    'high/high-b9-2.md': '고2 학습 계획 수립 | 연간 로드맵',
    'high/high-batch7-2.md': '고2 종합 학습 전략 | 균형 관리',
    'high/high-batch8-2.md': '고2 성공 가이드 | 입시 기반',
    'high/high-final-2.md': '고2 완벽 마스터 | 진로부터 학습까지',
    'high/high-b10-3.md': '고3 수능 D-300 전략 | 최종 스퍼트',
    'high/high-b11-3.md': '고3 입시 최종 점검 | 목표 대학',
    'high/high-b12-3.md': '고3 수능 마무리 | 실전 대비',
    'high/high-b13-3.md': '고3 면접 준비 | 자신감 있는 답변',
    'high/high-b14-3.md': '고3 논술 전략 | 논리적 글쓰기',
    'high/high-b9-3.md': '고3 연간 계획 | D-365 로드맵',
    'high/high-batch7-3.md': '고3 종합 입시 전략 | 수시와 정시',
    'high/high-batch8-3.md': '고3 합격 전략 | 최종 준비',
    'high/high-final-3.md': '고3 입시 완벽 가이드 | 대입 성공',

    # Middle school -2, -3, batch, final files
    'middle/mid-b10-2.md': '중2 공부 집중 전략 | 학습 의욕',
    'middle/mid-b11-2.md': '중2 내신 안정화 | 성적 유지',
    'middle/mid-b12-2.md': '중2 진로 탐색 시작 | 적성 발견',
    'middle/mid-b13-2.md': '중2 학습 효율화 | 시간 관리',
    'middle/mid-b14-2.md': '중2 과목별 학습법 | 균형 잡힌 공부',
    'middle/mid-b15-2.md': '중2 자기주도 학습 | 독립적 공부',
    'middle/mid-b9-2.md': '중2 학습 계획 | 연간 로드맵',
    'middle/middle-batch7-2.md': '중2 종합 학습 전략 | 전 과목',
    'middle/middle-batch8-2.md': '중2 성공 가이드 | 사춘기 극복',
    'middle/middle-final-2.md': '중2 완벽 마스터 | 학습과 성장',
    'middle/mid-b10-3.md': '중3 고교 선택 전략 | 진학 준비',
    'middle/mid-b11-3.md': '중3 최종 내신 관리 | 생기부 마무리',
    'middle/mid-b12-3.md': '중3 고등 예습 시작 | 선행 학습',
    'middle/mid-b13-3.md': '중3 진로 확정 | 고교 유형 선택',
    'middle/mid-b14-3.md': '중3 입시 준비 완성 | 고교 합격',
    'middle/mid-b15-3.md': '중3 종합 정리 | 중등 마무리',
    'middle/mid-b9-3.md': '중3 연간 계획 | 입시 로드맵',
    'middle/middle-batch7-3.md': '중3 종합 전략 | 고교 진학',
    'middle/middle-batch8-3.md': '중3 합격 가이드 | 특목고 준비',
    'middle/middle-final-3.md': '중3 입시 완벽 대비 | 고교 선택',
    'middle/middle-final-9.md': '중등 내신 최종 정리 | 종합 전략',

    # Elementary school files
    'elementary/dictation-preparation.md': '받아쓰기 완벽 대비 | 맞춤법 정복',
    'elementary/elem-b10-1.md': '초등 4학년 공부 가이드 | 사고력 키우기',
    'elementary/elem-b10-2.md': '초4 학습 습관 형성 | 자기주도 학습',
    'elementary/elem-b10-3.md': '초등 4학년 과목별 전략 | 핵심 학습법',
    'elementary/elem-b10-4.md': '초4 사고력 수학 | 문제 해결 능력',
    'elementary/elem-b11-1.md': '초등 5학년 학습법 | 심화 학습 시작',
    'elementary/elem-b11-2.md': '초5 공부 습관 완성 | 중등 준비',
    'elementary/elem-b11-3.md': '초등 5학년 과목 전략 | 응용력 향상',
    'elementary/elem-b11-4.md': '초5 심화 학습 가이드 | 창의적 사고',
    'elementary/elem-b12-1.md': '초등 6학년 중등 준비 | 입학 대비',
    'elementary/elem-b12-2.md': '초6 학습 마무리 | 중학교 예습',
    'elementary/elem-b12-3.md': '초등 6학년 총정리 | 기초 완성',
    'elementary/elem-b12-4.md': '초6 중등 과목 미리보기 | 선행 학습',
    'elementary/elem-b13-1.md': '초등 종합 학습 전략 | 전 학년 가이드',
    'elementary/elem-b14-1.md': '초등생 공부 습관 | 평생 학습 기초',
    'elementary/elem-b15-1.md': '초등 교육 완벽 가이드 | 학부모 필독',
    'elementary/elem-b9-1.md': '초등 1학년 입학 준비 | 학교 적응',
    'elementary/elem-b9-2.md': '초1 학교생활 가이드 | 친구 사귀기',
    'elementary/elem-b9-3.md': '초등 1학년 공부법 | 기초 학습',
    'elementary/elem-b9-4.md': '초1 학습 습관 시작 | 즐거운 공부',
    'elementary/elementary-batch7-1.md': '초등 저학년 학습 전략 | 1-3학년',
    'elementary/elementary-math-study-guide.md': '초등 수학 학습 가이드 | 연산부터 응용까지',
    'elementary/english-phonics-guide.md': '파닉스 완벽 가이드 | 영어 읽기 기초',
    'elementary/english-vocabulary-memorization.md': '초등 영어 단어 암기법 | 효과적 학습',
    'elementary/exam-study-planning.md': '초등 시험 공부 계획 | 효율적 준비',
    'elementary/math-calculation-skills.md': '연산 능력 향상 | 빠르고 정확한 계산',
    'elementary/reading-comprehension-guide.md': '독해력 향상 가이드 | 글 이해 능력',
    'elementary/reading-habit-formation.md': '독서 습관 형성법 | 평생 독서가 되기',
    'elementary/self-directed-learning-habits.md': '자기주도 학습 습관 | 스스로 공부하기',
    'elementary/study-habits-formation.md': '올바른 학습 습관 형성 | 초등 시기 핵심',
    'elementary/upper-grade-study-methods.md': '초등 고학년 공부법 | 4-6학년 전략',
    'elementary/word-problems-solving.md': '수학 문장제 풀이법 | 문제 이해력',
    'elementary/elem-b13-2.md': '초등 2학년 기초 학습 | 읽기 쓰기 완성',
    'elementary/elem-b14-2.md': '초2 학습 습관 정착 | 규칙적 공부',
    'elementary/elementary-batch7-2.md': '초2 종합 학습 가이드 | 기초 다지기',
    'elementary/elementary-batch8-2.md': '초등 2학년 완벽 가이드 | 즐거운 학습',
    'elementary/elem-b13-3.md': '초등 3학년 사고력 향상 | 논리적 사고',
    'elementary/elem-b14-3.md': '초3 학습 습관 완성 | 자기주도',
    'elementary/elementary-batch7-3.md': '초3 종합 학습 전략 | 습관 형성',
    'elementary/elementary-batch8-3.md': '초등 3학년 마스터 | 학습 독립',
    'elementary/elem-b13-4.md': '초등 4학년 심화 학습 | 응용력',
    'elementary/elem-b14-4.md': '초4 창의적 사고 | 문제 해결',
    'elementary/elementary-batch7-4.md': '초4 종합 가이드 | 사고력 완성',
    'elementary/elementary-batch8-4.md': '초등 4학년 완벽 학습 | 실력 향상',

    # Exam files
    'exam/exam-mastery-final.md': '시험 완벽 마스터 | 전략부터 실전까지',
    'exam/exam-preparation-1.md': '시험 2주 전 준비 | 효율적 마무리',

    # Tutoring files
    'tutoring/private-tutor-selection-guide.md': '과외 선생님 선택 가이드 | 우리 아이 맞는 선생님 찾기',
}

def fix_file_title(file_path):
    """파일의 제목을 고유하게 수정"""
    rel_path = str(file_path.relative_to(Path('content')))

    # 매핑에 있는 파일인지 확인
    if rel_path not in TITLE_MAP:
        return False, "매핑 없음"

    new_title = TITLE_MAP[rel_path]

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # title 교체
        new_content = re.sub(
            r'^title:\s*"([^"]*)"',
            f'title: "{new_title}"',
            content,
            count=1,
            flags=re.MULTILINE
        )

        if new_content == content:
            return False, "변경 없음"

        # 파일 저장
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        return True, new_title

    except Exception as e:
        return False, f"오류: {e}"

def main():
    print("🔍 남은 중복 제목 수정 시작...\n")

    content_dir = Path('content')

    stats = {
        'updated': 0,
        'skipped': 0,
        'errors': 0
    }

    for rel_path, new_title in TITLE_MAP.items():
        file_path = content_dir / rel_path

        if not file_path.exists():
            print(f"⏭️  {rel_path} - 파일 없음")
            stats['skipped'] += 1
            continue

        success, message = fix_file_title(file_path)

        if success:
            stats['updated'] += 1
            print(f"✅ {rel_path}")
            print(f"   → {message}")
        else:
            if "오류" in message:
                stats['errors'] += 1
                print(f"❌ {rel_path} - {message}")
            else:
                stats['skipped'] += 1

    print("\n" + "="*80)
    print("📊 제목 수정 완료 통계")
    print("="*80)
    print(f"수정 완료: {stats['updated']}")
    print(f"스킵: {stats['skipped']}")
    print(f"오류: {stats['errors']}")
    print("="*80)

if __name__ == '__main__':
    main()
