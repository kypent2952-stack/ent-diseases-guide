#!/usr/bin/env python3
"""guides.json → index.html 폴백 영역(정적 카드 HTML, 준비 중 목록, 내장 JSON) 재생성.

사용법:  python3 tools/build_fallback.py
guides.json을 고친 뒤 한 번 실행하면 JSON을 못 읽는 환경(파일 직접 열기, JS 꺼짐,
네트워크 오류)에서도 같은 목록이 보입니다. 마크업은 index.html의 JS 렌더와 동일합니다.
"""
import html, json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
AUD = {"pro": "의료진", "patient": "환자"}
e = lambda s: html.escape(str(s if s is not None else ""), quote=True).replace("&#x27;", "&#39;")

def card(g):
    tags = "".join(f'<span class="kyp-badge kyp-badge--{e(a)}">{e(AUD.get(a, a))}</span>' for a in g.get("audience", []))
    return (f'<li><article class="kyp-card guide"><h3>{e(g["title"])}</h3>'
            f'<div class="guide__tags">{tags}</div><p>{e(g["summary"])}</p>'
            f'<div class="guide__actions"><a class="kyp-btn" href="{e(g["url"])}" aria-label="{e(g["title"])} 바로가기">바로가기 →</a></div>'
            '</article></li>')

def main():
    data = json.loads((ROOT / "guides.json").read_text(encoding="utf-8"))
    cats = ""
    for c in data["categories"]:
        items = [g for g in data["guides"] if g["category"] == c["id"]]
        if not items:
            continue
        cats += (f'<section class="cat" data-cat="{e(c["id"])}" aria-labelledby="cat-{e(c["id"])}">'
                 f'<div class="cat__head"><h2 id="cat-{e(c["id"])}"><span aria-hidden="true">{e(c["icon"])}</span> {e(c["name"])}</h2>'
                 f'<p>{e(c["description"])}</p></div><ul class="grid">{"".join(map(card, items))}</ul></section>')
    up = "".join(f'<li><div class="kyp-card soon"><span class="kyp-badge">준비 중</span><h3>{e(x["title"])}</h3><p>{e(x["summary"])}</p></div></li>'
                 for x in data.get("upcoming", []))
    slim = {k: data[k] for k in ("categories", "guides", "upcoming")}
    js = json.dumps(slim, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    js = f'<script type="application/json" id="guides-fallback">{js}</script>'

    p = ROOT / "index.html"
    s = p.read_text(encoding="utf-8")
    for name, body in (("HTML", cats), ("UPCOMING", up), ("JSON", js)):
        pat = re.compile(rf"(<!-- FALLBACK:{name}:START[^>]*-->\n).*?(\n<!-- FALLBACK:{name}:END -->)", re.S)
        s, n = pat.subn(lambda m: m.group(1) + body + m.group(2), s)
        if n != 1:
            sys.exit(f"marker FALLBACK:{name} not found")
    p.write_text(s, encoding="utf-8")
    print(f"ok: {len(data['guides'])} guides, {len(data.get('upcoming', []))} upcoming")

if __name__ == "__main__":
    main()
