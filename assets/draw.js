// 첫 장면: 열리면 첫 문장이 우러나고, Refill을 누르면
// 문장이 사라지고 찻잔이 비었다가, 다시 차오르기 시작하는 순간 다른 문장이 왼쪽에 함께 나타납니다.
// 한 번 나온 문장은 목록을 다 돌기 전까지 다시 나오지 않습니다.
(function () {
  const button = document.querySelector("[data-draw]");
  const cup = document.querySelector(".vessel");
  if (!button || !cup) return;

  const lineEl = cup.querySelector(".line");
  const sourceEl = cup.querySelector(".source");
  const frame = document.querySelector(".cup-frame");
  const REFILL_MS = 1600;   // style.css의 drain-refill 길이와 같게
  const TEXT_AT_MS = 640;   // 다시 차오르기 시작하는 순간(drain-refill의 40%)에 새 문장도 나타나기 시작
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  let pool = [];
  let busy = false;

  // 첫 장면: 페이지가 열리면 바로 우러남
  requestAnimationFrame(() => setTimeout(() => cup.classList.add("steeped"), 200));

  if (!window.LINES || !window.LINES.length) { button.hidden = true; return; }

  function next() {
    if (!pool.length) pool = window.LINES.slice().sort(() => Math.random() - 0.5);
    return pool.pop();
  }

  function show(pick) {
    // \n은 줄바꿈으로. 긴 문장은 글자를 한 단계 줄여 왼쪽 칸에 넉넉히 들어가게
    lineEl.textContent = "";
    pick.text.split("\n").forEach((part, i) => {
      if (i) lineEl.appendChild(document.createElement("br"));
      lineEl.appendChild(document.createTextNode(part));
    });
    const len = pick.text.replace(/\n/g, "").length;
    lineEl.classList.toggle("is-mid", len > 20 && len <= 34);
    lineEl.classList.toggle("is-long", len > 34);
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
  }

  button.addEventListener("click", () => {
    if (busy) return;
    busy = true;
    const pick = next();
    cup.classList.remove("steeped");

    // 찻잔을 비웠다가 다시 채우는 동안 기다린 뒤 새 문장
    if (frame && !reduceMotion) {
      // 찰랑이는 방향과 세기를 매번 무작위로
      const angle = Math.random() * Math.PI * 2;
      const amp = 9 + Math.random() * 5;   // 9~14%
      const liquid = frame.querySelector(".liquid");
      if (liquid) {
        liquid.style.setProperty("--sx", (Math.cos(angle) * amp).toFixed(2) + "%");
        liquid.style.setProperty("--sy", (Math.sin(angle) * amp).toFixed(2) + "%");
      }
      frame.classList.remove("refilling");
      void frame.offsetWidth;   // 같은 애니메이션을 다시 시작하려면 한 번 끊어 줌
      frame.classList.add("refilling");
    }
    if (reduceMotion) {
      setTimeout(() => { show(pick); busy = false; }, 300);
    } else {
      setTimeout(() => {
        cup.classList.add("refill-sync");   // 새 문장만 느리게: 찻물이 다 차는 순간 함께 다 보이도록
        show(pick);
      }, TEXT_AT_MS);
      setTimeout(() => {
        cup.classList.remove("refill-sync");
        busy = false;                     // 다 차오를 때까지는 다시 누를 수 없음
      }, REFILL_MS);
    }
  });
})();
