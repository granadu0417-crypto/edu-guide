const fs = require('fs');
const path = require('path');

// 추가할 도시 정보
const newCities = {
  gangwon: {
    taebaek: {
      name: '태백시',
      schools: ['태백고', '황지고', '태백기계공고'],
      middleSchools: ['태백중', '황지중', '장성중']
    }
  },
  gyeongbuk: {
    yeongju: {
      name: '영주시',
      schools: ['영주고', '영광고', '제일고'],
      middleSchools: ['영주중', '영광중', '순흥중']
    },
    sangju: {
      name: '상주시',
      schools: ['상주고', '상산고', '상주여고'],
      middleSchools: ['상주중', '동성중', '함창중']
    }
  },
  gyeongnam: {
    miryang: {
      name: '밀양시',
      schools: ['밀양고', '삼문고', '세종고'],
      middleSchools: ['밀양중', '삼문중', '밀성중']
    },
    sacheon: {
      name: '사천시',
      schools: ['사천고', '삼천포고', '사천여고'],
      middleSchools: ['사천중', '삼천포중', '용산중']
    }
  },
  jeonbuk: {
    namwon: {
      name: '남원시',
      schools: ['남원고', '용성고', '한국부흥고'],
      middleSchools: ['남원중', '용성중', '금지중']
    },
    gimje: {
      name: '김제시',
      schools: ['김제고', '김제여고', '김제농공고'],
      middleSchools: ['김제중', '김제여중', '금구중']
    }
  },
  jeonnam: {
    naju: {
      name: '나주시',
      schools: ['나주고', '빛고을고', '금성고'],
      middleSchools: ['나주중', '영산중', '금성중']
    }
  }
};

// 서두 변형 풀
const introPool = {
  math: [
    '수학 성적, 지금부터 바꿀 수 있습니다.',
    '수학이 어렵다면 방법을 바꿔보세요.',
    '기초부터 차근차근, 수학 실력을 키워드립니다.',
    '수학 자신감, 올바른 방법으로 만들어갑니다.',
    '포기하기엔 이릅니다. 수학은 노력의 과목입니다.',
    '수학의 즐거움을 찾아드립니다.',
    '개념이 잡히면 문제가 보입니다.',
    '수학 고민, 함께 해결해 드립니다.'
  ],
  english: [
    '영어 실력, 꾸준함이 답입니다.',
    '영어가 어렵다면 방법을 바꿔보세요.',
    '기초부터 탄탄하게, 영어 실력을 완성합니다.',
    '영어 자신감, 체계적인 학습으로 만들어갑니다.',
    '영어는 매일의 습관입니다.',
    '독해의 즐거움을 찾아드립니다.',
    '문법이 잡히면 문장이 보입니다.',
    '영어 고민, 함께 풀어나갑니다.'
  ]
};

// 이미지 풀
const imagePool = [
  'photo-1503676260728-1c00da094a0b',
  'photo-1522202176988-66273c2fd55f',
  'photo-1523240795612-9a054b0db644',
  'photo-1517842645767-c639042777db',
  'photo-1513258496099-48168024aec0',
  'photo-1427504494785-3a9ca7044f45',
  'photo-1571260899304-425eee4c7efc',
  'photo-1519406596751-0a3ccc4937fe'
];

let imageIndex = 0;
const getImage = () => {
  const img = imagePool[imageIndex % imagePool.length];
  imageIndex++;
  return `https://images.unsplash.com/${img}?w=1200&h=630&fit=crop`;
};

// 고등 수학 템플릿
const highMathTemplate = (city, schools) => {
  const intro = introPool.math[Math.floor(Math.random() * introPool.math.length)];
  const schoolList = schools.join('·');
  return `---
title: "${city.name} 고등 수학과외 | ${schoolList} 내신 대비"
date: 2025-12-17
description: "${city.name} 고등학생 수학과외 전문. ${schoolList} 등 내신 맞춤 관리."
featured_image: "${getImage()}"
categories:
  - 고등교육
  - 수학과외
tags:
  - ${city.name}수학과외
  - ${city.name}고등수학
---
${intro}

${city.name}에서 수학과외를 찾는 학부모님들의 공통된 고민입니다. ${schools[0]}, ${schools[1]} 시험에서 함수와 미적분 문제가 자주 출제됩니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
학생의 현재 실력을 정확히 파악합니다. 어디서 막히는지 찾아냅니다.
</div>

## 고등 수학이 어려운 이유

### 추상적 개념의 증가

고등학교 수학은 눈에 보이지 않는 개념을 다룹니다. 함수, 극한, 미분의 개념이 핵심입니다.

### 복합적 사고력 요구

${city.name} 학생들 사이에서 수학 경쟁이 치열합니다. 여러 개념을 연결하는 능력이 필요합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
문제를 많이 푸는 것보다 개념을 깊이 이해하는 게 중요합니다.
</div>

## 학교별 수학 시험 특성

### ${schools[0]}

${city.name} 대표 학교입니다. 수학 시험 난이도가 높은 편입니다. 심화 문제 대비가 필요합니다.

### ${schools[1]}

${city.name}에 위치한 학교입니다. 기본 개념과 응용을 고르게 출제합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
내신 시험은 학교마다 다릅니다. 기출 분석이 핵심입니다.
</div>

## 과외가 필요한 이유

학원은 공식을 알려줍니다. 과외는 적용력을 훈련합니다.

수학은 이해의 과목입니다. 1:1로 막히는 부분을 정확히 짚어야 합니다.

## 학년별 학습 방향

### 고1

수학의 기본기를 다집니다. 중학 수학 복습과 함께 고등 개념을 익힙니다.

### 고2

핵심 단원을 완성합니다. 미적분, 확률과 통계를 집중 학습합니다.

### 고3

실전 감각을 키웁니다. 모의고사와 수능 대비를 병행합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
시험 3주 전부터는 내신에 집중합니다.
</div>

{{< cta-dual type="final" >}}

## 수업료 안내

${city.name} 고등 수학과외 비용입니다.

**고1-2**는 주1회 25만원 - 36만원, 주2회 33만원 - 53만원 선입니다.

**고3**은 주1회 28만원 - 40만원, 주2회 37만원 - 59만원이 일반적입니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
상담에서 기초 문제를 풀어봅니다. 현재 실력을 파악하고 방향을 정합니다.
</div>

## 자주 묻는 질문

**Q. 수학 기초가 부족한데 따라갈 수 있나요?**

가능합니다. 기초부터 차근차근 잡아드립니다.

**Q. 수학 실력이 늘려면 얼마나 걸리나요?**

집중해서 훈련하면 2-3개월 안에 변화가 느껴집니다.

**Q. 과외 횟수는 어떻게 정하나요?**

학생 상황에 따라 다릅니다. 기초가 부족하면 주2회, 유지 목적이면 주1회를 권장합니다.

**Q. 시험 기간에만 과외 가능한가요?**

가능합니다. 시험 2-3주 전부터 집중 수업을 진행합니다.

## 마무리

${city.name} 학생 여러분, 수학은 포기가 아닌 정복의 과목입니다.
`;
};

// 고등 영어 템플릿
const highEnglishTemplate = (city, schools) => {
  const intro = introPool.english[Math.floor(Math.random() * introPool.english.length)];
  const schoolList = schools.join('·');
  return `---
title: "${city.name} 고등 영어과외 | ${schoolList} 내신 대비"
date: 2025-12-17
description: "${city.name} 고등학생 영어과외 전문. ${schoolList} 등 내신 맞춤 관리."
featured_image: "${getImage()}"
categories:
  - 고등교육
  - 영어과외
tags:
  - ${city.name}영어과외
  - ${city.name}고등영어
---
${intro}

${city.name}에서 영어과외를 찾는 학부모님들의 공통된 고민입니다. ${schools[0]}, ${schools[1]} 시험에서 독해와 문법 문제가 중요합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
학생의 영어 실력을 정확히 진단합니다. 취약 영역을 파악합니다.
</div>

## 고등 영어가 어려운 이유

### 지문 길이와 난이도 증가

고등학교 영어는 긴 지문을 빠르게 읽고 이해해야 합니다. 독해 속도와 정확도가 핵심입니다.

### 복잡한 문법 구조

${city.name} 학생들 사이에서 영어 경쟁이 치열합니다. 복잡한 문장 구조 분석이 필요합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
단어 암기보다 문맥 파악 능력을 키웁니다.
</div>

## 학교별 영어 시험 특성

### ${schools[0]}

${city.name} 대표 학교입니다. 영어 시험에서 독해 비중이 높습니다.

### ${schools[1]}

${city.name}에 위치한 학교입니다. 문법과 어휘를 균형있게 출제합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
내신 시험은 학교마다 다릅니다. 교과서 완벽 분석이 핵심입니다.
</div>

## 과외가 필요한 이유

학원은 많은 학생을 가르칩니다. 과외는 1:1로 집중 케어합니다.

영어는 꾸준함의 과목입니다. 매일 조금씩 실력을 쌓아야 합니다.

## 학년별 학습 방향

### 고1

기본 문법을 완성합니다. 독해의 기초를 다집니다.

### 고2

심화 독해를 훈련합니다. 수능형 문제에 적응합니다.

### 고3

실전 감각을 완성합니다. 수능과 내신을 병행합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
시험 3주 전부터는 내신에 집중합니다.
</div>

{{< cta-dual type="final" >}}

## 수업료 안내

${city.name} 고등 영어과외 비용입니다.

**고1-2**는 주1회 25만원 - 36만원, 주2회 33만원 - 53만원 선입니다.

**고3**은 주1회 28만원 - 40만원, 주2회 37만원 - 59만원이 일반적입니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
상담에서 독해 지문을 읽어봅니다. 현재 실력을 파악하고 방향을 정합니다.
</div>

## 자주 묻는 질문

**Q. 영어 기초가 부족한데 따라갈 수 있나요?**

가능합니다. 기초부터 차근차근 잡아드립니다.

**Q. 영어 실력이 늘려면 얼마나 걸리나요?**

꾸준히 훈련하면 2-3개월 안에 변화가 느껴집니다.

**Q. 과외 횟수는 어떻게 정하나요?**

학생 상황에 따라 다릅니다. 기초가 부족하면 주2회, 유지 목적이면 주1회를 권장합니다.

**Q. 시험 기간에만 과외 가능한가요?**

가능합니다. 시험 2-3주 전부터 집중 수업을 진행합니다.

## 마무리

${city.name} 학생 여러분, 영어는 꾸준함이 답입니다.
`;
};

// 중등 수학 템플릿
const middleMathTemplate = (city, schools) => {
  const intro = introPool.math[Math.floor(Math.random() * introPool.math.length)];
  const schoolList = schools.join('·');
  return `---
title: "${city.name} 중등 수학과외 | ${schoolList} 내신 대비"
date: 2025-12-17
description: "${city.name} 중학생 수학과외 전문. ${schoolList} 등 내신 맞춤 관리."
featured_image: "${getImage()}"
categories:
  - 중등교육
  - 수학과외
tags:
  - ${city.name}중등수학
  - ${city.name}수학과외
---
${intro}

${city.name}에서 수학과외를 찾는 학부모님들의 공통된 고민입니다. ${schools[0]}, ${schools[1]} 시험에서 방정식과 함수 문제가 자주 출제됩니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
학생의 현재 실력을 정확히 파악합니다. 어디서 막히는지 찾아냅니다.
</div>

## 중등 수학이 어려운 이유

### 추상적 개념의 시작

중학교 수학은 문자와 식이 등장합니다. 방정식, 함수의 개념이 핵심입니다.

### 논리적 사고력 요구

${city.name} 학생들 사이에서 수학 경쟁이 치열합니다. 단계별 문제 해결 능력이 필요합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
개념을 확실히 이해한 후 문제를 풉니다.
</div>

## 학교별 수학 시험 특성

### ${schools[0]}

${city.name} 대표 학교입니다. 수학 시험에서 서술형 비중이 높습니다.

### ${schools[1]}

${city.name}에 위치한 학교입니다. 기본 개념과 응용을 고르게 출제합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
내신 시험은 학교마다 다릅니다. 기출 분석이 핵심입니다.
</div>

## 과외가 필요한 이유

학원은 진도를 나갑니다. 과외는 이해를 확인합니다.

수학은 기초가 중요합니다. 1:1로 빈틈없이 채워야 합니다.

## 학년별 학습 방향

### 중1

정수와 유리수를 완벽히 익힙니다. 문자와 식의 기초를 다집니다.

### 중2

일차함수를 완성합니다. 도형의 성질을 이해합니다.

### 중3

이차방정식과 이차함수를 익힙니다. 고등 수학 준비를 시작합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
시험 3주 전부터는 내신에 집중합니다.
</div>

{{< cta-dual type="final" >}}

## 수업료 안내

${city.name} 중등 수학과외 비용입니다.

**중학생**은 주1회 22만원 - 32만원, 주2회 29만원 - 47만원 선입니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
상담에서 기초 문제를 풀어봅니다. 현재 실력을 파악하고 방향을 정합니다.
</div>

## 자주 묻는 질문

**Q. 수학 기초가 부족한데 따라갈 수 있나요?**

가능합니다. 기초부터 차근차근 잡아드립니다.

**Q. 수학 실력이 늘려면 얼마나 걸리나요?**

집중해서 훈련하면 2-3개월 안에 변화가 느껴집니다.

**Q. 과외 횟수는 어떻게 정하나요?**

학생 상황에 따라 다릅니다. 기초가 부족하면 주2회, 유지 목적이면 주1회를 권장합니다.

## 마무리

${city.name} 학생 여러분, 중학교 수학이 고등 수학의 기초입니다.
`;
};

// 중등 영어 템플릿
const middleEnglishTemplate = (city, schools) => {
  const intro = introPool.english[Math.floor(Math.random() * introPool.english.length)];
  const schoolList = schools.join('·');
  return `---
title: "${city.name} 중등 영어과외 | ${schoolList} 내신 대비"
date: 2025-12-17
description: "${city.name} 중학생 영어과외 전문. ${schoolList} 등 내신 맞춤 관리."
featured_image: "${getImage()}"
categories:
  - 중등교육
  - 영어과외
tags:
  - ${city.name}중등영어
  - ${city.name}영어과외
---
${intro}

${city.name}에서 영어과외를 찾는 학부모님들의 공통된 고민입니다. ${schools[0]}, ${schools[1]} 시험에서 문법과 독해 문제가 중요합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
학생의 영어 실력을 정확히 진단합니다. 취약 영역을 파악합니다.
</div>

## 중등 영어가 어려운 이유

### 문법의 복잡성 증가

중학교 영어는 시제, 수동태 등 복잡한 문법이 등장합니다.

### 어휘량 증가

${city.name} 학생들 사이에서 영어 경쟁이 치열합니다. 암기해야 할 단어가 많아집니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
단순 암기가 아닌 이해 중심 학습을 합니다.
</div>

## 학교별 영어 시험 특성

### ${schools[0]}

${city.name} 대표 학교입니다. 영어 시험에서 교과서 본문 비중이 높습니다.

### ${schools[1]}

${city.name}에 위치한 학교입니다. 문법과 어휘를 균형있게 출제합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
내신 시험은 학교마다 다릅니다. 교과서 완벽 분석이 핵심입니다.
</div>

## 과외가 필요한 이유

학원은 많은 학생을 가르칩니다. 과외는 1:1로 집중 케어합니다.

영어는 기초가 중요합니다. 중학교 때 기초를 잡아야 합니다.

## 학년별 학습 방향

### 중1

기본 문법을 익힙니다. 문장 구조를 이해합니다.

### 중2

심화 문법을 배웁니다. 독해 기초를 다집니다.

### 중3

문법을 완성합니다. 고등 영어 준비를 시작합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
시험 3주 전부터는 내신에 집중합니다.
</div>

{{< cta-dual type="final" >}}

## 수업료 안내

${city.name} 중등 영어과외 비용입니다.

**중학생**은 주1회 22만원 - 32만원, 주2회 29만원 - 47만원 선입니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
상담에서 독해 지문을 읽어봅니다. 현재 실력을 파악하고 방향을 정합니다.
</div>

## 자주 묻는 질문

**Q. 영어 기초가 부족한데 따라갈 수 있나요?**

가능합니다. 기초부터 차근차근 잡아드립니다.

**Q. 영어 실력이 늘려면 얼마나 걸리나요?**

꾸준히 훈련하면 2-3개월 안에 변화가 느껴집니다.

**Q. 과외 횟수는 어떻게 정하나요?**

학생 상황에 따라 다릅니다. 기초가 부족하면 주2회, 유지 목적이면 주1회를 권장합니다.

## 마무리

${city.name} 학생 여러분, 중학교 영어가 고등 영어의 기초입니다.
`;
};

// 인덱스 템플릿
const indexTemplate = (city) => {
  return `---
title: "${city.name} 과외 | 중고등 수학·영어 전문"
date: 2025-12-17
description: "${city.name} 중고등학생 과외 전문. 수학, 영어 1:1 맞춤 수업."
---
${city.name}에서 과외 선생님을 찾고 계신가요?

검증된 선생님과 함께 성적 향상을 경험하세요.

## ${city.name} 과외 안내

- 고등 수학과외
- 고등 영어과외
- 중등 수학과외
- 중등 영어과외

{{< cta-dual type="final" >}}
`;
};

// 파일 생성
const baseDir = '/mnt/c/Users/user/Desktop/과외를부탁해/edu-guide/content/provinces';
let createdFiles = [];

for (const [province, cities] of Object.entries(newCities)) {
  for (const [cityKey, city] of Object.entries(cities)) {
    const cityDir = path.join(baseDir, province, cityKey);
    
    // 폴더 생성
    if (!fs.existsSync(cityDir)) {
      fs.mkdirSync(cityDir, { recursive: true });
    }
    
    // 파일 생성
    const files = [
      { name: '_index.md', content: indexTemplate(city) },
      { name: 'high-math.md', content: highMathTemplate(city, city.schools) },
      { name: 'high-english.md', content: highEnglishTemplate(city, city.schools) },
      { name: 'middle-math.md', content: middleMathTemplate(city, city.middleSchools) },
      { name: 'middle-english.md', content: middleEnglishTemplate(city, city.middleSchools) }
    ];
    
    for (const file of files) {
      const filePath = path.join(cityDir, file.name);
      fs.writeFileSync(filePath, file.content);
      createdFiles.push(filePath);
    }
  }
}

console.log(`생성된 파일 수: ${createdFiles.length}`);
console.log('생성된 도시:');
for (const [province, cities] of Object.entries(newCities)) {
  for (const [cityKey, city] of Object.entries(cities)) {
    console.log(`  - ${province}/${cityKey} (${city.name})`);
  }
}
