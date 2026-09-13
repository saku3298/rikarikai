(() => {
  const firstFilePage = 2;
  const lastFilePage = 25;
  const totalPages = lastFilePage - firstFilePage + 1;
  let current = 1;

  const image = document.getElementById('singlePage');
  const counter = document.getElementById('pageCounter');
  const prevButton = document.getElementById('prevButton');
  const nextButton = document.getElementById('nextButton');
  const finishLink = document.getElementById('finishLink');

  const fileName = (storyPage) => {
    const filePage = storyPage + firstFilePage - 1;
    return `pages/page-${String(filePage).padStart(2, '0')}.jpg`;
  };

  const showPage = (page) => {
    current = Math.min(totalPages, Math.max(1, page));
    image.src = fileName(current);
    image.alt = `第1話 ${current}ページ目`;
    counter.textContent = `${current} / ${totalPages}`;
    prevButton.disabled = current === 1;
    nextButton.disabled = current === totalPages;
    document.title = `第1話 ${current}/${totalPages} | リカリカイ`;
  };

  const scrollPages = document.getElementById('scrollPages');
  for (let page = 1; page <= totalPages; page += 1) {
    const img = document.createElement('img');
    img.src = fileName(page);
    img.alt = `第1話 ${page}ページ目`;
    img.loading = page <= 2 ? 'eager' : 'lazy';
    img.decoding = 'async';
    scrollPages.appendChild(img);
  }

  prevButton.addEventListener('click', () => showPage(current - 1));
  nextButton.addEventListener('click', () => showPage(current + 1));
  document.getElementById('prevArea').addEventListener('click', () => showPage(current - 1));
  document.getElementById('nextArea').addEventListener('click', () => showPage(current + 1));

  document.addEventListener('keydown', (event) => {
    if (event.key === 'ArrowLeft') showPage(current - 1);
    if (event.key === 'ArrowRight' || event.key === ' ') {
      event.preventDefault();
      showPage(current + 1);
    }
    if (event.key === 'Home') showPage(1);
    if (event.key === 'End') showPage(totalPages);
  });

  document.getElementById('fullscreenButton').addEventListener('click', async () => {
    if (!document.fullscreenElement) await document.documentElement.requestFullscreen();
    else await document.exitFullscreen();
  });

  finishLink.addEventListener('click', () => sessionStorage.removeItem('rikarikai-page'));
  showPage(Number(sessionStorage.getItem('rikarikai-page')) || 1);
  window.addEventListener('beforeunload', () => sessionStorage.setItem('rikarikai-page', current));
})();
