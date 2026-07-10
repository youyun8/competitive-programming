/* ═══════════════════════════════════════════════════════════════
   雲端進度同步設定（選用）

   在 https://console.firebase.google.com 建立免費專案後，把「專案設定 →
   一般 → 您的應用程式 → SDK 設定和設定」裡的設定值貼到下面。完整步驟見
   README.md「跨裝置進度同步」章節。

   只要 apiKey 還是下面這個 "YOUR_API_KEY" 預設值，網站就會停留在「本機
   模式」：練習進度仍然可以正常標記，只是只存在目前這個瀏覽器，不會有
   登入按鈕、也不會跨裝置同步。這完全不影響網站其他功能。
   ═══════════════════════════════════════════════════════════════ */
window.FIREBASE_CONFIG = {
  apiKey: "YOUR_API_KEY",
  authDomain: "YOUR_PROJECT.firebaseapp.com",
  projectId: "YOUR_PROJECT",
  storageBucket: "YOUR_PROJECT.appspot.com",
  messagingSenderId: "YOUR_SENDER_ID",
  appId: "YOUR_APP_ID"
};
