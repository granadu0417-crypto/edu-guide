#!/bin/bash
# 콘텐츠 줄 수 분포 체크 스크립트
# 사용법: ./scripts/check-line-distribution.sh [폴더경로]

CONTENT_PATH="${1:-/home/user/edu-guide/content}"

echo "========================================"
echo "📊 콘텐츠 줄 수 분포 분석"
echo "경로: $CONTENT_PATH"
echo "========================================"
echo ""

# 전체 파일 수
TOTAL=$(find "$CONTENT_PATH" -name "*.md" -type f | wc -l)
echo "📁 전체 파일 수: $TOTAL개"
echo ""

# 목표 분포
echo "🎯 목표 분포 vs 현재 분포"
echo "----------------------------------------"

find "$CONTENT_PATH" -name "*.md" -type f -exec wc -l {} \; 2>/dev/null | awk -v total="$TOTAL" '
{
  lines = $1
  if (lines >= 100 && lines <= 130) a++
  else if (lines >= 131 && lines <= 160) b++
  else if (lines >= 161 && lines <= 200) c++
  else if (lines >= 201 && lines <= 250) d++
  else if (lines >= 251 && lines <= 300) e++
  else other++
}
END {
  printf "100-130줄: %4d개 (%5.1f%%) | 목표: 25%% | ", a, a/total*100
  diff = a/total*100 - 25
  if (diff > 5) printf "⚠️ 초과 (+%.1f%%)\n", diff
  else if (diff < -5) printf "⚠️ 부족 (%.1f%%)\n", diff
  else printf "✅ 적정\n"

  printf "131-160줄: %4d개 (%5.1f%%) | 목표: 30%% | ", b, b/total*100
  diff = b/total*100 - 30
  if (diff > 5) printf "⚠️ 초과 (+%.1f%%)\n", diff
  else if (diff < -5) printf "⚠️ 부족 (%.1f%%)\n", diff
  else printf "✅ 적정\n"

  printf "161-200줄: %4d개 (%5.1f%%) | 목표: 25%% | ", c, c/total*100
  diff = c/total*100 - 25
  if (diff > 5) printf "⚠️ 초과 (+%.1f%%)\n", diff
  else if (diff < -5) printf "⚠️ 부족 (%.1f%%)\n", diff
  else printf "✅ 적정\n"

  printf "201-250줄: %4d개 (%5.1f%%) | 목표: 15%% | ", d, d/total*100
  diff = d/total*100 - 15
  if (diff > 5) printf "⚠️ 초과 (+%.1f%%)\n", diff
  else if (diff < -5) printf "⚠️ 부족 (%.1f%%)\n", diff
  else printf "✅ 적정\n"

  printf "251-300줄: %4d개 (%5.1f%%) | 목표:  5%% | ", e, e/total*100
  diff = e/total*100 - 5
  if (diff > 5) printf "⚠️ 초과 (+%.1f%%)\n", diff
  else if (diff < -5) printf "⚠️ 부족 (%.1f%%)\n", diff
  else printf "✅ 적정\n"

  if (other > 0) printf "\n기타(100줄 미만 또는 300줄 초과): %d개\n", other
}'

echo ""
echo "========================================"
echo "⚠️ 동일 줄 수 집중 현황 (50개 이상)"
echo "========================================"

find "$CONTENT_PATH" -name "*.md" -type f -exec wc -l {} \; 2>/dev/null | \
  awk '{print $1}' | sort -n | uniq -c | sort -rn | \
  awk '$1 >= 50 {printf "%d개 파일이 %d줄에 집중 ← 분산 필요\n", $1, $2}'

echo ""
echo "========================================"
echo "📈 권장 조치"
echo "========================================"

find "$CONTENT_PATH" -name "*.md" -type f -exec wc -l {} \; 2>/dev/null | awk -v total="$TOTAL" '
{
  lines = $1
  if (lines >= 100 && lines <= 130) a++
  else if (lines >= 131 && lines <= 160) b++
  else if (lines >= 161 && lines <= 200) c++
  else if (lines >= 201 && lines <= 250) d++
  else if (lines >= 251 && lines <= 300) e++
}
END {
  need_short = int(total * 0.25) - a
  need_standard = int(total * 0.30) - b
  need_detail = int(total * 0.25) - c
  need_deep = int(total * 0.15) - d
  need_comprehensive = int(total * 0.05) - e

  if (need_short > 0) printf "• 100-130줄 파일 %d개 추가 필요\n", need_short
  if (need_standard > 0) printf "• 131-160줄 파일 %d개 추가 필요\n", need_standard
  if (need_detail > 0) printf "• 161-200줄 파일 %d개 추가 필요\n", need_detail
  if (need_deep > 0) printf "• 201-250줄 파일 %d개 추가 필요\n", need_deep
  if (need_comprehensive > 0) printf "• 251-300줄 파일 %d개 추가 필요\n", need_comprehensive

  if (need_short <= 0 && need_standard <= 0 && need_detail <= 0 && need_deep <= 0 && need_comprehensive <= 0) {
    print "✅ 모든 구간이 목표 비율을 충족합니다!"
  }
}'

echo ""
