/* ═══════════════════════════════════════════════════════════════
   DP 上分攻略 — 共用行為
   1) 讀取／套用使用者設定（主題、字體大小、版面寬度）— 立即執行，避免畫面閃爍
   2) DOMContentLoaded 後：設定面板互動、手機側欄、目錄高亮、程式碼語法上色、
      題目總表篩選（僅在該頁存在對應元素時執行）
   ═══════════════════════════════════════════════════════════════ */
(function () {
  "use strict";

  var STORE_KEY = "dp-settings";
  var LEGACY_THEME_KEY = "dp-theme"; // 舊版單一主題設定，仍相容讀取

  var DEFAULTS = { theme: "system", fontSize: "md", width: "normal" };
  var FONT_PX = { sm: "14px", md: "16px", lg: "18px", xl: "21px" };
  var WIDTH_PX = { narrow: "720px", normal: "960px", wide: "1200px", full: "none" };

  function loadSettings() {
    var s = Object.assign({}, DEFAULTS);
    try {
      var raw = localStorage.getItem(STORE_KEY);
      if (raw) Object.assign(s, JSON.parse(raw));
      else {
        var legacy = localStorage.getItem(LEGACY_THEME_KEY);
        if (legacy === "light" || legacy === "dark") s.theme = legacy;
      }
    } catch (e) { /* localStorage 不可用時使用預設值 */ }
    return s;
  }

  function saveSettings(s) {
    try { localStorage.setItem(STORE_KEY, JSON.stringify(s)); } catch (e) {}
  }

  function applySettings(s) {
    var root = document.documentElement;
    if (s.theme === "light" || s.theme === "dark") root.dataset.theme = s.theme;
    else delete root.dataset.theme;
    root.style.setProperty("--content-fs", FONT_PX[s.fontSize] || FONT_PX.md);
    root.style.setProperty("--content-max", WIDTH_PX[s.width] || WIDTH_PX.normal);
  }

  var settings = loadSettings();
  applySettings(settings); // 立即套用，避免深色模式/字體閃爍

  function setSetting(key, value) {
    settings[key] = value;
    applySettings(settings);
    saveSettings(settings);
    syncPanelUI();
  }

  /* ── 設定面板 ── */
  var panelWired = false;
  function syncPanelUI() {
    var overlay = document.getElementById("settingsOverlay");
    if (!overlay) return;
    overlay.querySelectorAll(".seg button").forEach(function (btn) {
      var group = btn.closest(".seg").dataset.group;
      btn.classList.toggle("active", settings[group] === btn.dataset.value);
    });
  }

  function initSettingsPanel() {
    var btn = document.getElementById("settingsBtn");
    var overlay = document.getElementById("settingsOverlay");
    if (!btn || !overlay || panelWired) return;
    panelWired = true;

    function open() { overlay.hidden = false; syncPanelUI(); }
    function close() { overlay.hidden = true; }

    btn.addEventListener("click", open);
    overlay.addEventListener("click", function (e) { if (e.target === overlay) close(); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && !overlay.hidden) close(); });
    var closeBtn = document.getElementById("settingsCloseBtn");
    if (closeBtn) closeBtn.addEventListener("click", close);

    overlay.querySelectorAll(".seg button").forEach(function (b) {
      b.addEventListener("click", function () {
        setSetting(b.closest(".seg").dataset.group, b.dataset.value);
      });
    });

    var resetBtn = document.getElementById("settingsResetBtn");
    if (resetBtn) resetBtn.addEventListener("click", function () {
      settings = Object.assign({}, DEFAULTS);
      applySettings(settings);
      saveSettings(settings);
      syncPanelUI();
    });
  }

  /* ── 手機側欄抽屜 ── */
  function initMobileNav() {
    var sb = document.getElementById("sidebar");
    var mb = document.getElementById("menuBtn");
    if (!sb || !mb) return;
    mb.addEventListener("click", function () { sb.classList.toggle("open"); });
    sb.addEventListener("click", function (e) { if (e.target.tagName === "A") sb.classList.remove("open"); });
  }

  /* ── 目錄目前頁面高亮 ── */
  function initActiveNav() {
    var page = document.body.dataset.page;
    if (!page) return;
    var link = document.querySelector('#toc a[data-page="' + page + '"]');
    if (link) link.classList.add("active");
  }

  /* ── 輕量 C++/Python 語法上色 ── */
  var KW = {
    cpp: /\b(auto|break|case|catch|char|class|const|continue|default|do|double|else|enum|false|float|for|function|if|int|long|namespace|new|nullptr|operator|priority_queue|private|public|return|short|signed|sizeof|static|string|struct|switch|template|this|throw|true|try|typedef|typename|union|unsigned|using|vector|void|while|multiset|set|map|pair|greater|less)\b/g,
    py: /\b(and|as|assert|break|class|continue|def|del|elif|else|except|False|finally|for|from|global|if|import|in|is|lambda|None|not|or|pass|print|raise|return|True|try|while|with|yield|range|len|max|min)\b/g
  };
  function esc(s) { return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }
  function hl(src, lang) {
    var parts = [];
    var re = lang === "cpp"
      ? /(\/\/[^\n]*|\/\*[\s\S]*?\*\/|"(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*')/g
      : /(#[^\n]*|"""[\s\S]*?"""|"(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*')/g;
    var last = 0, m;
    function plain(t) {
      return esc(t)
        .replace(KW[lang], '<span class="tok-kw">$&</span>')
        .replace(/\b(\d+(?:\.\d+)?(?:LL|L|f)?)\b/g, '<span class="tok-num">$1</span>')
        .replace(/(\w+)(\()/g, '<span class="tok-fn">$1</span>$2');
    }
    while ((m = re.exec(src))) {
      parts.push(plain(src.slice(last, m.index)));
      var cls = (m[0][0] === "/" || m[0][0] === "#") ? "tok-com" : "tok-str";
      parts.push('<span class="' + cls + '">' + esc(m[0]) + "</span>");
      last = m.index + m[0].length;
    }
    parts.push(plain(src.slice(last)));
    return parts.join("");
  }
  function initSyntaxHighlight() {
    document.querySelectorAll("code.lang-cpp, code.lang-py").forEach(function (el) {
      var lang = el.classList.contains("lang-cpp") ? "cpp" : "py";
      el.innerHTML = hl(el.textContent, lang);
    });
  }

  /* ── 題目總表篩選（僅題目總表頁面使用） ── */
  function initProblemsPage() {
    var tbl = document.getElementById("ptbl");
    var data = window.DP_PROBLEMS;
    if (!tbl || !data) return;

    var state = { text: "", stars: new Set(), tags: new Set() };
    var ALLTAGS = Array.from(new Set(data.flatMap(function (r) { return r[4]; })));
    var starHTML = function (n) { return '<span class="stars s' + n + '">' + "★".repeat(n) + "</span>"; };

    function chip(label, onToggle) {
      var el = document.createElement("span");
      el.className = "chip clickable";
      el.textContent = label;
      el.onclick = function () {
        el.classList.toggle("on");
        onToggle(el.classList.contains("on"));
        render();
      };
      return el;
    }
    var starsBox = document.getElementById("f-stars");
    var tagsBox = document.getElementById("f-tags");
    for (var s = 1; s <= 5; s++) {
      (function (s) {
        starsBox.appendChild(chip("★".repeat(s), function (on) { on ? state.stars.add(s) : state.stars.delete(s); }));
      })(s);
    }
    ALLTAGS.forEach(function (t) {
      tagsBox.appendChild(chip(t, function (on) { on ? state.tags.add(t) : state.tags.delete(t); }));
    });
    var textInput = document.getElementById("f-text");
    textInput.addEventListener("input", function (e) {
      state.text = e.target.value.trim().toLowerCase();
      render();
    });

    function render() {
      var tb = tbl.querySelector("tbody");
      tb.innerHTML = "";
      var shown = 0;
      data.forEach(function (row) {
        var name = row[0], src = row[1], url = row[2], st = row[3], tags = row[4], idea = row[5], id = row[6];
        if (state.stars.size && !state.stars.has(st)) return;
        if (state.tags.size && !Array.from(state.tags).some(function (t) { return tags.indexOf(t) !== -1; })) return;
        if (state.text && (name + src + idea + tags.join()).toLowerCase().indexOf(state.text) === -1) return;
        shown++;
        var tr = document.createElement("tr");
        if (id) tr.dataset.problemId = id;
        var link = url ? '<a href="' + url + '" target="_blank" rel="noopener">' + name + "</a>" : "<b>" + name + "</b>";
        tr.innerHTML = "<td>" + link + "</td><td>" + src + "</td><td>" + starHTML(st) + "</td>" +
          "<td>" + tags.map(function (t) { return '<span class="chip">' + t + "</span>"; }).join("") + "</td><td>" + idea + "</td>" +
          '<td class="progress-cell"></td>';
        tb.appendChild(tr);
      });
      document.getElementById("ptbl-count").textContent = "顯示 " + shown + " / " + data.length + " 題";
      if (window.DPProgress) window.DPProgress.paint();
    }
    var totalEl = document.getElementById("ptbl-total");
    if (totalEl) totalEl.textContent = data.length;
    render();
  }

  document.addEventListener("DOMContentLoaded", function () {
    initSettingsPanel();
    initMobileNav();
    initActiveNav();
    initSyntaxHighlight();
    initProblemsPage();
  });
})();
