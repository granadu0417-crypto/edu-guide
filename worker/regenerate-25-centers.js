const fs = require('fs');

// ============================================
// 25개 센터 "과외" 제거 재생성 스크립트
// 목적: 등록번호 수정 시 사용한 스크립트에서 "과외" 키워드가 남아있었음
// 해결: 메인 스크립트 로직으로 25개 센터만 재생성
// ============================================

// 센터 해시 함수
function getCenterHash(centerName) {
  return centerName.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0);
}

// 표현 풀 파싱 (메인 스크립트와 동일)
function parseExpressionPool(filePath) {
  const content = fs.readFileSync(filePath, 'utf-8');
  const pool = {
    openings: { math: [], english: [], korean: [], general: [] },
    boxes: { diag: [], method: [], exam: [], manage: [], hw: [], wrong: [], study: [], grade: [] },
    h2Titles: { import: [], school: [], method: [], grade: [], fee: [], center: [], faq: [], habit: [], test: [], parent: [] },
    faq: { questions: {}, answers: {} },
    closings: { math: [], english: [] },
    strategies: {
      math: { mid1: [], mid2: [], mid3: [], midGen: [], high1: [], high2: [], high3: [], highGen: [] },
      english: { mid1: [], mid2: [], mid3: [], midGen: [], high1: [], high2: [], high3: [], highGen: [] }
    },
    methods: { concept: [], solve: [], wrong: [], time: [], memo: [] },
    schools: { gen: [], mid: [] },
    centers: [],
    synonyms: []
  };

  // 서두 문장 파싱
  const mathOpenings = content.match(/\[M-OPEN-\d+\]\s*[^\n]+/g) || [];
  pool.openings.math = mathOpenings.map(function(e) { return e.replace(/\[M-OPEN-\d+\]\s*/, '').trim(); });

  const engOpenings = content.match(/\[E-OPEN-\d+\]\s*[^\n]+/g) || [];
  pool.openings.english = engOpenings.map(function(e) { return e.replace(/\[E-OPEN-\d+\]\s*/, '').trim(); });

  const korOpenings = content.match(/\[K-OPEN-\d+\]\s*[^\n]+/g) || [];
  pool.openings.korean = korOpenings.map(function(e) { return e.replace(/\[K-OPEN-\d+\]\s*/, '').trim(); });

  pool.openings.general = [].concat(pool.openings.math, pool.openings.english, pool.openings.korean);

  // 아이보리 박스 파싱
  var boxPatterns = [
    { key: 'diag', pattern: /\[BOX-DIAG-\d+\]\s*[^\n]+/g },
    { key: 'method', pattern: /\[BOX-METHOD-\d+\]\s*[^\n]+/g },
    { key: 'exam', pattern: /\[BOX-EXAM-\d+\]\s*[^\n]+/g },
    { key: 'manage', pattern: /\[BOX-MANAGE-\d+\]\s*[^\n]+/g },
    { key: 'hw', pattern: /\[BOX-HW-\d+\]\s*[^\n]+/g },
    { key: 'wrong', pattern: /\[BOX-WRONG-\d+\]\s*[^\n]+/g },
    { key: 'study', pattern: /\[BOX-STUDY-\d+\]\s*[^\n]+/g },
    { key: 'grade', pattern: /\[BOX-GRADE-\d+\]\s*[^\n]+/g }
  ];

  boxPatterns.forEach(function(item) {
    var matches = content.match(item.pattern) || [];
    pool.boxes[item.key] = matches.map(function(e) { return e.replace(/\[BOX-[A-Z]+-\d+\]\s*/, '').trim(); });
  });

  // H2 제목 파싱
  var h2Categories = ['IMPORT', 'SCHOOL', 'METHOD', 'GRADE', 'FEE', 'CENTER', 'FAQ', 'HABIT', 'TEST', 'PARENT'];
  h2Categories.forEach(function(cat) {
    var catKey = cat.toLowerCase();
    var pattern = new RegExp('\\[H2-' + cat + '-\\d+\\]\\s*[^\\n]+', 'g');
    var matches = content.match(pattern) || [];
    pool.h2Titles[catKey] = matches.map(function(e) { return e.replace(/\[H2-[A-Z]+-\d+\]\s*/, '').trim(); });
  });

  // FAQ 파싱
  var faqCategories = ['BASIC', 'PRIORITY', 'TIME', 'HW', 'ENG', 'MATH', 'ALL', 'STAGNANT', 'COMPARE', 'CONSULT'];
  faqCategories.forEach(function(cat) {
    var catKey = cat.toLowerCase();
    var qPattern = new RegExp('\\[FAQ-Q-' + cat + '-\\d+\\]\\s*Q\\.\\s*([^\\n]+)', 'g');
    var qMatch;
    pool.faq.questions[catKey] = [];
    while ((qMatch = qPattern.exec(content)) !== null) {
      pool.faq.questions[catKey].push(qMatch[1].trim());
    }
    var aPattern = new RegExp('\\[FAQ-A-' + cat + '-\\d+\\]\\s*A\\.\\s*([^\\n]+)', 'g');
    var aMatch;
    pool.faq.answers[catKey] = [];
    while ((aMatch = aPattern.exec(content)) !== null) {
      pool.faq.answers[catKey].push(aMatch[1].trim());
    }
  });

  // 마무리 문장 파싱
  var mathCloseMatches = content.match(/\[CLOSE-M-\d+\]\s*[^\n]+/g) || [];
  pool.closings.math = mathCloseMatches.map(function(e) { return e.replace(/\[CLOSE-M-\d+\]\s*/, '').trim(); });

  var engCloseMatches = content.match(/\[CLOSE-E-\d+\]\s*[^\n]+/g) || [];
  pool.closings.english = engCloseMatches.map(function(e) { return e.replace(/\[CLOSE-E-\d+\]\s*/, '').trim(); });

  // 동의어 파싱
  var synonymMatches = content.match(/\[SYN-\d+\]\s*[^\n]+/g) || [];
  pool.synonyms = synonymMatches.map(function(e) {
    var line = e.replace(/\[SYN-\d+\]\s*/, '').trim();
    var parts = line.split(':');
    if (parts.length === 2) {
      return { base: parts[0].trim(), variants: parts[1].split(',').map(function(v) { return v.trim(); }) };
    }
    return null;
  }).filter(Boolean);

  return pool;
}

// 아이보리 박스 HTML 생성
function createBox(content) {
  return '<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">\n<strong>이렇게 수업합니다!</strong><br>\n' + content + '\n</div>';
}

// 동의어 치환
function applySynonyms(text, pool, seed) {
  var result = text;
  pool.synonyms.forEach(function(syn, idx) {
    if (syn && syn.base && syn.variants.length > 0) {
      var variantIdx = (seed + idx) % (syn.variants.length + 1);
      if (variantIdx > 0) {
        var replacement = syn.variants[variantIdx - 1];
        result = result.replace(new RegExp(syn.base, 'g'), replacement);
      }
    }
  });
  return result;
}

// 콘텐츠 생성 함수
function generateContent(centerSlug, articleId, pool, centerConfigs) {
  var center = centerConfigs[centerSlug];
  if (!center) {
    console.error('센터 설정 없음: ' + centerSlug);
    return null;
  }

  // 센터 해시 계산
  var centerHash = getCenterHash(center.name);

  // 글 타입 결정
  var subject, subjectName, subjectTag;
  if (articleId <= 12) {
    subject = 'math'; subjectName = '수학'; subjectTag = '수학학원';
  } else if (articleId <= 24) {
    subject = 'english'; subjectName = '영어'; subjectTag = '영어학원';
  } else if (articleId <= 30) {
    subject = 'korean'; subjectName = '국어'; subjectTag = '국어학원';
  } else if (articleId <= 36) {
    subject = 'science'; subjectName = '과학'; subjectTag = '과학학원';
  } else if (articleId <= 40) {
    subject = 'social'; subjectName = '사회'; subjectTag = '사회학원';
  } else {
    subject = 'general'; subjectName = '종합'; subjectTag = '학습코칭';
  }

  // 학년 결정
  var isHigh = articleId % 2 === 1;
  var gradeType = isHigh ? '고등' : '중등';

  // 제목 접미사 풀
  var titleSuffixes = [
    '수능 대비', '개념 완성', '실력 향상', '개념 정리', '취약 유형 보완',
    '기초 다지기', '심화 학습', '내신 대비', '성적 향상', '학습 관리',
    '실전 훈련', '문제 풀이', '1:1 맞춤', '집중 과정', '단기 완성'
  ];
  var suffixIdx = (articleId + centerHash) % titleSuffixes.length;
  var titleSuffix = titleSuffixes[suffixIdx];

  // 학교 정보
  var highSchools = (center.schools && center.schools.high) || ['지역 고등학교'];
  var midSchools = (center.schools && center.schools.middle) || ['지역 중학교'];
  var schoolName = isHigh ? highSchools[articleId % highSchools.length] : midSchools[articleId % midSchools.length];

  // 랜드마크
  var apartments = center.apartments || ['주변 아파트'];
  var apartmentName = apartments[(articleId + centerHash) % apartments.length];
  var stationName = center.station ? center.station.replace('역역', '역') : '지역';

  // 제목 템플릿 (학원 포함)
  var titleTemplates = [
    apartmentName + ' 인근 ' + gradeType + ' ' + subjectName + '학원 | ' + titleSuffix + ' | 와와학습코칭센터 ' + center.name,
    stationName + ' ' + gradeType + ' ' + subjectName + ' ' + titleSuffix + '학원 | ' + schoolName + ' 내신 대비 | 와와학습코칭센터 ' + center.name,
    (center.district || center.city) + ' ' + gradeType + ' ' + subjectName + ' 코칭학원 | ' + schoolName + ' 맞춤 수업 | ' + center.name,
    schoolName + ' ' + subjectName + ' 성적 향상 코칭 | ' + (center.district || center.city) + ' ' + gradeType + '학원 | ' + center.name
  ];
  var titleIdx = (articleId + centerHash) % titleTemplates.length;
  var title = titleTemplates[titleIdx];

  // description
  var descriptions = [
    center.city + ' ' + (center.district || '') + ' ' + center.name + ' ' + subjectName + ' 학원. ' + stationName + ' 인근. ' + schoolName + ' 학생 맞춤 지도.',
    gradeType + ' ' + subjectName + ' 전문 코칭센터. ' + (center.district || center.city) + ' ' + stationName + ' 위치. ' + schoolName + ' 내신 대비.',
    center.name + ' ' + gradeType + ' ' + subjectName + ' 수업. ' + apartmentName + ' 인근. 1:1 맞춤 학습 관리.'
  ];
  var descIdx = (articleId + centerHash) % descriptions.length;
  var description = descriptions[descIdx];

  // 태그 (학원으로)
  var tags = [
    center.name.replace('점', ''),
    center.city + subjectTag,
    stationName.replace('역', ''),
    schoolName
  ];

  // 서두 선택
  var openingPool = subject === 'math' ? pool.openings.math :
                    subject === 'english' ? pool.openings.english :
                    subject === 'korean' ? pool.openings.korean : pool.openings.general;
  var openingIdx = (articleId + centerHash) % Math.max(openingPool.length, 1);
  var opening = openingPool[openingIdx] || (subjectName + ' 학습, 기초부터 탄탄하게 잡아야 합니다.');

  // 아이보리 박스 선택
  var boxTypes = ['diag', 'method', 'exam', 'manage', 'hw', 'wrong', 'study', 'grade'];
  var boxCount = 5 + (articleId % 3);
  var boxes = [];
  for (var i = 0; i < boxCount; i++) {
    var boxType = boxTypes[(articleId + i + centerHash) % boxTypes.length];
    var boxPool = pool.boxes[boxType] || [];
    var boxIdx = (articleId + i + centerHash) % Math.max(boxPool.length, 1);
    if (boxPool[boxIdx]) {
      boxes.push(boxPool[boxIdx]);
    }
  }

  // H2 제목 선택
  var h2Types = ['import', 'school', 'method', 'grade', 'fee', 'center', 'habit'];
  var h2Titles = {};
  h2Types.forEach(function(type, idx) {
    var h2Pool = pool.h2Titles[type] || [];
    var h2Idx = (articleId + idx + centerHash) % Math.max(h2Pool.length, 1);
    h2Titles[type] = h2Pool[h2Idx] || (type + ' 관련 내용');
  });

  // 마무리
  var closePool = subject === 'english' ? pool.closings.english : pool.closings.math;
  var closeIdx = (articleId + centerHash) % Math.max(closePool.length, 1);
  var closing = closePool[closeIdx] || (center.name + '에서 함께 시작하세요.');

  // FAQ 선택
  var faqCats = Object.keys(pool.faq.questions);
  var faqItems = [];
  for (var j = 0; j < 3; j++) {
    var cat = faqCats[(articleId + j + centerHash) % faqCats.length];
    var qPool = pool.faq.questions[cat] || [];
    var aPool = pool.faq.answers[cat] || [];
    var qIdx = (articleId + j + centerHash) % Math.max(qPool.length, 1);
    var aIdx = (articleId + j + centerHash) % Math.max(aPool.length, 1);
    if (qPool[qIdx] && aPool[aIdx]) {
      faqItems.push({ q: qPool[qIdx], a: aPool[aIdx] });
    }
  }

  // 수업료
  var isSeoul = center.city === '서울';
  var feeTable = isSeoul ?
    '| 학년 | 주1회 | 주2회 |\n|------|-------|-------|\n| 초등 | 15만원 - 25만원 | 28만원 - 42만원 |\n| 중등 | 25만원 - 35만원 | 32만원 - 50만원 |\n| 고1-2 | 28만원 - 40만원 | 36만원 - 56만원 |\n| 고3 | 32만원 - 45만원 | 40만원 - 65만원 |' :
    '| 학년 | 주1회 | 주2회 |\n|------|-------|-------|\n| 초등 | 12만원 - 22만원 | 25만원 - 38만원 |\n| 중등 | 22만원 - 32만원 | 29만원 - 47만원 |\n| 고1-2 | 25만원 - 36만원 | 33만원 - 53만원 |\n| 고3 | 28만원 - 40만원 | 37만원 - 59만원 |';

  // FAQ 마크다운
  var faqMd = faqItems.map(function(faq) { return '**Q. ' + faq.q + '**\n\nA. ' + faq.a; }).join('\n\n');

  // 마크다운 콘텐츠
  var mdContent = '---\n' +
    'title: "' + title + '"\n' +
    'date: 2026-01-11\n' +
    'description: "' + description + '"\n' +
    'tags:\n  - ' + tags.join('\n  - ') + '\n' +
    'featured_image: "/images/wawalong.jpg"\n' +
    '---\n\n' +
    opening + '\n\n' +
    createBox(boxes[0] || '첫 수업에서 학생의 현재 실력을 정확히 진단합니다.') + '\n\n' +
    '## ' + (h2Titles.import || '학습의 중요성') + '\n\n' +
    gradeType + ' ' + subjectName + '은 기초 개념 이해가 무엇보다 중요합니다. ' + schoolName + ' 학생들의 학습 패턴을 분석하여 맞춤형 커리큘럼을 제공합니다.\n\n' +
    createBox(boxes[1] || '개념 이해 → 유형 분석 → 문제 적용 순으로 체계적으로 진행합니다.') + '\n\n' +
    '## ' + (h2Titles.school || '학교별 맞춤 수업') + '\n\n' +
    schoolName + '을 비롯한 ' + (center.district || center.city) + ' 지역 학교들의 시험 경향을 분석합니다. 학교별 기출 유형에 맞춘 대비가 가능합니다.\n\n' +
    createBox(boxes[2] || '학교별 기출문제 분석으로 시험 대비 효율을 높입니다.') + '\n\n' +
    '## ' + (h2Titles.method || '학습 방법') + '\n\n' +
    gradeType + ' ' + subjectName + ' 학습 전략을 체계적으로 세워드립니다.\n\n' +
    (boxes[3] ? createBox(boxes[3]) + '\n\n' : '') +
    '## ' + (h2Titles.grade || '학년별 전략') + '\n\n' +
    (isHigh ? '고등학생' : '중학생') + '에게 맞는 학습 로드맵을 제시합니다. 내신과 수능을 균형 있게 준비할 수 있도록 지도합니다.\n\n' +
    (boxes[4] ? createBox(boxes[4]) + '\n\n' : '') +
    '## ' + (h2Titles.fee || '수업료 안내') + '\n\n' +
    feeTable + '\n\n' +
    '수업 시간, 횟수에 따라 조정될 수 있습니다. 상담 시 자세한 안내를 받으실 수 있습니다.\n\n' +
    (boxes[5] ? createBox(boxes[5]) + '\n\n' : '') +
    '## ' + (h2Titles.center || '센터 위치') + '\n\n' +
    center.fullName + '\n' +
    '📝 등록번호: ' + center.registration + '\n' +
    '🚇 ' + stationName + ' 인근\n\n' +
    (boxes[6] ? createBox(boxes[6]) + '\n\n' : '') +
    '## 자주 묻는 질문\n\n' +
    faqMd + '\n\n' +
    '## 마무리\n\n' +
    closing + '\n\n' +
    '{{< cta-kakao-consultation >}}\n';

  // 동의어 치환
  mdContent = applySynonyms(mdContent, pool, articleId + centerHash);

  return mdContent;
}

// 인덱스 페이지 생성
function generateIndexPage(centerSlug, centerConfigs) {
  var center = centerConfigs[centerSlug];
  if (!center) return null;

  var stationName = center.station ? center.station.replace('역역', '역') : '';

  var titleVariants = [
    center.name + ' | ' + center.city + ' ' + (center.district || '') + ' 학습코칭학원',
    '와와학습코칭센터 ' + center.name + ' | ' + (center.district || center.city) + ' 학원',
    (center.district || center.city) + ' ' + center.name + ' | 초중고 학습코칭학원'
  ];
  var titleIdx = getCenterHash(center.name) % titleVariants.length;
  var title = titleVariants[titleIdx];

  var tags = [
    center.name.replace('점', ''),
    center.city + '학원',
    (center.district || center.city) + '코칭',
    stationName ? stationName.replace('역', '') : center.city
  ].filter(Boolean);

  return '---\n' +
    'title: "' + title + '"\n' +
    'date: 2026-01-11\n' +
    'description: "' + center.city + ' ' + (center.district || '') + ' ' + center.name + '. ' + stationName + ' 인근 초중고 학습코칭센터."\n' +
    'tags:\n  - ' + tags.join('\n  - ') + '\n' +
    'featured_image: "/images/wawalong.jpg"\n' +
    '---\n\n' +
    '# 와와학습코칭센터 ' + center.name + '\n\n' +
    center.city + ' ' + (center.district || '') + ' 지역의 학습코칭 전문 센터입니다.\n\n' +
    '## 센터 정보\n\n' +
    '📝 등록번호: ' + center.registration + '\n' +
    '🚇 위치: ' + stationName + ' 인근\n\n' +
    '## 학습 프로그램\n\n' +
    '- 초등 기초학습\n' +
    '- 중등 내신 대비\n' +
    '- 고등 수능/내신 병행\n' +
    '- 1:1 맞춤 코칭\n\n' +
    '상담 예약은 아래 버튼을 통해 진행해주세요.\n\n' +
    '{{< cta-kakao-consultation >}}\n';
}

// 메인 실행
function main() {
  console.log('=== 25개 센터 재생성 시작 ===\n');

  // 표현 풀 로드
  var poolPath = './COACHING_EXPRESSION_POOL.md';
  if (!fs.existsSync(poolPath)) {
    console.error('표현 풀 파일 없음: ' + poolPath);
    return;
  }
  var pool = parseExpressionPool(poolPath);
  console.log('표현 풀 로드 완료');

  // 25개 센터 키 로드
  var fixedKeys = JSON.parse(fs.readFileSync('./fixed-center-keys.json', 'utf-8'));
  console.log('\n대상 센터: ' + fixedKeys.length + '개');
  console.log(fixedKeys.join(', '));

  // 센터 설정 로드
  var centerConfigs = JSON.parse(fs.readFileSync('./generated-center-configs.json', 'utf-8'));

  var allKvData = [];

  fixedKeys.forEach(function(centerSlug, idx) {
    var centerConfig = centerConfigs[centerSlug];
    if (!centerConfig) {
      console.log('  [' + (idx + 1) + '/' + fixedKeys.length + '] ' + centerSlug + ' - 설정 없음, 스킵');
      return;
    }

    console.log('[' + (idx + 1) + '/' + fixedKeys.length + '] ' + centerSlug + ' (' + centerConfig.name + ') 재생성 중...');

    // 51개 글 생성
    for (var i = 1; i <= 51; i++) {
      var content = generateContent(centerSlug, i, pool, centerConfigs);
      if (content) {
        allKvData.push({
          key: '/coaching/' + centerSlug + '/' + i + '/index',
          value: content
        });
      }
    }

    // 인덱스 페이지 생성
    var indexContent = generateIndexPage(centerSlug, centerConfigs);
    if (indexContent) {
      allKvData.push({
        key: '/coaching/' + centerSlug + '/index',
        value: indexContent
      });
    }

    console.log('  완료: 52개 (51 콘텐츠 + 1 인덱스)');
  });

  // KV 파일 저장
  var outputPath = './fixed-25-centers-kv.json';
  fs.writeFileSync(outputPath, JSON.stringify(allKvData, null, 2));
  console.log('\n=== 저장 완료: ' + outputPath + ' (' + allKvData.length + '개) ===');

  // 키워드 체크
  var contentStr = JSON.stringify(allKvData);
  var gwaoeCount = (contentStr.match(/과외/g) || []).length;
  console.log('\n검증: "과외" 키워드 ' + gwaoeCount + '개 (0이어야 정상)');
}

main();
