// /middle/ 인덱스 페이지 재생성 스크립트
// 지역 콘텐츠 제외, 일반 학습 가이드만 포함
// 카드 그리드 UI 버전

const fs = require('fs');
const path = require('path');

const contentDir = path.join(__dirname, '..', 'content', 'middle');
const outputFile = path.join(__dirname, 'middle-index-update.json');

// 페이지네이션 설정
const ITEMS_PER_PAGE = 12;

// 기본 이미지 배열 (featured_image 없는 경우 사용)
const defaultImages = [
  'https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=800&h=450&fit=crop',
  'https://images.unsplash.com/photo-1427504494785-3a9ca7044f45?w=800&h=450&fit=crop',
  'https://images.unsplash.com/photo-1509062522246-3755977927d7?w=800&h=450&fit=crop',
  'https://images.unsplash.com/photo-1488190211105-8b0e65b80b4e?w=800&h=450&fit=crop',
  'https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=800&h=450&fit=crop'
];

// YAML 프론트매터 파싱
function parseYaml(content) {
  const match = content.match(/^---\n([\s\S]*?)\n---/);
  if (!match) return null;

  const yaml = match[1];
  const result = {};

  // title
  const titleMatch = yaml.match(/title:\s*"?([^"\n]+)"?/);
  if (titleMatch) result.title = titleMatch[1].trim();

  // description
  const descMatch = yaml.match(/description:\s*"?([^"\n]+)"?/);
  if (descMatch) result.description = descMatch[1].trim().substring(0, 120);

  // date
  const dateMatch = yaml.match(/date:\s*(\d{4}-\d{2}-\d{2})/);
  if (dateMatch) result.date = dateMatch[1];

  // featured_image
  const imgMatch = yaml.match(/featured_image:\s*"?([^"\n]+)"?/);
  if (imgMatch) result.featured_image = imgMatch[1].trim();

  return result;
}

// 일반 가이드 파일인지 확인 (지역명 제외)
function isGeneralGuide(filename) {
  // 지역명이 포함된 파일 패턴 제외
  const regionalPatterns = [
    /^gangnam-/, /^gangdong-/, /^gangbuk-/, /^gangseo-/,
    /^gwanak-/, /^gwangjin-/, /^guro-/, /^geumcheon-/,
    /^nowon-/, /^dobong-/, /^dongdaemun-/, /^dongjak-/,
    /^mapo-/, /^seodaemun-/, /^seocho-/, /^seongdong-/,
    /^seongbuk-/, /^songpa-/, /^yangcheon-/, /^yeongdeungpo-/,
    /^yongsan-/, /^eunpyeong-/, /^jongno-/, /^jung-/, /^jungnang-/,
    /^goyang-/, /^gwangmyeong-/, /^guri-/, /^gunpo-/,
    /^gimpo-/, /^namyangju-/, /^bucheon-/, /^seongnam-/,
    /^suwon-/, /^siheung-/, /^ansan-/, /^anyang-/,
    /^yongin-/, /^uijeongbu-/, /^icheon-/, /^paju-/,
    /^pyeongtaek-/, /^hanam-/, /^hwaseong-/
  ];

  return !regionalPatterns.some(pattern => pattern.test(filename));
}

// 메인 실행
async function main() {
  console.log('=== /middle/ 인덱스 페이지 재생성 (카드 그리드 UI) ===\n');

  const files = fs.readdirSync(contentDir)
    .filter(f => f.endsWith('.md') && f !== '_index.md');

  console.log(`총 파일 수: ${files.length}`);

  const generalGuides = files.filter(isGeneralGuide);
  console.log(`일반 가이드 수: ${generalGuides.length}`);

  const excludedFiles = files.filter(f => !isGeneralGuide(f));
  if (excludedFiles.length > 0) {
    console.log(`제외된 지역 파일: ${excludedFiles.length}`);
    excludedFiles.slice(0, 5).forEach(f => console.log(`  - ${f}`));
  }

  // 글 목록 생성
  const articles = [];

  for (let i = 0; i < generalGuides.length; i++) {
    const file = generalGuides[i];
    const filePath = path.join(contentDir, file);
    const content = fs.readFileSync(filePath, 'utf8');
    const meta = parseYaml(content);

    if (meta && meta.title) {
      const slug = file.replace('.md', '');
      // 이미지 없으면 기본 이미지 배열에서 순환 선택
      let image = meta.featured_image;
      if (!image || image === '/images/default.jpg') {
        image = defaultImages[i % defaultImages.length];
      }

      articles.push({
        title: meta.title,
        url: `/middle/${slug}/`,
        description: meta.description || '중학교 학습에 관한 유용한 정보를 확인하세요.',
        date: meta.date || '2025-10-28',
        image: image
      });
    }
  }

  // 날짜순 정렬 (최신순)
  articles.sort((a, b) => new Date(b.date) - new Date(a.date));

  console.log(`\n생성할 글 목록: ${articles.length}개`);

  // JSON-LD 목록 생성
  const itemListElement = articles.map((article, index) => ({
    "@type": "ListItem",
    "position": index + 1,
    "item": {
      "@type": "Article",
      "name": article.title,
      "url": `https://edukoreaai.com${article.url}`,
      "description": article.description,
      "datePublished": article.date,
      "image": article.image,
      "author": {
        "@type": "Organization",
        "name": "과외를부탁해 편집팀"
      }
    }
  }));

  // HTML 생성
  const html = generateHtml(articles, itemListElement);

  // KV 업로드용 JSON 파일 생성
  const kvData = [{
    key: "/middle/index",
    value: html
  }];

  fs.writeFileSync(outputFile, JSON.stringify(kvData, null, 2));
  console.log(`\n✅ 생성 완료: ${outputFile}`);
  console.log(`\n다음 명령어로 KV에 업로드:`);
  console.log(`npx wrangler kv bulk put "middle-index-update.json" --namespace-id 725aefb7b1c64c6c90d2cf4daf061bf3 --remote`);
}

function generateHtml(articles, itemListElement) {
  const title = '중학생 학습 가이드 | 내신부터 진로까지 | 과외를부탁해';
  const description = '중학교 내신 성공의 모든 것을 담았습니다. 학년별 맞춤 전략과 과목별 학습법으로 안정적인 성적 관리 방법을 안내합니다.';

  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "ItemList",
    "name": "중학생 학습 가이드 | 내신부터 진로까지",
    "description": description,
    "url": "https://edukoreaai.com/middle/",
    "numberOfItems": articles.length,
    "itemListElement": itemListElement
  };

  // 페이지네이션 계산
  const totalPages = Math.ceil(articles.length / ITEMS_PER_PAGE);

  // 카드 HTML 생성 (data-index 추가)
  const articleCards = articles.map((article, index) => `
<a href="${article.url}" class="guide-card" data-index="${index}">
<div class="guide-card-image-wrapper">
<img src="${article.image}" alt="${article.title}" class="guide-card-image" loading="lazy">
</div>
<div class="guide-card-content">
<span class="guide-card-category">중학생</span>
<h3 class="guide-card-title">${article.title}</h3>
<p class="guide-card-desc">${article.description}</p>
<div class="guide-card-footer">
<span class="guide-card-date">${article.date}</span>
<span class="guide-card-arrow">→</span>
</div>
</div>
</a>`).join('\n');

  // 페이지네이션 HTML
  const paginationHtml = totalPages > 1 ? `
<div class="pagination" id="pagination">
<button class="pagination-btn" id="prevBtn" onclick="changePage(-1)">← 이전</button>
<div id="pageNumbers"></div>
<button class="pagination-btn" id="nextBtn" onclick="changePage(1)">다음 →</button>
</div>
<div class="pagination-info" id="pageInfo"></div>` : '';

  // 페이지네이션 JavaScript
  const paginationJs = totalPages > 1 ? `
<script>
(function(){
const ITEMS_PER_PAGE=${ITEMS_PER_PAGE},TOTAL=${articles.length},TOTAL_PAGES=${totalPages};
let currentPage=1;
function showPage(p){
currentPage=Math.max(1,Math.min(p,TOTAL_PAGES));
const cards=document.querySelectorAll('.guide-card');
const start=(currentPage-1)*ITEMS_PER_PAGE,end=start+ITEMS_PER_PAGE;
cards.forEach((c,i)=>{c.style.display=(i>=start&&i<end)?'flex':'none';});
document.getElementById('prevBtn').disabled=currentPage===1;
document.getElementById('nextBtn').disabled=currentPage===TOTAL_PAGES;
document.getElementById('pageInfo').textContent='총 '+TOTAL+'개 중 '+(start+1)+'-'+Math.min(end,TOTAL)+'번째';
renderPageNumbers();
window.scrollTo({top:document.querySelector('.guide-index-container').offsetTop-100,behavior:'smooth'});
history.replaceState(null,null,'#page='+currentPage);
}
window.changePage=function(d){showPage(currentPage+d);};
window.goToPage=function(p){showPage(p);};
function renderPageNumbers(){
const c=document.getElementById('pageNumbers');
let h='';
if(TOTAL_PAGES<=7){for(let i=1;i<=TOTAL_PAGES;i++)h+=btn(i);}
else{
h+=btn(1);
if(currentPage>3)h+='<span class="pagination-ellipsis">...</span>';
let s=Math.max(2,currentPage-1),e=Math.min(TOTAL_PAGES-1,currentPage+1);
if(currentPage<=3){s=2;e=4;}
if(currentPage>=TOTAL_PAGES-2){s=TOTAL_PAGES-3;e=TOTAL_PAGES-1;}
for(let i=s;i<=e;i++)h+=btn(i);
if(currentPage<TOTAL_PAGES-2)h+='<span class="pagination-ellipsis">...</span>';
h+=btn(TOTAL_PAGES);
}
c.innerHTML=h;
}
function btn(n){return '<button class="pagination-num'+(n===currentPage?' active':'')+'" onclick="goToPage('+n+')">'+n+'</button>';}
const hash=window.location.hash;
if(hash.startsWith('#page=')){const p=parseInt(hash.split('=')[1]);if(p>=1&&p<=TOTAL_PAGES)currentPage=p;}
showPage(currentPage);
})();
</script>` : '';

  return `<!doctype html><html lang=ko><head><meta charset=UTF-8><meta name=viewport content="width=device-width,initial-scale=1"><link rel=preconnect href=https://www.googletagmanager.com crossorigin><link rel=preconnect href=https://cdn.jsdelivr.net crossorigin><link rel=dns-prefetch href=https://www.googletagmanager.com><link rel=dns-prefetch href=https://cdn.jsdelivr.net><title>${title}</title>
<meta name=description content="${description}"><meta name=keywords content="중학생,중학교,내신,공부법,중등교육,학원,과외,중간고사,기말고사"><meta name=author content="과외를부탁해 편집팀"><link rel=canonical href=https://edukoreaai.com/middle/><meta name=naver-site-verification content="228c0da6bfc9eda328a78ce3a4417c8ff8630d59"><meta property="og:title" content="${title}"><meta property="og:description" content="${description}"><meta property="og:type" content="website"><meta property="og:url" content="https://edukoreaai.com/middle/"><meta property="og:site_name" content="과외를부탁해"><meta property="og:locale" content="ko_KR"><meta property="og:image" content="https://edukoreaai.com/images/og-default.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name=twitter:card content="summary_large_image"><meta name=twitter:title content="${title}"><meta name=twitter:description content="${description}"><meta name=twitter:image content="https://edukoreaai.com/images/og-default.jpg"><script type=application/ld+json>{"@context":"https://schema.org","@type":"WebSite","name":"과외를부탁해","url":"https:\\/\\/edukoreaai.com\\/","description":"초등학생부터 고등학생까지, 학습에 필요한 모든 정보를 한곳에서. 과목별 공부법, 내신 대비, 수능 준비, 지역별 학원·과외 정보까지.","publisher":{"@type":"Organization","name":"과외를부탁해"},"potentialAction":{"@type":"SearchAction","target":"https:\\/\\/edukoreaai.com\\/search?q={search_term_string}","query-input":"required name=search_term_string"},"inLanguage":"ko-KR"}</script><script async src="https://www.googletagmanager.com/gtag/js?id=G-FP3W863XX4"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}gtag("js",new Date),gtag("config","G-FP3W863XX4")</script><link rel=preload as=style href=https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css><link rel=stylesheet href=https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css media=print onload='this.media="all"'><noscript><link rel=stylesheet href=https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css></noscript><link rel=icon type=image/x-icon href=/images/favicon.ico><link rel=icon type=image/png sizes=16x16 href=/images/favicon-16x16.png><link rel=icon type=image/png sizes=32x32 href=/images/favicon-32x32.png><link rel=apple-touch-icon sizes=180x180 href=/images/apple-touch-icon.png><link rel=manifest href=/manifest.json><meta name=theme-color content="#10b981"><link rel=icon type=image/png sizes=192x192 href=/images/icon-192.png><link rel=icon type=image/png sizes=512x512 href=/images/icon-512.png><meta name=apple-mobile-web-app-capable content="yes"><meta name=apple-mobile-web-app-status-bar-style content="black-translucent"><meta name=apple-mobile-web-app-title content="과외를부탁해"><link rel=preload as=style href=/css/style.css><link rel=preload as=style href=/css/viral.css><link rel=stylesheet href=/css/style.css media=print onload='this.media="all"'><link rel=stylesheet href=/css/viral.css media=print onload='this.media="all"'><noscript><link rel=stylesheet href=/css/style.css><link rel=stylesheet href=/css/viral.css></noscript></head><body><header class=site-header><div class=wide-container><div class=header-content><div class=header-top><div class=site-logo><a href=/><img src=/images/logo.svg alt="과외를부탁해 로고" class=logo-image loading=eager>
<span>과외를부탁해</span></a></div><button class=mobile-menu-toggle aria-label="메뉴 열기">
<span></span>
<span></span>
<span></span></button></div><div class=header-actions><a href=/search/ class=search-btn aria-label=검색><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentcolor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/></svg></a><div class=usage-counter><div class=label>누적 사용자</div><div class=count><span id="usageCount">1,000</span>명</div></div></div><nav class=main-nav><ul><li class=has-dropdown><a href>지역별 과외</a><ul class=dropdown><li><a href=/seoul/>서울</a></li><li><a href=/gyeonggi/>경기</a></li><li><a href=/busan/>부산</a></li><li><a href=/incheon/>인천</a></li><li><a href=/daegu/>대구</a></li><li><a href=/cities/>기타 지역</a></li></ul></li><li class=has-dropdown><a href>학습 가이드</a><ul class=dropdown><li><a href=/elementary/>초등학생</a></li><li><a href=/middle/>중학생</a></li><li><a href=/high/>고등학생</a></li></ul></li><li class=has-dropdown><a href>과목별</a><ul class=dropdown><li><a href=/subjects/korean/>국어</a></li><li><a href=/subjects/english/>영어</a></li><li><a href=/subjects/math/>수학</a></li><li><a href=/subjects/science/>과학</a></li><li><a href=/subjects/social/>사회</a></li></ul></li><li><a href=/tutoring/>학습플랜</a></li><li><a href=/exam/>시험 대비</a></li><li><a href=/consultation/>무료 상담</a></li></ul></nav></div></div></header><script>(function(){const e=document.querySelector(".mobile-menu-toggle"),t=document.querySelector(".main-nav"),n=document.querySelector(".site-header");e&&(e.addEventListener("click",function(){this.classList.toggle("active"),t.classList.toggle("active"),document.body.classList.toggle("menu-open");const e=this.classList.contains("active");this.setAttribute("aria-label",e?"메뉴 닫기":"메뉴 열기")}),document.addEventListener("click",function(s){!n.contains(s.target)&&t.classList.contains("active")&&(e.classList.remove("active"),t.classList.remove("active"),document.body.classList.remove("menu-open"),e.setAttribute("aria-label","메뉴 열기"))}))})()</script><main>
<script type=application/ld+json>${JSON.stringify(jsonLd)}</script>
<div class="guide-index-container">
<div class="guide-header guide-header-middle">
<h1 class="guide-header-title">중학생 학습 가이드</h1>
<p class="guide-header-desc">${description}</p>
<div class="guide-header-stats">
<span class="guide-stat"><strong>${articles.length}</strong>개의 가이드</span>
<span class="guide-stat-divider">|</span>
<span class="guide-stat">내신 · 진로 · 학습법</span>
</div>
</div>
<div class="guide-card-grid">
${articleCards}
</div>
${paginationHtml}
</div>
${paginationJs}
</main><footer class=site-footer><div class=wide-container><div class=footer-content><div class=footer-brand><div class=footer-logo><img src=/images/logo.svg alt="과외를부탁해 로고" loading=lazy>
<span>과외를부탁해</span></div><p class=footer-tagline>초등학생부터 고등학생까지,<br>학습에 필요한 모든 정보를 한곳에서</p></div><div class=footer-links><div class=footer-column><h4>학습 가이드</h4><ul><li><a href=/elementary/>초등학생 가이드</a></li><li><a href=/middle/>중학생 가이드</a></li><li><a href=/high/>고등학생 가이드</a></li><li><a href=/exam/>시험 대비 전략</a></li></ul></div><div class=footer-column><h4>과목별 학습</h4><ul><li><a href=/subjects/korean/>국어 학습법</a></li><li><a href=/subjects/english/>영어 학습법</a></li><li><a href=/subjects/math/>수학 학습법</a></li><li><a href=/subjects/science/>과학 학습법</a></li></ul></div><div class=footer-column><h4>지역별 과외</h4><ul><li><a href=/seoul/>서울</a></li><li><a href=/gyeonggi/>경기</a></li><li><a href=/busan/>부산</a></li><li><a href=/cities/>기타 지역</a></li></ul></div><div class=footer-column><h4>상담 서비스</h4><ul><li><a href=/consultation/>무료 상담 신청</a></li><li><a href=/tutoring/>학습플랜</a></li></ul></div></div></div><div class=footer-bottom><p>© 2025 과외를부탁해. All rights reserved. | <a href=/privacy/>개인정보처리방침</a> | <a href=/terms/>이용약관</a></p></div></div></footer><div class=floating-cta><a href=/consultation/ class=cta-button>무료 상담 신청</a></div><script>document.addEventListener("DOMContentLoaded",function(){const e=document.querySelector(".floating-cta");if(e){let t=window.pageYOffset;window.addEventListener("scroll",function(){const n=window.pageYOffset;n>t&&n>300?e.classList.add("hidden"):e.classList.remove("hidden"),t=n})}})</script></body></html>`;
}

main().catch(console.error);
