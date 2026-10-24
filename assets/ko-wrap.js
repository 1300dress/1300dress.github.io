// 타이틀 안의 한글을 .ko 스팬으로 감쌉니다. 영문·숫자는 Junicode, 한글은 본명조로 나뉘게 하려는 것.
// 세로 비율 때문에 .ko는 inline-block이라 줄바꿈이 안 되므로, 어절(띄어쓰기 단위)마다 따로 감쌉니다.
(function () {
  const K = "ᄀ-ᇿ㄰-㆏가-힣〈-】×·";
  const KO = new RegExp(`([${K}]+)`);

  function wrapText(node) {
    const parts = node.nodeValue.split(KO);
    if (parts.length < 2) return;
    const frag = document.createDocumentFragment();
    parts.forEach(p => {
      if (!p) return;
      if (KO.test(p)) {
        const s = document.createElement("span");
        s.className = "ko";
        s.textContent = p;
        frag.appendChild(s);
      } else {
        frag.appendChild(document.createTextNode(p));
      }
    });
    node.parentNode.replaceChild(frag, node);
  }

  function koWrap(root) {
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
      acceptNode: n => n.parentElement.closest(".ko") ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT,
    });
    const nodes = [];
    while (walker.nextNode()) nodes.push(walker.currentNode);
    nodes.forEach(wrapText);
  }

  window.koWrap = koWrap;
  document.querySelectorAll(".title, h1, h2").forEach(koWrap);
})();
