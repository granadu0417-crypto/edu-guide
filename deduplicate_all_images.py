#!/usr/bin/env python3
"""
전체 사이트 이미지 중복 제거 스크립트
모든 .md 파일에 고유한 교육/학습 관련 이미지 할당
"""

import os
import re
import hashlib
from pathlib import Path
from collections import defaultdict

# 교육/학습 관련 Unsplash 이미지 풀 (150개)
EDUCATION_IMAGES = [
    # 학습/공부 (30개)
    "photo-1434030216411-0b793f4b4173",  # 책상, 노트, 공부
    "photo-1456513080510-7bf3a84b82f8",  # 펜과 노트
    "photo-1503676260728-1c00da094a0b",  # 공부하는 학생들
    "photo-1513001900722-370f803f498d",  # 책과 공부
    "photo-1509062522246-3755977927d7",  # 학습 자료
    "photo-1427504494785-3a9ca7044f45",  # 교실
    "photo-1488998427799-e3362cec87c3",  # 노트북과 공부
    "photo-1522202176988-66273c2fd55f",  # 그룹 스터디
    "photo-1497215842964-222b430dc094",  # 컴퓨터 학습
    "photo-1519389950473-47ba0277781c",  # 회의/토론
    "photo-1524178232363-1fb2b075b655",  # 노트 필기
    "photo-1491841651911-c44c30c34548",  # 독서
    "photo-1523240795612-9a054b0db644",  # 책장
    "photo-1457369804613-52c61a468e7d",  # 책 읽기
    "photo-1497633762265-9d179a990aa6",  # 도서관 책
    "photo-1481627834876-b7833e8f5570",  # 책 더미
    "photo-1516979187457-637abb4f9353",  # 공부 중
    "photo-1454165804606-c3d57bc86b40",  # 책상 위 책
    "photo-1476357471311-43c0db9fb2b4",  # 학습 환경
    "photo-1455390582262-044cdead277a",  # 책 읽기
    "photo-1519389950473-47ba0277781c",  # 테이블 학습
    "photo-1472173148041-00294f0814a2",  # 공부 책상
    "photo-1484480974693-6ca0a78fb36b",  # 플래너 노트
    "photo-1450101499163-c8848c66ca85",  # 손 글씨
    "photo-1503454537195-1dcabb73ffb9",  # 어린이 학습
    "photo-1546410531-bb4caa6b424d",  # 영어 알파벳
    "photo-1635070041078-e363dbe005cb",  # 수학 공식
    "photo-1532094349884-543bc11b234d",  # 과학 실험
    "photo-1526666923127-b2970f64b422",  # 지구본
    "photo-1573164574230-db1d5e960238",  # 상담

    # 교육 환경 (20개)
    "photo-1588196749597-9ff075ee6b5b",  # 교실 환경
    "photo-1509228468518-180dd4864904",  # 학교
    "photo-1515169067868-5387ec356754",  # 강의실
    "photo-1521737711867-e3b97375f902",  # 세미나
    "photo-1523050854058-8df90110c9f1",  # 강당
    "photo-1562774053-701939374585",  # 교육 시설
    "photo-1580582932707-520aed937b7b",  # 책상 배치
    "photo-1577896851231-70ef18881754",  # 학습 공간
    "photo-1557804506-669a67965ba0",  # 회의실
    "photo-1553877522-43269d4ea984",  # 도서관
    "photo-1521587760476-6c12a4b040da",  # 독서실
    "photo-1524995997946-a1c2e315a42f",  # 열람실
    "photo-1507003211169-0a1dd7228f2d",  # 사무 환경
    "photo-1573496359142-b8d87734a5a2",  # 학습실
    "photo-1517842645767-c639042777db",  # 세미나실
    "photo-1552664730-d307ca884978",  # 학원
    "photo-1556761175-4b46a572b786",  # 교육 센터
    "photo-1517245386807-bb43f82c33c4",  # 컨퍼런스
    "photo-1515187029135-18ee286d815b",  # 강의
    "photo-1531482615713-2afd69097998",  # 교육 공간

    # 학생/사람 (20개)
    "photo-1543269865-0a740d43b90c",  # 학생 개인
    "photo-1596495577886-d920f1fb7238",  # 공부하는 학생
    "photo-1488190211105-8b0e65b80b4e",  # 집중하는 학생
    "photo-1516534775068-ba3e7458af70",  # 학습 중인 학생
    "photo-1529070538774-1843cb3265df",  # 초등학생
    "photo-1503454537195-1dcabb73ffb9",  # 어린이
    "photo-1544776193-352d25ca82cd",  # 청소년
    "photo-1464082354059-27db6ce50048",  # 고등학생
    "photo-1517694712202-14dd9538aa97",  # 대학생
    "photo-1554224155-8d04cb21cd6c",  # 그룹 학습
    "photo-1522071820081-009f0129c71c",  # 팀 스터디
    "photo-1524661135-423995f22d0b",  # 도시 학생
    "photo-1488646953014-85cb44e25828",  # 선생님
    "photo-1511629091441-ee46146481b6",  # 강사
    "photo-1573497019940-1c28c88b4f3e",  # 멘토
    "photo-1573496359142-b8d87734a5a2",  # 교육자
    "photo-1551836022-d5d88e9218df",  # 수업 중
    "photo-1554224154-26032ffc0d07",  # 강의 중
    "photo-1611162617474-5b21e879e113",  # 튜터
    "photo-1573496774426-fe3dce7ef4df",  # 코칭

    # 학습 도구 (20개)
    "photo-1471107340929-a87cd0f5b5f3",  # 책
    "photo-1476357471311-43c0db9fb2b4",  # 공책
    "photo-1455390582262-044cdead277a",  # 교과서
    "photo-1512820790803-83ca734da794",  # 참고서
    "photo-1506784983877-45594efa4cbe",  # 노트
    "photo-1517842645767-c639042777db",  # 필기구
    "photo-1455390582262-044cdead277a",  # 연필
    "photo-1587825140708-dfaf72ae4b04",  # 펜
    "photo-1488190211105-8b0e65b80b4e",  # 형광펜
    "photo-1611162616475-46b635cb6868",  # 자
    "photo-1635070041078-e363dbe005cb",  # 계산기
    "photo-1584308666744-24d5c474f2ae",  # 컴퓨터
    "photo-1484417894907-623942c8ee29",  # 태블릿
    "photo-1588196749597-9ff075ee6b5b",  # 칠판
    "photo-1562654501-a0ccc0fc3fb1",  # 화이트보드
    "photo-1532622785990-d2c36a76f5a6",  # 프로젝터
    "photo-1581092160562-40aa08e78837",  # 마이크
    "photo-1517842645767-c639042777db",  # 스피커
    "photo-1581090464777-f3220bbe1b8b",  # 헤드폰
    "photo-1611162616475-46b635cb6868",  # 웹캠

    # 과목별 (20개)
    "photo-1455390582262-044cdead277a",  # 국어
    "photo-1546410531-bb4caa6b424d",  # 영어
    "photo-1635070041078-e363dbe005cb",  # 수학
    "photo-1532094349884-543bc11b234d",  # 과학
    "photo-1526666923127-b2970f64b422",  # 사회
    "photo-1518770660439-4636190af475",  # 역사
    "photo-1453906971074-ce568cccbc63",  # 지리
    "photo-1517245386807-bb43f82c33c4",  # 윤리
    "photo-1553877522-43269d4ea984",  # 철학
    "photo-1509228468518-180dd4864904",  # 체육
    "photo-1507003211169-0a1dd7228f2d",  # 음악
    "photo-1460661419201-fd4cecdf8a8b",  # 미술
    "photo-1484417894907-623942c8ee29",  # 정보
    "photo-1488190211105-8b0e65b80b4e",  # 기술
    "photo-1498050108023-c5249f4df085",  # 코딩
    "photo-1516321318423-f06f85e504b3",  # 로봇
    "photo-1581091226825-a6a2a5aee158",  # 과학실험
    "photo-1562774053-701939374585",  # 화학
    "photo-1614935151651-0bea6508db6b",  # 물리
    "photo-1581092921461-eab62e97a780",  # 생물

    # 학습 활동 (20개)
    "photo-1522202176988-66273c2fd55f",  # 토론
    "photo-1552664730-d307ca884978",  # 발표
    "photo-1521737711867-e3b97375f902",  # 프레젠테이션
    "photo-1517842645767-c639042777db",  # 세미나
    "photo-1515187029135-18ee286d815b",  # 강연
    "photo-1507537297725-24a1c029d3ca",  # 워크샵
    "photo-1588196749597-9ff075ee6b5b",  # 실습
    "photo-1573497019940-1c28c88b4f3e",  # 실험
    "photo-1606326608606-aa0b62935f2b",  # 프로젝트
    "photo-1556761175-4b46a572b786",  # 과제
    "photo-1600880292089-90a7e086ee0c",  # 시험
    "photo-1434030216411-0b793f4b4173",  # 평가
    "photo-1517842645767-c639042777db",  # 리뷰
    "photo-1522202176988-66273c2fd55f",  # 협업
    "photo-1531482615713-2afd69097998",  # 팀워크
    "photo-1573497019940-1c28c88b4f3e",  # 멘토링
    "photo-1573496359142-b8d87734a5a2",  # 코칭
    "photo-1611162617474-5b21e879e113",  # 튜터링
    "photo-1589395937527-f9d5b2a9e1f9",  # 상담
    "photo-1573164574230-db1d5e960238",  # 컨설팅

    # 학습 성과 (20개)
    "photo-1531844251246-9a1bfaae09fc",  # 졸업
    "photo-1523050854058-8df90110c9f1",  # 학위
    "photo-1541339907198-e08756dedf3f",  # 성취
    "photo-1523240795612-9a054b0db644",  # 성공
    "photo-1454165804606-c3d57bc86b40",  # 목표
    "photo-1450101499163-c8848c66ca85",  # 계획
    "photo-1484480974693-6ca0a78fb36b",  # 전략
    "photo-1488190211105-8b0e65b80b4e",  # 진로
    "photo-1522202176988-66273c2fd55f",  # 경력
    "photo-1553877522-43269d4ea984",  # 미래
    "photo-1517842645767-c639042777db",  # 비전
    "photo-1531482615713-2afd69097998",  # 꿈
    "photo-1531844251246-9a1bfaae09fc",  # 희망
    "photo-1523240795612-9a054b0db644",  # 열정
    "photo-1573497019940-1c28c88b4f3e",  # 도전
    "photo-1573496359142-b8d87734a5a2",  # 성장
    "photo-1611162617474-5b21e879e113",  # 발전
    "photo-1589395937527-f9d5b2a9e1f9",  # 향상
    "photo-1573164574230-db1d5e960238",  # 개선
    "photo-1531844251246-9a1bfaae09fc",  # 우수
]

def get_unique_image_for_file(filepath, used_images):
    """파일 경로 기반 해시로 고유 이미지 할당"""
    # 파일 경로의 MD5 해시 생성
    file_hash = hashlib.md5(str(filepath).encode()).hexdigest()
    hash_int = int(file_hash, 16)

    # 사용 가능한 이미지 찾기
    for i in range(len(EDUCATION_IMAGES)):
        index = (hash_int + i) % len(EDUCATION_IMAGES)
        image_id = EDUCATION_IMAGES[index]
        if image_id not in used_images:
            return image_id

    # 모든 이미지가 사용된 경우 (150개 이상의 파일)
    # 해시 기반으로 선택
    return EDUCATION_IMAGES[hash_int % len(EDUCATION_IMAGES)]

def update_featured_image(filepath, new_image_id):
    """featured_image 업데이트"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        if not content.startswith('---'):
            return False

        parts = content.split('---', 2)
        if len(parts) < 3:
            return False

        frontmatter = parts[1]
        body = parts[2]

        # 기존 featured_image 찾기
        old_match = re.search(r'featured_image:\s*.+', frontmatter)
        new_url = f'https://images.unsplash.com/{new_image_id}?w=1200&h=630&fit=crop'

        if old_match:
            # 교체
            new_frontmatter = frontmatter.replace(
                old_match.group(0),
                f'featured_image: {new_url}'
            )
        else:
            # 없으면 추가
            new_frontmatter = frontmatter + f'\nfeatured_image: {new_url}\n'

        # 파일 쓰기
        new_content = f'---{new_frontmatter}---{body}'
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

        return True

    except Exception as e:
        print(f"❌ Error updating {filepath}: {e}")
        return False

def main():
    """메인 함수"""
    base_path = Path("/mnt/c/Users/user/Desktop/클로드/에듀코리아/edu-guide/content")

    print("=" * 80)
    print("🎨 전체 사이트 이미지 중복 제거\n")

    # 모든 .md 파일 찾기 (_index.md 제외)
    all_files = []
    for md_file in base_path.rglob('*.md'):
        if md_file.name != '_index.md':  # 섹션 _index.md는 이미 처리됨
            all_files.append(md_file)

    print(f"📊 발견된 파일: {len(all_files)}개\n")

    # 이미지 할당
    used_images = set()
    file_image_map = {}

    for filepath in all_files:
        image_id = get_unique_image_for_file(filepath, used_images)
        file_image_map[filepath] = image_id
        used_images.add(image_id)

    print(f"✅ 고유 이미지 할당 완료: {len(used_images)}개 이미지 사용\n")

    # 파일 업데이트
    print("=" * 80)
    print("🔧 이미지 업데이트 중...\n")

    updated_count = 0
    error_count = 0

    for filepath, image_id in file_image_map.items():
        if update_featured_image(filepath, image_id):
            updated_count += 1
            if updated_count % 100 == 0:
                print(f"  ✅ {updated_count}개 파일 처리됨...")
        else:
            error_count += 1

    # 결과 출력
    print("\n" + "=" * 80)
    print(f"\n📊 완료\n")
    print(f"✅ 수정됨: {updated_count}개")
    print(f"❌ 오류: {error_count}개")
    print(f"\n총 파일: {len(all_files)}개")
    print(f"고유 이미지: {len(used_images)}개 / {len(EDUCATION_IMAGES)}개 사용 가능\n")

if __name__ == "__main__":
    main()
