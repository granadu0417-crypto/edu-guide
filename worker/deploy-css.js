// CSS 파일을 KV에 배포하는 스크립트
const fs = require('fs');
const path = require('path');

const staticDir = path.join(__dirname, '..', 'static');
const outputFile = path.join(__dirname, 'css-kv-update.json');

// CSS 파일 목록
const cssFiles = [
  { src: 'css/style.css', key: '/css/style.css' },
  { src: 'css/viral.css', key: '/css/viral.css' }
];

const kvData = [];

for (const file of cssFiles) {
  const filePath = path.join(staticDir, file.src);

  if (fs.existsSync(filePath)) {
    const content = fs.readFileSync(filePath, 'utf8');
    kvData.push({
      key: file.key,
      value: content
    });
    console.log(`✅ ${file.key} (${content.length} bytes)`);
  } else {
    console.log(`❌ ${file.key} - 파일 없음`);
  }
}

fs.writeFileSync(outputFile, JSON.stringify(kvData, null, 2));
console.log(`\n📦 생성 완료: ${outputFile}`);
console.log(`\n배포 명령어:`);
console.log(`npx wrangler kv bulk put "css-kv-update.json" --namespace-id 725aefb7b1c64c6c90d2cf4daf061bf3 --remote`);
