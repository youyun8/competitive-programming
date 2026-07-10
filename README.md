# competitive-programming

## 📚 演算法上分攻略

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
- **練習進度追蹤 + 跨裝置同步**：每題（策略頁面的題目卡片、全站題目總表的每一列）都能標記「尚未練習 ⬜／需複習 🔶／已通過 ✅」；用 Google 帳號登入後，同一帳號在不同裝置登入會看到相同進度（見下方「[跨裝置進度同步](#️-跨裝置進度同步選用)」設定）。進度以**題目 id** 為 key、橫跨全站所有主題共用同一份資料（單一 key：`algo-guide-progress`）。**未設定雲端同步時完全不影響使用**——進度會退回只存在目前瀏覽器
- **全站題目總表**（`pages/problems.html`）可依**主題**、難度星級、策略標籤（皆可複選）與關鍵字即時篩選，並顯示已通過/需複習/尚未練習的統計；從主題內頁點側欄的「📋 全站題目總表」連結會自動帶上該主題的篩選（網址帶 `#topic=<id>`），仍可手動清除篩選看全部
- 手機自動收合為抽屜式側欄；程式碼區塊有自寫的輕量 C++ / Python 語法上色
- 網站本身零外部依賴、可離線使用；只有「雲端進度同步」這一項功能會在設定好之後連線 Google 的 Firebase 服務（未設定時完全不會發出任何外部請求）

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
    │   ├── problems-data.js     # 全站題目總表資料（每列多一欄「主題 id」，橫跨所有主題合併存放）
    │   ├── progress.js          # 練習進度追蹤 + Firebase 登入/雲端同步（全站共用一份）
    │   └── firebase-config.js   # 你的 Firebase 專案金鑰（預設是佔位值＝本機模式）
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

只需要 Python 3 標準函式庫，沒有其他相依套件。腳本會印出所有寫入的檔案。

### 本機預覽

因為網站本身沒有使用 `fetch()`／XHR 讀取其他檔案（共用樣式與腳本都是透過 `<link>`／`<script src>` 載入，這在 `file://` 協定下也能正常運作），最簡單的預覽方式是**直接用瀏覽器開啟 `site/index.html`**，不需要啟動任何伺服器。（雲端進度同步功能需要連上 Firebase；沒有網路或還沒設定 Firebase 時，其餘所有功能——包含本機進度標記——都不受影響。）

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

網站是純靜態的（GitHub Pages 沒有自己的伺服器），沒辦法自己驗證使用者身份、存資料。要做到「不同裝置登入同一個帳號、看到相同的練習進度」，必須接上一個雲端服務——這裡選用 **Firebase**（Google 的免費 BaaS：Authentication + Firestore），因為它的 SDK 可以完全在瀏覽器端運作，不需要自己架後端伺服器，且免費額度（Spark Plan）對這種規模的個人使用完全足夠。

**在你完成下面的設定之前，網站會自動停留在「本機模式」**：練習進度照樣能標記，只是存在 `localStorage`、換瀏覽器/裝置就看不到——不會有任何錯誤或壞掉的畫面，側欄只會顯示「☁️ 尚未設定雲端同步」。

### 設定步驟

1. **建立 Firebase 專案**
   - 到 [Firebase Console](https://console.firebase.google.com)，用你的 Google 帳號登入
   - 點「新增專案」，取個名字（例如 `algo-guide`），一路下一步（可以關閉 Google Analytics，用不到）

2. **開啟 Google 登入**
   - 左側選單 **Authentication → Sign-in method**（或「開始使用」後進到這頁）
   - 啟用 **Google** 這個登入提供者，設定一個支援電子郵件後儲存

3. **設定授權網域**（重要，不做這步登入會失敗）
   - 同樣在 Authentication 頁面，點 **Settings → Authorized domains**
   - 加入你的 GitHub Pages 網域，例如 `youyun8.github.io`（Firebase 預設只信任它自己配的網域和 `localhost`）

4. **建立 Firestore 資料庫**
   - 左側選單 **Firestore Database → 建立資料庫**
   - 位置隨意選（挑離你近的），**先選「正式版模式（production mode）」**（安全規則下一步會設定成只能存取自己的資料）

5. **設定 Firestore 安全規則**
   - **Firestore Database → 規則**分頁，貼上：
     ```
     rules_version = '2';
     service cloud.firestore {
       match /databases/{database}/documents {
         match /users/{uid} {
           allow read, write: if request.auth != null && request.auth.uid == uid;
         }
       }
     }
     ```
   - 這確保每個使用者只能讀寫自己 `users/{自己的 uid}` 那份文件，看不到、也改不到別人的進度

6. **取得設定值**
   - **專案設定**（左上角齒輪圖示）→ 一般 → 往下捲到「你的應用程式」→ 點 `</>`（網頁應用程式圖示）新增一個應用程式
   - 取個暱稱（例如 `algo-guide-web`），**不需要**勾選「同時設定 Firebase Hosting」
   - 建立後會看到一段 `firebaseConfig = { apiKey: "...", authDomain: "...", ... }`，把這幾個值複製起來

7. **貼進網站設定檔**
   - 打開 `site/assets/firebase-config.js`，把預設的佔位值換成第 6 步拿到的實際值：
     ```js
     window.FIREBASE_CONFIG = {
       apiKey: "AIzaSy...",
       authDomain: "algo-guide-xxxxx.firebaseapp.com",
       projectId: "algo-guide-xxxxx",
       storageBucket: "algo-guide-xxxxx.appspot.com",
       messagingSenderId: "1234567890",
       appId: "1:1234567890:web:abcdef123456"
     };
     ```
   - commit、push（或走一般部署流程），網站偵測到 `apiKey` 不再是 `"YOUR_API_KEY"` 後就會自動載入 Firebase SDK、側欄出現「🔑 用 Google 同步進度」按鈕。因為全站只有一份 `assets/`，設定一次就對所有主題生效

> `apiKey` 這類 Firebase 前端設定值本來就設計成公開在瀏覽器程式碼裡（它不是密碼），真正的存取控制來自第 5 步的 Firestore 安全規則——這也是為什麼那條規則不能省略。

### 資料怎麼存、怎麼同步

- 每人的進度存在 Firestore 的 `users/{該使用者的 uid}` 這份文件裡，格式是 `{ progress: { "lc-630": "done", "poj-2287": "review", ... } }`（key 是題目 id，可在 `assets/problems-data.js` 每列第 7 欄、或 `topics/<id>/content/s2-*.html` 卡片的 `data-problem-id` 屬性看到；全站所有主題讀寫同一份文件）
- 登入後 `assets/progress.js` 用 Firestore 的 `onSnapshot` 即時監聽該文件，換裝置登入同一帳號會立刻讀到雲端的最新進度；兩個裝置同時開著網站，其中一台標記進度後，另一台也會即時更新（不用重新整理）
- 第一次登入、雲端還沒有任何資料時，會把你登入前在本機標記的進度一次推上雲端，成為之後同步的起點
- 登出後，網站退回只用瀏覽器 `localStorage` 裡的本機快取（不會遺失剛剛同步過的資料，只是不會再跨裝置更新）

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
| 點「用 Google 同步進度」沒反應或跳出 `auth/unauthorized-domain` | 部署後的網域沒有加進 Firebase 的授權網域清單 | Firebase Console → Authentication → Settings → Authorized domains，加入你的 `*.github.io` 網域 |
| 登入後進度沒有同步、Console 出現 `Missing or insufficient permissions` | Firestore 安全規則沒設定，或設定的 `uid` 條件寫錯 | 對照上方「跨裝置進度同步」第 5 步重新貼一次安全規則，並確認是發布（Publish）過的 |
| 側欄一直顯示「☁️ 尚未設定雲端同步」 | `assets/firebase-config.js` 還是預設的 `"YOUR_API_KEY"` 佔位值 | 依照「跨裝置進度同步」章節，把 Firebase 專案的實際設定值貼進該檔案並重新部署 |

### 自訂網域（選用）

若要掛自訂網域，在 `site/` 底下新增一個 `CNAME` 檔（內容為你的網域，如 `algo.example.com`），`build.py` 不會動到這個檔案，正常 commit 進去即可；同時要在網域的 DNS 設定 `CNAME` 指向 `<owner>.github.io`。

---

## 📄 授權與題目來源

題目連結指向各原始平台（LeetCode／力扣、Codeforces、AtCoder、洛谷、POJ、UVa、USACO、NOI/NOIP/APIO 官方或鏡像站），本站僅整理分類與提供思路說明，不重製題目內容。
