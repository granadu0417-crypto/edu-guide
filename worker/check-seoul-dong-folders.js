const fs = require('fs');
const path = require('path');

const seoulPath = 'content/seoul';
const districts = fs.readdirSync(seoulPath).filter(f =>
  fs.statSync(path.join(seoulPath, f)).isDirectory()
);

console.log('=== 서울 구별 동(폴더) 수 ===');

const results = [];

districts.forEach(district => {
  const districtPath = path.join(seoulPath, district);
  const items = fs.readdirSync(districtPath);

  // Count Korean-named folders (동 folders have Korean names)
  const dongFolders = items.filter(item => {
    const fullPath = path.join(districtPath, item);
    return fs.statSync(fullPath).isDirectory() && /[가-힣]/.test(item);
  });

  results.push({ district, count: dongFolders.length, dongs: dongFolders });
});

results.sort((a, b) => a.count - b.count);

results.forEach(r => {
  console.log(`${r.district}: ${r.count}개 동`);
});

console.log('\n=== 상세 내역 (5개 이하 동) ===');
results.filter(r => r.count <= 5).forEach(r => {
  console.log(`\n[${r.district}] ${r.count}개:`);
  r.dongs.forEach(d => console.log(`  - ${d}`));
});
