#!/usr/bin/env python3
"""
靜態頁面產生器 — DP 上分攻略

用途：把 content/ 目錄下的內容片段（每個子主題一個 .html 檔）套上共用的
版面模板（側欄導覽、設定面板、上一頁/下一頁），輸出成 dp-guide/ 底下
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
    '<text y=%22.9em%22 font-size=%2290%22>%F0%9F%93%88</text></svg>'
)

SITE_NAME = "DP 上分攻略"

# ── 頁面登記表 ──────────────────────────────────────────────────
# id, path (相對於 dp-guide/ 根目錄), nav 標題, 卡片描述, 內容片段檔名
PAGES = [
    dict(id="index", path="index.html", nav=None, title="首頁",
         desc="從入門到程式競賽專家的動態規劃策略分類與競程題單", frag=None),
    dict(id="theory", path="pages/theory.html", nav="1. 理論基礎",
         title="理論基礎：DP 思考框架",
         desc="三大前提、解題六步驟、記憶化 vs 遞推、複雜度反推狀態設計",
         frag="s1-theory.html"),
    dict(id="s01", path="pages/strategies/01-linear.html", nav="2.1 線性 DP",
         title="2.1 線性 DP（入門三件套與 LIS 家族）",
         desc="「前 i 個」與「以 i 結尾」兩種視角，從爬樓梯到 LIS 二維偏序",
         frag="s2-1.html", group="strategies"),
    dict(id="s02", path="pages/strategies/02-grid.html", nav="2.2 網格與座標 DP",
         title="2.2 網格與座標 DP",
         desc="路徑計數、倒推設計（地下城）與雙路徑同步（方格取數）",
         frag="s2-2.html", group="strategies"),
    dict(id="s03", path="pages/strategies/03-knapsack.html", nav="2.3 背包全家桶",
         title="2.3 背包全家桶（背包九講精華）",
         desc="0/1、完全、多重、分組、依賴、二維費用、計數與退背包",
         frag="s2-3.html", group="strategies"),
    dict(id="s04", path="pages/strategies/04-interval.html", nav="2.4 區間 DP",
         title="2.4 區間 DP",
         desc="石子合併、迴文、戳氣球的「枚舉最後一步」與狀態加維",
         frag="s2-4.html", group="strategies"),
    dict(id="s05", path="pages/strategies/05-two-sequences.html", nav="2.5 雙序列 DP",
         title="2.5 雙序列 DP",
         desc="LCS、編輯距離、子序列計數與萬用字元/正則匹配",
         frag="s2-5.html", group="strategies"),
    dict(id="s06", path="pages/strategies/06-state-machine.html", nav="2.6 狀態機 DP",
         title="2.6 狀態機 DP",
         desc="股票系列全解、KMP 自動機上的計數與矩陣冪",
         frag="s2-6.html", group="strategies"),
    dict(id="s07", path="pages/strategies/07-bitmask.html", nav="2.7 位元狀壓 DP",
         title="2.7 位元狀壓 DP",
         desc="集合推進型與行輪廓型：TSP、配對計數、棋盤放置",
         frag="s2-7.html", group="strategies"),
    dict(id="s08", path="pages/strategies/08-tree.html", nav="2.8 樹上 DP",
         title="2.8 樹上 DP",
         desc="樹上獨立集、樹上背包、換根 DP 與覆蓋三態",
         frag="s2-8.html", group="strategies"),
    dict(id="s09", path="pages/strategies/09-digit.html", nav="2.9 數位 DP",
         title="2.9 數位 DP",
         desc="tight/lead 兩面旗的統一模板，windy 數到 mod 2520 壓縮",
         frag="s2-9.html", group="strategies"),
    dict(id="s10", path="pages/strategies/10-counting-expectation.html", nav="2.10 計數與期望 DP",
         title="2.10 計數 DP 與期望 DP",
         desc="不重不漏的計數、逆推期望、對稱性壓縮與二次期望",
         frag="s2-10.html", group="strategies"),
    dict(id="s11", path="pages/strategies/11-graph-game.html", nav="2.11 圖上與博弈 DP",
         title="2.11 圖上 DP 與博弈 DP",
         desc="DAG 拓撲序、SCC 縮點、分層圖與 minimax 差值博弈",
         frag="s2-11.html", group="strategies"),
    dict(id="s12", path="pages/strategies/12-optimization.html", nav="2.12 DP 優化技術",
         title="2.12 DP 優化技術（競賽分水嶺）",
         desc="前綴和、單調佇列、斜率優化、Knuth、分治、wqs 二分、矩陣冪、bitset",
         frag="s2-12.html", group="strategies"),
    dict(id="s13", path="pages/strategies/13-expert.html", nav="2.13 專家專題",
         title="2.13 專家專題",
         desc="輪廓線/插頭 DP、SOS、連通塊插入、動態 DP、DP 套 DP",
         frag="s2-13.html", group="strategies"),
    dict(id="pitfalls", path="pages/pitfalls.html", nav="3. 常見錯誤與除錯",
         title="常見錯誤與除錯（假 DP 教材）",
         desc="後效性、背包方向、恰好裝滿、狀態不完整——高頻坑與修法",
         frag="s3-pitfalls.html"),
    dict(id="method", path="pages/method.html", nav="4. 狀態設計方法論",
         title="狀態設計實戰方法論",
         desc="從暴力遞迴機械化推導 DP、四視角、降維清單與對拍驗證器",
         frag="s4-method.html"),
    dict(id="problems", path="pages/problems.html", nav="5. 題目總表（可篩選）",
         title="題目總表（可篩選）",
         desc="86 題可依難度星級、策略標籤與關鍵字篩選的總表",
         frag="s5-problems.html"),
    dict(id="roadmap", path="pages/roadmap.html", nav="6. 學習路線圖",
         title="學習路線圖",
         desc="四階段學習計畫，每階段附代表題與畢業檢定",
         frag="s6-roadmap.html"),
]
BY_ID = {p["id"]: p for p in PAGES}
# 供 content 片段內部超連結使用的錨點 → 頁面 id 對照
ANCHOR_TO_ID = {
    "s1": "theory",
    "s2-1": "s01", "s2-2": "s02", "s2-3": "s03", "s2-4": "s04",
    "s2-5": "s05", "s2-6": "s06", "s2-7": "s07", "s2-8": "s08",
    "s2-9": "s09", "s2-10": "s10", "s2-11": "s11", "s2-12": "s12",
    "s2-13": "s13",
    "s3": "pitfalls", "s4": "method", "s5": "problems", "s6": "roadmap",
}
# 特殊錨點：連到姊妹站（貪心指南，部署於網站根目錄、即 dp-guide/ 的上一層）
GREEDY_HOME = "../index.html"


def rel(current_path, target_path):
    """回傳從 current_path 所在目錄到 target_path 的相對路徑（皆為相對於 dp-guide/ 根目錄的路徑）。"""
    cur_dir = posixpath.dirname(current_path) or "."
    return posixpath.relpath(target_path, cur_dir)


def fix_cross_refs(html, current_path):
    for anchor, target_id in ANCHOR_TO_ID.items():
        target = BY_ID[target_id]["path"]
        html = html.replace('href="#%s"' % anchor, 'href="%s"' % rel(current_path, target))
    html = html.replace('href="#greedy"', 'href="%s"' % rel(current_path, GREEDY_HOME))
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
    for pid in ("pitfalls", "method", "problems", "roadmap"):
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
    full_title = SITE_NAME if page["id"] == "index" else (page["title"] + " — " + SITE_NAME)

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
  <div class="logo"><a href="{home}">📈 DP 上分攻略<span>動態規劃 × 競程題單</span></a></div>
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
  <p>DP 上分攻略 · 純靜態多頁網站 · 無外部依賴 · 深淺色主題自適應</p>
  <p>題目連結指向 LeetCode（力扣）、Codeforces、AtCoder、洛谷、POJ 等原站。姊妹站：<a href="{greedy}">貪心演算法完全指南</a>。</p>
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
        greedy=rel(p, GREEDY_HOME),
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
    for pid in ("pitfalls", "method", "problems", "roadmap"):
        p = BY_ID[pid]
        cards.append('<a class="topic-card" href="%s"><span class="tc-no">%s</span>'
                      '<div class="tc-title">%s</div>'
                      '<div class="tc-desc">%s</div></a>' %
                      (p["path"], pid[0].upper(), p["nav"], p["desc"]))

    intro = fix_cross_refs(read_frag("s0-intro.html"), "index.html")
    return """
<div class="hero">
  <h1>DP 上分攻略</h1>
  <p>動態規劃策略分類 × 競程題單。13 大策略分類 × 系統化的狀態設計方法論 × 86 道精選例題，從第一道爬樓梯一路打到插頭 DP 與 DP 套 DP。</p>
  <div class="badges">
    <span>★ 入門 → ★★★★★ 專家</span>
    <span>13 大策略分類</span>
    <span>LeetCode / Codeforces / AtCoder / 洛谷 / POJ</span>
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
        os.makedirs(os.path.dirname(out_path) or ROOT, exist_ok=True)
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
