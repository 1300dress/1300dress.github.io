// 문장뽑기 릴스: 인스타그램에서 화면을 꾹 눌러 멈추듯, 누르면 멈추고 다시 누르면 이어서 돌아감
document.querySelectorAll(".j-frame.is-pick").forEach((frame) => {
  const v = frame.querySelector("video");
  const toggle = () => {
    const picking = !v.paused;
    picking ? v.pause() : v.play();
    frame.classList.toggle("is-picked", picking);
    frame.setAttribute("aria-pressed", String(picking));
    frame.setAttribute("aria-label", picking ? "다시 눌러 이어서 돌리기" : "눌러서 행운의 문장 뽑기");
  };
  frame.addEventListener("click", toggle);
  frame.addEventListener("keydown", (e) => {
    if (e.key === "Enter" || e.key === " ") { e.preventDefault(); toggle(); }
  });
});
