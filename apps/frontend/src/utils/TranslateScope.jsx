import React, { useMemo, useRef, useState, useEffect } from "react";
import { useTranslation } from "react-i18next";
import { translateBatch } from "../utils/translateApi";
import { I18N_TO_TARGET } from "../utils/lang";

const Ctx = React.createContext(null);
export const useScopeTr = () => React.useContext(Ctx);

export default function TranslateScope({ children }) {
  const { i18n } = useTranslation();
  const lang = useMemo(() => (i18n.language || "zh").split("-")[0], [i18n.language]);
  const target = I18N_TO_TARGET[lang] || null;

  const [version, setVersion] = useState(0);

  // 翻譯結果：`${lang}|t|${src}` / `${lang}|h|${src}`
  const mapRef = useRef(new Map());

  // 本輪需要翻譯的 queue（用 Set 去重）
  const qTextRef = useRef(new Set());
  const qHtmlRef = useRef(new Set());

  const timerRef = useRef(null);
  const runningRef = useRef(false);

  const schedule = () => {
    if (!target) {
      setVersion((v) => v + 1);
      return;
    }
    if (timerRef.current) clearTimeout(timerRef.current);
    timerRef.current = setTimeout(async () => {
      if (runningRef.current) return;
      runningRef.current = true;

      try {
        const map = mapRef.current;

        const texts = Array.from(qTextRef.current);
        const htmls = Array.from(qHtmlRef.current);
        qTextRef.current.clear();
        qHtmlRef.current.clear();

        const uniqText = texts.filter((t) => !map.has(`${lang}|t|${t}`));
        const uniqHtml = htmls.filter((h) => !map.has(`${lang}|h|${h}`));

        if (!uniqText.length && !uniqHtml.length) return;

        if (uniqText.length) {
          const out = await translateBatch(uniqText, target, { isHtml: false });
          uniqText.forEach((src, idx) => map.set(`${lang}|t|${src}`, out[idx] || src));
        }

        if (uniqHtml.length) {
          const out = await translateBatch(uniqHtml, target, { isHtml: true });
          uniqHtml.forEach((src, idx) => map.set(`${lang}|h|${src}`, out[idx] || src));
        }

        setVersion((v) => v + 1);
      } finally {
        runningRef.current = false;
      }
    }, 120);
  };

  // 語言切換：不用清 map（key 有 lang），但要刷新一次讓顯示更新
  useEffect(() => {
    setVersion((v) => v + 1);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [lang]);

  const tr = (src) => {
    if (!target) return src;
    return mapRef.current.get(`${lang}|t|${src}`) || src;
  };

  const trHtml = (src) => {
    if (!target) return src;
    return mapRef.current.get(`${lang}|h|${src}`) || src;
  };

  const registerText = (src) => {
    if (!src) return;
    qTextRef.current.add(src);
    schedule();
  };

  const registerHtml = (src) => {
    if (!src) return;
    qHtmlRef.current.add(src);
    schedule();
  };

  return (
    <Ctx.Provider value={{ tr, trHtml, registerText, registerHtml, version }}>
      {children}
    </Ctx.Provider>
  );
}
