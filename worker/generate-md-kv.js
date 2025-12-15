#!/usr/bin/env node
/**
 * Markdown Direct KV 생성기
 *
 * .md 파일을 직접 KV에 저장하기 위한 JSON 생성
 * Hugo 빌드 없이 초 단위 배포 가능
 *
 * 사용법:
 *   node generate-md-kv.js           # 전체 배포
 *   node generate-md-kv.js --changed "file1.md file2.md"  # 증분 배포
 */

const fs = require('fs');
const path = require('path');

const CONTENT_DIR = path.join(__dirname, '..', 'content');
const OUTPUT_DIR = __dirname;
const BATCH_SIZE = 800; // KV bulk upload 제한

// content/seoul/gangnam.md -> /seoul/gangnam/
function contentPathToUrlPath(filePath) {
  let relativePath = path.relative(CONTENT_DIR, filePath);

  // Windows 경로 처리
  relativePath = relativePath.replace(/\\/g, '/');

  // .md 제거
  relativePath = relativePath.replace(/\.md$/, '');

  // _index 처리
  if (relativePath.endsWith('/_index') || relativePath === '_index') {
    relativePath = relativePath.replace(/_index$/, '');
  }

  // index 처리
  if (relativePath.endsWith('/index')) {
    relativePath = relativePath.replace(/\/index$/, '');
  }

  // KV 키 형식: /path/to/page/index
  let kvKey = '/' + relativePath;
  if (kvKey === '/') {
    kvKey = '/index';
  } else if (!kvKey.endsWith('/index')) {
    kvKey = kvKey + '/index';
  }

  return kvKey;
}

// 모든 .md 파일 찾기
function findAllMdFiles(dir, files = []) {
  const items = fs.readdirSync(dir);

  for (const item of items) {
    const fullPath = path.join(dir, item);
    const stat = fs.statSync(fullPath);

    if (stat.isDirectory()) {
      findAllMdFiles(fullPath, files);
    } else if (item.endsWith('.md')) {
      files.push(fullPath);
    }
  }

  return files;
}

// 증분 배포용: 변경된 파일만 처리
function parseChangedFiles(changedArg) {
  if (!changedArg) return [];

  return changedArg
    .split(/[\n\s]+/)
    .filter(f => f.trim() && f.startsWith('content/') && f.endsWith('.md'))
    .map(f => path.join(__dirname, '..', f));
}

// 메인 함수
function main() {
  const args = process.argv.slice(2);
  let mdFiles = [];
  let isIncremental = false;

  // 증분 배포 체크
  const changedIdx = args.indexOf('--changed');
  if (changedIdx !== -1 && args[changedIdx + 1]) {
    mdFiles = parseChangedFiles(args[changedIdx + 1]);
    isIncremental = true;
    console.log('🚀 증분 배포 모드');
  } else {
    mdFiles = findAllMdFiles(CONTENT_DIR);
    console.log('🚀 전체 배포 모드');
  }

  console.log(`📁 처리할 파일: ${mdFiles.length}개\n`);

  if (mdFiles.length === 0) {
    console.log('ℹ️  처리할 파일이 없습니다.');
    fs.writeFileSync(path.join(OUTPUT_DIR, 'md-kv-1.json'), '[]');
    return;
  }

  // KV 페어 생성
  const pairs = [];
  let success = 0;
  let failed = 0;

  for (const filePath of mdFiles) {
    try {
      const content = fs.readFileSync(filePath, 'utf-8');
      const kvKey = contentPathToUrlPath(filePath);

      pairs.push({
        key: kvKey,
        value: content
      });

      success++;
    } catch (err) {
      console.error(`❌ 오류: ${filePath} - ${err.message}`);
      failed++;
    }
  }

  console.log(`\n📊 결과: 성공 ${success}개, 실패 ${failed}개`);

  // 배치 파일 생성
  const batchCount = Math.ceil(pairs.length / BATCH_SIZE);
  console.log(`\n📦 배치 파일 생성: ${batchCount}개`);

  for (let i = 0; i < batchCount; i++) {
    const batch = pairs.slice(i * BATCH_SIZE, (i + 1) * BATCH_SIZE);
    const fileName = isIncremental ? 'md-kv-incremental.json' : `md-kv-${i + 1}.json`;
    const filePath = path.join(OUTPUT_DIR, fileName);

    fs.writeFileSync(filePath, JSON.stringify(batch, null, 2));
    console.log(`   ✅ ${fileName} (${batch.length}개 항목)`);

    // 증분 배포는 파일 1개만
    if (isIncremental) break;
  }

  // 배치 개수 저장 (GitHub Actions용)
  if (!isIncremental) {
    fs.writeFileSync(
      path.join(OUTPUT_DIR, 'batch-count.txt'),
      String(batchCount)
    );
    console.log(`\n📝 batch-count.txt: ${batchCount}`);
  }

  console.log('\n✅ KV JSON 생성 완료!');
  console.log('\n📝 업로드 명령어:');

  if (isIncremental) {
    console.log('   npx wrangler kv bulk put "md-kv-incremental.json" --namespace-id 725aefb7b1c64c6c90d2cf4daf061bf3');
  } else {
    for (let i = 1; i <= batchCount; i++) {
      console.log(`   npx wrangler kv bulk put "md-kv-${i}.json" --namespace-id 725aefb7b1c64c6c90d2cf4daf061bf3`);
    }
  }
}

main();
