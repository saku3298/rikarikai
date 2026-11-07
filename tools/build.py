#!/usr/bin/env python3
"""work.json から、このサイトのHTMLをすべて生成します。

使い方（リポジトリのルートで）:
    python3 tools/build.py

生成されるもの:
    index.html（作品トップ）、episodeN.html（各話）、volumeN.html（単行本）、404.html

編集してよいのは work.json、css/、js/ です。生成されたHTMLは直接編集しないでください。

話・巻を追加するとき:
  1. 画像を置く
       images/episodes/episode02-001.webp, episode02-002.webp …（話2桁-ページ3桁）
       images/thumbs/episode02.webp
       images/volumes/volume02-cover.webp（巻を追加するとき）
  2. work.json の "episodes" / "volumes" に追記する
  3. python3 tools/build.py
ページ数は画像の枚数から自動で数えます。
"""
import glob, hashlib, html, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
e = html.escape

data = json.load(open("work.json", encoding="utf-8"))
site, work = data["site"], data["work"]
episodes, volumes, related = data["episodes"], data.get("volumes", []), data.get("related", [])
site_link = data.get("site_link")
BASE = site["url"].rstrip("/") + "/"
TITLE = work["title"]


def ver(path):
    return hashlib.md5(open(path, "rb").read()).hexdigest()[:8]


def img(base):
    """拡張子なしのパスから、実在する画像（webp優先）のパスを返す"""
    for ext in ("webp", "jpg", "png"):
        if os.path.exists(f"{base}.{ext}"):
            return f"{base}.{ext}"
    sys.exit(f"エラー: 画像が見つかりません: {base}.webp（または .jpg）")


def count_pages(no):
    for ext in ("webp", "jpg"):
        n = len(glob.glob(f"images/episodes/episode{no:02d}-*.{ext}"))
        if n:
            return n
    sys.exit(f"エラー: images/episodes/episode{no:02d}-001.webp などがありません")


for ep in episodes:
    ep["pages"] = count_pages(ep["no"])
ep_by_no = {ep["no"]: ep for ep in episodes}
vol_of_ep = {}
for v in volumes:
    for n in v["episodes"]:
        vol_of_ep[n] = v

V_CSS = ver("css/style.css")
V_VIEWER = ver("js/viewer.js")
V_TOP = ver("js/top.js")


def head(title, desc, url, typ, prefix="", theme=False):
    og = f'''<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="{typ}">
<meta property="og:site_name" content="{e(site["name"])}">
<meta property="og:locale" content="ja_JP">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}images/ogp/default.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{e(TITLE)}">
<meta name="twitter:card" content="summary_large_image">'''
    return f'''<!doctype html>
<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">{'<meta name="theme-color" content="#111111">' if theme else ''}
<title>{e(title)}</title>
{og}
<link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{prefix}css/style.css?v={V_CSS}"></head>
'''


def vol_cover(v):
    return img(f"images/volumes/volume{v['no']:02d}-cover")


def index_page():
    first, last = episodes[0], episodes[-1]
    hero_vol = volumes[0] if volumes else None
    hero_img = (f'<img src="{vol_cover(hero_vol)}" alt="{e(TITLE)} 第{hero_vol["no"]}巻表紙">' if hero_vol else "")
    rows = "".join(
        f'<a class="episode-row" href="episode{ep["no"]}.html" data-ep="{ep["no"]}">'
        f'<img class="episode-thumb" src="{img(f"images/thumbs/episode{ep["no"]:02d}")}" alt="第{ep["no"]}話 {e(ep["title"])}">'
        f'<div class="episode-meta"><div class="episode-title">第{ep["no"]}話 <span>{e(ep["title"])}</span></div></div>'
        f'<div class="episode-read">読む</div></a>' for ep in episodes)
    tiles = "".join(
        f'<a class="volume-tile" href="volume{v["no"]}.html"><img src="{vol_cover(v)}" alt="{e(TITLE)} 第{v["no"]}巻表紙">'
        f'<div><strong>第{v["no"]}巻</strong><span>{e(v["summary"])}</span></div></a>'
        for v in sorted(volumes, key=lambda v: -v["no"]))
    tab = ' target="_blank" rel="noopener"'
    cards = "".join(
        f'<a class="author-work-card" href="{e(r["url"])}"{tab if r.get("new_tab") else ""}>'
        f'<img src="{img("images/related/" + r["cover"])}" alt="{e(r["cover_alt"])}">'
        f'<div><div class="author-work-title">{e(r["title"])}</div><div class="author-work-author">作者：{e(r["author"])}</div>'
        f'<span class="author-work-label">コミックス</span></div></a>' for r in related)
    if site_link:
        cards += (f'<a class="author-work-card" href="{e(site_link["url"])}"{tab if site_link.get("new_tab") else ""}>'
                  f'<img src="{img("images/work/" + site_link["image"])}" alt="{e(site_link["title"])}">'
                  f'<div><div class="author-work-title">{e(site_link["title"])}</div>'
                  f'<div class="author-work-author">{e(site_link["description"])}</div>'
                  f'<span class="author-work-label">作品集</span></div></a>')
    related_html = f'<div class="info-section"><h2>同じ作者の作品</h2>{cards}</div>' if (related or site_link) else ""
    footer_link = f' ｜ <a href="{e(site_link["url"])}" target="_blank" rel="noopener" style="text-decoration:underline">{e(site_link["title"])}</a>' if site_link else ""
    return head(TITLE, site["description"], BASE, "website") + f'''<body class="top-page"><div class="jp-shell">
<section class="jp-hero">{hero_img}<div class="jp-hero-right"><div class="jp-hero-text"><div class="jp-kicker">ORIGINAL MANGA</div><div class="jp-logo">{e(TITLE)}</div></div></div></section>
<section class="jp-info"><h1 class="jp-title">{e(TITLE)}</h1><div class="jp-author">{e(work["author"])}</div><div class="jp-tags"><span>オリジナル漫画</span><span>全{len(episodes)}話公開中</span></div><div class="jp-actions"><a class="jp-btn primary" href="episode{first["no"]}.html">第{first["no"]}話から読む</a><a class="jp-btn" href="episode{last["no"]}.html">最新話から読む</a></div></section>
<nav class="jp-tabs" aria-label="作品メニュー"><button class="jp-tab active" data-tab="episodes">話</button><button class="jp-tab" data-tab="comics">コミックス</button><button class="jp-tab" data-tab="info">作品情報</button></nav>
<section id="episodes" class="jp-panel active"><div class="episode-sort-header"><span>全{len(episodes)}話</span><div class="sort-switch episode-sort"><button type="button" class="sort-btn active" data-order="asc">1話から</button><span>|</span><button type="button" class="sort-btn" data-order="desc">最新話から</button></div></div><div class="range-bar"><button class="range-btn active">1-</button></div><div class="episode-list">{rows}</div></section>
<section id="comics" class="jp-panel"><div class="comics-header"><strong>コミックス</strong><div class="comics-sort"><span class="active">新しい順</span></div></div><div class="volume-list">{tiles}</div></section>
<section id="info" class="jp-panel info-panel"><div class="work-intro"><div class="work-catch">{e(TITLE)}</div><p class="work-summary">{e(work["summary"])}</p><div class="author-profile"><img src="{img("images/work/author-portrait")}" alt="{e(work["author_portrait_alt"])}"><div><span>作者</span><strong>{e(work["author"])}</strong></div></div></div>{related_html}</section>
</div><footer>{e(site["copyright"])}{footer_link}</footer>
<script src="js/top.js?v={V_TOP}"></script></body></html>
'''


def pages_html(items, eager):
    out = []
    for i, (src, alt, attr) in enumerate(items):
        lazy = "" if i < eager else ' loading="lazy"'
        out.append(f'    <div class="manga-page"{attr}><img{lazy} src="{src}" alt="{e(alt)}"></div>')
    return "\n".join(out)


def reader_tail(total, footer_links):
    return (f'<div class="page-nav"><button id="prev" type="button">← 次のページ</button>'
            f'<button id="next" type="button">前のページ →</button></div>'
            f'<div class="counter" id="counter">1 / {total}</div>'
            f'<div class="reader-footer">{footer_links}</div>'
            f'<script src="js/viewer.js?v={V_VIEWER}"></script></body></html>\n')


def reader_top(back_href, back_text):
    return (f'<body class="reader-page"><header class="reader-bar"><div class="reader-bar-inner">'
            f'<div class="reader-title"><a id="context-back" href="{back_href}">{back_text}</a></div>'
            f'<div class="reader-controls"><button class="small-btn" id="top" type="button">先頭へ</button></div></div><div class="progress" aria-hidden="true"><div id="progress-fill"></div></div></header>\n')


def episode_page(ep):
    no, v = ep["no"], vol_of_ep.get(ep["no"])
    title = f'第{no}話「{ep["title"]}」 | {TITLE}'
    desc = f'オリジナル漫画『{TITLE}』第{no}話「{ep["title"]}」'
    items = [(img(f"images/episodes/episode{no:02d}-{p:03d}"), f"第{no}話 ページ{p}", f' data-i="{p - 1}"')
             for p in range(1, ep["pages"] + 1)]
    vattr = f' data-volume-href="volume{v["no"]}.html" data-volume-label="第{v["no"]}巻"' if v else ""
    nav = f'<div class="episode-nav"><a class="small-btn" href="volume{v["no"]}.html">第{v["no"]}巻の目次</a></div>' if v else ""
    footer = '<a href="index.html">HOME</a>' + (f'　|　<a href="volume{v["no"]}.html">第{v["no"]}巻</a>' if v else "")
    return (head(title, desc, f"{BASE}episode{no}.html", "article", theme=True)
            + reader_top("index.html", "← 話一覧へ戻る")
            + f'<main class="viewer" id="viewer"{vattr}>\n{pages_html(items, 2)}\n</main>\n{nav}'
            + reader_tail(ep["pages"], footer))


def volume_page(v):
    no = v["no"]
    title = f'第{no}巻 | {TITLE}'
    desc = f'オリジナル漫画『{TITLE}』第{no}巻'
    items = [(vol_cover(v), f"{TITLE} 第{no}巻 表紙", ' data-volume-cover="true"')]
    i = 0
    for n in v["episodes"]:
        ep = ep_by_no[n]
        for p in range(1, ep["pages"] + 1):
            items.append((img(f"images/episodes/episode{n:02d}-{p:03d}"), f"第{n}話 ページ{p}", f' data-i="{i}"'))
            i += 1
    footer = '<a href="index.html">HOME</a>　|　<a href="index.html#comics">コミックス一覧</a>'
    return (head(title, desc, f"{BASE}volume{no}.html", "article", theme=True)
            + reader_top("index.html#comics", "← コミックス一覧へ戻る")
            + f'<main class="viewer" id="viewer" data-volume-reader="true">\n{pages_html(items, 3)}\n</main>\n'
            + reader_tail(len(items), footer))


def not_found_page():
    return f'''<!doctype html>
<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex">
<title>ページが見つかりません | {e(TITLE)}</title>
<link rel="icon" href="{BASE}assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{BASE}css/style.css?v={V_CSS}"></head>
<body class="top-page"><div class="jp-shell"><div class="nf">
<p class="nf-code" aria-hidden="true">404</p>
<h1>ページが見つかりません</h1>
<p>URLがまちがっているか、ページが移動したのかもしれません。</p>
<div class="jp-actions" style="justify-content:center"><a class="jp-btn primary" href="{BASE}">{e(TITLE)}のトップへ</a></div>
</div></div><footer>{e(site["copyright"])}</footer></body></html>
'''


def write(path, text):
    open(path, "w", encoding="utf-8", newline="\n").write(text)
    print("生成:", path)


write("index.html", index_page())
for ep in episodes:
    write(f"episode{ep['no']}.html", episode_page(ep))
for v in volumes:
    write(f"volume{v['no']}.html", volume_page(v))
write("404.html", not_found_page())
print("完了")
