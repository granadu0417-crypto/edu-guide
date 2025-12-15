#!/usr/bin/env python3
"""가이드 콘텐츠 리라이팅 - tutoring, subjects, local, high, middle, exam, consultation 등"""

import os
import re

# 아이보리 박스 표현 풀 - 가이드 콘텐츠용 (40개)
GUIDE_BOX_POOL = [
    "학생의 현재 상황과 목표를 정확히 파악합니다. 맞춤 계획을 세우는 것이 첫걸음입니다.",
    "무작정 진도를 나가지 않습니다. 기초부터 차근차근 쌓아갑니다.",
    "이해가 될 때까지 설명합니다. 외우기보다 이해가 먼저입니다.",
    "문제 풀이 과정을 함께 점검합니다. 어디서 막히는지 정확히 파악합니다.",
    "틀린 문제를 분석합니다. 같은 실수를 반복하지 않도록 합니다.",
    "개념을 확실히 잡은 후 문제로 넘어갑니다. 기본이 중요합니다.",
    "학생 수준에 맞는 난이도로 시작합니다. 너무 어려우면 포기하게 됩니다.",
    "꾸준히 복습하도록 안내합니다. 한 번 배운 것을 잊지 않게 합니다.",
    "상담을 통해 학생에게 맞는 방법을 찾습니다. 모든 학생이 같은 방법으로 배우지 않습니다.",
    "수업 후 피드백을 드립니다. 오늘 무엇을 배웠고, 무엇을 더 해야 하는지 알려드립니다.",
    "학부모님과 정기적으로 소통합니다. 진행 상황을 공유합니다.",
    "목표를 명확히 설정합니다. 목표가 있어야 동기가 생깁니다.",
    "단계별로 진행합니다. 갑자기 어려운 내용으로 넘어가지 않습니다.",
    "약점을 정확히 파악합니다. 약점을 보완해야 성적이 오릅니다.",
    "실수 패턴을 분석합니다. 반복되는 실수를 줄이면 점수가 오릅니다.",
    "시간 관리도 훈련합니다. 실전에서는 시간이 부족합니다.",
    "다양한 유형의 문제를 경험하게 합니다. 새로운 문제도 풀 수 있게 됩니다.",
    "개념과 문제 풀이를 병행합니다. 이론만 알아서는 부족합니다.",
    "학교 수업과 연계하여 진행합니다. 학교 진도에 맞춰 준비합니다.",
    "내신과 수능을 효율적으로 병행합니다. 두 마리 토끼를 잡는 전략이 있습니다.",
    "질문을 많이 하도록 유도합니다. 질문해야 배웁니다.",
    "오답 노트를 함께 만듭니다. 시험 전에 다시 보면 도움이 됩니다.",
    "풀이 과정을 깔끔하게 쓰는 연습을 합니다. 서술형에서 점수를 잃지 않습니다.",
    "기출문제를 분석합니다. 출제 경향을 파악하면 대비가 쉬워집니다.",
    "시험 전에는 집중 대비합니다. 시험 범위를 철저히 준비합니다.",
    "방학은 부족한 부분을 채우는 시간입니다. 효율적으로 활용합니다.",
    "선행보다 현행이 중요합니다. 지금 배우는 것을 확실히 해야 합니다.",
    "스스로 공부하는 방법을 알려드립니다. 과외가 끝나도 혼자 할 수 있어야 합니다.",
    "흥미를 유지하도록 합니다. 재미가 있어야 오래 합니다.",
    "실력에 맞는 교재를 선택합니다. 너무 쉽거나 어려우면 효과가 없습니다.",
    "정기적인 테스트로 실력을 점검합니다. 현재 위치를 알아야 합니다.",
    "취약한 단원을 집중적으로 보완합니다. 모든 단원을 똑같이 하지 않습니다.",
    "문제를 읽는 방법부터 알려드립니다. 문제 이해가 반입니다.",
    "계산 실수를 줄이는 방법을 훈련합니다. 실수도 실력입니다.",
    "긴 지문을 빠르게 읽는 연습을 합니다. 시간 싸움이기 때문입니다.",
    "어려운 개념도 쉽게 풀어서 설명합니다. 이해가 안 되면 다른 방법으로 설명합니다.",
    "학생의 페이스에 맞춥니다. 빠르게 갈 수 있으면 빠르게, 천천히 가야 하면 천천히.",
    "자신감을 키워줍니다. 할 수 있다는 믿음이 중요합니다.",
    "꾸준함이 중요함을 알려드립니다. 하루에 많이 하는 것보다 매일 조금씩이 낫습니다.",
    "결과를 급하게 기대하지 않습니다. 시간이 필요합니다. 꾸준히 하면 반드시 오릅니다.",
]


def rewrite_file(filepath, pool_index):
    """파일을 표현 풀을 사용하여 리라이팅"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return False, f"읽기 실패: {e}"

    # 아이보리 박스 패턴
    box_pattern = r'(<div style="background-color: #FDF8F0[^>]*>\s*<strong>이렇게 수업합니다!</strong><br>\s*)([^<]+)(</div>)'

    # 박스가 없으면 스킵
    if not re.search(box_pattern, content):
        return False, "아이보리 박스 없음"

    # 박스 교체
    box_count = len(re.findall(box_pattern, content))
    box_idx = [0]

    def replace_box(m):
        # 인덱스 계산 - 다양한 조합 사용
        idx = (pool_index * 7 + box_idx[0] * 13) % len(GUIDE_BOX_POOL)
        replacement = GUIDE_BOX_POOL[idx]
        box_idx[0] += 1
        return f'{m.group(1)}{replacement}\n{m.group(3)}'

    new_content = re.sub(box_pattern, replace_box, content)

    # 변경이 없으면 스킵
    if new_content == content:
        return False, "변경 없음"

    # 파일 쓰기
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True, "성공"
    except Exception as e:
        return False, f"쓰기 실패: {e}"


def process_folder(folder_path, start_index=0):
    """폴더 내 모든 파일 처리"""
    files = []

    for root, dirs, filenames in os.walk(folder_path):
        for filename in filenames:
            if filename.endswith('.md') and not filename.startswith('_'):
                filepath = os.path.join(root, filename)
                files.append(filepath)

    print(f"  - {os.path.basename(folder_path)}: {len(files)}개 파일")

    success_count = 0
    fail_count = 0
    skip_count = 0

    for idx, filepath in enumerate(files):
        success, msg = rewrite_file(filepath, start_index + idx)
        if success:
            success_count += 1
        elif msg == "아이보리 박스 없음" or msg == "변경 없음":
            skip_count += 1
        else:
            fail_count += 1
            print(f"    실패: {os.path.basename(filepath)} - {msg}")

    return success_count, fail_count, skip_count, len(files)


def main():
    # 처리할 폴더 목록
    base_path = '/home/user/edu-guide/content'
    folders = [
        'tutoring',
        'subjects',
        'local',
        'high',
        'middle',
        'exam',
        'consultation',
        'elementary',
        'cities',
    ]

    total_success = 0
    total_fail = 0
    total_skip = 0
    total_files = 0
    current_index = 0

    print("=== 가이드 콘텐츠 리라이팅 시작 ===\n")

    for folder in folders:
        folder_path = os.path.join(base_path, folder)
        if os.path.exists(folder_path):
            success, fail, skip, count = process_folder(folder_path, current_index)
            total_success += success
            total_fail += fail
            total_skip += skip
            total_files += count
            current_index += count

    print(f"\n=== 완료 ===")
    print(f"총 파일: {total_files}")
    print(f"성공: {total_success}")
    print(f"스킵 (박스 없음): {total_skip}")
    print(f"실패: {total_fail}")


if __name__ == '__main__':
    main()
