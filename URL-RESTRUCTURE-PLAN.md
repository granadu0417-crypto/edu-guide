# URL 구조 개편 계획서

> **작성일**: 2025-12-10
> **상태**: 계획 단계 (개발 전)
> **목표**: SEO 최적화를 위한 지역 중심 URL 구조로 전환

---

## 1. 프로젝트 개요

### 1-1. 배경
- 현재 콘텐츠 3,343개, 계속 증가 예정
- `/middle/`, `/high/` 폴더에 각각 960개 글 집중 (관리 어려움)
- 검색 패턴 "강남구 수학과외"와 URL 구조 불일치
- 미래 확장 (과목 추가, 화상과외 등) 고려 필요

### 1-2. 목표
- 검색 패턴과 URL 일치 ("강남구 수학과외" → `/seoul/gangnam/...`)
- 클릭 깊이 개선 (현재 4-5 → 목표 3 이내)
- 지역 SEO 강화 (네이버, 구글)
- 미래 확장성 확보

### 1-3. 우선순위
1. 네이버 SEO
2. 구글 SEO
3. 사용자 경험(UX)

---

## 2. 현재 상태 분석

### 2-1. 폴더별 콘텐츠 현황
| 폴더 | 글 수 | 설명 |
|------|-------|------|
| high | 960개 | 고등 과외 (지역+동+과목) |
| middle | 960개 | 중등 과외 (지역+동+과목) |
| tutoring | 629개 | 학습플랜, 과외 가이드 |
| subjects | 369개 | 과목별 학습법 |
| local | 210개 | 지역 정보 |
| exam | 71개 | 시험 대비 |
| consultation | 70개 | 상담 관련 |
| elementary | 47개 | 초등 과외 |
| cities | 26개 | 구별 허브 페이지 |
| **총계** | **3,343개** | |

### 2-2. 현재 URL 구조
```
/middle/jungnang-muk2-middle-english/     # 중랑구 묵2동 중등 영어
/middle/gangnam-daechi1-middle-math/      # 강남구 대치1동 중등 수학
/high/jungnang-muk2-high-english/         # 중랑구 묵2동 고등 영어
/high/gangnam-daechi1-high-math/          # 강남구 대치1동 고등 수학
```

### 2-3. 현재 메뉴 구조 (config.toml)
```
학습 가이드 ─┬─ 초등학생 → /elementary/
             ├─ 중학생 → /middle/
             └─ 고등학생 → /high/

과목별 ─┬─ 국어 → /subjects/korean/
        ├─ 영어 → /subjects/english/
        ├─ 수학 → /subjects/math/
        ├─ 과학 → /subjects/science/
        └─ 사회 → /subjects/social/

학습플랜 → /tutoring/
시험 대비 → /exam/
지역정보 → /cities/
무료 상담 → /consultation/
```

### 2-4. 현재 파일명 패턴 분석
```
/middle/ 폴더:
  {구영문}-{동영문}-middle-{과목}.md
  예: gangnam-daechi1-middle-math.md
      jungnang-muk2-middle-english.md

/high/ 폴더:
  {구영문}-{동영문}-high-{과목}.md
  예: gangnam-daechi1-high-math.md
      jungnang-muk2-high-english.md
```

---

## 3. 목표 구조

### 3-1. 결정 사항
- **단위**: 구(區) 단위로 묶음 (동 단위 X)
- **URL 언어**: 영문 (구글 SEO 고려)
- **계층**: 시/도 → 구 → 학년-과목

### 3-2. 새 폴더 구조
```
content/
├── seoul/                          # 서울시
│   ├── _index.md                   # 서울 허브 페이지
│   ├── gangnam/                    # 강남구
│   │   ├── _index.md               # 강남구 허브 (모든 글 목록)
│   │   ├── middle-math.md          # 강남구 중등 수학과외
│   │   ├── middle-english.md       # 강남구 중등 영어과외
│   │   ├── high-math.md            # 강남구 고등 수학과외
│   │   ├── high-english.md         # 강남구 고등 영어과외
│   │   └── (미래: video-math.md, elementary-math.md 등)
│   ├── seocho/                     # 서초구
│   │   ├── _index.md
│   │   ├── middle-math.md
│   │   └── ...
│   ├── jungnang/                   # 중랑구
│   │   ├── _index.md
│   │   ├── middle-math.md
│   │   └── ...
│   └── ... (25개 구)
├── gyeonggi/                       # 경기도
│   ├── _index.md
│   ├── bundang/                    # 분당
│   ├── ilsan/                      # 일산
│   └── ...
├── subjects/                       # 과목별 (지역 무관) - 유지
├── tutoring/                       # 학습플랜 - 유지
├── exam/                           # 시험 대비 - 유지
├── consultation/                   # 상담 - 유지
├── elementary/                     # 초등 (지역 무관) - 유지 또는 통합 검토
└── learning-plan/                  # 학습플랜 - 유지
```

### 3-3. 새 URL 구조
```
# 변경 전 → 변경 후

/middle/gangnam-daechi1-middle-math/     → /seoul/gangnam/middle-math/
/middle/gangnam-daechi2-middle-math/     → /seoul/gangnam/middle-math/ (통합)
/middle/gangnam-daechi3-middle-math/     → /seoul/gangnam/middle-math/ (통합)
/high/gangnam-daechi1-high-math/         → /seoul/gangnam/high-math/
/middle/jungnang-muk2-middle-english/    → /seoul/jungnang/middle-english/
/high/jungnang-muk2-high-english/        → /seoul/jungnang/high-english/

# 기존 유지
/subjects/...                            → /subjects/... (유지)
/tutoring/...                            → /tutoring/... (유지)
/exam/...                                → /exam/... (유지)
```

### 3-4. 새 메뉴 구조
```
지역별 과외 ─┬─ 서울 ─┬─ 강남구
             │        ├─ 서초구
             │        ├─ 송파구
             │        ├─ ... (25개 구)
             │        └─ 전체보기
             ├─ 경기 ─┬─ 분당
             │        ├─ 일산
             │        └─ ...
             └─ 기타 지역

학습 가이드 ─┬─ 초등학생 (과목별 학습법)
             ├─ 중학생 (과목별 학습법)
             └─ 고등학생 (과목별 학습법)

과목별 (유지)
학습플랜 (유지)
시험 대비 (유지)
무료 상담 (유지)
```

---

## 4. 콘텐츠 통합 전략

### 4-1. 동 단위 → 구 단위 통합

현재 강남구에는 동별로 별도 파일이 존재:
```
gangnam-daechi1-middle-math.md
gangnam-daechi2-middle-math.md
gangnam-daechi3-middle-math.md
gangnam-daechi4-middle-math.md
gangnam-yeoksam1-middle-math.md
gangnam-yeoksam2-middle-math.md
... (약 20+ 파일)
```

통합 후:
```
/seoul/gangnam/middle-math.md  (1개 파일)
```

### 4-2. 통합 콘텐츠 작성 방식

**옵션 A**: 대표 파일 선정 후 나머지는 리다이렉트
- 가장 잘 작성된 파일 1개 선택
- 나머지 URL은 301 리다이렉트

**옵션 B**: 새 콘텐츠 작성 (권장)
- 구 전체를 아우르는 새 콘텐츠 작성
- 동별 특징을 섹션으로 포함
- 기존 URL 모두 301 리다이렉트

### 4-3. 예상 통합 결과

| 구분 | 통합 전 | 통합 후 | 비고 |
|------|---------|---------|------|
| /middle/ | 960개 | 0개 | 지역별로 분산 |
| /high/ | 960개 | 0개 | 지역별로 분산 |
| /seoul/gangnam/ | 0개 | ~10개 | 과목별 통합 |
| /seoul/jungnang/ | 0개 | ~10개 | 과목별 통합 |
| ... | ... | ... | ... |

---

## 5. 서울시 구 목록 및 영문명

| 한글 | 영문 (URL) | 현재 콘텐츠 유무 |
|------|------------|-----------------|
| 강남구 | gangnam | O |
| 강동구 | gangdong | O |
| 강북구 | gangbuk | O |
| 강서구 | gangseo | O |
| 관악구 | gwanak | O |
| 광진구 | gwangjin | O |
| 구로구 | guro | O |
| 금천구 | geumcheon | O |
| 노원구 | nowon | O |
| 도봉구 | dobong | O |
| 동대문구 | dongdaemun | O |
| 동작구 | dongjak | O |
| 마포구 | mapo | O |
| 서대문구 | seodaemun | O |
| 서초구 | seocho | O |
| 성동구 | seongdong | O |
| 성북구 | seongbuk | O |
| 송파구 | songpa | O |
| 양천구 | yangcheon | O |
| 영등포구 | yeongdeungpo | O |
| 용산구 | yongsan | O |
| 은평구 | eunpyeong | O |
| 종로구 | jongno | O |
| 중구 | jung | O |
| 중랑구 | jungnang | O |

---

## 6. 리다이렉트 전략

### 6-1. Hugo aliases 사용
```yaml
# /seoul/gangnam/middle-math.md 파일 내
---
title: "강남구 중등 수학과외"
aliases:
  - /middle/gangnam-daechi1-middle-math/
  - /middle/gangnam-daechi2-middle-math/
  - /middle/gangnam-daechi3-middle-math/
  - /middle/gangnam-yeoksam1-middle-math/
  - /middle/gangnam-yeoksam2-middle-math/
  # ... 모든 기존 URL
---
```

### 6-2. 리다이렉트 매핑 규칙
```
기존 URL 패턴: /middle/{구}-{동}-middle-{과목}/
새 URL: /seoul/{구}/middle-{과목}/

기존 URL 패턴: /high/{구}-{동}-high-{과목}/
새 URL: /seoul/{구}/high-{과목}/
```

---

## 7. 마이그레이션 단계

### Phase 1: 준비 (현재 세션)
- [x] 현재 상태 분석
- [x] 목표 구조 설계
- [x] 계획서 작성
- [ ] 구별 콘텐츠 현황 상세 분석

### Phase 2: 새 구조 생성
- [ ] /seoul/ 폴더 구조 생성
- [ ] 각 구별 _index.md (허브 페이지) 생성
- [ ] 통합 콘텐츠 작성 (구별 × 학년별 × 과목별)

### Phase 3: 리다이렉트 설정
- [ ] 기존 URL → 새 URL aliases 매핑
- [ ] 리다이렉트 테스트

### Phase 4: 메뉴 업데이트
- [ ] config.toml 메뉴 구조 변경
- [ ] 네비게이션 테스트

### Phase 5: 정리
- [ ] 기존 /middle/, /high/ 폴더 정리 (백업 후 삭제)
- [ ] sitemap 재생성 확인
- [ ] Search Console에서 색인 요청

---

## 8. 기술적 고려사항

### 8-1. Hugo 섹션 구조
- `/seoul/` 폴더에 `_index.md` 필수
- 각 구 폴더에도 `_index.md` 필수 (목록 페이지 역할)

### 8-2. 택소노미 활용
```toml
# config.toml
[taxonomies]
  category = "categories"
  tag = "tags"
  region = "regions"      # 지역 택소노미
  grade = "grades"        # 학년 택소노미
  subject = "subjects"    # 과목 택소노미
```

### 8-3. 프론트매터 구조
```yaml
---
title: "강남구 중등 수학과외 | 내신·선행 완벽 대비"
date: 2025-12-10
description: "강남구 중학생을 위한 1:1 맞춤 수학과외..."
featured_image: "/images/edu_0001_xxx.jpg"
aliases:
  - /middle/gangnam-daechi1-middle-math/
  - /middle/gangnam-daechi2-middle-math/
  # ...
regions:
  - 서울
  - 강남구
grades:
  - 중등
subjects:
  - 수학
categories:
  - 중등교육
  - 수학과외
tags:
  - 강남구수학과외
  - 중등수학
  - 강남과외
---
```

---

## 9. 예상 작업량

### 9-1. 새로 작성해야 할 콘텐츠
| 지역 | 구 수 | 과목 | 학년 | 총 파일 수 |
|------|-------|------|------|-----------|
| 서울 | 25개 | 2개(수학,영어) | 2개(중,고) | 100개 |
| 경기 | 10개 | 2개 | 2개 | 40개 |
| **총계** | | | | **~140개** |

### 9-2. 리다이렉트 설정
- /middle/ 960개 → 25개 구로 매핑
- /high/ 960개 → 25개 구로 매핑
- 총 1,920개 URL 리다이렉트

---

## 10. 다음 세션 체크리스트

다음 세션에서 이 문서를 먼저 읽고 아래 순서로 진행:

1. [ ] 이 문서(URL-RESTRUCTURE-PLAN.md) 읽기
2. [ ] 구별 현재 콘텐츠 수 상세 분석
3. [ ] 통합 콘텐츠 템플릿 작성
4. [ ] 테스트용 1개 구(예: 강남구) 먼저 마이그레이션
5. [ ] 테스트 결과 확인 후 전체 진행

---

## 11. 미결정 사항 (추후 논의)

- [ ] 경기도 구조 (분당, 일산 등 시/구 구분)
- [ ] elementary 콘텐츠 통합 여부
- [ ] local 폴더 콘텐츠 처리 방안
- [ ] 화상과외 등 새 카테고리 URL 규칙

---

## 12. 변경 이력

| 날짜 | 변경 내용 | 작성자 |
|------|----------|--------|
| 2025-12-10 | 최초 작성 | Claude |

---

## 13. 구별 상세 콘텐츠 현황 (2025-12-10 분석)

### 13-1. 지역 기반 콘텐츠 (마이그레이션 대상)

| 구(영문) | 중등수학 | 중등영어 | 고등수학 | 고등영어 | 총계 | 통합 후 |
|----------|----------|----------|----------|----------|------|---------|
| songpa | 27 | 27 | 27 | 27 | 108 | 4 |
| gangseo | 23 | 23 | 23 | 23 | 92 | 4 |
| gangnam | 22 | 22 | 22 | 22 | 88 | 4 |
| seongbuk | 22 | 22 | 22 | 22 | 88 | 4 |
| gwanak | 20 | 20 | 20 | 20 | 80 | 4 |
| gangdong | 19 | 19 | 19 | 19 | 76 | 4 |
| nowon | 19 | 19 | 19 | 19 | 76 | 4 |
| yangcheon | 18 | 18 | 18 | 18 | 72 | 4 |
| yeongdeungpo | 18 | 18 | 18 | 18 | 72 | 4 |
| jongno | 17 | 17 | 17 | 17 | 68 | 4 |
| seongdong | 17 | 17 | 17 | 17 | 68 | 4 |
| eunpyeong | 16 | 16 | 16 | 16 | 64 | 4 |
| guro | 16 | 16 | 16 | 16 | 64 | 4 |
| jungnang | 16 | 16 | 16 | 16 | 64 | 4 |
| mapo | 16 | 16 | 16 | 16 | 64 | 4 |
| yongsan | 16 | 16 | 16 | 16 | 64 | 4 |
| dongjak | 15 | 15 | 15 | 15 | 60 | 4 |
| gwangjin | 15 | 15 | 15 | 15 | 60 | 4 |
| junggu | 15 | 15 | 15 | 15 | 60 | 4 |
| dobong | 14 | 14 | 14 | 14 | 56 | 4 |
| dongdaemun | 14 | 14 | 14 | 14 | 56 | 4 |
| seodaemun | 14 | 14 | 14 | 14 | 56 | 4 |
| gangbuk | 13 | 13 | 13 | 13 | 52 | 4 |
| seocho | 13 | 13 | 13 | 13 | 52 | 4 |
| geumcheon | 10 | 10 | 10 | 10 | 40 | 4 |
| **총계** | **425** | **425** | **425** | **425** | **1,700** | **100** |

### 13-2. 일반 가이드 콘텐츠 (유지 또는 별도 처리)

/middle/, /high/ 폴더 내 지역 패턴이 아닌 파일: **218개**

```
예시:
- _index.md
- advanced-tutoring-guide.md
- basic-foundation-tutoring.md
- english-grammar-guide.md
- math-difficult-problems.md
- mid-b10-1.md, mid-b10-2.md ...
```

**처리 방안**:
- 학습 가이드 성격 → /subjects/ 또는 /tutoring/으로 이동
- 학년별 가이드 → /학년/ 허브 페이지 하위로 유지

### 13-3. 마이그레이션 요약

| 항목 | 변경 전 | 변경 후 |
|------|---------|---------|
| 지역 기반 콘텐츠 | 1,700개 (동 단위) | 100개 (구 단위) |
| 리다이렉트 설정 | - | 1,700개 URL |
| 새 허브 페이지 | - | 27개 (서울 1 + 구 25 + 경기 1) |
| 일반 가이드 | 218개 | 218개 (위치 검토) |

---

**이 문서는 URL 구조 개편이 완료될 때까지 업데이트됩니다.**
