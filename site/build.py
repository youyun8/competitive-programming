#!/usr/bin/env python3
"""
靜態頁面產生器 — 演算法策略圖鑑

用途：把每個「主題」（貪心、DP、……）底下 topics/<id>/content/ 的內容片段
套上共用的版面模板（側欄導覽、主題切換器、設定面板、上一頁/下一頁），輸出
成 site/ 底下的最終靜態頁面；並產生站級的首頁（列出所有主題）與全站題目
總表（合併所有主題的題目、可用主題/難度/標籤/關鍵字篩選）。

CI 不需要執行這支腳本 —— 產生的 .html 檔會直接進版控、GitHub Pages 只是
原樣提供這些靜態檔案。

使用時機：修改任何 topics/<id>/content/*.html 之後，執行：
    python3 build.py
重新產生所有頁面。

新增一個主題（例如「字串演算法」）：
    1. 建立 topics/<新id>/content/*.html（比照既有主題的章節結構）
    2. 在下面的 TOPICS 清單新增一筆 dict（見既有兩筆的欄位）
    3. 在 assets/site.js 的 TOPIC_META 補一筆 {icon, label, short}
    4. 執行 python3 build.py —— 首頁的主題卡片、側欄的主題切換器、全站題目
       總表的主題篩選都會自動出現這個新主題，不需要改動其他任何程式碼
"""
import posixpath
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

SITE_NAME = "演算法策略圖鑑"
FAVICON = (
    'data:image/svg+xml,'
    '<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22>'
    '<text y=%22.9em%22 font-size=%2290%22>%F0%9F%A7%AD</text></svg>'
)

# ── 主題註冊表 ──────────────────────────────────────────────────
# 每個主題是一個獨立的策略分類站中站，共用同一份版面/設定/進度系統。
# pages 欄位結構與舊版單主題 build.py 相同：id, path, nav, title, desc, frag[, group]
TOPICS = [
    dict(
        id="greedy", icon="🧭", short="貪心", name="貪心演算法",
        tagline="從排序貪心到擬陣與模擬費用流的完整策略分類",
        home_desc="從入門到程式競賽專家的貪心演算法策略分類與題目整理",
        pages=[
            dict(id="index", path="topics/greedy/index.html", nav=None, title="首頁", frag=None),
            dict(id="theory", path="topics/greedy/pages/theory.html", nav="1. 理論基礎",
                 title="理論基礎：什麼時候貪心是對的",
                 desc="貪心選擇性質、最優子結構、四大證明技巧與反例構造的系統方法",
                 frag="s1-theory.html"),
            dict(id="s01", path="topics/greedy/pages/strategies/01-sorting.html", nav="2.1 排序貪心",
                 title="2.1 排序貪心（Sort & Sweep）",
                 desc="找到正確排序鍵，排序後線性掃描，決策就變得顯然",
                 frag="s2-1.html", group="strategies"),
            dict(id="s02", path="topics/greedy/pages/strategies/02-intervals.html", nav="2.2 區間問題全家桶",
                 title="2.2 區間問題全家桶（Interval Scheduling Family）",
                 desc="活動選擇、區間覆蓋、區間分組——左右端點排序的完整對照",
                 frag="s2-2.html", group="strategies"),
            dict(id="s03", path="topics/greedy/pages/strategies/03-exchange-scheduling.html", nav="2.3 交換論證排程",
                 title="2.3 交換論證排程（Scheduling by Exchange Argument）",
                 desc="Smith's Rule、Johnson's Rule 與交換論證+DP 的組合套路",
                 frag="s2-3.html", group="strategies"),
            dict(id="s04", path="topics/greedy/pages/strategies/04-regret.html", nav="2.4 反悔貪心",
                 title="2.4 反悔貪心（Regret Greedy）",
                 desc="先貪心接受，再用堆撤銷最差決策的萬用框架",
                 frag="s2-4.html", group="strategies"),
            dict(id="s05", path="topics/greedy/pages/strategies/05-heap.html", nav="2.5 堆積貪心",
                 title="2.5 堆積貪心（Priority-Queue Greedy）",
                 desc="Huffman 編碼、對頂堆與多路歸併",
                 frag="s2-5.html", group="strategies"),
            dict(id="s06", path="topics/greedy/pages/strategies/06-lexicographic.html", nav="2.6 字典序貪心",
                 title="2.6 字典序貪心與單調堆疊構造",
                 desc="逐位確定最小/最大字元，搭配可行性檢查與單調棧實作",
                 frag="s2-6.html", group="strategies"),
            dict(id="s07", path="topics/greedy/pages/strategies/07-math.html", nav="2.7 數學貪心與調整法",
                 title="2.7 數學貪心與調整法",
                 desc="中位數、排序不等式、均值不等式與 canonical 硬幣系統",
                 frag="s2-7.html", group="strategies"),
            dict(id="s08", path="topics/greedy/pages/strategies/08-graph.html", nav="2.8 圖上貪心",
                 title="2.8 圖上貪心",
                 desc="MST 的 Cut/Cycle Property、Dijkstra 正確性邊界、Boruvka",
                 frag="s2-8.html", group="strategies"),
            dict(id="s09", path="topics/greedy/pages/strategies/09-data-structures.html", nav="2.9 貪心 × 資料結構",
                 title="2.9 貪心 × 資料結構",
                 desc="並查集找空位、線段樹/BIT 加速貪心決策",
                 frag="s2-9.html", group="strategies"),
            dict(id="s10", path="topics/greedy/pages/strategies/10-binary-search.html", nav="2.10 貪心 × 二分答案",
                 title="2.10 貪心 × 二分答案（參數化貪心）",
                 desc="最大化最小值 → 二分答案 + 貪心可行性驗證",
                 frag="s2-10.html", group="strategies"),
            dict(id="s11", path="topics/greedy/pages/strategies/11-expert.html", nav="2.11 專家專題",
                 title="2.11 專家專題",
                 desc="擬陣與 Rado–Edmonds 定理、slope trick、模擬費用流",
                 frag="s2-11.html", group="strategies"),
            dict(id="pitfalls", path="topics/greedy/pages/pitfalls.html", nav="3. 經典「假貪心」陷阱",
                 title="經典「假貪心」陷阱",
                 desc="五個貪心失效的反例，以及為什麼失敗、正確解法指向",
                 frag="s3-pitfalls.html"),
            dict(id="proofs", path="topics/greedy/pages/proofs.html", nav="4. 證明方法實戰模板",
                 title="證明方法實戰模板",
                 desc="交換論證五步驟、領先論證模板，以及對拍驗證器範例碼",
                 frag="s4-proofs.html"),
            dict(id="roadmap", path="topics/greedy/pages/roadmap.html", nav="6. 學習路線圖",
                 title="學習路線圖",
                 desc="四階段學習計畫，每階段附代表題與畢業檢定",
                 frag="s6-roadmap.html"),
        ],
        # 主題內部錨點（content 片段用 href="#s2-1" 這種寫法互相引用）→ 頁面 id
        anchor_to_id={
            "s1": "theory", "s2-11": "s11",
            "s3": "pitfalls", "s4": "proofs", "s4-3": "proofs#s4-3",
            "s6": "roadmap",
        },
    ),
    dict(
        id="dp", icon="📈", short="DP", name="動態規劃",
        tagline="13 大策略分類、狀態設計方法論與 DP 優化技術全解",
        home_desc="從入門到程式競賽專家的動態規劃策略分類與題目整理",
        pages=[
            dict(id="index", path="topics/dp/index.html", nav=None, title="首頁", frag=None),
            dict(id="theory", path="topics/dp/pages/theory.html", nav="1. 理論基礎",
                 title="理論基礎：DP 思考框架",
                 desc="三大前提、解題六步驟、記憶化 vs 遞推、複雜度反推狀態設計",
                 frag="s1-theory.html"),
            dict(id="s01", path="topics/dp/pages/strategies/01-linear.html", nav="2.1 線性 DP",
                 title="2.1 線性 DP（入門三件套與 LIS 家族）",
                 desc="「前 i 個」與「以 i 結尾」兩種視角，從爬樓梯到 LIS 二維偏序",
                 frag="s2-1.html", group="strategies"),
            dict(id="s02", path="topics/dp/pages/strategies/02-grid.html", nav="2.2 網格與座標 DP",
                 title="2.2 網格與座標 DP",
                 desc="路徑計數、倒推設計（地下城）與雙路徑同步（方格取數）",
                 frag="s2-2.html", group="strategies"),
            dict(id="s03", path="topics/dp/pages/strategies/03-knapsack.html", nav="2.3 背包全家桶",
                 title="2.3 背包全家桶（背包九講精華）",
                 desc="0/1、完全、多重、分組、依賴、二維費用、計數與退背包",
                 frag="s2-3.html", group="strategies"),
            dict(id="s04", path="topics/dp/pages/strategies/04-interval.html", nav="2.4 區間 DP",
                 title="2.4 區間 DP",
                 desc="石子合併、迴文、戳氣球的「枚舉最後一步」與狀態加維",
                 frag="s2-4.html", group="strategies"),
            dict(id="s05", path="topics/dp/pages/strategies/05-two-sequences.html", nav="2.5 雙序列 DP",
                 title="2.5 雙序列 DP",
                 desc="LCS、編輯距離、子序列計數與萬用字元/正則匹配",
                 frag="s2-5.html", group="strategies"),
            dict(id="s06", path="topics/dp/pages/strategies/06-state-machine.html", nav="2.6 狀態機 DP",
                 title="2.6 狀態機 DP",
                 desc="股票系列全解、KMP 自動機上的計數與矩陣冪",
                 frag="s2-6.html", group="strategies"),
            dict(id="s07", path="topics/dp/pages/strategies/07-bitmask.html", nav="2.7 位元狀壓 DP",
                 title="2.7 位元狀壓 DP",
                 desc="集合推進型與行輪廓型：TSP、配對計數、棋盤放置",
                 frag="s2-7.html", group="strategies"),
            dict(id="s08", path="topics/dp/pages/strategies/08-tree.html", nav="2.8 樹上 DP",
                 title="2.8 樹上 DP",
                 desc="樹上獨立集、樹上背包、換根 DP 與覆蓋三態",
                 frag="s2-8.html", group="strategies"),
            dict(id="s09", path="topics/dp/pages/strategies/09-digit.html", nav="2.9 數位 DP",
                 title="2.9 數位 DP",
                 desc="tight/lead 兩面旗的統一模板，windy 數到 mod 2520 壓縮",
                 frag="s2-9.html", group="strategies"),
            dict(id="s10", path="topics/dp/pages/strategies/10-counting-expectation.html", nav="2.10 計數與期望 DP",
                 title="2.10 計數 DP 與期望 DP",
                 desc="不重不漏的計數、逆推期望、對稱性壓縮與二次期望",
                 frag="s2-10.html", group="strategies"),
            dict(id="s11", path="topics/dp/pages/strategies/11-graph-game.html", nav="2.11 圖上與博弈 DP",
                 title="2.11 圖上 DP 與博弈 DP",
                 desc="DAG 拓撲序、SCC 縮點、分層圖與 minimax 差值博弈",
                 frag="s2-11.html", group="strategies"),
            dict(id="s12", path="topics/dp/pages/strategies/12-optimization.html", nav="2.12 DP 優化技術",
                 title="2.12 DP 優化技術（競賽分水嶺）",
                 desc="前綴和、單調佇列、斜率優化、Knuth、分治、wqs 二分、矩陣冪、bitset",
                 frag="s2-12.html", group="strategies"),
            dict(id="s13", path="topics/dp/pages/strategies/13-expert.html", nav="2.13 專家專題",
                 title="2.13 專家專題",
                 desc="輪廓線/插頭 DP、SOS、連通塊插入、動態 DP、DP 套 DP",
                 frag="s2-13.html", group="strategies"),
            dict(id="pitfalls", path="topics/dp/pages/pitfalls.html", nav="3. 常見錯誤與除錯",
                 title="常見錯誤與除錯（假 DP 教材）",
                 desc="後效性、背包方向、恰好裝滿、狀態不完整——高頻坑與修法",
                 frag="s3-pitfalls.html"),
            dict(id="method", path="topics/dp/pages/method.html", nav="4. 狀態設計方法論",
                 title="狀態設計實戰方法論",
                 desc="從暴力遞迴機械化推導 DP、四視角、降維清單與對拍驗證器",
                 frag="s4-method.html"),
            dict(id="roadmap", path="topics/dp/pages/roadmap.html", nav="6. 學習路線圖",
                 title="學習路線圖",
                 desc="四階段學習計畫，每階段附代表題與畢業檢定",
                 frag="s6-roadmap.html"),
        ],
        anchor_to_id={
            "s1": "theory",
            "s2-1": "s01", "s2-2": "s02", "s2-3": "s03", "s2-4": "s04",
            "s2-5": "s05", "s2-6": "s06", "s2-7": "s07", "s2-8": "s08",
            "s2-9": "s09", "s2-10": "s10", "s2-11": "s11", "s2-12": "s12",
            "s2-13": "s13",
            "s3": "pitfalls", "s4": "method", "s6": "roadmap",
        },
    ),
]
TOPIC_BY_ID = {t["id"]: t for t in TOPICS}
for _t in TOPICS:
    _t["page_by_id"] = {p["id"]: p for p in _t["pages"]}

# 站級（不屬於任何單一主題）的頁面
GLOBAL_PAGES = {
    "problems": dict(id="problems", path="pages/problems.html"),
}


def rel(current_path, target_path):
    """回傳從 current_path 所在目錄到 target_path 的相對路徑（皆為相對於 site/ 根目錄的路徑）。"""
    cur_dir = posixpath.dirname(current_path) or "."
    return posixpath.relpath(target_path, cur_dir)


def fix_cross_refs(html, current_path, topic):
    """解析 content 片段裡的三種內部連結寫法：
       #s2-1 等章節錨點 → 該主題內對應頁面（含 proofs#s4-3 這種帶頁內片段的特例）
       #problems        → 全站題目總表
       #topic-<id>       → 另一個主題的首頁（主題間互相引用）
    """
    for anchor, target in topic["anchor_to_id"].items():
        frag = ""
        tid = target
        if "#" in target:
            tid, frag = target.split("#", 1)
            frag = "#" + frag
        page = topic["page_by_id"][tid]
        html = html.replace('href="#%s"' % anchor, 'href="%s%s"' % (rel(current_path, page["path"]), frag))
    html = html.replace('href="#problems"', 'href="%s"' % rel(current_path, GLOBAL_PAGES["problems"]["path"]))
    for other in TOPICS:
        home = other["page_by_id"]["index"]
        html = html.replace('href="#topic-%s"' % other["id"], 'href="%s"' % rel(current_path, home["path"]))
    return html


def render_topic_switcher(current_path, active_topic_id):
    out = ['<div id="topicSwitcher">']
    for t in TOPICS:
        home = t["page_by_id"]["index"]
        cls = "active" if t["id"] == active_topic_id else ""
        out.append('<a class="%s" data-topic="%s" href="%s">%s %s</a>' %
                    (cls, t["id"], rel(current_path, home["path"]), t["icon"], t["short"]))
    out.append("</div>")
    return "\n    ".join(out)


def render_nav(current_path, topic):
    """側欄章節導覽：只列出「目前所在主題」的章節（首頁與全站題目總表不屬於任何主題，不顯示這一段）。"""
    if topic is None:
        return ""
    out = []
    home = topic["page_by_id"]["index"]
    out.append('<a class="lv1" data-page="index" href="%s">🏠 %s 首頁</a>' % (rel(current_path, home["path"]), topic["name"]))
    theory = topic["page_by_id"].get("theory")
    if theory:
        out.append('<a class="lv1" data-page="theory" href="%s">%s</a>' % (rel(current_path, theory["path"]), theory["nav"]))
    out.append('<span class="lv1-label">2. 策略分類</span>')
    for p in topic["pages"]:
        if p.get("group") == "strategies":
            out.append('<a class="lv2" data-page="%s" href="%s">%s</a>' % (p["id"], rel(current_path, p["path"]), p["nav"]))
    for pid in ("pitfalls", "proofs", "method", "roadmap"):
        p = topic["page_by_id"].get(pid)
        if p:
            out.append('<a class="lv1" data-page="%s" href="%s">%s</a>' % (pid, rel(current_path, p["path"]), p["nav"]))
    return "\n    ".join(out)


def render_pagenav(current_path, topic, current_id):
    order = [p["id"] for p in topic["pages"]]
    i = order.index(current_id)
    parts = ['<div class="pagenav">']
    if i > 0:
        prev = topic["page_by_id"][order[i - 1]]
        label = ("🏠 " + topic["name"] + " 首頁") if prev["id"] == "index" else prev["nav"]
        parts.append('<a class="prev" href="%s"><span class="dir">← 上一節</span>%s</a>' %
                      (rel(current_path, prev["path"]), label))
    if i < len(order) - 1:
        nxt = topic["page_by_id"][order[i + 1]]
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
      <span class="settings-label">側欄字體大小</span>
      <div class="seg" data-group="sidebarFontSize">
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


def render_shell(path, page_id, title, desc, topic, body_html, pagenav_html=""):
    """所有頁面（站級首頁／題目總表／各主題的頁面）共用的最外層版面骨架。"""
    css = rel(path, "assets/site.css")
    js = rel(path, "assets/site.js")
    math_config = rel(path, "assets/math-config.js")
    supabase_cfg = rel(path, "assets/supabase-config.js")
    progress_js = rel(path, "assets/progress.js")
    extra_script = ""
    if page_id == "problems":
        extra_script = '<script src="%s"></script>\n' % rel(path, "assets/problems-data.js")

    # 站級首頁（topic is None）標題就是站名；主題首頁與其他頁面一律帶上站名當後綴，
    # 否則不同主題的首頁分頁標題會一模一樣，瀏覽器分頁/書籤都分不出是哪個主題。
    full_title = SITE_NAME if (page_id == "index" and topic is None) else (title + " — " + SITE_NAME)
    topic_attr = ' data-topic="%s"' % topic["id"] if topic else ""
    # 從主題頁面點「全站題目總表」時帶上 #topic=<id>，讓總表預先篩選成目前主題（仍可手動清除篩選）
    problems_href = rel(path, GLOBAL_PAGES["problems"]["path"])
    if topic and page_id != "problems":
        problems_href += "#topic=" + topic["id"]

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
<script src="{math_config}"></script>
<script defer src="https://cdn.jsdelivr.net/npm/mathjax@4/tex-chtml.js"></script>
<script src="{supabase_cfg}"></script>
<script src="{progress_js}"></script>
</head>
<body data-page="{pid}"{topic_attr}>
<div class="layout">

<aside id="sidebar">
  <div class="logo"><a href="{home}">🧭 {site_name}</a></div>
  <div class="toolbtns">
    <button id="settingsBtn" class="toolbtn">⚙️ 設定</button>
  </div>
  <div id="authBox" class="authbox"></div>
  <span class="lv1-label">主題</span>
  {switcher}
  <a class="sitewide" href="{problems}"><span class="sitewide-icon" aria-hidden="true">📋</span><span>全站題目總表</span></a>
  <hr class="sidebar-divider">
  <nav id="toc">
    {nav}
  </nav>
</aside>
<button id="sidebarToggle" class="sidebar-toggle" type="button"
        aria-label="收合側欄" aria-expanded="true" title="收合側欄">‹</button>
<button id="menuBtn" aria-label="開啟目錄" aria-expanded="false">☰</button>

<main>
{body}
{pagenav}
<footer class="site-footer">
  <p>題目連結指向 LeetCode（力扣）、Codeforces、AtCoder、洛谷、POJ 等原站。</p>
</footer>
</main>
</div>

{settings}
{extra_script}</body>
</html>
""".format(
        title=full_title, desc=desc, favicon=FAVICON, css=css, js=js,
        math_config=math_config,
        supabase_cfg=supabase_cfg, progress_js=progress_js, pid=page_id, topic_attr=topic_attr,
        home=rel(path, "index.html"), site_name=SITE_NAME,
        switcher=render_topic_switcher(path, topic["id"] if topic else None),
        problems=problems_href,
        nav=render_nav(path, topic), body=body_html, pagenav=pagenav_html,
        settings=SETTINGS_PANEL, extra_script=extra_script,
    )


def read_frag(topic, name):
    with open(os.path.join(ROOT, "topics", topic["id"], "content", name), encoding="utf-8") as f:
        return f.read()


def build_topic_index_body(topic):
    home_path = topic["page_by_id"]["index"]["path"]
    cards = []
    theory = topic["page_by_id"].get("theory")
    if theory:
        cards.append('<a class="topic-card" href="%s"><span class="tc-no">1</span>'
                      '<div class="tc-title">理論基礎</div>'
                      '<div class="tc-desc">%s</div></a>' % (rel(home_path, theory["path"]), theory["desc"]))
    for p in topic["pages"]:
        if p.get("group") == "strategies":
            cards.append('<a class="topic-card" href="%s"><span class="tc-no">%s</span>'
                          '<div class="tc-title">%s</div>'
                          '<div class="tc-desc">%s</div></a>' %
                          (rel(home_path, p["path"]), p["nav"].split(" ")[0], p["nav"], p["desc"]))
    for pid in ("pitfalls", "proofs", "method", "roadmap"):
        p = topic["page_by_id"].get(pid)
        if not p:
            continue
        label = pid[0].upper() if pid != "roadmap" else "6"
        cards.append('<a class="topic-card" href="%s"><span class="tc-no">%s</span>'
                      '<div class="tc-title">%s</div>'
                      '<div class="tc-desc">%s</div></a>' % (rel(home_path, p["path"]), label, p["nav"], p["desc"]))

    intro = fix_cross_refs(read_frag(topic, "s0-intro.html"), home_path, topic)
    return """
<div class="hero">
  <h1>{icon} {name}</h1>
  <p>{home_desc}</p>
  <div class="badges">
    <span>★ 入門 → ★★★★★ 專家</span>
    <span>{n_strat} 大策略分類</span>
    <span>LeetCode / Codeforces / AtCoder / 洛谷 / POJ</span>
  </div>
</div>

{intro}

<h2>快速導覽</h2>
<p class="lede">每個子主題都是獨立頁面，可從側欄或下面的卡片進入；頁尾有「上一節 / 下一節」可依順序閱讀。</p>
<div class="card-grid">
{cards}
</div>
""".format(icon=topic["icon"], name=topic["name"], home_desc=topic["home_desc"],
           n_strat=sum(1 for p in topic["pages"] if p.get("group") == "strategies"),
           intro=intro, cards="\n".join(cards))


def count_problems():
    """從 assets/problems-data.js 數一下總題數，只用來在首頁 hero 顯示，不影響其他邏輯。"""
    path = os.path.join(ROOT, "assets", "problems-data.js")
    if not os.path.exists(path):
        return 0
    text = open(path, encoding="utf-8").read()
    return sum(1 for line in text.splitlines() if line.strip().startswith('["'))


def build_site_index_body():
    cards = []
    for t in TOPICS:
        home = t["page_by_id"]["index"]
        cards.append(
            '<a class="topic-hero-card" href="%s">'
            '<div class="th-icon">%s</div>'
            '<div class="th-title">%s</div>'
            '<div class="th-desc">%s</div>'
            '<div class="th-cta">進入主題 →</div>'
            '</a>' % (home["path"], t["icon"], t["name"], t["tagline"])
        )
    cards.append(
        '<div class="topic-hero-card topic-future">'
        '<div class="th-icon">✨</div>'
        '<div class="th-title">更多主題陸續加入中</div>'
        '<div class="th-desc">字串演算法、資料結構專題、圖論……歡迎期待，站內架構已為擴充做好準備。</div>'
        '</div>'
    )
    return """
<div class="hero">
  <h1>{site_name}</h1>
  <p>一套統一的介面，收錄程式競賽各大演算法主題的策略分類與題目整理 —— 每個主題都是從入門（★）到程式競賽專家（★★★★★）的完整攻略，共用同一份顯示設定與練習進度追蹤，之後新增主題也不需要另外做介面。</p>
  <div class="badges">
    <span>{n_topics} 個主題，持續擴充</span>
    <span>{n_problems} 題全站題目總表</span>
    <span>LeetCode / Codeforces / AtCoder / 洛谷 / POJ</span>
  </div>
</div>

<h2>選擇一個主題開始</h2>
<p class="lede">點進任一主題後，側欄會出現該主題的完整章節目錄；隨時可用側欄上方的「主題」切換器換到另一個主題，兩邊的顯示設定與練習進度完全共用。</p>
<div class="topic-grid">
{cards}
</div>

<h2>全站題目總表</h2>
<p class="lede home-problems-lede">不想按章節讀，直接刷題也可以 —— <a href="{problems}">全站題目總表</a>橫跨所有主題，可依主題、難度星級、策略標籤與關鍵字篩選。</p>
""".format(site_name=SITE_NAME, n_topics=len(TOPICS), n_problems=count_problems(),
           cards="\n".join(cards), problems=GLOBAL_PAGES["problems"]["path"])


PROBLEMS_PAGE_BODY = """
<h2>題目總表（可篩選）</h2>
<p>共 <b id="ptbl-total"></b> 題，橫跨全站所有主題。點擊主題／星級／標籤可篩選（可複選），輸入關鍵字可搜尋題名與想法。</p>
<p id="progress-summary" class="small"></p>

<div class="callout when"><b>📶 練習進度同步</b>
<p>每題右側可標記「尚未練習 ⬜ / 需複習 🔶 / 已通過 ✅」。登入後（見側欄）進度會同步到雲端，換裝置登入同一帳號會看到相同紀錄；未登入時進度只存在目前瀏覽器。同一題若在多個主題都有出現，標記一次、所有地方都會同步。</p></div>

<div class="filterbar">
  <input id="f-text" type="search" placeholder="🔍 搜尋題名 / 來源 / 關鍵想法…">
  <div class="row"><span class="lbl">主題</span><span id="f-topics"></span></div>
  <div class="row"><span class="lbl">難度</span><span id="f-stars"></span></div>
  <div class="row"><span class="lbl">標籤</span><span id="f-tags"></span></div>
  <div class="row"><span id="ptbl-count"></span></div>
</div>

<div class="tbl-wrap"><table id="ptbl">
  <thead><tr><th>題目</th><th>主題</th><th>來源</th><th>難度</th><th>標籤</th><th>關鍵想法</th><th>進度</th></tr></thead>
  <tbody></tbody>
</table></div>
"""


def main():
    for topic in TOPICS:
        for page in topic["pages"]:
            out_path = os.path.join(ROOT, page["path"])
            os.makedirs(os.path.dirname(out_path), exist_ok=True)
            if page["id"] == "index":
                body = build_topic_index_body(topic)
                pagenav = render_pagenav(page["path"], topic, page["id"])
                title, desc = topic["name"], topic["home_desc"]
            else:
                body = fix_cross_refs(read_frag(topic, page["frag"]), page["path"], topic)
                pagenav = render_pagenav(page["path"], topic, page["id"])
                title, desc = page["title"], page["desc"]
            html = render_shell(page["path"], page["id"], title, desc, topic, body, pagenav)
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(html)
            print("wrote", page["path"])

    problems_path = GLOBAL_PAGES["problems"]["path"]
    out_path = os.path.join(ROOT, problems_path)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(render_shell(problems_path, "problems", "全站題目總表",
                              "橫跨所有主題、可依主題／難度星級／策略標籤／關鍵字篩選的題目總表",
                              None, PROBLEMS_PAGE_BODY))
    print("wrote", problems_path)

    index_path = "index.html"
    with open(os.path.join(ROOT, index_path), "w", encoding="utf-8") as f:
        f.write(render_shell(index_path, "index", SITE_NAME,
                              "一套統一介面收錄的程式競賽演算法策略分類與題目整理站", None, build_site_index_body()))
    print("wrote", index_path)


if __name__ == "__main__":
    main()
