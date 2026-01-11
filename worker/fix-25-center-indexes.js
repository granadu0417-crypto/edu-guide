const fs = require('fs');

// 25개 수정 대상 센터
const fixedCenterKeys = [
  "eunpyeong", "cheongra", "rst", "mjd", "bd2", "pungsan", "jj2", "jg", "shd", "bg",
  "d2", "ds2", "gj", "sch", "taepyeong", "jj3", "bs3", "gp", "pst", "dgj",
  "ds3", "eunpyeong2", "eunpyeong3", "bnj", "mg"
];

// 센터 설정 로드
const configs = JSON.parse(fs.readFileSync('./generated-center-configs.json', 'utf-8'));

// 51개 아티클 제목 템플릿
const articleTemplates = [
  // 수학 (1-17)
  { id: 1, subject: '수학', title: '{district} 중등 수학학원' },
  { id: 2, subject: '수학', title: '{landmark} 고등 수학학원' },
  { id: 3, subject: '수학', title: '{midSchool} 인근 중1 수학학원' },
  { id: 4, subject: '수학', title: '{location} 중2 수학학원' },
  { id: 5, subject: '수학', title: '{district} 중3 수학학원' },
  { id: 6, subject: '수학', title: '{landmark} 고1 수학학원' },
  { id: 7, subject: '수학', title: '{highSchool} 인근 고2 수학학원' },
  { id: 8, subject: '수학', title: '{location} 고3 수학학원' },
  { id: 9, subject: '수학', title: '{district} 중등 수학 개념학원' },
  { id: 10, subject: '수학', title: '{landmark} 고등 수학 개념학원' },
  { id: 11, subject: '수학', title: '{midSchool} 인근 수학 기초반학원' },
  { id: 12, subject: '수학', title: '{location} 수능 수학학원' },
  { id: 13, subject: '수학', title: '{district} 내신 수학학원' },
  { id: 14, subject: '수학', title: '{landmark} 수학 심화반학원' },
  { id: 15, subject: '수학', title: '{midSchool} 인근 수학 코칭학원' },
  { id: 16, subject: '수학', title: '{location} 예비중 수학학원' },
  { id: 17, subject: '수학', title: '{district} 예비고 수학학원' },
  // 영어 (18-34)
  { id: 18, subject: '영어', title: '{landmark} 중등 영어학원' },
  { id: 19, subject: '영어', title: '{highSchool} 인근 고등 영어학원' },
  { id: 20, subject: '영어', title: '{location} 중1 영어학원' },
  { id: 21, subject: '영어', title: '{district} 중2 영어학원' },
  { id: 22, subject: '영어', title: '{landmark} 중3 영어학원' },
  { id: 23, subject: '영어', title: '{highSchool} 인근 고1 영어학원' },
  { id: 24, subject: '영어', title: '{location} 고2 영어학원' },
  { id: 25, subject: '영어', title: '{district} 고3 영어학원' },
  { id: 26, subject: '영어', title: '{landmark} 영어 문법학원' },
  { id: 27, subject: '영어', title: '{highSchool} 인근 영어 독해학원' },
  { id: 28, subject: '영어', title: '{location} 영어 기초반학원' },
  { id: 29, subject: '영어', title: '{district} 수능 영어학원' },
  { id: 30, subject: '영어', title: '{landmark} 내신 영어학원' },
  { id: 31, subject: '영어', title: '{highSchool} 인근 영어 심화반학원' },
  { id: 32, subject: '영어', title: '{location} 영어 코칭학원' },
  { id: 33, subject: '영어', title: '{district} 예비중 영어학원' },
  { id: 34, subject: '영어', title: '{landmark} 예비고 영어학원' },
  // 종합 (35-51)
  { id: 35, subject: '종합', title: '{midSchool} 인근 중등 전과목학원' },
  { id: 36, subject: '종합', title: '{location} 고등 전과목학원' },
  { id: 37, subject: '종합', title: '{district} 중1 종합반학원' },
  { id: 38, subject: '종합', title: '{landmark} 중2 종합반학원' },
  { id: 39, subject: '종합', title: '{midSchool} 인근 중3 종합반학원' },
  { id: 40, subject: '종합', title: '{location} 고1 종합반학원' },
  { id: 41, subject: '종합', title: '{district} 초등학원' },
  { id: 42, subject: '종합', title: '{landmark} 중등 내신관리학원' },
  { id: 43, subject: '종합', title: '{highSchool} 인근 고등 내신관리학원' },
  { id: 44, subject: '종합', title: '{location} 자기주도학습학원' },
  { id: 45, subject: '종합', title: '{district} 학습코칭학원' },
  { id: 46, subject: '종합', title: '{landmark} 1:1 맞춤수업학원' },
  { id: 47, subject: '종합', title: '{midSchool} 인근 중등 학습관리학원' },
  { id: 48, subject: '종합', title: '{location} 고등 학습관리학원' },
  { id: 49, subject: '종합', title: '{district} 방학특강학원' },
  { id: 50, subject: '종합', title: '{landmark} 예비중 종합학원' },
  { id: 51, subject: '종합', title: '{highSchool} 인근 내신관리 전과목학원' }
];

// 수업료 테이블 (지역별)
const priceTableA = `| 학년 | 주3회 | 주4회 | 주5회 |
|------|-------|-------|-------|
| 초등 | 220,000원 | 286,000원 | 352,000원 |
| 중등 | 239,000원 | 310,000원 | 382,000원 |
| 고등 | 275,000원 | 358,000원 | 440,000원 |`;

const priceTableB = `| 학년 | 주3회 | 주4회 | 주5회 |
|------|-------|-------|-------|
| 초등 | 198,000원 | 257,000원 | 316,000원 |
| 중등 | 215,000원 | 279,000원 | 343,000원 |
| 고등 | 248,000원 | 322,000원 | 396,000원 |`;

function generateArticleTitle(template, config) {
  const landmark = config.landmarks?.[0] || `${config.location} 인근`;
  const highSchool = config.schools?.high?.[0] || `${config.district} 고등학교`;
  const midSchool = config.schools?.mid?.[0] || `${config.district} 중학교`;

  return template.title
    .replace('{district}', config.district)
    .replace('{location}', config.location)
    .replace('{landmark}', landmark)
    .replace('{highSchool}', highSchool)
    .replace('{midSchool}', midSchool);
}

function generateIndexPage(centerKey, config) {
  const today = new Date().toISOString().split('T')[0];
  const priceTable = config.priceRegion === 'A' ? priceTableA : priceTableB;

  const highSchools = config.schools?.high || [];
  const midSchools = config.schools?.mid || [];
  const landmark = config.landmarks?.[0] || `${config.location} 인근`;

  // 학교 목록 생성
  const schoolList = [
    ...highSchools.slice(0, 2).map(s => `- ${s} (도보 거리)`),
    ...midSchools.slice(0, 2).map(s => `- ${s} (도보 거리)`)
  ].join('\n');

  // 아티클 카드 생성
  const mathArticles = articleTemplates.filter(t => t.subject === '수학')
    .map(t => `<div class="article-card"><a href="/coaching/${centerKey}/${t.id}/">${generateArticleTitle(t, config)}</a></div>`)
    .join('\n');

  const engArticles = articleTemplates.filter(t => t.subject === '영어')
    .map(t => `<div class="article-card"><a href="/coaching/${centerKey}/${t.id}/">${generateArticleTitle(t, config)}</a></div>`)
    .join('\n');

  const generalArticles = articleTemplates.filter(t => t.subject === '종합')
    .map(t => `<div class="article-card"><a href="/coaching/${centerKey}/${t.id}/">${generateArticleTitle(t, config)}</a></div>`)
    .join('\n');

  const content = `---
title: "${config.name} | 와와학습코칭센터 ${config.city} ${config.district}"
date: ${today}
categories:
  - 학습코칭
description: "${config.city} ${config.district} 와와학습코칭센터 ${config.name}. ${config.location} 도보 거리. ${highSchools[0] || ''}, ${midSchools[0] || ''} 인근. 체계적인 맞춤지도와 전과목 통합 케어."
tags:
  - 와와학습코칭센터
  - ${config.city}학원
  - ${config.district}학원
  - ${config.location}
  - ${midSchools[0] || config.district + '중'}
  - ${highSchools[0] || config.district + '고'}
featured_image: "/images/wawalong.jpg"
---

# 와와학습코칭센터 ${config.name}

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>센터 정보</strong><br>
<br>
🚇 ${config.location} 도보 거리<br>
📝 등록번호: ${config.registration}
</div>

## ${config.name} 주변 학교

**걸어서 갈 수 있는 거리의 학교들**

${schoolList}

---

## ${config.name} 학습 가이드

${config.name}에서 제공하는 **지역 맞춤형 학습 콘텐츠**입니다. ${config.location} 인근 학생들을 위한 과목별, 학년별 상세 가이드를 확인하세요.

<style>
.article-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 15px;
  margin: 20px 0;
}
.article-card {
  background: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  padding: 15px;
  transition: all 0.3s ease;
}
.article-card:hover {
  background: #e9ecef;
  border-color: #4A90E2;
  box-shadow: 0 4px 8px rgba(74, 144, 226, 0.2);
}
.article-card a {
  text-decoration: none;
  color: #212529;
  font-weight: 500;
  display: block;
}
.article-card a:hover {
  color: #4A90E2;
}
.subject-title {
  font-size: 1.1em;
  font-weight: 600;
  color: #495057;
  margin: 25px 0 15px 0;
  padding-bottom: 8px;
  border-bottom: 2px solid #dee2e6;
}
</style>

<div class="subject-title">📐 수학</div>
<div class="article-grid">
${mathArticles}
</div>

<div class="subject-title">📚 영어</div>
<div class="article-grid">
${engArticles}
</div>

<div class="subject-title">📝 종합</div>
<div class="article-grid">
${generalArticles}
</div>

---

## 수업료 안내

${priceTable}

상담 후 학생의 현재 수준과 목표에 맞는 수업 횟수를 결정합니다.

---

## 자주 묻는 질문

**Q. 상담은 어떻게 받을 수 있나요?**

방문 상담을 권장드립니다. ${config.location} 도보 거리에 위치해 있습니다. 학생과 함께 방문해주시면 학생의 현재 상태를 파악하고 맞춤형 학습 계획을 세워드립니다.

**Q. 수업 시간은 어떻게 되나요?**

학생과 협의하여 결정합니다. 학교 일정, 학원 일정을 고려하여 최적의 시간을 찾아드립니다. 평일 오후와 저녁, 주말 오전과 오후 수업이 가능합니다.

**Q. 시험 기간에는 어떻게 수업하나요?**

시험 기간에는 집중 대비 수업으로 전환합니다. 학교별 시험 범위에 맞춰 기출문제 분석, 예상문제 풀이, 오답 정리를 진행합니다.

---

## 인근 아파트

${landmark} 등 인근 아파트에서 많은 학생들이 다니고 있습니다.

---

[← 와와학습코칭센터 전체 센터 보기](/coaching/)
`;

  return content;
}

// 메인 실행
console.log('=== 25개 센터 인덱스 페이지 재생성 ===\n');

const kvData = [];

for (const centerKey of fixedCenterKeys) {
  const config = configs[centerKey];
  if (!config) {
    console.log(`⚠️ ${centerKey}: 설정 없음, 건너뜀`);
    continue;
  }

  const content = generateIndexPage(centerKey, config);

  kvData.push({
    key: `/coaching/${centerKey}/index`,
    value: content
  });

  console.log(`✅ ${centerKey} (${config.name}): 인덱스 페이지 생성`);
}

// KV JSON 저장
fs.writeFileSync('./fix-25-center-indexes-kv.json', JSON.stringify(kvData, null, 2));
console.log(`\n📦 KV 파일 생성: fix-25-center-indexes-kv.json (${kvData.length}개)`);
console.log('\n배포 명령어:');
console.log('npx wrangler kv bulk put "fix-25-center-indexes-kv.json" --namespace-id 725aefb7b1c64c6c90d2cf4daf061bf3 --remote');
