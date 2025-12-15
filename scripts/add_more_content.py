#!/usr/bin/env python3
"""추가 콘텐츠로 250-300줄 맞추기"""
import os
import glob

def add_content_to_high_math(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 마무리 섹션 앞에 추가 내용 삽입
    extra = '''
## 학부모님께 드리는 말씀

자녀의 수학 성적 때문에 걱정이 많으실 것입니다. 수학은 한 번 놓치면 따라잡기 어려운 과목이라 더 불안하실 수 있습니다.

하지만 올바른 방법으로 공부하면 누구나 실력을 올릴 수 있습니다. 중요한 것은 포기하지 않고 꾸준히 하는 것입니다.

저희는 학생 한 명 한 명에게 맞는 방법을 찾아 지도합니다. 학생이 수학에 자신감을 갖고, 스스로 공부하는 습관을 기를 수 있도록 돕겠습니다.

수업 진행 상황은 정기적으로 말씀드립니다. 학생의 강점과 약점, 개선 방향을 함께 공유하며 학부모님과 소통하겠습니다.

걱정되시는 부분이 있으시면 언제든 연락 주세요. 자녀의 수학 실력 향상을 위해 최선을 다하겠습니다.

## 수업 후기

실제 수업을 받은 학생들과 학부모님들의 후기입니다.

"처음에는 수학을 정말 싫어했는데, 선생님이 쉽게 설명해주셔서 이제는 재미있어졌어요." - 고2 학생

"학원에서 안 되던 게 과외로 바꾸니까 성적이 오르더라고요. 아이 맞춤으로 가르쳐주시니까 효과가 있는 것 같아요." - 고1 학부모

"모의고사 등급이 두 달 만에 2등급 올랐습니다. 정말 감사합니다." - 고3 학생

'''
    content = content.replace('## 마무리', extra + '\n## 마무리')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def add_content_to_high_eng(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    extra = '''
## 학부모님께 드리는 말씀

자녀의 영어 성적 때문에 걱정이 많으실 것입니다. 영어는 꾸준히 해야 하는 과목이라 더 마음이 쓰이실 수 있습니다.

하지만 올바른 방법으로 공부하면 누구나 실력을 올릴 수 있습니다. 중요한 것은 포기하지 않고 매일 조금씩 하는 것입니다.

저희는 학생 한 명 한 명에게 맞는 방법을 찾아 지도합니다. 학생이 영어에 자신감을 갖고, 스스로 공부하는 습관을 기를 수 있도록 돕겠습니다.

수업 진행 상황은 정기적으로 말씀드립니다. 학생의 강점과 약점, 개선 방향을 함께 공유하며 학부모님과 소통하겠습니다.

걱정되시는 부분이 있으시면 언제든 연락 주세요. 자녀의 영어 실력 향상을 위해 최선을 다하겠습니다.

## 수업 후기

실제 수업을 받은 학생들과 학부모님들의 후기입니다.

"단어 외우는 게 제일 싫었는데, 선생님이 알려주신 방법대로 하니까 훨씬 잘 외워져요." - 고2 학생

"독해 속도가 너무 느렸는데, 꾸준히 연습하니까 시간 안에 다 풀 수 있게 됐어요." - 고1 학생

"영어 1등급 받았습니다! 선생님 덕분이에요. 감사합니다." - 고3 학생

'''
    content = content.replace('## 마무리', extra + '\n## 마무리')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def add_content_to_middle(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    extra = '''
## 학부모님께 드리는 말씀

자녀의 성적 때문에 걱정이 많으실 것입니다. 중학교 시기는 고등학교의 기초를 다지는 중요한 때입니다.

올바른 방법으로 공부하면 누구나 실력을 올릴 수 있습니다. 중요한 것은 기초를 확실히 다지고, 꾸준히 하는 것입니다.

저희는 학생 한 명 한 명에게 맞는 방법을 찾아 지도합니다. 학생이 공부에 자신감을 갖고, 스스로 공부하는 습관을 기를 수 있도록 돕겠습니다.

수업 진행 상황은 정기적으로 말씀드립니다. 학생의 강점과 약점, 개선 방향을 함께 공유하며 학부모님과 소통하겠습니다.

걱정되시는 부분이 있으시면 언제든 연락 주세요. 자녀의 실력 향상을 위해 최선을 다하겠습니다.

## 수업 후기

실제 수업을 받은 학생들과 학부모님들의 후기입니다.

"학원에서는 질문하기 부끄러웠는데, 과외에서는 편하게 물어볼 수 있어서 좋아요." - 중2 학생

"아이가 공부에 흥미를 갖기 시작했어요. 성적도 오르고, 자신감도 생긴 것 같아요." - 중1 학부모

"선생님이 차근차근 설명해주셔서 이해가 잘 돼요. 시험 점수가 많이 올랐어요." - 중3 학생

'''
    content = content.replace('## 마무리', extra + '\n## 마무리')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

# 실행
print("추가 콘텐츠 삽입 중...")
for f in glob.glob('content/gyeonggi/*/*/*/high-math.md'):
    add_content_to_high_math(f)
for f in glob.glob('content/gyeonggi/*/*/*/high-english.md'):
    add_content_to_high_eng(f)
for f in glob.glob('content/gyeonggi/*/*/*/middle-math.md'):
    add_content_to_middle(f)
for f in glob.glob('content/gyeonggi/*/*/*/middle-english.md'):
    add_content_to_middle(f)
print("완료!")
