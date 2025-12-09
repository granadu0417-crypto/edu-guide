#!/bin/bash
echo "# 서초구 동별 제목 목록 (실제 작성된 파일 기준)" > seocho_titles_summary.md
echo "" >> seocho_titles_summary.md

dongs="seochodong jamwondong banpobondong banpo2dong banpo4dong bangbaebondong bangbae2dong bangbae4dong yangjae1dong yangjae2dong naegokdong"

for dong in $dongs; do
  echo "## ${dong}" >> seocho_titles_summary.md
  echo "" >> seocho_titles_summary.md
  
  echo "### 중등 영어" >> seocho_titles_summary.md
  git show origin/claude/review-and-prepare-01NKzrsVbfVATo3AKkey33vm:content/middle/seocho-${dong}-middle-english.md 2>/dev/null | grep "^title:" >> seocho_titles_summary.md
  echo "" >> seocho_titles_summary.md
  
  echo "### 중등 수학" >> seocho_titles_summary.md
  git show origin/claude/review-and-prepare-01NKzrsVbfVATo3AKkey33vm:content/middle/seocho-${dong}-middle-math.md 2>/dev/null | grep "^title:" >> seocho_titles_summary.md
  echo "" >> seocho_titles_summary.md
  
  echo "### 고등 영어" >> seocho_titles_summary.md
  git show origin/claude/review-and-prepare-01NKzrsVbfVATo3AKkey33vm:content/high/seocho-${dong}-high-english.md 2>/dev/null | grep "^title:" >> seocho_titles_summary.md
  echo "" >> seocho_titles_summary.md
  
  echo "### 고등 수학" >> seocho_titles_summary.md
  git show origin/claude/review-and-prepare-01NKzrsVbfVATo3AKkey33vm:content/high/seocho-${dong}-high-math.md 2>/dev/null | grep "^title:" >> seocho_titles_summary.md
  echo "" >> seocho_titles_summary.md
  echo "---" >> seocho_titles_summary.md
  echo "" >> seocho_titles_summary.md
done
