/* ═══════════════════════════════════════════════════════════════
   DP 上分攻略 — 練習進度追蹤 + 跨裝置雲端同步

   本機模式（預設）：進度存在 localStorage，換瀏覽器/裝置看不到彼此。
   雲端模式（設定好 assets/firebase-config.js 後自動啟用）：
     使用者用 Google 帳號登入 → 進度存進該帳號專屬的 Firestore 文件
     → 從任何裝置用同一 Google 帳號登入都會讀到同一份進度，且透過
       onSnapshot 即時監聽，多裝置同時開著也會互相同步。

   設定步驟請見 README.md「跨裝置進度同步」章節。
   ═══════════════════════════════════════════════════════════════ */
(function () {
  "use strict";

  var LOCAL_KEY = "dp-progress";
  var STATUSES = ["none", "review", "done"];
  var LABELS = { none: "尚未練習", review: "需複習", done: "已通過" };
  var ICONS = { none: "⬜", review: "🔶", done: "✅" };
  var FIREBASE_SDK_BASE = "https://www.gstatic.com/firebasejs/10.13.0/";

  var cache = loadLocal();
  var currentUser = null;
  var firebaseReady = false;
  var auth = null, db = null, unsubscribeDoc = null;

  function loadLocal() {
    try { return JSON.parse(localStorage.getItem(LOCAL_KEY) || "{}"); } catch (e) { return {}; }
  }
  function saveLocal() {
    try { localStorage.setItem(LOCAL_KEY, JSON.stringify(cache)); } catch (e) {}
  }

  function getStatus(id) { return cache[id] || "none"; }

  function setStatus(id, status) {
    cache[id] = status;
    saveLocal();
    paint();
    if (currentUser && db) {
      var update = { updatedAt: firebase.firestore.FieldValue.serverTimestamp() };
      update["progress." + id] = status;
      db.collection("users").doc(currentUser.uid).set(update, { merge: true })
        .catch(function (e) { console.error("[DPProgress] 寫入雲端失敗：", e); });
    }
  }

  function summary() {
    var s = { none: 0, review: 0, done: 0 };
    Object.keys(cache).forEach(function (id) {
      if (s[cache[id]] !== undefined) s[cache[id]]++;
    });
    return s;
  }

  /* ── 每題的進度控制元件（⬜/🔶/✅ 三顆小按鈕） ── */
  function controlHTML(id) {
    var st = getStatus(id);
    return '<span class="progress-ctl" data-for="' + id + '">' +
      STATUSES.map(function (s) {
        return '<button type="button" data-status="' + s + '" class="' + (s === st ? "active" : "") +
          '" aria-label="' + LABELS[s] + '" title="' + LABELS[s] + '">' + ICONS[s] + "</button>";
      }).join("") + "</span>";
  }

  function wireControl(el, id) {
    if (!el) return;
    el.querySelectorAll("button").forEach(function (btn) {
      btn.addEventListener("click", function (ev) {
        ev.preventDefault();
        setStatus(id, btn.dataset.status);
      });
    });
  }

  function applyStatusClass(target, id) {
    target.classList.remove("status-none", "status-review", "status-done");
    target.classList.add("status-" + getStatus(id));
  }

  /* 把控制元件塞進頁面上所有帶 data-problem-id 的地方（題目卡片 + 總表列），
     可重複呼叫（例如篩選後表格重繪、或雲端資料同步回來時）以刷新狀態。 */
  function paint() {
    document.querySelectorAll(".problem[data-problem-id]").forEach(function (card) {
      var id = card.dataset.problemId;
      applyStatusClass(card, id);
      var head = card.querySelector(".p-head");
      if (!head) return;
      var existing = head.querySelector(".progress-ctl");
      if (existing) existing.remove();
      head.insertAdjacentHTML("beforeend", controlHTML(id));
      wireControl(head.querySelector(".progress-ctl"), id);
    });
    document.querySelectorAll("tr[data-problem-id]").forEach(function (tr) {
      var id = tr.dataset.problemId;
      applyStatusClass(tr, id);
      var cell = tr.querySelector(".progress-cell");
      if (!cell) return;
      cell.innerHTML = controlHTML(id);
      wireControl(cell.querySelector(".progress-ctl"), id);
    });
    renderSummary();
  }

  function renderSummary() {
    var el = document.getElementById("progress-summary");
    if (!el) return;
    var s = summary();
    var total = (window.DP_PROBLEMS && window.DP_PROBLEMS.length) || (s.none + s.review + s.done);
    var untouched = Math.max(0, total - s.review - s.done);
    el.textContent = "✅ 已通過 " + s.done + "　🔶 需複習 " + s.review + "　⬜ 尚未練習 " + untouched;
  }

  /* ── 登入狀態顯示 ── */
  function renderAuthUI() {
    var box = document.getElementById("authBox");
    if (!box) return;
    if (!isConfigured(window.FIREBASE_CONFIG)) {
      box.innerHTML = '<div class="authbox-msg" title="尚未設定 assets/firebase-config.js，進度僅存在本機瀏覽器">☁️ 尚未設定雲端同步</div>';
      return;
    }
    if (!firebaseReady) {
      box.innerHTML = '<div class="authbox-msg">☁️ 連線中…</div>';
      return;
    }
    if (currentUser) {
      var label = currentUser.displayName || currentUser.email || "已登入";
      box.innerHTML =
        '<div class="authbox-user">' +
        '<span class="authbox-email" title="' + esc(currentUser.email || "") + '">👤 ' + esc(label) + "</span>" +
        '<button id="signOutBtn" class="toolbtn">登出</button>' +
        "</div>";
      var so = document.getElementById("signOutBtn");
      if (so) so.addEventListener("click", function () { auth.signOut(); });
    } else {
      box.innerHTML = '<button id="signInBtn" class="toolbtn">🔑 用 Google 同步進度</button>';
      var si = document.getElementById("signInBtn");
      if (si) si.addEventListener("click", function () {
        auth.signInWithPopup(new firebase.auth.GoogleAuthProvider())
          .catch(function (e) { alert("登入失敗：" + e.message); });
      });
    }
  }
  function esc(s) { return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }

  /* ── Firebase 初始化：設定檔沒填就完全不載入 SDK，維持純本機模式 ── */
  function isConfigured(cfg) {
    return !!(cfg && cfg.apiKey && cfg.apiKey.indexOf("YOUR_") !== 0);
  }

  function loadScript(src) {
    return new Promise(function (resolve, reject) {
      var s = document.createElement("script");
      s.src = src;
      s.onload = resolve;
      s.onerror = function () { reject(new Error("載入失敗：" + src)); };
      document.head.appendChild(s);
    });
  }

  function initFirebase() {
    var cfg = window.FIREBASE_CONFIG;
    if (!isConfigured(cfg)) return;

    loadScript(FIREBASE_SDK_BASE + "firebase-app-compat.js")
      .then(function () { return loadScript(FIREBASE_SDK_BASE + "firebase-auth-compat.js"); })
      .then(function () { return loadScript(FIREBASE_SDK_BASE + "firebase-firestore-compat.js"); })
      .then(function () {
        firebase.initializeApp(cfg);
        auth = firebase.auth();
        db = firebase.firestore();
        firebaseReady = true;
        renderAuthUI();

        auth.onAuthStateChanged(function (user) {
          if (unsubscribeDoc) { unsubscribeDoc(); unsubscribeDoc = null; }
          currentUser = user;
          renderAuthUI();
          if (!user) return;

          var ref = db.collection("users").doc(user.uid);
          unsubscribeDoc = ref.onSnapshot(function (snap) {
            if (snap.exists && snap.data().progress) {
              cache = Object.assign({}, cache, snap.data().progress);
              saveLocal();
            } else if (Object.keys(cache).length) {
              // 遠端還沒有資料：把登入前累積的本機進度推上去，成為雲端的起點
              ref.set({ progress: cache }, { merge: true });
            }
            paint();
          }, function (err) { console.error("[DPProgress] 同步監聽失敗：", err); });
        });
      })
      .catch(function (e) {
        console.error("[DPProgress] Firebase 載入失敗：", e);
        renderAuthUI();
      });
  }

  document.addEventListener("DOMContentLoaded", function () {
    paint();
    renderAuthUI();
    initFirebase();
  });

  window.DPProgress = { getStatus: getStatus, setStatus: setStatus, paint: paint, summary: summary };
})();
