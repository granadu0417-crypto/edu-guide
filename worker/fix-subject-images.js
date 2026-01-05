// 과학/논술/코딩 이미지 수정 스크립트
// 플레이스홀더 이미지를 실제 Unsplash 이미지로 교체

const fs = require('fs');
const path = require('path');

const GANGNAM_DIR = '/mnt/c/Users/user/Desktop/과외를부탁해/edu-guide-fresh/content/seoul/gangnam';

// 과목별 실제 Unsplash 이미지 ID 풀
const IMAGE_POOLS = {
  science: [
    'edu_0201_1596495578065-6e0763fa1178.jpg',
    'edu_0202_1635070041078-e363dbe005cb.jpg',
    'edu_0203_1509228468518-180dd4864904.jpg',
    'edu_0204_1635070041409-e63e783ce3b1.jpg',
    'edu_0205_1518133910546-b6c2fb7d79e3.jpg',
    'edu_0206_1453733190371-0a9bedd82893.jpg',
    'edu_0207_1596495577886-d920f1fb7238.jpg',
    'edu_0208_1611532736597-de2d4265fba3.jpg',
    'edu_0209_1580894894513-541e068a3e2b.jpg',
    'edu_0210_1613909207039-6b173b755cc1.jpg',
    'edu_0211_1559494007-9f5847c49d94.jpg',
    'edu_0212_1544383835-bda2bc66a55d.jpg',
    'edu_0213_1518435579668-52e6c59a9c85.jpg',
    'edu_0214_1611329857570-f02f340e7378.jpg',
    'edu_0215_1512314889357-e157c22f938d.jpg',
    'edu_0216_1516796181074-bf453fbfa3e6.jpg',
    'edu_0217_1515879218367-8466d910aaa4.jpg',
    'edu_0218_1554475901-4538ddfbccc2.jpg',
    'edu_0219_1581078426770-6d336e5de7bf.jpg',
    'edu_0220_1611348586804-61bf6c080437.jpg',
    'edu_0221_1611348524140-53c9a25263d6.jpg',
    'edu_0222_1611351888222-c5797b8b5c2f.jpg',
    'edu_0223_1596495577933-6c64e3a7d20a.jpg',
    'edu_0224_1580894732444-8ecded7900cd.jpg'
  ],
  essay: [
    'edu_0301_1457369804613-52c61a468e7d.jpg',
    'edu_0302_1456513080510-7bf3a84b82f8.jpg',
    'edu_0303_1546410531-bb4caa6b424d.jpg',
    'edu_0304_1553877522-43269d4ea984.jpg',
    'edu_0305_1515378791036-0648a3ef77b2.jpg',
    'edu_0306_1519389950473-47ba0277781c.jpg',
    'edu_0307_1523240795612-9a054b0db644.jpg',
    'edu_0308_1488190211105-8b0e65b80b4e.jpg',
    'edu_0309_1434030216411-0b793f4b4173.jpg',
    'edu_0310_1455390582262-044cdead277a.jpg',
    'edu_0311_1471107340929-a87cd0f5b5f3.jpg',
    'edu_0312_1415369629372-26f2fe60c467.jpg',
    'edu_0313_1447069387593-a5de0862481e.jpg',
    'edu_0314_1476234251651-f353703a034d.jpg',
    'edu_0315_1516321497487-e288fb19713f.jpg',
    'edu_0316_1521587760476-6c12a4b040da.jpg',
    'edu_0317_1507842217343-583bb7270b66.jpg',
    'edu_0318_1497633762265-9d179a990aa6.jpg',
    'edu_0319_1516979187457-637abb4f9353.jpg',
    'edu_0320_1512820790803-83ca734da794.jpg',
    'edu_0321_1550399105-c4db5fb85c18.jpg',
    'edu_0322_1491841573634-28140fc7ced7.jpg'
  ],
  coding: [
    'edu_0401_1531482615713-2afd69097998.jpg',
    'edu_0402_1515187029135-18ee286d815b.jpg',
    'edu_0403_1573497019940-1c28c88b4f3e.jpg',
    'edu_0404_1573496359142-b8d87734a5a2.jpg',
    'edu_0405_1573497019236-17f8177b81e8.jpg',
    'edu_0406_1573497161161-c3e73707e25c.jpg',
    'edu_0407_1600195077077-7c815f540a3d.jpg',
    'edu_0408_1604134967494-8a9ed3adea0d.jpg',
    'edu_0409_1611162617474-5b21e879e113.jpg',
    'edu_0410_1611162616475-46b635cb6868.jpg',
    'edu_0411_1611162618071-b39a2ec055fb.jpg',
    'edu_0412_1611162617213-7d7a39e9b1d7.jpg',
    'edu_0413_1594608661623-aa0bd3a69d98.jpg',
    'edu_0414_1599687351724-dfa3c4ff81b5.jpg',
    'edu_0415_1609234656388-0ff363383899.jpg',
    'edu_0416_1609234656432-46d0b41c3dad.jpg',
    'edu_0417_1610484826967-09c5720778c7.jpg',
    'edu_0418_1622556498246-755f44ca76f3.jpg',
    'edu_0419_1603354350317-6f7aaa5911c5.jpg',
    'edu_0420_1603354350266-f2b10492ea3e.jpg',
    'edu_0421_1607990281513-2c110a25bd8c.jpg',
    'edu_0422_1587691592099-24045742c181.jpg',
    'edu_0423_1588072432836-e10032774350.jpg',
    'edu_0424_1588702547919-26089e690ecc.jpg'
  ]
};

function fixImages() {
  const files = fs.readdirSync(GANGNAM_DIR).filter(f => f.endsWith('.md'));

  let scienceIdx = 0;
  let essayIdx = 0;
  let codingIdx = 0;
  let fixedCount = 0;

  for (const file of files) {
    const filePath = path.join(GANGNAM_DIR, file);
    let content = fs.readFileSync(filePath, 'utf-8');
    let modified = false;

    // 과학 이미지 수정
    if (file.includes('-science')) {
      const oldPattern = /featured_image: "\/images\/edu_\d+_science(_m)?\.jpg"/;
      if (oldPattern.test(content)) {
        const newImage = IMAGE_POOLS.science[scienceIdx % IMAGE_POOLS.science.length];
        content = content.replace(oldPattern, `featured_image: "/images/${newImage}"`);
        scienceIdx++;
        modified = true;
      }
    }

    // 논술 이미지 수정
    if (file.includes('-essay')) {
      const oldPattern = /featured_image: "\/images\/edu_\d+_essay\.jpg"/;
      if (oldPattern.test(content)) {
        const newImage = IMAGE_POOLS.essay[essayIdx % IMAGE_POOLS.essay.length];
        content = content.replace(oldPattern, `featured_image: "/images/${newImage}"`);
        essayIdx++;
        modified = true;
      }
    }

    // 코딩 이미지 수정
    if (file.includes('-coding')) {
      const oldPattern = /featured_image: "\/images\/edu_\d+_coding(_m)?\.jpg"/;
      if (oldPattern.test(content)) {
        const newImage = IMAGE_POOLS.coding[codingIdx % IMAGE_POOLS.coding.length];
        content = content.replace(oldPattern, `featured_image: "/images/${newImage}"`);
        codingIdx++;
        modified = true;
      }
    }

    if (modified) {
      fs.writeFileSync(filePath, content, 'utf-8');
      fixedCount++;
      console.log(`Fixed: ${file}`);
    }
  }

  console.log(`\n총 ${fixedCount}개 파일 수정 완료`);
  console.log(`  과학: ${scienceIdx}개`);
  console.log(`  논술: ${essayIdx}개`);
  console.log(`  코딩: ${codingIdx}개`);
}

fixImages();
