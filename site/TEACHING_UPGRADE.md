# 初學者教學升級清單

本文件追蹤 `topics/*/content/*.html` 的內容升級；這些檔案是網站教學頁面的唯一來源，
公開頁面由 `python3 build.py` 產生。完成一頁的標準是：能獨立閱讀，包含問題情境、
白話直覺、正式定義、可手算 trace、圖像、程式導讀、複雜度、適用訊號、至少三個常見錯誤、
漸進練習、已確認的參考資料，以及頁末重點複習。

狀態：`完成`、`進行中`、`待補強`。

## 第一階段：資料結構核心

| 狀態 | 公開頁面 | 內容來源 | 主要補強方向 |
| --- | --- | --- | --- |
| 完成 | `/topics/ds/pages/theory.html` | `topics/ds/content/s1-theory.html` | 操作分析、可合併性、不變量、均攤與勢能、線上／離線 |
| 完成 | `/topics/ds/pages/strategies/01-prefix-sums.html` | `topics/ds/content/s2-1.html` | 前綴和、差分、ST 表逐步建表 |
| 完成 | `/topics/ds/pages/strategies/02-monotonic.html` | `topics/ds/content/s2-2.html` | 候選人淘汰、堆疊／佇列 trace、均攤分析 |
| 完成 | `/topics/ds/pages/strategies/03-heap.html` | `topics/ds/content/s2-3.html` | heap 操作、對頂堆、懶刪除 |
| 完成 | `/topics/ds/pages/strategies/04-dsu.html` | `topics/ds/content/s2-4.html` | 集合合併、路徑壓縮、帶權／種類 DSU |
| 完成 | `/topics/ds/pages/strategies/05-bit.html` | `topics/ds/content/s2-5.html` | lowbit 管轄範圍、更新／查詢路徑、倍增 |
| 完成 | `/topics/ds/pages/strategies/06-segment-tree.html` | `topics/ds/content/s2-6.html` | 建樹、查詢拆區間、lazy 不變量與 push 順序 |
| 完成 | `/topics/ds/pages/strategies/07-segment-tree-advanced.html` | `topics/ds/content/s2-7.html` | 權值化、動態開點、樹上二分、合併的完整小例子 |
| 完成 | `/topics/ds/pages/strategies/08-sweepline-cdq.html` | `topics/ds/content/s2-8.html` | 離線、事件排序、CDQ 維度消除 |
| 完成 | `/topics/ds/pages/strategies/09-balanced-bst.html` | `topics/ds/content/s2-9.html` | split／merge 不變量與 FHQ Treap trace |
| 完成 | `/topics/ds/pages/strategies/10-sqrt.html` | `topics/ds/content/s2-10.html` | 分塊取捨、莫隊指標移動 |
| 完成 | `/topics/ds/pages/strategies/11-tree.html` | `topics/ds/content/s2-11.html` | LCA、樹上差分、樹剖、DSU on tree |
| 完成 | `/topics/ds/pages/strategies/12-persistent.html` | `topics/ds/content/s2-12.html` | 版本、路徑複製、主席樹差分 |
| 完成 | `/topics/ds/pages/strategies/13-expert.html` | `topics/ds/content/s2-13.html` | Beats、線段樹分治、LCT 等術語拆解 |
| 完成 | `/topics/ds/pages/pitfalls.html` | `topics/ds/content/s3-pitfalls.html` | overflow、空集合、懶標記、下標反例 |
| 完成 | `/topics/ds/pages/method.html` | `topics/ds/content/s4-method.html` | 題型辨識、線上／離線選型決策 |
| 完成 | `/topics/ds/pages/roadmap.html` | `topics/ds/content/s6-roadmap.html` | 每階段先備知識、檢核與漸進題單 |
| 完成 | `/topics/ds/` | `topics/ds/content/s0-intro.html` | 初學者使用方式與學習順序 |

## 第二階段：動態規劃

`topics/dp/content/` 共 18 頁：導讀、理論、13 個策略、陷阱、方法論、路線圖。
優先順序為線性 DP、網格、背包、雙序列、區間、狀態機，再處理樹上／數位／狀壓與優化。
每頁須把「狀態代表什麼」放在公式前，並提供完整狀態表與每格轉移來源。

已完成來源：`s0-intro.html`、`s1-theory.html`、`s2-1.html`～`s2-13.html`、
`s3-pitfalls.html`、`s4-method.html`、`s6-roadmap.html`。公開路由依序為主題首頁、
`pages/theory.html`、`pages/strategies/01-linear.html`～`13-expert.html`、
`pages/pitfalls.html`、`pages/method.html`、`pages/roadmap.html`。

## 第三階段：貪心

`topics/greedy/content/` 共 17 頁：導讀、理論、11 個策略、陷阱、證明、路線圖。
優先順序為排序、區間、交換論證、反悔、堆，再處理字典序、數學、圖上與進階組合。
每個貪心規則都要先展示暴力選擇樹，再給交換論證或反例。

已完成來源：`s0-intro.html`、`s1-theory.html`、`s2-1.html`～`s2-11.html`、
`s3-pitfalls.html`、`s4-proofs.html`、`s6-roadmap.html`。公開路由依序為主題首頁、
`pages/theory.html`、`pages/strategies/01-sorting.html`～`11-expert.html`、
`pages/pitfalls.html`、`pages/proofs.html`、`pages/roadmap.html`。

## 第四階段：字串

`topics/strings/content/` 共 17 頁：導讀、理論、11 個策略、陷阱、方法論、路線圖。
優先順序為雜湊、KMP、Z、Trie、Manacher，再處理 AC、後綴數組與各種自動機。
每頁須以短字串逐字元展示陣列／指標變化，並明確統一 0-based 或 1-based 定義。

已完成來源：`s0-intro.html`、`s1-theory.html`、`s2-1.html`～`s2-11.html`、
`s3-pitfalls.html`、`s4-method.html`、`s6-roadmap.html`。公開路由依序為主題首頁、
`pages/theory.html`、`pages/strategies/01-hashing.html`～`11-expert.html`、
`pages/pitfalls.html`、`pages/method.html`、`pages/roadmap.html`。

## 尚未存在的主題

目前程式庫尚無圖論、數論、計算幾何的內容來源與路由。它們不列入「修改既有頁面」的
68 個公開教學頁清單；待四個既有主題達到一致品質後，再新增主題註冊、導覽與內容頁。
