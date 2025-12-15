#!/usr/bin/env node
/**
 * 증분 배포용 KV JSON 생성기
 * 변경된 content 파일에 해당하는 HTML만 KV로 변환
 *
 * 사용법:
 *   node generate-incremental-kv.js "content/seoul/file1.md content/seoul/file2.md"
 *   또는
 *   node generate-incremental-kv.js --all  (전체 배포)
 */

const fs = require('fs');
const path = require('path');

const PUBLIC_DIR = path.join(__dirname, '..', 'public');
const OUTPUT_FILE = path.join(__dirname, 'kv-incremental.json');

// content/seoul/gangnam/gangnam-gu-math.md -> /seoul/gangnam/gangnam-gu-math/
function contentPathToUrlPath(contentPath) {
  // content/ 제거
  let urlPath = contentPath.replace(/^content\//, '');
  // .md 제거
  urlPath = urlPath.replace(/\.md$/, '');
  // _index 처리
  urlPath = urlPath.replace(/_index$/, '');
  // index 처리
  if (urlPath.endsWith('/index')) {
    urlPath = urlPath.replace(/\/index$/, '');
  }

  return '/' + urlPath;
}

// URL 경로 -> public/ 내 HTML 파일 경로
function urlPathToPublicFile(urlPath) {
  // / -> /index.html
  // /seoul/ -> /seoul/index.html
  // /seoul/gangnam -> /seoul/gangnam/index.html

  let htmlPath = urlPath;
  if (htmlPath === '' || htmlPath === '/') {
    htmlPath = '/index.html';
  } else if (!htmlPath.endsWith('.html') && !htmlPath.endsWith('.xml') && !htmlPath.endsWith('.json')) {
    htmlPath = htmlPath + '/index.html';
  }

  return path.join(PUBLIC_DIR, htmlPath);
}

// KV 키 생성 (기존 로직과 동일)
function getKVKey(urlPath) {
  let key = urlPath;

  // 끝에 / 없으면 추가 후 index 붙이기
  if (key === '' || key === '/') {
    return '/index';
  }

  // /seoul/gangnam -> /seoul/gangnam/index
  if (!key.endsWith('/')) {
    key = key + '/index';
  } else {
    key = key + 'index';
  }

  return key;
}

function main() {
  const args = process.argv.slice(2);

  // --all 옵션이면 전체 배포
  if (args.includes('--all')) {
    console.log('⚠️  전체 배포 모드 - 기존 generate-kv-json.js 사용 권장');
    process.exit(0);
  }

  // 변경된 파일 목록 파싱
  const changedFilesArg = args[0] || '';
  const changedFiles = changedFilesArg
    .split(/[\n\s]+/)
    .filter(f => f.trim() && f.startsWith('content/') && f.endsWith('.md'));

  if (changedFiles.length === 0) {
    console.log('ℹ️  변경된 content 파일 없음 - 배포 스킵');
    // 빈 파일 생성 (워크플로우에서 체크용)
    fs.writeFileSync(OUTPUT_FILE, '[]');
    process.exit(0);
  }

  console.log('🚀 증분 KV JSON 생성기');
  console.log(`   변경된 파일: ${changedFiles.length}개`);
  console.log('');

  // 변경된 파일들 출력
  console.log('📝 변경된 content 파일:');
  changedFiles.forEach(f => console.log(`   - ${f}`));
  console.log('');

  // KV 페어 생성
  const pairs = [];
  let success = 0;
  let failed = 0;

  for (const contentPath of changedFiles) {
    try {
      const urlPath = contentPathToUrlPath(contentPath);
      const publicFile = urlPathToPublicFile(urlPath);
      const kvKey = getKVKey(urlPath);

      // public/ 파일이 존재하는지 확인
      if (!fs.existsSync(publicFile)) {
        console.warn(`   ⚠️ HTML 없음: ${publicFile}`);
        failed++;
        continue;
      }

      const content = fs.readFileSync(publicFile, 'utf-8');
      pairs.push({ key: kvKey, value: content });
      console.log(`   ✅ ${contentPath} -> ${kvKey}`);
      success++;

    } catch (err) {
      console.warn(`   ❌ 오류: ${contentPath} - ${err.message}`);
      failed++;
    }
  }

  console.log('');
  console.log(`📊 결과: 성공 ${success}개, 실패 ${failed}개`);

  // JSON 파일 생성
  if (pairs.length > 0) {
    fs.writeFileSync(OUTPUT_FILE, JSON.stringify(pairs, null, 2));
    console.log(`\n✅ ${OUTPUT_FILE} 생성 완료 (${pairs.length}개 항목)`);
    console.log('\n📝 업로드 명령어:');
    console.log('   npx wrangler kv bulk put "kv-incremental.json" --namespace-id 725aefb7b1c64c6c90d2cf4daf061bf3');
  } else {
    fs.writeFileSync(OUTPUT_FILE, '[]');
    console.log('\nℹ️  업로드할 항목 없음');
  }
}

main();
