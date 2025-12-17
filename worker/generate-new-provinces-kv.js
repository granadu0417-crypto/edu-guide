const fs = require('fs');
const path = require('path');

const contentDir = path.join(__dirname, '..', 'content', 'provinces');

// 새로 추가된 8개 도시
const newCities = [
  { province: 'gangwon', city: 'taebaek' },
  { province: 'gyeongbuk', city: 'yeongju' },
  { province: 'gyeongbuk', city: 'sangju' },
  { province: 'gyeongnam', city: 'miryang' },
  { province: 'gyeongnam', city: 'sacheon' },
  { province: 'jeonbuk', city: 'namwon' },
  { province: 'jeonbuk', city: 'gimje' },
  { province: 'jeonnam', city: 'naju' }
];

const kvData = [];

for (const { province, city } of newCities) {
  const cityDir = path.join(contentDir, province, city);

  if (!fs.existsSync(cityDir)) {
    console.log(`경고: ${cityDir} 없음`);
    continue;
  }

  const files = fs.readdirSync(cityDir).filter(f => f.endsWith('.md'));

  for (const file of files) {
    const filePath = path.join(cityDir, file);
    const content = fs.readFileSync(filePath, 'utf-8');

    // KV 키 생성
    let key;
    if (file === '_index.md') {
      key = `/provinces/${province}/${city}/index`;
    } else {
      const baseName = file.slice(0, -3); // .md 제거
      key = `/provinces/${province}/${city}/${baseName}`;
    }

    kvData.push({ key, value: content });
  }
}

// JSON 파일로 저장
const outputPath = path.join(__dirname, 'new-provinces-kv.json');
fs.writeFileSync(outputPath, JSON.stringify(kvData, null, 2));

console.log(`생성 완료: ${kvData.length}개 엔트리`);
console.log(`파일: ${outputPath}`);

// 키 목록 출력
kvData.forEach(item => console.log(`  ${item.key}`));
