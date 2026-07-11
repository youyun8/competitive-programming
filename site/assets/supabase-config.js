/* ═══════════════════════════════════════════════════════════════
   雲端進度同步設定（選用）

   在 Supabase 建立專案並執行 README.md 提供的資料表 SQL 後，從
   Project Settings → API 複製 Project URL 與 Publishable key。

   保留預設值時，網站只使用 localStorage，不會載入 Supabase SDK，
   也不會發出任何雲端請求。
   ═══════════════════════════════════════════════════════════════ */
window.SUPABASE_CONFIG = {
  url: "https://gcoezuhysnwknqokqhsl.supabase.co",
  publishableKey: "sb_publishable_8ik2y9dKnELP7nnV648IBQ_HOunjhy6"
};
