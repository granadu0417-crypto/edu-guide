#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
중복 이미지 해결 스크립트 v3
- 같은 구(區) 내에서 절대 중복 없음
- 폴더별로 순차 배정
- 최대한 고르게 분산
"""

import os
import re
from pathlib import Path
from collections import defaultdict

# 대규모 이미지 풀 (190개)
ALL_IMAGES = [
    # 수학 관련 (30개)
    "photo-1635070041078-e363dbe005cb",
    "photo-1596495578065-6e0763fa1178",
    "photo-1509228468518-180dd4864904",
    "photo-1635070041409-e63e783ce3b1",
    "photo-1518133910546-b6c2fb7d79e3",
    "photo-1453733190371-0a9bedd82893",
    "photo-1596495577886-d920f1fb7238",
    "photo-1611532736597-de2d4265fba3",
    "photo-1580894894513-541e068a3e2b",
    "photo-1613909207039-6b173b755cc1",
    "photo-1559494007-9f5847c49d94",
    "photo-1544383835-bda2bc66a55d",
    "photo-1518435579668-52e6c59a9c85",
    "photo-1611329857570-f02f340e7378",
    "photo-1512314889357-e157c22f938d",
    "photo-1516796181074-bf453fbfa3e6",
    "photo-1515879218367-8466d910aaa4",
    "photo-1554475901-4538ddfbccc2",
    "photo-1581078426770-6d336e5de7bf",
    "photo-1611348586804-61bf6c080437",
    "photo-1611348524140-53c9a25263d6",
    "photo-1611351888222-c5797b8b5c2f",
    "photo-1596495577933-6c64e3a7d20a",
    "photo-1580894732444-8ecded7900cd",
    "photo-1580894732930-0babd100d356",
    "photo-1611532736579-6b16e2b50449",
    "photo-1596495578144-45fa0dc87783",
    "photo-1611329532992-0b7ba27d85fb",
    "photo-1596495578034-4b9c9c7b0de9",
    "photo-1509228627152-72ae9ae6848d",
    # 영어 관련 (30개)
    "photo-1457369804613-52c61a468e7d",
    "photo-1456513080510-7bf3a84b82f8",
    "photo-1546410531-bb4caa6b424d",
    "photo-1553877522-43269d4ea984",
    "photo-1515378791036-0648a3ef77b2",
    "photo-1519389950473-47ba0277781c",
    "photo-1523240795612-9a054b0db644",
    "photo-1488190211105-8b0e65b80b4e",
    "photo-1434030216411-0b793f4b4173",
    "photo-1455390582262-044cdead277a",
    "photo-1471107340929-a87cd0f5b5f3",
    "photo-1415369629372-26f2fe60c467",
    "photo-1447069387593-a5de0862481e",
    "photo-1476234251651-f353703a034d",
    "photo-1516321497487-e288fb19713f",
    "photo-1521587760476-6c12a4b040da",
    "photo-1507842217343-583bb7270b66",
    "photo-1497633762265-9d179a990aa6",
    "photo-1516979187457-637abb4f9353",
    "photo-1512820790803-83ca734da794",
    "photo-1550399105-c4db5fb85c18",
    "photo-1491841573634-28140fc7ced7",
    "photo-1473186578172-c141e6798cf4",
    "photo-1510154221590-ff0b49f38f88",
    "photo-1481627834876-b7833e8f5570",
    "photo-1474932430478-367dbb6832c1",
    "photo-1532012197267-da84d127e765",
    "photo-1506880018603-83d5b814b5a6",
    "photo-1519682337058-a94d519337bc",
    "photo-1457314880312-5d4aa18f8bc1",
    # 학생/공부 (40개)
    "photo-1503676260728-1c00da094a0b",
    "photo-1522202176988-66273c2fd55f",
    "photo-1517842645767-c639042777db",
    "photo-1513258496099-48168024aec0",
    "photo-1427504494785-3a9ca7044f45",
    "photo-1571260899304-425eee4c7efc",
    "photo-1519406596751-0a3ccc4937fe",
    "photo-1524178232363-1fb2b075b655",
    "photo-1509062522246-3755977927d7",
    "photo-1544717305-2782549b5136",
    "photo-1544717301-9cdcb1f5940f",
    "photo-1529390079861-591de354faf5",
    "photo-1501504905252-473c47e087f8",
    "photo-1509869175650-a1d97972541a",
    "photo-1510531704581-5b2870972060",
    "photo-1528980917907-8df7f48f6f2a",
    "photo-1525921429624-479b6a26d84d",
    "photo-1588072432836-e10032774350",
    "photo-1588702547923-7093a6c3ba33",
    "photo-1587691592099-24045742c181",
    "photo-1580894906475-403935091be2",
    "photo-1573497019940-1c28c88b4f3e",
    "photo-1573496359142-b8d87734a5a2",
    "photo-1573497019236-17f8177b81e8",
    "photo-1573497161161-c3e73707e25c",
    "photo-1577896851231-70ef18881754",
    "photo-1578574577315-3fbeb0cecdc2",
    "photo-1580582932707-520aed937b7b",
    "photo-1580894908361-967195033215",
    "photo-1582719478250-c89cae4dc85b",
    "photo-1584697964358-3e14ca57658b",
    "photo-1588196749597-9ff075ee6b5b",
    "photo-1588345921523-c2dcdb7f1dcd",
    "photo-1509228627152-72ae9ae6848d",
    "photo-1454165804606-c3d57bc86b40",
    "photo-1513128034602-7814ccaddd4e",
    "photo-1560785496-3c9d27877182",
    "photo-1531482615713-2afd69097998",
    "photo-1517048676732-d65bc937f952",
    "photo-1486312338219-ce68d2c6f44d",
    # 교실/학교 (30개)
    "photo-1562774053-701939374585",
    "photo-1544717305-f9c88f2897bc",
    "photo-1541339907198-e08756dedf3f",
    "photo-1511629091441-ee46146481b6",
    "photo-1507003211169-0a1dd7228f2d",
    "photo-1594608661623-aa0bd3a69d98",
    "photo-1596496578664-db76b5bf3f63",
    "photo-1596496181848-3091d4878b24",
    "photo-1596496050827-8299e0220de1",
    "photo-1596496050755-c923e73e42e1",
    "photo-1606761568499-6d2451b23c66",
    "photo-1591123120675-6f7f1aae0e5b",
    "photo-1598025678451-af5c59b29c40",
    "photo-1599687267812-35c05ff70ee9",
    "photo-1600195077077-7c815f540a3d",
    "photo-1604134967494-8a9ed3adea0d",
    "photo-1604580864964-0462f5d5b1a8",
    "photo-1605711285791-0219e80e43a3",
    "photo-1607013407627-6ee814329547",
    "photo-1610484826967-09c5720778c7",
    "photo-1546953304-5d96f43c2e94",
    "photo-1592280771190-3e2e4d977f1e",
    "photo-1580537659466-0a9bfa916a54",
    "photo-1523050854058-8df90110c9f1",
    "photo-1522071820081-009f0129c71c",
    "photo-1551836022-deb4988cc6c0",
    "photo-1552664730-d307ca884978",
    "photo-1531538606174-0f90ff5dce83",
    "photo-1517245386807-bb43f82c33c4",
    "photo-1560439514-4e9645039924",
    # 책/노트/문구류 (20개)
    "photo-1544716278-ca5e3f4abd8c",
    "photo-1489533119213-66a5cd877091",
    "photo-1544716278-e513176f20b5",
    "photo-1568667256549-094345857637",
    "photo-1553729459-efe14ef6055d",
    "photo-1554048612-b6a482bc67e5",
    "photo-1535905557558-afc4877a26fc",
    "photo-1544947950-fa07a98d237f",
    "photo-1476234251651-f353703a034d",
    "photo-1507842217343-583bb7270b66",
    "photo-1415369629372-26f2fe60c467",
    "photo-1491841573634-28140fc7ced7",
    "photo-1473186578172-c141e6798cf4",
    "photo-1510154221590-ff0b49f38f88",
    "photo-1532012197267-da84d127e765",
    "photo-1506880018603-83d5b814b5a6",
    "photo-1519682337058-a94d519337bc",
    "photo-1457314880312-5d4aa18f8bc1",
    "photo-1455390582262-044cdead277a",
    "photo-1471107340929-a87cd0f5b5f3",
    # 튜터링/1:1 수업 (20개)
    "photo-1515187029135-18ee286d815b",
    "photo-1611162617474-5b21e879e113",
    "photo-1611162616475-46b635cb6868",
    "photo-1611162618071-b39a2ec055fb",
    "photo-1611162617213-7d7a39e9b1d7",
    "photo-1599687351724-dfa3c4ff81b5",
    "photo-1609234656388-0ff363383899",
    "photo-1609234656432-46d0b41c3dad",
    "photo-1622556498246-755f44ca76f3",
    "photo-1603354350317-6f7aaa5911c5",
    "photo-1603354350266-f2b10492ea3e",
    "photo-1607990281513-2c110a25bd8c",
    "photo-1588702547919-26089e690ecc",
    "photo-1588702547954-4800ead296ef",
    "photo-1593642632823-8f785ba67e45",
    "photo-1596496181871-9681eacf9764",
    "photo-1542626991-cbc4e32524cc",
    "photo-1507537297725-24a1c029d3ca",
    "photo-1521737711867-e3b97375f902",
    "photo-1521737852567-6949f3f9f2b5",
    # 추가 교육 이미지 (20개)
    "photo-1600880292203-757bb62b4baf",
    "photo-1557804506-669a67965ba0",
    "photo-1556911220-e15b29be8c8f",
    "photo-1513001900722-370f803f498d",
    "photo-1461749280684-dccba630e2f6",
    "photo-1505682634904-d7c8d95cdc50",
    "photo-1516534775068-ba3e7458af70",
    "photo-1587825140708-dfaf72ae4b04",
    "photo-1503454537195-1dcabb73ffb9",
    "photo-1516627145497-ae6968895b74",
    "photo-1558618666-fcd25c85cd64",
    "photo-1551434678-e076c223a692",
    "photo-1454165804606-c3d57bc86b40",
    "photo-1434030216411-0b793f4b4173",
    "photo-1456513080510-7bf3a84b82f8",
    "photo-1512820790803-83ca734da794",
    "photo-1550399105-c4db5fb85c18",
    "photo-1481627834876-b7833e8f5570",
    "photo-1474932430478-367dbb6832c1",
    "photo-1497633762265-9d179a990aa6",
]

def get_image_url(photo_id):
    """Unsplash 이미지 URL 생성"""
    return f"https://images.unsplash.com/{photo_id}?w=1200&h=630&fit=crop"

def extract_district(filename):
    """파일명에서 구(區) 이름 추출"""
    # gangnam-apgujeong1-high-math.md -> gangnam
    parts = filename.split('-')
    if parts:
        return parts[0]
    return 'unknown'

def process_files():
    """모든 파일에 고유 이미지 배정"""
    content_dir = Path('/home/user/edu-guide/content')
    folders = ['high', 'middle', 'local', 'tutoring', 'subjects', 'elementary', 'exam', 'consultation']

    # 폴더별 + 구별로 파일 그룹화
    folder_district_files = defaultdict(lambda: defaultdict(list))

    for folder in folders:
        folder_path = content_dir / folder
        if not folder_path.exists():
            continue

        md_files = list(folder_path.glob('*.md'))
        md_files = [f for f in md_files if f.stem != '_index']

        for md_file in sorted(md_files):
            district = extract_district(md_file.stem)
            folder_district_files[folder][district].append(md_file)

    # 전역 이미지 인덱스 (폴더마다 다른 시작점)
    folder_offset = {
        'high': 0,
        'middle': 50,
        'local': 100,
        'tutoring': 120,
        'subjects': 140,
        'elementary': 145,
        'exam': 160,
        'consultation': 175,
    }

    total_updated = 0
    image_usage = defaultdict(int)

    for folder in folders:
        if folder not in folder_district_files:
            continue

        folder_count = 0
        base_offset = folder_offset.get(folder, 0)

        # 각 구(區)별로 순차 배정
        district_idx = 0
        for district, files in sorted(folder_district_files[folder].items()):
            for file_idx, md_file in enumerate(files):
                # 구마다 시작 인덱스를 다르게 + 파일 인덱스
                # 이렇게 하면 같은 구 내에서 겹치지 않음
                img_idx = (base_offset + district_idx * 10 + file_idx) % len(ALL_IMAGES)

                # 파일 업데이트
                try:
                    with open(md_file, 'r', encoding='utf-8') as f:
                        content = f.read()

                    pattern = r'(featured_image:\s*)["\']?https://images\.unsplash\.com/[^"\'\n]+["\']?'
                    new_url = get_image_url(ALL_IMAGES[img_idx])
                    replacement = f'featured_image: "{new_url}"'

                    new_content, count = re.subn(pattern, replacement, content)

                    if count > 0:
                        with open(md_file, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        folder_count += 1
                        total_updated += 1
                        image_usage[ALL_IMAGES[img_idx]] += 1

                except Exception as e:
                    print(f"Error: {md_file}: {e}")

            district_idx += 1

        print(f"{folder}: {folder_count} 파일 업데이트")

    print(f"\n총 {total_updated} 파일 업데이트 완료")
    print(f"사용된 고유 이미지: {len(image_usage)}개")

    # 중복 통계
    duplicates = {k: v for k, v in image_usage.items() if v >= 3}
    if duplicates:
        print(f"\n3회 이상 사용: {len(duplicates)}개")
        for img, count in sorted(duplicates.items(), key=lambda x: -x[1])[:5]:
            print(f"  {count}회: {img}")

def main():
    print(f"이미지 풀 크기: {len(ALL_IMAGES)}개")
    print("=" * 60)
    process_files()

if __name__ == '__main__':
    main()
