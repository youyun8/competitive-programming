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
    dict(
        id="strings", icon="🔤", short="字串", name="字串演算法",
        tagline="從雜湊與 KMP 到後綴自動機的完整策略分類",
        home_desc="從入門到程式競賽專家的字串演算法策略分類與題目整理",
        pages=[
            dict(id="index", path="topics/strings/index.html", nav=None, title="首頁", frag=None),
            dict(id="theory", path="topics/strings/pages/theory.html", nav="1. 理論基礎",
                 title="理論基礎：字串的共同語言",
                 desc="border 與週期的核心等式、三種匹配思維、複雜度反推與實作工具箱",
                 frag="s1-theory.html"),
            dict(id="s01", path="topics/strings/pages/strategies/01-hashing.html", nav="2.1 字串雜湊",
                 title="2.1 字串雜湊（Polynomial Hashing）",
                 desc="O(1) 子串比較、防卡雙模數、hash+二分求 LCP",
                 frag="s2-1.html", group="strategies"),
            dict(id="s02", path="topics/strings/pages/strategies/02-kmp.html", nav="2.2 KMP 與週期",
                 title="2.2 KMP、失配函數與週期",
                 desc="fail 鏈 = 所有 border、最小週期 n−fail[n]、KMP 自動機",
                 frag="s2-2.html", group="strategies"),
            dict(id="s03", path="topics/strings/pages/strategies/03-z-function.html", nav="2.3 Z 函數",
                 title="2.3 Z 函數（擴展 KMP）",
                 desc="Z-box 線性構造、exkmp、Z 與 fail 的方向對照",
                 frag="s2-3.html", group="strategies"),
            dict(id="s04", path="topics/strings/pages/strategies/04-manacher.html", nav="2.4 Manacher",
                 title="2.4 Manacher（線性迴文半徑）",
                 desc="插 # 統一奇偶、鏡像繼承、迴文計數與拼接應用",
                 frag="s2-4.html", group="strategies"),
            dict(id="s05", path="topics/strings/pages/strategies/05-trie.html", nav="2.5 Trie 與 01-Trie",
                 title="2.5 Trie 與 01-Trie",
                 desc="前綴樹、逐位貪心求最大 XOR、樹上路徑 XOR 轉化",
                 frag="s2-5.html", group="strategies"),
            dict(id="s06", path="topics/strings/pages/strategies/06-aho-corasick.html", nav="2.6 AC 自動機",
                 title="2.6 AC 自動機（多模式匹配）",
                 desc="Trie 圖、fail 樹子樹和、自動機上 DP",
                 frag="s2-6.html", group="strategies"),
            dict(id="s07", path="topics/strings/pages/strategies/07-suffix-array.html", nav="2.7 後綴數組",
                 title="2.7 後綴數組（Suffix Array）",
                 desc="倍增構造、height 陣列與 LCP Lemma、去重與分組應用",
                 frag="s2-7.html", group="strategies"),
            dict(id="s08", path="topics/strings/pages/strategies/08-sam.html", nav="2.8 後綴自動機",
                 title="2.8 後綴自動機（SAM）",
                 desc="endpos 等價類、parent 樹、線上構造與應用地圖",
                 frag="s2-8.html", group="strategies"),
            dict(id="s09", path="topics/strings/pages/strategies/09-pam.html", nav="2.9 迴文自動機",
                 title="2.9 迴文自動機（PAM／迴文樹）",
                 desc="本質不同迴文至多 n 個、雙根增量構造、出現次數統計",
                 frag="s2-9.html", group="strategies"),
            dict(id="s10", path="topics/strings/pages/strategies/10-lyndon.html", nav="2.10 最小表示與 Lyndon",
                 title="2.10 最小表示法與 Lyndon 分解",
                 desc="雙指標批量淘汰、Duval 演算法、最小後綴",
                 frag="s2-10.html", group="strategies"),
            dict(id="s11", path="topics/strings/pages/strategies/11-expert.html", nav="2.11 專家專題",
                 title="2.11 專家專題",
                 desc="失配樹、廣義 SAM、SAM×線段樹合併、border 理論、位平行",
                 frag="s2-11.html", group="strategies"),
            dict(id="pitfalls", path="topics/strings/pages/pitfalls.html", nav="3. 常見錯誤與陷阱",
                 title="常見錯誤與陷阱",
                 desc="hash 被卡全家桶、下標制混用、統計順序、多測清空——高頻坑與修法",
                 frag="s3-pitfalls.html"),
            dict(id="method", path="topics/strings/pages/method.html", nav="4. 模板整理與選型",
                 title="模板整理與選型方法論",
                 desc="選型決策樹、一題三解對照、模板風格約定與對拍驗證器",
                 frag="s4-method.html"),
            dict(id="roadmap", path="topics/strings/pages/roadmap.html", nav="6. 學習路線圖",
                 title="學習路線圖",
                 desc="四階段學習計畫，每階段附代表題與畢業檢定",
                 frag="s6-roadmap.html"),
        ],
        anchor_to_id={
            "s1": "theory",
            "s2-1": "s01", "s2-2": "s02", "s2-3": "s03", "s2-4": "s04",
            "s2-5": "s05", "s2-6": "s06", "s2-7": "s07", "s2-8": "s08",
            "s2-9": "s09", "s2-10": "s10", "s2-11": "s11",
            "s3": "pitfalls", "s4": "method", "s6": "roadmap",
        },
    ),
    dict(
        id="ds", icon="🧱", short="資結", name="競賽資料結構",
        tagline="從前綴和與 BIT 到吉司機線段樹與 LCT 的完整策略分類",
        home_desc="從入門到程式競賽專家的競賽資料結構策略分類與題目整理",
        pages=[
            dict(id="index", path="topics/ds/index.html", nav=None, title="首頁", frag=None),
            dict(id="theory", path="topics/ds/pages/theory.html", nav="1. 理論基礎",
                 title="理論基礎：維護增量的思考框架",
                 desc="操作分析法、可合併性、均攤與勢能、離線 vs 線上、複雜度預算",
                 frag="s1-theory.html"),
            dict(id="s01", path="topics/ds/pages/strategies/01-prefix-sums.html", nav="2.1 前綴和・差分・ST 表",
                 title="2.1 前綴和、差分與 ST 表（靜態的力量）",
                 desc="預處理換查詢：一維/二維前綴和、差分打點、可重複貢獻 RMQ",
                 frag="s2-1.html", group="strategies"),
            dict(id="s02", path="topics/ds/pages/strategies/02-monotonic.html", nav="2.2 單調堆疊與單調佇列",
                 title="2.2 單調堆疊與單調佇列",
                 desc="維護有用候選人：下一個更大元素、滑窗最值、均攤 O(n)",
                 frag="s2-2.html", group="strategies"),
            dict(id="s03", path="topics/ds/pages/strategies/03-heap.html", nav="2.3 堆與對頂堆",
                 title="2.3 堆、對頂堆與可刪堆",
                 desc="動態中位數、懶惰刪除、multiset 的替代範圍",
                 frag="s2-3.html", group="strategies"),
            dict(id="s04", path="topics/ds/pages/strategies/04-dsu.html", nav="2.4 並查集",
                 title="2.4 並查集（DSU）",
                 desc="等價類維護：種類/帶權 DSU、離線倒序、可撤銷預告",
                 frag="s2-4.html", group="strategies"),
            dict(id="s05", path="topics/ds/pages/strategies/05-bit.html", nav="2.5 樹狀數組 BIT",
                 title="2.5 樹狀數組（BIT / Fenwick Tree）",
                 desc="lowbit 切前綴：逆序對、雙 BIT 區間和、BIT 上倍增求第 k 小",
                 frag="s2-5.html", group="strategies"),
            dict(id="s06", path="topics/ds/pages/strategies/06-segment-tree.html", nav="2.6 線段樹基礎",
                 title="2.6 線段樹基礎（build／懶標記／資訊設計）",
                 desc="懶標記三函式分工、先乘後加、最大子段和四元組",
                 frag="s2-6.html", group="strategies"),
            dict(id="s07", path="topics/ds/pages/strategies/07-segment-tree-advanced.html", nav="2.7 線段樹進階",
                 title="2.7 線段樹進階（權值／動態開點／合併／二分／李超）",
                 desc="值域當下標、用到才開點、樹上二分與線段樹合併、李超樹",
                 frag="s2-7.html", group="strategies"),
            dict(id="s08", path="topics/ds/pages/strategies/08-sweepline-cdq.html", nav="2.8 掃描線與離線分治",
                 title="2.8 掃描線、二維數點與離線分治（CDQ／整體二分）",
                 desc="把一個維度變成時間：矩形面積並、三維偏序、整體二分",
                 frag="s2-8.html", group="strategies"),
            dict(id="s09", path="topics/ds/pages/strategies/09-balanced-bst.html", nav="2.9 平衡樹",
                 title="2.9 平衡樹（FHQ Treap／Splay）",
                 desc="split/merge 兩原語打天下：名次、區間翻轉、整體偏移",
                 frag="s2-9.html", group="strategies"),
            dict(id="s10", path="topics/ds/pages/strategies/10-sqrt.html", nav="2.10 分塊與莫隊",
                 title="2.10 分塊與莫隊（根號演算法）",
                 desc="不可合併資訊的救生圈：整塊標記散塊暴力、詢問重排",
                 frag="s2-10.html", group="strategies"),
            dict(id="s11", path="topics/ds/pages/strategies/11-tree.html", nav="2.11 樹上資料結構",
                 title="2.11 樹上資料結構（LCA／樹上差分／樹剖／DSU on tree）",
                 desc="把樹線性化：DFS 序、歐拉序、重鏈剖分序與樹上差分",
                 frag="s2-11.html", group="strategies"),
            dict(id="s12", path="topics/ds/pages/strategies/12-persistent.html", nav="2.12 可持久化",
                 title="2.12 可持久化資料結構",
                 desc="版本共享 O(log n)：主席樹區間第 k 小、可持久化 01-Trie",
                 frag="s2-12.html", group="strategies"),
            dict(id="s13", path="topics/ds/pages/strategies/13-expert.html", nav="2.13 專家專題",
                 title="2.13 專家專題",
                 desc="吉司機線段樹、線段樹分治、LCT、ODT、回滾莫隊、樹套樹",
                 frag="s2-13.html", group="strategies"),
            dict(id="pitfalls", path="topics/ds/pages/pitfalls.html", nav="3. 常見錯誤與陷阱",
                 title="常見錯誤與陷阱",
                 desc="線段樹 4n、標記複合順序、離散化漏值、莫隊指標順序——高頻坑與修法",
                 frag="s3-pitfalls.html"),
            dict(id="method", path="topics/ds/pages/method.html", nav="4. 選型方法論",
                 title="選型方法論與離線思維",
                 desc="操作規格書、選型決策表、五種離線重排與對拍驗證器",
                 frag="s4-method.html"),
            dict(id="roadmap", path="topics/ds/pages/roadmap.html", nav="6. 學習路線圖",
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

# 每頁共用的初學者教學骨架。專屬演算法、公式與範例仍放在 content/；
# 這裡只提供一致的閱讀入口、除錯流程、題型辨識與可靠延伸資源。
BEGINNER_META = {
    "ds": {
        "question": "資料會被怎樣修改？每次又要查哪一段、哪個集合或哪個排名？",
        "brute": "若每次操作都重新掃過全部資料，單次通常要 O(n)；操作數也接近 n 時，總時間容易變成 O(n²)。",
        "intuition": "資料結構的工作，是把上一次已整理好的資訊留下來；下一次只修補受影響的部分，而不是全部重算。",
        "invariant": "先說清楚每個欄位代表哪一段資料，以及更新前後必須永遠成立的關係。",
        "errors": [
            "只背操作模板，卻說不出節點、陣列格或 parent 指標代表什麼。",
            "混用 0-based、1-based 或閉區間、半開區間，造成 off-by-one。",
            "只算單次操作，忘記乘上操作次數與節點數，也沒有估算記憶體。",
        ],
        "signals": "修改與查詢交錯、需要維護集合關係、區間資訊、排名或動態最值。",
        "refs": [
            ("https://cp-algorithms.com/data_structures/segment_tree.html", "cp-algorithms：Segment Tree", "從可合併資訊理解區間資料結構的正式定義與複雜度。"),
            ("https://usaco.guide/gold/", "USACO Guide Gold", "用分級題目練習資料結構選型。"),
            ("https://oi-wiki.org/ds/", "OI Wiki 資料結構", "補強中文術語、變形與進階應用。"),
        ],
    },
    "dp": {
        "question": "暴力遞迴會重複計算哪些相同子問題？要記住哪些資訊，才能讓未來決策不需要回頭看完整歷史？",
        "brute": "直接枚舉所有選擇常形成指數級遞迴樹；同一個剩餘問題會從不同路徑被算很多次。",
        "intuition": "DP 像填表：每格只保存『未來真正需要知道的摘要』，並從已算好的較小問題轉移過來。",
        "invariant": "寫轉移前先用一句完整中文定義 dp 狀態，包含範圍、是否必選、恰好或至多等條件。",
        "errors": [
            "狀態定義少了條件，導致不同歷史被錯誤合併。",
            "初始化把不可達狀態設成 0，讓不存在的方案參與轉移。",
            "迴圈順序與轉移依賴相反，讀到本輪剛更新的值或尚未計算的值。",
        ],
        "signals": "求最優值、方案數或可行性，而且問題能由較小範圍、較少物品或較短前綴組成。",
        "refs": [
            ("https://usaco.guide/gold/intro-dp", "USACO Guide：Introduction to DP", "補強狀態與轉移的入門推導。"),
            ("https://cp-algorithms.com/dynamic_programming/intro-to-dp.html", "cp-algorithms：Introduction to DP", "比較記憶化與遞推。"),
            ("https://atcoder.jp/contests/dp/tasks", "AtCoder Educational DP Contest", "用一組漸進題目建立 DP 題型辨識。"),
        ],
    },
    "greedy": {
        "question": "能不能現在做一個局部選擇，而且保證不會害未來失去最佳答案？",
        "brute": "暴力會枚舉每一步的所有選擇，形成龐大決策樹；貪心想證明其中大多數分支永遠不必探索。",
        "intuition": "貪心不是『看起來最好就選』，而是證明某個最佳答案可以被交換成包含目前選擇，且不會變差。",
        "invariant": "每做一次選擇後，都要說清楚剩餘問題仍保留什麼性質，以及被丟掉的候選人為何不可能更好。",
        "errors": [
            "只憑直覺挑最大或最小，沒有交換論證、領先論證或反證。",
            "排序鍵選錯，或忘記相同主鍵時的 tie-break 會影響答案。",
            "只測隨機資料，沒有刻意構造讓局部最佳與全域最佳衝突的小反例。",
        ],
        "signals": "排序後逐一決策、要求字典序最小、選最多活動、成本可交換比較，或可撤銷最差選擇。",
        "refs": [
            ("https://cp-algorithms.com/schedules/schedule-with-completion-duration.html", "cp-algorithms：Scheduling with Deadlines", "觀察排序、集合與貪心決策如何配合。"),
            ("https://usaco.guide/silver/greedy-sorting", "USACO Guide：Greedy with Sorting", "練習從排序鍵建立貪心直覺。"),
            ("https://cses.fi/problemset/list/", "CSES Problem Set", "用 Sorting and Searching 類題目練習可證明的局部選擇。"),
        ],
    },
    "strings": {
        "question": "字串比較中有哪些前綴、後綴或子串資訊被反覆重算？失配後能否利用已知結構跳過位置？",
        "brute": "從每個起點重新逐字比較，最壞會反覆檢查相同字元，讓長字串退化到 O(nm) 或 O(n²)。",
        "intuition": "字串演算法的核心常是記住『已經匹配了多少』或『哪些片段相同』，失敗時不必完全從零開始。",
        "invariant": "先固定下標制與陣列定義；每個 pi、z、fail、len 或 link 值都必須能用一句話精確描述。",
        "errors": [
            "0-based 與 1-based 公式混用，尤其是長度、右端點與回退位置。",
            "把子串和子序列混為一談，或忘記空字串、單字元與全部相同字元。",
            "只背建表程式，無法手算一個短字串，因此失配時不知道該跳去哪裡。",
        ],
        "signals": "大量模式匹配、重複子串、border、週期、迴文、前綴統計或字典序比較。",
        "refs": [
            ("https://cp-algorithms.com/string/prefix-function.html", "cp-algorithms：Prefix Function", "從 KMP 的 prefix function 建立失配跳轉與線性分析直覺。"),
            ("https://usaco.guide/adv/string-search", "USACO Guide：String Searching", "補強匹配演算法與題目選型。"),
            ("https://oi-wiki.org/string/", "OI Wiki 字串", "補強中文術語、圖示與進階結構。"),
        ],
    },
}

# 48 個策略頁各自的最小手算。這些例子刻意很小，讓讀者能在看模板前先走完一次。
MINI_TRACES = {
    ("ds", "s01"): (
        "<li>陣列 [3,1,4,2] 的前綴和依序是 0,3,4,8,10。</li>"
        "<li>區間 [2,4] 的和不用重加三個數，只算 10-3=7。</li>"
        "<li>讀者應理解：預處理保存了從開頭累積的重工。</li>"
    ),
    ("ds", "s02"): (
        "<li>依序讀 [2,1,4,3]；找下一個更大值時，堆疊先放 2。</li>"
        "<li>1 不可能回答 2，保留；4 到來時連續彈出 1、2，兩者答案都是 4。</li>"
        "<li>每個元素只進出一次，這就是均攤 O(n) 的來源。</li>"
    ),
    ("ds", "s03"): (
        "<li>串流加入 [5,1,8,3]；小根堆可隨時取目前最小值 1。</li>"
        "<li>若要中位數，左半用大根堆 [3,1]，右半用小根堆 [5,8]。</li>"
        "<li>兩堆大小差至多 1，中位數便在堆頂。</li>"
    ),
    ("ds", "s04"): (
        "<li>初始 {1},{2},{3},{4}；合併 1-2 後 parent[2]=1。</li>"
        "<li>再合併 2-3，find(2) 先找到根 1，因此把 3 接到 1。</li>"
        "<li>查 1 與 3 時根相同，表示兩者已由傳遞關係連通。</li>"
    ),
    ("ds", "s05"): (
        "<li>對 [2,1,3,4] 建 BIT；tree[4] 管整段 [1,4]，tree[3] 只管 [3,3]。</li>"
        "<li>查 prefix(3) 先取 tree[3]=3，再跳到 tree[2]=3，得到 6。</li>"
        "<li>每次用 lowbit 刪掉最右側一段已統計範圍。</li>"
    ),
    ("ds", "s06"): (
        "<li>陣列 [2,1,3,4] 的根存總和 10，左右孩子分別存 3、7。</li>"
        "<li>查 [2,4] 時拆成葉 [2,2] 與完整節點 [3,4]，得到 1+7。</li>"
        "<li>區間加 [1,2]+5 時先在 [1,2] 記 lazy，不必立刻改兩個葉。</li>"
    ),
    ("ds", "s07"): (
        "<li>[2,5,5,8] 改用值域計數後，左半 [1,5] 的 count 是 3。</li>"
        "<li>查第 3 小先往左；跳過 [1,3] 的 1 個數後，把 k 改成 2。</li>"
        "<li>最後到葉 5；完整四功能 trace 見本頁正文。</li>"
    ),
    ("ds", "s08"): (
        "<li>三個點 (1,3),(2,1),(3,2) 依 x 排序後，x 維度已由掃描順序處理。</li>"
        "<li>掃到每個點時，用 BIT 查目前 y 以下有幾點，再把自己的 y 加入。</li>"
        "<li>離線的意思是先重排詢問，讓一個維度不再需要資料結構維護。</li>"
    ),
    ("ds", "s09"): (
        "<li>Treap 中鍵值 [1,3,5] 要插入 4，先 split 成 ≤3 與 >3。</li>"
        "<li>得到 [1,3]、[5]，把新節點 4 放中間再 merge。</li>"
        "<li>BST 順序由鍵值維持，樹高則由隨機 priority 維持。</li>"
    ),
    ("ds", "s10"): (
        "<li>n=8、塊長約 3，可分 [1..3]、[4..6]、[7..8]。</li>"
        "<li>查 [2,7]：左右零散位置逐個算，中間完整塊直接讀摘要。</li>"
        "<li>零散最多 O(√n)，完整塊也最多 O(√n)。</li>"
    ),
    ("ds", "s11"): (
        "<li>樹邊 1-2、1-3、3-4；root=1 時 depth 為 0,1,1,2。</li>"
        "<li>LCA(2,4) 先把 4 提到深度 1，再一起上跳，於節點 1 相遇。</li>"
        "<li>樹上技巧常先把路徑拆成少數祖先區段，再交給線性資料結構。</li>"
    ),
    ("ds", "s12"): (
        "<li>版本 0 的 [1,4] 全為 0；把位置 3 加一得到版本 1。</li>"
        "<li>只複製根、[3,4]、[3,3] 三個路徑節點，其餘節點與版本 0 共用。</li>"
        "<li>每次修改只新增 O(log n) 節點，舊版本仍可查詢。</li>"
    ),
    ("ds", "s13"): (
        "<li>一條邊在時間 2～4 存活，就把它放進覆蓋 [2,4] 的時間線段樹節點。</li>"
        "<li>DFS 進入節點時 union，離開時 rollback，葉子即該時間的圖。</li>"
        "<li>抽象重點：把難以刪除的操作改成可撤銷的加入。</li>"
    ),
    ("dp", "s01"): (
        "<li>爬 4 階：dp[0]=1，dp[1]=1。</li>"
        "<li>dp[2]=dp[1]+dp[0]=2，dp[3]=3，dp[4]=5。</li>"
        "<li>每格代表到達該位置的方法數，來源只可能是前 1 或前 2 階。</li>"
    ),
    ("dp", "s02"): (
        "<li>2×3 網格中，dp[row][column] 表示走到該格的方法數。</li>"
        "<li>第一列與第一欄都只有 1 種；右下格由上方 1 與左方 2 相加得 3。</li>"
        "<li>先畫箭頭確認每格依賴誰，再決定迴圈順序。</li>"
    ),
    ("dp", "s03"): (
        "<li>容量 5，物品 (重量2,價值3)、(重量3,價值4)。</li>"
        "<li>0/1 背包倒序更新：第二件加入後 dp[5]=dp[2]+4=7。</li>"
        "<li>若正序，第二件可能在同一輪被重複使用，會錯變完全背包。</li>"
    ),
    ("dp", "s04"): (
        "<li>石堆 [1,2,3]；長度 2 的成本是 merge(1,2)=3、merge(2,3)=5。</li>"
        "<li>整段 [1,3] 枚舉最後切點：3+總和6 或 5+總和6。</li>"
        "<li>取較小得 9；區間 DP 通常依區間長度由短到長填。</li>"
    ),
    ("dp", "s05"): (
        "<li>比較 \"ab\" 與 \"ac\"；dp[i][j] 是兩個前綴的 LCS 長度。</li>"
        "<li>a=a，所以 dp[1][1]=1；b≠c，dp[2][2]=max(dp[1][2],dp[2][1])=1。</li>"
        "<li>雙序列 DP 的兩個座標分別代表各自看了多少字元。</li>"
    ),
    ("dp", "s06"): (
        "<li>股價 [3,1,4]；每天只需記「手上有股票」與「手上沒股票」兩種狀態。</li>"
        "<li>第 2 天持有=max(原持有 -3, 昨天空手0-1)=-1。</li>"
        "<li>第 3 天空手=max(原空手0, 昨天持有-1+4)=3。</li>"
    ),
    ("dp", "s07"): (
        "<li>三個工作用 mask 的三個 bit 表示是否完成；000 是空集合。</li>"
        "<li>從 001 可加入工作 2 或 3，分別到 011、101。</li>"
        "<li>狀態數是 2³=8；每個 bit 都有明確語意才不會轉移錯位。</li>"
    ),
    ("dp", "s08"): (
        "<li>樹 1 連 2、3；每點權重為 5、4、3，不能同時選相鄰點。</li>"
        "<li>選 1 時孩子都不能選，值 5；不選 1 時可選 2、3，值 7。</li>"
        "<li>父節點狀態決定孩子允許哪些狀態，後序 DFS 才能先取得孩子答案。</li>"
    ),
    ("dp", "s09"): (
        "<li>計算 0～25 中不含數字 2 的個數，從十位開始逐位決定。</li>"
        "<li>若目前位選得比上界小，tight 變 false，後面可自由選 0～9。</li>"
        "<li>若仍貼住上界，下一位最多只能選上界對應數字。</li>"
    ),
    ("dp", "s10"): (
        "<li>擲公平硬幣直到第一次正面；設期望次數為 E。</li>"
        "<li>每次一定先擲 1 次；反面機率 1/2 時又回到同一狀態。</li>"
        "<li>E=1+(1/2)E，解得 E=2；先列狀態方程再移項。</li>"
    ),
    ("dp", "s11"): (
        "<li>DAG 有 1→2、1→3、2→4、3→4。</li>"
        "<li>依拓撲序 1,2,3,4 推最長路，dp[4] 從 dp[2]+1、dp[3]+1 取大。</li>"
        "<li>有環時無法直接排依賴，需先縮 SCC 或改用其他模型。</li>"
    ),
    ("dp", "s12"): (
        "<li>轉移只會看前 3 個 dp 值時，不必每格重新掃三個候選。</li>"
        "<li>單調佇列保留可能成為最大值的索引；新值進來時淘汰尾端較差者。</li>"
        "<li>優化不改狀態定義，只加速同一個轉移中的候選搜尋。</li>"
    ),
    ("dp", "s13"): (
        "<li>2×3 棋盤逐格掃描時，只需記住掃描線上兩格是否已有連接。</li>"
        "<li>處理下一格後，把舊輪廓左移並加入新局部狀態。</li>"
        "<li>輪廓 DP 把整個已處理區域壓成邊界摘要，而不是保存完整圖形。</li>"
    ),
    ("greedy", "s01"): (
        "<li>工作時長 [3,1,2]；若目標減少總等待，排序成 [1,2,3]。</li>"
        "<li>等待時間是 0+1+3=4；原順序則是 0+3+4=7。</li>"
        "<li>短工作放前面，能少被更多後續工作重複等待。</li>"
    ),
    ("greedy", "s02"): (
        "<li>活動 [1,3]、[2,5]、[4,6]，按結束時間排序。</li>"
        "<li>先選 [1,3]，跳過重疊的 [2,5]，再選 [4,6]，共 2 個。</li>"
        "<li>最早結束留下最大的後續可用時間。</li>"
    ),
    ("greedy", "s03"): (
        "<li>兩工作 A、B 若排 AB，局部成本為某個式子 C(AB)。</li>"
        "<li>再算交換後 C(BA)，把共同項消掉，只比較剩下的不等式。</li>"
        "<li>若所有相鄰逆序都能交換不變差，排序規則便有證明。</li>"
    ),
    ("greedy", "s04"): (
        "<li>期限內暫時接受工作時長 [2,1,3]；總時間超標時反悔。</li>"
        "<li>最大堆彈出目前最耗時的 3，保留 2、1。</li>"
        "<li>反悔不是隨機撤銷，而是撤銷最能釋放資源的既有選擇。</li>"
    ),
    ("greedy", "s05"): (
        "<li>合併重量 [1,2,6]；先合 1+2=3，再合 3+6=9，總成本 12。</li>"
        "<li>若先合 2+6=8，再合 1+8=9，總成本 17。</li>"
        "<li>小值會被重複計入，越早合併越能控制總成本。</li>"
    ),
    ("greedy", "s06"): (
        "<li>從 \"1432\" 刪 1 位求最小；讀到 3 時，前面的 4 比 3 大。</li>"
        "<li>刪掉 4 得 \"132\"；若刪其他位置，第一個不同位會更大。</li>"
        "<li>字典序問題優先保住更小的高位，單調堆疊負責反悔。</li>"
    ),
    ("greedy", "s07"): (
        "<li>把 [1,7,9] 全移到同一位置，選中位數 7，距離和 6+0+2=8。</li>"
        "<li>選平均附近 6 時成本 5+1+3=9。</li>"
        "<li>絕對值距離的斜率在中位數左右改變符號，因此中位數最優。</li>"
    ),
    ("greedy", "s08"): (
        "<li>三點邊權：AB=1、BC=2、AC=5。</li>"
        "<li>Kruskal 先選 AB、BC，三點已連通，跳過形成環且更貴的 AC。</li>"
        "<li>每一步選跨越目前連通塊的最便宜安全邊。</li>"
    ),
    ("greedy", "s09"): (
        "<li>期限 1、2、2 的工作收益為 5、4、3。</li>"
        "<li>按收益由大到小，DSU 找不超過期限的最晚空位。</li>"
        "<li>資料結構只加速『下一個可用位置』，貪心順序仍需獨立證明。</li>"
    ),
    ("greedy", "s10"): (
        "<li>在位置 [1,2,8] 放 2 個基地，猜最小距離至少 5。</li>"
        "<li>從 1 開始貪心放下一個最早可行位置 8，成功。</li>"
        "<li>若距離 8 失敗，所有更大的距離也失敗，因此答案可二分。</li>"
    ),
    ("greedy", "s11"): (
        "<li>先在三個元素的小集合列出所有可行子集，檢查加入順序是否影響可行性。</li>"
        "<li>若較小獨立集總能從較大獨立集補一個元素，才具有擬陣交換性。</li>"
        "<li>專家級貪心先辨認結構定理，不能從普通排序模板硬猜。</li>"
    ),
    ("strings", "s01"): (
        "<li>字串 \"abcd\" 用 base 多項式建立前綴 hash。</li>"
        "<li>比較子串 \"bc\" 與另一段時，用兩個前綴值相減並校正次方。</li>"
        "<li>O(1) 比較來自預先保存所有前綴貢獻；碰撞風險仍需雙 hash 或核對。</li>"
    ),
    ("strings", "s02"): (
        "<li>模式 \"abab\" 的最長真前後綴長度依序是 0,0,1,2。</li>"
        "<li>匹配到 \"aba\" 後失配，不必退回開頭，跳到長度 1 的 border。</li>"
        "<li>fail/pi 保存的是可重用的已匹配前綴。</li>"
    ),
    ("strings", "s03"): (
        "<li>字串 \"ababa\" 的 Z 值是 [5,0,3,0,1]。</li>"
        "<li>Z[2]=3 表示從位置 2 開始的 \"aba\" 與整串前綴相同。</li>"
        "<li>Z-box 讓落在已知匹配區間內的位置先繼承資訊，再向外擴展。</li>"
    ),
    ("strings", "s04"): (
        "<li>字串 \"aba\" 以 b 為中心可向兩側擴 1，迴文半徑覆蓋整串。</li>"
        "<li>處理新中心時，先利用對稱位置的已知半徑，再檢查邊界外字元。</li>"
        "<li>Manacher 省掉每個中心重複比較已知相同的內部區域。</li>"
    ),
    ("strings", "s05"): (
        "<li>插入 \"cat\"、\"car\"；根→c→a 的兩個節點被共用。</li>"
        "<li>第三個字元才分成 t 與 r；查 \"cap\" 時在 p 邊失敗。</li>"
        "<li>Trie 把共同前綴只存一次，每走一條邊就消耗一個字元。</li>"
    ),
    ("strings", "s06"): (
        "<li>模式 \"he\"、\"she\" 建成 Trie；處理 \"she\" 時走 s→h→e。</li>"
        "<li>h 節點失配後可沿 fail 接到根的 h；e 節點因此也能報告 \"he\"。</li>"
        "<li>fail 邊讓多模式匹配共享失配後仍有用的後綴。</li>"
    ),
    ("strings", "s07"): (
        "<li>\"aba\" 的後綴是 \"aba\"、\"ba\"、\"a\"。</li>"
        "<li>排序後為 \"a\"、\"aba\"、\"ba\"，所以 SA=[3,1,2]（1-based）。</li>"
        "<li>倍增法先按 1 字元排名，再按 2、4、8 字元排名。</li>"
    ),
    ("strings", "s08"): (
        "<li>依序加入 \"a\"、\"b\"、\"a\"；SAM 每步新增代表所有新後綴的狀態。</li>"
        "<li>最後一步新增的不同子串是 \"a\"、\"ba\"、\"aba\" 中尚未出現者。</li>"
        "<li>狀態代表 endpos 相同的一群子串，不是單一子串。</li>"
    ),
    ("strings", "s09"): (
        "<li>讀 \"ababa\" 時，本質不同迴文依序出現 a、b、aba、bab、ababa。</li>"
        "<li>每加入一字元，只可能新增一個以目前位置結尾的最長新迴文。</li>"
        "<li>fail 指向目前迴文的最長真迴文後綴。</li>"
    ),
    ("strings", "s10"): (
        "<li>環狀字串 \"baca\" 的旋轉有 baca、acab、caba、abac。</li>"
        "<li>比較候選起點時，一旦某位置較大，就能批量淘汰一段不可能起點。</li>"
        "<li>最小表示答案是 \"abac\"，起點在最後一個 a。</li>"
    ),
    ("strings", "s11"): (
        "<li>先用 \"ababa\" 列出所有 border、不同子串與迴文，觀察同一資訊在不同結構中的表示。</li>"
        "<li>例如 SAM 擅長一般子串，PAM 擅長迴文；不要只因名稱相似就混用。</li>"
        "<li>專家題通常是把自動機狀態再接 DP、線段樹或樹上統計。</li>"
    ),
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


def render_beginner_intro(topic, page):
    """在每個主題頁正文前加入一致但依主題調整的初學者閱讀入口。"""
    meta = BEGINNER_META[topic["id"]]
    title = page.get("title", topic["name"])
    desc = page.get("desc", topic["home_desc"])
    trace = MINI_TRACES.get((topic["id"], page["id"]))
    trace_html = ""
    if trace:
        trace_html = """
  <div class="mini-trace">
    <h3>最小可手算例子</h3>
    <ol>%s</ol>
  </div>
""" % trace
    return """
<aside class="beginner-guide" aria-label="本頁初學者閱讀指南">
  <div class="beginner-guide-head">
    <span aria-hidden="true">🧭</span>
    <div><b>初學者閱讀指南</b><small>%s</small></div>
  </div>
  <h3>這頁要解決什麼問題？</h3>
  <p><b>先問：</b>%s</p>
  <p>本頁聚焦「%s」。%s</p>
  <p><b>暴力做法的代價：</b>%s</p>
  <h3>核心直覺</h3>
  <p>%s</p>
  <div class="callout proof"><b>閱讀程式前先找不變量</b><p>%s</p></div>
  <details class="predict-box"><summary>先猜猜看：什麼時候該想到這頁？</summary>
    <p>%s</p>
  </details>
%s
</aside>
""" % (
        title,
        meta["question"],
        desc,
        "先在紙上用 3～8 個元素走一次，再對照正文的公式與程式碼。",
        meta["brute"],
        meta["intuition"],
        meta["invariant"],
        meta["signals"],
        trace_html,
    )


def render_beginner_recap(topic, page):
    """在每頁正文後加入除錯、自我檢查與可靠參考資料。"""
    meta = BEGINNER_META[topic["id"]]
    errors = "\n".join("<li>%s</li>" % item for item in meta["errors"])
    refs = "\n".join(
        '<li><a href="%s" target="_blank" rel="noopener">%s</a>——%s</li>' % item
        for item in meta["refs"]
    )
    return """
<section class="beginner-recap" aria-label="本頁複習與除錯">
  <h3>常見誤解與除錯順序</h3>
  <ol class="bug-list">%s</ol>
  <p><b>最小測資順序：</b>先測空集合或最短輸入，再測單一元素、全部相同、嚴格遞增／遞減、
  重複值與最大邊界；若答案可能累加，另外檢查 32-bit overflow。</p>
  <h3>複雜度與適用時機</h3>
  <p>不要只記正文最後的 Big-O。請把它拆成「狀態／節點／候選數量 × 每次轉移或操作成本」，
  再代入題目的最大資料範圍。若乘積超過時間預算，就回頭找是否重算、能否排序、離線、
  壓縮狀態或使用更合適的資料結構。</p>
  <h3>參考資料</h3>
  <ul class="reference-list">%s</ul>
  <div class="callout idea"><b>你現在應該記得什麼</b>
    <ul>
      <li>本頁主題：%s。</li>
      <li>看到的題型訊號：%s</li>
      <li>最重要的不變量：%s</li>
      <li>複雜度要從處理的資料量與每次操作成本相乘推回來。</li>
      <li>先用最小反例驗證直覺，再套模板；模板不是正確性證明。</li>
    </ul>
  </div>
</section>
""" % (
        errors,
        refs,
        page.get("desc", topic["home_desc"]),
        meta["signals"],
        meta["invariant"],
    )


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
        '<div class="th-desc">圖論、數論、計算幾何……歡迎期待，站內架構已為擴充做好準備。</div>'
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
                body = (
                    render_beginner_intro(topic, page) +
                    build_topic_index_body(topic) +
                    render_beginner_recap(topic, page)
                )
                pagenav = render_pagenav(page["path"], topic, page["id"])
                title, desc = topic["name"], topic["home_desc"]
            else:
                body = fix_cross_refs(read_frag(topic, page["frag"]), page["path"], topic)
                if page["id"] != "s07" or topic["id"] != "ds":
                    body = (
                        render_beginner_intro(topic, page) +
                        body +
                        render_beginner_recap(topic, page)
                    )
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
