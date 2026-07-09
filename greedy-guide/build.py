#!/usr/bin/env python3
"""
靜態頁面產生器 — 貪心演算法完全指南

用途：把 content/ 目錄下的內容片段（每個子主題一個 .html 檔）套上共用的
版面模板（側欄導覽、設定面板、上一頁/下一頁），輸出成 greedy-guide/ 底下
的最終靜態頁面。CI 不需要執行這支腳本 —— 產生的 .html 檔會直接進版控、
GitHub Pages 只是原樣提供這些靜態檔案。

使用時機：修改 content/*.html 的教學內容之後，執行：
    python3 build.py
重新產生所有頁面。若新增子主題頁面，請一併在下面的 PAGES 清單中登記。
"""
import posixpath
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
CONTENT_DIR = os.path.join(ROOT, "content")

FAVICON = (
    'data:image/svg+xml,'
    '<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22>'
    '<text y=%22.9em%22 font-size=%2290%22>%F0%9F%A7%AD</text></svg>'
)

# ── 頁面登記表 ──────────────────────────────────────────────────
# id, path (相對於 greedy-guide/ 根目錄), nav 標題, 卡片描述, 內容片段檔名
PAGES = [
    dict(id="index", path="index.html", nav=None, title="首頁",
         desc="從入門到程式競賽專家的貪心演算法策略分類與題目整理", frag=None),
    dict(id="theory", path="pages/theory.html", nav="1. 理論基礎",
         title="理論基礎：什麼時候貪心是對的",
         desc="貪心選擇性質、最優子結構、四大證明技巧與反例構造的系統方法",
         frag="s1-theory.html"),
    dict(id="s01", path="pages/strategies/01-sorting.html", nav="2.1 排序貪心",
         title="2.1 排序貪心（Sort & Sweep）",
         desc="找到正確排序鍵，排序後線性掃描，決策就變得顯然",
         frag="s2-1.html", group="strategies"),
    dict(id="s02", path="pages/strategies/02-intervals.html", nav="2.2 區間問題全家桶",
         title="2.2 區間問題全家桶（Interval Scheduling Family）",
         desc="活動選擇、區間覆蓋、區間分組——左右端點排序的完整對照",
         frag="s2-2.html", group="strategies"),
    dict(id="s03", path="pages/strategies/03-exchange-scheduling.html", nav="2.3 交換論證排程",
         title="2.3 交換論證排程（Scheduling by Exchange Argument）",
         desc="Smith's Rule、Johnson's Rule 與交換論證+DP 的組合套路",
         frag="s2-3.html", group="strategies"),
    dict(id="s04", path="pages/strategies/04-regret.html", nav="2.4 反悔貪心",
         title="2.4 反悔貪心（Regret Greedy）",
         desc="先貪心接受，再用堆撤銷最差決策的萬用框架",
         frag="s2-4.html", group="strategies"),
    dict(id="s05", path="pages/strategies/05-heap.html", nav="2.5 堆積貪心",
         title="2.5 堆積貪心（Priority-Queue Greedy）",
         desc="Huffman 編碼、對頂堆與多路歸併",
         frag="s2-5.html", group="strategies"),
    dict(id="s06", path="pages/strategies/06-lexicographic.html", nav="2.6 字典序貪心",
         title="2.6 字典序貪心與單調堆疊構造",
         desc="逐位確定最小/最大字元，搭配可行性檢查與單調棧實作",
         frag="s2-6.html", group="strategies"),
    dict(id="s07", path="pages/strategies/07-math.html", nav="2.7 數學貪心與調整法",
         title="2.7 數學貪心與調整法",
         desc="中位數、排序不等式、均值不等式與 canonical 硬幣系統",
         frag="s2-7.html", group="strategies"),
    dict(id="s08", path="pages/strategies/08-graph.html", nav="2.8 圖上貪心",
         title="2.8 圖上貪心",
         desc="MST 的 Cut/Cycle Property、Dijkstra 正確性邊界、Boruvka",
         frag="s2-8.html", group="strategies"),
    dict(id="s09", path="pages/strategies/09-data-structures.html", nav="2.9 貪心 × 資料結構",
         title="2.9 貪心 × 資料結構",
         desc="並查集找空位、線段樹/BIT 加速貪心決策",
         frag="s2-9.html", group="strategies"),
    dict(id="s10", path="pages/strategies/10-binary-search.html", nav="2.10 貪心 × 二分答案",
         title="2.10 貪心 × 二分答案（參數化貪心）",
         desc="最大化最小值 → 二分答案 + 貪心可行性驗證",
         frag="s2-10.html", group="strategies"),
    dict(id="s11", path="pages/strategies/11-expert.html", nav="2.11 專家專題",
         title="2.11 專家專題",
         desc="擬陣與 Rado–Edmonds 定理、slope trick、模擬費用流",
         frag="s2-11.html", group="strategies"),
    dict(id="pitfalls", path="pages/pitfalls.html", nav="3. 經典「假貪心」陷阱",
         title="經典「假貪心」陷阱",
         desc="五個貪心失效的反例，以及為什麼失敗、正確解法指向",
         frag="s3-pitfalls.html"),
    dict(id="proofs", path="pages/proofs.html", nav="4. 證明方法實戰模板",
         title="證明方法實戰模板",
         desc="交換論證五步驟、領先論證模板，以及對拍驗證器範例碼",
         frag="s4-proofs.html"),
    dict(id="problems", path="pages/problems.html", nav="5. 題目總表（可篩選）",
         title="題目總表（可篩選）",
         desc="58 題可依難度星級、策略標籤與關鍵字篩選的總表",
         frag="s5-problems.html"),
    dict(id="roadmap", path="pages/roadmap.html", nav="6. 學習路線圖",
         title="學習路線圖",
         desc="四階段學習計畫，每階段附代表題與畢業檢定",
         frag="s6-roadmap.html"),
]
BY_ID = {p["id"]: p for p in PAGES}
# 供 content 片段內部超連結使用的舊錨點 → 頁面 id 對照
ANCHOR_TO_ID = {
    "s0": "index", "s1": "theory", "s2-11": "s11",
    "s3": "pitfalls", "s4": "proofs", "s4-3": "proofs#s4-3",
    "s5": "problems", "s6": "roadmap",
}


def rel(current_path, target_path):
    """回傳從 current_path 所在目錄到 target_path 的相對路徑（皆為相對於 greedy-guide/ 根目錄的路徑）。"""
    cur_dir = posixpath.dirname(current_path) or "."
    return posixpath.relpath(target_path, cur_dir)


def fix_cross_refs(html, current_path):
    for anchor, target_id in ANCHOR_TO_ID.items():
        frag = ""
        tid = target_id
        if "#" in target_id:
            tid, frag = target_id.split("#", 1)
            frag = "#" + frag
        target = BY_ID[tid]["path"]
        html = html.replace('href="#%s"' % anchor, 'href="%s%s"' % (rel(current_path, target), frag))
    return html


def render_nav(current_path, current_id):
    out = []
    out.append('<a class="lv1" data-page="index" href="%s">🏠 首頁</a>' % rel(current_path, "index.html"))
    out.append('<a class="lv1" data-page="theory" href="%s">%s</a>' %
                (rel(current_path, BY_ID["theory"]["path"]), BY_ID["theory"]["nav"]))
    out.append('<span class="lv1-label">2. 策略分類</span>')
    for p in PAGES:
        if p.get("group") == "strategies":
            out.append('<a class="lv2" data-page="%s" href="%s">%s</a>' %
                        (p["id"], rel(current_path, p["path"]), p["nav"]))
    for pid in ("pitfalls", "proofs", "problems", "roadmap"):
        p = BY_ID[pid]
        out.append('<a class="lv1" data-page="%s" href="%s">%s</a>' %
                    (pid, rel(current_path, p["path"]), p["nav"]))
    return "\n    ".join(out)


def render_pagenav(current_path, current_id):
    order = [p["id"] for p in PAGES]
    i = order.index(current_id)
    parts = ['<div class="pagenav">']
    if i > 0:
        prev = BY_ID[order[i - 1]]
        label = "首頁" if prev["id"] == "index" else prev["nav"]
        parts.append('<a class="prev" href="%s"><span class="dir">← 上一節</span>%s</a>' %
                      (rel(current_path, prev["path"]), label))
    if i < len(order) - 1:
        nxt = BY_ID[order[i + 1]]
        parts.append('<a class="next" href="%s"><span class="dir">下一節 →</span>%s</a>' %
                      (rel(current_path, nxt["path"]), nxt["nav"]))
    parts.append("</div>")
    return "\n".join(parts)


SETTINGS_PANEL = """
<div id="settingsOverlay" class="settings-overlay" hidden>
  <div class="settings-card" role="dialog" aria-label="顯示設定">
    <div class="settings-card-head">
      <h3>⚙️ 顯示設定</h3>
      <button id="settingsCloseBtn" class="settings-close" aria-label="關閉">✕</button>
    </div>
    <div class="settings-row">
      <span class="settings-label">主題</span>
      <div class="seg" data-group="theme">
        <button data-value="light">☀️ 淺色</button>
        <button data-value="dark">🌙 深色</button>
        <button data-value="system">🖥️ 跟隨系統</button>
      </div>
    </div>
    <div class="settings-row">
      <span class="settings-label">內文字體大小</span>
      <div class="seg" data-group="fontSize">
        <button data-value="sm">小</button>
        <button data-value="md">中</button>
        <button data-value="lg">大</button>
        <button data-value="xl">特大</button>
      </div>
    </div>
    <div class="settings-row">
      <span class="settings-label">版面寬度</span>
      <div class="seg" data-group="width">
        <button data-value="narrow">窄</button>
        <button data-value="normal">預設</button>
        <button data-value="wide">寬</button>
        <button data-value="full">全螢幕</button>
      </div>
    </div>
    <button id="settingsResetBtn" class="settings-reset">還原預設值</button>
  </div>
</div>
""".strip()


def render_page(page, body_html):
    p = page["path"]
    css = rel(p, "assets/site.css")
    js = rel(p, "assets/site.js")
    firebase_cfg = rel(p, "assets/firebase-config.js")
    progress_js = rel(p, "assets/progress.js")
    extra_script = ""
    if page["id"] == "problems":
        data_js = rel(p, "assets/problems-data.js")
        extra_script = '<script src="%s"></script>\n' % data_js

    pagenav = "" if page["id"] == "index" else render_pagenav(p, page["id"])
    full_title = "貪心演算法完全指南" if page["id"] == "index" else (page["title"] + " — 貪心演算法完全指南")

    return """<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="icon" href="{favicon}">
<link rel="stylesheet" href="{css}">
<script src="{js}"></script>
<script src="{firebase_cfg}"></script>
<script src="{progress_js}"></script>
</head>
<body data-page="{pid}">
<div class="layout">

<aside id="sidebar">
  <div class="logo"><a href="{home}">🧭 貪心演算法<span>完全指南</span></a></div>
  <div class="toolbtns">
    <button id="settingsBtn" class="toolbtn">⚙️ 設定</button>
  </div>
  <div id="authBox" class="authbox"></div>
  <nav id="toc">
    {nav}
  </nav>
</aside>
<button id="menuBtn" aria-label="開啟目錄">☰</button>

<main>
{body}
{pagenav}
<footer class="site-footer">
  <p>貪心演算法完全指南 · 純靜態多頁網站 · 無外部依賴 · 深淺色主題自適應</p>
  <p>題目連結指向 LeetCode（力扣）、Codeforces、AtCoder、洛谷、POJ 等原站。</p>
</footer>
</main>
</div>

{settings}
{extra_script}</body>
</html>
""".format(
        title=full_title, desc=page["desc"], favicon=FAVICON, css=css, js=js,
        firebase_cfg=firebase_cfg, progress_js=progress_js,
        pid=page["id"], home=rel(p, "index.html"), nav=render_nav(p, page["id"]),
        body=body_html, pagenav=pagenav, settings=SETTINGS_PANEL, extra_script=extra_script,
    )


def read_frag(name):
    with open(os.path.join(CONTENT_DIR, name), encoding="utf-8") as f:
        return f.read()


def build_index_body():
    cards = []
    cards.append('<a class="topic-card" href="%s"><span class="tc-no">1</span>'
                  '<div class="tc-title">理論基礎</div>'
                  '<div class="tc-desc">%s</div></a>' % (BY_ID["theory"]["path"], BY_ID["theory"]["desc"]))
    for p in PAGES:
        if p.get("group") == "strategies":
            cards.append('<a class="topic-card" href="%s"><span class="tc-no">%s</span>'
                          '<div class="tc-title">%s</div>'
                          '<div class="tc-desc">%s</div></a>' %
                          (p["path"], p["nav"].split(" ")[0], p["nav"], p["desc"]))
    for pid in ("pitfalls", "proofs", "problems", "roadmap"):
        p = BY_ID[pid]
        cards.append('<a class="topic-card" href="%s"><span class="tc-no">%s</span>'
                      '<div class="tc-title">%s</div>'
                      '<div class="tc-desc">%s</div></a>' %
                      (p["path"], pid[0].upper(), p["nav"], p["desc"]))

    intro = read_frag("s0-intro.html")
    return """
<div class="hero">
  <h1>貪心演算法完全指南</h1>
  <p>系統化的策略分類 × 嚴謹的正確性證明 × 60+ 道精選例題，從第一道排序貪心一路打到 slope trick 與模擬費用流。</p>
  <div class="badges">
    <span>★ 入門 → ★★★★★ 專家</span>
    <span>11 大策略分類</span>
    <span>LeetCode / Codeforces / AtCoder / 洛谷 / USACO</span>
  </div>
</div>

{intro}

<h2>快速導覽</h2>
<p class="lede">每個子主題都是獨立頁面，可從側欄或下面的卡片進入；頁尾有「上一節 / 下一節」可依順序閱讀。</p>
<div class="card-grid">
{cards}
</div>
""".format(intro=intro, cards="\n".join(cards))


def main():
    for page in PAGES:
        out_path = os.path.join(ROOT, page["path"])
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        if page["id"] == "index":
            body = build_index_body()
        else:
            body = fix_cross_refs(read_frag(page["frag"]), page["path"])
        html = render_page(page, body)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)
        print("wrote", page["path"])


if __name__ == "__main__":
    main()
