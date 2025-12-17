#!/usr/bin/env node
/**
 * 사이트맵 분할 스크립트
 * 12,576개 URL을 5,000개씩 분할하여 sitemap-index.xml 생성
 */

const fs = require('fs');
const path = require('path');

const SITEMAP_PATH = './public/sitemap.xml';
const OUTPUT_DIR = './public';
const URLS_PER_FILE = 5000;
const SITE_URL = 'https://edukoreaai.com';

// 사이트맵 읽기
const sitemapContent = fs.readFileSync(SITEMAP_PATH, 'utf-8');

// URL 추출 (모든 <url>...</url> 블록)
const urlRegex = /<url>[\s\S]*?<\/url>/g;
const urls = sitemapContent.match(urlRegex) || [];

console.log(`총 URL 수: ${urls.length}`);

// 분할 파일 수 계산
const numFiles = Math.ceil(urls.length / URLS_PER_FILE);
console.log(`분할 파일 수: ${numFiles}`);

const sitemapFiles = [];

for (let i = 0; i < numFiles; i++) {
  const start = i * URLS_PER_FILE;
  const end = Math.min(start + URLS_PER_FILE, urls.length);
  const chunk = urls.slice(start, end);

  const filename = `sitemap-${i + 1}.xml`;
  const filepath = path.join(OUTPUT_DIR, filename);

  const content = `<?xml version="1.0" encoding="utf-8" standalone="yes"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">
${chunk.join('\n')}
</urlset>`;

  fs.writeFileSync(filepath, content);
  console.log(`✓ ${filename}: ${chunk.length}개 URL (${start + 1} ~ ${end})`);

  sitemapFiles.push({
    filename,
    count: chunk.length
  });
}

// sitemap-index.xml 생성
const today = new Date().toISOString().split('T')[0];
const indexContent = `<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${sitemapFiles.map(f => `  <sitemap>
    <loc>${SITE_URL}/${f.filename}</loc>
    <lastmod>${today}</lastmod>
  </sitemap>`).join('\n')}
</sitemapindex>`;

const indexPath = path.join(OUTPUT_DIR, 'sitemap-index.xml');
fs.writeFileSync(indexPath, indexContent);
console.log(`\n✓ sitemap-index.xml 생성 완료`);

// 요약 출력
console.log('\n=== 분할 결과 ===');
console.log(`총 URL: ${urls.length}개`);
console.log(`분할 파일: ${numFiles}개`);
sitemapFiles.forEach(f => {
  console.log(`  - ${f.filename}: ${f.count}개`);
});
console.log(`\n📌 Google Search Console에서 제출할 URL:`);
console.log(`   ${SITE_URL}/sitemap-index.xml`);
