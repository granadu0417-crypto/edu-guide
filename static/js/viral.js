// 사용자 카운터 초기화 및 애니메이션
function initUsageCounter() {
    const storageKey = 'eduguide_usage_count';
    const baseCount = 245780;
    let currentCount = parseInt(localStorage.getItem(storageKey)) || baseCount;

    currentCount++;
    localStorage.setItem(storageKey, currentCount);

    const countElement = document.getElementById('usageCount');
    if (!countElement) return;

    let displayCount = currentCount - 100;
    const increment = Math.ceil(100 / 30);

    const timer = setInterval(() => {
        displayCount += increment;
        if (displayCount >= currentCount) {
            displayCount = currentCount;
            clearInterval(timer);
        }
        countElement.textContent = displayCount.toLocaleString();
    }, 30);
}

// 페이스북 공유
function shareFacebook() {
    const url = encodeURIComponent(window.location.href);
    const shareUrl = `https://www.facebook.com/sharer/sharer.php?u=${url}`;
    window.open(shareUrl, '_blank', 'width=600,height=400');
}

// 트위터 공유
function shareTwitter() {
    const url = encodeURIComponent(window.location.href);
    const text = encodeURIComponent(document.title);
    const shareUrl = `https://twitter.com/intent/tweet?url=${url}&text=${text}`;
    window.open(shareUrl, '_blank', 'width=600,height=400');
}

// 링크 복사
function copyLink() {
    const url = window.location.href;
    const btn = document.getElementById('copyBtn');
    if (!btn) return;

    if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(url).then(() => {
            const originalHTML = btn.innerHTML;
            btn.innerHTML = '<span>✅</span> 복사 완료!';
            btn.style.background = '#10b981';
            btn.style.color = 'white';

            setTimeout(() => {
                btn.innerHTML = originalHTML;
                btn.style.background = 'white';
                btn.style.color = '#667eea';
            }, 2000);
        }).catch(err => {
            alert('링크 복사에 실패했습니다.');
        });
    } else {
        const textarea = document.createElement('textarea');
        textarea.value = url;
        textarea.style.position = 'fixed';
        textarea.style.opacity = '0';
        document.body.appendChild(textarea);
        textarea.select();

        try {
            document.execCommand('copy');
            const originalHTML = btn.innerHTML;
            btn.innerHTML = '<span>✅</span> 복사 완료!';
            btn.style.background = '#10b981';
            btn.style.color = 'white';

            setTimeout(() => {
                btn.innerHTML = originalHTML;
                btn.style.background = 'white';
                btn.style.color = '#667eea';
            }, 2000);
        } catch (err) {
            alert('링크 복사에 실패했습니다.');
        }

        document.body.removeChild(textarea);
    }
}

// 북마크 팝업 표시
function showBookmarkPopup() {
    const visitKey = 'eduguide_visit_count';
    const popupDismissedKey = 'eduguide_bookmark_dismissed';

    if (localStorage.getItem(popupDismissedKey)) {
        return;
    }

    let visitCount = parseInt(localStorage.getItem(visitKey)) || 0;
    visitCount++;
    localStorage.setItem(visitKey, visitCount);

    if (visitCount === 3) {
        const popup = document.getElementById('bookmarkPopup');
        if (popup) {
            popup.style.display = 'block';
        }
    }
}

function closeBookmarkPopup(addBookmark) {
    const popup = document.getElementById('bookmarkPopup');
    if (popup) {
        popup.style.display = 'none';
    }
    localStorage.setItem('eduguide_bookmark_dismissed', 'true');

    if (addBookmark) {
        alert('Ctrl+D (Windows) 또는 Cmd+D (Mac)를 눌러 북마크에 추가하세요!');
    }
}

// 서비스 워커 등록
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/sw.js')
        .then(registration => console.log('SW registered'))
        .catch(err => console.log('SW registration failed'));
}

// 페이지 로드 시 초기화
window.addEventListener('load', () => {
    initUsageCounter();
    showBookmarkPopup();
});
