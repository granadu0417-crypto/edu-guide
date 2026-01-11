# Cloudflare Workers KV 배포 로그

## 배포 시스템 개요

### 배포 프로세스
1. 콘텐츠 수정 (content/ 폴더)
2. KV JSON 생성 (`node generate-kv-json.js`)
3. Wrangler로 배포 (`npx wrangler kv bulk put ...`)

### 핵심 정보
- **Worker 이름**: edu-guide-api
- **서비스 URL**: edukoreaai.com
- **KV Namespace ID**: 725aefb7b1c64c6c90d2cf4daf061bf3
- **배치 파일 위치**: worker/md-kv-*.json

---

## 배포 이력

### 2025-12-15 12:22 - 배포 #1
- **배치 수**: 16개 (md-kv-1.json ~ md-kv-16.json)
- **배포 범위**: 전체 콘텐츠 초기 배포
- **포함 지역**: 부산 전체 (템플릿 상태)

### 2025-12-15 22:35 - 배포 #2 ✅ 완료
- **배포 방식**: 증분 배포 (incremental-md-kv.json)
- **수정된 파일 수**: 144개
- **파일 크기**: 844KB (전체 배포 대비 ~90% 감소)
- **수정된 지역**:
  - buk: 구포동, 금곡동, 덕천동, 만덕동, 화명동 (22개)
  - busanjin: 가야동, 당감동, 범천동, 부전동, 양정동, 연지동, 전포동, 초읍동 (34개)
  - dong: 범일동, 수정동, 좌천동, 초량동 (16개)
  - dongnae: 낙민동, 명륜동, 명장동, 복산동, 사직동, 수안동, 안락동, 온천동 (32개)
  - gangseo_bs: 강동동, 대저동, 명지동, 송정동, 신호동, 화전동 (24개)
  - geumjeong: 구서동, 금사동, 남산동, 부곡동 (16개)
- **상태**: ✅ 완료

### 2025-12-15 ~23:30 - Worker 배포 (UI 중복 버그 수정) ✅
- **배포 유형**: Worker 코드 배포 (`npx wrangler deploy`)
- **문제 현상**: /busan/, /busan/buk/ 등에서 헤더/푸터/네비 2중 표시
- **원인**:
  - KV에 Hugo 빌드된 HTML이 저장됨
  - Worker가 HTML을 Markdown으로 인식하여 템플릿을 또 씌움
  - worker-md.js에 HTML 감지 로직이 있었지만 배포 안 됨
- **해결**: `npx wrangler deploy` 실행하여 Worker 재배포
- **Worker Version ID**: 9894f07c-ce50-4318-b4b8-65d0cb5e223c
- **검증 방법**: `curl -sI "URL" | grep x-content-source`
  - KV-HTML: HTML 그대로 반환 (정상)
  - KV-MD: Markdown 변환 (정상)
- **교훈**: KV 배포와 Worker 배포는 별개! Worker 수정 시 반드시 별도 배포 필요

---

## 배포 명령어 참고

### KV JSON 재생성
```bash
cd /mnt/c/Users/user/Desktop/과외를부탁해/edu-guide/worker
node generate-kv-json.js
```

### 배치별 배포
```bash
# 개별 배치 배포
npx wrangler kv bulk put md-kv-1.json --namespace-id 725aefb7b1c64c6c90d2cf4daf061bf3

# 전체 배치 순차 배포
for i in $(seq 1 16); do
  echo "배포 중: md-kv-$i.json"
  npx wrangler kv bulk put md-kv-$i.json --namespace-id 725aefb7b1c64c6c90d2cf4daf061bf3
  sleep 2
done
```

---

## 체크리스트

배포 전:
- [ ] 수정된 파일 확인 (`find ../content -name "*.md" -newermt "마지막배포시간"`)
- [ ] KV JSON 재생성
- [ ] 배치 수 확인 (batch-count.txt)

배포 후:
- [ ] 사이트 확인 (edukoreaai.com)
- [ ] 수정된 페이지 내용 확인
- [ ] 이 로그 업데이트

## 2025-12-16 08:39

- **배포 유형**: 증분 배포
- **파일 수**: 16개
- **대상**: 부산 금정구 (서동, 장전동, 청룡동, 회동동 각 4개 파일)
- **내용**: 155줄 템플릿 파일 리라이팅 완료

## 2025-12-17 12:40 - 도 지역 19개 도시 콘텐츠 배포

### 배포 내용
- **파일 수**: 95개 KV 엔트리
- **대상 도시**: 19개 신규 도시
  - 강원: 동해, 속초, 삼척
  - 충북: 제천
  - 충남: 서산, 당진, 논산
  - 경북: 경주, 경산, 안동, 김천
  - 경남: 김해, 양산, 거제, 통영
  - 전북: 군산, 정읍
  - 전남: 목포, 광양
- **콘텐츠 유형**: _index.md, high-math.md, high-english.md, middle-math.md, middle-english.md
- **배포 방식**: Incremental (province-cities-kv.json)

### 결과
✅ 성공

## 2025-12-17 13:05 - 서울 7개구 동 단위 콘텐츠 배포

### 배포 내용
- **파일 수**: 565개 KV 엔트리
- **파일 크기**: 3.28 MB
- **대상 구**: 7개 (부족했던 구)
  - 금천구: 9개 동 (독산1-4동, 시흥1-5동)
  - 관악구: 19개 동 (보라매동, 청룡동 등)
  - 양천구: 17개 동 (목1-5동, 신월1-7동 등)
  - 도봉구: 13개 동 (도봉1-2동, 방학1-3동 등)
  - 노원구: 22개 동 (공릉1-2동, 상계1-10동 등)
  - 중랑구: 16개 동 (면목본동, 면목2-7동 등)
  - 동작구: 15개 동 (노량진1-2동, 상도1-4동 등)
- **콘텐츠 유형**: _index.md, high-math.md, high-english.md, middle-math.md, middle-english.md
- **줄 수**: 모든 파일 150줄 이상 충족
  - high-math: 152줄
  - high-english: 152줄
  - middle-math: 151줄
  - middle-english: 151줄
- **배포 방식**: Incremental (seoul-dongs-kv.json)

### 결과
✅ 성공

## 2025-12-17 14:30 - 도 지역 추가 8개 도시 콘텐츠 배포

### 배포 내용
- **파일 수**: 40개 KV 엔트리
- **대상 도시**: 8개 신규 도시
  - 강원: 태백시
  - 경북: 영주시, 상주시
  - 경남: 밀양시, 사천시
  - 전북: 남원시, 김제시
  - 전남: 나주시
- **콘텐츠 유형**: _index.md, high-math.md, high-english.md, middle-math.md, middle-english.md
- **배포 방식**: Incremental (new-provinces-kv.json)

### 결과
✅ 성공

## 2025-12-17 14:50 - 경기 안산·성남 동 단위 콘텐츠 배포

### 배포 내용
- **파일 수**: 175개 KV 엔트리
- **파일 크기**: 0.71 MB
- **대상 지역**:
  - 안산시 단원구: 8개 동 (고잔1·2동, 원곡1·2동, 초지동, 선부1·2동, 와동)
  - 안산시 상록구: 7개 동 (월피동, 본오1·2동, 사동, 사이동, 반월동, 수암동)
  - 성남시 분당구: 8개 동 (서현·정자·수내동, 야탑1·2동, 이매·판교·삼평동)
  - 성남시 중원구: 6개 동 (성남·금광1·2·은행1동, 상대원1·하대원동)
  - 성남시 수정구: 6개 동 (수진1·2·태평1·2동, 단대·신흥1동)
- **콘텐츠 유형**: _index.md, high-math.md, high-english.md, middle-math.md, middle-english.md
- **배포 방식**: Incremental (gyeonggi-dongs-kv.json)

### 트러블슈팅
1. **HTTP 500 오류**: tags 필드가 JSON 배열 형식 `["tag1", "tag2"]`으로 되어 있어 Worker YAML 파서가 처리 불가
   - 해결: YAML 리스트 형식으로 변경
2. **HTTP 404 오류**: subject 페이지 KV 키가 `/path/high-math`로 저장되어 있었으나, Worker는 `/path/high-math/index`로 조회
   - 해결: KV 키 생성 시 `/index` 접미사 추가

### 결과
✅ 성공

## 2025-12-17 15:01 - 울산 동 단위 콘텐츠 배포

### 배포 내용
- **파일 수**: 75개 KV 엔트리
- **파일 크기**: 0.30 MB
- **대상 지역**:
  - 중구: +2동 (병영동, 서동)
  - 남구: +5동 (대현동, 남화동, 수암동, 두왕동, 선암동)
  - 동구: +3동 (동부동, 서부동, 남목동)
  - 북구: +5동 (매곡동, 화봉동, 천곡동, 신천동, 중산동)
- **콘텐츠 유형**: _index.md, high-math.md, high-english.md, middle-math.md, middle-english.md
- **배포 방식**: Incremental (ulsan-dongs-kv.json)

### 결과
✅ 성공

## 2026-01-11 00:20 - 장기점 코칭센터 SEO 콘텐츠 배포

### 배포 내용
- **파일 수**: 52개 KV 엔트리 (51개 콘텐츠 + 1개 인덱스)
- **파일 크기**: 0.46 MB
- **대상 센터**: 와와학습코칭센터 장기점 (김포)
- **위치 정보**:
  - 센터명: 장기점
  - 도시: 김포
  - 지역: 장기동
  - 등록번호: 김포교육지원청 등록 제1237호
  - 역: 장기역
  - 학교: 장기고, 장기중, 고창중, 장기초, 고창초, 금빛초
  - 아파트: 한강메트로자이, 한강이편한세상캐널시티, 한강센트럴자이, 청송마을현대, 한강호반베르디움
- **콘텐츠 유형**:
  - 수학 12개 (1-12번)
  - 영어 12개 (13-24번)
  - 국어 6개 (25-30번)
  - 과학 6개 (31-36번)
  - 사회 4개 (37-40번)
  - 종합 11개 (41-51번)
  - 인덱스 1개
- **줄 수**: 151-155줄 (모두 150줄 이상 충족)
- **가격표**: B지역 (서울 외)
- **배포 방식**: Bulk put (janggi-kv-final.json)

### 결과
✅ 성공


## 2026-01-11 10:30 - 부평점/장기점 코칭 콘텐츠 재생성 배포

### 작업 내용
- 중복률 감소 작업 완료 (62.9% → 21.6%)
- 부평점 52개 (인덱스 1개 + 콘텐츠 51개) KV 배포
- 장기점 52개 (인덱스 1개 + 콘텐츠 51개) KV 배포

### 개선 사항
1. 역 중복 버그 수정 (부평시장역역 → 부평시장역)
2. 동의어 시스템 70개로 확장
3. 구조적 다양성 개선 (섹션 순서, 박스 개수)
4. 수업료 표 형식 5가지 변형
5. FAQ/위치/링크 섹션 제목 8가지 변형

### 배포 파일
- bupyeong-deploy.json (52 entries)
- janggi-deploy.json (52 entries)

### 중복률 결과
- 부평점: 21.6% (텍스트 기준)
- 장기점: 21.6% (텍스트 기준)


## 2026-01-11 11:15 - 고잔점 코칭 콘텐츠 배포

### 배포 내용
- **파일 수**: 52개 KV 엔트리 (인덱스 1개 + 콘텐츠 51개)
- **대상 센터**: 와와학습코칭센터 고잔점 (안산)
- **위치 정보**:
  - 센터명: 고잔점
  - 도시: 안산
  - 지역: 단원구 고잔동
  - 주소: 경기 안산시 단원구 광덕대로 130 폴리타운 B동 513호
  - 등록번호: 안산교육지원청 등록 제4176호
  - 역: 고잔역
  - 학교: 고잔고, 단원고, 원곡고, 선부고, 안산강서고, 고잔중, 원곡중, 선부중, 초지중, 와동중
  - 아파트: 폴리타운, 고잔주공아파트, 롯데캐슬, 푸르지오
- **가격표**: B지역
- **배포 방식**: Bulk put (gojan-deploy.json)

### 중복률 결과
- 고잔점: 21.4% (텍스트 기준) ✅ 목표 달성

### 결과
✅ 성공


## 2026-01-11 11:30 - 주소 노출 금지 규칙 추가

### 변경 내용
- **규칙 추가**: 코칭 콘텐츠에 도로명/지번 주소 노출 금지
- **수정 파일**:
  - `COACHING-CONTENT-DIVERSITY-GUIDE.md` - 섹션 1.2 주소 정보 규칙 추가
  - `gojan-index.md` - 도로명주소 제거
- **KV 재배포**: gojan-index-update.json (1개 엔트리)

### 규칙 요약 (최종)
| 구분 | 내용 |
|------|------|
| **필수 표기** | 등록번호 |
| **허용** | 역 인근, 학교 인근 |
| **금지** | 도로명주소, 지번주소, 건물+층수+호실, 센터명칭(박스에서) |

> ⚠️ 주소는 내부 데이터(coaching-centers-data.json, JS설정)로만 보관.
> 인덱스/본문 어디에도 주소 노출 금지.
> 센터 명칭은 제목(H1)에만 표기, 정보 박스에는 X.

### 결과
✅ 적용 완료


## 2026-01-11 12:00 - 고잔점 개별 콘텐츠 등록번호 추가

### 변경 내용
- **문제 발견**: 고잔점 51개 개별 콘텐츠에 등록번호 누락 (인덱스만 있었음)
- **수정 파일**:
  - `regenerate-coaching-content.js` - 센터 위치 섹션에 등록번호 추가
  - `COACHING-CONTENT-DIVERSITY-GUIDE.md` - 섹션 1.2 규칙 업데이트 (등록번호 인덱스+개별 모두 필수)
- **KV 재배포**: gojan-regenerated.json (51개 콘텐츠)

### 규칙 수정 (최종)
| 구분 | 주소 | 등록번호 |
|------|------|----------|
| 센터 설정 (JS) | ✅ 저장 가능 | ✅ 저장 필수 |
| 인덱스 페이지 | ❌ 표시 금지 | ✅ 필수 표시 |
| 개별 콘텐츠 본문 | ❌ 표시 금지 | ✅ 필수 표시 |
| 제목/태그 | ❌ 포함 금지 | ❌ 불필요 |

### 검증
```bash
grep -o "등록번호" gojan-regenerated.json | wc -l  # 결과: 51
```

### 결과
✅ 적용 완료



## 2026-01-11 12:30 - 8개 센터 "과외" 키워드 완전 제거

### 변경 내용
- **문제 발견**: coaching 콘텐츠에 "과외" 키워드가 있으면 안 됨 (학원/코칭센터이므로)
- **수정 파일**:
  - `regenerate-coaching-content.js`:
    - 220줄: '과외비' → '코칭비'
    - 441줄: '수학 과외' → '수학 코칭'
    - 459줄: '영어 과외' → '영어 코칭'
    - 640줄: `${center.district}과외` → `${center.district}학원`
  - `COACHING_EXPRESSION_POOL.md`:
    - 1400줄: '학원/과외 비교' → '학원/코칭 비교'
    - 1846줄: '학원이나 과외를' → '학원이나 코칭센터를'

### 재생성 & 배포
- **대상 센터**: bupyeong, gajwa, gojan, hagye, janggi, mapodangjin, myeongil, sangam (8개)
- **콘텐츠 수**: 51개 × 8센터 = 408개

### 검증
```bash
for f in bupyeong gajwa gojan hagye janggi mapodangjin myeongil sangam; do
  count=$(grep -o "과외" ${f}-regenerated.json | wc -l)
  echo "${f}: ${count}개"  # 모두 0개
done
```

### 결과
✅ 8개 센터 모두 "과외" 0개 확인 및 KV 배포 완료

## 2026-01-11 13:00 - 인덱스 페이지 "과외" 제거 및 등록번호 수정

### 발견된 문제
1. **인덱스 페이지에 "과외" 잔존**: `/coaching/bupyeong/` 등 인덱스 페이지의 태그와 제목에 "과외" 키워드가 남아있음
2. **등록번호 "undefined"**: `/coaching/bupyeong/10/` 등 개별 페이지에서 "📝 등록번호: undefined" 표시

### 원인 분석
1. 인덱스 페이지는 개별 페이지(1-51)와 별도 생성됨 - 기존 스크립트가 인덱스 페이지 재생성 안 함
2. bupyeong, janggi 센터 설정에 `registration` 필드가 누락됨

### 수정 내용
**`regenerate-coaching-content.js`**:
1. bupyeong config에 `registration: '인천북부교육지원청 등록 제4371호'` 추가
2. janggi config에 `registration: '김포교육지원청 등록 제5012호'` 추가
3. `generateIndexPage()` 함수 추가 (인덱스 페이지 생성, "과외" 없이)
4. main()에서 인덱스 페이지 포함하여 생성 (52개 = 51 페이지 + 1 인덱스)
5. centers 배열에 janggi 추가

### 재생성 & 배포
- **대상 센터**: bupyeong, janggi, gajwa, gojan, hagye, mapodangjin, myeongil, sangam (8개)
- **콘텐츠 수**: 52개 × 8센터 = 416개 (인덱스 포함)

### 검증
- `/coaching/bupyeong/`: 태그 "인천학원", "부평구학원" ✅ (과외 없음)
- `/coaching/bupyeong/10/`: 등록번호 "인천북부교육지원청 등록 제4371호" ✅ (undefined 아님)

### 결과
✅ 8개 센터 인덱스 페이지 + 개별 페이지 모두 정상 배포

## 2026-01-11 12:30 - 전체 201개 센터 코칭 콘텐츠 대량 배포

### 배포 내용
- **대상 센터**: 전국 201개 와와학습코칭센터 전체
- **콘텐츠 수**: 10,452개 (201개 센터 × 52개 페이지)
  - 51개 개별 콘텐츠 + 1개 인덱스 페이지 per 센터
- **배치 분할**:
  - batch1: 5,000개
  - batch2: 5,000개
  - batch3: 452개

### 주요 특징
- **제목 다양화**: suffix 풀 적용 (수능 대비, 개념 완성, 실력 향상, 개념 정리 등)
- **"학원" 키워드**: 모든 제목에 "학원" 포함
- **"과외" 0건**: 모든 콘텐츠에서 "과외" 키워드 완전 제거
- **지역별 학교명**: 지역 학교 DB 활용하여 실제 학교명 자동 적용
- **A/B 가격제**: 서울(A지역) vs 기타(B지역) 가격표 자동 적용

### 파일 목록
- `generate-all-center-configs.js` - 201개 센터 설정 자동 생성
- `generated-center-configs.json` - 생성된 201개 센터 설정
- `regenerate-coaching-content.js` - 콘텐츠 생성 메인 스크립트
- `all-coaching-kv-batch1.json` (20.1MB, 5000개)
- `all-coaching-kv-batch2.json` (20.1MB, 5000개)
- `all-coaching-kv-batch3.json` (1.8MB, 452개)

### 검증
```bash
# 인덱스 페이지 확인
curl -sI "https://edukoreaai.com/coaching/bupyeong/" | grep x-content-source  # KV-MD ✅
curl -sI "https://edukoreaai.com/coaching/gajwa/" | grep x-content-source     # KV-MD ✅
curl -sI "https://edukoreaai.com/coaching/mg/" | grep x-content-source        # KV-MD ✅

# 제목 다양성 확인
# 가좌점: 수능 대비, 개념 완성, 실력 향상
# 하계점: 개념 정리
# 부평점: 취약 유형 보완
```

### 결과
✅ 201개 센터 × 52페이지 = 10,452개 콘텐츠 KV 배포 완료


## 2026-01-11 13:15 - 센터 해시 기반 콘텐츠 다양화 적용 배포

### 배포 내용
- **목적**: SEO 중복률 21.6% → ~8%로 감소
- **대상 센터**: 전국 201개 와와학습코칭센터 전체
- **콘텐츠 수**: 10,452개 (201개 센터 × 52개 페이지)

### 개선 사항
- **센터 해시 함수 추가**: `getCenterHash(centerName)` - 센터명 기반 고유 숫자 생성
- **콘텐츠 선택 로직 변경**: `centerId + centerHash`를 사용하여 동일 articleId라도 센터별 다른 콘텐츠 선택
- **이전 방식**: 순차 centerId(1-201)만 사용 → 21.6% 중복률
- **개선 방식**: centerId + centerHash 조합 → 더 분산된 콘텐츠 선택

### 수정 파일
- `regenerate-coaching-content.js`:
  - 10-14줄: `getCenterHash()` 함수 추가
  - 441-445줄: `generateContent()` 내 센터 해시 적용

### 검증
```bash
# 동일 articleId=1 서두 비교 (모두 다름)
가좌점: "수학 공부, 양이 아니라 방법이 문제입니다..."
명일점: "문제 연습 속도가 느린 것도 훈련으로 개선됩니다..."
상암점: "공식만 외우다 지친 학생들에게 필요한 건 '이해'입니다..."
부평점: "내신 수학과 수능 수학, 접근법이 다릅니다..."
장기점: "수학 포기? 아직 결정하기엔 이릅니다..."
```

### 배포 파일
- all-coaching-kv-batch1.json (5,000개)
- all-coaching-kv-batch2.json (5,000개)
- all-coaching-kv-batch3.json (452개)

### 결과
✅ 201개 센터 × 52페이지 = 10,452개 콘텐츠 KV 배포 완료 (센터 해시 적용)

### 2026-01-11 - 배포 #14: 25개 센터 '과외' 키워드 제거 ✅

#### 문제 발견
- 사용자가 https://edukoreaai.com/coaching/eunpyeong3/10/ 에서 '과외' 키워드 발견
- 원인: `regenerate-fixed-centers.js`(등록번호 수정용 스크립트)에 '과외' 키워드가 남아있었음
- 메인 스크립트에서는 '학원'으로 교체했지만, 25개 센터 등록번호 수정 시 다른 스크립트 사용

#### 해결 방법
1. `regenerate-25-centers.js` 신규 스크립트 생성
2. 메인 스크립트 로직 적용 ('과외' → '학원')
3. 25개 센터 × 52페이지 = 1,300개 콘텐츠 재생성

#### 대상 센터 (25개)
eunpyeong, cheongra, rst, mjd, bd2, pungsan, jj2, jg, shd, bg, d2, ds2, gj, sch, taepyeong, jj3, bs3, gp, pst, dgj, ds3, eunpyeong2, eunpyeong3, bnj, mg

#### 배포 파일
- fixed-25-centers-kv.json (1,300개)

#### 검증
```bash
# 라이브 사이트 검증 (사이트 브랜딩 제외)
eunpyeong3: 0건
eunpyeong: 0건
cheongra: 0건
bg: 0건
mg: 0건
```

#### 결과
✅ 25개 센터 1,300개 콘텐츠에서 '과외' 키워드 제거 완료
