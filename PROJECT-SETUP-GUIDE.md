# Hugo + Cloudflare Pages 블로그 구축 완벽 가이드

> **작성일**: 2025년 10월 17일  
> **프로젝트**: 과외를부탁해 (edu-guide)  
> **스택**: Hugo v0.135.0-extended + Cloudflare Pages + Git

이 문서는 Hugo 정적 사이트 생성기와 Cloudflare Pages를 사용하여 교육 정보 블로그를 구축한 전체 과정을 기록합니다. 시행착오와 해결 방법을 포함하여 향후 유사한 프로젝트에 참고할 수 있도록 작성되었습니다.

---

## 📋 목차

1. [프로젝트 개요](#프로젝트-개요)
2. [기술 스택 및 선택 이유](#기술-스택-및-선택-이유)
3. [초기 설정 단계](#초기-설정-단계)
4. [프로젝트 구조](#프로젝트-구조)
5. [주요 구현 내용](#주요-구현-내용)
6. [시행착오 및 해결방법](#시행착오-및-해결방법)
7. [배포 프로세스](#배포-프로세스)
8. [유지보수 팁](#유지보수-팁)

---

## 프로젝트 개요

### 목적
초등학생부터 고등학생까지의 학습 정보를 제공하는 교육 블로그 플랫폼 구축

### 주요 기능
- 카테고리별 학습 정보 제공 (초등/중등/고등/지역)
- 반응형 디자인 (모바일/PC)
- SEO 최적화
- 빠른 페이지 로딩 (정적 사이트)
- 자동 배포 시스템

### 사이트 정보
- **사이트명**: 과외를부탁해
- **URL**: https://edu-guide.pages.dev/
- **프로젝트 경로**: `/mnt/d/claude/project2/edu-guide`

---

## 기술 스택 및 선택 이유

### Hugo Static Site Generator
**버전**: v0.135.0-extended (Windows)

**선택 이유**:
- ✅ **속도**: Go 언어 기반으로 매우 빠른 빌드 속도
- ✅ **SEO**: 정적 HTML 생성으로 검색엔진 최적화에 유리
- ✅ **성능**: 클라이언트 사이드 JavaScript 의존성 최소화
- ✅ **마크다운**: 콘텐츠 작성이 간편함
- ✅ **무료**: 오픈소스, 호스팅 비용 무료

### Cloudflare Pages
**선택 이유**:
- ✅ **무료 호스팅**: 무제한 대역폭
- ✅ **자동 배포**: Git 푸시 시 자동 빌드 및 배포
- ✅ **CDN**: 전 세계 엣지 서버를 통한 빠른 속도
- ✅ **SSL**: 자동 HTTPS 적용
- ✅ **간편함**: GitHub/GitLab 연동 간단

### Git Desktop
**선택 이유**:
- ✅ **시각적**: GUI로 변경사항 확인 용이
- ✅ **협업**: 버전 관리 및 협업에 필수
- ✅ **자동 배포 연동**: Cloudflare Pages와 연동

---

## 초기 설정 단계

### 1. Hugo 설치

```bash
# Windows 환경 (Scoop 사용)
scoop install hugo-extended

# 또는 직접 다운로드
# https://github.com/gohugoio/hugo/releases
# hugo_extended_0.135.0_windows-amd64.zip 다운로드 및 압축 해제
```

**중요**: 반드시 `hugo-extended` 버전을 설치해야 SCSS/SASS 사용 가능

### 2. 프로젝트 생성

```bash
# 프로젝트 디렉토리로 이동
cd /mnt/d/claude/project2

# Hugo 사이트 생성
hugo new site edu-guide
cd edu-guide
```

### 3. Git 초기화

```bash
# Git 저장소 초기화
git init

# .gitignore 파일 생성
echo "/public" >> .gitignore
echo "/resources" >> .gitignore
echo ".hugo_build.lock" >> .gitignore
```

### 4. GitHub Repository 생성 및 연결

1. GitHub에서 새 저장소 생성 (`edu-guide`)
2. Git Desktop 사용하여 로컬 저장소와 연결
3. 초기 커밋 및 푸시

```bash
git add .
git commit -m "Initial commit: Hugo site setup"
git branch -M main
git remote add origin https://github.com/[username]/edu-guide.git
git push -u origin main
```

### 5. Cloudflare Pages 연동

1. Cloudflare 대시보드 접속
2. Pages 섹션으로 이동
3. "Create a project" 클릭
4. GitHub 저장소 연결 (`edu-guide`)
5. 빌드 설정:
   - **Framework preset**: Hugo
   - **Build command**: `hugo --minify`
   - **Build output directory**: `public`
   - **Environment variables**: 
     - `HUGO_VERSION`: `0.135.0`

---

## 프로젝트 구조

```
edu-guide/
├── archetypes/           # 콘텐츠 템플릿
│   └── default.md
├── content/              # 마크다운 콘텐츠
│   ├── elementary/       # 초등학교 카테고리
│   ├── middle/          # 중학교 카테고리
│   ├── high/            # 고등학교 카테고리
│   ├── local/           # 지역 정보 카테고리
│   └── _index.md        # 홈페이지 콘텐츠
├── layouts/              # HTML 템플릿
│   ├── _default/
│   │   ├── baseof.html  # 기본 레이아웃
│   │   ├── list.html    # 목록 페이지
│   │   └── single.html  # 상세 페이지
│   ├── partials/
│   │   ├── header.html  # 헤더
│   │   └── footer.html  # 푸터
│   └── index.html       # 홈페이지 템플릿
├── static/               # 정적 파일
│   ├── css/
│   │   └── style.css    # 메인 스타일시트
│   ├── images/          # 이미지 파일
│   │   ├── infographic-korean.webp
│   │   ├── infographic-english.webp
│   │   ├── infographic-study-comparison.webp
│   │   └── infographic-curriculum.webp
│   └── favicon.ico
├── hugo.toml            # Hugo 설정 파일
├── hugo.exe             # Hugo 실행 파일 (Windows)
└── README.md
```

---

## 주요 구현 내용

### 1. Hugo 설정 (hugo.toml)

```toml
baseURL = 'https://edu-guide.pages.dev/'
languageCode = 'ko-kr'
title = '과외를부탁해 - 초중고 학습 정보 플랫폼'
theme = ''  # 커스텀 테마 사용

[params]
  description = "초등학생부터 고등학생까지, 학습에 필요한 모든 정보를 제공합니다"
  author = "과외를부탁해 편집팀"

[taxonomies]
  category = 'categories'
  tag = 'tags'

[markup]
  [markup.goldmark]
    [markup.goldmark.renderer]
      unsafe = true  # HTML in markdown 허용
[markup.tableOfContents]
      startLevel = 2
      endLevel = 4
```

### 2. 카테고리 구조 설정

각 카테고리마다 `_index.md` 파일 생성:

**예시: content/high/_index.md**
```markdown
---
title: "고등학교"
description: "고등학생을 위한 수능, 내신, 입시 정보"
---
```

### 3. 콘텐츠 작성 규칙

모든 글은 다음 형식의 Front Matter를 포함:

```markdown
---
title: "글 제목"
date: 2025-10-17T10:00:00+09:00
categories: ["카테고리1", "카테고리2"]
tags: ["태그1", "태그2"]
keywords: ["검색키워드1", "검색키워드2"]
description: "SEO를 위한 설명 (120자 이내)"
author: "과외를부탁해 편집팀"
featured_image: "https://images.unsplash.com/photo-xxxxx?w=1200&h=630&fit=crop"
---

# 본문 내용...
```

**중요**: `featured_image`는 **필수**입니다. 카테고리 목록 페이지에서 썸네일로 사용됩니다.

### 4. 홈페이지 히어로 섹션 (슬라이더)

`layouts/index.html`에 구현된 자동 슬라이드 기능:

```html
<div class="home-hero">
    <div class="hero-bg-slider">
        <div class="hero-bg-slide active" style="background-image: url('/images/infographic-korean.webp')"></div>
        <div class="hero-bg-slide" style="background-image: url('/images/infographic-english.webp')"></div>
        <div class="hero-bg-slide" style="background-image: url('/images/infographic-study-comparison.webp')"></div>
        <div class="hero-bg-slide" style="background-image: url('/images/infographic-curriculum.webp')"></div>
    </div>
    <div class="hero-overlay"></div>
    <div class="hero-content">
        <h1 class="hero-title">📚 과외를부탁해</h1>
        <p class="hero-subtitle">초등학생부터 고등학생까지, 학습에 필요한 모든 정보</p>
    </div>
</div>

<script>
(function() {
    const slides = document.querySelectorAll('.hero-bg-slide');
    let currentSlide = 0;
    
    function nextSlide() {
        slides[currentSlide].classList.remove('active');
        currentSlide = (currentSlide + 1) % slides.length;
        slides[currentSlide].classList.add('active');
    }
    
    // 5초마다 슬라이드 변경
    setInterval(nextSlide, 5000);
})();
</script>
```

**특징**:
- 5초마다 자동 전환
- 페이드 인/아웃 효과
- 4개의 커스텀 인포그래픽 이미지 사용
- 완전 투명 오버레이로 이미지 선명하게 표시

### 5. 반응형 디자인

`static/css/style.css`에서 모바일 최적화:

```css
@media (max-width: 768px) {
    .home-hero {
        padding: 40px 20px;
        margin-top: 2rem;
    }
    
    .hero-title {
        font-size: var(--font-xl);
    }
    
    /* 카테고리 그리드 - 2열 레이아웃 */
    .category-grid {
        grid-template-columns: repeat(2, 1fr);
        gap: 12px;
        padding: 0 8px;
    }
    
    /* 헤더 좌측 정렬 */
    .header-content {
        flex-direction: column;
        align-items: flex-start;
        gap: 0.8rem;
    }
    
    .main-nav ul {
        gap: 1rem;
        flex-wrap: wrap;
        justify-content: flex-start;
    }
}
```

---

## 시행착오 및 해결방법

### ⚠️ 문제 1: 카테고리 목록에서 이미지가 안 보임

**증상**:
- 글 상세 페이지에서는 이미지가 보임
- 카테고리 목록 페이지에서는 이미지가 안 보임 (액박)

**원인**:
- Front Matter에 `featured_image` 필드가 없음
- 또는 여러 글이 **동일한 이미지 URL**을 사용

**해결방법**:
```markdown
# 각 .md 파일의 Front Matter에 추가
featured_image: "https://images.unsplash.com/photo-xxxxx?w=1200&h=630&fit=crop"
```

**중요**: 각 글마다 **고유한** 이미지 URL을 사용해야 합니다!

### ⚠️ 문제 2: Hugo 명령어를 찾을 수 없음

**증상**:
```bash
$ hugo --minify
bash: hugo: command not found
```

**원인**:
- WSL 환경에서 Windows용 Hugo 실행 파일 사용

**해결방법**:
```bash
# 프로젝트 루트에 hugo.exe 파일이 있는 경우
./hugo.exe --minify

# 또는 절대 경로 사용
/mnt/d/claude/project2/edu-guide/hugo.exe --minify
```

### ⚠️ 문제 3: 모바일에서 헤더가 우측 정렬됨

**증상**:
- PC에서는 정상
- 모바일에서 로고와 메뉴가 우측에 붙어있음

**원인**:
- CSS에서 `align-items: flex-end` 설정

**해결방법**:
```css
@media (max-width: 768px) {
    .header-content {
        align-items: flex-start;  /* flex-end → flex-start */
    }
    
    .main-nav ul {
        justify-content: flex-start;  /* flex-end → flex-start */
    }
}
```

### ⚠️ 문제 4: 히어로 섹션 오버레이가 너무 진함

**증상**:
- 인포그래픽 이미지가 보라색으로 흐릿하게 보임

**원인**:
- 반투명 오버레이 `rgba(102, 126, 234, 0.85)`

**해결방법**:
```css
.hero-overlay {
    /* 기존 */
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.85) 0%, rgba(118, 75, 162, 0.85) 100%);
    
    /* 수정 - 완전 투명 */
    background: linear-gradient(135deg, rgba(102, 126, 234, 0) 0%, rgba(118, 75, 162, 0) 100%);
}
```

### ⚠️ 문제 5: Git Desktop에서 한글 파일명 깨짐

**증상**:
- 한글 파일명이 `\355\225\234\352\270\200.md` 형식으로 보임

**원인**:
- Git의 기본 문자 인코딩 설정

**해결방법**:
```bash
git config --global core.quotepath false
```

### ⚠️ 문제 6: Cloudflare Pages 빌드 실패

**증상**:
```
Error: Unable to locate config file or config directory
```

**원인**:
- Hugo 버전 불일치
- `hugo.toml` 파일 경로 문제

**해결방법**:
1. Cloudflare Pages 설정에서 환경 변수 추가:
   - `HUGO_VERSION`: `0.135.0`
2. 빌드 명령어 확인: `hugo --minify`
3. 출력 디렉토리 확인: `public`

---

## 배포 프로세스

### 자동 배포 워크플로우

1. **로컬에서 작업**:
   ```bash
   # 새 글 작성
   hugo new high/new-article.md
   
   # Front Matter 작성 (featured_image 필수!)
   
   # 로컬 서버로 미리보기
   ./hugo.exe server -D
   # http://localhost:1313 접속
   ```

2. **빌드 테스트**:
   ```bash
   # 프로덕션 빌드
   ./hugo.exe --minify
   
   # public/ 폴더 생성 확인
   ls public/
   ```

3. **Git 커밋**:
   - Git Desktop 사용
   - 변경사항 확인
   - 커밋 메시지 작성
   - Push to origin

4. **자동 배포**:
   - Cloudflare Pages가 자동으로 감지
   - 빌드 시작 (~2분 소요)
   - 배포 완료
   - https://edu-guide.pages.dev 자동 업데이트

### 수동 배포 (필요시)

Cloudflare Dashboard → Pages → edu-guide → Deployments → "Retry deployment"

---

## 유지보수 팁

### 1. 정기적인 체크리스트

**새 글 작성 시**:
- [ ] Front Matter에 `featured_image` 포함
- [ ] 이미지 URL이 다른 글과 중복되지 않는지 확인
- [ ] `description` 필드 작성 (SEO)
- [ ] 카테고리 및 태그 설정
- [ ] 로컬에서 미리보기 확인
- [ ] 모바일 반응형 확인

**커밋 전**:
- [ ] Hugo 빌드 성공 확인
- [ ] 변경사항 검토
- [ ] 의미 있는 커밋 메시지 작성

### 2. 이미지 최적화

**권장 사항**:
- WebP 형식 사용 (용량 50% 감소)
- 적절한 크기: 1200x630 (Open Graph)
- Unsplash 사용 시: `?w=1200&h=630&fit=crop` 파라미터 추가
- 커스텀 이미지는 `/static/images/` 폴더에 저장

**커스텀 이미지 추가 방법**:
```bash
# 이미지 파일을 static/images/에 복사
cp /path/to/image.webp static/images/

# 마크다운에서 참조
featured_image: "/images/image.webp"
```

### 3. SEO 최적화

**필수 Front Matter 필드**:
- `title`: 60자 이내
- `description`: 120-160자
- `keywords`: 관련 검색어 5-10개
- `featured_image`: Open Graph 이미지
- `date`: 발행일

**추가 최적화**:
- `hugo.toml`에 `googleAnalytics` 설정
- `sitemap.xml` 자동 생성 (Hugo 기본 제공)
- `robots.txt` 설정

### 4. 성능 모니터링

**체크 포인트**:
- Cloudflare Analytics에서 트래픽 확인
- 페이지 로딩 속도: < 3초
- Lighthouse 점수: 90점 이상
- 모바일 성능 테스트

### 5. 백업 전략

**자동 백업**:
- GitHub에 모든 소스 코드 저장됨
- Cloudflare Pages에 빌드 히스토리 보관

**권장 추가 백업**:
```bash
# 주기적으로 로컬 백업
tar -czf edu-guide-backup-$(date +%Y%m%d).tar.gz edu-guide/

# 또는 별도 Git 저장소에 미러링
git remote add backup https://gitlab.com/user/edu-guide.git
git push backup main
```

---

## 트러블슈팅 가이드

### 빌드 에러 발생 시

1. **로컬에서 빌드 테스트**:
   ```bash
   ./hugo.exe --minify
   ```

2. **에러 메시지 확인**:
   - 파일 경로 오류
   - Front Matter 형식 오류
   - 템플릿 문법 오류

3. **일반적인 해결 방법**:
   ```bash
   # 캐시 삭제
   rm -rf public/ resources/
   
   # 다시 빌드
   ./hugo.exe --minify
   ```

### 이미지가 안 보일 때

1. **featured_image 확인**:
   ```bash
   # 모든 .md 파일에서 featured_image 검색
   grep -r "featured_image" content/
   ```

2. **이미지 URL 중복 확인**:
   ```bash
   # 중복된 이미지 URL 찾기
   grep -rh "featured_image" content/ | sort | uniq -d
   ```

3. **이미지 URL 유효성 확인**:
   - 브라우저에서 직접 URL 접속 테스트
   - Unsplash 이미지는 파라미터 확인

### 배포가 안 될 때

1. **Cloudflare Pages 로그 확인**:
   - Dashboard → Pages → edu-guide → View build log

2. **환경 변수 확인**:
   - `HUGO_VERSION` 설정 확인

3. **빌드 명령어 확인**:
   - Build command: `hugo --minify`
   - Output directory: `public`

---

## 참고 자료

### Hugo 공식 문서
- 공식 사이트: https://gohugo.io/
- 문서: https://gohugo.io/documentation/
- 커뮤니티: https://discourse.gohugo.io/

### Cloudflare Pages
- 문서: https://developers.cloudflare.com/pages/
- Hugo 가이드: https://developers.cloudflare.com/pages/framework-guides/deploy-a-hugo-site/

### 유용한 도구
- Unsplash (무료 이미지): https://unsplash.com/
- WebP 변환: https://cloudconvert.com/
- Markdown 에디터: VS Code + Markdown Preview

---

## 버전 히스토리

### v1.0.0 (2025-10-17)
- ✅ 초기 Hugo 사이트 구축
- ✅ Cloudflare Pages 연동
- ✅ 4개 카테고리 구조 설정
- ✅ 반응형 디자인 구현
- ✅ 히어로 섹션 슬라이더 구현
- ✅ 커스텀 인포그래픽 이미지 적용

### 향후 계획
- [ ] 검색 기능 추가
- [ ] 댓글 시스템 통합
- [ ] 다크 모드 지원
- [ ] 관련 글 추천 기능
- [ ] RSS 피드 최적화

---

## 연락처

프로젝트 관련 문의: 과외를부탁해 편집팀  
사이트: https://edu-guide.pages.dev/

---

**📌 이 가이드를 참고하여 새로운 Hugo 블로그를 쉽게 시작할 수 있습니다!**
