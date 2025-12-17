const fs = require('fs');
const path = require('path');

// 랜딩 페이지 HTML 파일 읽기
const visitTutoringHtml = fs.readFileSync(path.join(__dirname, 'visit-tutoring.html'), 'utf8');
const onlineTutoringHtml = fs.readFileSync(path.join(__dirname, 'online-tutoring.html'), 'utf8');

// KV JSON 데이터 생성
const kvData = [
    {
        key: "/visit-tutoring/index",
        value: visitTutoringHtml
    },
    {
        key: "/online-tutoring/index",
        value: onlineTutoringHtml
    }
];

// JSON 파일로 저장
fs.writeFileSync(
    path.join(__dirname, 'landing-pages-kv.json'),
    JSON.stringify(kvData, null, 2),
    'utf8'
);

console.log('✅ landing-pages-kv.json 생성 완료!');
console.log(`   - /visit-tutoring/index (${visitTutoringHtml.length} bytes)`);
console.log(`   - /online-tutoring/index (${onlineTutoringHtml.length} bytes)`);
