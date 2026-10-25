# content/letter.md → letter.html (자기소개서 페이지)
# 프로젝트 상세와 같은 저널 위계: 머리(이름표 → 제목 → 쑥잎색 한 줄) → 항목마다 짧은 선 + 이름표 + 소제목 → 본문
import html, re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
src = (ROOT / "content" / "letter.md").read_text().strip().splitlines()

def inline(t):
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", html.escape(t, quote=False))

title, sub, secs, cur = "", "", [], None
for line in src:
    if line.startswith("# "):
        title = line[2:]
    elif line.startswith("## "):
        num, label = line[3:].split(". ", 1)
        cur = {"num": num, "label": label, "title": "", "ps": []}
        secs.append(cur)
    elif line.startswith("### "):
        cur["title"] = line[4:]
    elif line.strip() and cur is None:
        sub = line.strip()
    elif line.strip():
        cur["ps"].append(line.strip())

body = "\n\n".join(
    f'  <h2 class="j-sec" id="s{s["num"]}"><span class="j-sec-label">{s["num"]} · {html.escape(s["label"])}</span>'
    f'<span class="j-sec-title">{inline(s["title"])}</span></h2>\n'
    + "\n".join(f'  <p class="j-p">{inline(p)}</p>' for p in s["ps"])
    for s in secs)

(ROOT / "letter.html").write_text(f'''<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Letter — 조수빈</title>
  <link rel="icon" type="image/png" sizes="32x32" href="assets/icons/favicon-32.png">
  <link rel="icon" type="image/png" sizes="16x16" href="assets/icons/favicon-16.png">
  <link rel="icon" type="image/png" sizes="192x192" href="assets/icons/icon-192.png">
  <link rel="apple-touch-icon" href="assets/icons/apple-touch-icon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="assets/style.css">
  <link rel="stylesheet" href="assets/journal.css">
</head>
<body>
  <header class="site-header">
    <a class="name logo" href="index.html" aria-label="subin teahouse — 조수빈, 홈으로"><img class="logo-mark" src="assets/img/name.png" alt="" width="539" height="101"></a>
    <nav class="site-nav">
      <a href="about.html">About</a>
      <a href="letter.html" aria-current="page">Letter</a>
      <a href="cv.html">C/V</a>
      <a href="portfolio.html">Portfolio</a>
    </nav>
  </header>

  <article class="journal">
  <header class="j-head">
    <p class="j-kicker">Cover Letter</p>
    <h1 class="j-title">{html.escape(title)}</h1>
    <p class="j-why">{html.escape(sub)}</p>
  </header>

{body}

  <footer class="j-foot">
    <p class="j-back"><a href="cv.html">C/V 보기</a> &nbsp;·&nbsp; <a href="portfolio.html">Portfolio 보기</a></p>
  </footer>
  </article>

  <footer class="site-footer">© 조수빈 · 한 잔이 나가기 전, 마지막을 살핍니다.</footer>
  <script src="assets/ko-wrap.js"></script>
</body>
</html>
''')
print("built letter.html", len(secs), "sections")
