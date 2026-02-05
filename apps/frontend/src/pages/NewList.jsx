// src/pages/frontend/components/NewsListComponent.jsx
import React, { useState, useEffect, useMemo } from "react";
import { Link } from "react-router-dom";
import { news_list, news_get, news_delete } from "../utils/New"; // ← 路徑依你的專案調整
import { mockup_get } from "../utils/Mockup";                   // ← 取頁首 Banner 用
import { SITE_HOSTERS } from "../utils/Config.jsx";
import { useTranslation } from "react-i18next";
import Tr from "../utils/Tr.jsx";

const TPLANET_BASE = import.meta.env.VITE_HOST_URL_TPLANET;

// 從 localStorage 取 email（CMS 登入後可用），沒取到就用預設
const getEmail = () => {
  const fromLS = localStorage.getItem("email");
  return fromLS && fromLS.trim() ? fromLS.trim() : SITE_HOSTERS[0];
};

// 新聞卡片
const NewsCard = ({ item, isMainNews, onDeleted, isCMS }) => {
  const bannerUrl = useMemo(() => {
    const path = item?.content?.static?.banner;
    return path ? `${TPLANET_BASE}${path}` : "";
  }, [item]);

  const handleDelete = async () => {
    if (!item?.content?.uuid) return;
    if (!window.confirm(`即將刪除 : ${item.content.title}`)) return;

    const res = await news_delete(item.content.uuid);
    if (res?.result) {
      onDeleted?.(item.content.uuid);
    } else {
      alert(`刪除失敗：${res?.error || "未知錯誤"}`);
    }
  };

  const period = item?.content?.period || "";
  const title = item?.content?.title || "";
  const uuid = item?.content?.uuid;

  if (isMainNews) {
    return (
      <div className="row" id={`id_${uuid}`}>
        <div className="col-12 d-none d-md-block">
          <div
            className="img-fluid bg-cover position-relative"
            style={{
              backgroundImage: `url(${bannerUrl})`,
              width: "100%",
              height: "400px",
              backgroundRepeat: "no-repeat",
              backgroundSize: "cover",
            }}
          >
            <div className="d-flex flex-column h-100 justify-content-end text-white">
              <div className="bg-dark pt-2 pl-3 bg-opacity">
                <p className="mb-0 text-shadow">{period}</p>
                <Tr className="text-shadow" children={title} />
              </div>
            </div>
            <Link
              to={`/news_content/${uuid}`}
              className="stretched-link"
              aria-label={title}
            />
          </div>

          {isCMS && (
            <div className="text-center my-3">
              <button
                className="btn btn-danger rounded-pill text-white"
                style={{ width: "100px" }}
                onClick={handleDelete}
              >
                刪除
              </button>
            </div>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="col-md-4 mb-4" id={`id_${uuid}`}>
      <div className="rounded-0 position-relative">
        <div
          className="img-fluid bg-cover"
          style={{
            backgroundImage: `url(${bannerUrl})`,
            width: "100%",
            height: "288px",
            backgroundRepeat: "no-repeat",
            backgroundSize: "cover",
          }}
        >
          <div className="d-flex flex-column h-100 justify-content-end text-white">
            <div className="bg-dark pt-2 pl-3 bg-opacity">
              <p className="mb-0 text-shadow">{period}</p>
              <Tr className="text-shadow" children={title} />
            </div>
          </div>
          {!isCMS && (
            <Link
              to={`/news_content/${uuid}`}
              className="stretched-link"
              aria-label={title}
            />
          )}
        </div>
      </div>

      {isCMS && (
        <div className="text-center my-3">
          <button
            className="btn btn-danger rounded-pill text-white"
            style={{ width: "100px" }}
            onClick={async () => await handleDelete()}
          >
            刪除
          </button>
        </div>
      )}
    </div>
  );
};

const NewsListComponent = ({ isCMS = false }) => {
  const [newsList, setNewsList] = useState([]); // [{ uuid, start_date, content }, ...]
  const [loading, setLoading] = useState(true);
  const [bannerImage, setBannerImage] = useState(""); // ← 頁首 Banner
  const { t } = useTranslation();

  // 將 period 轉 Date（支援 dd/mm/yyyy；null 就放最後面）
  const parsePeriodDate = (periodStr) => {
    if (!periodStr) return null;
    const regex = /\b\d{2}\/\d{2}\/\d{4}\b/g;
    const m = periodStr.match(regex);
    if (m && m.length > 0) {
      const [dd, mm, yyyy] = m[0].split("/");
      return new Date(`${yyyy}-${mm}-${dd}T00:00:00`);
    }
    return null;
  };

  const loadNews = async () => {
    setLoading(true);
    try {
      const email = getEmail();

      // 1) 取頁首 Banner（mockup_get）
      try {
        const form = new FormData();
        form.append("email", email);
        const objMockup = await mockup_get(form);
        const p = objMockup?.description?.["news-banner-img"];
        setBannerImage(p ? `${TPLANET_BASE}${p}` : "");
      } catch (e) {
        console.warn("mockup_get 失敗或沒有 news-banner-img，可忽略：", e);
        setBannerImage("");
      }

      // 2) 取新聞列表
      const listRes = await news_list(DEFAULT_SITE_HOSTERS[0]);
      if (!listRes?.result) {
        console.error("news_list 失敗：", listRes?.error);
        setNewsList([]);
        return;
      }

      const uuids = Array.isArray(listRes.content) ? listRes.content : [];
      if (uuids.length === 0) {
        setNewsList([]);
        return;
      }

      // 逐一撈內容（必要時可改 Promise.all）
      const items = [];
      for (const uuid of uuids) {
        const one = await news_get(uuid);
        if (one?.result && one?.content) {
          if (isCMS && one.content.period == null) {
            // CMS 模式濾掉沒有 period 的
            continue;
          }
          items.push({
            uuid,
            start_date: parsePeriodDate(one.content.period),
            content: one.content,
          });
        }
      }

      // 排序：有日期在前、由新到舊；沒日期放最後
      items.sort((a, b) => {
        if (!a.start_date && !b.start_date) return 0;
        if (!a.start_date) return 1;
        if (!b.start_date) return -1;
        return b.start_date - a.start_date;
      });

      setNewsList(items);
    } catch (e) {
      console.error("載入新聞資料時發生錯誤:", e);
      setNewsList([]);
    } finally {
      setLoading(false);
    }
  };

  const handleDeleted = (uuid) => {
    setNewsList((prev) => prev.filter((n) => n.uuid !== uuid));
  };

  useEffect(() => {
    loadNews();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isCMS]);

  if (loading) return <div className="text-center">{t("common.loading")}</div>;

  if (!newsList.length) {
    return (
      <div className="container">
        {/* 頁首 Banner 區（有就顯示） */}
        {bannerImage && (
          <div
            id="news_banner_image"
            style={{
              backgroundImage: `url(${bannerImage})`,
              height: "300px",
              backgroundSize: "cover",
              backgroundPosition: "center",
              marginBottom: "2.5rem",
            }}
          />
        )}
        <div className="text-center py-5">{t("news.noNews")}</div>
      </div>
    );
  }

  const [main, ...rest] = newsList;

  return (
    <div className="container">
      {/* 頁首 Banner 區（有就顯示） */}
      {bannerImage && (
        <div
          id="news_banner_image"
          style={{
            backgroundImage: `url(${bannerImage})`,
            height: "300px",
            backgroundSize: "cover",
            backgroundPosition: "center",
            marginBottom: "2.5rem",
          }}
        />
      )}

      {/* 主要新聞（第一筆） */}
      <div id="main_news" className="row mb-4">
        {main && (
          <NewsCard
            item={main}
            isMainNews={true}
            onDeleted={handleDeleted}
            isCMS={isCMS}
          />
        )}
      </div>

      {/* 新聞列表（其餘） */}
      <div id="news_container" className="row">
        {rest.map((item) => (
          <NewsCard
            key={item.uuid}
            item={item}
            isMainNews={false}
            onDeleted={handleDeleted}
            isCMS={isCMS}
          />
        ))}
      </div>
    </div>
  );
};

export default NewsListComponent;
