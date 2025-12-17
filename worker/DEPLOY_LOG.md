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

