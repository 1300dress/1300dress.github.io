# 레이아웃 확인용 임시 이미지(SVG)를 assets/dummy/에 만듭니다. 실제 결과물로 오인되지 않게 모두 '임시'라고 적혀 있습니다.
# 실제 자료로 다 바꾸고 나면 assets/dummy/ 폴더째 지워도 됩니다.
import os
OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "dummy")
SIZES = {"4x5": (1080, 1350), "3x2": (1500, 1000), "16x9": (1600, 900), "1x1": (1200, 1200),
         "3x4": (1200, 1600), "21x9": (2100, 900), "9x16": (900, 1600)}
TONES = ["#e6e8de", "#ecebe6", "#e2e5dc"]

def svg(name, w, h, tone, label):
    fs = round(min(w, h) / 14)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  <defs><pattern id="p" width="28" height="28" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
    <line x1="0" y1="0" x2="0" y2="28" stroke="#56622f" stroke-opacity=".07" stroke-width="10"/></pattern></defs>
  <rect width="100%" height="100%" fill="{tone}"/><rect width="100%" height="100%" fill="url(#p)"/>
  <g font-family="Pretendard, -apple-system, sans-serif" text-anchor="middle" fill="#56622f">
    <text x="50%" y="{h/2 - fs*0.3:.0f}" font-size="{fs}" font-weight="600">{label}</text>
    <text x="50%" y="{h/2 + fs*0.9:.0f}" font-size="{fs*0.5:.0f}" fill="#7b8178">{name.replace("x", ":")} · 실제 결과물 아님</text>
  </g>
</svg>
'''

os.makedirs(OUT, exist_ok=True)
for name, (w, h) in SIZES.items():
    for i, tone in enumerate(TONES):
        open(os.path.join(OUT, f"img-{name}-{i+1}.svg"), "w", encoding="utf-8").write(svg(name, w, h, tone, "임시 이미지"))
open(os.path.join(OUT, "poster-9x16.svg"), "w", encoding="utf-8").write(svg("9x16", 900, 1600, TONES[0], "임시 영상 ▶"))
open(os.path.join(OUT, "poster-16x9.svg"), "w", encoding="utf-8").write(svg("16x9", 1600, 900, TONES[0], "임시 영상 ▶"))
print("ok")
