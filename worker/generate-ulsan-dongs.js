const fs = require('fs');
const path = require('path');

// 울산시 추가할 동 단위
const ulsanNewDongs = {
  jung_us: [
    { slug: 'byeongyeong', nameKr: '병영동' },
    { slug: 'seodong', nameKr: '서동' }
  ],
  nam_us: [
    { slug: 'daehyeon', nameKr: '대현동' },
    { slug: 'namhwa', nameKr: '남화동' },
    { slug: 'suam', nameKr: '수암동' },
    { slug: 'duwang', nameKr: '두왕동' },
    { slug: 'seonam', nameKr: '선암동' }
  ],
  dong_us: [
    { slug: 'dongbu', nameKr: '동부동' },
    { slug: 'seobu', nameKr: '서부동' },
    { slug: 'nammok', nameKr: '남목동' }
  ],
  buk_us: [
    { slug: 'maegok', nameKr: '매곡동' },
    { slug: 'hwabong', nameKr: '화봉동' },
    { slug: 'cheongok', nameKr: '천곡동' },
    { slug: 'sincheon', nameKr: '신천동' },
    { slug: 'jungsan', nameKr: '중산동' }
  ]
};

const guNames = {
  jung_us: '중구',
  nam_us: '남구',
  dong_us: '동구',
  buk_us: '북구'
};

const contentTypes = [
  { slug: 'high-math', title: '고등 수학과외', level: '고등학생', subject: '수학', category: '고등교육' },
  { slug: 'high-english', title: '고등 영어과외', level: '고등학생', subject: '영어', category: '고등교육' },
  { slug: 'middle-math', title: '중등 수학과외', level: '중학생', subject: '수학', category: '중등교육' },
  { slug: 'middle-english', title: '중등 영어과외', level: '중학생', subject: '영어', category: '중등교육' }
];

const images = [
  'photo-1503676260728-1c00da094a0b',
  'photo-1522202176988-66273c2fd55f',
  'photo-1523240795612-9a054b0db644',
  'photo-1517842645767-c639042777db',
  'photo-1513258496099-48168024aec0'
];

function generateIndex(gu, dong, idx) {
  const guName = guNames[gu];

  return `---
title: "울산 ${guName} ${dong.nameKr} 과외 | 수학·영어 1:1 맞춤 수업"
date: 2025-01-28
categories:
  - 울산
regions:
  - 울산
cities:
  - 울산시
description: "울산 ${guName} ${dong.nameKr} 초중고 과외를 찾으신다면! 수학, 영어 전문 과외 선생님이 1:1 맞춤 수업을 제공합니다."
tags:
  - ${dong.nameKr}과외
  - ${guName}과외
  - 울산과외
featured_image: "https://images.unsplash.com/${images[idx % images.length]}?w=1200&h=630&fit=crop"
---

울산 ${guName} ${dong.nameKr}에서 과외 선생님을 찾고 계신가요?

${dong.nameKr} 지역 학생들을 위한 1:1 맞춤 과외 수업을 제공합니다. 초등학생부터 고등학생까지, 수학과 영어 전문 선생님이 학생 개개인의 수준에 맞춰 수업합니다.

## ${dong.nameKr} 과외의 특징

${guName} ${dong.nameKr}은 교육열이 높은 지역입니다. 주변 학교 학생들의 학습 수준이 높아 내신 경쟁이 치열합니다. 이런 환경에서 좋은 성적을 받으려면 체계적인 학습 관리가 필요합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
${dong.nameKr} 지역 학교별 내신 출제 경향을 분석하여 수업합니다. 학교 시험 2주 전부터 집중 대비 수업을 진행합니다.
</div>

## 과외 과목

저희는 ${dong.nameKr}에서 다양한 과목의 과외를 제공합니다.

**수학**: 초등 연산부터 고등 수학까지, 개념 이해와 문제 풀이 능력을 함께 키워드립니다.

**영어**: 문법, 독해, 듣기, 말하기 모든 영역을 균형 있게 학습합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
주 1-2회 정기 수업으로 기본기를 다지고, 시험 기간에는 추가 수업으로 완벽 대비합니다.
</div>

## 수업 방식

1:1 개인 과외로 진행됩니다. 학생의 집 또는 스터디카페에서 수업이 가능합니다.

**방문 과외**: 선생님이 직접 방문하여 수업합니다. 이동 시간을 절약하고 편안한 환경에서 공부할 수 있습니다.

**온라인 과외**: 화상 수업으로 언제 어디서나 수업 가능합니다. 녹화 기능으로 복습도 가능합니다.

## 수업료 안내

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
첫 상담 시 학생 수준 진단 후 맞춤 커리큘럼을 제안드립니다. 수업료는 학년, 과목, 횟수에 따라 달라집니다.
</div>

**중학생** 기준 주1회 22만원 - 32만원, 주2회 29만원 - 47만원 선입니다.

**고1-2** 기준 주1회 25만원 - 36만원, 주2회 33만원 - 53만원 선입니다.

**고3** 기준 주1회 28만원 - 40만원, 주2회 37만원 - 59만원이 일반적입니다.

## 자주 묻는 질문

**Q. 선생님은 어떻게 매칭되나요?**

학생의 성향, 학습 목표, 선호 스타일을 고려하여 최적의 선생님을 매칭해 드립니다. 첫 수업 후 변경도 가능합니다.

**Q. 수업 시간과 장소는 어떻게 정하나요?**

학생과 선생님이 협의하여 정합니다. ${dong.nameKr} 내 학생 집, 스터디카페, 도서관 등에서 수업 가능합니다.

**Q. 시험 기간에 추가 수업이 가능한가요?**

네, 가능합니다. 정기 수업 외에 시험 대비 추가 수업을 신청하실 수 있습니다.

{{< cta-dual type="final" >}}

## 마무리

울산 ${guName} ${dong.nameKr}에서 과외를 찾고 계신다면 지금 상담 신청하세요. 학생에게 딱 맞는 선생님을 소개해 드리겠습니다. 첫 상담은 무료입니다.
`;
}

function generateSubjectContent(gu, dong, type, idx) {
  const guName = guNames[gu];
  const isHigh = type.slug.includes('high');
  const isMath = type.slug.includes('math');

  return `---
title: "울산 ${guName} ${dong.nameKr} ${type.level} ${type.subject}과외 | 내신·수능 대비"
date: 2025-01-28
categories:
  - ${type.category}
regions:
  - 울산
cities:
  - 울산시
description: "울산 ${guName} ${dong.nameKr} ${type.level} ${type.subject} 과외입니다. 1:1 맞춤 수업으로 내신과 수능을 완벽 대비합니다."
tags:
  - ${dong.nameKr} ${type.subject}과외
  - ${guName} ${type.subject}과외
  - 울산 ${type.subject}과외
  - ${type.level} ${type.subject}
featured_image: "https://images.unsplash.com/${images[(idx + (isMath ? 1 : 2)) % images.length]}?w=1200&h=630&fit=crop"
---

울산 ${guName} ${dong.nameKr}에서 ${type.level} ${type.subject} 과외를 찾고 계신가요?

${dong.nameKr} 지역 ${type.level}을 위한 ${type.subject} 전문 과외입니다. ${isHigh ? '고등학교' : '중학교'} ${type.subject}은 ${isMath ? '개념 이해와 문제 풀이 능력이 함께 필요합니다' : '독해력과 문법 실력이 기본이 되어야 합니다'}.

## ${dong.nameKr} ${type.level} ${type.subject}의 특징

${guName} ${dong.nameKr} 주변 학교들은 ${type.subject} 시험 난이도가 ${isHigh ? '상당히 높은 편입니다' : '점점 높아지고 있습니다'}. ${isMath ? '서술형 문제 비중이 높고, 응용 문제가 많이 출제됩니다.' : '지문 길이가 길고, 어휘 수준이 높습니다.'}

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
학교별 기출 문제를 분석하여 출제 경향을 파악합니다. ${type.subject} 내신 ${isMath ? '만점' : '1등급'}을 목표로 체계적으로 준비합니다.
</div>

## ${type.subject} 수업 커리큘럼

${isMath ? `
**개념 학습**: 교과서와 개념서를 병행하여 기초부터 탄탄하게 다집니다.

**유형 연습**: 자주 출제되는 유형을 반복 학습합니다. 실수를 줄이는 훈련을 합니다.

**심화 학습**: 고난도 문제에 도전합니다. 사고력을 키우는 문제를 풉니다.

**서술형 대비**: 서술형 답안 작성법을 훈련합니다. 부분 점수 전략도 알려드립니다.
` : `
**독해 훈련**: 다양한 지문을 읽고 핵심을 파악하는 훈련을 합니다.

**문법 정리**: ${isHigh ? '수능' : '내신'}에 자주 나오는 문법을 정리합니다. 헷갈리는 부분을 확실히 짚어드립니다.

**어휘 확장**: 매 수업 어휘 테스트를 진행합니다. 어휘력이 독해의 기본입니다.

**듣기 연습**: ${isHigh ? '수능 듣기 유형을 분석하고 연습합니다.' : '듣기 평가 대비 훈련을 합니다.'}
`}

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
${isMath ? '틀린 문제는 왜 틀렸는지 분석하고, 비슷한 유형을 반복 연습합니다.' : '독해 지문은 해석 후 구문 분석까지 꼼꼼하게 진행합니다.'}
</div>

## 학년별 ${type.subject} 전략

${isHigh ? `
**고1**: ${isMath ? '고등 수학의 기초인 수학(상), 수학(하)를 확실히 다집니다.' : '고등 영어 문법과 독해의 기초를 다집니다.'}

**고2**: ${isMath ? '수학I, 수학II를 학습하며 수능 기출을 병행합니다.' : '본격적인 수능 대비를 시작합니다. 독해 속도를 높입니다.'}

**고3**: ${isMath ? '선택과목(확률과통계, 미적분, 기하) 완성과 수능 파이널 준비.' : '수능 실전 연습과 파이널 정리에 집중합니다.'}
` : `
**중1**: ${isMath ? '정수, 방정식, 함수의 기초를 다집니다. 초등에서 연결되는 개념을 점검합니다.' : '기초 문법과 기본 어휘를 다집니다.'}

**중2**: ${isMath ? '도형, 확률, 함수 심화 학습. 서술형 대비를 시작합니다.' : '문법이 복잡해지는 시기입니다. 독해 실력도 함께 키웁니다.'}

**중3**: ${isMath ? '고등 선행과 내신을 병행합니다. 고입 대비도 진행합니다.' : '고등 영어 준비와 내신 완성을 동시에 합니다.'}
`}

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
학생의 현재 수준을 정확히 진단한 후 맞춤 커리큘럼을 구성합니다. 무리한 선행보다 현행 완성이 먼저입니다.
</div>

## ${type.subject} 수업료

${isHigh ? `
**고1-2** 기준 주1회 25만원 - 36만원, 주2회 33만원 - 53만원 선입니다.

**고3** 기준 주1회 28만원 - 40만원, 주2회 37만원 - 59만원이 일반적입니다.
` : `
**중학생** 기준 주1회 22만원 - 32만원, 주2회 29만원 - 47만원 선입니다.
`}

수업료는 학생 수준, 목표, 수업 횟수에 따라 달라질 수 있습니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
첫 상담에서 학생 상황을 파악하고 적정 수업 횟수와 수업료를 안내드립니다.
</div>

## 자주 묻는 질문

**Q. ${type.subject} 선생님은 어떤 분인가요?**

${isMath ? '수학 전공자, 수능 1등급 출신, 교육 경력 3년 이상의 선생님입니다.' : '영어 전공자, 토익·토플 고득점, 해외 경험이 있는 선생님입니다.'}

**Q. 성적이 많이 낮은데 괜찮을까요?**

물론입니다. 기초부터 차근차근 잡아드립니다. 현재 수준이 어디든 상관없습니다.

**Q. ${isHigh ? '수능' : '내신'}만 준비하면 되나요?**

${isHigh ? '내신과 수능 비중은 학생의 목표와 상황에 따라 조절합니다.' : '내신 위주로 수업하지만, 고등 대비도 함께 진행합니다.'}

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
${dong.nameKr} 지역 학생들의 목표와 상황에 맞춰 유연하게 수업합니다.
</div>

{{< cta-dual type="final" >}}

## 마무리

울산 ${guName} ${dong.nameKr} ${type.level} ${type.subject} 과외, 지금 시작하세요. 체계적인 학습 관리로 ${isMath ? '수학 실력 향상' : '영어 성적 향상'}을 도와드리겠습니다.
`;
}

// 메인 실행
const contentDir = path.join(__dirname, '..', 'content', 'ulsan');
let createdCount = 0;

for (const [gu, dongs] of Object.entries(ulsanNewDongs)) {
  for (let i = 0; i < dongs.length; i++) {
    const dong = dongs[i];
    const dongDir = path.join(contentDir, gu, dong.slug);

    if (!fs.existsSync(dongDir)) {
      fs.mkdirSync(dongDir, { recursive: true });
    }

    // _index.md
    fs.writeFileSync(
      path.join(dongDir, '_index.md'),
      generateIndex(gu, dong, i)
    );
    createdCount++;

    // 과목별 파일
    for (let j = 0; j < contentTypes.length; j++) {
      const type = contentTypes[j];
      fs.writeFileSync(
        path.join(dongDir, `${type.slug}.md`),
        generateSubjectContent(gu, dong, type, i + j)
      );
      createdCount++;
    }
  }
}

console.log(`생성 완료: ${createdCount}개 파일`);
console.log('중구: +2동 (병영동, 서동)');
console.log('남구: +5동 (대현동, 남화동, 수암동, 두왕동, 선암동)');
console.log('동구: +3동 (동부동, 서부동, 남목동)');
console.log('북구: +5동 (매곡동, 화봉동, 천곡동, 신천동, 중산동)');
console.log('총: 15동 x 5파일 = 75파일');
