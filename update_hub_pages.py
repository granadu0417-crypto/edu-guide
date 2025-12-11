#!/usr/bin/env python3
"""
Script to add middle school sections to district Hub pages
"""

import os
import glob
import re

# District name mappings
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

def get_middle_school_files(district_code):
    """Get list of middle school files for a district"""
    pattern = f"/home/user/edu-guide/content/middle/{district_code}-*-middle-math.md"
    files = glob.glob(pattern)
    return sorted(files)

def extract_dong_from_filename(filename):
    """Extract dong name from filename"""
    # filename format: /path/district-dong-middle-math.md
    basename = os.path.basename(filename)
    parts = basename.replace('-middle-math.md', '').split('-', 1)
    if len(parts) > 1:
        return parts[1]
    return None

def get_title_info(filepath):
    """Extract title from markdown file to get school names"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('title:'):
                    return line.replace('title:', '').strip().strip('"')
    except:
        pass
    return None

def read_hub_page(district_korean):
    """Read existing hub page"""
    filepath = f"/home/user/edu-guide/content/cities/{district_korean}/_index.md"
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return None

def has_middle_school_section(content):
    """Check if hub page already has middle school section"""
    return '## 중학생 과외 안내' in content

def update_description(content, district_korean):
    """Update description to include middle school info"""
    # Find description line
    desc_pattern = r'(description: "[^"]*고등학생[^"]*")'

    def replace_desc(match):
        desc = match.group(0)
        # Replace "고등학생" with "중·고등학생"
        new_desc = desc.replace('고등학생', '중·고등학생')
        # Add middle school names if not present
        if '중' not in new_desc.split('중·고등학생')[1][:50]:
            # Insert middle school info before "등 관내"
            new_desc = re.sub(r'(등\s+관내)', r', 중학교 등 관내', new_desc, count=1)
            new_desc = re.sub(r'(고등학교)(,\s+중학교\s+등\s+관내)', r'\1와 중학교\2', new_desc)
        return new_desc

    updated = re.sub(desc_pattern, replace_desc, content)
    return updated

def generate_middle_section(district_code, math_files):
    """Generate middle school section content"""
    sections = []

    # Group files by area
    dong_groups = {}
    for filepath in math_files:
        dong = extract_dong_from_filename(filepath)
        if dong:
            # Get school names from title
            title = get_title_info(filepath)
            if title and '-' in title:
                school_info = title.split('-')[1].strip().split('맞춤')[0].strip()
            else:
                school_info = "중학교"

            # Group similar dongs together
            base_dong = re.sub(r'\d+$', '', dong)
            if base_dong not in dong_groups:
                dong_groups[base_dong] = []
            dong_groups[base_dong].append((dong, school_info))

    # Generate sections
    section_content = "---\n\n## 중학생 과외 안내\n\n"

    for base_dong, dongs in sorted(dong_groups.items())[:3]:  # Limit to 3 major sections
        # Create area header
        dong_list = [d[0] for d in dongs]
        school_info = dongs[0][1] if dongs else "중학교"

        section_content += f"### {dong_list[0] if len(dong_list) == 1 else '·'.join(dong_list[:3])}\n\n"
        section_content += f"**{school_info}** 학생들이 거주합니다.\n\n"
        section_content += "**수학과외**\n"

        for dong, _ in dongs[:5]:  # Limit to 5 dongs per section
            section_content += f"- [{dong} 중등 수학과외](/middle/{district_code}-{dong}-middle-math/)\n"

        section_content += "\n**영어과외**\n"
        for dong, _ in dongs[:5]:
            section_content += f"- [{dong} 중등 영어과외](/middle/{district_code}-{dong}-middle-english/)\n"
        section_content += "\n"

    return section_content

def add_cost_section_if_needed(content):
    """Add middle school cost section if not present"""
    if '### 중학생' not in content:
        # Find the cost section and add middle school costs
        cost_pattern = r'(## 과외 비용 안내.*?### 영어과외.*?\n.*?\n)'

        def add_middle_costs(match):
            existing = match.group(0)
            middle_section = """
### 중학생

**수학**: 주1회 20만~28만원, 주2회 35만~48만원

**영어**: 주1회 18만~25만원, 주2회 32만~45만원

"""
            return existing + middle_section

        content = re.sub(cost_pattern, add_middle_costs, content, flags=re.DOTALL)

    return content

def add_middle_schools_to_school_section(content):
    """Add middle school subsection to school info section"""
    if '### 중학교' not in content:
        # Find the school section and add a middle school subsection
        school_pattern = r'(## .*주요.*학교 안내.*?)(^<div)'

        def add_middle_school_info(match):
            existing = match.group(1)
            div_tag = match.group(2)

            middle_info = """
### 중학교

지역 중학교들의 내신 특성을 파악한 맞춤 과외를 제공합니다.

"""
            return existing + middle_info + div_tag

        content = re.sub(school_pattern, add_middle_school_info, content, flags=re.MULTILINE | re.DOTALL)

    return content

def update_hub_page(district_code, district_korean):
    """Update a single hub page"""
    print(f"\nProcessing {district_korean} ({district_code})...")

    # Get middle school files
    math_files = get_middle_school_files(district_code)
    if not math_files:
        print(f"  No middle school files found for {district_code}")
        return False

    print(f"  Found {len(math_files)} middle school math files")

    # Read existing hub page
    content = read_hub_page(district_korean)
    if not content:
        print(f"  Hub page not found for {district_korean}")
        return False

    # Check if already has middle school section
    if has_middle_school_section(content):
        print(f"  Hub page already has middle school section")
        return False

    # Update description
    content = update_description(content, district_korean)

    # Add "중등과외" tag if not present
    if '중등과외' not in content:
        content = content.replace('  - 고등과외\n', '  - 고등과외\n  - 중등과외\n')

    # Generate middle school section
    middle_section = generate_middle_section(district_code, math_files)

    # Insert middle section before "## 주요 학교" or "## 과외 비용"
    insert_marker = re.search(r'\n## .*주요.*학교', content)
    if not insert_marker:
        insert_marker = re.search(r'\n## .*과외 비용', content)

    if insert_marker:
        pos = insert_marker.start()
        content = content[:pos] + '\n' + middle_section + content[pos:]

    # Add cost section
    content = add_cost_section_if_needed(content)

    # Add middle school info to school section
    content = add_middle_schools_to_school_section(content)

    # Update final message
    content = re.sub(
        r'에서 고등학생 과외를',
        r'에서 중·고등학생 과외를',
        content
    )

    # Write updated content
    filepath = f"/home/user/edu-guide/content/cities/{district_korean}/_index.md"
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"  ✓ Updated {district_korean} Hub page")
    return True

def main():
    """Main function"""
    print("Starting Hub page updates...")

    updated_count = 0
    for district_code, district_korean in DISTRICT_MAPPING.items():
        if update_hub_page(district_code, district_korean):
            updated_count += 1

    print(f"\n{'='*50}")
    print(f"Updated {updated_count} Hub pages")
    print(f"{'='*50}")

if __name__ == '__main__':
    main()
