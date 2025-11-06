#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
빈 _index.md 파일 콘텐츠 채우기
"""

from pathlib import Path

# 각 섹션별 콘텐츠
INDEX_CONTENTS = {
    'middle/_index.md': '''---
title: "중학생 학습 가이드 | 내신부터 진로까지"
description: "중학생을 위한 완벽한 학습 가이드. 학년별 내신 관리법, 과목별 학습 전략, 진로 탐색부터 고등학교 준비까지 중등 교육의 모든 것을 안내합니다."
categories: ["중학생"]
tags: ["중등", "중학교", "내신", "학습법", "진로탐색"]
featured_image: "https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=1200&h=630&fit=crop"
---

# 중학생 학습 가이드

중학교 시기는 **내신 관리**와 **진로 탐색**이 동시에 이루어지는 중요한 시기입니다. 체계적인 학습 전략과 자기 이해가 고등학교 성공의 토대가 됩니다.

## 📚 학년별 가이드

### 중1 - 적응과 기초
- [중1 첫 시험 대비](/middle/mid-b9-1/) - 중학교 적응 전략
- [중학교 학습법](/middle/mid-b9-2/) - 새로운 공부 방식
- [중1 내신 관리](/middle/mid-b9-3/) - 첫 내신 시험

### 중2 - 심화와 탐색
- [중2 학습 전략](/middle/mid-b10-1/) - 사춘기 극복 공부법
- [중2 진로 탐색](/middle/mid-b10-2/) - 적성 발견하기
- [중2 내신 관리](/middle/mid-b10-3/) - 안정적 성적 유지

### 중3 - 입시 준비
- [중3 입시 준비](/middle/mid-b11-1/) - 고교 진학 로드맵
- [중3 내신 마무리](/middle/mid-b11-2/) - 학생부 관리
- [고등 예습 전략](/middle/mid-b11-3/) - 고교 선행 학습

## 📖 과목별 학습법

### 국어
- [국어 문법 가이드](/middle/english-grammar-guide/) - 문법 완벽 정리
- [독해 실력 향상](/middle/reading-comprehension-advanced/) - 심화 독해

### 수학
- [수학 어려운 문제](/middle/math-difficult-problems/) - 고난도 문제 풀이
- [도형과 함수](/middle/math-geometry-functions/) - 중등 핵심 단원

### 영어
- [영어 듣기 실력](/middle/english-listening-skills/) - 듣기 마스터
- [영어 문법](/middle/english-grammar-guide/) - 체계적 문법

### 사회/과학
- [역사 공부법](/middle/history-study-methods/) - 암기와 이해
- [실험 노트 작성](/middle/science-lab-notebook/) - 탐구 활동

## 🎯 학습 전략

- [내신 관리](/middle/internal-grade-management/) - 학년별 내신 전략
- [서술형 대비](/middle/descriptive-assessment-strategy/) - 높은 점수 받기
- [암기와 노트필기](/middle/memory-note-taking/) - 효율적 학습
- [자기주도학습](/middle/self-directed-learning-complete-guide/) - 스스로 공부하기
- [시간 관리](/middle/time-management-planning/) - 효율적 계획

## 💡 중등 학습의 핵심

### 1. 내신이 중심
고등학교 진학과 대입을 위해 내신 성적 관리가 가장 중요합니다.

### 2. 자기주도성
스스로 계획하고 실천하는 자기주도 학습 능력을 키워야 합니다.

### 3. 진로 탐색
다양한 경험을 통해 자신의 적성과 흥미를 발견하는 시기입니다.

### 4. 학생부 관리
생기부 관리를 통해 자신만의 스토리를 만들어가야 합니다.

---

**중등 시기의 중요성**

중학교 성적과 학습 습관이 고등학교 성공을 결정합니다. 지금부터 체계적으로 준비하세요!

더 자세한 정보는 위의 카테고리별 가이드를 참고하세요!
''',
    'high/_index.md': '''---
title: "고등학생 입시 가이드 | 수능부터 대입까지"
description: "고등학생을 위한 완벽한 입시 가이드. 학년별 학습 전략, 수능 준비, 내신 관리, 학생부 종합전형부터 정시까지 대입의 모든 것을 안내합니다."
categories: ["고등학생"]
tags: ["고등", "고등학교", "수능", "대입", "입시전략"]
featured_image: "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=1200&h=630&fit=crop"
---

# 고등학생 입시 가이드

고등학교 3년은 **대학 입시**를 준비하는 시기입니다. 내신, 수능, 비교과 활동을 균형있게 관리하며 목표 대학 합격을 향해 나아가야 합니다.

## 📚 학년별 전략

### 고1 - 기초 다지기
- [고1 내신 전략](/high/high-b9-1/) - 고등 첫 시험 대비
- [고1 학습 습관](/high/high-b9-2/) - 고등 공부법 정착
- [생기부 관리 시작](/high/high-b9-3/) - 학생부 첫 단추

### 고2 - 진로 확정
- [고2 학습 로드맵](/high/high-b10-1/) - 진로 확정과 준비
- [고2 학생부](/high/high-b10-2/) - 심화 활동 전략
- [모의고사 대비](/high/high-b10-3/) - 수능 감각 유지

### 고3 - 입시 최종 준비
- [수능 D-365](/high/high-b11-1/) - 입시 최종 전략
- [수시 vs 정시](/high/high-b11-2/) - 전형 선택
- [면접 준비](/high/high-b11-3/) - 대학별 면접 대비

## 📖 수능 과목별 전략

### 국어
- [수능 국어](/high/korean-reading-strategy/) - 화법작문문학독해
- [독해 전략](/high/korean-reading-strategy/) - 비문학 정복

### 수학
- [수능 수학](/high/math-strategy/) - 미적분과 확률통계
- [수학 실전](/high/math-strategy/) - 킬러 문항 대비

### 영어
- [수능 영어](/high/english-strategy/) - 절대평가 1등급
- [영어 독해](/high/english-strategy/) - 빠르고 정확한 독해

## 🎯 입시 전형별 가이드

### 수시
- [학생부종합](/high/admissions-strategy/) - 생기부 완성 전략
- [학생부교과](/high/school-record-management/) - 내신 관리법
- [논술](/high/admissions-strategy/) - 논리적 글쓰기

### 정시
- [수능 전략](/high/suneung-d100-strategy/) - D-100 집중 전략
- [모의고사 활용](/high/mock-exam-strategy/) - 실전 감각 유지

## 💡 입시 전략

- [입시 전략](/high/admissions-strategy/) - 전형별 대비법
- [진로와 학과](/high/career-major-guide/) - 학과 선택 가이드
- [2026 수능 변화](/high/2026-suneung-changes/) - 최신 입시 정보
- [온라인 강의](/high/online-lecture-guide/) - 효과적 활용법
- [멘탈 관리](/high/mental-management/) - 입시 스트레스 대처
- [학부모 지원](/high/parent-support-guide/) - 부모님 역할

## 💡 고등 학습의 핵심

### 1. 균형 잡힌 준비
내신, 수능, 비교과 활동을 모두 챙겨야 합니다.

### 2. 장기적 계획
3년 로드맵을 세우고 체계적으로 준비하세요.

### 3. 자기 관리
시간 관리, 멘탈 관리가 성공의 열쇠입니다.

### 4. 정보 수집
입시 정보를 꾸준히 업데이트하고 활용하세요.

---

**고등학교의 목표**

목표 대학 합격을 위해 지금부터 체계적으로 준비하세요. 노력은 배신하지 않습니다!

더 자세한 정보는 위의 카테고리별 가이드를 참고하세요!
''',
    'local/_index.md': '''---
title: "지역별 교육 정보 | 서울·경기 학습 가이드"
description: "지역별 맞춤 교육 정보. 서울 25개구, 경기도 주요 지역의 학원·과외·교육 프로그램 정보와 지역 특성에 맞는 학습 전략을 제공합니다."
categories: ["지역정보"]
tags: ["지역", "서울", "경기", "학원", "과외", "교육정보"]
featured_image: "https://images.unsplash.com/photo-1547981609-4b6bfe67ca0b?w=1200&h=630&fit=crop"
---

# 지역별 교육 정보

지역마다 교육 환경과 특성이 다릅니다. 우리 지역에 맞는 **최적의 교육 정보**를 찾아보세요.

## 🏙️ 서울 지역

### 강남권
- [강남구 교육](/local/seoul/gangnam-math-tutoring/) - 대치동 학원가
- [서초구 교육](/local/seoul/seocho-math-tutoring/) - 양재·반포 학원
- [송파구 교육](/local/seoul/songpa-math-tutoring/) - 잠실·가락 교육

### 강북권
- [강북구 교육](/local/seoul/gangbuk-math-tutoring/) - 수유·미아 학원
- [노원구 교육](/local/seoul/nowon-math-tutoring/) - 중계동 학원가
- [도봉구 교육](/local/seoul/dobong-math-tutoring/) - 방학·쌍문 교육

### 서부권
- [마포구 교육](/local/mapo-english-tutor/) - 신촌·홍대 학원
- [은평구 교육](/local/seoul/eunpyeong-math-tutoring/) - 응암·불광 교육
- [서대문구 교육](/local/seoul/seodaemun-math-tutoring/) - 신촌 교육

### 동부권
- [강동구 교육](/local/seoul/gangdong-math-tutoring/) - 천호·길동 학원
- [광진구 교육](/local/seoul/gwangjin-math-tutoring/) - 자양·구의 교육
- [성동구 교육](/local/seoul/seongdong-math-tutoring/) - 왕십리·금호 학원

## 🌳 경기 지역

### 주요 도시
- [경기도 교육 가이드](/local/gyeonggi/gyeonggi-education-guide/) - 경기 교육 개관
- 성남·분당 교육 (준비 중)
- 고양·일산 교육 (준비 중)
- 용인·수지 교육 (준비 중)

## 📚 지역 교육 프로그램

### 공공 교육
- [지역아동센터 가이드](/local/community-learning-center-guide/) - 무료 교육 프로그램
- [공공도서관 활용](/local/public-library-guide/) - 지역 도서관 이용
- [교육복지 지원](/local/education-welfare-support-guide/) - 교육 지원 제도
- [교육지원센터](/local/education-support-center-guide/) - 지역 교육청 프로그램

### 방과후 프로그램
- [방과후 학교](/local/after-school-program-guide/) - 학교 방과후 활용
- [온라인 교육](/local/online-education-platform-guide/) - 온라인 학습 플랫폼

### 사교육
- [학원 선택 가이드](/local/private-academy-selection-guide/) - 우리 아이 맞는 학원
- [특목고 준비](/local/special-purpose-high-school-guide/) - 지역별 특목고

## 💡 지역별 교육의 특징

### 강남권
- 높은 교육열과 우수한 교육 인프라
- 다양한 학원과 과외 선택지
- 경쟁적 학습 분위기

### 강북권
- 합리적인 교육비와 안정적 환경
- 지역 밀착형 교육 커뮤니티
- 균형 잡힌 교육 접근

### 경기권
- 신도시 중심의 현대적 교육 시설
- 서울 접근성과 쾌적한 환경
- 다양한 교육 프로그램

## 🎯 지역 선택 가이드

### 우리 아이에게 맞는 지역은?

**학원가 접근성 중요**
→ 강남·대치, 목동, 중계동 추천

**교육비 부담 줄이기**
→ 강북권, 경기 신도시 추천

**공공 교육 활용**
→ 교육지원센터 발달 지역 추천

---

**지역 교육 정보의 중요성**

우리 지역의 교육 자원을 잘 활용하면 더 효과적인 학습이 가능합니다!

더 자세한 정보는 위의 지역별 가이드를 참고하세요!
'''
}

def fill_index_pages():
    """빈 _index.md 파일들에 콘텐츠 채우기"""
    content_dir = Path('content')

    for rel_path, content in INDEX_CONTENTS.items():
        file_path = content_dir / rel_path

        if not file_path.exists():
            print(f"⏭️  {rel_path} - 파일 없음")
            continue

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            print(f"✅ {rel_path} - 콘텐츠 작성 완료")

        except Exception as e:
            print(f"❌ {rel_path} - 오류: {e}")

def main():
    print("🔍 빈 _index.md 파일 콘텐츠 작성 시작...\n")
    fill_index_pages()
    print("\n" + "="*80)
    print("✅ _index.md 파일 콘텐츠 작성 완료!")
    print("="*80)

if __name__ == '__main__':
    main()
