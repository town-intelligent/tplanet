import React, { useEffect, useState } from "react";
import { mockup_get } from "../utils/Mockup.jsx";
import SdgsModal from "./backend/components/SdgSelect.jsx";
import Banner from "../assets/contact-us-banner.png";
import { Form, Button } from "react-bootstrap";
import SliderCaptchaComponent from "../utils/Captcha.jsx";
import { departments, SITE_HOSTERS } from "../utils/Config.jsx";
import { useTranslation } from "react-i18next";

export default function ContactUsPage() {
  const { t } = useTranslation();
  const [bannerUrl, setBannerUrl] = useState(null);
  const [isVerified, setIsVerified] = useState(false);
  const [selectedSDGs, setSelectedSDGs] = useState([]);
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    company: "",
    department: "",
    phone: "",
    sdgs: [],
    needs: "",
  });

  useEffect(() => {
    setFormData((prev) => ({
      ...prev,
      sdgs: selectedSDGs,
    }));
  }, [selectedSDGs]);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === "checkbox" ? checked : value,
    });
  };

  const handleSubmit = () => {
    if (!isVerified) {
      alert("請先驗證");
    }
    console.log("submit");
  };

  useEffect(() => {
    const fetchData = async () => {
      // mockup 取得 banner
      const form = new FormData();
      form.append("email", SITE_HOSTERS[0]);
      const obj_mockup = await mockup_get(form);

      try {
        if (obj_mockup.description?.["contact-us-banner-img"]) {
          const imgPath = obj_mockup.description["contact-us-banner-img"];
          setBannerUrl(import.meta.env.VITE_HOST_URL_TPLANET + imgPath);
        }
      } catch (e) {
        console.log(e);
      }
    };

    fetchData();
  }, []);

  return (
    <div>
      {/* Banner */}
      <div
        id="contact_us_banner_1"
        style={{
          backgroundImage: `url(${bannerUrl || Banner})`,
          backgroundSize: "cover",
          backgroundPosition: "center",
          height: "200px",
        }}
      />

      <Form className="w-5/6 mx-auto py-10">
        <div className="flex justify-between">
          <div className="col-md-5">
            <Form.Group className="mb-3" controlId="exampleForm.ControlInput1">
              <Form.Label>{t("contactus.name")}</Form.Label>
              <Form.Control
                type="name"
                name="name"
                value={formData.name}
                onChange={handleChange}
                required
              />
            </Form.Group>

            <Form.Group className="mb-3" controlId="exampleForm.ControlInput1">
              <Form.Label>{t("contactus.company")}</Form.Label>
              <Form.Control
                type="text"
                name="company"
                value={formData.company}
                onChange={handleChange}
              />
            </Form.Group>

            <Form.Group className="mb-3" controlId="exampleForm.ControlInput1">
              <Form.Label>{t("contactus.phone")}</Form.Label>
              <Form.Control
                type="phone"
                name="phone"
                value={formData.phone}
                onChange={handleChange}
                required
              />
            </Form.Group>
          </div>

          <div className="col-md-5">
            <Form.Group className="mb-3" controlId="exampleForm.ControlInput1">
              <Form.Label>{t("contactus.email")}</Form.Label>
              <Form.Control
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                required
              />
            </Form.Group>
            <Form.Group className="mb-3" controlId="exampleForm.ControlInput1">
              <Form.Label>{t("contactus.topics")}</Form.Label>
              <SdgsModal
                selectedSDGs={selectedSDGs}
                setSelectedSDGs={setSelectedSDGs}
              />
            </Form.Group>
          </div>
        </div>
        <Form.Group className="mb-3" controlId="exampleForm.ControlTextarea1">
          <Form.Label>{t("contactus.needs")}</Form.Label>
          <Form.Control
            as="textarea"
            name="needs"
            rows={3}
            value={formData.needs}
            onChange={handleChange}
            required
          />
        </Form.Group>
        <div className="flex justify-center">
          <SliderCaptchaComponent
            isVerified={isVerified}
            setIsVerified={setIsVerified}
          />
        </div>
        <div className="flex justify-center">
          <Button variant="secondary" onClick={handleSubmit}>
            {t("contactus.submit")}
          </Button>
        </div>
      </Form>
    </div>
  );
}
