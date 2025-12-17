// /subjects/ 하위 폴더별 인덱스 페이지 재생성 스크립트
// 과목별 학습 가이드 - 카드 그리드 UI + 페이지네이션 버전

const fs = require('fs');
const path = require('path');

const baseContentDir = path.join(__dirname, '..', 'content', 'subjects');
const outputFile = path.join(__dirname, 'subjects-index-update.json');

const ITEMS_PER_PAGE = 12;

// 과목별 설정
const subjectConfigs = {
  english: {
    title: '영어 학습법 | 문법 · 독해 · 회화 · 수능영어 | 과외를부탁해',
    description: '영어 실력을 확실히 올리는 학습법을 소개합니다. 문법, 독해, 회화, 수능 영어까지 체계적으로 준비하세요.',
    headerClass: 'guide-header-english',
    themeColor: '#3b82f6',
    category: '영어',
    subtitle: '문법 · 독해 · 회화',
    defaultImages: [
      'https://images.unsplash.com/photo-1457369804613-52c61a468e7d?w=800&h=450&fit=crop',
      'https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=800&h=450&fit=crop',
      'https://images.unsplash.com/photo-1546410531-bb4caa6b424d?w=800&h=450&fit=crop'
    ]
  },
  korean: {
    title: '국어 학습법 | 독서 · 문학 · 비문학 · 논술 | 과외를부탁해',
    description: '국어 실력의 기본은 독해력입니다. 문학, 비문학, 논술까지 체계적으로 학습하는 방법을 안내합니다.',
    headerClass: 'guide-header-korean',
    themeColor: '#f43f5e',
    category: '국어',
    subtitle: '독서 · 문학 · 비문학',
    defaultImages: [
      'https://images.unsplash.com/photo-1474932430478-367dbb6832c1?w=800&h=450&fit=crop',
      'https://images.unsplash.com/photo-1507842217343-583bb7270b66?w=800&h=450&fit=crop',
      'https://images.unsplash.com/photo-1512820790803-83ca734da794?w=800&h=450&fit=crop'
    ]
  },
  math: {
    title: '수학 학습법 | 개념 · 유형 · 심화 · 수능수학 | 과외를부탁해',
    description: '수학은 개념이 핵심입니다. 개념 이해부터 유형별 문제 풀이, 수능 수학까지 단계별로 학습하세요.',
    headerClass: 'guide-header-math',
    themeColor: '#6366f1',
    category: '수학',
    subtitle: '개념 · 유형 · 심화',
    defaultImages: [
      'https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=800&h=450&fit=crop',
      'https://images.unsplash.com/photo-1596495578065-6e0763fa1178?w=800&h=450&fit=crop',
      'https://images.unsplash.com/photo-1509228468518-180dd4864904?w=800&h=450&fit=crop'
    ]
  },
  science: {
    title: '과학 학습법 | 물리 · 화학 · 생명 · 지구과학 | 과외를부탁해',
    description: '과학은 원리 이해가 핵심입니다. 물리, 화학, 생명과학, 지구과학을 효과적으로 공부하는 방법을 알려드립니다.',
    headerClass: 'guide-header-science',
    themeColor: '#10b981',
    category: '과학',
    subtitle: '물리 · 화학 · 생명 · 지구',
    defaultImages: [
      'https://images.unsplash.com/photo-1532094349884-543bc11b234d?w=800&h=450&fit=crop',
      'https://images.unsplash.com/photo-1564325724739-bae0bd08f965?w=800&h=450&fit=crop',
      'https://images.unsplash.com/photo-1518152006812-edab29b069ac?w=800&h=450&fit=crop'
    ]
  },
  social: {
    title: '사회 학습법 | 역사 · 지리 · 윤리 · 정치 | 과외를부탁해',
    description: '사회 과목은 흐름을 이해하는 것이 중요합니다. 역사, 지리, 윤리, 정치경제를 효율적으로 학습하세요.',
    headerClass: 'guide-header-social',
    themeColor: '#f59e0b',
    category: '사회',
    subtitle: '역사 · 지리 · 윤리 · 정치',
    defaultImages: [
      'https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?w=800&h=450&fit=crop',
      'https://images.unsplash.com/photo-1461360370896-922624d12a74?w=800&h=450&fit=crop',
      'https://images.unsplash.com/photo-1447069387593-a5de0862481e?w=800&h=450&fit=crop'
    ]
  }
};

function parseYaml(content) {
  const match = content.match(/^---\n([\s\S]*?)\n---/);
  if (!match) return null;
  const yaml = match[1];
  const result = {};
  const titleMatch = yaml.match(/title:\s*"?([^"\n]+)"?/);
  if (titleMatch) result.title = titleMatch[1].trim();
  const descMatch = yaml.match(/description:\s*"?([^"\n]+)"?/);
  if (descMatch) result.description = descMatch[1].trim().substring(0, 120);
  const dateMatch = yaml.match(/date:\s*(\d{4}-\d{2}-\d{2})/);
  if (dateMatch) result.date = dateMatch[1];
  const imgMatch = yaml.match(/featured_image:\s*"?([^"\n]+)"?/);
  if (imgMatch) result.featured_image = imgMatch[1].trim();
  return result;
}

function generateHtml(subject, articles, itemListElement) {
  const config = subjectConfigs[subject];
  const totalPages = Math.ceil(articles.length / ITEMS_PER_PAGE);

  const jsonLd = {
    "@context": "https://schema.org", "@type": "ItemList",
    "name": config.title,
    "description": config.description,
    "url": `https://edukoreaai.com/subjects/${subject}/`,
    "numberOfItems": articles.length,
    "itemListElement": itemListElement
  };

  const articleCards = articles.map((article, idx) => `
<a href="${article.url}" class="guide-card" data-index="${idx}">
<div class="guide-card-image-wrapper"><img src="${article.image}" alt="${article.title}" class="guide-card-image" loading="lazy"></div>
<div class="guide-card-content"><span class="guide-card-category">${config.category}</span><h3 class="guide-card-title">${article.title}</h3>
<p class="guide-card-desc">${article.description}</p><div class="guide-card-footer"><span class="guide-card-date">${article.date}</span><span class="guide-card-arrow">→</span></div></div></a>`).join('\n');

  // 페이지네이션 HTML
  const paginationHtml = totalPages > 1 ? `
<div class="pagination" id="pagination">
<button class="pagination-btn" id="prevBtn" onclick="changePage(-1)">←</button>
<div id="pageNumbers"></div>
<button class="pagination-btn" id="nextBtn" onclick="changePage(1)">→</button>
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
document.getElementById('prevBtn').classList.toggle('disabled',currentPage===1);
document.getElementById('nextBtn').classList.toggle('disabled',currentPage===TOTAL_PAGES);
renderPageNumbers();
document.getElementById('pageInfo').textContent='총 '+TOTAL+'개 중 '+(start+1)+'-'+Math.min(end,TOTAL)+'번째';
window.scrollTo({top:document.querySelector('.guide-card-grid').offsetTop-100,behavior:'smooth'});
history.replaceState(null,null,'#page='+currentPage);
}
function renderPageNumbers(){
const c=document.getElementById('pageNumbers');
let h='';
const delta=2;
for(let i=1;i<=TOTAL_PAGES;i++){
if(i===1||i===TOTAL_PAGES||Math.abs(i-currentPage)<=delta){
h+='<button class="pagination-btn'+(i===currentPage?' active':'')+'" onclick="goToPage('+i+')">'+i+'</button>';
}else if(i===2||i===TOTAL_PAGES-1){
h+='<span class="pagination-ellipsis">...</span>';
}
}
c.innerHTML=h;
}
window.changePage=function(d){showPage(currentPage+d);};
window.goToPage=function(p){showPage(p);};
const hash=window.location.hash.match(/page=(\\d+)/);
showPage(hash?parseInt(hash[1]):1);
})();
</script>` : '';

  return `<!doctype html><html lang=ko><head><meta charset=UTF-8><meta name=viewport content="width=device-width,initial-scale=1"><link rel=preconnect href=https://www.googletagmanager.com crossorigin><link rel=preconnect href=https://cdn.jsdelivr.net crossorigin><title>${config.title}</title>
<meta name=description content="${config.description}"><meta name=keywords content="${config.category}학습법,${config.category}공부법,${config.category}과외,${config.category}학원"><meta name=author content="과외를부탁해 편집팀"><link rel=canonical href=https://edukoreaai.com/subjects/${subject}/><meta name=naver-site-verification content="228c0da6bfc9eda328a78ce3a4417c8ff8630d59"><meta property="og:title" content="${config.title}"><meta property="og:description" content="${config.description}"><meta property="og:type" content="website"><meta property="og:url" content="https://edukoreaai.com/subjects/${subject}/"><meta property="og:site_name" content="과외를부탁해"><meta property="og:locale" content="ko_KR"><meta property="og:image" content="https://edukoreaai.com/images/og-default.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name=twitter:card content="summary_large_image"><meta name=twitter:title content="${config.title}"><meta name=twitter:description content="${config.description}"><meta name=twitter:image content="https://edukoreaai.com/images/og-default.jpg"><script type=application/ld+json>{"@context":"https://schema.org","@type":"WebSite","name":"과외를부탁해","url":"https:\\/\\/edukoreaai.com\\/","description":"초등학생부터 고등학생까지, 학습에 필요한 모든 정보를 한곳에서.","publisher":{"@type":"Organization","name":"과외를부탁해"},"potentialAction":{"@type":"SearchAction","target":"https:\\/\\/edukoreaai.com\\/search?q={search_term_string}","query-input":"required name=search_term_string"},"inLanguage":"ko-KR"}</script><script async src="https://www.googletagmanager.com/gtag/js?id=G-FP3W863XX4"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}gtag("js",new Date),gtag("config","G-FP3W863XX4")</script><link rel=preload as=style href=https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css><link rel=stylesheet href=https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css media=print onload='this.media="all"'><noscript><link rel=stylesheet href=https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css></noscript><link rel=icon type=image/x-icon href=/images/favicon.ico><link rel=icon type=image/png sizes=16x16 href=/images/favicon-16x16.png><link rel=icon type=image/png sizes=32x32 href=/images/favicon-32x32.png><link rel=apple-touch-icon sizes=180x180 href=/images/apple-touch-icon.png><link rel=manifest href=/manifest.json><meta name=theme-color content="${config.themeColor}"><link rel=icon type=image/png sizes=192x192 href=/images/icon-192.png><link rel=icon type=image/png sizes=512x512 href=/images/icon-512.png><meta name=apple-mobile-web-app-capable content="yes"><meta name=apple-mobile-web-app-status-bar-style content="black-translucent"><meta name=apple-mobile-web-app-title content="과외를부탁해"><link rel=preload as=style href=/css/style.css><link rel=preload as=style href=/css/viral.css><link rel=stylesheet href=/css/style.css media=print onload='this.media="all"'><link rel=stylesheet href=/css/viral.css media=print onload='this.media="all"'><noscript><link rel=stylesheet href=/css/style.css><link rel=stylesheet href=/css/viral.css></noscript></head><body><header class=site-header><div class=wide-container><div class=header-content><div class=header-top><div class=site-logo><a href=/><img src=/images/logo.svg alt="과외를부탁해 로고" class=logo-image loading=eager><span>과외를부탁해</span></a></div><button class=mobile-menu-toggle aria-label="메뉴 열기"><span></span><span></span><span></span></button></div><div class=header-actions><a href=/search/ class=search-btn aria-label=검색><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentcolor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/></svg></a><div class=usage-counter><div class=label>누적 사용자</div><div class=count><span id="usageCount">1,000</span>명</div></div></div><nav class=main-nav><ul><li class=has-dropdown><a href>지역별 과외</a><ul class=dropdown><li><a href=/seoul/>서울</a></li><li><a href=/gyeonggi/>경기</a></li><li><a href=/busan/>부산</a></li><li><a href=/incheon/>인천</a></li><li><a href=/daegu/>대구</a></li><li><a href=/cities/>기타 지역</a></li></ul></li><li class=has-dropdown><a href>학습 가이드</a><ul class=dropdown><li><a href=/elementary/>초등학생</a></li><li><a href=/middle/>중학생</a></li><li><a href=/high/>고등학생</a></li></ul></li><li class=has-dropdown><a href>과목별</a><ul class=dropdown><li><a href=/subjects/korean/>국어</a></li><li><a href=/subjects/english/>영어</a></li><li><a href=/subjects/math/>수학</a></li><li><a href=/subjects/science/>과학</a></li><li><a href=/subjects/social/>사회</a></li></ul></li><li><a href=/tutoring/>학습플랜</a></li><li><a href=/exam/>시험 대비</a></li><li><a href=/consultation/>무료 상담</a></li></ul></nav></div></div></header><script>(function(){const e=document.querySelector(".mobile-menu-toggle"),t=document.querySelector(".main-nav"),n=document.querySelector(".site-header");e&&(e.addEventListener("click",function(){this.classList.toggle("active"),t.classList.toggle("active"),document.body.classList.toggle("menu-open");const e=this.classList.contains("active");this.setAttribute("aria-label",e?"메뉴 닫기":"메뉴 열기")}),document.addEventListener("click",function(s){!n.contains(s.target)&&t.classList.contains("active")&&(e.classList.remove("active"),t.classList.remove("active"),document.body.classList.remove("menu-open"),e.setAttribute("aria-label","메뉴 열기"))}))})()</script><main>
<script type=application/ld+json>${JSON.stringify(jsonLd)}</script>
<div class="guide-index-container">
<div class="guide-header ${config.headerClass}">
<h1 class="guide-header-title">${config.category} 학습법</h1>
<p class="guide-header-desc">${config.description}</p>
<div class="guide-header-stats">
<span class="guide-stat"><strong>${articles.length}</strong>개의 가이드</span>
<span class="guide-stat-divider">|</span>
<span class="guide-stat">${config.subtitle}</span>
</div>
</div>
<div class="guide-card-grid">
${articleCards}
</div>
${paginationHtml}
</div>
</main><footer class=site-footer><div class=wide-container><div class=footer-content><div class=footer-brand><div class=footer-logo><img src=/images/logo.svg alt="과외를부탁해 로고" loading=lazy><span>과외를부탁해</span></div><p class=footer-tagline>초등학생부터 고등학생까지,<br>학습에 필요한 모든 정보를 한곳에서</p></div><div class=footer-links><div class=footer-column><h4>학습 가이드</h4><ul><li><a href=/elementary/>초등학생 가이드</a></li><li><a href=/middle/>중학생 가이드</a></li><li><a href=/high/>고등학생 가이드</a></li><li><a href=/exam/>시험 대비 전략</a></li></ul></div><div class=footer-column><h4>과목별 학습</h4><ul><li><a href=/subjects/korean/>국어 학습법</a></li><li><a href=/subjects/english/>영어 학습법</a></li><li><a href=/subjects/math/>수학 학습법</a></li><li><a href=/subjects/science/>과학 학습법</a></li></ul></div><div class=footer-column><h4>지역별 과외</h4><ul><li><a href=/seoul/>서울</a></li><li><a href=/gyeonggi/>경기</a></li><li><a href=/busan/>부산</a></li><li><a href=/cities/>기타 지역</a></li></ul></div><div class=footer-column><h4>상담 서비스</h4><ul><li><a href=/consultation/>무료 상담 신청</a></li><li><a href=/tutoring/>학습플랜</a></li></ul></div></div></div><div class=footer-bottom><p>© 2025 과외를부탁해. All rights reserved. | <a href=/privacy/>개인정보처리방침</a> | <a href=/terms/>이용약관</a></p></div></div></footer><div class=floating-cta><a href=/consultation/ class=cta-button>무료 상담 신청</a></div><script>document.addEventListener("DOMContentLoaded",function(){const e=document.querySelector(".floating-cta");if(e){let t=window.pageYOffset;window.addEventListener("scroll",function(){const n=window.pageYOffset;n>t&&n>300?e.classList.add("hidden"):e.classList.remove("hidden"),t=n})}})</script>${paginationJs}</body></html>`;
}

async function main() {
  console.log('=== /subjects/ 하위 폴더별 인덱스 페이지 재생성 (카드 그리드 UI + 페이지네이션) ===\n');

  const kvData = [];
  const subjects = ['english', 'korean', 'math', 'science', 'social'];

  for (const subject of subjects) {
    const config = subjectConfigs[subject];
    const contentDir = path.join(baseContentDir, subject);

    if (!fs.existsSync(contentDir)) {
      console.log(`${subject}: 폴더 없음, 스킵`);
      continue;
    }

    const files = fs.readdirSync(contentDir)
      .filter(f => f.endsWith('.md') && f !== '_index.md');

    console.log(`${subject}: ${files.length}개 파일`);

    const articles = [];
    for (let i = 0; i < files.length; i++) {
      const file = files[i];
      const filePath = path.join(contentDir, file);
      const content = fs.readFileSync(filePath, 'utf8');
      const meta = parseYaml(content);

      if (meta && meta.title) {
        const slug = file.replace('.md', '');
        let image = meta.featured_image;
        if (!image || image === '/images/default.jpg') {
          image = config.defaultImages[i % config.defaultImages.length];
        }
        articles.push({
          title: meta.title,
          url: `/subjects/${subject}/${slug}/`,
          description: meta.description || `${config.category} 학습에 관한 유용한 정보를 확인하세요.`,
          date: meta.date || '2025-10-28',
          image: image
        });
      }
    }

    articles.sort((a, b) => new Date(b.date) - new Date(a.date));

    const itemListElement = articles.map((article, index) => ({
      "@type": "ListItem", "position": index + 1,
      "item": { "@type": "Article", "name": article.title, "url": `https://edukoreaai.com${article.url}`,
        "description": article.description, "datePublished": article.date, "image": article.image,
        "author": { "@type": "Organization", "name": "과외를부탁해 편집팀" } }
    }));

    const html = generateHtml(subject, articles, itemListElement);
    kvData.push({ key: `/subjects/${subject}/index`, value: html });
  }

  fs.writeFileSync(outputFile, JSON.stringify(kvData, null, 2));
  console.log(`\n✅ 생성 완료: ${outputFile}`);
  console.log(`npx wrangler kv bulk put "subjects-index-update.json" --namespace-id 725aefb7b1c64c6c90d2cf4daf061bf3 --remote`);
}

main().catch(console.error);
