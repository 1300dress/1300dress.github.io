// 한 번 나온 문장은 목록을 다 돌기 전까지 다시 나오지 않습니다.
(function () {
  const button = document.querySelector("[data-draw]");
  const cup = document.querySelector(".cup");
  if (!button || !cup || !window.LINES || !window.LINES.length) return;

  const lineEl = cup.querySelector(".line");
  const sourceEl = cup.querySelector(".source");
  let pool = [];

  function next() {
    if (!pool.length) pool = window.LINES.slice().sort(() => Math.random() - 0.5);
    return pool.pop();
  }

  button.addEventListener("click", () => {
    const pick = next();
    cup.classList.remove("steeped");
    // 다시 우러나는 효과를 위해 한 프레임 쉬었다가 표시
    setTimeout(() => {
      lineEl.textContent = pick.text;
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
      button.textContent = "한 잔 더";
    }, 250);
  });
})();
