const fs = require('fs');
const path = require('path');

const contentDir = path.join(__dirname, '..', 'content', 'ulsan');

// 새로 추가된 울산 동 단위
const ulsanNewDongs = {
  jung_us: ['byeongyeong', 'seodong'],
  nam_us: ['daehyeon', 'namhwa', 'suam', 'duwang', 'seonam'],
  dong_us: ['dongbu', 'seobu', 'nammok'],
  buk_us: ['maegok', 'hwabong', 'cheongok', 'sincheon', 'jungsan']
};

const kvData = [];

for (const [gu, dongs] of Object.entries(ulsanNewDongs)) {
  for (const dong of dongs) {
    const dongDir = path.join(contentDir, gu, dong);

    if (!fs.existsSync(dongDir)) {
      console.log(`경고: ${dongDir} 없음`);
      continue;
    }

    const files = fs.readdirSync(dongDir).filter(f => f.endsWith('.md'));

    for (const file of files) {
      const filePath = path.join(dongDir, file);
      const content = fs.readFileSync(filePath, 'utf-8');

      let key;
      if (file === '_index.md') {
        key = `/ulsan/${gu}/${dong}/index`;
      } else {
        const baseName = file.slice(0, -3);
        key = `/ulsan/${gu}/${dong}/${baseName}/index`;
      }

      kvData.push({ key, value: content });
    }
  }
}

// JSON 파일로 저장
const outputPath = path.join(__dirname, 'ulsan-dongs-kv.json');
fs.writeFileSync(outputPath, JSON.stringify(kvData, null, 2));

console.log(`생성 완료: ${kvData.length}개 엔트리`);
console.log(`파일: ${outputPath}`);
console.log(`파일 크기: ${(fs.statSync(outputPath).size / 1024 / 1024).toFixed(2)} MB`);
