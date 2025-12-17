#!/usr/bin/env node
/**
 * 마크다운 직접 배포용 증분 KV JSON 생성기
 * 마지막 배포 이후 변경된 파일만 KV로 변환
 *
 * 사용법:
 *   node generate-incremental-md-kv.js                    # 마지막 배포 이후 변경된 파일
 *   node generate-incremental-md-kv.js --since "2025-12-15 12:22"  # 특정 시간 이후 변경
 *   node generate-incremental-md-kv.js --files "file1.md file2.md" # 특정 파일만
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const CONTENT_DIR = path.join(__dirname, '..', 'content');
const OUTPUT_FILE = path.join(__dirname, 'incremental-md-kv.json');
const LAST_DEPLOY_FILE = path.join(__dirname, 'last-deploy-time.txt');

// 마지막 배포 시간 가져오기
function getLastDeployTime() {
  // 1. last-deploy-time.txt 파일 확인
  if (fs.existsSync(LAST_DEPLOY_FILE)) {
    return fs.readFileSync(LAST_DEPLOY_FILE, 'utf-8').trim();
  }

  // 2. md-kv-1.json 파일 수정 시간 사용
  const mdKvFile = path.join(__dirname, 'md-kv-1.json');
  if (fs.existsSync(mdKvFile)) {
    const stat = fs.statSync(mdKvFile);
    return stat.mtime.toISOString().replace('T', ' ').substring(0, 19);
  }

  // 3. 기본값: 1시간 전
  const oneHourAgo = new Date(Date.now() - 60 * 60 * 1000);
  return oneHourAgo.toISOString().replace('T', ' ').substring(0, 19);
}

// content 경로를 KV 키로 변환
function contentPathToKvKey(contentPath) {
  let key = contentPath
    .replace(CONTENT_DIR, '')
    .replace(/\\/g, '/')
    .replace(/\.md$/, '')
    .replace(/_index$/, '');

  if (!key.startsWith('/')) key = '/' + key;
  if (key === '/') return '/index';

  return key + '/index';
}

// 마크다운 파일 읽기
function readMarkdownFile(filePath) {
  try {
    return fs.readFileSync(filePath, 'utf-8');
  } catch (err) {
    console.warn(`   ⚠️ 파일 읽기 실패: ${filePath}`);
    return null;
  }
}

// 변경된 파일 찾기
function findChangedFiles(sinceTime) {
  const cmd = `find "${CONTENT_DIR}" -name "*.md" -newermt "${sinceTime}" -type f`;
  try {
    const result = execSync(cmd, { encoding: 'utf-8' });
    return result.trim().split('\n').filter(f => f.trim());
  } catch (err) {
    console.error('파일 검색 오류:', err.message);
    return [];
  }
}

function main() {
  const args = process.argv.slice(2);

  let changedFiles = [];
  let sinceTime = '';

  // 인자 파싱
  if (args.includes('--files')) {
    const idx = args.indexOf('--files');
    const filesArg = args[idx + 1] || '';
    changedFiles = filesArg.split(/[\n\s]+/).filter(f => f.trim() && f.endsWith('.md'));
    console.log('🚀 지정된 파일 배포 모드');
  } else if (args.includes('--since')) {
    const idx = args.indexOf('--since');
    sinceTime = args[idx + 1] || getLastDeployTime();
    changedFiles = findChangedFiles(sinceTime);
    console.log(`🚀 증분 배포 모드 (${sinceTime} 이후)`);
  } else {
    // 기본: 마지막 배포 이후 변경된 파일
    sinceTime = getLastDeployTime();
    changedFiles = findChangedFiles(sinceTime);
    console.log(`🚀 증분 배포 모드 (마지막 배포: ${sinceTime})`);
  }

  console.log(`   변경된 파일: ${changedFiles.length}개\n`);

  if (changedFiles.length === 0) {
    console.log('ℹ️  변경된 파일 없음 - 배포 스킵');
    fs.writeFileSync(OUTPUT_FILE, '[]');
    return;
  }

  // KV 페어 생성
  const pairs = [];
  let success = 0;
  let failed = 0;

  for (const filePath of changedFiles) {
    const content = readMarkdownFile(filePath);
    if (!content) {
      failed++;
      continue;
    }

    const kvKey = contentPathToKvKey(filePath);
    pairs.push({ key: kvKey, value: content });
    success++;
  }

  console.log(`📊 결과: 성공 ${success}개, 실패 ${failed}개`);

  // JSON 파일 생성
  if (pairs.length > 0) {
    fs.writeFileSync(OUTPUT_FILE, JSON.stringify(pairs, null, 2));
    console.log(`\n✅ ${path.basename(OUTPUT_FILE)} 생성 완료 (${pairs.length}개 항목)`);
    console.log('\n📝 업로드 명령어:');
    console.log('   npx wrangler kv bulk put "incremental-md-kv.json" --namespace-id 725aefb7b1c64c6c90d2cf4daf061bf3');
    console.log('\n⏰ 배포 후 시간 기록:');
    console.log('   echo "$(date +\'%Y-%m-%d %H:%M:%S\')" > last-deploy-time.txt');
  } else {
    fs.writeFileSync(OUTPUT_FILE, '[]');
    console.log('\nℹ️  업로드할 항목 없음');
  }
}

main();
