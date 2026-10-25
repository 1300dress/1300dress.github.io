# content/letter.md → letter.html (자기소개서 페이지). 제목의 " / " 자리에서 줄을 바꿈
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
  <style>
    /* 맨 아래 PDF 내려받기: C/V와 같은 쑥잎색 버튼 */
    .cv-download {{ margin: 72px 0 0; text-align: center; }}
    .cv-pdf {{ display: inline-flex; align-items: center; gap: 8px; padding: 10px 22px; border-radius: 999px; font-size: 14px; font-weight: 500; color: var(--paper); background: var(--ssuk-deep); text-decoration: none; }}
    .cv-pdf:hover, .cv-pdf:focus-visible {{ background: var(--ink); color: var(--paper); }}
    /* 인쇄하면 A4 자기소개서 PDF: 웹과 같은 위계, 좌우 여백 넉넉히 */
    @media print {{
      @page {{ size: A4; margin: 20mm 30mm 18mm;
        @bottom-right {{ content: counter(page) " / " counter(pages); font: 7.5pt "Pretendard", sans-serif; color: #7b8178; }} }}
      html, body {{ background: #fff !important; }}
      body {{ padding: 0; }}
      .site-header, .site-footer, .j-foot, .cv-download {{ display: none !important; }}
      .journal {{ display: block; margin: 0; font-size: 9.6pt; line-height: 1.8; }}
      .j-head {{ padding-top: 0; margin-bottom: 12mm; }}
      .j-kicker {{ font-size: 8pt; margin-bottom: 3mm; }}
      .j-title {{ font-size: 25pt; }}
      .j-why {{ font-size: 12pt; margin-top: 3mm; }}
      .j-sec {{ margin: 11mm 0 4mm; break-after: avoid; }}
      .j-sec::before {{ margin-bottom: 4mm; }}
      .j-sec-label {{ font-size: 9pt; }}
      .j-sec-title {{ font-size: 14pt; margin-top: 1.5mm; }}
      .j-p {{ margin-bottom: 1.1em; orphans: 2; widows: 2; }}
      a {{ color: inherit; text-decoration: none; }}
    }}
  </style>
</head>
<body>
  <header class="site-header">
    <a class="name logo" href="index.html?welcome" aria-label="subin teahouse — 조수빈, 홈으로"><img class="logo-mark" src="assets/img/name.png" alt="" width="539" height="101"></a>
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
    <h1 class="j-title">{"<br>".join(html.escape(t.strip()) for t in title.split(" / "))}</h1>
    <p class="j-why">{html.escape(sub)}</p>
  </header>

{body}

  <p class="cv-download"><a class="cv-pdf" href="assets/subin-jo-cover-letter.pdf" download>PDF Download <span aria-hidden="true">↓</span></a></p>

  <footer class="j-foot">
    <p class="j-back"><a href="cv.html">C/V 보기</a> &nbsp;·&nbsp; <a href="portfolio.html">Portfolio 보기</a></p>
  </footer>
  </article>

  <footer class="site-footer">© 조수빈 · 맑게 비추고 깊게 우려내는 콘텐츠 마케터</footer>
  <script src="assets/ko-wrap.js"></script>
</body>
</html>
''')
print("built letter.html", len(secs), "sections")
