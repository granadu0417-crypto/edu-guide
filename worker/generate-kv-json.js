/**
 * generate-kv-json.js
 *
 * Hugo 빌드 결과물(public/)을 Cloudflare KV용 JSON 파일로 변환
 *
 * 사용법: node generate-kv-json.js
 * 결과물: kv-data-1.json ~ kv-data-N.json
 */

const fs = require('fs');
const path = require('path');

// 설정
const PUBLIC_DIR = path.join(__dirname, '..', 'public');
const OUTPUT_DIR = __dirname;
const BATCH_SIZE = 1500; // 배치당 파일 수 (Wrangler bulk put 제한 고려)
const MAX_BATCHES = 15; // deploy.yml에 맞춤

// 텍스트 파일 확장자 (KV에 저장할 파일들)
const TEXT_EXTENSIONS = ['.html', '.css', '.js', '.json', '.xml', '.txt', '.svg'];

// 제외할 파일/폴더 패턴
const EXCLUDE_PATTERNS = [
  /\.map$/,           // 소스맵 제외
  /node_modules/,     // node_modules 제외
  /\.git/,            // git 폴더 제외
];

/**
 * 디렉토리를 재귀적으로 스캔하여 모든 파일 경로 반환
 */
function getAllFiles(dirPath, arrayOfFiles = []) {
  const files = fs.readdirSync(dirPath);

  files.forEach((file) => {
    const fullPath = path.join(dirPath, file);

    // 제외 패턴 체크
    if (EXCLUDE_PATTERNS.some(pattern => pattern.test(fullPath))) {
      return;
    }

    if (fs.statSync(fullPath).isDirectory()) {
      arrayOfFiles = getAllFiles(fullPath, arrayOfFiles);
    } else {
      arrayOfFiles.push(fullPath);
    }
  });

  return arrayOfFiles;
}

/**
 * 파일 경로를 KV 키로 변환
 * public/seoul/gangnam/index.html → /seoul/gangnam/index
 */
function pathToKey(filePath) {
  // public/ 경로 제거
  let key = filePath.replace(PUBLIC_DIR, '');

  // Windows 경로 처리
  key = key.replace(/\\/g, '/');

  // .html 확장자 제거 (index.html → index)
  if (key.endsWith('.html')) {
    key = key.replace(/\.html$/, '');
  }

  // 앞에 / 확인
  if (!key.startsWith('/')) {
    key = '/' + key;
  }

  return key;
}

/**
 * 파일이 텍스트 파일인지 확인
 */
function isTextFile(filePath) {
  const ext = path.extname(filePath).toLowerCase();
  return TEXT_EXTENSIONS.includes(ext);
}

/**
 * 메인 함수
 */
function main() {
  console.log('🚀 KV JSON 생성 시작...\n');

  // public 폴더 확인
  if (!fs.existsSync(PUBLIC_DIR)) {
    console.error('❌ public/ 폴더가 없습니다. 먼저 Hugo 빌드를 실행하세요.');
    console.error('   명령어: hugo --minify');
    process.exit(1);
  }

  // 모든 파일 스캔
  console.log('📁 파일 스캔 중...');
  const allFiles = getAllFiles(PUBLIC_DIR);
  console.log(`   총 ${allFiles.length}개 파일 발견\n`);

  // 텍스트 파일만 필터링
  const textFiles = allFiles.filter(isTextFile);
  console.log(`📝 텍스트 파일: ${textFiles.length}개`);
  console.log(`🖼️  바이너리 파일 (제외): ${allFiles.length - textFiles.length}개\n`);

  // KV 데이터 생성
  console.log('🔄 KV 데이터 변환 중...');
  const kvData = [];
  let errorCount = 0;

  textFiles.forEach((filePath) => {
    try {
      const key = pathToKey(filePath);
      const value = fs.readFileSync(filePath, 'utf8');

      kvData.push({ key, value });
    } catch (err) {
      console.error(`   ⚠️ 읽기 실패: ${filePath}`);
      errorCount++;
    }
  });

  console.log(`   ✅ ${kvData.length}개 변환 완료`);
  if (errorCount > 0) {
    console.log(`   ⚠️ ${errorCount}개 실패\n`);
  }

  // 배치로 분할
  console.log('\n📦 배치 파일 생성 중...');
  const batches = [];
  for (let i = 0; i < kvData.length; i += BATCH_SIZE) {
    batches.push(kvData.slice(i, i + BATCH_SIZE));
  }

  // 최대 배치 수 확인
  if (batches.length > MAX_BATCHES) {
    console.warn(`⚠️ 배치 수(${batches.length})가 최대(${MAX_BATCHES})를 초과합니다.`);
    console.warn(`   deploy.yml의 배치 단계를 늘려야 할 수 있습니다.\n`);
  }

  // JSON 파일 저장
  batches.forEach((batch, index) => {
    const fileName = `kv-data-${index + 1}.json`;
    const filePath = path.join(OUTPUT_DIR, fileName);

    fs.writeFileSync(filePath, JSON.stringify(batch, null, 0));

    const sizeMB = (Buffer.byteLength(JSON.stringify(batch)) / 1024 / 1024).toFixed(2);
    console.log(`   ✅ ${fileName}: ${batch.length}개 항목 (${sizeMB} MB)`);
  });

  // 남은 배치 파일은 빈 배열로 생성 (deploy.yml 호환성)
  for (let i = batches.length + 1; i <= MAX_BATCHES; i++) {
    const fileName = `kv-data-${i}.json`;
    const filePath = path.join(OUTPUT_DIR, fileName);
    fs.writeFileSync(filePath, '[]');
    console.log(`   📄 ${fileName}: 빈 파일 (호환성용)`);
  }

  // 요약 출력
  console.log('\n' + '='.repeat(50));
  console.log('📊 요약');
  console.log('='.repeat(50));
  console.log(`총 KV 항목: ${kvData.length}개`);
  console.log(`배치 파일: ${batches.length}개`);
  console.log(`배치당 크기: 최대 ${BATCH_SIZE}개`);

  const totalSize = batches.reduce((acc, batch) => {
    return acc + Buffer.byteLength(JSON.stringify(batch));
  }, 0);
  console.log(`총 데이터 크기: ${(totalSize / 1024 / 1024).toFixed(2)} MB`);

  console.log('\n✅ KV JSON 생성 완료!');
  console.log('   다음 단계: GitHub에 push하면 자동 배포됩니다.\n');
}

// 실행
main();
