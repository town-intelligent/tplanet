import React, { useEffect, useMemo, useState } from "react";
import { useTranslation } from "react-i18next";

// 之後可從登入/Context 拿
const DEFAULT_EMAIL = "minamj@nantou.gov.tw";

// 固定欄位（UI 使用 SDG1~SDG17）
const SDG_COLUMNS_UI = Array.from({ length: 17 }, (_, i) => `SDG${i + 1}`);
// 後端鍵名（API 使用 SDG-1~SDG-17）
const SDG_KEYS_API = Array.from({ length: 17 }, (_, i) => `SDG-${i + 1}`);

// 你希望表格行數固定、不會因為 API 沒資料而變少
const BASE_DEPARTMENTS = [
  "新北市小鎮風土股份有限公司",
  "南投縣小鎮文創股份有限公司",
  "花蓮縣真本事城鄉育成股份有限公司",
  "連江縣海島幌旅創生股份有限公司",
  "高雄市南方島嶼股份有限公司",
  "南投縣大美國際文化創意事業有限公司",
  "桃園市政府青年事務局",
];

const SDGHeatmap = () => {
  const [rows, setRows] = useState([]);       // 轉成 UI 欄位後的資料
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const { t } = useTranslation();

  // 你原本的 hardcode（當 API 掛了或還沒上新 view 參數時，用這個兜住）
  const HARDCODE = useMemo(
    () => [
      { 局處: "新北市小鎮風土股份有限公司", ...Object.fromEntries(SDG_COLUMNS_UI.map((k) => [k, 0])) },
      { 局處: "南投縣小鎮文創股份有限公司", ...Object.fromEntries(SDG_COLUMNS_UI.map((k) => [k, 0])) },
      { 局處: "花蓮縣真本事城鄉育成股份有限公司", ...Object.fromEntries(SDG_COLUMNS_UI.map((k) => [k, 0])) },
      { 局處: "連江縣海島幌旅創生股份有限公司", ...Object.fromEntries(SDG_COLUMNS_UI.map((k) => [k, 0])) },
      { 局處: "高雄市南方島嶼股份有限公司", ...Object.fromEntries(SDG_COLUMNS_UI.map((k) => [k, 0])) },
      { 局處: "南投縣大美國際文化創意事業有限公司", ...Object.fromEntries(SDG_COLUMNS_UI.map((k) => [k, 0])) },
      { 局處: "桃園市政府青年事務局", ...Object.fromEntries(SDG_COLUMNS_UI.map((k) => [k, 0])) },
    ],
    []
  );

  useEffect(() => {
    const fetchData = async () => {
      const base = import.meta.env.VITE_HOST_URL_TPLANET; // e.g. https://beta-tplanet-backend.ntsdgs.tw
      try {
        const res = await fetch(`${base}/dashboard/sdgs`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email: DEFAULT_EMAIL, view: "by_project_b" }),
        });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const json = await res.json();

        // 後端若還沒上新欄位，這裡會是 undefined → 走 fallback
        const list = json?.content?.sdgs_by_project_b ?? [];

        // 過濾空白/null project_b（隱匿 null）
        const clean = list.filter(
          (r) => ((r?.project_b ?? "").toString().trim().length > 0)
        );

        // project_b -> row（把 "SDG-1" 轉為 "SDG1"）
        const mapByProjectB = {};
        for (const row of clean) {
          const project_b = row.project_b;
          const uiRow = { 局處: project_b };
          SDG_KEYS_API.forEach((apiKey, idx) => {
            const uiKey = SDG_COLUMNS_UI[idx];
            uiRow[uiKey] = Number(row[apiKey] ?? 0);
          });
          mapByProjectB[project_b] = uiRow;
        }

        // 以 BASE_DEPARTMENTS 為基準：API 沒的補 0；API 多出的加在後面
        const merged = [
          ...BASE_DEPARTMENTS.map(
            (dep) =>
              mapByProjectB[dep] || {
                局處: dep,
                ...Object.fromEntries(SDG_COLUMNS_UI.map((k) => [k, 0])),
              }
          ),
          ...Object.keys(mapByProjectB)
            .filter((dep) => !BASE_DEPARTMENTS.includes(dep))
            .map((dep) => mapByProjectB[dep]),
        ];

        setRows(merged.length ? merged : HARDCODE);
        setError("");
      } catch (e) {
        console.error(e);
        setRows(HARDCODE);
        setError("資料載入失敗，已使用預設資料。");
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [HARDCODE]);

  // 色階計算（避免全 0 導致除以 0）
  const allValues = rows.flatMap((r) => SDG_COLUMNS_UI.map((c) => r[c]));
  const maxValue = allValues.length ? Math.max(...allValues) : 0;
  const minValue = allValues.length ? Math.min(...allValues) : 0;
  const range = Math.max(1, maxValue - minValue);

  const getBackgroundStyle = (value) => {
    if (value === 0) return { backgroundColor: "#ffffff" };
    const t = (value - minValue) / range;
    if (t <= 0.2) return { backgroundColor: "#dbeafe" };
    if (t <= 0.4) return { backgroundColor: "#93c5fd" };
    if (t <= 0.6) return { backgroundColor: "#3b82f6" };
    if (t <= 0.8) return { backgroundColor: "#fca5a5" };
    return { backgroundColor: "#ef4444" };
  };

  const getTextColor = (value) => {
    if (value === 0) return "#1f2937";
    const t = (value - minValue) / range;
    return t <= 0.4 ? "#1f2937" : "#ffffff";
  };

  if (loading) {
    return <div className="p-6 w-5/6 mx-auto">資料載入中…</div>;
  }

  return (
    <div className="p-6 w-5/6 mx-auto">
      {/* 訊息 */}
      {error && <div className="mb-2 text-sm text-red-600">{error}</div>}

      {/* 圖例 */}
      <div className="mb-6 flex items-center justify-between gap-4 flex-wrap">
        <div>
          <span className="text-center text-lg font-bold">
            {t("map.heatmapTitle")}
          </span>
        </div>
        <div className="flex items-center gap-4">
          <span className="text-sm font-medium text-gray-700">{t("map.intensity")}：</span>
          <div className="flex items-center gap-1">
            <span className="text-xs text-gray-600">{t("map.low")}</span>
            <div className="w-4 h-4 border border-gray-300" style={{ backgroundColor: "#dbeafe" }}></div>
            <div className="w-4 h-4 border border-gray-300" style={{ backgroundColor: "#93c5fd" }}></div>
            <div className="w-4 h-4 border border-gray-300" style={{ backgroundColor: "#3b82f6" }}></div>
            <div className="w-4 h-4 border border-gray-300" style={{ backgroundColor: "#fca5a5" }}></div>
            <div className="w-4 h-4 border border-gray-300" style={{ backgroundColor: "#ef4444" }}></div>
            <span className="text-xs text-gray-600">{t("map.high")}</span>
          </div>
          <div className="flex items-center gap-2 ml-4">
            <div className="w-4 h-4 border border-gray-300" style={{ backgroundColor: "#ffffff" }}></div>
            <span className="text-xs text-gray-600">{t("map.noInvestment")}</span>
          </div>
        </div>
      </div>

      {/* 熱度圖表格 */}
      <div
        className="overflow-auto border border-gray-300 rounded-lg shadow-lg"
        style={{ height: "360px" }}
      >
        <table className="min-w-full">
          {/* 表頭 */}
          <thead className="bg-gray-50 sticky top-0 z-20">
            <tr>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider border-r border-gray-300 sticky left-0 bg-gray-50 z-30 whitespace-nowrap">
                {t("map.department")}
              </th>
              {SDG_COLUMNS_UI.map((sdg) => (
                <th
                  key={sdg}
                  className="px-3 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider border-r border-gray-200 min-w-[60px] whitespace-nowrap"
                >
                  {sdg}
                </th>
              ))}
            </tr>
          </thead>

          {/* 表身 */}
          <tbody className="bg-white divide-y divide-gray-200">
            {rows.map((row, rowIndex) => (
              <tr key={rowIndex} className="hover:bg-gray-50">
                <td className="px-4 py-3 text-sm font-medium text-gray-900 border-r border-gray-300 sticky left-0 bg-white z-10 whitespace-nowrap">
                  {row.局處}
                </td>
                {SDG_COLUMNS_UI.map((sdg) => (
                  <td
                    key={sdg}
                    className="px-3 py-3 text-sm text-center border-r border-gray-200 font-medium transition-all duration-200 hover:scale-110 whitespace-nowrap"
                    style={{
                      backgroundColor: getBackgroundStyle(row[sdg]).backgroundColor,
                      color: getTextColor(row[sdg]),
                    }}
                  >
                    {row[sdg]}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default SDGHeatmap;
