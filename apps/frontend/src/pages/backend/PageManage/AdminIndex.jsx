import React, { useEffect, useState } from "react";
import ProjectImg from "../../../assets/project_img.jpg";
import TPlanetMap from "../../../assets/tplanet_map.png";
import CSR from "../../../assets/nantou-csr.png";
import SDGs from "../../../assets/sdgs.png";
import DigitalTwin from "../../../assets/digital-twin.png";
import { useTranslation } from "react-i18next";

const HomepageEditor = () => {
  const [data, setData] = useState({
    "banner-image": ProjectImg,
    "t-planet-img": TPlanetMap,
    "csr-img": CSR,
    "sdg-img": SDGs,
    "twins-img": DigitalTwin,
    "t-planet-description": "",
    "csr-description": "",
    "sdg-description": "",
    "twins-description": "",
  });

  // 新增：實際要上傳的檔案
  const [files, setFiles] = useState({});
  const [errors, setErrors] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  const { t } = useTranslation();

  // --- 工具：嘗試把字串 JSON 解析成物件 ---
  const tryParseJSON = (s) => {
    if (typeof s !== "string") return null;
    try {
      return JSON.parse(s);
    } catch {
      return null;
    }
  };

  // --- 工具：把舊的巢狀 description 攤平（相容 400 範例）---
  const normalizeDescription = (desc) => {
    let p = { ...(desc || {}) };
    for (let i = 0; i < 3; i++) {
      const inner = tryParseJSON(p.description);
      if (inner && typeof inner === "object") {
        // 內層攤平補到外層（外層已存在的優先）
        Object.entries(inner).forEach(([k, v]) => {
          if (!(k in p)) p[k] = v;
        });
        p.description = inner.description;
      } else {
        break;
      }
    }
    // 如果 description 看起來像 JSON，就刪掉避免污染 state
    if (typeof p.description !== "string" || p.description.trim().startsWith("{")) {
      delete p.description;
    }
    return p;
  };

  useEffect(() => {
    const mockup_get = async () => {
      const form = new FormData();
      form.append("email", localStorage.getItem("email"));

      try {
        const response = await fetch(
          `${import.meta.env.VITE_HOST_URL_TPLANET}/mockup/get`,
          {
            method: "POST",
            body: form,
          }
        );

        const obj = await response.json();
        console.log("Mockup Get Response:", obj);

        if (obj.result !== false && obj.description && Object.keys(obj.description).length > 0) {
          setData(normalizeDescription(obj.description));
        }
      } catch (e) {
        console.log(e);
      }
    };

    mockup_get();
  }, []);

  // 圖片上傳處理（預覽用 base64，實際上傳用 File）
  const handleImageUpload = (file, key) => {
    const maxSize = 5 * 1024 * 1024; // 5MB
    const allowedTypes = ["image/jpeg", "image/png", "image/jpg", "image/gif"]; // 加上 gif

    if (!allowedTypes.includes(file.type)) {
      alert(t("edit.cms_upload_format"));
      return;
    }
    if (file.size > maxSize) {
      alert(t("edit.cms_upload_size"));
      return;
    }

    // 預覽（dataURL）
    const reader = new FileReader();
    reader.onload = (e) => {
      setData((prev) => ({
        ...prev,
        [key]: e.target.result,
      }));
    };
    reader.readAsDataURL(file);

    // 送到後端的實際檔案
    setFiles((prev) => ({ ...prev, [key]: file }));
  };

  // 更新描述內容
  const updateDescription = (key, value) => {
    setData((prev) => ({
      ...prev,
      [key]: value,
    }));
  };

  // 驗證表單
  const validateForm = () => {
    const newErrors = {};

    if (!data["banner-image"]) {
      newErrors.bannerImage = t("edit.cms_upload_banner_required");
    }

    const descriptions = [
      "t-planet-description",
      "csr-description",
      "sdg-description",
      "twins-description",
    ];
    descriptions.forEach((key) => {
      if (!String(data[key] || "").trim()) {
        newErrors[key] = t("edit.cms_desc_required");
      }
    });

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  // 送出（逐欄位 append；圖片送 File）
  const handleSave = async () => {
    if (!validateForm()) {
      alert(t("edit.cms_validation_all_required"));
      return;
    }

    setIsLoading(true);
    try {
      const form = new FormData();
      form.append("email", localStorage.getItem("email"));

      // 如需保證 HTML <p> 包裹，可用 wrapAsP；否則直接送字串
      const wrapAsP = (v) => {
        const s = String(v || "").trim();
        if (!s) return "";
        return s.startsWith("<") ? s : `<p>${s}</p>`;
      };

      // 文字描述欄位
      form.append("t-planet-description", wrapAsP(data["t-planet-description"]));
      form.append("csr-description", wrapAsP(data["csr-description"]));
      form.append("sdg-description", wrapAsP(data["sdg-description"]));
      form.append("twins-description", wrapAsP(data["twins-description"]));

      // 圖片欄位：有新檔案才上傳；沒有就不覆蓋（後端保留舊值）
      const imageKeys = [
        "banner-image",
        "t-planet-img",
        "csr-img",
        "sdg-img",
        "twins-img",
        // 若未來有下列兩個，也可解鎖：
        // "news-banner-img",
        // "contact-us-banner-img",
      ];
      imageKeys.forEach((k) => {
        if (files[k]) {
          form.append(k, files[k], files[k].name);
        }
      });

      const response = await fetch(
        `${import.meta.env.VITE_HOST_URL_TPLANET}/mockup/new`,
        {
          method: "POST",
          body: form,
        }
      );

      if (response.ok) {
        alert(t("edit.cms_save_success"));
        setErrors({});
      } else {
        throw new Error("儲存失敗");
      }
    } catch (error) {
      console.error(error);
      alert(t("edit.cms_save_failed"));
    } finally {
      setIsLoading(false);
    }
  };

  // 圖片編輯子元件
  const ImageEditor = ({
    imageKey,
    label,
    currentImage,
    className = "img-fluid",
  }) => {
    // 判斷圖片來源：如果是 data URL (base64) 就直接使用，否則加上 API URL
    const getImageSrc = (imageData) => {
      if (!imageData) return currentImage; // fallback
      if (typeof imageData === "string" && imageData.startsWith("data:")) {
        return imageData; // 使用者剛上傳的 base64
      }
      // 後端回傳的相對路徑
      return `${import.meta.env.VITE_HOST_URL_TPLANET}${imageData}`;
    };

    return (
      <div className="relative group">
        <img
          className={className}
          src={getImageSrc(data[imageKey])}
          alt={label}
          onError={(e) => {
            e.currentTarget.src = currentImage;
          }}
        />

        <div className="absolute bottom-0 right-0">
          <button
            onClick={() =>
              document.getElementById(`upload-${imageKey}`).click()
            }
            className="bg-[#317EE0] text-white px-4 py-2 rounded hover:bg-blue-600 flex items-center"
          >
            {t("edit.cms_edit_image")}
          </button>
          <input
            id={`upload-${imageKey}`}
            type="file"
            accept="image/*"
            className="hidden"
            onChange={(e) =>
              e.target.files[0] &&
              handleImageUpload(e.target.files[0], imageKey)
            }
          />
        </div>
      </div>
    );
  };

  // 描述編輯子元件
  const DescriptionEditor = ({
    descKey,
    placeholder,
    className = "text-xl",
  }) => (
    <div>
      <div>
        <textarea
          value={data[descKey] || ""}
          onChange={(e) => updateDescription(descKey, e.target.value)}
          placeholder={placeholder}
          className={`w-full p-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 ${
            errors[descKey] ? "border-red-500" : "border-gray-300"
          }`}
          rows="4"
        />
        {errors[descKey] && (
          <div className="mt-1 flex items-center text-red-600 text-sm">
            ⚠️ {errors[descKey]}
          </div>
        )}
      </div>
    </div>
  );

  return (
    <div className="relative">
      <section className="flex-grow mt-5">
        <div className="container mx-auto px-0 py-2">
          <div className="text-center">
            {/* 橫幅圖片 */}
            <ImageEditor
              imageKey="banner-image"
              label="Project Banner"
              currentImage="/api/placeholder/1200/400"
              className="img-fluid"
            />
            {errors.bannerImage && (
              <div className="mt-2 flex items-center justify-center text-red-600 text-sm">
                ⚠️ {errors.bannerImage}
              </div>
            )}
          </div>
        </div>

        <div className="container mx-auto">
          <div className="py-4">
            <div className="flex justify-center py-6">
              <div className="col-md-10">
                {/* T-Planet 描述 */}
                <DescriptionEditor
                  descKey="t-planet-description"
                  placeholder={t("adminIndex.cms_placeholder_tplanet")}
                  className="px-3 md:px-0 text-xl"
                />
              </div>
            </div>
          </div>

          <div className="py-4">
            <div className="flex justify-center">
              <div className="w-full md:w-10/12">
                <div className="text-center">
                  {/* T-Planet 地圖 */}
                  <ImageEditor
                    imageKey="t-planet-img"
                    label="T Planet Map"
                    currentImage="/api/placeholder/800/600"
                    className="img-fluid"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-light py-4">
          <div className="container mx-auto">
            {/* CSR 區塊 */}
            <div className="flex justify-center">
              <div className="w-full md:w-10/12">
                <div className="card p-2 md:p-4">
                  <div className="flex flex-col md:flex-row items-center">
                    <div className="w-full md:w-5/12 text-center">
                      <ImageEditor
                        imageKey="csr-img"
                        label="CSR"
                        currentImage="/api/placeholder/400/300"
                        className="img-fluid p-3 md:p-0"
                      />
                    </div>
                    <div className="w-full md:w-7/12">
                      <div className="card-body">
                        <DescriptionEditor
                          descKey="csr-description"
                          placeholder={t("adminIndex.cms_placeholder_csr")}
                          className="card-text text-xl"
                        />
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* SDG 區塊 */}
            <div className="flex justify-center mt-5">
              <div className="w-full md:w-10/12">
                <div className="card p-2 md:p-4">
                  <div className="flex flex-col md:flex-row items-center">
                    <div className="w-full md:w-5/12 text中心">
                      <ImageEditor
                        imageKey="sdg-img"
                        label="SDGs"
                        currentImage="/api/placeholder/400/300"
                        className="img-fluid p-3 md:p-0"
                      />
                    </div>
                    <div className="w-full md:w-7/12">
                      <div className="card-body">
                        <DescriptionEditor
                          descKey="sdg-description"
                          placeholder={t("adminIndex.cms_placeholder_sdg")}
                          className="card-text text-xl"
                        />
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Digital Twin 區塊 */}
            <div className="flex justify-center mt-5">
              <div className="w-full md:w-10/12">
                <div className="card p-2 md:p-4">
                  <div className="flex flex-col md:flex-row items-center">
                    <div className="w-full md:w-5/12 text-center">
                      <ImageEditor
                        imageKey="twins-img"
                        label="Digital Twin"
                        currentImage="/api/placeholder/400/300"
                        className="img-fluid p-3 md:p-0"
                      />
                    </div>
                    <div className="w-full md:w-7/12">
                      <div className="card-body">
                        <DescriptionEditor
                          descKey="twins-description"
                          placeholder={t("adminIndex.cms_placeholder_digital_twin")}
                          className="card-text text-xl"
                        />
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* 儲存按鈕 */}
        <div className="p-6">
          <div className="flex justify-center">
            <button
              onClick={handleSave}
              disabled={isLoading}
              className="bg-[#317EE0] rounded text-white px-8 py-2 hover:bg-blue-600 disabled:bg-gray-400 flex items-center font-medium"
            >
              {isLoading ? t("edit.cms_saving") : t("edit.cms_save")}
            </button>
          </div>
        </div>
      </section>
    </div>
  );
};

export default HomepageEditor;