const fs = require('fs');
const path = require('path');

// 신규 생성된 19개 도시
const newCities = [
  { province: 'gangwon', city: 'donghae' },
  { province: 'gangwon', city: 'sokcho' },
  { province: 'gangwon', city: 'samcheok' },
  { province: 'chungbuk', city: 'jecheon' },
  { province: 'chungnam', city: 'seosan' },
  { province: 'chungnam', city: 'dangjin' },
  { province: 'chungnam', city: 'nonsan' },
  { province: 'gyeongbuk', city: 'gyeongju' },
  { province: 'gyeongbuk', city: 'gyeongsan' },
  { province: 'gyeongbuk', city: 'andong' },
  { province: 'gyeongbuk', city: 'gimcheon' },
  { province: 'gyeongnam', city: 'gimhae' },
  { province: 'gyeongnam', city: 'yangsan' },
  { province: 'gyeongnam', city: 'geoje' },
  { province: 'gyeongnam', city: 'tongyeong' },
  { province: 'jeonbuk', city: 'gunsan' },
  { province: 'jeonbuk', city: 'jeongeup' },
  { province: 'jeonnam', city: 'mokpo' },
  { province: 'jeonnam', city: 'gwangyang' }
];

const kvData = [];

newCities.forEach(({ province, city }) => {
  const basePath = `content/provinces/${province}/${city}`;
  
  // 파일 목록
  const files = ['_index.md', 'high-math.md', 'high-english.md', 'middle-math.md', 'middle-english.md'];
  
  files.forEach(file => {
    const filePath = path.join(basePath, file);
    if (fs.existsSync(filePath)) {
      const content = fs.readFileSync(filePath, 'utf-8');
      
      // KV 키 생성
      let key;
      if (file === '_index.md') {
        key = `/provinces/${province}/${city}/index`;
      } else {
        const slug = file.replace('.md', '');
        key = `/provinces/${province}/${city}/${slug}`;
      }
      
      kvData.push({ key, value: content });
    }
  });
});

console.log(`총 ${kvData.length}개 KV 엔트리 생성`);
fs.writeFileSync('worker/province-cities-kv.json', JSON.stringify(kvData, null, 2));
console.log('worker/province-cities-kv.json 파일 생성 완료');
