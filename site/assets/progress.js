/* ═══════════════════════════════════════════════════════════════
   演算法策略圖鑑 — 練習進度追蹤 + Supabase 跨裝置同步

   預設只使用 localStorage。設定 assets/supabase-config.js 後，使用者
   可以用 Email magic link 登入；登入時讀取雲端進度，每次標記後立即
   upsert 自己的資料列，回到分頁時再同步一次其他裝置的最新變更。
   ═══════════════════════════════════════════════════════════════ */
(function () {
  "use strict";

  var LOCAL_KEY = "algo-guide-progress";
  var STATUSES = ["none", "review", "done"];
  var LABELS = { none: "尚未練習", review: "需複習", done: "已通過" };
  var ICONS = { none: "⬜", review: "🔶", done: "✅" };
  var SUPABASE_SDK_URL =
    "https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2";

  var cache = loadLocal();
  var currentUser = null;
  var cloudClient = null;
  var cloudReady = false;
  var cloudError = "";
  var authMessage = "";
  var lastSyncAt = 0;

  function loadLocal() {
    try {
      return JSON.parse(localStorage.getItem(LOCAL_KEY) || "{}");
    } catch (error) {
      console.warn("[Progress] 無法讀取本機進度：", error);
      return {};
    }
  }

  function saveLocal() {
    try {
      localStorage.setItem(LOCAL_KEY, JSON.stringify(cache));
    } catch (error) {
      console.warn("[Progress] 無法儲存本機進度：", error);
    }
  }

  function getStatus(id) {
    return cache[id] || "none";
  }

  function setStatus(id, status) {
    if (STATUSES.indexOf(status) === -1) return;
    cache[id] = status;
    saveLocal();
    paint();
    if (currentUser && cloudClient) {
      writeCloudStatus(id, status);
    }
  }

  function writeCloudStatus(id, status) {
    cloudClient
      .from("user_progress")
      .upsert(
        {
          user_id: currentUser.id,
          problem_id: id,
          status: status,
          updated_at: new Date().toISOString()
        },
        { onConflict: "user_id,problem_id" }
      )
      .then(function (result) {
        if (result.error) {
          console.error("[Progress] 寫入雲端失敗：", result.error);
        }
      });
  }

  function summary() {
    var result = { none: 0, review: 0, done: 0 };
    Object.keys(cache).forEach(function (id) {
      if (result[cache[id]] !== undefined) {
        result[cache[id]]++;
      }
    });
    return result;
  }

  function controlHTML(id) {
    var status = getStatus(id);
    return (
      '<span class="progress-ctl" data-for="' +
      id +
      '">' +
      STATUSES.map(function (candidate) {
        return (
          '<button type="button" data-status="' +
          candidate +
          '" class="' +
          (candidate === status ? "active" : "") +
          '" aria-label="' +
          LABELS[candidate] +
          '" title="' +
          LABELS[candidate] +
          '">' +
          ICONS[candidate] +
          "</button>"
        );
      }).join("") +
      "</span>"
    );
  }

  function wireControl(element, id) {
    if (!element) return;
    element.querySelectorAll("button").forEach(function (button) {
      button.addEventListener("click", function (event) {
        event.preventDefault();
        setStatus(id, button.dataset.status);
      });
    });
  }

  function applyStatusClass(target, id) {
    target.classList.remove("status-none", "status-review", "status-done");
    target.classList.add("status-" + getStatus(id));
  }

  function paint() {
    document.querySelectorAll(".problem[data-problem-id]").forEach(function (card) {
      var id = card.dataset.problemId;
      var head = card.querySelector(".p-head");
      applyStatusClass(card, id);
      if (!head) return;
      var existing = head.querySelector(".progress-ctl");
      if (existing) existing.remove();
      head.insertAdjacentHTML("beforeend", controlHTML(id));
      wireControl(head.querySelector(".progress-ctl"), id);
    });
    document.querySelectorAll("tr[data-problem-id]").forEach(function (row) {
      var id = row.dataset.problemId;
      var cell = row.querySelector(".progress-cell");
      applyStatusClass(row, id);
      if (!cell) return;
      cell.innerHTML = controlHTML(id);
      wireControl(cell.querySelector(".progress-ctl"), id);
    });
    renderSummary();
  }

  function renderSummary() {
    var element = document.getElementById("progress-summary");
    if (!element) return;
    var counts = summary();
    var total =
      (window.PROBLEMS && window.PROBLEMS.length) ||
      counts.none + counts.review + counts.done;
    var untouched = Math.max(0, total - counts.review - counts.done);
    element.textContent =
      "✅ 已通過 " +
      counts.done +
      "　🔶 需複習 " +
      counts.review +
      "　⬜ 尚未練習 " +
      untouched;
  }

  function escapeHTML(value) {
    return String(value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function isConfigured(config) {
    return !!(
      config &&
      config.url &&
      config.publishableKey &&
      config.url.indexOf("YOUR_") !== 0 &&
      config.publishableKey.indexOf("YOUR_") !== 0
    );
  }

  function renderAuthUI() {
    var box = document.getElementById("authBox");
    if (!box) return;
    if (!isConfigured(window.SUPABASE_CONFIG)) {
      box.innerHTML =
        '<div class="authbox-msg" title="尚未設定 assets/supabase-config.js，進度僅存在本機瀏覽器">☁️ 本機進度模式</div>';
      return;
    }
    if (cloudError) {
      box.innerHTML =
        '<div class="authbox-msg">' + escapeHTML(cloudError) + "</div>";
      return;
    }
    if (!cloudReady) {
      box.innerHTML = '<div class="authbox-msg">☁️ 連線中…</div>';
      return;
    }
    if (currentUser) {
      box.innerHTML =
        '<div class="authbox-user">' +
        '<span class="authbox-email" title="' +
        escapeHTML(currentUser.email || "") +
        '">👤 ' +
        escapeHTML(currentUser.email || "已登入") +
        "</span>" +
        '<button id="signOutBtn" class="toolbtn">登出</button>' +
        "</div>" +
        (authMessage
          ? '<div class="authbox-msg">' + escapeHTML(authMessage) + "</div>"
          : "");
      document.getElementById("signOutBtn").addEventListener("click", function () {
        cloudClient.auth.signOut();
      });
      return;
    }

    box.innerHTML =
      '<form id="signInForm" class="authbox-form">' +
      '<label for="syncEmail">跨裝置同步</label>' +
      '<input id="syncEmail" type="email" autocomplete="email" placeholder="Email" required>' +
      '<button class="toolbtn" type="submit">寄送登入連結</button>' +
      "</form>" +
      (authMessage
        ? '<div class="authbox-msg">' + escapeHTML(authMessage) + "</div>"
        : "");
    document.getElementById("signInForm").addEventListener("submit", signIn);
  }

  function signIn(event) {
    event.preventDefault();
    var email = document.getElementById("syncEmail").value.trim();
    if (!email) return;
    authMessage = "正在寄送…";
    renderAuthUI();
    cloudClient.auth
      .signInWithOtp({
        email: email,
        options: { emailRedirectTo: window.location.href.split("#")[0] }
      })
      .then(function (result) {
        authMessage = result.error
          ? "寄送失敗：" + result.error.message
          : "登入連結已寄出，請檢查信箱。";
        renderAuthUI();
      });
  }

  function loadScript(src) {
    return new Promise(function (resolve, reject) {
      var script = document.createElement("script");
      script.src = src;
      script.onload = resolve;
      script.onerror = function () {
        reject(new Error("載入失敗：" + src));
      };
      document.head.appendChild(script);
    });
  }

  function syncCloudProgress() {
    if (!currentUser || !cloudClient) return Promise.resolve();
    var userId = currentUser.id;
    lastSyncAt = Date.now();
    return cloudClient
      .from("user_progress")
      .select("problem_id,status")
      .eq("user_id", userId)
      .then(function (result) {
        if (result.error) throw result.error;
        if (!currentUser || currentUser.id !== userId) return;
        var remote = {};
        (result.data || []).forEach(function (row) {
          if (STATUSES.indexOf(row.status) !== -1) {
            remote[row.problem_id] = row.status;
          }
        });

        var missingRows = Object.keys(cache)
          .filter(function (id) {
            return remote[id] === undefined;
          })
          .map(function (id) {
            return {
              user_id: userId,
              problem_id: id,
              status: cache[id],
              updated_at: new Date().toISOString()
            };
          });
        cache = Object.assign({}, cache, remote);
        saveLocal();
        paint();
        authMessage = "已同步";
        renderAuthUI();

        if (missingRows.length) {
          return cloudClient
            .from("user_progress")
            .upsert(missingRows, { onConflict: "user_id,problem_id" })
            .then(function (writeResult) {
              if (writeResult.error) throw writeResult.error;
            });
        }
      })
      .catch(function (error) {
        if (!currentUser || currentUser.id !== userId) return;
        authMessage = "同步失敗，進度仍保存在本機。";
        console.error("[Progress] 同步失敗：", error);
        renderAuthUI();
      });
  }

  function handleSession(session) {
    currentUser = session && session.user ? session.user : null;
    authMessage = "";
    renderAuthUI();
    if (currentUser) {
      syncCloudProgress();
    }
  }

  function initCloud() {
    var config = window.SUPABASE_CONFIG;
    if (!isConfigured(config)) return;
    loadScript(SUPABASE_SDK_URL)
      .then(function () {
        cloudClient = window.supabase.createClient(
          config.url,
          config.publishableKey
        );
        cloudReady = true;
        renderAuthUI();
        return cloudClient.auth.getSession();
      })
      .then(function (result) {
        if (result.error) throw result.error;
        handleSession(result.data.session);
        cloudClient.auth.onAuthStateChange(function (event, session) {
          window.setTimeout(function () {
            handleSession(session);
          }, 0);
        });
      })
      .catch(function (error) {
        cloudError = "雲端服務載入失敗，已改用本機模式。";
        console.error("[Progress] Supabase 初始化失敗：", error);
        renderAuthUI();
      });
  }

  document.addEventListener("visibilitychange", function () {
    if (
      document.visibilityState === "visible" &&
      currentUser &&
      Date.now() - lastSyncAt > 10000
    ) {
      syncCloudProgress();
    }
  });

  document.addEventListener("DOMContentLoaded", function () {
    paint();
    renderAuthUI();
    initCloud();
  });

  window.Progress = {
    getStatus: getStatus,
    setStatus: setStatus,
    paint: paint,
    summary: summary,
    sync: syncCloudProgress
  };
})();
