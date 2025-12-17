const fs = require('fs');
const path = require('path');

const contentDir = path.join(__dirname, '..', 'content', 'gyeonggi');

// 안산시 동 단위
const ansanDongs = {
  danwon: ['gojan1', 'gojan2', 'wongok1', 'wongok2', 'choji1', 'seonbu1', 'seonbu2', 'wadong'],
  sangnok: ['wolpi1', 'bono1', 'bono2', 'sadong', 'sayi', 'banwol', 'suam']
};

// 성남시 동 단위
const seongnamDongs = {
  bundang: ['seohyeon', 'jeongja', 'sunae', 'yatap1', 'yatap2', 'imae', 'pangyo', 'sampyeong'],
  jungwon: ['seongnam', 'geumgwang1', 'geumgwang2', 'eunhaeng1', 'sangdaewon1', 'hadaewon'],
  sujeong: ['sujin1', 'sujin2', 'taepyeong1', 'taepyeong2', 'dandae', 'sinheung1']
};

const kvData = [];

// 안산 동 처리
for (const [gu, dongs] of Object.entries(ansanDongs)) {
  for (const dong of dongs) {
    const dongDir = path.join(contentDir, 'ansan', gu, dong);

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
        key = `/gyeonggi/ansan/${gu}/${dong}/index`;
      } else {
        const baseName = file.slice(0, -3);
        key = `/gyeonggi/ansan/${gu}/${dong}/${baseName}/index`;
      }

      kvData.push({ key, value: content });
    }
  }
}

// 성남 동 처리
for (const [gu, dongs] of Object.entries(seongnamDongs)) {
  for (const dong of dongs) {
    const dongDir = path.join(contentDir, 'seongnam', gu, dong);

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
        key = `/gyeonggi/seongnam/${gu}/${dong}/index`;
      } else {
        const baseName = file.slice(0, -3);
        key = `/gyeonggi/seongnam/${gu}/${dong}/${baseName}/index`;
      }

      kvData.push({ key, value: content });
    }
  }
}

// JSON 파일로 저장
const outputPath = path.join(__dirname, 'gyeonggi-dongs-kv.json');
fs.writeFileSync(outputPath, JSON.stringify(kvData, null, 2));

console.log(`생성 완료: ${kvData.length}개 엔트리`);
console.log(`파일: ${outputPath}`);
console.log(`파일 크기: ${(fs.statSync(outputPath).size / 1024 / 1024).toFixed(2)} MB`);
