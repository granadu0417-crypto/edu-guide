# Cloudflare Workers + KV 마이그레이션 계획

> **작성일**: 2025-12-12
> **목적**: Cloudflare Pages 20,000 파일 제한 해결을 위한 Workers + KV 아키텍처 전환

---

## 1. 배경 및 문제점

### 현재 상황
- **플랫폼**: Cloudflare Pages + Hugo (정적 사이트)
- **현재 파일 수**: 10,931개
- **목표 파일 수**: ~22,704개
- **제한**: Cloudflare Pages는 **20,000개 파일** 제한

### 발생 에러
```
16:59:52.311 ✘ [ERROR] Error: Pages only supports up to 20,000 files in a deployment.
Ensure you have specified your build output directory correctly.
```

### 콘텐츠 목표 (포기 불가)
| 항목 | 내용 |
|------|------|
| 수도권 | 서울/경기/인천 - **모든 법정동** 커버 |
| 지방 광역시 | 부산/대구/대전/광주/울산/세종 - **인기 동** 선별 |
| 과목 | 수학, 영어, 국어, 사회, 과학, 논술 = **6개** |
| 학년 | 중등, 고등 = **2개 (분리)** |
| 동당 파일 | 6과목 × 2학년 = **12개** |

### 예상 파일 수 계산
| 지역 | 법정동 수 | × 12파일 | 파일 수 |
|------|----------|----------|---------|
| 서울 | 467 | × 12 | 5,604 |
| 경기 | ~1,000 | × 12 | ~12,000 |
| 인천 | ~200 | × 12 | ~2,400 |
| 지방 (인기동) | ~225 | × 12 | ~2,700 |
| **총합** | **~1,892** | | **~22,704** |

→ **20,000 제한 초과** → Workers + KV로 해결

---

## 2. 해결 방안: Cloudflare Workers + KV

### 왜 Workers + KV인가?

| 비교 항목 | Cloudflare Pages | Workers + KV |
|-----------|------------------|--------------|
| 파일 제한 | 20,000 ❌ | **없음** ✅ |
| SEO | 좋음 | **좋음** (SSR) |
| 보안 | Cloudflare 기본 | **Cloudflare 풀스택** |
| 속도 | 빠름 | 빠름 (Edge) |
| 비용 | 무료 | 무료 (충분) |
| 확장성 | 제한적 | **무제한** |

### 장점 상세

**SEO 관점:**
- Workers가 완전한 HTML 반환 → 구글 크롤링 정상
- URL 구조 기존과 동일 유지 가능
- Edge 네트워크로 전세계 빠른 응답 → Core Web Vitals 향상
- 페이지별 동적 메타태그 생성 가능

**보안 관점:**
- DDoS 방어 (Cloudflare 기본)
- WAF (웹 애플리케이션 방화벽)
- Bot 관리
- SSL/TLS 자동
- Rate Limiting

**확장성 관점:**
- KV 저장소: 무제한 (1GB 무료)
- Workers 요청: 10만 요청/일 (무료)
- 페이지 수: **제한 없음**

---

## 3. 아키텍처 설계

### 현재 구조 (Hugo + Pages)
```
edu-guide/
├── content/
│   ├── seoul/
│   │   ├── gangnam-daechi-high-math.md
│   │   ├── gangnam-daechi-high-english.md
│   │   └── ... (수천 개 파일)
│   ├── gyeonggi/
│   └── ...
├── layouts/
├── static/
└── config.toml
```
→ 빌드 시 모든 .md → .html 변환 → 20,000개 초과 시 에러

### 새 구조 (Workers + KV)
```
edu-guide-workers/
├── src/
│   ├── index.js          # Worker 메인 로직
│   ├── router.js         # URL 라우팅
│   ├── renderer.js       # HTML 렌더링
│   └── templates/        # HTML 템플릿
│       ├── base.html
│       ├── tutoring.html
│       └── list.html
├── data/
│   ├── regions.json      # 지역 데이터 (서울/경기/인천...)
│   ├── schools.json      # 학교 데이터
│   ├── subjects.json     # 과목 데이터
│   └── prices.json       # 가격 데이터
├── scripts/
│   └── upload-to-kv.js   # KV 업로드 스크립트
├── wrangler.toml         # Cloudflare 설정
└── package.json
```

### 데이터 흐름
```
사용자 요청: GET /서울/강남구/대치동/고등-수학과외/

┌─────────────────────────────────────────────────────────┐
│                    Cloudflare Edge                       │
├─────────────────────────────────────────────────────────┤
│  1. Worker 수신                                          │
│     ↓                                                    │
│  2. URL 파싱                                             │
│     - 지역: 서울 > 강남구 > 대치동                         │
│     - 학년: 고등                                          │
│     - 과목: 수학                                          │
│     ↓                                                    │
│  3. KV에서 데이터 조회                                    │
│     - 지역 정보: KV.get("region:서울:강남구:대치동")        │
│     - 학교 정보: KV.get("schools:대치동")                  │
│     - 가격 정보: KV.get("prices:고등:수학")                │
│     ↓                                                    │
│  4. 템플릿 + 데이터 조합 → HTML 생성                       │
│     ↓                                                    │
│  5. 응답 반환 (완전한 HTML)                               │
└─────────────────────────────────────────────────────────┘

→ 구글봇이 보는 것: 일반 정적 페이지와 동일!
```

---

## 4. 데이터 구조 설계

### KV 키 구조

```javascript
// 지역 데이터
"region:서울" → { name: "서울특별시", districts: ["강남구", "강동구", ...] }
"region:서울:강남구" → { name: "강남구", dongs: ["대치동", "삼성동", ...] }
"region:서울:강남구:대치동" → {
  name: "대치동",
  type: "법정동",
  description: "대치동은 강남구의 대표적인 학원가..."
}

// 학교 데이터
"schools:서울:강남구:대치동" → {
  high: ["휘문고", "단대부고", "중동고", "숙명여고"],
  middle: ["대치중", "휘문중", "단대부중"]
}

// 과목 데이터
"subject:math" → {
  name: "수학",
  description: "...",
  curriculum: { middle: [...], high: [...] }
}

// 가격 데이터 (고정값)
"prices" → {
  elementary: { once: "12만원 - 22만원", twice: "25만원 - 38만원" },
  middle: { once: "22만원 - 32만원", twice: "29만원 - 47만원" },
  high12: { once: "25만원 - 36만원", twice: "33만원 - 53만원" },
  high3: { once: "28만원 - 40만원", twice: "37만원 - 59만원" }
}

// 템플릿 데이터
"template:tutoring" → "<!DOCTYPE html>..."
"template:list" → "<!DOCTYPE html>..."
```

### 콘텐츠 표현 풀 (기존 EXPRESSION_POOL.md 활용)

```javascript
// 서두 문단 풀
"expressions:intro" → [
  "고등학교 수학, 중학교 때와 완전히 다르네요.",
  "수학 성적이 갑자기 떨어졌나요?",
  "고등학교에 올라온 후 수학이 어려워졌다는 말, 정말 많이 듣습니다.",
  // ... 30개
]

// 마무리 풀
"expressions:outro" → [...]

// 아이보리 박스 풀
"expressions:ivory_box_1" → [...]
```

---

## 5. URL 구조 설계

### 라우팅 패턴

```javascript
// 지역 목록
GET /                           → 메인 페이지
GET /서울/                      → 서울 구 목록
GET /서울/강남구/               → 강남구 동 목록

// 과외 상세 페이지
GET /서울/강남구/대치동/고등-수학과외/    → 과외 상세
GET /서울/강남구/대치동/중등-영어과외/    → 과외 상세

// SEO용 대체 URL (선택)
GET /고등-수학과외/서울/강남구/대치동/    → 과외 상세 (리다이렉트 또는 동일 처리)
```

### URL 파싱 로직

```javascript
// src/router.js
function parseUrl(pathname) {
  // /서울/강남구/대치동/고등-수학과외/
  const parts = pathname.split('/').filter(Boolean);

  if (parts.length === 4) {
    const [city, district, dong, typeSubject] = parts;
    const [level, subject] = typeSubject.split('-');

    return {
      type: 'tutoring-detail',
      city,      // 서울
      district,  // 강남구
      dong,      // 대치동
      level,     // 고등
      subject    // 수학과외
    };
  }

  // ... 다른 패턴 처리
}
```

---

## 6. 템플릿 시스템

### 기본 HTML 템플릿

```html
<!-- templates/tutoring.html -->
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{title}}</title>
  <meta name="description" content="{{description}}">
  <meta property="og:title" content="{{title}}">
  <meta property="og:description" content="{{description}}">
  <link rel="canonical" href="{{canonical_url}}">
  <!-- 스타일 -->
</head>
<body>
  <header>{{header}}</header>

  <main>
    <h1>{{h1_title}}</h1>

    <section class="intro">
      {{intro_paragraph}}
    </section>

    <div class="ivory-box">
      <strong>이렇게 수업합니다!</strong><br>
      {{ivory_box_content}}
    </div>

    <!-- 학교 정보 -->
    <section class="schools">
      <h2>{{district}} {{dong}} 주요 학교</h2>
      {{schools_content}}
    </section>

    <!-- 가격 정보 -->
    <section class="pricing">
      <h2>수업료 안내</h2>
      {{pricing_content}}
    </section>

    <!-- CTA -->
    <div class="cta">
      {{cta_content}}
    </div>

    <!-- FAQ -->
    <section class="faq">
      {{faq_content}}
    </section>
  </main>

  <footer>{{footer}}</footer>
</body>
</html>
```

### 템플릿 렌더링

```javascript
// src/renderer.js
function render(template, data) {
  let html = template;

  for (const [key, value] of Object.entries(data)) {
    html = html.replace(new RegExp(`{{${key}}}`, 'g'), value);
  }

  return html;
}
```

---

## 7. 구현 단계

### Phase 1: 기본 구조 (1-2일)
- [ ] Wrangler 프로젝트 초기화
- [ ] 기본 Worker 설정
- [ ] KV 네임스페이스 생성
- [ ] 라우팅 로직 구현

### Phase 2: 데이터 마이그레이션 (2-3일)
- [ ] 기존 콘텐츠에서 데이터 추출
- [ ] JSON 데이터 파일 생성
- [ ] KV 업로드 스크립트 작성
- [ ] 데이터 업로드 및 검증

### Phase 3: 템플릿 시스템 (2-3일)
- [ ] HTML 템플릿 작성
- [ ] 렌더링 로직 구현
- [ ] 기존 스타일 적용
- [ ] 반응형 디자인 확인

### Phase 4: SEO 최적화 (1-2일)
- [ ] 메타 태그 동적 생성
- [ ] sitemap.xml 생성 로직
- [ ] robots.txt 설정
- [ ] 구조화 데이터 (JSON-LD) 추가

### Phase 5: 테스트 및 배포 (1-2일)
- [ ] 로컬 테스트 (wrangler dev)
- [ ] 스테이징 배포
- [ ] 성능 테스트
- [ ] 프로덕션 배포

---

## 8. 중요 참고사항

### 기존 CLAUDE.md 규칙 유지

Workers + KV로 전환해도 콘텐츠 규칙은 동일하게 적용:

1. **가격 정보 고정** (절대 변경 금지)
   - 초등: 주1회 12만원 - 22만원 / 주2회 25만원 - 38만원
   - 중등: 주1회 22만원 - 32만원 / 주2회 29만원 - 47만원
   - 고1-2: 주1회 25만원 - 36만원 / 주2회 33만원 - 53만원
   - 고3: 주1회 28만원 - 40만원 / 주2회 37만원 - 59만원

2. **학교명 정확성** - 지역별 학교 데이터 정확히 유지

3. **표현 다양화** - EXPRESSION_POOL.md 활용하여 중복 방지

4. **물결표(~) 사용 금지** - 하이픈(-) 사용

5. **환불 관련 내용 금지**

### 기존 Git 브랜치
- 현재 브랜치: `claude/review-duplicate-reduction-018onSC9irwoWUxh5bgXzzws`
- 기존 커밋 히스토리 참조 가능

---

## 9. 로컬 개발 시작 명령어

```bash
# 1. Wrangler CLI 설치
npm install -g wrangler

# 2. Cloudflare 로그인
wrangler login

# 3. 프로젝트 생성
mkdir edu-guide-workers
cd edu-guide-workers
wrangler init

# 4. KV 네임스페이스 생성
wrangler kv:namespace create "EDU_GUIDE_DATA"
wrangler kv:namespace create "EDU_GUIDE_DATA" --preview

# 5. 로컬 개발 서버
wrangler dev
```

---

## 10. 예상 무료 플랜 사용량

| 항목 | 무료 한도 | 예상 사용량 |
|------|----------|------------|
| Workers 요청 | 100,000/일 | ~10,000/일 |
| KV 읽기 | 100,000/일 | ~50,000/일 |
| KV 쓰기 | 1,000/일 | ~100/일 (업데이트 시) |
| KV 저장소 | 1GB | ~100MB |

→ **무료 플랜으로 충분히 운영 가능**

---

## 11. 연락처 및 참고 자료

- Cloudflare Workers 문서: https://developers.cloudflare.com/workers/
- KV 문서: https://developers.cloudflare.com/workers/runtime-apis/kv/
- Wrangler CLI: https://developers.cloudflare.com/workers/wrangler/

---

**이 문서를 로컬 Claude Code에 전달하여 작업을 이어가세요!**
