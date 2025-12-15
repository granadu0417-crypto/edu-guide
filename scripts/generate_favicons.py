#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
로고 기반 파비콘 생성 스크립트
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_simple_favicon(size, output_path):
    """간단한 파비콘 생성 (로고 색상 기반)"""
    # 브랜드 컬러
    bg_color = (102, 126, 234)  # #667eea
    icon_color = (255, 217, 61)  # #ffd93d (북마크 색상)

    # 이미지 생성
    img = Image.new('RGBA', (size, size), bg_color + (255,))
    draw = ImageDraw.Draw(img)

    # 중앙에 북마크 아이콘 그리기
    margin = size // 6

    # 책 본체 (흰색 사각형)
    book_left = margin
    book_top = margin
    book_right = size - margin
    book_bottom = size - margin
    draw.rounded_rectangle(
        [book_left, book_top, book_right, book_bottom],
        radius=size // 20,
        fill=(255, 255, 255, 240)
    )

    # 책 선들
    line_y1 = book_top + (book_bottom - book_top) // 4
    line_y2 = book_top + (book_bottom - book_top) // 2
    line_y3 = book_top + 3 * (book_bottom - book_top) // 4

    line_margin = margin + size // 15
    line_width = max(2, size // 40)

    draw.line([line_margin, line_y1, book_right - line_margin, line_y1],
              fill=bg_color, width=line_width)
    draw.line([line_margin, line_y2, book_right - line_margin, line_y2],
              fill=bg_color, width=line_width)
    draw.line([line_margin, line_y3, book_right - line_margin - size // 10, line_y3],
              fill=bg_color, width=line_width)

    # 북마크
    bookmark_width = size // 8
    bookmark_left = book_right - margin - bookmark_width
    bookmark_top = book_top - size // 8
    bookmark_bottom = book_top + size // 4

    draw.rectangle(
        [bookmark_left, bookmark_top, bookmark_left + bookmark_width, bookmark_bottom],
        fill=icon_color
    )

    # 북마크 삼각형 끝
    triangle_points = [
        (bookmark_left, bookmark_bottom),
        (bookmark_left + bookmark_width, bookmark_bottom),
        (bookmark_left + bookmark_width // 2, bookmark_bottom + bookmark_width // 2)
    ]
    draw.polygon(triangle_points, fill=icon_color)

    # 저장
    img.save(output_path, 'PNG')
    print(f"✅ Created: {output_path} ({size}x{size})")

def create_ico_file(png_files, output_path):
    """여러 PNG를 하나의 ICO 파일로 변환"""
    images = []
    for png_file in png_files:
        img = Image.open(png_file)
        images.append(img)

    # 첫 번째 이미지를 기준으로 ICO 저장
    images[0].save(output_path, format='ICO', sizes=[(img.size[0], img.size[1]) for img in images])
    print(f"✅ Created: {output_path} (multi-size ICO)")

def main():
    # 출력 디렉토리
    output_dir = 'static/images'
    os.makedirs(output_dir, exist_ok=True)

    print("🎨 파비콘 생성 시작...\n")

    # 각 크기별 PNG 생성
    sizes = [16, 32, 180, 192, 512]
    png_files = []

    for size in sizes:
        if size == 180:
            output_path = f'{output_dir}/apple-touch-icon.png'
        elif size == 16:
            output_path = f'{output_dir}/favicon-16x16.png'
        elif size == 32:
            output_path = f'{output_dir}/favicon-32x32.png'
        else:
            output_path = f'{output_dir}/icon-{size}.png'

        create_simple_favicon(size, output_path)

        # ICO 파일용으로 16, 32만 저장
        if size in [16, 32]:
            png_files.append(output_path)

    # ICO 파일 생성
    create_ico_file(png_files, f'{output_dir}/favicon.ico')

    print("\n" + "=" * 80)
    print("📊 파비콘 생성 완료")
    print("=" * 80)
    print("생성된 파일:")
    print("  - favicon.ico (16x16, 32x32)")
    print("  - favicon-16x16.png")
    print("  - favicon-32x32.png")
    print("  - apple-touch-icon.png (180x180)")
    print("  - icon-192.png (192x192, PWA)")
    print("  - icon-512.png (512x512, PWA)")
    print("=" * 80)

if __name__ == '__main__':
    main()
