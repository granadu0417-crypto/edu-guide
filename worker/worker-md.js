/**
 * 과외를부탁해 - Markdown Direct Render Worker
 *
 * .md 파일을 KV에 직접 저장하고, Worker에서 HTML로 변환하여 서빙
 * Hugo 빌드 없이 초 단위 배포 가능
 */

// ============================================================
// YAML Front Matter 파서
// ============================================================
function parseYamlFrontMatter(content) {
  const match = content.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
  if (!match) {
    return { frontMatter: {}, body: content };
  }

  const yamlStr = match[1];
  const body = match[2];
  const frontMatter = {};

  // 간단한 YAML 파싱 (중첩 없는 경우)
  const lines = yamlStr.split('\n');
  let currentKey = null;
  let currentArray = null;

  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed) continue;

    // 배열 항목
    if (trimmed.startsWith('- ')) {
      if (currentKey && currentArray !== null) {
        currentArray.push(trimmed.slice(2).trim().replace(/^["']|["']$/g, ''));
      }
      continue;
    }

    // 키: 값
    const colonIdx = trimmed.indexOf(':');
    if (colonIdx > 0) {
      const key = trimmed.slice(0, colonIdx).trim();
      const value = trimmed.slice(colonIdx + 1).trim();

      if (value === '') {
        // 배열 시작
        currentKey = key;
        currentArray = [];
        frontMatter[key] = currentArray;
      } else {
        // 일반 값
        currentKey = null;
        currentArray = null;
        frontMatter[key] = value.replace(/^["']|["']$/g, '');
      }
    }
  }

  return { frontMatter, body };
}

// ============================================================
// Markdown to HTML 변환기
// ============================================================
function markdownToHtml(markdown) {
  let html = markdown;

  // 코드 블록 보호 (변환 전 임시 치환)
  const codeBlocks = [];
  html = html.replace(/```[\s\S]*?```/g, (match) => {
    codeBlocks.push(match);
    return `__CODE_BLOCK_${codeBlocks.length - 1}__`;
  });

  // 인라인 코드 보호
  const inlineCodes = [];
  html = html.replace(/`[^`]+`/g, (match) => {
    inlineCodes.push(match);
    return `__INLINE_CODE_${inlineCodes.length - 1}__`;
  });

  // 헤딩 (H1-H6)
  html = html.replace(/^######\s+(.+)$/gm, '<h6>$1</h6>');
  html = html.replace(/^#####\s+(.+)$/gm, '<h5>$1</h5>');
  html = html.replace(/^####\s+(.+)$/gm, '<h4>$1</h4>');
  html = html.replace(/^###\s+(.+)$/gm, '<h3>$1</h3>');
  html = html.replace(/^##\s+(.+)$/gm, '<h2>$1</h2>');
  html = html.replace(/^#\s+(.+)$/gm, '<h1>$1</h1>');

  // 볼드, 이탤릭
  html = html.replace(/\*\*\*(.+?)\*\*\*/g, '<strong><em>$1</em></strong>');
  html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
  html = html.replace(/\*(.+?)\*/g, '<em>$1</em>');

  // 링크
  html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2">$1</a>');

  // 이미지
  html = html.replace(/!\[([^\]]*)\]\(([^)]+)\)/g, '<img src="$2" alt="$1" loading="lazy">');

  // 수평선
  html = html.replace(/^---$/gm, '<hr>');
  html = html.replace(/^\*\*\*$/gm, '<hr>');

  // 순서 없는 목록
  html = html.replace(/^[\*\-]\s+(.+)$/gm, '<li>$1</li>');
  html = html.replace(/(<li>.*<\/li>\n?)+/g, '<ul>$&</ul>');

  // 순서 있는 목록
  html = html.replace(/^\d+\.\s+(.+)$/gm, '<li>$1</li>');

  // 문단 (빈 줄로 구분)
  const blocks = html.split(/\n\n+/);
  html = blocks.map(block => {
    block = block.trim();
    if (!block) return '';
    // 이미 HTML 태그로 시작하면 그대로
    if (/^<[a-zA-Z]/.test(block)) return block;
    // div (아이보리 박스 등)는 그대로
    if (block.includes('<div')) return block;
    // 문단으로 감싸기
    return `<p>${block.replace(/\n/g, '<br>')}</p>`;
  }).join('\n\n');

  // 코드 블록 복원
  html = html.replace(/__CODE_BLOCK_(\d+)__/g, (_, idx) => {
    const code = codeBlocks[parseInt(idx)];
    const match = code.match(/```(\w*)\n([\s\S]*?)```/);
    if (match) {
      const lang = match[1] || '';
      const content = match[2].replace(/</g, '&lt;').replace(/>/g, '&gt;');
      return `<pre><code class="language-${lang}">${content}</code></pre>`;
    }
    return code;
  });

  // 인라인 코드 복원
  html = html.replace(/__INLINE_CODE_(\d+)__/g, (_, idx) => {
    const code = inlineCodes[parseInt(idx)];
    const content = code.slice(1, -1).replace(/</g, '&lt;').replace(/>/g, '&gt;');
    return `<code>${content}</code>`;
  });

  return html;
}

// ============================================================
// 숏코드 처리
// ============================================================
function processShortcodes(html) {
  // {{< cta-dual type="final" >}}
  html = html.replace(/\{\{<\s*cta-dual\s+type="final"\s*>\}\}/g, getCTAFinalHTML());

  // {{< cta-dual type="inline" >}}
  html = html.replace(/\{\{<\s*cta-dual\s+type="inline"\s*>\}\}/g, getCTAInlineHTML());

  return html;
}

function getCTAFinalHTML() {
  return `
<div class="cta-dual-final">
  <div class="dual-final-box">
    <h3>🎓 지금 바로 1:1 무료 체험수업 신청하세요!</h3>
    <p class="dual-final-desc">우리 아이와 잘 맞는 1:1맞춤 선생님과 체험수업 받아보시고 결정하세요!</p>
    <div class="dual-final-buttons">
      <a href="https://pf.kakao.com/_Cixlaxl/chat" target="_blank" rel="noopener noreferrer" class="dual-btn-final-kakao">
        💬 카카오톡 상담하기
      </a>
      <a href="https://naver.me/FGENm9ex" target="_blank" rel="noopener noreferrer" class="dual-btn-final-trial">
        ✨ 무료체험 신청하기
      </a>
    </div>
    <div class="dual-final-features">
      <div class="feature-item"><span class="feature-icon">✅</span><span class="feature-text">완전 무료</span></div>
      <div class="feature-item"><span class="feature-icon">⚡</span><span class="feature-text">빠른 답변</span></div>
    </div>
  </div>
</div>`;
}

function getCTAInlineHTML() {
  return `
<div class="cta-dual-inline">
  <div class="dual-inline-box">
    <div class="dual-inline-icon">📞</div>
    <div class="dual-inline-content">
      <h3>궁금한 점이 있으신가요?</h3>
      <p>전문가와 1:1 무료 상담 또는 무료체험을 신청하세요</p>
    </div>
    <div class="dual-inline-buttons">
      <a href="https://pf.kakao.com/_Cixlaxl/chat" target="_blank" rel="noopener noreferrer" class="dual-btn-kakao">
        💬 카카오톡 상담
      </a>
      <a href="https://naver.me/FGENm9ex" target="_blank" rel="noopener noreferrer" class="dual-btn-trial">
        ✨ 무료체험 신청
      </a>
    </div>
  </div>
</div>`;
}

// ============================================================
// HTML 템플릿 렌더링
// ============================================================
function renderFullHTML(frontMatter, contentHtml, path, visitorCount = 0) {
  const title = frontMatter.title || '과외를부탁해';
  const description = frontMatter.description || '초등학생부터 고등학생까지, 학습에 필요한 모든 정보를 한곳에서.';
  const featuredImage = frontMatter.featured_image || '';
  const categories = frontMatter.categories || [];
  const tags = frontMatter.tags || [];
  const date = frontMatter.date || '';

  // 읽기 시간 계산 (단어 수 / 200)
  const wordCount = contentHtml.replace(/<[^>]*>/g, '').length / 2; // 한글은 2바이트
  const readingTime = Math.max(1, Math.ceil(wordCount / 400));

  const dateFormatted = date ? formatKoreanDate(date) : '';
  const permalink = `https://edukoreaai.com${path}`;

  return `<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <link rel="preconnect" href="https://www.googletagmanager.com" crossorigin>
    <link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>

    <title>${escapeHtml(title)} | 과외를부탁해</title>
    <meta name="description" content="${escapeHtml(description)}">
    <meta name="author" content="과외를부탁해 편집팀">
    <link rel="canonical" href="${permalink}">

    <meta name="naver-site-verification" content="228c0da6bfc9eda328a78ce3a4417c8ff8630d59" />

    <meta property="og:title" content="${escapeHtml(title)} | 과외를부탁해">
    <meta property="og:description" content="${escapeHtml(description)}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="${permalink}">
    <meta property="og:site_name" content="과외를부탁해">
    <meta property="og:locale" content="ko_KR">
    ${featuredImage ? `<meta property="og:image" content="${featuredImage}">` : ''}
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">

    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="${escapeHtml(title)} | 과외를부탁해">
    <meta name="twitter:description" content="${escapeHtml(description)}">
    ${featuredImage ? `<meta name="twitter:image" content="${featuredImage}">` : ''}

    <script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": "${escapeHtml(title)}",
        "description": "${escapeHtml(description)}",
        ${featuredImage ? `"image": "${featuredImage}",` : ''}
        "author": {"@type": "Organization", "name": "과외를부탁해 편집팀"},
        "publisher": {"@type": "Organization", "name": "과외를부탁해"},
        "datePublished": "${date}",
        "mainEntityOfPage": {"@type": "WebPage", "@id": "${permalink}"}
    }
    </script>

    <script async src="https://www.googletagmanager.com/gtag/js?id=G-FP3W863XX4"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', 'G-FP3W863XX4');
    </script>

    <link rel="preload" as="style" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">

    <link rel="icon" type="image/x-icon" href="/images/favicon.ico">
    <link rel="manifest" href="/manifest.json">
    <meta name="theme-color" content="#667eea">

    <link rel="stylesheet" href="/css/style.css">
    <link rel="stylesheet" href="/css/viral.css">

    <style>
    ${getInlineStyles()}
    </style>
</head>
<body>
    ${getHeaderHTML(visitorCount)}

    <main>
        <div class="container">
            <article>
                <div class="article-meta">
                    ${categories.length ? `<div class="categories">${categories.map(c => `<span class="category-tag">${escapeHtml(c)}</span>`).join('')}</div>` : ''}
                </div>

                <h1 class="article-title">${escapeHtml(title)}</h1>

                <div class="article-info">
                    <span class="author">✍️ 과외를부탁해 편집팀</span>
                    <span class="date">📅 ${dateFormatted}</span>
                    <span class="reading-time">⏱️ ${readingTime}분</span>
                </div>

                ${featuredImage ? `
                <div class="featured-image">
                    <img src="${featuredImage}" alt="${escapeHtml(title)}" loading="lazy" width="1200" height="630" decoding="async">
                </div>
                ` : ''}

                <div class="article-content">
                    ${contentHtml}
                </div>

                <div class="cta-final-banner">
                    <h3>🎓 지금 바로 1:1 무료 체험수업 신청하세요!</h3>
                    <p>우리 아이와 잘 맞는 1:1맞춤 선생님과 체험수업 받아보시고 결정하세요!</p>
                    <div class="cta-final-buttons">
                        <a href="https://pf.kakao.com/_Cixlaxl/chat" target="_blank" rel="noopener noreferrer" class="btn-kakao">💬 카카오톡 상담하기</a>
                        <a href="https://naver.me/FGENm9ex" target="_blank" rel="noopener noreferrer" class="btn-trial">✨ 무료체험 신청하기</a>
                    </div>
                    <div class="cta-final-features">
                        <span>✅ 완전 무료</span>
                        <span>⚡ 빠른 답변</span>
                    </div>
                </div>

                ${tags.length ? `
                <div class="article-tags">
                    <strong>태그:</strong>
                    ${tags.map(t => `<a href="/tags/${encodeURIComponent(t)}" class="tag">#${escapeHtml(t)}</a>`).join('')}
                </div>
                ` : ''}
            </article>
        </div>
    </main>

    ${getFooterHTML()}

    <a href="https://pf.kakao.com/_Cixlaxl/chat" target="_blank" class="floating-kakao" rel="noopener noreferrer">
        <span class="kakao-icon">💬</span>
        <span class="kakao-text">무료상담</span>
    </a>

    <script src="/js/viral.js" defer></script>

    <script>
    (function() {
      const startTime = Date.now();
      window.addEventListener('beforeunload', function() {
        const duration = Math.floor((Date.now() - startTime) / 1000);
        navigator.sendBeacon('https://analytics-tracker.granadu0417.workers.dev/track', JSON.stringify({
          referrer: document.referrer || 'direct',
          page_url: window.location.href,
          session_duration: duration
        }));
      });
    })();
    </script>
</body>
</html>`;
}

function formatKoreanDate(dateStr) {
  try {
    const d = new Date(dateStr);
    return `${d.getFullYear()}년 ${String(d.getMonth() + 1).padStart(2, '0')}월 ${String(d.getDate()).padStart(2, '0')}일`;
  } catch {
    return dateStr;
  }
}

function escapeHtml(str) {
  if (!str) return '';
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function getHeaderHTML(visitorCount = 0) {
  // 숫자 포맷팅 (천 단위 콤마)
  const formattedCount = visitorCount.toLocaleString('ko-KR');

  return `
<header class="site-header">
    <div class="wide-container">
        <div class="header-content">
            <div class="header-top">
                <div class="site-logo">
                    <a href="/">
                        <img src="/images/logo.svg" alt="과외를부탁해 로고" class="logo-image" loading="eager">
                        <span>과외를부탁해</span>
                    </a>
                </div>
                <button class="mobile-menu-toggle" aria-label="메뉴 열기">
                    <span></span><span></span><span></span>
                </button>
            </div>
            <div class="header-actions">
                <a href="/search/" class="search-btn" aria-label="검색">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/>
                    </svg>
                </a>
                <div class="usage-counter">
                    <div class="label">누적 방문자</div>
                    <div class="count"><span id="usageCount">${formattedCount}</span>명</div>
                </div>
            </div>
            <nav class="main-nav">
                <ul>
                    <li class="has-dropdown">
                        <a href="#">지역별 과외</a>
                        <ul class="dropdown">
                            <li><a href="/seoul/">서울</a></li>
                            <li><a href="/gyeonggi/">경기</a></li>
                            <li><a href="/busan/">부산</a></li>
                            <li><a href="/incheon/">인천</a></li>
                            <li><a href="/daegu/">대구</a></li>
                            <li><a href="/cities/">기타 지역</a></li>
                        </ul>
                    </li>
                    <li class="has-dropdown">
                        <a href="#">학습 가이드</a>
                        <ul class="dropdown">
                            <li><a href="/elementary/">초등학생</a></li>
                            <li><a href="/middle/">중학생</a></li>
                            <li><a href="/high/">고등학생</a></li>
                        </ul>
                    </li>
                    <li class="has-dropdown">
                        <a href="#">과목별</a>
                        <ul class="dropdown">
                            <li><a href="/subjects/korean/">국어</a></li>
                            <li><a href="/subjects/english/">영어</a></li>
                            <li><a href="/subjects/math/">수학</a></li>
                            <li><a href="/subjects/science/">과학</a></li>
                            <li><a href="/subjects/social/">사회</a></li>
                        </ul>
                    </li>
                    <li><a href="/tutoring/">학습플랜</a></li>
                    <li><a href="/exam/">시험 대비</a></li>
                    <li><a href="/consultation/">무료 상담</a></li>
                </ul>
            </nav>
        </div>
    </div>
</header>
<script>
(function() {
    const menuToggle = document.querySelector('.mobile-menu-toggle');
    const mainNav = document.querySelector('.main-nav');
    if (menuToggle) {
        menuToggle.addEventListener('click', function() {
            this.classList.toggle('active');
            mainNav.classList.toggle('active');
            document.body.classList.toggle('menu-open');
        });
    }
})();
</script>`;
}

function getFooterHTML() {
  return `
<footer class="site-footer">
    <div class="wide-container">
        <div class="footer-content">
            <div class="footer-info">
                <h4>📚 과외를부탁해</h4>
                <p>초등학생부터 고등학생까지<br>학습에 필요한 모든 정보를 한곳에서</p>
            </div>
            <div class="footer-disclaimer">
                <p><strong>⚠️ 안내사항</strong></p>
                <p>본 사이트의 모든 콘텐츠는 정보 제공 목적이며, 학습 효과를 보장하지 않습니다.</p>
            </div>
        </div>
        <div class="footer-bottom">
            <p>&copy; 2025 과외를부탁해. All rights reserved.</p>
        </div>
    </div>
</footer>`;
}

function getInlineStyles() {
  return `
.article-meta { margin-bottom: 1rem; }
.categories { display: flex; gap: 0.5rem; }
.category-tag { background: #4a90e2; color: white; padding: 0.3rem 0.8rem; border-radius: 4px; font-size: 0.8125rem; font-weight: 600; }
.article-title { font-size: 2.5rem; line-height: 1.3; margin-bottom: 1rem; color: #2c3e50; }
.article-info { display: flex; gap: 1.5rem; padding-bottom: 2rem; border-bottom: 1px solid #e1e8ed; margin-bottom: 3rem; color: #95a5a6; font-size: 0.9375rem; }
.article-content { font-size: 1.0625rem; line-height: 1.9; }
.featured-image { margin: 2rem 0 3rem 0; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
.featured-image img { width: 100%; height: auto; display: block; }
.article-tags { margin-top: 3rem; padding-top: 2rem; border-top: 1px solid #e1e8ed; }
.tag { display: inline-block; margin: 0 0.5rem; color: #4a90e2; font-size: 0.9375rem; }

.cta-final-banner { text-align: center; padding: 52px 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 20px; box-shadow: 0 16px 48px rgba(102, 126, 234, 0.3); margin: 40px 0; }
.cta-final-banner h3 { color: white; font-size: 28px; font-weight: 800; margin: 0 0 12px; line-height: 1.4; }
.cta-final-banner p { color: rgba(255, 255, 255, 0.9); font-size: 16px; margin: 0 0 32px; font-weight: 500; }
.cta-final-buttons { display: flex; justify-content: center; gap: 16px; margin-bottom: 32px; flex-wrap: wrap; }
.cta-final-banner .btn-kakao, .cta-final-banner .btn-trial { padding: 18px 40px; text-decoration: none; border-radius: 50px; font-weight: 800; font-size: 18px; transition: all 0.3s ease; display: inline-block; }
.cta-final-banner .btn-kakao { background: linear-gradient(135deg, #FEE500 0%, #FFD700 100%); color: #3C1E1E; box-shadow: 0 8px 24px rgba(254, 229, 0, 0.4); }
.cta-final-banner .btn-trial { background: white; color: #667eea; box-shadow: 0 8px 24px rgba(255, 255, 255, 0.3); }
.cta-final-features { display: flex; justify-content: center; gap: 28px; }
.cta-final-features span { color: rgba(255, 255, 255, 0.95); font-size: 15px; font-weight: 600; }

.dual-final-box { text-align: center; padding: 52px 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 20px; box-shadow: 0 16px 48px rgba(102, 126, 234, 0.3); margin: 56px 0 40px; }
.dual-final-box h3 { color: white; font-size: 28px; font-weight: 800; margin: 0 0 12px; }
.dual-final-desc { color: rgba(255, 255, 255, 0.9); font-size: 16px; margin: 0 0 32px; }
.dual-final-buttons { display: flex; justify-content: center; gap: 16px; margin-bottom: 32px; flex-wrap: wrap; }
.dual-btn-final-kakao, .dual-btn-final-trial { padding: 18px 40px; text-decoration: none; border-radius: 50px; font-weight: 800; font-size: 18px; transition: all 0.3s ease; }
.dual-btn-final-kakao { background: linear-gradient(135deg, #FEE500 0%, #FFD700 100%); color: #3C1E1E; }
.dual-btn-final-trial { background: white; color: #667eea; }
.dual-final-features { display: flex; justify-content: center; gap: 28px; }
.feature-item { display: flex; align-items: center; gap: 8px; color: rgba(255, 255, 255, 0.95); font-size: 15px; font-weight: 600; }

.dual-inline-box { display: flex; align-items: center; gap: 20px; padding: 28px 32px; background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%); border-radius: 16px; border: 2px solid #e9ecef; margin: 48px 0; }
.dual-inline-icon { font-size: 42px; }
.dual-inline-content h3 { margin: 0 0 6px; font-size: 19px; font-weight: 700; }
.dual-inline-content p { margin: 0; font-size: 14px; color: #6c757d; }
.dual-inline-buttons { display: flex; gap: 12px; }
.dual-btn-kakao, .dual-btn-trial { padding: 12px 24px; text-decoration: none; border-radius: 25px; font-weight: 700; font-size: 15px; }
.dual-btn-kakao { background: linear-gradient(135deg, #FEE500 0%, #FFD700 100%); color: #3C1E1E; }
.dual-btn-trial { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }

.floating-kakao { position: fixed; bottom: 20px; right: 20px; background: #FEE500; color: #3C1E1E; padding: 15px 20px; border-radius: 50px; text-decoration: none; font-weight: 700; box-shadow: 0 4px 12px rgba(0,0,0,0.15); z-index: 1000; display: flex; align-items: center; gap: 8px; }
.floating-kakao:hover { transform: translateY(-3px); box-shadow: 0 6px 20px rgba(0,0,0,0.2); }

@media (max-width: 768px) {
  .article-title { font-size: 1.6rem; }
  .article-info { gap: 1rem; font-size: 0.85rem; }
  .cta-final-banner { padding: 40px 28px; }
  .cta-final-banner h3 { font-size: 24px; }
  .cta-final-buttons { flex-direction: column; align-items: center; }
  .cta-final-banner .btn-kakao, .cta-final-banner .btn-trial { width: 100%; max-width: 300px; }
  .dual-inline-box { flex-wrap: wrap; justify-content: center; text-align: center; }
  .dual-inline-buttons { width: 100%; justify-content: center; flex-direction: column; }
}
`;
}

// ============================================================
// 404 페이지
// ============================================================
function render404HTML(visitorCount = 0) {
  return `<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>페이지를 찾을 수 없습니다 | 과외를부탁해</title>
    <link rel="stylesheet" href="/css/style.css">
    <style>
    .error-page { text-align: center; padding: 100px 20px; }
    .error-page h1 { font-size: 120px; color: #667eea; margin: 0; }
    .error-page h2 { font-size: 24px; margin: 20px 0; }
    .error-page p { color: #666; margin-bottom: 30px; }
    .error-page a { display: inline-block; padding: 15px 30px; background: #667eea; color: white; text-decoration: none; border-radius: 8px; }
    </style>
</head>
<body>
    ${getHeaderHTML(visitorCount)}
    <main>
        <div class="error-page">
            <h1>404</h1>
            <h2>페이지를 찾을 수 없습니다</h2>
            <p>요청하신 페이지가 존재하지 않거나 이동되었습니다.</p>
            <a href="/">홈으로 돌아가기</a>
        </div>
    </main>
    ${getFooterHTML()}
</body>
</html>`;
}

// ============================================================
// Worker 메인 핸들러
// ============================================================
const PAGES_ORIGIN = 'https://3842efa4.edu-guide.pages.dev';
const VISITOR_COUNT_KEY = '__visitor_count__';

// 방문자 카운터 증가 및 조회
async function incrementVisitorCount(env) {
  try {
    // 현재 값 조회
    const currentValue = await env.KV.get(VISITOR_COUNT_KEY, 'text');
    let count = currentValue ? parseInt(currentValue, 10) : 0;

    // 카운터 증가
    count += 1;

    // 새 값 저장 (비동기로 처리하여 응답 속도에 영향 없도록)
    await env.KV.put(VISITOR_COUNT_KEY, count.toString());

    return count;
  } catch (e) {
    console.error('Visitor count error:', e);
    return 0;
  }
}

// 방문자 카운터 조회만 (증가 없이)
async function getVisitorCount(env) {
  try {
    const currentValue = await env.KV.get(VISITOR_COUNT_KEY, 'text');
    return currentValue ? parseInt(currentValue, 10) : 0;
  } catch (e) {
    return 0;
  }
}

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    let path = decodeURIComponent(url.pathname);

    // 정적 파일: KV에서 먼저 찾고, 없으면 Pages 폴백 (카운터 증가 안 함)
    if (isStaticFile(path)) {
      const kvContent = await env.KV.get(path, 'text');
      if (kvContent !== null) {
        const contentType = getContentType(path);
        return new Response(kvContent, {
          headers: {
            'Content-Type': contentType,
            'Cache-Control': 'public, max-age=86400',
            'X-Content-Source': 'KV-Static'
          }
        });
      }
      // KV에 없으면 Pages로 폴백
      return proxyToPages(path);
    }

    // 경로 정규화
    if (!path.endsWith('/') && !path.includes('.')) {
      return Response.redirect(`${url.origin}${path}/`, 301);
    }

    // 301 리다이렉트: /high/ 지역별 콘텐츠 → /seoul/
    // 예: /high/dobong-banghak1-high-math/ → /seoul/dobong/banghak1-high-math/
    const highRegionalMatch = path.match(/^\/high\/([a-z]+)-(.+)-high-(math|english)\/$/);
    if (highRegionalMatch) {
      const district = highRegionalMatch[1];
      const neighborhood = highRegionalMatch[2];
      const subject = highRegionalMatch[3];
      const newPath = `/seoul/${district}/${neighborhood}-high-${subject}/`;
      return Response.redirect(`${url.origin}${newPath}`, 301);
    }

    // 301 리다이렉트: /middle/ 지역별 콘텐츠 → /seoul/
    // 예: /middle/gangnam-apgujeong-middle-english/ → /seoul/gangnam/apgujeong-middle-english/
    const middleRegionalMatch = path.match(/^\/middle\/([a-z]+)-(.+)-middle-(math|english)\/$/);
    if (middleRegionalMatch) {
      const district = middleRegionalMatch[1];
      const neighborhood = middleRegionalMatch[2];
      const subject = middleRegionalMatch[3];
      const newPath = `/seoul/${district}/${neighborhood}-middle-${subject}/`;
      return Response.redirect(`${url.origin}${newPath}`, 301);
    }

    // 방문자 카운터 증가 (HTML 페이지 요청에만)
    // waitUntil을 사용하여 응답 속도에 영향 없이 처리
    let visitorCount = 0;
    try {
      // 카운터 증가는 백그라운드에서 처리
      const countPromise = incrementVisitorCount(env);
      ctx.waitUntil(countPromise.then(() => {}));

      // 현재 값은 바로 조회
      visitorCount = await getVisitorCount(env);
    } catch (e) {
      console.error('Counter error:', e);
    }

    // KV 키 생성
    let kvKey = path;
    if (kvKey === '/') {
      kvKey = '/index';
    } else if (kvKey.endsWith('/')) {
      kvKey = kvKey.slice(0, -1) + '/index';
    }

    // KV에서 .md 콘텐츠 가져오기
    const mdContent = await env.KV.get(kvKey, 'text');

    if (mdContent) {
      const trimmedContent = mdContent.trim().toLowerCase();

      // KV에 저장된 콘텐츠가 이미 HTML인 경우 (기존 Hugo 빌드 데이터 또는 메인 페이지)
      // 직접 반환하되, 카운터 값은 동적으로 주입
      if (trimmedContent.startsWith('<!doctype') || trimmedContent.startsWith('<html')) {
        // 카운터 값을 HTML에 주입 (id="usageCount" 또는 id="userCount" 찾아서 교체)
        // 따옴표 있는 경우(id="usageCount")와 없는 경우(id=usageCount) 모두 매칭
        const formattedCount = visitorCount.toLocaleString('ko-KR');
        let modifiedHtml = mdContent
          .replace(/<span id="?usageCount"?>[^<]*<\/span>/gi, `<span id="usageCount">${formattedCount}</span>`)
          .replace(/<span id="?userCount"?>[^<]*<\/span>/gi, `<span id="usageCount">${formattedCount}</span>`);

        return new Response(modifiedHtml, {
          status: 200,
          headers: {
            'Content-Type': 'text/html; charset=utf-8',
            'Cache-Control': 'public, max-age=60',
            'X-Content-Source': 'KV-HTML',
            'X-Visitor-Count': visitorCount.toString()
          }
        });
      }

      // Markdown 콘텐츠 → HTML 변환
      const { frontMatter, body } = parseYamlFrontMatter(mdContent);
      let htmlContent = markdownToHtml(body);
      htmlContent = processShortcodes(htmlContent);
      const fullHtml = renderFullHTML(frontMatter, htmlContent, path, visitorCount);

      return new Response(fullHtml, {
        status: 200,
        headers: {
          'Content-Type': 'text/html; charset=utf-8',
          'Cache-Control': 'public, max-age=60',
          'X-Content-Source': 'KV-MD',
          'X-Visitor-Count': visitorCount.toString()
        }
      });
    }

    // 콘텐츠 없으면 Pages에서 시도 (기존 HTML)
    const pagesResponse = await fetch(`${PAGES_ORIGIN}${path}`);
    if (pagesResponse.ok) {
      const html = await pagesResponse.text();
      return new Response(html, {
        status: 200,
        headers: {
          'Content-Type': 'text/html; charset=utf-8',
          'Cache-Control': 'public, max-age=3600',
          'X-Content-Source': 'Pages'
        }
      });
    }

    // 404
    return new Response(render404HTML(visitorCount), {
      status: 404,
      headers: {
        'Content-Type': 'text/html; charset=utf-8',
        'X-Visitor-Count': visitorCount.toString()
      }
    });
  }
};

function isStaticFile(path) {
  const staticExtensions = [
    '.css', '.js', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico',
    '.woff', '.woff2', '.ttf', '.eot', '.webp', '.json', '.xml',
    '.txt', '.pdf', '.mp4', '.webm', '.mp3'
  ];
  return staticExtensions.some(ext => path.endsWith(ext));
}

async function proxyToPages(path) {
  const response = await fetch(`${PAGES_ORIGIN}${path}`);

  const contentType = getContentType(path);
  const headers = new Headers(response.headers);
  headers.set('Content-Type', contentType);
  headers.set('Cache-Control', 'public, max-age=86400');

  return new Response(response.body, {
    status: response.status,
    headers
  });
}

function getContentType(path) {
  const ext = path.split('.').pop().toLowerCase();
  const types = {
    'html': 'text/html; charset=utf-8',
    'css': 'text/css; charset=utf-8',
    'js': 'application/javascript; charset=utf-8',
    'json': 'application/json; charset=utf-8',
    'xml': 'application/xml; charset=utf-8',
    'png': 'image/png',
    'jpg': 'image/jpeg',
    'jpeg': 'image/jpeg',
    'gif': 'image/gif',
    'svg': 'image/svg+xml',
    'ico': 'image/x-icon',
    'webp': 'image/webp',
    'woff': 'font/woff',
    'woff2': 'font/woff2',
    'ttf': 'font/ttf',
    'pdf': 'application/pdf',
    'mp4': 'video/mp4',
    'webm': 'video/webm',
    'mp3': 'audio/mpeg'
  };
  return types[ext] || 'application/octet-stream';
}
