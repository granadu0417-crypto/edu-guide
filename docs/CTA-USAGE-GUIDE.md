# CTA Shortcode 사용 가이드

## 개요

콘텐츠에서 자연스럽게 카카오톡 상담으로 유도하는 2가지 CTA 컴포넌트입니다.

---

## 1. 중간용 CTA (Subtle 스타일)

### 사용 위치
- 콘텐츠 중간 (약 40% 지점)
- H2 섹션 사이
- 자연스러운 흐름 속에서

### 사용법
```markdown
{{< cta-consultation >}}
```

### 커스텀 메시지
```markdown
{{< cta-consultation message="궁금한 점이 있으시면 언제든지 문의해주세요" >}}
```

### 예시
```markdown
## 2. 독서 습관을 만드는 구체적인 방법

매일 정해진 시간에 책을 읽는 것이 중요합니다...

{{< cta-consultation message="우리 아이에게 맞는 독서 계획이 궁금하시다면?" >}}

## 3. 학년별 추천 도서
```

---

## 2. 끝용 CTA (Prominent 스타일)

### 사용 위치
- 콘텐츠 마지막 (결론 직후)
- 핵심 내용 전달 후

### 사용법
```markdown
{{< cta-consultation-final >}}
```

### 커스텀 메시지
```markdown
{{< cta-consultation-final
    title="독서 습관 상담받으세요"
    message="우리 아이에게 딱 맞는 독서 계획을 함께 만들어드립니다"
>}}
```

### 예시
```markdown
## 결론

독서 습관은 평생 가는 자산입니다. 오늘부터 시작해보세요.

{{< cta-consultation-final
    title="학습 상담이 필요하신가요?"
    message="언제든지 카카오톡으로 문의해주세요"
>}}
```

---

## 권장 사용 패턴

### 표준 패턴 (3000자+ 글)
```markdown
[서론 - 500자]

## H2 섹션 1
[내용 - 800자]

## H2 섹션 2
[내용 - 800자]

{{< cta-consultation >}}  ← 중간 CTA (40% 지점)

## H2 섹션 3
[내용 - 600자]

## 결론
[내용 - 300자]

{{< cta-consultation-final >}}  ← 끝 CTA
```

### 짧은 글 패턴 (1500자 이하)
```markdown
[서론]

## H2 섹션 1
[내용]

## H2 섹션 2
[내용]

## 결론
[내용]

{{< cta-consultation-final >}}  ← 끝 CTA만 사용
```

---

## GA4 이벤트 추적

### 자동 추적 항목
- 이벤트 카테고리: `Conversion`
- 이벤트 라벨:
  - 중간 CTA: `Content CTA Subtle - [페이지 제목]`
  - 끝 CTA: `Content CTA Final - [페이지 제목]`
- Value:
  - 중간 CTA: 1
  - 끝 CTA: 2 (높은 가중치)

### GA4에서 확인하는 방법
1. GA4 대시보드 → 이벤트
2. `click` 이벤트 선택
3. 매개변수 필터: `event_label` contains `CTA`

---

## 스타일 특징

### 중간용 CTA (Subtle)
- 부드러운 그레이 배경
- 작은 카카오톡 아이콘
- 보라색 버튼
- 모바일: 수직 레이아웃

### 끝용 CTA (Prominent)
- 그라데이션 배경 (보라색)
- 큰 애니메이션 아이콘
- 노란색 버튼 (강조)
- 백그라운드 회전 효과
- 모바일: 전체 너비 버튼

---

## 접근성

- 키보드 내비게이션 지원
- 포커스 스타일 명확함
- ARIA 라벨 자동 추가
- 스크린 리더 호환

---

## 주의사항

1. **과도한 사용 금지**: 하나의 글에 CTA는 최대 2개
2. **자연스러운 배치**: 문맥과 어울리는 위치에 배치
3. **메시지 커스터마이징**: 콘텐츠 주제에 맞게 메시지 변경
4. **모바일 테스트**: 항상 모바일에서 확인

---

## 문제 해결

### CTA가 표시되지 않는 경우
1. Hugo 빌드 재실행: `hugo --gc --minify`
2. 브라우저 캐시 삭제
3. shortcode 파일 경로 확인:
   - `layouts/shortcodes/cta-consultation.html`
   - `layouts/shortcodes/cta-consultation-final.html`

### 스타일이 깨지는 경우
1. 기존 CSS와 충돌 가능성 확인
2. 브라우저 개발자 도구에서 CSS 검사
3. z-index 문제 확인

---

## 업데이트 내역

- 2025-01-XX: 초기 버전 생성
  - 중간용 CTA (Subtle)
  - 끝용 CTA (Prominent)
  - GA4 이벤트 추적
  - 모바일 최적화
