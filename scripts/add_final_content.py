#!/usr/bin/env python3
import glob

extra_high = '''
## 상담 안내

상담은 무료로 진행됩니다. 학생의 현재 상황을 파악하고, 적합한 학습 방향을 제안해드립니다.

상담 시에는 최근 성적표나 모의고사 결과를 준비해주시면 더 구체적인 상담이 가능합니다.

전화 상담, 카카오톡 상담, 직접 만남 상담 모두 가능합니다. 편한 방법으로 연락 주세요.

'''

extra_mid = '''
## 상담 안내

상담은 무료로 진행됩니다. 학생의 현재 상황을 파악하고, 적합한 학습 방향을 제안해드립니다.

상담 시에는 최근 성적표를 준비해주시면 더 구체적인 상담이 가능합니다.

전화 상담, 카카오톡 상담, 직접 만남 상담 모두 가능합니다. 편한 방법으로 연락 주세요.

'''

for f in glob.glob('content/gyeonggi/*/*/*/high-math.md'):
    with open(f, 'r', encoding='utf-8') as file:
        c = file.read()
    c = c.replace('## 마무리', extra_high + '## 마무리')
    with open(f, 'w', encoding='utf-8') as file:
        file.write(c)

for f in glob.glob('content/gyeonggi/*/*/*/high-english.md'):
    with open(f, 'r', encoding='utf-8') as file:
        c = file.read()
    c = c.replace('## 마무리', extra_high + '## 마무리')
    with open(f, 'w', encoding='utf-8') as file:
        file.write(c)

for f in glob.glob('content/gyeonggi/*/*/*/middle-math.md'):
    with open(f, 'r', encoding='utf-8') as file:
        c = file.read()
    c = c.replace('## 마무리', extra_mid + '## 마무리')
    with open(f, 'w', encoding='utf-8') as file:
        file.write(c)

for f in glob.glob('content/gyeonggi/*/*/*/middle-english.md'):
    with open(f, 'r', encoding='utf-8') as file:
        c = file.read()
    c = c.replace('## 마무리', extra_mid + '## 마무리')
    with open(f, 'w', encoding='utf-8') as file:
        file.write(c)

print("완료!")
