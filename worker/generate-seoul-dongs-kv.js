const fs = require('fs');
const path = require('path');

const targetDistricts = ['geumcheon', 'gwanak', 'yangcheon', 'dobong', 'nowon', 'jungnang', 'dongjak'];
const kvData = [];

const baseDir = '/mnt/c/Users/user/Desktop/과외를부탁해/edu-guide';

for (const district of targetDistricts) {
  const districtPath = path.join(baseDir, 'content', 'seoul', district);

  if (!fs.existsSync(districtPath)) continue;

  const dongs = fs.readdirSync(districtPath).filter(item =>
    fs.statSync(path.join(districtPath, item)).isDirectory()
  );

  for (const dong of dongs) {
    const dongPath = path.join(districtPath, dong);
    const files = fs.readdirSync(dongPath).filter(f => f.endsWith('.md'));

    for (const file of files) {
      const filePath = path.join(dongPath, file);
      const content = fs.readFileSync(filePath, 'utf-8');

      // KV 키 생성
      let key;
      if (file === '_index.md') {
        key = '/seoul/' + district + '/' + encodeURIComponent(dong) + '/index';
      } else {
        const fileName = file.replace('.md', '');
        key = '/seoul/' + district + '/' + encodeURIComponent(dong) + '/' + fileName + '/index';
      }

      kvData.push({ key, value: content });
    }
  }
}

// 단일 파일로 저장
const outputPath = path.join(baseDir, 'worker', 'seoul-dongs-kv.json');
fs.writeFileSync(outputPath, JSON.stringify(kvData, null, 0));
console.log('seoul-dongs-kv.json 생성 완료: ' + kvData.length + '개 엔트리');
console.log('파일 크기: ' + (fs.statSync(outputPath).size / 1024 / 1024).toFixed(2) + ' MB');
