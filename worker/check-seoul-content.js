const fs = require('fs');
const path = require('path');

const seoulPath = 'content/seoul';
const districts = fs.readdirSync(seoulPath).filter(f =>
  fs.statSync(path.join(seoulPath, f)).isDirectory()
);

const results = [];

districts.forEach(district => {
  const districtPath = path.join(seoulPath, district);
  let fileCount = 0;

  // Count all .md files recursively
  const countFiles = (dir) => {
    const items = fs.readdirSync(dir);
    items.forEach(item => {
      const fullPath = path.join(dir, item);
      const stat = fs.statSync(fullPath);
      if (stat.isDirectory()) {
        countFiles(fullPath);
      } else if (item.endsWith('.md')) {
        fileCount++;
      }
    });
  };

  countFiles(districtPath);
  results.push({ district, fileCount });
});

// Sort by file count
results.sort((a, b) => a.fileCount - b.fileCount);

console.log('=== 서울 구별 콘텐츠 파일 수 ===');
results.forEach(r => {
  console.log(`${r.district}: ${r.fileCount}개`);
});

console.log('\n=== 총계 ===');
console.log(`총 파일 수: ${results.reduce((sum, r) => sum + r.fileCount, 0)}개`);
