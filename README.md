# competitive-programming

## 📚 演算法策略圖鑑

**一套統一介面**，收錄程式競賽各大演算法主題的策略分類與題目整理——每個主題都是從入門（★）到程式競賽專家（★★★★★）的完整攻略，共用同一份側欄導覽、顯示設定與練習進度追蹤。之後新增主題（例如字串演算法）不需要另外做網站，只要在主題註冊表登記一筆即可自動出現在首頁、側欄切換器與全站題目總表。

**🌐 線上網站：https://youyun8.github.io/competitive-programming/**

目前收錄的主題：

| 主題 | 網址 | 內容 |
|---|---|---|
| 🧭 **貪心演算法** | `/topics/greedy/` | 11 大策略分類、四大證明技巧、假貪心陷阱、路線圖 |
| 📈 **動態規劃** | `/topics/dp/` | 13 大策略分類、狀態設計方法論、DP 優化技術、路線圖 |
| ✨ 更多主題陸續加入中 | — | 字串演算法、資料結構專題、圖論……站內架構已為擴充做好準備 |

共 146 題可篩選的**全站題目總表**（`/pages/problems.html`）橫跨所有主題，同一題若在多個主題都有出現（例如同一道題目分別用貪心與 DP 兩種角度講解），練習進度只需標記一次、兩邊自動同步。

---

## ✨ 網站功能

- **一套共用介面**：首頁列出所有主題卡片；側欄固定的「主題」切換器可隨時在主題之間切換，切換後仍停留在同一種頁面類型（例如都在看策略分類頁）；每個主題內的章節導覽依目前頁面自動高亮，頁尾提供「上一節 / 下一節」可依順序閱讀
- **⚙️ 顯示設定面板**（每頁側欄都有）：
  - 主題（深色模式意義上的）：淺色 / 深色 / 跟隨系統
  - 內文字體大小：小 / 中 / 大 / 特大
  - 版面寬度：窄 / 預設 / 寬 / 全螢幕
  - 設定存在瀏覽器 `localStorage`（單一 key：`algo-guide-settings`），全站共用、切換頁面或重新整理都會保留
- **練習進度追蹤 + 跨裝置同步**：每題（策略頁面的題目卡片、全站題目總表的每一列）都能標記「尚未練習 ⬜／需複習 🔶／已通過 ✅」；設定 Supabase 後可用 Email magic link 登入，同一信箱在不同裝置會看到相同進度（見下方「[跨裝置進度同步](#️-跨裝置進度同步選用)」）。進度以**題目 id** 為 key、橫跨全站所有主題共用同一份資料（本機 key：`algo-guide-progress`）。**未設定雲端同步時完全不影響使用**——進度只存在目前瀏覽器
- **全站題目總表**（`pages/problems.html`）可依**主題**、難度星級、策略標籤（皆可複選）與關鍵字即時篩選，並顯示已通過/需複習/尚未練習的統計；從主題內頁點側欄的「📋 全站題目總表」連結會自動帶上該主題的篩選（網址帶 `#topic=<id>`），仍可手動清除篩選看全部
- 手機自動收合為抽屜式側欄；演算法程式碼統一使用 C++，並有自寫的輕量語法上色
- 數學式與時間複雜度統一用 TeX 撰寫，頁面透過 MathJax 4 CDN 排版；其餘網站內容維持純靜態
- 本機建置零安裝相依；雲端進度同步只有在完成 Supabase 設定後才會載入其瀏覽器 SDK

---

## 📁 專案結構

```
competitive-programming/
├── .github/workflows/
│   └── deploy-pages.yml       # GitHub Actions：組裝 site/ 後部署到 GitHub Pages
└── site/                      # 網站根目錄（部署時這個資料夾的內容就是網站的根目錄）
    ├── index.html              # 站級首頁：列出所有主題卡片（由 build.py 產生，勿手動編輯）
    ├── build.py                # 靜態頁面產生器：主題註冊表 + content/ → 所有頁面
    ├── assets/                 # 全站共用，所有主題都用同一份
    │   ├── site.css             # 共用樣式（主題色變數、字體大小/版面寬度、主題切換器）
    │   ├── site.js              # 共用行為（設定面板、側欄、主題切換高亮、語法上色、題目篩選）
    │   ├── math-config.js        # MathJax 4 的 TeX 分隔符與略過標籤設定
    │   ├── problems-data.js     # 全站題目總表資料（每列多一欄「主題 id」，橫跨所有主題合併存放）
    │   ├── progress.js          # 練習進度追蹤 + Supabase 登入/雲端同步（全站共用一份）
    │   └── supabase-config.js   # Supabase 公開連線設定（預設是佔位值＝本機模式）
    ├── pages/
    │   └── problems.html        # 全站題目總表（由 build.py 產生；唯一不屬於任何主題的頁面）
    └── topics/                  # 每個主題一個資料夾，彼此結構相同、互不相依
        ├── greedy/               # 🧭 貪心演算法
        │   ├── index.html          # 主題首頁（由 build.py 產生）
        │   ├── content/            # ★ 這個主題教學內容的唯一來源（source of truth）
        │   │   ├── s0-intro.html     # 主題首頁導讀
        │   │   ├── s1-theory.html
        │   │   ├── s2-1.html … s2-11.html  # 策略分類章節
        │   │   ├── s3-pitfalls.html
        │   │   ├── s4-proofs.html
        │   │   └── s6-roadmap.html
        │   ├── pages/               # 產生出的章節頁（由 build.py 產生）
        │   └── OUTLINE.md           # 這個主題的內容大綱
        └── dp/                   # 📈 動態規劃（結構同上，章節到 s2-13、多一份 s4-method.html）
```

**內容與版面是分離的**：`topics/<id>/content/*.html` 只放教學內文（不含側欄、設定面板等版面），`build.py` 負責把內文套上共用版面模板，產生最終要部署的靜態頁面。這代表：

- ✅ 修改教學內容 → 編輯對應主題 `content/` 底下的檔案 → 重新執行 `site/build.py`
- ✅ 修改版面／導覽／設定功能 → 編輯 `build.py`（模板）或 `assets/site.css`／`assets/site.js` → 重新執行一次 `build.py` 讓所有頁面（所有主題）套上新版面
- 🚫 不要直接手動編輯 `index.html` 或 `pages/*.html`（下次執行 `build.py` 會被覆蓋）

---

## 🧩 新增一個主題（例如「字串演算法」）

這是這套架構存在的目的——新增主題**不需要另外做介面**，只要：

1. 建立 `site/topics/strings/content/*.html`，內容片段結構比照既有主題（`s0-intro.html` 首頁導讀、`s1-theory.html` 理論、`s2-N.html` 策略章節、`s3-pitfalls.html` 陷阱、`s6-roadmap.html` 路線圖……依需要增減）
2. 打開 `site/build.py`，在檔案開頭的 `TOPICS` 清單新增一筆 `dict(id="strings", icon="🔤", short="字串", name="字串演算法", ...)`，`pages` 欄位登記這個主題的所有章節（照抄既有兩個主題的寫法即可）
3. 打開 `site/assets/site.js`，在 `TOPIC_META` 補一筆 `strings: { label: "字串演算法", short: "字串", icon: "🔤" }`（題目總表的主題欄位與篩選 chip 要用）
4. 把這個主題的題目加進 `site/assets/problems-data.js`（每列最後一欄是主題 id，例如 `"strings"`）
5. 執行 `python3 build.py`——首頁的主題卡片、側欄的主題切換器、全站題目總表的主題篩選都會自動出現這個新主題

不需要新增 workflow、不需要新的 `index.html` 骨架、不需要複製 `site.css`／`site.js`——這些全站只有一份。

---

## 🛠️ 本機開發

### 修改內容後重新產生頁面

```bash
cd site && python3 build.py
```

只需要 Python 3 標準函式庫，沒有其他建置相依套件。腳本會印出所有寫入的檔案；瀏覽器顯示 TeX 時需要連線載入 MathJax 4 CDN。

### 本機預覽

若只測本機內容與進度，可直接用瀏覽器開啟 `site/index.html`。若要測 Email magic link 雲端登入，請使用下方的本機 HTTP 伺服器，並把 `http://localhost:8000/**` 加到 Supabase 的 Redirect URLs；`file://` 不能作為登入回呼網址。沒有網路或尚未設定 Supabase 時，其餘功能都不受影響。

若想用本機伺服器預覽：

```bash
cd site && python3 -m http.server 8000
# 開瀏覽器造訪 http://localhost:8000/
```

### 新增一個子主題頁面（在既有主題內）

1. 在該主題的 `content/` 新增一個 `.html` 片段檔（只寫內文，從 `<h2>...</h2>` 開始）
2. 打開 `build.py`，在該主題 `dict(...)` 的 `pages` 清單中新增一筆對應的頁面 dict（`id`、`path`、`nav`、`title`、`desc`、`frag`）
3. 若新頁面會被其他頁面用 `href="#s..."` 這種錨點引用，順便在該主題的 `anchor_to_id` 對照表補上映射；跨主題引用用 `href="#topic-<id>"`，連到全站題目總表用 `href="#problems"`（這兩種是站級特殊錨點，`fix_cross_refs()` 會自動解析，不需要在每個主題的 `anchor_to_id` 裡重複登記）
4. 執行 `python3 build.py` 重新產生所有頁面（側欄導覽、上一頁/下一頁會自動更新）

### 新增一道題目

- 加進 `assets/problems-data.js` 的陣列裡，格式是 `[題名, 來源, URL, 難度星級, [標籤...], 關鍵想法, 題目id, 主題id]`，**題目 id 必須全站唯一**（用來記錄練習進度，也用來讓同一題在題目總表與策略頁面卡片之間同步狀態）；例外：若同一道真實題目要從兩個不同主題的角度各講一次（例如貪心與 DP 都收錄同一題），兩筆資料**可以刻意共用同一個題目 id**，這樣使用者在任一邊標記進度，兩邊都會同步
- 若同一題也會出現在 `topics/<id>/content/s2-*.html` 的某張 `.problem` 卡片裡，把該卡片的 `<div class="problem">` 加上同一個 `data-problem-id="..."`，兩處的進度狀態就會自動連動
- id 命名慣例：`lc-455`、`poj-2287`、`luogu-p1080`、`cf-865d`、`atcoder-dp-o` 這種「判題平台+題號」小寫格式；沒有對應題號的概念性條目用 `misc-XX` 或描述性 slug（如 `tree-diameter`）

---

## ☁️ 跨裝置進度同步（選用）

網站是純靜態的，GitHub Pages 不提供登入與資料庫。這裡改用 **Supabase Auth + Postgres**：使用者只要輸入 Email、點信箱裡的 magic link，不必另外設定 Google OAuth；瀏覽器直接透過 Supabase 的公開 API 連線，資料則由 Row Level Security（RLS）限制成每人只能讀寫自己的進度。

**在你完成下面的設定之前，網站會自動停留在「本機進度模式」**：練習進度照樣存在 `localStorage`，不載入 Supabase SDK，也不會發出雲端請求。

### 設定步驟

1. **建立 Supabase 專案**
   - 到 [Supabase Dashboard](https://supabase.com/dashboard) 建立一個專案。

2. **建立資料表與 RLS 規則**
   - 打開 **SQL Editor → New query**，執行以下 SQL：

     ```sql
     create table public.user_progress (
       user_id uuid not null references auth.users(id) on delete cascade,
       problem_id text not null,
       status text not null check (status in ('none', 'review', 'done')),
       updated_at timestamptz not null default now(),
       primary key (user_id, problem_id)
     );

     alter table public.user_progress enable row level security;

     grant select, insert, update, delete
       on table public.user_progress
       to authenticated;

     create policy "Users manage only their own progress"
       on public.user_progress
       for all
       to authenticated
       using ((select auth.uid()) = user_id)
       with check ((select auth.uid()) = user_id);
     ```

   - RLS 規則會在資料庫層強制 `auth.uid() = user_id`，匿名訪客與其他使用者都無法讀寫不屬於自己的資料。

3. **設定 magic link 回呼網址**
   - 到 **Authentication → URL Configuration**。
   - 將 **Site URL** 設成 `https://youyun8.github.io/competitive-programming/`。
   - 在 **Redirect URLs** 加入 `https://youyun8.github.io/competitive-programming/**`；本機測試另加 `http://localhost:8000/**`。

4. **取得兩個公開設定值**
   - 從專案的 **Connect** 對話框或 **Project Settings → API** 複製 Project URL 與 Publishable key。
   - 不要使用 `service_role` secret；瀏覽器端只應放 Publishable key。

5. **填入網站設定檔**
   - 編輯 `site/assets/supabase-config.js`：

     ```js
     window.SUPABASE_CONFIG = {
       url: "https://your-project.supabase.co",
       publishableKey: "sb_publishable_..."
     };
     ```

   - commit 並重新部署。網站偵測到兩個值不再是 `YOUR_...` 佔位字串後，才會載入 Supabase SDK 並顯示 Email 登入表單。

> Project URL 與 Publishable key 本來就會公開在前端；安全邊界是第 2 步的 RLS。不要把 `service_role` secret 放進 repo 或瀏覽器。

### 資料怎麼存、怎麼同步

- 每個題目的進度是一列，主鍵為 `(user_id, problem_id)`；同一題出現在不同主題頁時仍共用同一個 `problem_id`。
- 登入時會讀取雲端資料；雲端沒有而本機已有的題目會上傳，同一題兩邊都有時以雲端值為準。
- 登入後每次標記都立即 upsert；另一台裝置重新載入頁面，或切回已開啟的分頁時，會再抓一次最新進度。
- 登出後繼續使用 `localStorage` 快取；未設定 Supabase 時不載入外部 SDK。

---

## 🚀 部署（GitHub Actions → GitHub Pages）

網站透過 [`.github/workflows/deploy-pages.yml`](.github/workflows/deploy-pages.yml) 自動部署到 **GitHub Pages**，來源是這個 repo 本身（不需要另外的伺服器或第三方服務）。

流程：

1. **觸發**：每次 `push` 到 `main` 分支（或在 GitHub 的 Actions 頁面手動點 *Run workflow*，對應 `workflow_dispatch`）都會觸發部署
2. **Assemble site**：把 `site/` 複製到 `_site/`，並移除不需要部署的開發用檔案——每個主題的 `content/` 原始片段、`build.py`、`OUTLINE.md`（這些只在本機修改內容時用得到，產生好的 `.html` 才是要部署的東西）
3. **Setup Pages**（`configure-pages`）：確認 repo 的 GitHub Pages 設定，`enablement: true` 代表如果 Pages 還沒啟用，會自動把來源設成「GitHub Actions」
4. **Upload artifact + Deploy**：把 `_site/` 打包部署到 GitHub Pages 的 `github-pages` environment，並輸出網址

因為是靜態網站，CI **不需要**任何建置步驟（不跑 `npm install`、不跑 `build.py`）——`site/` 底下已經是產生好的最終 HTML/CSS/JS，直接組裝部署即可。`build.py` 只在你本機修改內容後手動執行一次、把結果一起 commit 進去。

### 驗證部署狀態

- 到 repo 的 **Actions** 分頁（`https://github.com/<owner>/<repo>/actions`），可以看到每次 push 觸發的 workflow run，成功會顯示綠勾勾
- 點進某次 run，`deploy` job 的 **Deploy to GitHub Pages** 步驟輸出裡會有實際的網站網址（也會顯示在 run 頁面上方的 environment 連結）
- 到 repo 的 **Settings → Pages**，可以看到目前生效的網址與部署歷史

### 首次啟用（一般不需要手動做，備用步驟）

`enablement: true` 通常會自動處理好第一次啟用。如果所在的 organization 政策關閉了自動啟用、或想手動確認設定，可以到：

1. Repo → **Settings → Pages**
2. **Build and deployment → Source** 選擇 **GitHub Actions**（不是 "Deploy from a branch"）
3. 儲存後重新觸發一次 workflow（push 一個 commit，或用 *Run workflow* 手動觸發）

### 手動重新觸發部署

不想額外 commit 也能重新部署：到 **Actions → Deploy site to GitHub Pages → Run workflow**，選擇 `main` 分支後執行（對應 workflow 裡的 `workflow_dispatch` 觸發條件）。

### 常見問題排解

| 現象 | 原因 | 解法 |
|---|---|---|
| workflow 執行失敗，幾秒內就結束，沒有詳細 log | Push 的分支不在觸發清單，或被 `github-pages` environment 的分支保護規則擋下 | 確認改動已經合併/推送到 `main`；GitHub Pages 的 environment 預設只允許 `main` 部署 |
| 部署成功但網站 404 | `_site/` 組裝路徑錯誤，或 `index.html` 不在根目錄 | 確認 workflow 的 Assemble site 步驟把 `site/` 複製到 `_site/`，且 `_site/index.html` 存在 |
| 樣式/腳本沒套用 | `assets/site.css`／`assets/site.js` 路徑算錯 | 檢查是不是手動改了 `topics/<id>/pages/*.html` 而非改 `content/` 後重新跑 `build.py`（相對路徑深度由 `build.py` 自動計算，手動編輯容易算錯） |
| 修改了 `content/` 但網站沒變 | 忘記重新執行 `build.py`，或執行後忘記 commit 產生的檔案 | `cd site && python3 build.py`，再 `git add` 產生出的 `index.html`／`topics/*/pages/`／`pages/problems.html` 一起 commit |
| 新增主題後首頁/側欄沒出現 | `build.py` 的 `TOPICS` 清單忘記加、或 `assets/site.js` 的 `TOPIC_META` 忘記加 | 對照上方「新增一個主題」章節，兩處都要補；只改一處會導致圖示/篩選 chip 顯示異常 |
| 第一次啟用 Pages 時 workflow 失敗 | 極少數情況下 organization 層級關閉了 Actions 自動管理 Pages 的權限 | 依照上方「首次啟用」的手動步驟，把 Source 設成 GitHub Actions 後重新觸發 |
| magic link 點開後回到錯誤網址或無法登入 | Supabase 沒有允許目前頁面的回呼網址 | 到 Authentication → URL Configuration，確認 Site URL 與含 `/**` 的 Redirect URL 都已加入 |
| 登入後 Console 顯示 `row-level security`、`401` 或 `403` | 資料表、grant 或 RLS policy 沒有完整建立 | 重新執行「跨裝置進度同步」第 2 步 SQL，確認 table 的 RLS 已啟用 |
| 側欄一直顯示「☁️ 本機進度模式」 | `assets/supabase-config.js` 仍是 `YOUR_...` 佔位值 | 填入 Project URL 與 Publishable key，重新執行 `build.py` 並部署 |
| 收不到登入信 | 郵件被分類、Email provider 設定或寄送頻率限制 | 先檢查垃圾郵件，再到 Supabase Authentication 的 Users 與 Logs 查看寄送結果 |

### 自訂網域（選用）

若要掛自訂網域，在 `site/` 底下新增一個 `CNAME` 檔（內容為你的網域，如 `algo.example.com`），`build.py` 不會動到這個檔案，正常 commit 進去即可；同時要在網域的 DNS 設定 `CNAME` 指向 `<owner>.github.io`。

---

## 📄 授權與題目來源

題目連結指向各原始平台（LeetCode／力扣、Codeforces、AtCoder、洛谷、POJ、UVa、USACO、NOI/NOIP/APIO 官方或鏡像站），本站僅整理分類與提供思路說明，不重製題目內容。
