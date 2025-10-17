# 🔧 트러블슈팅 및 시행착오 기록

> **작성일**: 2025년 10월 17일  
> **프로젝트**: 과외를부탁해 (edu-guide)  
> **목적**: AI 및 개발자를 위한 실전 문제 해결 가이드

이 문서는 프로젝트를 진행하면서 겪었던 모든 시행착오와 해결 방법을 상세히 기록합니다. 향후 유사한 문제 발생 시 빠르게 해결하고, AI가 같은 실수를 반복하지 않도록 돕기 위해 작성되었습니다.

---

## 📋 목차

1. [이미지 관련 문제](#이미지-관련-문제)
2. [Hugo 빌드 문제](#hugo-빌드-문제)
3. [CSS 및 레이아웃 문제](#css-및-레이아웃-문제)
4. [Git 및 배포 문제](#git-및-배포-문제)
5. [성능 최적화 문제](#성능-최적화-문제)
6. [AI 협업 시 주의사항](#ai-협업-시-주의사항)

---

## 이미지 관련 문제

### ❌ 문제 1: 카테고리 목록에서 이미지 액박 (가장 빈번)

#### 증상
- **상세 페이지**: 이미지 정상 표시
- **카테고리 목록 페이지**: 이미지 깨짐 (액박)
- **홈페이지 최신 글**: 일부만 이미지 표시

#### 발견 과정
```
사용자: "우선 지역정보탭에 있는 글 하나를 내가 캡처한거거든? 캡처2 를 우선 봐봐 
        전국 특목고 ~ 이렇게 되있는글에 이미지 안보이지?"

AI: (스크린샷 분석) "이미지가 표시되지 않는 것을 확인했습니다"

사용자: "근데 캡처3을 봐봐 해당글을 들어가서보면 이미지가 보이거든?"

AI: "아! 문제를 이해했습니다. 목록 페이지에서만 안 보이는 거군요!"
```

#### 근본 원인 분석

**원인 1: featured_image 필드 누락**
```markdown
# ❌ 잘못된 예시 - featured_image 없음
---
title: "중학생을 위한 수학 어려운 문제 유형 분석"
date: 2025-10-16T14:00:00+09:00
categories: ["중학교", "수학"]
---
```

**원인 2: 동일한 이미지 URL 중복 사용**
```markdown
# ❌ 문제 상황 - 여러 글이 같은 이미지 사용
# special-purpose-high-school-guide.md
featured_image: "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=1200&h=630&fit=crop"

# admissions-strategy.md (같은 URL!)
featured_image: "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=1200&h=630&fit=crop"
```

#### 해결 방법

**Step 1: featured_image 확인**
```bash
# 모든 마크다운 파일에서 featured_image 검색
grep -r "featured_image" content/

# featured_image가 없는 파일 찾기
find content/ -name "*.md" -exec grep -L "featured_image" {} \;
```

**Step 2: 각 파일에 고유한 이미지 추가**
```markdown
# ✅ 올바른 예시 - 각 글마다 다른 이미지
---
title: "중학생을 위한 수학 어려운 문제 유형 분석"
date: 2025-10-16T14:00:00+09:00
categories: ["중학교", "수학"]
featured_image: "https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=1200&h=630&fit=crop"
---
```

**Step 3: 중복 이미지 URL 검사**
```bash
# 중복된 이미지 URL 찾기
grep -rh "featured_image" content/ | sort | uniq -d
```

#### 예방 방법
```markdown
# 새 글 작성 시 체크리스트
- [ ] featured_image 필드 포함
- [ ] 이미지 URL이 다른 글과 중복되지 않는지 확인
- [ ] 이미지 URL 브라우저에서 직접 테스트
- [ ] 로컬 서버에서 목록 페이지 미리보기
```

#### 실제 수정 사례

**사례 1: math-difficult-problems.md**
```diff
# Front Matter 수정
---
 title: "중학생을 위한 수학 어려운 문제 유형 분석"
 date: 2025-10-16T14:00:00+09:00
 categories: ["중학교", "수학"]
+featured_image: "https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=1200&h=630&fit=crop"
---
```

**사례 2: special-purpose-high-school-guide.md (중복 해결)**
```diff
# 다른 글과 중복된 이미지 URL 변경
---
 title: "전국 특목고 완벽 가이드"
-featured_image: "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=1200&h=630&fit=crop"
+featured_image: "https://images.unsplash.com/photo-1562774053-701939374585?w=1200&h=630&fit=crop"
---
```

**사례 3: 2026-suneung-changes.md**
```diff
---
 title: "2026학년도 수능 변경사항 총정리"
 description: "킬러문항 폐지, 과목 구조 개편 등 현 고2 학생들이 꼭 알아야 할 정보"
+featured_image: "https://images.unsplash.com/photo-1427504494785-3a9ca7044f45?w=1200&h=630&fit=crop"
---
```

---

### ❌ 문제 2: 커스텀 이미지 경로 오류

#### 증상
- 로컬에서는 이미지 표시됨
- 배포 후 이미지 404 에러

#### 원인
```html
<!-- ❌ 잘못된 경로 -->
<img src="static/images/logo.png">

<!-- ❌ 절대 경로 없음 -->
<img src="images/logo.png">
```

#### 해결
```html
<!-- ✅ 올바른 경로 -->
<img src="/images/logo.png">

<!-- ✅ Hugo 변수 사용 -->
<img src="{{ "images/logo.png" | relURL }}">
```

---

## Hugo 빌드 문제

### ❌ 문제 3: hugo: command not found

#### 증상
```bash
$ hugo --minify
bash: hugo: 명령어를 찾을 수 없음
```

#### 원인
- WSL 환경에서 Windows용 Hugo 실행 파일 사용
- PATH 환경변수 미설정

#### 해결 방법

**방법 1: 상대 경로 사용**
```bash
# 프로젝트 루트에서
./hugo.exe --minify
```

**방법 2: 절대 경로 사용**
```bash
/mnt/d/claude/project2/edu-guide/hugo.exe --minify
```

**방법 3: alias 설정 (영구적)**
```bash
# ~/.bashrc 또는 ~/.zshrc에 추가
alias hugo='/mnt/d/claude/project2/edu-guide/hugo.exe'

# 적용
source ~/.bashrc
```

---

### ❌ 문제 4: Hugo Extended 버전 미사용

#### 증상
```
Error: SCSS/SASS support requires the extended version of Hugo
```

#### 원인
- 일반 Hugo 설치 (Extended 아님)
- SCSS/SASS 파일 사용 시 필수

#### 해결
```bash
# ❌ 일반 버전
hugo version
# hugo v0.135.0 linux/amd64 BuildDate=unknown

# ✅ Extended 버전 설치
scoop install hugo-extended

# 확인
hugo version
# hugo v0.135.0-extended linux/amd64 BuildDate=unknown
```

---

## CSS 및 레이아웃 문제

### ❌ 문제 5: 모바일 헤더 우측 정렬

#### 증상
- PC: 정상 (좌측 정렬)
- 모바일: 로고와 메뉴가 우측에 붙음

#### 발견 과정
```
사용자: "모바일버전에서 상단에 표기되는 로고랑 메뉴가 전부 우측정렬로 되있거든? 
        좌측정렬로 해주면좋을거같아!"
```

#### 원인 분석
```css
/* ❌ 문제 코드 - PC용 스타일이 모바일에도 적용됨 */
.header-content {
    display: flex;
    align-items: flex-end;  /* 우측 정렬 */
}

.main-nav ul {
    justify-content: flex-end;  /* 우측 정렬 */
}
```

#### 해결
```css
/* ✅ 모바일 전용 스타일 추가 */
@media (max-width: 768px) {
    .header-content {
        flex-direction: column;
        align-items: flex-start;  /* 좌측 정렬 */
        gap: 0.8rem;
    }
    
    .main-nav ul {
        gap: 1rem;
        flex-wrap: wrap;
        justify-content: flex-start;  /* 좌측 정렬 */
    }
}
```

#### 파일 위치
`/mnt/d/claude/project2/edu-guide/static/css/style.css`

---

### ❌ 문제 6: 히어로 섹션 오버레이가 너무 진함

#### 증상
- 인포그래픽 배경 이미지가 보라색으로 흐릿함
- 이미지 디테일이 잘 안 보임

#### 발견 과정
```
사용자: "반투명으로 해서 히어로 섹션으로 보라색? 되있잖아, 
        차라리 반투명을 버리고 투명으로 가는게 좋을거같은데??"
```

#### 원인
```css
/* ❌ 문제 코드 - 반투명 오버레이 */
.hero-overlay {
    background: linear-gradient(
        135deg, 
        rgba(102, 126, 234, 0.85) 0%,  /* 85% 불투명 */
        rgba(118, 75, 162, 0.85) 100%
    );
}
```

#### 해결
```css
/* ✅ 완전 투명으로 변경 */
.hero-overlay {
    background: linear-gradient(
        135deg, 
        rgba(102, 126, 234, 0) 0%,  /* 완전 투명 */
        rgba(118, 75, 162, 0) 100%
    );
}
```

#### 추가 옵션
```css
/* 옵션 1: 오버레이 완전 제거 */
.hero-overlay {
    display: none;
}

/* 옵션 2: 약한 그라데이션 (0.3) */
.hero-overlay {
    background: linear-gradient(
        135deg, 
        rgba(102, 126, 234, 0.3) 0%,
        rgba(118, 75, 162, 0.3) 100%
    );
}
```

#### 디자인 팁
- 텍스트 가독성이 중요하면: opacity 0.4-0.6
- 이미지 선명도가 중요하면: opacity 0-0.3
- 배경이 어두우면: 흰색 텍스트 + 낮은 opacity
- 배경이 밝으면: 검은색 텍스트 + 높은 opacity

---

### ❌ 문제 7: Z-index 레이어 순서 혼란

#### 증상
- 슬라이더 이미지가 텍스트 위에 표시됨
- 클릭 불가능한 버튼

#### 원인
```css
/* ❌ Z-index 미설정 */
.hero-bg-slider { }  /* z-index 없음 */
.hero-content { }    /* z-index 없음 */
```

#### 해결
```css
/* ✅ 올바른 레이어 순서 */
.hero-bg-slider {
    z-index: 0;  /* 가장 뒤 (배경) */
}

.hero-overlay {
    z-index: 1;  /* 중간 (오버레이) */
}

.hero-content {
    z-index: 2;  /* 가장 앞 (텍스트/버튼) */
    position: relative;  /* z-index 적용을 위해 필수 */
}
```

---

## Git 및 배포 문제

### ❌ 문제 8: Git에서 한글 파일명 깨짐

#### 증상
```bash
$ git status
modified:   content/middle/\354\225\214\353\246\274.md
```

#### 원인
- Git의 기본 문자 인코딩 설정
- UTF-8 파일명을 8진수로 표시

#### 해결
```bash
# 전역 설정
git config --global core.quotepath false

# 저장소별 설정
git config core.quotepath false

# 확인
git status
# modified:   content/middle/알림.md
```

---

### ❌ 문제 9: Cloudflare Pages 빌드 실패

#### 증상
```
Error: Unable to locate config file or config directory
```

#### 원인
- Hugo 버전 불일치
- Cloudflare가 기본 Hugo 버전 사용

#### 해결
**Cloudflare Pages 설정**:
1. Dashboard → Pages → edu-guide → Settings
2. Environment variables 추가:
   - Variable name: `HUGO_VERSION`
   - Value: `0.135.0`
3. Save
4. Retry deployment

---

### ❌ 문제 10: 배포 후 404 에러

#### 증상
- 로컬: 정상 작동
- 배포 후: 일부 페이지 404

#### 원인 및 해결

**원인 1: baseURL 설정 오류**
```toml
# ❌ 잘못된 설정
baseURL = 'http://localhost:1313/'

# ✅ 올바른 설정
baseURL = 'https://edu-guide.pages.dev/'
```

**원인 2: 대소문자 구분**
```markdown
# ❌ 파일명과 링크 대소문자 불일치
# 파일: content/High/article.md
# 링크: /high/article/

# ✅ 일치시키기
# 파일: content/high/article.md
# 링크: /high/article/
```

---

## 성능 최적화 문제

### ❌ 문제 11: 이미지 로딩 느림

#### 증상
- 페이지 로딩 5초 이상
- Lighthouse 점수 낮음

#### 원인
- 원본 이미지 크기 사용 (5MB+)
- WebP 미사용

#### 해결

**방법 1: Unsplash 파라미터 사용**
```markdown
# ❌ 원본 크기
featured_image: "https://images.unsplash.com/photo-123456"

# ✅ 최적화된 크기
featured_image: "https://images.unsplash.com/photo-123456?w=1200&h=630&fit=crop&q=80"
```

**방법 2: WebP 변환**
```bash
# ImageMagick 사용
convert input.jpg -quality 80 output.webp

# cwebp 사용
cwebp -q 80 input.jpg -o output.webp
```

**방법 3: Hugo 이미지 처리**
```html
{{ $image := resources.Get "images/hero.jpg" }}
{{ $webp := $image.Resize "1200x webp q80" }}
<img src="{{ $webp.RelPermalink }}" loading="lazy">
```

---

### ❌ 문제 12: 카테고리 목록 페이지 느림

#### 증상
- 글이 많아질수록 로딩 시간 증가
- 554개 페이지 빌드 시 2초+

#### 해결

**페이지네이션 추가**
```html
<!-- layouts/_default/list.html -->
{{ $paginator := .Paginate (where .Pages "Type" "in" (slice "high")) 12 }}

{{ range $paginator.Pages }}
  <!-- 글 카드 -->
{{ end }}

{{ template "_internal/pagination.html" . }}
```

**리소스 최적화**
```toml
# hugo.toml
[minify]
  minifyOutput = true

[build]
  writeStats = true
```

---

## AI 협업 시 주의사항

### 🤖 주의 1: 스크린샷 분석 vs 직접 URL

#### 비효율적 방법
```
사용자: "캡처2.png 파일을 봐봐"
AI: (스크린샷 읽기 시도)
```

#### 효율적 방법
```
사용자: "https://edu-guide.pages.dev/high/article/ 이 링크를 확인해줘"
AI: (직접 접근 가능)
```

#### 교훈
- 가능한 **직접 URL 제공**
- 스크린샷은 시각적 설명이 필요할 때만
- 파일 경로 > 스크린샷

---

### 🤖 주의 2: 문제 설명의 구체성

#### 비효율적 설명
```
사용자: "이미지가 안 보여"
AI: (어디서? 어떤 이미지? 추가 질문 필요)
```

#### 효율적 설명
```
사용자: "카테고리 목록 페이지에서 특정 글 2개의 썸네일 이미지가 액박으로 나와. 
        하지만 그 글 상세 페이지에 들어가면 이미지가 정상적으로 보여"
AI: (바로 문제 파악 가능)
```

#### 교훈
- **어디서** (위치)
- **무엇이** (대상)
- **어떻게** (증상)
- **추가 컨텍스트** (다른 곳에서는?)

---

### 🤖 주의 3: 변경 사항 확인

#### 위험한 패턴
```
AI: "파일을 수정했습니다"
사용자: "좋아!" (확인 안 함)
→ 나중에 문제 발생
```

#### 안전한 패턴
```
AI: "파일을 수정했습니다. 로컬에서 미리보기 확인해주세요"
사용자: (확인 후) "잘 적용됐어!"
→ 즉시 피드백
```

#### 교훈
- 수정 후 **항상 로컬 테스트**
- Hugo 서버 실행: `./hugo.exe server -D`
- 모바일/PC 모두 확인

---

### 🤖 주의 4: 점진적 구현

#### 비효율적 방식
```
AI: "10개 기능을 한번에 구현하겠습니다"
→ 어디서 문제인지 찾기 어려움
```

#### 효율적 방식
```
AI: "먼저 1개 기능을 구현하고 테스트하겠습니다"
사용자: "좋아, 다음 기능도 해줘"
→ 문제 발생 시 즉시 파악
```

#### 교훈
- **작은 단위로 구현**
- 각 단계마다 확인
- 문제 발생 시 롤백 용이

---

## 빠른 참조 체크리스트

### 새 글 작성 시
```markdown
- [ ] Front Matter에 featured_image 포함
- [ ] 이미지 URL 중복 확인 (grep -rh "featured_image" content/ | sort | uniq -d)
- [ ] description 필드 작성 (SEO)
- [ ] 카테고리 및 태그 설정
- [ ] 로컬 미리보기 (./hugo.exe server -D)
- [ ] 모바일 반응형 확인 (개발자 도구)
```

### 커밋 전
```bash
- [ ] Hugo 빌드 성공 (./hugo.exe --minify)
- [ ] public/ 폴더 생성 확인
- [ ] 변경사항 검토 (git diff)
- [ ] 의미 있는 커밋 메시지 작성
```

### 배포 후
```markdown
- [ ] Cloudflare Pages 빌드 성공 확인
- [ ] 실제 사이트 접속 테스트
- [ ] 이미지 로딩 확인
- [ ] 모바일 테스트
- [ ] Lighthouse 점수 확인 (성능 90+)
```

---

## 추가 리소스

### 디버깅 명령어
```bash
# 모든 featured_image 검색
grep -r "featured_image" content/

# featured_image 없는 파일 찾기
find content/ -name "*.md" -exec grep -L "featured_image" {} \;

# 중복 이미지 URL 찾기
grep -rh "featured_image" content/ | sort | uniq -d

# Hugo 빌드 (상세 로그)
./hugo.exe --minify --verbose

# 로컬 서버 실행 (초안 포함)
./hugo.exe server -D --bind 0.0.0.0
```

### 유용한 도구
- **이미지 최적화**: https://squoosh.app/
- **WebP 변환**: https://cloudconvert.com/
- **Lighthouse**: Chrome DevTools
- **모바일 테스트**: Chrome DevTools (Ctrl+Shift+M)

---

**📌 이 문서는 지속적으로 업데이트됩니다. 새로운 문제 발생 시 즉시 기록하세요!**
