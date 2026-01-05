// 과목별 이미지 수정 스크립트 v2
// 실제 존재하는 static/images 폴더의 이미지 파일 사용

const fs = require('fs');
const path = require('path');

const GANGNAM_DIR = '/mnt/c/Users/user/Desktop/과외를부탁해/edu-guide-fresh/content/seoul/gangnam';
const IMAGES_DIR = '/mnt/c/Users/user/Desktop/과외를부탁해/edu-guide-fresh/static/images';

// 실제 존재하는 이미지 파일 목록 가져오기
function getExistingImages() {
  const files = fs.readdirSync(IMAGES_DIR)
    .filter(f => f.endsWith('.jpg') && f.startsWith('edu_'))
    .sort();
  return files;
}

function fixImages() {
  const existingImages = getExistingImages();
  console.log(`사용 가능한 이미지: ${existingImages.length}개`);

  // 과목별로 다른 범위의 이미지 할당
  // 국어: 200-299, 과학: 300-399, 논술: 400-499, 코딩: 500-599
  const subjectRanges = {
    korean: { start: 200, end: 299 },
    science: { start: 300, end: 399 },
    essay: { start: 400, end: 499 },
    coding: { start: 500, end: 599 }
  };

  const files = fs.readdirSync(GANGNAM_DIR).filter(f => f.endsWith('.md') && f !== '_index.md');

  let fixedCount = 0;
  const counters = { korean: 0, science: 0, essay: 0, coding: 0 };

  for (const file of files) {
    const filePath = path.join(GANGNAM_DIR, file);
    let content = fs.readFileSync(filePath, 'utf-8');
    let modified = false;
    let subject = null;

    // 과목 판별
    if (file.includes('-korean')) subject = 'korean';
    else if (file.includes('-science')) subject = 'science';
    else if (file.includes('-essay')) subject = 'essay';
    else if (file.includes('-coding')) subject = 'coding';

    if (!subject) continue;

    // 이미지 인덱스 계산
    const range = subjectRanges[subject];
    const idx = range.start + (counters[subject] % (range.end - range.start + 1));

    // edu_XXXX 형식에 맞는 이미지 찾기
    const targetPrefix = `edu_${String(idx).padStart(4, '0')}_`;
    const matchingImage = existingImages.find(img => img.startsWith(targetPrefix));

    if (matchingImage) {
      // 기존 이미지 경로 패턴 찾아서 교체
      const oldPattern = /featured_image: "[^"]+"/;
      if (oldPattern.test(content)) {
        content = content.replace(oldPattern, `featured_image: "/images/${matchingImage}"`);
        modified = true;
        counters[subject]++;
      }
    } else {
      console.log(`Warning: No image found for ${file} (looking for ${targetPrefix}*)`);
    }

    if (modified) {
      fs.writeFileSync(filePath, content, 'utf-8');
      fixedCount++;
      console.log(`Fixed: ${file} -> ${matchingImage}`);
    }
  }

  console.log(`\n총 ${fixedCount}개 파일 수정 완료`);
  console.log(`  국어: ${counters.korean}개`);
  console.log(`  과학: ${counters.science}개`);
  console.log(`  논술: ${counters.essay}개`);
  console.log(`  코딩: ${counters.coding}개`);
}

fixImages();
