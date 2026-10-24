// 유리다관 한 장면: 열리면 첫 문장이 우러나고, '한 잔 우리기'를 누를 때마다 비웠다가 다른 문장을 우립니다.
// 한 번 나온 문장은 목록을 다 돌기 전까지 다시 나오지 않습니다.
(function () {
  const button = document.querySelector("[data-draw]");
  const cup = document.querySelector(".vessel");
  if (!button || !cup) return;

  const lineEl = cup.querySelector(".line");
  const sourceEl = cup.querySelector(".source");
  let pool = [];

  // 첫 장면: 페이지가 열리면 바로 우러남
  requestAnimationFrame(() => setTimeout(() => cup.classList.add("steeped"), 200));

  if (!window.LINES || !window.LINES.length) { button.hidden = true; return; }

  function next() {
    if (!pool.length) pool = window.LINES.slice().sort(() => Math.random() - 0.5);
    return pool.pop();
  }

  button.addEventListener("click", () => {
    const pick = next();
    cup.classList.remove("steeped");
    // 다관을 비우는 시간을 두고 다시 우림
    setTimeout(() => {
      lineEl.textContent = pick.text;
      if (window.koWrap) window.koWrap(lineEl);
      sourceEl.innerHTML = "";
      const label = document.createTextNode("— " + pick.source);
      if (pick.href) {
        const a = document.createElement("a");
        a.href = pick.href;
        a.appendChild(label);
        sourceEl.appendChild(a);
      } else {
        sourceEl.appendChild(label);
      }
      cup.classList.add("steeped");
    }, 700);
  });
})();
