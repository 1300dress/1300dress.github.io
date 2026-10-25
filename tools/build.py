# 프로젝트 상세 페이지(저널) 빌드: content/projects/*.json → projects/NN.html
# 원고와 미디어 순서는 JSON에만 있고, 모양은 assets/journal.css가 맡습니다.
# 실행: python3 tools/build.py   (블록 종류와 노션 대응표는 content/README.md)
import html, json, os, re

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SRC = os.path.join(ROOT, "content", "projects")
OUT = os.path.join(ROOT, "projects")

def esc(s):
    return html.escape(s or "", quote=True)

def todo(s):
    return f'<span class="todo">{esc(s)}</span>'

def media_src(src):
    # JSON에는 사이트 루트 기준 경로(assets/…)나 외부 URL을 적습니다
    return src if re.match(r"^(https?:)?//", src) else "../" + src.lstrip("/")

def caption(text, cls="j-cap"):
    return f'\n    <figcaption class="{cls}">{text}</figcaption>' if text else ""

def img(item, cls=""):
    ratio = item.get("ratio", "")
    style = f' style="aspect-ratio: {ratio.replace(":", " / ")}"' if ratio else ""
    return f'<img src="{esc(media_src(item["src"]))}" alt="{esc(item.get("alt", ""))}" loading="lazy"{style}{cls}>'

def video(b):
    ratio = b.get("ratio", "16:9")
    poster = f' poster="{esc(media_src(b["poster"]))}"' if b.get("poster") else ""
    src = media_src(b["src"]) + ("" if b.get("poster") else "#t=0.1")   # 포스터가 없으면 첫 장면을 보여 줌
    # loop: 소리 없는 짧은 반복 영상(문장뽑기 띠 등)은 컨트롤 없이 자동 재생
    attrs = "autoplay muted loop playsinline" if b.get("loop") else 'controls playsinline preload="metadata"'
    return (f'<div class="j-frame" style="aspect-ratio: {ratio.replace(":", " / ")}">'
            f'<video {attrs}{poster}>'
            f'<source src="{esc(src)}" type="{esc(b.get("mime", "video/mp4"))}">'
            f'</video></div>')

def grid_item(i):
    media = video(i) if i["src"].endswith(".mp4") else img(i)
    cap = f'<span class="j-grid-cap">{i["caption"]}</span>' if i.get("caption") else ""
    return f'<li>{media}{cap}</li>'


# 문단·인용의 글은 작성자가 쓴 그대로 넣습니다(<em>, <a>, <br> 정도의 인라인 태그 허용)
def block(b):
    t = b["type"]
    dummy = " is-dummy" if b.get("dummy") else ""
    if t == "section":
        title = f'<span class="j-sec-title">{b["title"]}</span>' if b.get("title") else ""
        return (f'  <h2 class="j-sec" id="{esc(b["label"].lower())}">'
                f'<span class="j-sec-label">{esc(b["label"])}</span>{title}</h2>')
    if t == "p":
        return f'  <p class="j-p{dummy}">{b["text"]}</p>'
    if t == "quote":
        cite = f'<cite>{b["cite"]}</cite>' if b.get("cite") else ""
        return f'  <blockquote class="j-quote{dummy}"><p>{b["text"]}</p>{cite}</blockquote>'
    if t == "image":
        return (f'  <figure class="j-fig is-{b.get("width", "text")}{dummy}">\n    {img(b)}'
                f'{caption(b.get("caption"))}\n  </figure>')
    if t == "pair":
        imgs = "\n    ".join(img(i) for i in b["items"])
        return (f'  <figure class="j-fig j-pair is-{b.get("width", "wide")}{dummy}">\n    <div class="j-pair-row">\n    {imgs}\n    </div>'
                f'{caption(b.get("caption"))}\n  </figure>')
    if t == "carousel":
        slides = "\n      ".join(f'<li>{img(i)}</li>' for i in b["items"])
        n = len(b["items"])
        hint = f'<span class="j-cap-hint">{n}장 · 옆으로 넘겨 보기</span>'
        return (f'  <figure class="j-fig j-carousel is-wide{dummy}">\n    <ol class="j-slides" tabindex="0" aria-label="캐러셀 {n}장">\n      {slides}\n    </ol>'
                f'{caption(hint + (b.get("caption") or ""))}\n  </figure>')
    if t == "video":
        ratio = b.get("ratio", "16:9")
        shape = "is-vertical" if ratio in ("9:16", "4:5", "3:4") else "is-landscape"
        layout = " is-aside" if b.get("layout") == "aside" else ""
        width = b.get("width", "text" if shape == "is-vertical" else "wide")
        return (f'  <figure class="j-fig j-video {shape} is-{width}{layout}{dummy}">\n    {video(b)}'
                f'{caption(b.get("caption"))}\n  </figure>')
    if t == "grid":                              # 표지 모음·릴스 묶음: cols(넓은 화면) / mcols(모바일) 칸
        items = "\n      ".join(grid_item(i) for i in b["items"])
        scroll = " is-scroll" if b.get("scroll") else ""
        style = f'--cols: {b.get("cols", 3)}; --mcols: {b.get("mcols", 2)}'
        return (f'  <figure class="j-fig j-grid is-{b.get("width", "wide")}{dummy}">\n    <ul class="j-grid-list{scroll}" style="{style}">\n      {items}\n    </ul>'
                f'{caption(b.get("caption"))}\n  </figure>')
    if t == "break":
        return '  <hr class="j-break">'
    raise ValueError(f"모르는 블록 종류: {t}")

def meta_rows(meta):
    rows = []
    for m in meta:
        v = m["value"] if m.get("value") else todo(m.get("todo", m["label"] + " 확인"))
        rows.append(f'      <div><dt>{esc(m["label"])}</dt><dd>{v}</dd></div>')
    return "\n".join(rows)

def credits(items):
    if not items:
        return ""
    rows = []
    for c in items:
        v = f'<a href="{esc(c["href"])}">{esc(c["value"])}</a>' if c.get("href") else c["value"]
        rows.append(f'      <div><dt>{esc(c["label"])}</dt><dd>{v}</dd></div>')
    return '    <dl class="j-credits">\n' + "\n".join(rows) + "\n    </dl>\n"

def neighbor(p, rel):
    if not p:
        return f'<span class="j-nav-empty"></span>'
    arrow = "← 이전" if rel == "prev" else "다음 →"
    return (f'<a class="j-nav-{rel}" href="{p["num"]}.html" rel="{rel}">'
            f'<span class="j-nav-dir">{arrow} · ({int(p["num"])})</span>'
            f'<span class="j-nav-title title">{esc(p["title"])}</span>'
            f'<span class="j-nav-why">{esc(p["why"])}</span></a>')

HEAD = """<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} — 조수빈</title>
  <meta name="description" content="{why}">
  <link rel="icon" type="image/png" sizes="32x32" href="../assets/icons/favicon-32.png">
  <link rel="icon" type="image/png" sizes="16x16" href="../assets/icons/favicon-16.png">
  <link rel="icon" type="image/png" sizes="192x192" href="../assets/icons/icon-192.png">
  <link rel="apple-touch-icon" href="../assets/icons/apple-touch-icon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../assets/style.css">
  <link rel="stylesheet" href="../assets/journal.css">
</head>
<body>
  <!-- 이 파일은 tools/build.py가 content/projects/{num}.json으로 만듭니다. 직접 고치지 말고 JSON을 고친 뒤 다시 빌드하세요. -->
  <header class="site-header">
    <a class="name logo" href="../index.html" aria-label="subin teahouse — 조수빈, 홈으로"><img class="logo-mark" src="../assets/img/name.png" alt="" width="539" height="101"></a>
    <nav class="site-nav">
      <a href="../about.html">About</a>
      <a href="../cv.html">C/V</a>
      <a href="../portfolio.html" aria-current="page">Portfolio</a>
    </nav>
  </header>
"""

def page(p, prev, nxt):
    notice = ('    <p class="j-notice">임시 시안 · 이 페이지의 글·이미지·영상은 레이아웃 확인용 더미입니다. '
              '실제 원고와 결과물로 바뀔 예정입니다.</p>\n') if p.get("status") == "dummy" else ""
    if p.get("status") == "media":
        notice = '    <p class="j-notice">작업 중 · 이미지와 영상은 실제 결과물이고, 글은 아직 임시 원고입니다.</p>\n'
    # 자동 반복 영상은 '동작 줄이기' 설정을 켠 사람에게는 멈춘 채 컨트롤을 보여 줌
    motion = ('  <script>if(matchMedia("(prefers-reduced-motion: reduce)").matches)'
              'document.querySelectorAll("video[autoplay]").forEach(v=>{v.pause();v.controls=true;});</script>\n'
              ) if any(b.get("loop") or any(i.get("loop") for i in b.get("items", [])) for b in p["body"]) else ""
    dek = f'    <p class="j-dek">{p["dek"]}</p>\n' if p.get("dek") else ""
    body = "\n\n".join(block(b) for b in p["body"])
    return (HEAD.format(title=esc(p["title"]), why=esc(p["why"]), num=p["num"]) + f"""
  <article class="journal">
  <header class="j-head">
{notice}    <p class="j-kicker"><span class="num">({int(p["num"])})</span> · {esc(p["category"])}</p>
    <h1 class="j-title">{esc(p["title"])}</h1>
    <p class="j-why">{esc(p["why"])}</p>
{dek}    <dl class="j-meta">
{meta_rows(p["meta"])}
    </dl>
  </header>

{body}

  <footer class="j-foot">
{credits(p.get("credits"))}    <nav class="j-nav" aria-label="다른 프로젝트">
      {neighbor(prev, "prev")}
      {neighbor(nxt, "next")}
    </nav>
    <p class="j-back"><a href="../portfolio.html">Portfolio 전체 보기</a></p>
  </footer>
  </article>

  <footer class="site-footer">© 조수빈 · 한 잔이 나가기 전, 마지막을 살핍니다.</footer>
  <script src="../assets/ko-wrap.js"></script>
{motion}</body>
</html>
""")

def main():
    files = sorted(f for f in os.listdir(SRC) if re.fullmatch(r"\d\d\.json", f))
    projects = [json.load(open(os.path.join(SRC, f), encoding="utf-8")) for f in files]
    for i, p in enumerate(projects):
        prev = projects[i - 1] if i > 0 else None
        nxt = projects[i + 1] if i + 1 < len(projects) else None
        path = os.path.join(OUT, f'{p["num"]}.html')
        open(path, "w", encoding="utf-8").write(page(p, prev, nxt))
        print("built", os.path.relpath(path, ROOT))

if __name__ == "__main__":
    main()
