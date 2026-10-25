// 문장뽑기 릴스: 인스타그램에서 화면을 꾹 눌러 멈추듯, 버튼(또는 영상)을 누르면 멈추고 다시 누르면 이어서 돌아감
document.querySelectorAll(".j-frame.is-pick").forEach((frame) => {
  const fig = frame.closest("figure");
  const v = frame.querySelector("video");
  const btn = fig.querySelector(".j-pick-btn");
  const label = btn.querySelector(".j-pick-label");
  const toggle = () => {
    const picking = !v.paused;
    picking ? v.pause() : v.play();
    frame.classList.toggle("is-picked", picking);
    btn.setAttribute("aria-pressed", String(picking));
    label.textContent = picking ? "뽑았습니다 · 다시 돌리기" : "눌러서 행운의 문장 뽑기";
  };
  btn.addEventListener("click", toggle);
  frame.addEventListener("click", toggle);
});
