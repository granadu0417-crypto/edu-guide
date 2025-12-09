#!/usr/bin/env python3
"""
Fix Hub pages - extract Korean dong names and reorganize middle school sections
"""

import os
import glob
import re

DISTRICT_MAPPING = {
    'guro': '구로구',
    'geumcheon': '금천구',
    'dobong': '도봉구',
    'gangbuk': '강북구',
    'nowon': '노원구',
    'dongdaemun': '동대문구',
    'jungnang': '중랑구',
    'seongbuk': '성북구',
    'gangseo': '강서구',
    'gwanak': '관악구',
    'yangcheon': '양천구',
    'yeongdeungpo': '영등포구',
    'dongjak': '동작구',
    'mapo': '마포구',
    'seodaemun': '서대문구',
    'eunpyeong': '은평구',
    'yongsan': '용산구',
    'jongno': '종로구',
    'junggu': '중구',
    'seongdong': '성동구'
}

def get_dong_info_from_file(filepath):
    """Extract Korean dong name and school names from file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('title:'):
                    title = line.replace('title:', '').strip().strip('"')
                    # Format: "종로구 부암동 중등 수학과외 - 경신중·동성중·중앙중 맞춤 관리"
                    parts = title.split()
                    if len(parts) >= 3:
                        dong_korean = parts[1]  # e.g., "부암동"
                        if '-' in title:
                            schools = title.split('-')[1].strip().split('맞춤')[0].strip()
                        else:
                            schools = ""
                        return dong_korean, schools
    except:
        pass
    return None, None

def get_middle_files_with_info(district_code):
    """Get all middle school files with Korean names"""
    pattern = f"/home/user/edu-guide/content/middle/{district_code}-*-middle-math.md"
    files = glob.glob(pattern)

    dong_info = []
    for filepath in sorted(files):
        dong_korean, schools = get_dong_info_from_file(filepath)
        if dong_korean:
            # Extract English code for URL
            basename = os.path.basename(filepath)
            dong_code = basename.replace(f'{district_code}-', '').replace('-middle-math.md', '')
            dong_info.append((dong_code, dong_korean, schools))

    return dong_info

def group_dongs(dong_info):
    """Group dongs by area for cleaner presentation"""
    # Simple grouping - could be improved
    groups = {}
    for dong_code, dong_korean, schools in dong_info:
        # Group by base name (remove numbers)
        base = re.sub(r'[0-9]+동$', '동', dong_korean)
        if base not in groups:
            groups[base] = []
        groups[base].append((dong_code, dong_korean, schools))

    return groups

def generate_middle_section(district_code, dong_info):
    """Generate properly formatted middle school section"""
    if not dong_info:
        return ""

    groups = group_dongs(dong_info)

    section = "---\n\n## 중학생 과외 안내\n\n"

    # Get unique schools across all dongs
    all_schools = set()
    for _, _, schools in dong_info:
        if schools:
            all_schools.update(schools.split('·'))

    # Create sections
    for base_dong, dongs in list(groups.items())[:5]:  # Limit to 5 major groups
        # Group header
        if len(dongs) == 1:
            header = dongs[0][1]  # Single dong
        elif len(dongs) <= 3:
            header = '·'.join([d[1] for d in dongs])
        else:
            header = f"{dongs[0][1]} 외 {len(dongs)-1}개 동"

        section += f"### {header}\n\n"

        # School info from first dong
        schools = dongs[0][2] if dongs[0][2] else "중학교"
        section += f"**{schools}** 학생들이 거주합니다.\n\n"

        # Math section
        section += "**수학과외**\n"
        for dong_code, dong_korean, _ in dongs[:6]:  # Limit to 6 dongs per group
            section += f"- [{dong_korean} 중등 수학과외](/middle/{district_code}-{dong_code}-middle-math/)\n"

        section += "\n**영어과외**\n"
        for dong_code, dong_korean, _ in dongs[:6]:
            section += f"- [{dong_korean} 중등 영어과외](/middle/{district_code}-{dong_code}-middle-english/)\n"

        section += "\n"

    return section

def fix_hub_page(district_code, district_korean):
    """Fix a single hub page"""
    print(f"Fixing {district_korean}...")

    filepath = f"/home/user/edu-guide/content/cities/{district_korean}/_index.md"

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        print(f"  ✗ Could not read file")
        return False

    # Get dong info
    dong_info = get_middle_files_with_info(district_code)
    if not dong_info:
        print(f"  ✗ No middle school files found")
        return False

    # Generate new middle school section
    new_middle_section = generate_middle_section(district_code, dong_info)

    # Remove old middle school section
    content = re.sub(
        r'\n## 중학생 과외 안내.*?(?=\n## |\n---\n\n## |$)',
        '',
        content,
        flags=re.DOTALL
    )

    # Insert new middle section before school info or cost section
    insert_pos = re.search(r'\n## .*주요.*학교|## .*과외 비용', content)
    if insert_pos:
        pos = insert_pos.start()
        content = content[:pos] + '\n' + new_middle_section + content[pos:]

    # Ensure middle school costs are in cost section
    if '### 중학생' not in content:
        cost_section_match = re.search(
            r'(### 영어과외\n\n\*\*고1~2.*?\n\n\*\*고3.*?\n)',
            content,
            re.DOTALL
        )
        if cost_section_match:
            pos = cost_section_match.end()
            middle_costs = """
### 중학생

**수학**: 주1회 20만~28만원, 주2회 35만~48만원

**영어**: 주1회 18만~25만원, 주2회 32만~45만원

"""
            content = content[:pos] + middle_costs + content[pos:]

    # Add middle school info to school section if not present
    if '### 중학교' not in content and '## .*주요.*학교' in content:
        school_section_match = re.search(
            r'(## .*주요.*학교 안내.*?)(^<div)',
            content,
            re.MULTILINE | re.DOTALL
        )
        if school_section_match:
            pos = school_section_match.start(2)
            middle_school_info = """
### 중학교

지역 중학교들의 내신 특성을 파악한 맞춤 과외를 제공합니다.

"""
            content = content[:pos] + middle_school_info + content[pos:]

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"  ✓ Fixed {district_korean}")
    return True

def main():
    fixed_count = 0
    for district_code, district_korean in DISTRICT_MAPPING.items():
        if fix_hub_page(district_code, district_korean):
            fixed_count += 1

    print(f"\n{'='*50}")
    print(f"Fixed {fixed_count}/{len(DISTRICT_MAPPING)} Hub pages")
    print(f"{'='*50}")

if __name__ == '__main__':
    main()
