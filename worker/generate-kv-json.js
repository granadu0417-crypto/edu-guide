#!/usr/bin/env node
/**
 * Hugo public/ 콘텐츠를 KV bulk upload용 JSON 파일로 변환
 *
 * 사용법:
 *   node generate-kv-json.js
 *
 * 출력:
 *   worker/kv-data-1.json, kv-data-2.json, ... (배치별 파일)
 *
 * 업로드:
 *   npx wrangler kv bulk put "kv-data-1.json" --namespace-id 725aefb7b1c64c6c90d2cf4daf061bf3
 */

const fs = require('fs');
const path = require('path');

const PUBLIC_DIR = path.join(__dirname, '..', 'public');
const OUTPUT_DIR = __dirname;
const BATCH_SIZE = 1000;

// 바이너리 파일 확장자 (텍스트로 처리 불가)
const BINARY_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.gif', '.ico', '.webp', '.woff', '.woff2', '.ttf', '.eot', '.svg'];

// 제외할 파일 패턴
const EXCLUDE_PATTERNS = [
  /\.DS_Store$/,
  /Thumbs\.db$/,
];

function shouldExclude(filePath) {
  return EXCLUDE_PATTERNS.some(pattern => pattern.test(filePath));
}

function isBinaryFile(filePath) {
  const ext = path.extname(filePath).toLowerCase();
  return BINARY_EXTENSIONS.includes(ext);
}

function getKVKey(filePath) {
  let key = '/' + path.relative(PUBLIC_DIR, filePath).replace(/\\/g, '/');

  // index.html -> /index
  if (key.endsWith('/index.html')) {
    key = key.replace('/index.html', '/index');
  } else if (key.endsWith('.html')) {
    key = key.replace('.html', '');
  }

  return key;
}

function getAllFiles(dir, fileList = []) {
  const files = fs.readdirSync(dir);

  for (const file of files) {
    const filePath = path.join(dir, file);
    const stat = fs.statSync(filePath);

    if (stat.isDirectory()) {
      getAllFiles(filePath, fileList);
    } else if (!shouldExclude(filePath) && !isBinaryFile(filePath)) {
      fileList.push(filePath);
    }
  }

  return fileList;
}

function main() {
  console.log('🚀 Hugo → KV JSON 생성기');
  console.log(`   소스: ${PUBLIC_DIR}`);
  console.log('');

  // 1. 파일 목록 수집
  console.log('📁 파일 목록 수집 중...');
  const files = getAllFiles(PUBLIC_DIR);
  console.log(`   총 ${files.length}개 텍스트 파일 발견`);

  // 2. KV 페어 생성
  console.log('\n🔧 KV 키-값 페어 생성 중...');
  const pairs = [];
  let skipped = 0;

  for (const filePath of files) {
    try {
      const content = fs.readFileSync(filePath, 'utf-8');
      const key = getKVKey(filePath);
      pairs.push({ key, value: content });
    } catch (err) {
      console.warn(`   ⚠️ 스킵: ${filePath}`);
      skipped++;
    }
  }

  console.log(`   성공: ${pairs.length}개`);
  console.log(`   스킵: ${skipped}개`);

  // 3. 샘플 출력
  console.log('\n📋 샘플 KV 키 (처음 10개):');
  pairs.slice(0, 10).forEach(p => {
    console.log(`   ${p.key} (${p.value.length} bytes)`);
  });

  // 4. 배치별 JSON 파일 생성
  const batches = [];
  for (let i = 0; i < pairs.length; i += BATCH_SIZE) {
    batches.push(pairs.slice(i, i + BATCH_SIZE));
  }

  console.log(`\n📤 JSON 파일 생성 (${batches.length}개 배치)`);

  const outputFiles = [];
  for (let i = 0; i < batches.length; i++) {
    const fileName = `kv-data-${i + 1}.json`;
    const filePath = path.join(OUTPUT_DIR, fileName);
    fs.writeFileSync(filePath, JSON.stringify(batches[i], null, 2));
    outputFiles.push(fileName);
    console.log(`   ✅ ${fileName} (${batches[i].length}개 항목)`);
  }

  // 5. 업로드 명령어 출력
  console.log('\n📝 KV 업로드 명령어:');
  console.log('   cd worker');
  outputFiles.forEach(f => {
    console.log(`   npx wrangler kv bulk put "${f}" --namespace-id 725aefb7b1c64c6c90d2cf4daf061bf3`);
  });

  console.log('\n✅ JSON 파일 생성 완료!');
}

main();
