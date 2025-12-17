const fs = require('fs');
const path = require('path');

// 서울 부족 구별 추가할 동 목록
const districtsToAdd = {
  geumcheon: {
    name: '금천구',
    dongs: ['독산1동', '독산2동', '독산3동', '독산4동', '시흥1동', '시흥2동', '시흥3동', '시흥4동', '시흥5동']
  },
  gwanak: {
    name: '관악구',
    dongs: ['보라매동', '청룡동', '성현동', '행운동', '낙성대동', '청림동', '서원동', '신원동', '서림동', '신사동', '난곡동', '난향동', '조원동', '대학동', '삼성동', '미성동', '중앙동', '인헌동', '은천동']
  },
  yangcheon: {
    name: '양천구',
    dongs: ['목1동', '목2동', '목3동', '목4동', '목5동', '신월1동', '신월2동', '신월3동', '신월4동', '신월5동', '신월6동', '신월7동', '신정1동', '신정2동', '신정3동', '신정4동', '신정6동', '신정7동']
  },
  dobong: {
    name: '도봉구',
    dongs: ['도봉1동', '도봉2동', '방학1동', '방학2동', '방학3동', '쌍문1동', '쌍문2동', '쌍문3동', '쌍문4동', '창1동', '창2동', '창3동', '창4동', '창5동']
  },
  nowon: {
    name: '노원구',
    dongs: ['공릉1동', '공릉2동', '상계1동', '상계2동', '상계3동', '상계4동', '상계5동', '상계6동', '상계7동', '상계8동', '상계9동', '상계10동', '월계1동', '월계2동', '월계3동', '중계1동', '중계2동', '중계3동', '중계4동', '중계본동', '하계1동', '하계2동']
  },
  jungnang: {
    name: '중랑구',
    dongs: ['면목본동', '면목2동', '면목3·8동', '면목4동', '면목5동', '면목7동', '상봉1동', '상봉2동', '중화1동', '중화2동', '묵1동', '묵2동', '망우본동', '망우3동', '신내1동', '신내2동']
  },
  dongjak: {
    name: '동작구',
    dongs: ['노량진1동', '노량진2동', '상도1동', '상도2동', '상도3동', '상도4동', '흑석동', '사당1동', '사당2동', '사당3동', '사당4동', '사당5동', '대방동', '신대방1동', '신대방2동']
  }
};

// 서두 풀 (10개)
const introPool = [
  (gu, dong) => `${gu} ${dong}에서 과외를 찾고 계시나요? 학생 맞춤 1:1 수업을 진행합니다.`,
  (gu, dong) => `${dong} 학생들의 실력 향상을 위한 맞춤 수업을 제공합니다.`,
  (gu, dong) => `${gu} ${dong} 지역 과외 전문입니다. 기초부터 심화까지 체계적으로 지도합니다.`,
  (gu, dong) => `${dong}에서 좋은 선생님 찾기 어려우셨죠? 검증된 선생님을 연결해드립니다.`,
  (gu, dong) => `${gu} ${dong} 학생들에게 최적화된 수업을 제공합니다.`,
  (gu, dong) => `성적 향상의 시작은 좋은 선생님입니다. ${dong}에서 만나보세요.`,
  (gu, dong) => `${dong} 과외 알아보시나요? 경험 많은 선생님이 함께합니다.`,
  (gu, dong) => `학원보다 효과적인 1:1 수업, ${gu} ${dong}에서 시작하세요.`,
  (gu, dong) => `${dong} 학생들의 목표 달성을 돕습니다. 맞춤 커리큘럼으로 진행합니다.`,
  (gu, dong) => `${gu} ${dong}에서 실력 있는 선생님을 만나보세요.`
];

// 마무리 풀 (10개)
const outroPool = [
  (gu, dong) => `${gu} ${dong} 학생 여러분, 지금 바로 시작하세요.`,
  (gu, dong) => `${dong}에서 좋은 결과를 함께 만들어가겠습니다.`,
  (gu, dong) => `${gu} ${dong} 학생들의 성공을 응원합니다.`,
  (gu, dong) => `${dong}에서 목표를 이루는 그날까지 함께하겠습니다.`,
  (gu, dong) => `지금 시작하면 ${dong} 학생도 달라질 수 있습니다.`,
  (gu, dong) => `${gu} ${dong}에서 꿈을 향한 첫걸음을 내딛으세요.`,
  (gu, dong) => `${dong} 학생들, 더 늦기 전에 시작하세요.`,
  (gu, dong) => `좋은 선생님과 함께라면 ${dong} 학생도 충분히 해낼 수 있습니다.`,
  (gu, dong) => `${gu} ${dong}에서 원하는 성적을 만들어가세요.`,
  (gu, dong) => `시작이 반입니다. ${dong}에서 오늘 시작하세요.`
];

// 이미지 풀 (30개)
const imagePool = [
  '/images/edu_0001_6f16r5jSVKs.jpg',
  '/images/edu_0002_F5ohqqoA9nA.jpg',
  '/images/edu_0003_M3qUP8csxfE.jpg',
  '/images/edu_0004_qJ37SUK_yI8.jpg',
  '/images/edu_0005_RKP8bG4HSeM.jpg',
  '/images/edu_0006_ZTSaijEjt8A.jpg',
  '/images/edu_0007_h_iOKOBp8ok.jpg',
  '/images/edu_0008_j2JKh3ycN2M.jpg',
  '/images/edu_0009_pnrHtY6XN-E.jpg',
  '/images/edu_0010_qc1qRAU7fYY.jpg',
  '/images/edu_0011_sf4HXkF6bDc.jpg',
  '/images/edu_0012_z8Pn1-RBhB0.jpg',
  '/images/edu_0013_C9IlYEZQp6o.jpg',
  '/images/edu_0014_FKN5YW0xJ9E.jpg',
  '/images/edu_0015_HpRAshSoBHU.jpg',
  '/images/edu_0016_I_LxDFIIRIA.jpg',
  '/images/edu_0017_LOHVrTsdvzs.jpg',
  '/images/edu_0018_N4gnTPt5D_U.jpg',
  '/images/edu_0019_Of_m3hMsoAA.jpg',
  '/images/edu_0020_P5UkJGXRNg8.jpg',
  '/images/edu_0021_Q0HmyPg3QGc.jpg',
  '/images/edu_0022_X6CTbNTOjss.jpg',
  '/images/edu_0023_I_LxDFIIRIA.jpg',
  '/images/edu_0024_LOHVrTsdvzs.jpg',
  '/images/edu_0025_N4gnTPt5D_U.jpg',
  '/images/edu_0026_Of_m3hMsoAA.jpg',
  '/images/edu_0027_P5UkJGXRNg8.jpg',
  '/images/edu_0028_Q0HmyPg3QGc.jpg',
  '/images/edu_0029_X6CTbNTOjss.jpg',
  '/images/edu_0030_6f16r5jSVKs.jpg'
];

let imageIndex = 0;
let introIndex = 0;
let outroIndex = 0;

function getNextImage() {
  const img = imagePool[imageIndex % imagePool.length];
  imageIndex++;
  return img;
}

function getIntro(gu, dong) {
  const fn = introPool[introIndex % introPool.length];
  introIndex++;
  return fn(gu, dong);
}

function getOutro(gu, dong) {
  const fn = outroPool[outroIndex % outroPool.length];
  outroIndex++;
  return fn(gu, dong);
}

// _index.md 생성
function generateIndexMd(gu, dong) {
  return `---
title: "${gu} ${dong} 과외 | 맞춤 수학·영어 1:1 수업"
date: 2025-12-17
description: "${gu} ${dong} 지역 중등·고등 수학·영어 과외. 학생 맞춤 1:1 과외 정보."
featured_image: "${getNextImage()}"
regions:
  - 서울
cities:
  - ${gu}
tags:
  - ${dong}과외
  - ${dong}수학과외
  - ${dong}영어과외
  - ${gu}과외
---

${dong}은 ${gu}의 주거 밀집 지역으로, 다양한 학교가 위치해 있습니다.

## 수업 안내

**수학**: 개념 이해부터 문제 풀이까지 체계적으로 진행합니다.

**영어**: 내신과 수능을 균형 있게 준비합니다.

상세 정보는 아래 링크를 확인하세요.

{{< cta-dual type="final" >}}
`;
}

// high-math.md 생성
function generateHighMathMd(gu, dong) {
  return `---
title: "${gu} ${dong} 고등 수학과외 | 맞춤 커리큘럼"
date: 2025-12-17
categories:
- 고등교육
- 수학
tags:
- 서울
- ${gu}
- ${dong}
- 고등수학과외
- 수학과외
- 내신대비
- 수능대비
description: "${gu} ${dong} 지역 고등 수학 과외 전문. 학생 맞춤 1:1 수업으로 내신과 수능을 동시에 준비합니다."
featured_image: "${getNextImage()}"
---

${getIntro(gu, dong)}

수학은 계단식 과목입니다. 앞 단계를 완벽히 이해해야 다음 단계로 넘어갈 수 있습니다. 기초에 빈틈이 있으면 점점 더 힘들어집니다.

혼자 공부하면 어디가 문제인지 모를 수 있습니다. 전문가의 도움을 받으면 효율적으로 문제를 해결할 수 있습니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
첫 수업에서 학생의 현재 실력을 파악합니다. 어디가 부족한지 정확히 진단하고 수업을 시작합니다.
</div>

## 고등 수학, 왜 어려워지나요?

고등학교 수학은 중학교와 차원이 다릅니다. 개념이 추상적으로 변하고, 문제 유형도 다양해집니다.

수학Ⅰ, 수학Ⅱ, 미적분, 기하, 확률과 통계 등 과목이 세분화됩니다. 각 과목의 특성을 이해하고 대비해야 합니다.

내신과 수능에서 요구하는 역량이 다릅니다. 내신은 교과서 위주로, 수능은 사고력과 응용력이 중요합니다.

킬러 문항은 여러 개념을 복합적으로 적용해야 풀립니다. 기본기가 약하면 손도 못 댑니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
학생의 목표(내신/수능)에 따라 맞춤 전략을 세웁니다. 효율적인 방향으로 안내합니다.
</div>

## 1:1 과외가 효과적인 이유

1:1 과외의 가장 큰 장점은 맞춤 수업입니다. 학생의 수준에 맞춰 진도를 조절합니다. 이해가 안 되면 더 설명하고, 이해했으면 다음으로 넘어갑니다.

질문을 바로 할 수 있습니다. 모르는 게 생기면 그 자리에서 해결합니다. 학원에서는 질문하기가 어렵습니다.

학생의 약점을 정확히 파악할 수 있습니다. 어떤 유형에서 자주 틀리는지, 어떤 개념이 부족한지 선생님이 알고 있습니다.

진도에 쫓기지 않습니다. 학원은 정해진 커리큘럼대로 나가야 하지만, 과외는 학생 페이스에 맞춥니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
매 수업 시작 전 지난 내용을 복습합니다. 잊어버리기 전에 다시 확인합니다.
</div>

## 효과적인 학습 방법

수학 공부의 핵심은 개념 이해입니다. 공식만 외워서는 응용 문제를 풀 수 없습니다. 왜 그런 공식이 나오는지 알아야 합니다.

문제 풀이는 양보다 질입니다. 많이 푸는 것보다 제대로 푸는 게 중요합니다. 틀린 문제는 반드시 다시 풀어봐야 합니다.

오답 정리는 필수입니다. 같은 실수를 반복하지 않도록 오답 노트를 만드세요. 시험 직전에 오답 노트만 봐도 효과적입니다.

기출문제는 최고의 교재입니다. 출제 경향을 파악하고, 비슷한 유형에 익숙해지세요.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
오답 노트를 함께 만들어갑니다. 자주 틀리는 유형을 집중적으로 연습합니다.
</div>

## 학년별 학습 전략

학년별로 전략이 다릅니다. 고1은 기초를 다지는 시기입니다. 이전 학년 내용에 빈틈이 있다면 먼저 메워야 합니다.

고2는 심화 학습을 시작합니다. 핵심 개념들을 충실히 학습하세요. 내신과 모의고사 대비를 병행합니다.

고3은 정리와 실전 연습의 시기입니다. 기출문제를 많이 풀어보세요. 시간 관리 연습도 중요합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
학생의 학년과 목표에 맞춰 커리큘럼을 설계합니다. 낭비 없이 효율적으로 공부합니다.
</div>

## 흔히 하는 실수들

가장 흔한 건 계산 실수입니다. 급하게 풀다 보면 부호를 틀리거나 숫자를 잘못 쓰는 경우가 많습니다. 검산 습관을 들이세요.

개념을 대충 알고 넘어가는 것도 문제입니다. 이해한 것 같아도 막상 문제에 적용하면 막힙니다. 직접 풀어봐야 진짜 아는 겁니다.

문제를 끝까지 읽지 않는 실수도 있습니다. 조건을 놓치거나 묻는 것과 다른 답을 쓰는 경우가 많습니다.

어려운 문제에 너무 오래 붙잡혀 있는 것도 문제입니다. 시험에서는 시간 배분이 중요합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
학생이 자주 하는 실수 패턴을 파악하고 고쳐나갑니다.
</div>

## 시험 대비 전략

시험 2주 전부터 본격적으로 준비하세요. 교과서와 수업 노트를 다시 읽고, 핵심 개념을 정리하세요.

기출문제를 풀어보세요. 학교 시험은 출제 경향이 있습니다. 선생님별 스타일을 파악하는 것도 중요합니다.

시험 전날에는 새로운 문제를 풀지 마세요. 오답 노트와 핵심 정리 노트를 복습하는 게 효과적입니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
시험 범위에 맞춰 집중적으로 대비합니다. 예상 문제를 함께 풀어봅니다.
</div>

## 수업료 안내

${gu} ${dong} 지역 고등 수학 과외 수업료입니다.

**고1-2**는 주1회 25만원 - 36만원, 주2회 33만원 - 53만원 선입니다.

**고3**은 주1회 28만원 - 40만원, 주2회 37만원 - 59만원이 일반적입니다.

정확한 비용은 학생의 현재 수준과 목표에 따라 달라질 수 있습니다.

{{< cta-dual type="final" >}}

## 자주 묻는 질문

**Q. 주 몇 회 수업이 좋나요?**

학생 상황에 따라 다릅니다. 기초가 부족하면 주 2-3회, 유지 목적이면 주 1회가 적당합니다.

**Q. 내신과 수능 중 뭘 먼저 해야 하나요?**

학년에 따라 다릅니다. 고1-2는 내신 중심으로, 고3은 수능 비중을 높여갑니다.

**Q. 수학 기초가 많이 약해도 괜찮을까요?**

물론입니다. 부족한 부분을 파악해서 그 부분부터 채워나갑니다.

**Q. 선행 학습이 필요한가요?**

기초가 탄탄하면 선행도 가능합니다. 하지만 현재 진도가 우선입니다. 기초 없는 선행은 의미가 없습니다.

**Q. 학원과 과외 중 어떤 게 효과적인가요?**

학생 성향에 따라 다릅니다. 스스로 질문하기 어려운 학생, 진도가 맞지 않는 학생에게는 1:1 과외가 더 효과적입니다.

## 마무리

${getOutro(gu, dong)}
`;
}

// high-english.md 생성
function generateHighEnglishMd(gu, dong) {
  return `---
title: "${gu} ${dong} 고등 영어과외 | 내신·수능 대비"
date: 2025-12-17
categories:
- 고등교육
- 영어
tags:
- 서울
- ${gu}
- ${dong}
- 고등영어과외
- 영어과외
- 내신대비
- 수능대비
description: "${gu} ${dong} 지역 고등 영어 과외 전문. 학생 맞춤 1:1 수업으로 내신과 수능을 동시에 준비합니다."
featured_image: "${getNextImage()}"
---

${getIntro(gu, dong)}

영어는 꾸준함이 중요한 과목입니다. 매일 조금씩 하는 것이 효과적입니다. 한꺼번에 몰아서 하면 금방 잊어버립니다.

고등학교 영어는 중학교와 다릅니다. 어휘 수준이 높아지고, 문장 구조가 복잡해집니다. 체계적인 학습이 필요합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
학생의 영어 실력을 정확히 진단합니다. 독해, 어휘, 문법 중 어디가 부족한지 파악하고 시작합니다.
</div>

## 고등 영어, 왜 어려워지나요?

고등학교 영어는 중학교 영어보다 어휘 수준이 확 올라갑니다. 문장 구조도 복잡해지고 지문도 길어집니다.

내신과 수능 영어는 방향이 다릅니다. 내신은 교과서 본문 위주, 수능은 EBS 연계와 비연계 문제를 다룹니다.

수능 영어는 시간 싸움입니다. 70분 안에 45문제를 풀어야 합니다. 빈칸 추론, 순서 배열 같은 고난도 문제도 있습니다.

듣기도 무시할 수 없습니다. 수능 듣기 17문제는 확실히 잡아야 1등급이 가능합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
학생의 목표에 따라 내신형 또는 수능형으로 방향을 잡습니다. 두 가지를 병행하기도 합니다.
</div>

## 1:1 과외가 효과적인 이유

1:1 과외의 장점은 맞춤 수업입니다. 학생이 어려워하는 부분을 집중적으로 다룹니다. 학원에서는 이게 어렵습니다.

질문을 바로 할 수 있습니다. 모르는 단어나 문법이 있으면 그 자리에서 물어볼 수 있습니다.

학생의 약점을 선생님이 알고 있습니다. 어떤 유형에서 틀리는지, 무슨 문법이 약한지 파악하고 있습니다.

진도에 쫓기지 않습니다. 이해가 될 때까지 반복하고, 확실히 알면 다음으로 넘어갑니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
학생의 학교 교과서에 맞춰 수업합니다. 시험에 나올 내용을 집중적으로 다룹니다.
</div>

## 효과적인 학습 방법

영어 공부의 기본은 어휘입니다. 단어를 모르면 독해가 안 됩니다. 매일 정해진 양을 꾸준히 외우세요.

문법은 이해가 중요합니다. 무작정 외우면 응용이 안 됩니다. 왜 그렇게 되는지 알아야 합니다.

독해 연습도 매일 하세요. 다양한 지문을 읽으면서 실력을 키워야 합니다. 해석이 아니라 이해하는 연습이 필요합니다.

듣기는 매일 꾸준히 해야 합니다. EBS 듣기 교재를 활용하세요.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
수업 시간에 단어 테스트를 합니다. 외웠는지 확인하고 넘어갑니다.
</div>

## 학년별 학습 전략

고1은 기초를 다지는 시기입니다. 기본 문법을 확실히 잡고, 어휘력을 늘려가세요.

고2는 심화 학습을 시작합니다. 복잡한 문장 구조를 익히고, 독해 실력을 높여가세요.

고3은 실전 연습의 시기입니다. 기출문제를 많이 풀고, 시간 관리 연습을 하세요.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
학년에 맞는 커리큘럼으로 진행합니다. 내신과 수능을 균형 있게 준비합니다.
</div>

## 흔히 하는 실수들

단어를 문맥 없이 외우는 게 흔한 실수입니다. 문장 속에서 어떻게 쓰이는지 함께 익혀야 합니다.

문법만 공부하고 독해를 소홀히 하는 것도 문제입니다. 문법은 독해를 위한 도구입니다.

시험에서 시간 배분을 못하는 경우도 많습니다. 평소에 시간을 재고 푸는 연습을 하세요.

영어 공부를 몰아서 하는 것도 안 좋습니다. 영어는 매일 조금씩 꾸준히 해야 효과가 있습니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
실제 시험처럼 시간을 재고 연습합니다. 시간 안에 정확하게 푸는 연습을 합니다.
</div>

## 시험 대비 전략

시험 2주 전부터 본격적으로 준비하세요. 교과서 본문을 완벽히 이해하고, 주요 표현을 정리하세요.

문법 문제는 교과서에서 출제됩니다. 본문에 나온 문법 포인트를 확인하세요.

서술형 대비도 해야 합니다. 작문 연습을 미리 해두세요. 시험 전날에는 본문을 다시 읽어보세요.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
시험 범위에 맞춰 집중 대비합니다. 예상 문제를 함께 풀어봅니다.
</div>

## 수업료 안내

${gu} ${dong} 지역 고등 영어 과외 수업료입니다.

**고1-2**는 주1회 25만원 - 36만원, 주2회 33만원 - 53만원 선입니다.

**고3**은 주1회 28만원 - 40만원, 주2회 37만원 - 59만원이 일반적입니다.

정확한 비용은 학생의 현재 수준과 목표에 따라 달라질 수 있습니다.

{{< cta-dual type="final" >}}

## 자주 묻는 질문

**Q. 영어 단어는 어떻게 외워야 하나요?**

문장과 함께 외우세요. 단어만 외우면 쓰임새를 모릅니다.

**Q. 수능 영어 1등급 받을 수 있나요?**

꾸준히 노력하면 가능합니다. 체계적인 계획이 필요합니다.

**Q. 영어 기초가 많이 약해도 괜찮을까요?**

물론입니다. 부족한 부분을 파악해서 그 부분부터 채워나갑니다.

**Q. 선행 학습이 필요한가요?**

기초가 탄탄하면 선행도 가능합니다. 하지만 현재 진도가 우선입니다.

**Q. 학원과 과외 중 어떤 게 효과적인가요?**

학생 성향에 따라 다릅니다. 스스로 질문하기 어려운 학생, 진도가 맞지 않는 학생에게는 1:1 과외가 더 효과적입니다.

## 마무리

${getOutro(gu, dong)}
`;
}

// middle-math.md 생성
function generateMiddleMathMd(gu, dong) {
  return `---
title: "${gu} ${dong} 중등 수학과외 | 기초부터 탄탄하게"
date: 2025-12-17
categories:
- 중등교육
- 수학
tags:
- 서울
- ${gu}
- ${dong}
- 중등수학과외
- 수학과외
- 내신대비
description: "${gu} ${dong} 지역 중등 수학 과외 전문. 학생 맞춤 1:1 수업으로 기초를 탄탄하게 다집니다."
featured_image: "${getNextImage()}"
---

${getIntro(gu, dong)}

중학교 수학은 고등학교 수학의 기초입니다. 여기서 빈틈이 생기면 나중에 힘들어집니다. 지금 확실히 잡아두세요.

수학은 계단식 과목입니다. 앞 단계를 이해해야 다음 단계로 넘어갈 수 있습니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
첫 수업에서 학생의 실력을 파악합니다. 어디가 부족한지 정확히 진단하고 시작합니다.
</div>

## 중학 수학, 왜 갑자기 어려워지나요?

초등학교 때는 산수였습니다. 숫자와 계산이 전부였죠. 하지만 중학교 수학은 다릅니다.

문자가 등장합니다. x, y 같은 변수 개념이 처음 나옵니다. 눈에 보이지 않는 것을 다루기 시작합니다.

음수가 나옵니다. "마이너스 곱하기 마이너스는 플러스"가 직관적으로 이해되지 않습니다. 추상적 사고가 필요해집니다.

방정식, 함수, 도형의 증명까지. 중학교 3년 동안 수학은 완전히 다른 과목이 됩니다.

여기서 포기하는 학생이 많습니다. 하지만 기초만 잡으면 고등학교까지 쉬워집니다. 중학교가 기회입니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
추상적인 개념을 구체적인 예시로 설명합니다. 이해될 때까지 다양한 방법으로 접근합니다.
</div>

## 1:1 과외가 효과적인 이유

1:1 과외는 학생 맞춤입니다. 이해가 안 되면 더 설명하고, 알면 다음으로 넘어갑니다.

질문을 바로 할 수 있습니다. 학원에서는 질문하기 어렵지만, 과외에서는 바로 물어볼 수 있습니다.

학생의 약점을 선생님이 알고 있습니다. 어디서 자주 틀리는지 파악하고 있습니다.

진도에 쫓기지 않습니다. 학원은 정해진 속도로 나가지만, 과외는 학생 페이스에 맞춥니다. 이해될 때까지 충분히 시간을 씁니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
매 수업 시작 전 지난 내용을 복습합니다. 잊기 전에 다시 확인합니다.
</div>

## 효과적인 학습 방법

수학 공부의 핵심은 개념 이해입니다. 공식만 외워서는 응용 문제를 풀 수 없습니다.

문제 풀이는 양보다 질입니다. 많이 푸는 것보다 제대로 푸는 게 중요합니다.

오답 정리는 필수입니다. 틀린 문제는 반드시 다시 풀어봐야 합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
오답 노트를 함께 만들어갑니다. 같은 실수를 반복하지 않도록 합니다.
</div>

## 학년별 학습 전략

중1은 수학적 사고의 기초를 다지는 시기입니다. 정수, 방정식 개념을 확실히 잡으세요.

중2는 난이도가 올라갑니다. 함수, 도형 개념을 충실히 익히세요.

중3은 고등학교 준비 시기입니다. 이차방정식, 이차함수를 완벽히 이해해야 합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
학년에 맞는 커리큘럼으로 진행합니다. 다음 학년을 대비합니다.
</div>

## 흔히 하는 실수들

계산 실수가 가장 많습니다. 서두르다 보면 부호를 틀리거나 숫자를 잘못 씁니다. 검산 습관을 들이세요.

개념을 대충 알고 넘어가는 것도 문제입니다. 이해한 것 같아도 막상 문제에 적용하면 막힙니다.

문제를 끝까지 읽지 않는 실수도 많습니다. 조건을 놓치면 틀립니다.

어려운 문제에 너무 오래 붙잡혀 있는 것도 안 좋습니다. 시험에서는 시간 배분이 중요합니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
학생이 자주 하는 실수 패턴을 파악하고 고쳐나갑니다.
</div>

## 시험 대비 전략

시험 2주 전부터 본격적으로 준비하세요. 교과서와 노트를 다시 보고, 핵심 개념을 정리하세요.

기출문제를 풀어보세요. 학교 선생님의 출제 스타일을 파악하세요.

모르는 문제는 표시해두고, 시험 전날 다시 확인하세요. 마지막까지 포기하지 마세요.

시험 당일에는 쉬운 문제부터 풀어 시간을 확보하세요. 어려운 문제에 발목 잡히지 마세요.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
시험 범위에 맞춰 집중 대비합니다. 예상 문제를 함께 풀어봅니다.
</div>

## 수업료 안내

${gu} ${dong} 지역 중등 수학 과외 수업료입니다.

**중학생**은 주1회 22만원 - 32만원, 주2회 29만원 - 47만원 선입니다.

정확한 비용은 학생의 현재 수준과 목표에 따라 달라질 수 있습니다.

{{< cta-dual type="final" >}}

## 자주 묻는 질문

**Q. 주 몇 회 수업이 좋나요?**

학생 상황에 따라 다릅니다. 기초가 부족하면 주 2-3회, 유지 목적이면 주 1회가 적당합니다.

**Q. 수학 기초가 많이 약해도 괜찮을까요?**

물론입니다. 부족한 부분을 파악해서 그 부분부터 채워나갑니다.

**Q. 선행 학습이 필요한가요?**

기초가 탄탄하면 선행도 가능합니다. 하지만 현재 진도가 우선입니다.

**Q. 학원과 과외 중 어떤 게 나을까요?**

학생 성향에 따라 다릅니다. 혼자 질문하기 어려워하거나, 진도가 맞지 않는 학생은 과외가 효과적입니다. 1:1로 맞춤 수업이 가능합니다.

**Q. 문제집은 어떤 걸 쓰나요?**

학생 수준과 학교에 맞춰 선정합니다. 교과서, 개념서, 문제집을 단계별로 활용합니다.

## 마무리

${getOutro(gu, dong)}
`;
}

// middle-english.md 생성
function generateMiddleEnglishMd(gu, dong) {
  return `---
title: "${gu} ${dong} 중등 영어과외 | 기초부터 확실하게"
date: 2025-12-17
categories:
- 중등교육
- 영어
tags:
- 서울
- ${gu}
- ${dong}
- 중등영어과외
- 영어과외
- 내신대비
description: "${gu} ${dong} 지역 중등 영어 과외 전문. 학생 맞춤 1:1 수업으로 기초를 확실하게 다집니다."
featured_image: "${getNextImage()}"
---

${getIntro(gu, dong)}

중학교 영어는 고등학교 영어의 기초입니다. 여기서 기본기를 잡아야 나중에 편합니다.

영어는 꾸준함이 중요한 과목입니다. 매일 조금씩 하는 것이 효과적입니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
첫 수업에서 학생의 영어 실력을 파악합니다. 독해, 어휘, 문법 중 어디가 부족한지 진단합니다.
</div>

## 중학 영어, 왜 갑자기 어려워지나요?

초등학교 영어는 쉬웠습니다. 간단한 회화와 기초 단어가 전부였죠. 하지만 중학교 영어는 다릅니다.

문법이 본격적으로 시작됩니다. 시제, 문장 구조, 접속사 등 규칙이 복잡해집니다. 암기만으로는 한계가 있습니다.

독해 지문이 길어집니다. 초등학교 때 3-4줄이었다면, 중학교에서는 한 페이지 이상 읽어야 합니다.

서술형 문제가 많아집니다. 단순 객관식이 아니라 직접 영작을 해야 합니다. 문법 실력이 드러납니다.

영어는 포기하면 따라잡기 어렵습니다. 중학교 때 기초를 놓치면 고등학교에서 더 힘들어집니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
문법을 이해 중심으로 설명합니다. 외우는 영어가 아니라 이해하는 영어를 가르칩니다.
</div>

## 1:1 과외가 효과적인 이유

1:1 과외는 학생 맞춤입니다. 어려워하는 부분을 집중적으로 다룹니다.

질문을 바로 할 수 있습니다. 모르는 단어나 문법이 있으면 바로 물어볼 수 있습니다.

학생의 약점을 선생님이 알고 있습니다. 어떤 문법이 약한지, 어떤 유형에서 틀리는지 파악하고 있습니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
학생의 학교 교과서에 맞춰 수업합니다. 시험에 나올 내용을 다룹니다.
</div>

## 효과적인 학습 방법

영어 공부의 기본은 어휘입니다. 단어를 모르면 독해가 안 됩니다. 매일 꾸준히 외우세요.

문법은 이해가 중요합니다. 무작정 외우면 응용이 안 됩니다.

독해 연습도 매일 하세요. 다양한 글을 읽으면서 실력을 키우세요.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
수업 시간에 단어 테스트를 합니다. 외웠는지 확인하고 넘어갑니다.
</div>

## 학년별 학습 전략

중1은 영어의 기초를 다지는 시기입니다. 기본 문법과 어휘를 확실히 잡으세요.

중2는 난이도가 올라갑니다. 복잡한 문장 구조를 익히세요.

중3은 고등학교 준비 시기입니다. 독해 실력을 키우고, 문법을 완벽히 정리하세요.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
학년에 맞는 커리큘럼으로 진행합니다. 다음 학년을 대비합니다.
</div>

## 흔히 하는 실수들

단어를 문맥 없이 외우는 게 흔한 실수입니다. 문장과 함께 외워야 쓰임새를 압니다.

문법만 공부하고 독해를 소홀히 하는 것도 문제입니다. 문법은 독해를 위한 도구입니다.

시험에서 시간 배분을 못하는 경우도 많습니다. 평소에 시간을 재고 푸는 연습을 하세요.

영어 공부를 몰아서 하는 것도 안 좋습니다. 매일 조금씩 꾸준히 하는 게 효과적입니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
학생이 자주 하는 실수 패턴을 파악하고 고쳐나갑니다.
</div>

## 시험 대비 전략

시험 2주 전부터 본격적으로 준비하세요. 교과서 본문을 완벽히 이해하세요.

문법 문제는 교과서에서 출제됩니다. 본문에 나온 문법 포인트를 확인하세요.

서술형 대비도 해야 합니다. 작문 연습을 미리 해두세요.

단어 암기는 시험 전날까지 반복하세요. 아는 단어도 다시 확인하세요.

듣기 평가가 있다면 미리 연습하세요. 평소에 영어 듣기에 익숙해지면 시험이 쉬워집니다.

<div style="background-color: #FDF8F0; border-left: 3px solid #d4a574; padding: 18px; margin: 15px 0; font-size: 0.95em;">
<strong>이렇게 수업합니다!</strong><br>
시험 범위에 맞춰 집중 대비합니다. 예상 문제를 함께 풀어봅니다.
</div>

## 수업료 안내

${gu} ${dong} 지역 중등 영어 과외 수업료입니다.

**중학생**은 주1회 22만원 - 32만원, 주2회 29만원 - 47만원 선입니다.

정확한 비용은 학생의 현재 수준과 목표에 따라 달라질 수 있습니다.

{{< cta-dual type="final" >}}

## 자주 묻는 질문

**Q. 영어 단어는 어떻게 외워야 하나요?**

문장과 함께 외우세요. 단어만 외우면 쓰임새를 모릅니다.

**Q. 영어 기초가 많이 약해도 괜찮을까요?**

물론입니다. 부족한 부분을 파악해서 그 부분부터 채워나갑니다.

**Q. 선행 학습이 필요한가요?**

기초가 탄탄하면 선행도 가능합니다. 하지만 현재 진도가 우선입니다.

**Q. 학원과 과외 중 어떤 게 나을까요?**

학생 성향에 따라 다릅니다. 혼자 질문하기 어려워하거나, 진도가 맞지 않는 학생은 과외가 효과적입니다. 1:1로 맞춤 수업이 가능합니다.

**Q. 문법 교재는 따로 쓰나요?**

학생 수준에 맞는 문법서를 선정합니다. 교과서와 병행하여 체계적으로 정리합니다.

## 마무리

${getOutro(gu, dong)}
`;
}

// 메인 실행
let totalFiles = 0;

Object.entries(districtsToAdd).forEach(([districtCode, districtInfo]) => {
  const { name: guName, dongs } = districtInfo;

  dongs.forEach(dong => {
    const dongPath = path.join('content/seoul', districtCode, dong);

    // 이미 존재하는지 확인
    if (fs.existsSync(dongPath)) {
      console.log(`[SKIP] ${guName} ${dong} - 이미 존재`);
      return;
    }

    // 폴더 생성
    fs.mkdirSync(dongPath, { recursive: true });

    // 파일 생성
    fs.writeFileSync(path.join(dongPath, '_index.md'), generateIndexMd(guName, dong));
    fs.writeFileSync(path.join(dongPath, 'high-math.md'), generateHighMathMd(guName, dong));
    fs.writeFileSync(path.join(dongPath, 'high-english.md'), generateHighEnglishMd(guName, dong));
    fs.writeFileSync(path.join(dongPath, 'middle-math.md'), generateMiddleMathMd(guName, dong));
    fs.writeFileSync(path.join(dongPath, 'middle-english.md'), generateMiddleEnglishMd(guName, dong));

    totalFiles += 5;
    console.log(`[OK] ${guName} ${dong} - 5개 파일 생성`);
  });
});

console.log(`\n총 ${totalFiles}개 파일 생성 완료`);
