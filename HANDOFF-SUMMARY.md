# 로컬 Claude Code 핸드오프 요약

> **날짜**: 2025-12-12
> **목적**: 웹 Claude Code에서 로컬 Claude Code로 작업 인계

---

## 1. 프로젝트 현황

### 기본 정보
- **프로젝트**: edu-guide (교육/과외 SEO 콘텐츠 사이트)
- **기술 스택**: Hugo + Cloudflare Pages
- **현재 파일 수**: 10,931개 마크다운 파일
- **Git 브랜치**: `claude/review-duplicate-reduction-018onSC9irwoWUxh5bgXzzws`

### 폴더별 파일 현황
| 폴더 | 파일 수 |
|------|---------|
| seoul | 3,211 |
| gyeonggi | 3,216 |
| incheon | 971 |
| busan | 586 |
| daegu | 326 |
| daejeon | 276 |
| gwangju | 271 |
| ulsan | 216 |
| sejong | 66 |
| 기타 (high/middle/local 등) | ~1,792 |

---

## 2. 해결해야 할 핵심 문제

### Cloudflare Pages 20,000 파일 제한
```
16:59:52.311 ✘ [ERROR] Error: Pages only supports up to 20,000 files in a deployment.
```

### 목표 콘텐츠 규모
| 항목 | 수량 |
|------|------|
| 수도권 법정동 | ~1,667개 |
| 지방 인기동 | ~225개 |
| 과목 | 6개 (수학, 영어, 국어, 사회, 과학, 논술) |
| 학년 | 2개 (중등, 고등) |
| 동당 파일 | 12개 |
| **총 필요 파일** | **~22,704개** |

→ 20,000 제한 초과 → **Workers + KV로 해결**

---

## 3. 결정된 해결 방안

### Cloudflare Workers + KV 선택 이유

1. **파일 제한 없음** - 무제한 페이지 생성 가능
2. **SEO 문제 없음** - SSR로 완전한 HTML 반환
3. **보안 우수** - Cloudflare 풀스택 보안 유지
4. **비용** - 무료 플랜으로 충분
5. **확장성** - 향후 과목/지역 추가 자유로움

### 거부된 대안들
- ❌ Vercel 이전 - 사용자가 Cloudflare 유지 원함
- ❌ 서브도메인 분리 - SEO 분산 우려
- ❌ 콘텐츠 축소 - 사업 목표와 충돌

---

## 4. 핵심 제약사항 (반드시 준수)

### 콘텐츠 규칙 (CLAUDE.md 참조)

1. **가격 정보 고정** (절대 변경 금지)
   ```
   초등: 주1회 12만원 - 22만원 / 주2회 25만원 - 38만원
   중등: 주1회 22만원 - 32만원 / 주2회 29만원 - 47만원
   고1-2: 주1회 25만원 - 36만원 / 주2회 33만원 - 53만원
   고3: 주1회 28만원 - 40만원 / 주2회 37만원 - 59만원
   ```

2. **물결표(~) 사용 금지** → 하이픈(-) 사용
3. **환불 관련 내용 금지**
4. **표현 다양화** - EXPRESSION_POOL.md 활용
5. **학교명 정확성** - 지역별 학교 데이터 유지

---

## 5. 참조해야 할 문서들

| 문서 | 경로 | 내용 |
|------|------|------|
| 콘텐츠 가이드라인 | `/home/user/edu-guide/CLAUDE.md` | 콘텐츠 작성 규칙 전체 |
| 표현 풀 | `/home/user/edu-guide/EXPRESSION_POOL.md` | 다양한 표현 목록 |
| **마이그레이션 계획** | `/home/user/edu-guide/WORKERS-KV-MIGRATION.md` | Workers + KV 상세 설계 |

---

## 6. 다음 단계 (로컬에서 진행)

### 즉시 시작할 작업
1. `WORKERS-KV-MIGRATION.md` 문서 검토
2. Wrangler CLI 설치 및 Cloudflare 로그인
3. 새 Workers 프로젝트 초기화
4. KV 네임스페이스 생성

### 구현 순서
```
Phase 1: 기본 구조 (1-2일)
    ↓
Phase 2: 데이터 마이그레이션 (2-3일)
    ↓
Phase 3: 템플릿 시스템 (2-3일)
    ↓
Phase 4: SEO 최적화 (1-2일)
    ↓
Phase 5: 테스트 및 배포 (1-2일)
```

---

## 7. 대화 맥락 요약

### 사용자 요구사항
1. 전국 동 단위 과외 콘텐츠 SEO 사이트
2. 수도권(서울/경기/인천): 모든 법정동 커버
3. 지방 광역시: 인기 동만 선별
4. 6과목 × 2학년 = 동당 12개 페이지
5. 20,000 파일 제한 문제 해결
6. Cloudflare 생태계 유지 희망

### 기술적 결정
- Hugo + Pages → Workers + KV 전환
- 정적 생성 → 동적 SSR
- 마크다운 파일 → KV 데이터 + 템플릿

### 사용자 성향
- 기술적 세부사항보다 결과 중시
- SEO와 보안에 관심 높음
- Cloudflare 플랫폼 선호
- 비용 효율성 중요

---

## 8. 주의사항

### 하지 말아야 할 것
- ❌ 기존 콘텐츠 규칙 변경
- ❌ 가격 정보 수정
- ❌ 다른 호스팅으로 이전 제안
- ❌ 콘텐츠 축소 제안

### 해야 할 것
- ✅ Workers + KV 아키텍처 구현
- ✅ 기존 콘텐츠 데이터화
- ✅ SEO 최적화 유지
- ✅ 표현 다양화 시스템 구현

---

## 9. 연락처 및 리소스

- Cloudflare Workers 문서: https://developers.cloudflare.com/workers/
- KV 문서: https://developers.cloudflare.com/workers/runtime-apis/kv/
- Wrangler CLI: https://developers.cloudflare.com/workers/wrangler/

---

**이 문서와 WORKERS-KV-MIGRATION.md를 함께 참조하여 작업을 진행하세요!**
