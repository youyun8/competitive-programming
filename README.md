# competitive-programming

程式競賽主題攻略站——每個演算法主題一個獨立的純靜態多頁網站，可離線瀏覽，選用性的雲端練習進度同步。

**🌐 線上網站：**

| 攻略 | 網址 | 內容 |
|---|---|---|
| 📚 **貪心演算法完全指南** | https://youyun8.github.io/competitive-programming/ | 11 大策略分類、四大證明技巧、假貪心陷阱、58 題總表與路線圖 |
| 📈 **DP 上分攻略** | https://youyun8.github.io/competitive-programming/dp/ | 動態規劃 13 大策略分類、狀態設計方法論、86 題總表與路線圖 |

兩個攻略都是從入門（★）到程式競賽專家（★★★★★）的策略分類與題目整理，並互相交叉引用（例如貪心的 slope trick ↔ DP 的凸優化視角）。

- **貪心指南**涵蓋：排序貪心、區間全家桶、交換論證排程、反悔貪心、堆積貪心、字典序、數學貪心、圖上貪心、貪心×資料結構、貪心×二分、slope trick／擬陣／模擬費用流專題。
- **DP 上分攻略**涵蓋：線性、網格、背包全家桶、區間、雙序列、狀態機、狀壓、樹上（含換根）、數位、計數與期望、圖上與博弈、DP 優化技術（單調佇列／斜率／Knuth／分治／wqs 二分／矩陣冪／bitset）、專家專題（輪廓線與插頭、SOS、連通塊插入、動態 DP、DP 套 DP），外加常見錯誤除錯手冊與狀態設計方法論。

---

## ✨ 網站功能（兩個攻略共通）

- **每個子主題一個獨立頁面**（貪心 17 頁、DP 19 頁），側欄導覽會依目前頁面自動高亮，頁尾提供「上一節 / 下一節」可依順序閱讀
- **⚙️ 顯示設定面板**（每頁側欄都有）：
  - 主題：淺色 / 深色 / 跟隨系統
  - 內文字體大小：小 / 中 / 大 / 特大
  - 版面寬度：窄 / 預設 / 寬 / 全螢幕
  - 設定存在瀏覽器 `localStorage`（兩站各自獨立：`greedy-settings` / `dp-settings`），切換頁面或重新整理都會保留
- **練習進度追蹤 + 跨裝置同步**：每題（策略頁面的題目卡片、題目總表的每一列）都能標記「尚未練習 ⬜／需複習 🔶／已通過 ✅」；用 Google 帳號登入後，同一帳號在不同裝置登入會看到相同進度（見下方「[跨裝置進度同步](#️-跨裝置進度同步選用)」設定）。兩個攻略共用同一份 Firestore 使用者文件（題目 id 全站唯一，同一題在兩站會同步狀態）。**未設定雲端同步時完全不影響使用**——進度會退回只存在目前瀏覽器
- **題目總表**（各自的 `pages/problems.html`）可依難度星級、策略標籤（可複選）與關鍵字即時篩選，並顯示已通過/需複習/尚未練習的統計
- 手機自動收合為抽屜式側欄；程式碼區塊有自寫的輕量 C++ / Python 語法上色
- 教學內容本身零外部依賴、可離線使用；只有「雲端進度同步」這一項功能會在設定好之後連線 Google 的 Firebase 服務（未設定時完全不會發出任何外部請求）

---

## 📁 專案結構

```
competitive-programming/
├── .github/workflows/
│   └── deploy-pages.yml       # GitHub Actions：組裝兩個攻略後部署到 GitHub Pages
├── greedy-guide/               # 貪心演算法完全指南（部署於網站根目錄 /）
│   ├── index.html              # 首頁（由 build.py 產生，勿手動編輯）
│   ├── pages/                  # 產生出的內容頁（theory / strategies/* / pitfalls / proofs / problems / roadmap）
│   ├── content/                # ★ 教學內容的唯一來源（source of truth）
│   ├── assets/                 # site.css / site.js / problems-data.js / progress.js / firebase-config.js
│   ├── build.py                # 靜態頁面產生器：content/ + 模板 → index.html / pages/*.html
│   └── OUTLINE.md              # 內容大綱
└── dp-guide/                   # DP 上分攻略（部署於 /dp/）
    ├── index.html              # 首頁（由 build.py 產生，勿手動編輯）
    ├── pages/                  # theory / strategies/01-linear … 13-expert / pitfalls / method / problems / roadmap
    ├── content/                # ★ 教學內容的唯一來源
    │   ├── s0-intro.html       # 首頁導讀
    │   ├── s1-theory.html      # DP 思考框架
    │   ├── s2-1.html … s2-13.html  # 13 個策略分類
    │   ├── s3-pitfalls.html    # 常見錯誤與除錯
    │   ├── s4-method.html      # 狀態設計方法論
    │   ├── s5-problems.html    # 題目總表骨架
    │   └── s6-roadmap.html     # 學習路線圖
    ├── assets/                 # 與 greedy 同構（storage key 與資料變數名不同：DP_PROBLEMS / dp-progress）
    ├── build.py
    └── OUTLINE.md
```

**內容與版面是分離的**（兩個攻略同一套機制）：`content/*.html` 只放教學內文（不含側欄、設定面板等版面），`build.py` 負責把內文套上共用版面模板，產生最終要部署的靜態頁面。這代表：

- ✅ 修改教學內容 → 編輯對應攻略 `content/` 底下的檔案 → 重新執行該攻略的 `build.py`
- ✅ 修改版面／導覽／設定功能 → 編輯 `build.py`（模板）或 `assets/site.css`／`assets/site.js` → 重新執行一次 `build.py` 讓所有頁面套上新版面
- 🚫 不要直接手動編輯 `index.html` 或 `pages/*.html`（下次執行 `build.py` 會被覆蓋）

---

## 🛠️ 本機開發

### 修改內容後重新產生頁面

```bash
cd greedy-guide && python3 build.py   # 或
cd dp-guide && python3 build.py
```

只需要 Python 3 標準函式庫，沒有其他相依套件。腳本會印出所有寫入的檔案。

### 本機預覽

因為網站本身沒有使用 `fetch()`／XHR 讀取其他檔案（共用樣式與腳本都是透過 `<link>`／`<script src>` 載入，這在 `file://` 協定下也能正常運作），最簡單的預覽方式是**直接用瀏覽器開啟 `greedy-guide/index.html` 或 `dp-guide/index.html`**，不需要啟動任何伺服器。（雲端進度同步功能需要連上 Firebase；沒有網路或還沒設定 Firebase 時，其餘所有功能——包含本機進度標記——都不受影響。唯一的例外是 DP 站頁尾「姊妹站」連結假設貪心指南在上一層目錄，這只有在部署後的網站結構下才成立。）

若想用本機伺服器模擬部署後的結構：

```bash
mkdir -p /tmp/site/dp && cp -r greedy-guide/. /tmp/site/ && cp -r dp-guide/. /tmp/site/dp/
cd /tmp/site && python3 -m http.server 8000
# 貪心：http://localhost:8000/    DP：http://localhost:8000/dp/
```

### 新增一個子主題頁面

1. 在該攻略的 `content/` 新增一個 `.html` 片段檔（只寫內文，從 `<h2>...</h2>` 開始）
2. 打開該攻略的 `build.py`，在檔案開頭的 `PAGES` 清單中新增一筆對應的 `dict(...)`（`id`、`path`、`nav`、`title`、`desc`、`frag`）
3. 若新頁面會被其他頁面用 `href="#s..."` 這種錨點引用，順便在 `ANCHOR_TO_ID` 對照表補上映射
4. 執行 `python3 build.py` 重新產生所有頁面（側欄導覽、上一頁/下一頁會自動更新）

### 新增一道題目

- 加進該攻略 `assets/problems-data.js` 的陣列裡，格式是 `[題名, 來源, URL, 難度星級, [標籤...], 關鍵想法, 題目id]`，**最後的 id 必須是全站唯一**（用來記錄練習進度，也用來讓同一題在題目總表與策略頁面卡片之間同步狀態；兩個攻略共用進度命名空間，同一題用同一個 id 就會跨站同步）
- 若同一題也會出現在 `content/s2-*.html` 的某張 `.problem` 卡片裡，把該卡片的 `<div class="problem">` 加上同一個 `data-problem-id="..."`，兩處的進度狀態就會自動連動
- id 命名慣例：`lc-455`、`poj-2287`、`luogu-p1080`、`cf-865d`、`atcoder-dp-o` 這種「判題平台+題號」小寫格式；沒有對應題號的概念性條目用 `misc-XX` 或描述性 slug（如 `tree-diameter`）

---

## ☁️ 跨裝置進度同步（選用）

網站是純靜態的（GitHub Pages 沒有自己的伺服器），沒辦法自己驗證使用者身份、存資料。要做到「不同裝置登入同一個帳號、看到相同的練習進度」，必須接上一個雲端服務——這裡選用 **Firebase**（Google 的免費 BaaS：Authentication + Firestore），因為它的 SDK 可以完全在瀏覽器端運作，不需要自己架後端伺服器，且免費額度（Spark Plan）對這種規模的個人使用完全足夠。

**在你完成下面的設定之前，網站會自動停留在「本機模式」**：練習進度照樣能標記，只是存在 `localStorage`、換瀏覽器/裝置就看不到——不會有任何錯誤或壞掉的畫面，側欄只會顯示「☁️ 尚未設定雲端同步」。

### 設定步驟

1. **建立 Firebase 專案**
   - 到 [Firebase Console](https://console.firebase.google.com)，用你的 Google 帳號登入
   - 點「新增專案」，取個名字（例如 `cp-guides`），一路下一步（可以關閉 Google Analytics，用不到）

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
   - 取個暱稱（例如 `cp-guides-web`），**不需要**勾選「同時設定 Firebase Hosting」
   - 建立後會看到一段 `firebaseConfig = { apiKey: "...", authDomain: "...", ... }`，把這幾個值複製起來

7. **貼進網站設定檔**
   - 打開 `greedy-guide/assets/firebase-config.js` 與 `dp-guide/assets/firebase-config.js`，把預設的佔位值換成第 6 步拿到的實際值（兩份填同一組值，兩站就會共用同一個 Firebase 專案與進度資料）：
     ```js
     window.FIREBASE_CONFIG = {
       apiKey: "AIzaSy...",
       authDomain: "cp-guides-xxxxx.firebaseapp.com",
       projectId: "cp-guides-xxxxx",
       storageBucket: "cp-guides-xxxxx.appspot.com",
       messagingSenderId: "1234567890",
       appId: "1:1234567890:web:abcdef123456"
     };
     ```
   - commit、push（或走一般部署流程），網站偵測到 `apiKey` 不再是 `"YOUR_API_KEY"` 後就會自動載入 Firebase SDK、側欄出現「🔑 用 Google 同步進度」按鈕

> `apiKey` 這類 Firebase 前端設定值本來就設計成公開在瀏覽器程式碼裡（它不是密碼），真正的存取控制來自第 5 步的 Firestore 安全規則——這也是為什麼那條規則不能省略。

### 資料怎麼存、怎麼同步

- 每人的進度存在 Firestore 的 `users/{該使用者的 uid}` 這份文件裡，格式是 `{ progress: { "lc-630": "done", "poj-2287": "review", ... } }`（key 是題目 id，可在各攻略 `assets/problems-data.js` 每列的最後一欄、或 `content/s2-*.html` 卡片的 `data-problem-id` 屬性看到；兩個攻略讀寫同一份文件）
- 登入後 `assets/progress.js` 用 Firestore 的 `onSnapshot` 即時監聽該文件，換裝置登入同一帳號會立刻讀到雲端的最新進度；兩個裝置同時開著網站，其中一台標記進度後，另一台也會即時更新（不用重新整理）
- 第一次登入、雲端還沒有任何資料時，會把你登入前在本機標記的進度一次推上雲端，成為之後同步的起點
- 登出後，網站退回只用瀏覽器 `localStorage` 裡的本機快取（不會遺失剛剛同步過的資料，只是不會再跨裝置更新）

---

## 🚀 部署（GitHub Actions → GitHub Pages）

網站透過 [`.github/workflows/deploy-pages.yml`](.github/workflows/deploy-pages.yml) 自動部署到 **GitHub Pages**，來源是這個 repo 本身（不需要另外的伺服器或第三方服務）。

流程：

1. **觸發**：每次 `push` 到 `main` 分支（或在 GitHub 的 Actions 頁面手動點 *Run workflow*，對應 `workflow_dispatch`）都會觸發部署
2. **Assemble site**：把 `greedy-guide/` 複製到 `_site/`（網站根目錄）、`dp-guide/` 複製到 `_site/dp/`，並移除不需要部署的 `content/`、`build.py`、`OUTLINE.md`——**貪心指南保持原本的根目錄網址不變**，DP 上分攻略掛在 `/dp/` 子路徑
3. **Setup Pages**（`configure-pages`）：確認 repo 的 GitHub Pages 設定，`enablement: true` 代表如果 Pages 還沒啟用，會自動把來源設成「GitHub Actions」
4. **Upload artifact + Deploy**：把 `_site/` 打包部署到 GitHub Pages 的 `github-pages` environment，並輸出網址

因為是靜態網站，CI **不需要**任何建置步驟（不跑 `npm install`、不跑 `build.py`）——各攻略底下已經是產生好的最終 HTML/CSS/JS，直接組裝部署即可。`build.py` 只在你本機修改內容後手動執行一次、把結果一起 commit 進去。

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

不想額外 commit 也能重新部署：到 **Actions → Deploy guides to GitHub Pages → Run workflow**，選擇 `main` 分支後執行（對應 workflow 裡的 `workflow_dispatch` 觸發條件）。

### 常見問題排解

| 現象 | 原因 | 解法 |
|---|---|---|
| workflow 執行失敗，幾秒內就結束，沒有詳細 log | Push 的分支不在觸發清單，或被 `github-pages` environment 的分支保護規則擋下 | 確認改動已經合併/推送到 `main`；GitHub Pages 的 environment 預設只允許 `main` 部署 |
| 部署成功但網站 404 | `_site/` 組裝路徑錯誤，或 `index.html` 不在對應目錄根部 | 確認 workflow 的 Assemble site 步驟：貪心在 `_site/`、DP 在 `_site/dp/`，且各自的 `index.html` 存在 |
| 樣式/腳本沒套用 | `assets/site.css`／`assets/site.js` 路徑算錯 | 檢查是不是手動改了 `pages/*.html` 而非改 `content/` 後重新跑 `build.py`（相對路徑深度由 `build.py` 自動計算，手動編輯容易算錯） |
| 修改了 `content/` 但網站沒變 | 忘記重新執行 `build.py`，或執行後忘記 commit 產生的檔案 | 到對應攻略目錄執行 `python3 build.py`，再 `git add` 產生出的 `index.html`／`pages/` 一起 commit |
| 第一次啟用 Pages 時 workflow 失敗 | 極少數情況下 organization 層級關閉了 Actions 自動管理 Pages 的權限 | 依照上方「首次啟用」的手動步驟，把 Source 設成 GitHub Actions 後重新觸發 |
| 點「用 Google 同步進度」沒反應或跳出 `auth/unauthorized-domain` | 部署後的網域沒有加進 Firebase 的授權網域清單 | Firebase Console → Authentication → Settings → Authorized domains，加入你的 `*.github.io` 網域 |
| 登入後進度沒有同步、Console 出現 `Missing or insufficient permissions` | Firestore 安全規則沒設定，或設定的 `uid` 條件寫錯 | 對照上方「跨裝置進度同步」第 5 步重新貼一次安全規則，並確認是發布（Publish）過的 |
| 側欄一直顯示「☁️ 尚未設定雲端同步」 | 該攻略的 `assets/firebase-config.js` 還是預設的 `"YOUR_API_KEY"` 佔位值 | 依照「跨裝置進度同步」章節，把 Firebase 專案的實際設定值貼進**兩個攻略**的設定檔並重新部署 |

### 自訂網域（選用）

若要掛自訂網域，在 `greedy-guide/` 底下新增一個 `CNAME` 檔（內容為你的網域，如 `cp.example.com`；組裝時會被複製到網站根目錄），`build.py` 不會動到這個檔案，正常 commit 進去即可；同時要在網域的 DNS 設定 `CNAME` 指向 `<owner>.github.io`。

---

## 📄 授權與題目來源

題目連結指向各原始平台（LeetCode／力扣、Codeforces、AtCoder、洛谷、POJ、UVa、USACO、NOI/NOIP/APIO 官方或鏡像站），本站僅整理分類與提供思路說明，不重製題目內容。
