# 전국 지역 URL 구조 통합 계획서

> **작성일**: 2025-12-10
> **목표**: 전국 지역별 콘텐츠 URL 구조 표준화 및 SEO 최적화

---

## 1. 현재 상태 분석

### 1-1. 지역별 콘텐츠 현황

| 지역 | 현재 위치 | 파일 수 | 구조 |
|------|-----------|---------|------|
| **서울** | `/seoul/{구}/` | 126개 | ✅ 완료 (25개 구) |
| **경기도** | `/local/gyeonggi/` | 70개 | 시 단위 flat 구조 |
| **부산** | `/local/busan-*.md` | 3개 | 단일 파일 |
| **대구** | `/local/daegu-*.md` | 3개 | 단일 파일 |
| **인천** | `/local/incheon-*.md` | 3개 | 단일 파일 |
| **광주** | `/local/gwangju-*.md` | 3개 | 단일 파일 |
| **대전** | `/local/daejeon-*.md` | 3개 | 단일 파일 |
| **울산** | `/local/ulsan-*.md` | 3개 | 단일 파일 |
| **세종** | `/local/sejong-*.md` | 3개 | 단일 파일 |
| **강원** | `/local/gangwon-*.md` | 2개 | 단일 파일 |
| **충북** | `/local/chungbuk-*.md` | 2개 | 단일 파일 |
| **충남** | `/local/chungnam-*.md` | 2개 | 단일 파일 |
| **전북** | `/local/jeonbuk-*.md` | 2개 | 단일 파일 |
| **전남** | `/local/jeonnam-*.md` | 2개 | 단일 파일 |
| **경북** | `/local/gyeongbuk-*.md` | 2개 | 단일 파일 |
| **경남** | `/local/gyeongnam-*.md` | 2개 | 단일 파일 |
| **제주** | `/local/jeju-*.md` | 2개 | 단일 파일 |

### 1-2. 경기도 기존 시/군 목록 (70개 파일)

| 시/군 | 파일 수 | 과목 |
|-------|---------|------|
| 성남 (분당) | 4개 | 수학, 영어, 과학 |
| 수원 | 4개 | 교육가이드, 수학, 영어, 과학 |
| 용인 | 4개 | 교육가이드, 수학, 영어, 과학 |
| 고양 (일산) | 4개 | 수학, 영어, 과학 |
| 부천 | 4개 | 교육가이드, 수학, 영어, 과학 |
| 안양 (평촌) | 4개 | 수학, 영어, 과학 |
| 안산 | 4개 | 교육가이드, 수학, 영어 |
| 화성 | 4개 | 교육가이드, 수학, 영어, 과학 |
| 남양주 | 3개 | 교육가이드, 수학, 영어 |
| 의정부 | 4개 | 교육가이드, 수학, 영어, 과학 |
| 파주 | 4개 | 교육가이드, 수학, 영어, 과학 |
| 김포 | 3개 | 교육가이드, 수학, 영어 |
| 광명 | 3개 | 교육가이드, 수학, 영어 |
| 시흥 | 3개 | 교육가이드, 수학, 영어 |
| 평택 | 4개 | 교육가이드, 수학, 영어, 과학 |
| 하남 | 1개 | 교육가이드 |
| 구리 | 1개 | 교육가이드 |
| 군포 | 1개 | 교육가이드 |
| 오산 | 1개 | 교육가이드 |
| 이천 | 1개 | 교육가이드 |
| 양주 | 1개 | 교육가이드 |
| 안성 | 1개 | 교육가이드 |
| 광주(경기) | 1개 | 교육가이드 |

---

## 2. 목표 URL 구조

### 2-1. 계층 구조 설계

```
/                           # 홈
├── seoul/                  # 서울특별시 ✅ 완료
│   ├── _index.md
│   └── {구}/
│       ├── _index.md
│       ├── middle-math.md
│       ├── middle-english.md
│       ├── high-math.md
│       └── high-english.md
│
├── gyeonggi/               # 경기도 (신규)
│   ├── _index.md           # 경기도 허브
│   └── {시}/
│       ├── _index.md
│       ├── middle-math.md
│       ├── middle-english.md
│       ├── high-math.md
│       └── high-english.md
│
├── busan/                  # 부산광역시 (신규)
│   ├── _index.md           # 부산 허브
│   └── {구}/               # 부산 16개 구군
│       ├── _index.md
│       └── ...
│
├── incheon/                # 인천광역시 (신규)
│   ├── _index.md
│   └── {구}/               # 인천 10개 구군
│
├── daegu/                  # 대구광역시 (신규)
├── daejeon/                # 대전광역시 (신규)
├── gwangju/                # 광주광역시 (신규)
├── ulsan/                  # 울산광역시 (신규)
├── sejong/                 # 세종특별자치시 (신규)
│
└── provinces/              # 도 단위 (신규)
    ├── gangwon/            # 강원특별자치도
    ├── chungbuk/           # 충청북도
    ├── chungnam/           # 충청남도
    ├── jeonbuk/            # 전북특별자치도
    ├── jeonnam/            # 전라남도
    ├── gyeongbuk/          # 경상북도
    ├── gyeongnam/          # 경상남도
    └── jeju/               # 제주특별자치도
```

### 2-2. URL 규칙

| 지역 유형 | URL 패턴 | 예시 |
|-----------|----------|------|
| 서울 | `/seoul/{구}/` | `/seoul/gangnam/high-math/` |
| 경기도 | `/gyeonggi/{시}/` | `/gyeonggi/seongnam/high-math/` |
| 광역시 | `/{도시}/` | `/busan/high-math/` |
| 도 | `/provinces/{도}/` | `/provinces/gangwon/` |

---

## 3. 경기도 마이그레이션 계획

### 3-1. 대상 시/군 (31개)

| 순위 | 시/군 | 영문 | 인구 | 우선순위 |
|------|-------|------|------|----------|
| 1 | 수원시 | suwon | 120만 | 높음 |
| 2 | 용인시 | yongin | 110만 | 높음 |
| 3 | 고양시 | goyang | 108만 | 높음 |
| 4 | 성남시 | seongnam | 93만 | 높음 |
| 5 | 부천시 | bucheon | 82만 | 높음 |
| 6 | 화성시 | hwaseong | 95만 | 높음 |
| 7 | 남양주시 | namyangju | 73만 | 높음 |
| 8 | 안산시 | ansan | 65만 | 중간 |
| 9 | 안양시 | anyang | 55만 | 중간 |
| 10 | 평택시 | pyeongtaek | 58만 | 중간 |
| 11 | 의정부시 | uijeongbu | 46만 | 중간 |
| 12 | 시흥시 | siheung | 52만 | 중간 |
| 13 | 파주시 | paju | 50만 | 중간 |
| 14 | 김포시 | gimpo | 50만 | 중간 |
| 15 | 광명시 | gwangmyeong | 28만 | 낮음 |
| 16 | 군포시 | gunpo | 27만 | 낮음 |
| 17 | 하남시 | hanam | 30만 | 낮음 |
| 18 | 오산시 | osan | 23만 | 낮음 |
| 19 | 양주시 | yangju | 24만 | 낮음 |
| 20 | 이천시 | icheon | 22만 | 낮음 |
| 21 | 구리시 | guri | 20만 | 낮음 |
| 22 | 안성시 | anseong | 19만 | 낮음 |
| 23 | 포천시 | pocheon | 14만 | 낮음 |
| 24 | 의왕시 | uiwang | 16만 | 낮음 |
| 25 | 여주시 | yeoju | 11만 | 낮음 |
| 26 | 동두천시 | dongducheon | 9만 | 낮음 |
| 27 | 과천시 | gwacheon | 7만 | 낮음 |
| 28 | 양평군 | yangpyeong | 12만 | 낮음 |
| 29 | 가평군 | gapyeong | 6만 | 낮음 |
| 30 | 연천군 | yeoncheon | 4만 | 낮음 |

### 3-2. 경기도 특수 지역 (별도 처리)

| 지역 | 소속 시 | 특징 |
|------|---------|------|
| **분당** | 성남시 | 교육특구, 별도 URL 유지 |
| **일산** | 고양시 | 교육특구, 별도 URL 유지 |
| **평촌** | 안양시 | 교육특구, 별도 URL 유지 |
| **수지** | 용인시 | 교육특구, 별도 URL 유지 |
| **동탄** | 화성시 | 신도시, 별도 URL 고려 |

### 3-3. 경기도 새 URL 구조

```
/gyeonggi/
├── _index.md               # 경기도 허브 (31개 시군 버튼)
├── seongnam/               # 성남시
│   ├── _index.md           # 성남시 허브
│   ├── middle-math.md      # 중등 수학
│   ├── middle-english.md   # 중등 영어
│   ├── high-math.md        # 고등 수학
│   └── high-english.md     # 고등 영어
├── bundang/                # 분당 (특수지역)
│   ├── _index.md
│   └── ... (동일 구조)
├── suwon/                  # 수원시
├── yongin/                 # 용인시
├── suji/                   # 수지 (특수지역)
├── goyang/                 # 고양시
├── ilsan/                  # 일산 (특수지역)
├── anyang/                 # 안양시
├── pyeongchon/             # 평촌 (특수지역)
└── ... (나머지 시군)
```

### 3-4. 리다이렉트 매핑 (경기도)

```yaml
# 기존 → 새 URL
/local/gyeonggi/seongnam-math-tutoring/ → /gyeonggi/seongnam/high-math/
/local/gyeonggi/bundang-english-tutoring/ → /gyeonggi/bundang/high-english/
/local/gyeonggi/suwon-education-guide/ → /gyeonggi/suwon/
/local/gyeonggi/ilsan-math-tutoring/ → /gyeonggi/ilsan/high-math/
```

---

## 4. 광역시 마이그레이션 계획

### 4-1. 광역시별 구/군 목록

| 광역시 | 구/군 수 | 주요 구 | 우선순위 |
|--------|----------|---------|----------|
| **부산** | 16개 | 해운대구, 수영구, 남구, 동래구, 연제구 | 높음 |
| **인천** | 10개 | 연수구, 남동구, 부평구, 서구 | 높음 |
| **대구** | 8개 | 수성구, 달서구, 동구, 북구 | 중간 |
| **대전** | 5개 | 서구, 유성구, 중구, 동구, 대덕구 | 중간 |
| **광주** | 5개 | 남구, 서구, 북구, 동구, 광산구 | 중간 |
| **울산** | 5개 | 남구, 중구, 동구, 북구, 울주군 | 낮음 |
| **세종** | 1개 | 세종시 전체 | 낮음 |

### 4-2. 광역시 URL 구조

```
/busan/                     # 부산광역시
├── _index.md               # 부산 허브
├── haeundae/               # 해운대구
│   ├── _index.md
│   ├── middle-math.md
│   ├── middle-english.md
│   ├── high-math.md
│   └── high-english.md
├── suyeong/                # 수영구
├── nam/                    # 남구
├── dongnae/                # 동래구
└── ... (16개 구군)

/incheon/                   # 인천광역시
├── _index.md
├── yeonsu/                 # 연수구
├── namdong/                # 남동구
├── bupyeong/               # 부평구
└── ... (10개 구군)
```

### 4-3. 리다이렉트 매핑 (광역시)

```yaml
# 기존 → 새 URL
/local/busan-math-tutoring/ → /busan/high-math/
/local/busan-english-tutoring/ → /busan/high-english/
/local/busan-education-guide/ → /busan/
/local/incheon-math-tutoring/ → /incheon/high-math/
```

---

## 5. 도 단위 계획

### 5-1. 도별 구조

| 도 | 영문 | 주요 시 | 콘텐츠 전략 |
|----|----- |---------|-------------|
| 강원 | gangwon | 춘천, 원주, 강릉 | 도 단위 허브만 |
| 충북 | chungbuk | 청주, 충주 | 청주 구 단위 확장 |
| 충남 | chungnam | 천안, 아산 | 천안/아산 분리 |
| 전북 | jeonbuk | 전주, 익산 | 전주 구 단위 확장 |
| 전남 | jeonnam | 순천, 여수 | 도 단위 허브만 |
| 경북 | gyeongbuk | 포항, 구미 | 도 단위 허브만 |
| 경남 | gyeongnam | 창원, 진주 | 창원 구 단위 확장 |
| 제주 | jeju | 제주시, 서귀포 | 도 단위 허브만 |

### 5-2. 도 단위 URL 구조

```
/provinces/
├── _index.md               # 도 전체 허브
├── gangwon/
│   ├── _index.md           # 강원도 허브
│   ├── chuncheon/          # 춘천시 (확장 시)
│   └── wonju/              # 원주시 (확장 시)
├── chungbuk/
│   ├── _index.md           # 충북 허브
│   └── cheongju/           # 청주시
├── chungnam/
│   ├── _index.md           # 충남 허브
│   ├── cheonan/            # 천안시
│   └── asan/               # 아산시
└── ... (나머지 도)
```

---

## 6. 마이그레이션 우선순위

### Phase 1: 경기도 (최우선)
- **기간**: 1단계
- **범위**: 경기도 주요 15개 시 (인구 30만 이상)
- **파일 수**: 약 80개 (15시 × 5파일 + 특수지역)
- **리다이렉트**: 70개 기존 URL

### Phase 2: 부산/인천 (높음)
- **기간**: 2단계
- **범위**: 부산 16개 구, 인천 10개 구
- **파일 수**: 약 130개 (26구 × 5파일)
- **리다이렉트**: 6개 기존 URL

### Phase 3: 기타 광역시 (중간)
- **기간**: 3단계
- **범위**: 대구, 대전, 광주, 울산, 세종
- **파일 수**: 약 120개 (24구 × 5파일)
- **리다이렉트**: 15개 기존 URL

### Phase 4: 도 단위 (낮음)
- **기간**: 4단계
- **범위**: 8개 도
- **파일 수**: 약 50개 (허브 + 주요 시)
- **리다이렉트**: 16개 기존 URL

---

## 7. cities 페이지 업데이트

### 7-1. 버튼 URL 변경

```html
<!-- 현재 (변경 전) -->
<a href="/cities/강남구/">강남구</a>
<a href="/local/gyeonggi/seongnam-math-tutoring/">성남시</a>

<!-- 변경 후 -->
<a href="/seoul/gangnam/">강남구</a>
<a href="/gyeonggi/seongnam/">성남시</a>
```

### 7-2. 새 버튼 구조

```markdown
## 서울특별시
[강남구](/seoul/gangnam/) [서초구](/seoul/seocho/) ...

## 경기도
[성남시](/gyeonggi/seongnam/) [분당](/gyeonggi/bundang/) ...

## 부산광역시
[해운대구](/busan/haeundae/) [수영구](/busan/suyeong/) ...
```

---

## 8. 예상 작업량

| 단계 | 지역 | 신규 파일 | 리다이렉트 | 예상 시간 |
|------|------|-----------|------------|-----------|
| Phase 1 | 경기도 | ~80개 | ~70개 | 2시간 |
| Phase 2 | 부산/인천 | ~130개 | ~6개 | 3시간 |
| Phase 3 | 기타 광역시 | ~120개 | ~15개 | 3시간 |
| Phase 4 | 도 단위 | ~50개 | ~16개 | 1시간 |
| **합계** | **전체** | **~380개** | **~107개** | **9시간** |

---

## 9. 체크리스트

### 마이그레이션 전
- [ ] 기존 URL 전체 목록 백업
- [ ] 이미지 파일 확인
- [ ] 학교 정보 데이터 수집

### 마이그레이션 중
- [ ] 각 지역별 _index.md 생성
- [ ] 콘텐츠 파일 생성 (middle/high × math/english)
- [ ] aliases로 리다이렉트 설정
- [ ] 이미지 경로 확인

### 마이그레이션 후
- [ ] 빌드 테스트 (hugo server)
- [ ] 리다이렉트 동작 확인
- [ ] cities 페이지 버튼 URL 업데이트
- [ ] sitemap 확인
- [ ] Search Console 색인 요청

---

## 10. 다음 단계

1. **즉시**: Phase 1 (경기도) 진행
2. **검증**: 빌드 및 배포 테스트
3. **순차**: Phase 2~4 진행

---

**문서 버전**: 1.0
**최종 수정**: 2025-12-10
