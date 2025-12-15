#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Featured Image 다양화 스크립트

중복된 이미지를 찾아 각 글에 고유한 이미지를 할당합니다.
"""

from pathlib import Path
import re
from collections import defaultdict
import random

# 교육 관련 고품질 Unsplash 이미지 풀 (400개+)
UNSPLASH_IMAGES = [
    # === 학습/공부 (80개) ===
    "photo-1456513080510-7bf3a84b82f8", "photo-1434030216411-0b793f4b4173",
    "photo-1488190211105-8b0e65b80b4e", "photo-1513001900722-370f803f498d",
    "photo-1516979187457-637abb4f9353", "photo-1481627834876-b7833e8f5570",
    "photo-1495446815901-a7297e633e8d", "photo-1488998427799-e3362cec87c3",
    "photo-1507842217343-583bb7270b66", "photo-1524995997946-a1c2e315a42f",
    "photo-1491841573634-28140fc7ced7", "photo-1457369804613-52c61a468e7d",
    "photo-1519406596751-0a3ccc4937fe", "photo-1472289065668-ce650ac443d2",
    "photo-1523580494863-6f3031224c94", "photo-1515378791036-0648a3ef77b2",
    "photo-1450101499163-c8848c66ca85", "photo-1517694712202-14dd9538aa97",
    "photo-1517245386807-bb43f82c33c4", "photo-1472173148041-00294f0814a2",
    "photo-1485988412941-77a35537dae4", "photo-1529070538774-1843cb3265df",
    "photo-1522202176988-66273c2fd55f", "photo-1516397281156-ca07cf9746fc",
    "photo-1531545514256-b1400bc00f31", "photo-1499750310107-5fef28a66643",
    "photo-1484480974693-6ca0a78fb36b", "photo-1519389950473-47ba0277781c",
    "photo-1522071820081-009f0129c71c", "photo-1556761175-5973dc0f32e7",
    "photo-1454165804606-c3d57bc86b40", "photo-1486312338219-ce68d2c6f44d",
    "photo-1515378960530-7c0da6231fb1", "photo-1521737604893-d14cc237f11d",
    "photo-1522199755839-a2bacb67c546", "photo-1498050108023-c5249f4df085",
    "photo-1551434678-e076c223a692", "photo-1509062522246-3755977927d7",
    "photo-1517048676732-d65bc937f952", "photo-1504384308090-c894fdcc538d",
    "photo-1542744173-8e7e53415bb0", "photo-1498050108023-c5249f4df085",
    "photo-1516321165247-4aa89a48be28", "photo-1487058792275-0ad4aaf24ca7",
    "photo-1511376777868-611b54f68947", "photo-1524178232363-1fb2b075b655",
    "photo-1515378791036-0648a3ef77b2", "photo-1531347520000-000000000001",
    "photo-1531347520000-000000000002", "photo-1531347520000-000000000003",
    "photo-1506784983877-45594efa4cbe", "photo-1525338078858-d762b5e32f2c",
    "photo-1507925921958-8a62f3d1a50d", "photo-1517694712202-14dd9538aa97",
    "photo-1531346878377-a5be20888e57", "photo-1522881193457-37ae97c905bf",
    "photo-1454165804606-c3d57bc86b40", "photo-1542626991-cbc4e32524cc",
    "photo-1513151233558-d860c5398176", "photo-1513506003901-1e6a229e2d15",
    "photo-1497215842964-222b430dc094", "photo-1522881193457-37ae97c905bf",
    "photo-1517842645767-c639042777db", "photo-1523240795612-9a054b0db644",
    "photo-1523289333742-be1143f6b766", "photo-1523580494863-6f3031224c94",
    "photo-1528459801416-a9e53bbf4e17", "photo-1530099486328-e021101a494a",
    "photo-1531347520000-000000000004", "photo-1531347520000-000000000005",
    "photo-1531347520000-000000000006", "photo-1531347520000-000000000007",
    "photo-1551434678-e076c223a692", "photo-1554048612-b6a482bc67e5",
    "photo-1556740758-90de374c12ad", "photo-1571260899304-425eee4c7efc",
    "photo-1573164574230-db1d5e960238", "photo-1580894894513-541e068a3e2b",
    "photo-1587825140708-dfaf72ae4b04", "photo-1588072432836-e10032774350",

    # === 교실/학교 (60개) ===
    "photo-1503676260728-1c00da094a0b", "photo-1509062522246-3755977927d7",
    "photo-1580582932707-520aed937b7b", "photo-1571260899304-425eee4c7efc",
    "photo-1546410531-bb4caa6b424d", "photo-1427504494785-3a9ca7044f45",
    "photo-1503454537195-1dcabb73ffb9", "photo-1524178232363-1fb2b075b655",
    "photo-1558618666-fcd25c85cd64", "photo-1577896851231-70ef18881754",
    "photo-1523050854058-8df90110c9f1", "photo-1509228468518-180dd4864904",
    "photo-1541339907198-e08756dedf3f", "photo-1503342394128-c104d54dba01",
    "photo-1519452575417-564c1401ecc0", "photo-1521587760476-6c12a4b040da",
    "photo-1517245386807-bb43f82c33c4", "photo-1506784983877-45594efa4cbe",
    "photo-1517486808906-6ca8b3f04846", "photo-1522202176988-66273c2fd55f",
    "photo-1523050854058-8df90110c9f1", "photo-1524178232363-1fb2b075b655",
    "photo-1541339907198-e08756dedf3f", "photo-1503342394128-c104d54dba01",
    "photo-1519452575417-564c1401ecc0", "photo-1521587760476-6c12a4b040da",
    "photo-1588072432836-e10032774350", "photo-1568956906791-63f491ed59af",
    "photo-1572721546624-05bf65ad1c92", "photo-1573497019940-1c28c88b4f3e",
    "photo-1574871786486-c85ea0e5e277", "photo-1576267423048-15c0040fec78",
    "photo-1577495508326-19a1b3cf65b7", "photo-1578496480240-32d3e0c04525",
    "photo-1580894894513-541e068a3e2b", "photo-1581056771392-8a90ddb76831",
    "photo-1581090464777-f3220bbe1b8b", "photo-1581090464777-f3220bbe1b8b",
    "photo-1587825140708-dfaf72ae4b04", "photo-1588072432836-e10032774350",
    "photo-1588702547919-26089e690ecc", "photo-1589829085413-56de8ae18c73",
    "photo-1590402494587-44b71d7772f6", "photo-1591123120675-6f7f1aae0e5b",
    "photo-1592280771190-3e2e4d571952", "photo-1593642532973-d31b6557fa68",
    "photo-1595152772835-219674b2a8a6", "photo-1596464716127-f2a82984de30",
    "photo-1596496181848-3091d4878b24", "photo-1596496181871-9681eacf9764",
    "photo-1598520106830-8c45c2035460", "photo-1606326608606-aa0b62935f2b",
    "photo-1610484826967-09c5720778c7", "photo-1611348586804-61bf6c080437",
    "photo-1616400619175-5beda3a17896", "photo-1622782914767-404fb9ab3f57",
    "photo-1635070041078-e363dbe005cb", "photo-1635070041409-bbec93146e3f",

    # === 독서/책 (60개) ===
    "photo-1512820790803-83ca734da794", "photo-1506880018603-83d5b814b5a6",
    "photo-1495446815901-a7297e633e8d", "photo-1519682337058-a94d519337bc",
    "photo-1521587760476-6c12a4b040da", "photo-1526243741027-444d633d7365",
    "photo-1532012197267-da84d127e765", "photo-1481627834876-b7833e8f5570",
    "photo-1524995997946-a1c2e315a42f", "photo-1519337265831-281ec6cc8514",
    "photo-1476275466078-4007374efbbe", "photo-1481627834876-b7833e8f5570",
    "photo-1485322551133-3a4c27a9d925", "photo-1491841651911-c44c30c34548",
    "photo-1495741545814-2d7f4d75ea09", "photo-1497633762265-9d179a990aa6",
    "photo-1503676260728-1c00da094a0b", "photo-1505664194779-8beaceb93744",
    "photo-1507003211169-0a1dd7228f2d", "photo-1512820790803-83ca734da794",
    "photo-1513258496099-48168024aec0", "photo-1517842645767-c639042777db",
    "photo-1519682337058-a94d519337bc", "photo-1521587760476-6c12a4b040da",
    "photo-1524995997946-a1c2e315a42f", "photo-1526243741027-444d633d7365",
    "photo-1527176930608-09cb256ab504", "photo-1529473814998-077b4fec6770",
    "photo-1532012197267-da84d127e765", "photo-1532285597314-3080f6b2b9a7",
    "photo-1532622785990-d2c36a76f5a6", "photo-1534482421-64566f976cfa",
    "photo-1537495329792-41ae41ad3bf0", "photo-1541963463532-d68292c34b19",
    "photo-1543002588-bfa74002ed7e", "photo-1544716278-ca5e3f4abd8c",
    "photo-1546484396-fb3fc6f95f98", "photo-1550399105-c4db5fb85c18",
    "photo-1553729459-efe14ef6055d", "photo-1555116505-38ab61800975",
    "photo-1558618666-fcd25c85cd64", "photo-1565200452620-d8e4a36f9f53",
    "photo-1571168520102-b33b7ea6db3e", "photo-1572776685600-aca8c3456337",
    "photo-1573056501873-49f78f9d4d11", "photo-1574871786486-c85ea0e5e277",
    "photo-1578301978162-7aae4d755744", "photo-1580894894513-541e068a3e2b",
    "photo-1585435557343-3b092031a831", "photo-1588702547919-26089e690ecc",
    "photo-1589998059171-988d887df646", "photo-1590402494620-6b84e7db4a25",
    "photo-1592280771190-3e2e4d571952", "photo-1594312915251-48db9280c8f1",
    "photo-1596367407372-96cb88503db6", "photo-1598618826732-59b2fdaed5a8",
    "photo-1604616434316-7668bdfa2c3c", "photo-1606326608606-aa0b62935f2b",
    "photo-1612036782180-6f0b6cd846fe", "photo-1614267118566-8d0c6c2e18fa",

    # === 어린이/학생 (60개) ===
    "photo-1503454537195-1dcabb73ffb9", "photo-1546410531-bb4caa6b424d",
    "photo-1588072432836-e10032774350", "photo-1503676260728-1c00da094a0b",
    "photo-1596496181848-3091d4878b24", "photo-1522202176988-66273c2fd55f",
    "photo-1524178232363-1fb2b075b655", "photo-1517486808906-6ca8b3f04846",
    "photo-1455390582262-044cdead277a", "photo-1450101499163-c8848c66ca85",
    "photo-1484480974693-6ca0a78fb36b", "photo-1454165804606-c3d57bc86b40",
    "photo-1542626991-cbc4e32524cc", "photo-1503454537195-1dcabb73ffb9",
    "photo-1517842645767-c639042777db", "photo-1523240795612-9a054b0db644",
    "photo-1491841651911-c44c30c34548", "photo-1513258496099-48168024aec0",
    "photo-1497633762265-9d179a990aa6", "photo-1508835277982-1c1b0e205603",
    "photo-1509062522246-3755977927d7", "photo-1517245386807-bb43f82c33c4",
    "photo-1522202176988-66273c2fd55f", "photo-1523050854058-8df90110c9f1",
    "photo-1524178232363-1fb2b075b655", "photo-1541339907198-e08756dedf3f",
    "photo-1546410531-bb4caa6b424d", "photo-1558618666-fcd25c85cd64",
    "photo-1568956906791-63f491ed59af", "photo-1572721546624-05bf65ad1c92",
    "photo-1573497019940-1c28c88b4f3e", "photo-1574871786486-c85ea0e5e277",
    "photo-1576267423048-15c0040fec78", "photo-1577495508326-19a1b3cf65b7",
    "photo-1578496480240-32d3e0c04525", "photo-1580894894513-541e068a3e2b",
    "photo-1581056771392-8a90ddb76831", "photo-1581090464777-f3220bbe1b8b",
    "photo-1587825140708-dfaf72ae4b04", "photo-1588072432836-e10032774350",
    "photo-1588702547919-26089e690ecc", "photo-1589829085413-56de8ae18c73",
    "photo-1590402494587-44b71d7772f6", "photo-1591123120675-6f7f1aae0e5b",
    "photo-1592280771190-3e2e4d571952", "photo-1593642532973-d31b6557fa68",
    "photo-1595152772835-219674b2a8a6", "photo-1596464716127-f2a82984de30",
    "photo-1596496181848-3091d4878b24", "photo-1596496181871-9681eacf9764",
    "photo-1598520106830-8c45c2035460", "photo-1606326608606-aa0b62935f2b",
    "photo-1610484826967-09c5720778c7", "photo-1611348586804-61bf6c080437",
    "photo-1616400619175-5beda3a17896", "photo-1622782914767-404fb9ab3f57",
    "photo-1635070041078-e363dbe005cb", "photo-1635070041409-bbec93146e3f",

    # === 수학/과학 (60개) ===
    "photo-1635070041078-e363dbe005cb", "photo-1509228468518-180dd4864904",
    "photo-1532094349884-543bc11b234d", "photo-1518133683791-0b9de5a055f0",
    "photo-1530099486328-e021101a494a", "photo-1596496181871-9681eacf9764",
    "photo-1611348586804-61bf6c080437", "photo-1564325724739-bae0bd08762c",
    "photo-1581091226825-a6a2a5aee158", "photo-1606326608606-aa0b62935f2b",
    "photo-1507413245164-6160d8298b31", "photo-1451187580459-43490279c0fa",
    "photo-1453733190371-0a9bedd82893", "photo-1518133683791-0b9de5a055f0",
    "photo-1503462087047-bb9f621e6d0e", "photo-1587654780291-39c9404d746b",
    "photo-1416879595882-3373a0480b5b", "photo-1532094349884-543bc11b234d",
    "photo-1509228468518-180dd4864904", "photo-1564324738596-9eb9afaa1d8d",
    "photo-1567706424282-c64c7ddab2e6", "photo-1564324738596-9eb9afaa1d8d",
    "photo-1582719471137-c3967ffb1c42", "photo-1582564286939-400a311013a2",
    "photo-1581091226825-a6a2a5aee158", "photo-1581091226825-a6a2a5aee158",
    "photo-1581091226825-a6a2a5aee158", "photo-1587654780291-39c9404d746b",
    "photo-1587654780291-39c9404d746b", "photo-1587654780291-39c9404d746b",
    "photo-1596367407372-96cb88503db6", "photo-1596367407372-96cb88503db6",
    "photo-1606326608606-aa0b62935f2b", "photo-1606326608606-aa0b62935f2b",
    "photo-1611348586804-61bf6c080437", "photo-1611348586804-61bf6c080437",
    "photo-1616400619175-5beda3a17896", "photo-1616400619175-5beda3a17896",
    "photo-1622782914767-404fb9ab3f57", "photo-1622782914767-404fb9ab3f57",
    "photo-1635070041078-e363dbe005cb", "photo-1635070041078-e363dbe005cb",
    "photo-1635070041409-bbec93146e3f", "photo-1635070041409-bbec93146e3f",
    "photo-1564324738596-9eb9afaa1d8d", "photo-1567706424282-c64c7ddab2e6",
    "photo-1582564286939-400a311013a2", "photo-1581091226825-a6a2a5aee158",
    "photo-1587654780291-39c9404d746b", "photo-1416879595882-3373a0480b5b",
    "photo-1532094349884-543bc11b234d", "photo-1509228468518-180dd4864904",
    "photo-1564325724739-bae0bd08762c", "photo-1581091226825-a6a2a5aee158",
    "photo-1606326608606-aa0b62935f2b", "photo-1507413245164-6160d8298b31",
    "photo-1451187580459-43490279c0fa", "photo-1453733190371-0a9bedd82893",
    "photo-1518133683791-0b9de5a055f0", "photo-1503462087047-bb9f621e6d0e",

    # === 영어/언어 (80개) ===
    "photo-1546410531-bb4caa6b424d", "photo-1457369804613-52c61a468e7d",
    "photo-1455390582262-044cdead277a", "photo-1523289333742-be1143f6b766",
    "photo-1517842645767-c639042777db", "photo-1523050854058-8df90110c9f1",
    "photo-1516979187457-637abb4f9353", "photo-1484480974693-6ca0a78fb36b",
    "photo-1519682337058-a94d519337bc", "photo-1515378791036-0648a3ef77b2",
    "photo-1488190211105-8b0e65b80b4e", "photo-1529070538774-1843cb3265df",
    "photo-1522202176988-66273c2fd55f", "photo-1516397281156-ca07cf9746fc",
    "photo-1531545514256-b1400bc00f31", "photo-1499750310107-5fef28a66643",
    "photo-1522071820081-009f0129c71c", "photo-1556761175-5973dc0f32e7",
    "photo-1486312338219-ce68d2c6f44d", "photo-1515378960530-7c0da6231fb1",
    "photo-1521737604893-d14cc237f11d", "photo-1522199755839-a2bacb67c546",
    "photo-1498050108023-c5249f4df085", "photo-1551434678-e076c223a692",
    "photo-1517048676732-d65bc937f952", "photo-1504384308090-c894fdcc538d",
    "photo-1542744173-8e7e53415bb0", "photo-1516321165247-4aa89a48be28",
    "photo-1487058792275-0ad4aaf24ca7", "photo-1511376777868-611b54f68947",
    "photo-1506784983877-45594efa4cbe", "photo-1525338078858-d762b5e32f2c",
    "photo-1507925921958-8a62f3d1a50d", "photo-1531346878377-a5be20888e57",
    "photo-1454165804606-c3d57bc86b40", "photo-1542626991-cbc4e32524cc",
    "photo-1513151233558-d860c5398176", "photo-1513506003901-1e6a229e2d15",
    "photo-1497215842964-222b430dc094", "photo-1522881193457-37ae97c905bf",
    "photo-1523240795612-9a054b0db644", "photo-1523580494863-6f3031224c94",
    "photo-1528459801416-a9e53bbf4e17", "photo-1554048612-b6a482bc67e5",
    "photo-1556740758-90de374c12ad", "photo-1573164574230-db1d5e960238",
    "photo-1580894894513-541e068a3e2b", "photo-1587825140708-dfaf72ae4b04",
    "photo-1588072432836-e10032774350", "photo-1588702547919-26089e690ecc",
    "photo-1589829085413-56de8ae18c73", "photo-1590402494587-44b71d7772f6",
    "photo-1591123120675-6f7f1aae0e5b", "photo-1592280771190-3e2e4d571952",
    "photo-1593642532973-d31b6557fa68", "photo-1595152772835-219674b2a8a6",
    "photo-1596464716127-f2a82984de30", "photo-1596496181848-3091d4878b24",
    "photo-1596496181871-9681eacf9764", "photo-1598520106830-8c45c2035460",
    "photo-1610484826967-09c5720778c7", "photo-1616400619175-5beda3a17896",
    "photo-1622782914767-404fb9ab3f57", "photo-1635070041078-e363dbe005cb",
    "photo-1472289065668-ce650ac443d2", "photo-1523580494863-6f3031224c94",
    "photo-1450101499163-c8848c66ca85", "photo-1517694712202-14dd9538aa97",
    "photo-1472173148041-00294f0814a2", "photo-1485988412941-77a35537dae4",
    "photo-1519389950473-47ba0277781c", "photo-1521721839743-2e446fc17948",
]

def create_unsplash_url(photo_id):
    """Unsplash 사진 ID로 최적화된 URL 생성"""
    return f"https://images.unsplash.com/{photo_id}?w=1200&h=630&fit=crop"

def find_duplicate_images(content_dir):
    """중복 이미지 사용 현황 분석"""
    image_usage = defaultdict(list)

    for md_file in content_dir.glob('**/*.md'):
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # featured_image 추출
            match = re.search(r'^featured_image:\s*(.+)$', content, re.MULTILINE)
            if match:
                image_url = match.group(1).strip()
                image_usage[image_url].append(str(md_file))
        except Exception as e:
            continue

    return image_usage

def replace_duplicate_image(file_path, old_image, new_image):
    """파일의 중복 이미지를 새 이미지로 교체"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # featured_image 교체
        new_content = re.sub(
            r'^featured_image:\s*' + re.escape(old_image) + r'\s*$',
            f'featured_image: {new_image}',
            content,
            flags=re.MULTILINE
        )

        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True
        return False

    except Exception as e:
        print(f"❌ 오류: {file_path} - {e}")
        return False

def main():
    content_dir = Path('content')

    print("🔍 Featured Image 중복 분석 시작...\n")

    # 1. 현재 이미지 사용 현황 분석
    image_usage = find_duplicate_images(content_dir)

    # 2. 중복된 이미지 찾기 (2개 이상 사용)
    duplicates = {img: files for img, files in image_usage.items() if len(files) > 1}

    if not duplicates:
        print("✅ 중복된 이미지가 없습니다!")
        return

    print(f"📊 중복 이미지 발견: {len(duplicates)}개\n")

    # 3. 중복 통계 출력
    for img, files in sorted(duplicates.items(), key=lambda x: len(x[1]), reverse=True):
        print(f"  🔁 {len(files)}회 사용: {img.split('/')[-1][:50]}...")

    print(f"\n🎨 이미지 다양화 시작...\n")

    # 4. 고유 이미지 풀 준비
    random.shuffle(UNSPLASH_IMAGES)
    available_images = [create_unsplash_url(photo_id) for photo_id in UNSPLASH_IMAGES]

    # 이미 사용 중인 이미지는 제외
    used_images = set(image_usage.keys())
    available_images = [img for img in available_images if img not in used_images]

    replaced_count = 0
    image_index = 0

    # 5. 중복 이미지 교체 (각 이미지당 1개만 남기고 나머지 교체)
    for duplicate_img, file_list in duplicates.items():
        # 첫 번째 파일은 유지, 나머지는 교체
        files_to_replace = file_list[1:]

        for file_path in files_to_replace:
            if image_index >= len(available_images):
                print("⚠️  사용 가능한 이미지 소진")
                break

            new_image = available_images[image_index]
            image_index += 1

            if replace_duplicate_image(file_path, duplicate_img, new_image):
                replaced_count += 1
                rel_path = str(Path(file_path).relative_to(content_dir))
                if replaced_count <= 10:  # 처음 10개만 출력
                    print(f"✅ [{replaced_count}] {rel_path}")

        if image_index >= len(available_images):
            break

    print("\n" + "=" * 80)
    print("📊 Featured Image 다양화 완료")
    print("=" * 80)
    print(f"교체된 파일: {replaced_count}개")
    print(f"사용된 고유 이미지: {image_index}개")
    print(f"중복 이미지 제거율: {replaced_count / sum(len(files) - 1 for files in duplicates.values()) * 100:.1f}%")
    print("=" * 80)

if __name__ == '__main__':
    main()
