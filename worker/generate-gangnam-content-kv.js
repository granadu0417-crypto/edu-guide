// 강남구 콘텐츠 KV 생성 스크립트
// 수정된 이미지 포함하여 개별 콘텐츠 파일을 KV JSON으로 생성

const fs = require('fs');
const path = require('path');

const GANGNAM_DIR = '/mnt/c/Users/user/Desktop/과외를부탁해/edu-guide-fresh/content/seoul/gangnam';
const OUTPUT_FILE = '/mnt/c/Users/user/Desktop/과외를부탁해/edu-guide-fresh/worker/gangnam-content-kv.json';

function generateKV() {
  const files = fs.readdirSync(GANGNAM_DIR).filter(f => f.endsWith('.md') && f !== '_index.md');
  const kvData = [];

  for (const file of files) {
    const filePath = path.join(GANGNAM_DIR, file);
    const content = fs.readFileSync(filePath, 'utf-8');

    // 파일명에서 확장자 제거하여 URL 경로 생성
    const slug = file.replace('.md', '');
    const key = `/seoul/gangnam/${slug}/index`;

    kvData.push({
      key,
      value: content
    });
  }

  fs.writeFileSync(OUTPUT_FILE, JSON.stringify(kvData, null, 2), 'utf-8');
  console.log(`생성 완료: ${kvData.length}개 항목`);
  console.log(`출력 파일: ${OUTPUT_FILE}`);
}

generateKV();
