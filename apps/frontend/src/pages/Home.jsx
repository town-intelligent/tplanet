import React, { useEffect, useState } from "react";
import { SITE_HOSTERS } from "../utils/Config.jsx";
import ProjectImg from "../assets/project_img.jpg";
import TPlanetMap from "../assets/tplanet_map.png";
import CSR from "../assets/nantou-csr.png";
import SDGs from "../assets/sdgs.png";
import DigitalTwin from "../assets/digital-twin.png";
import TrHtml from "../utils/TrHtml.jsx";


const Home = () => {
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

  useEffect(() => {
    const mockup_get = async () => {
      const form = new FormData();
      form.append("email", SITE_HOSTERS[0]);

      try {
        const response = await fetch(
          `${import.meta.env.VITE_HOST_URL_TPLANET}/mockup/get`,
          {
            method: "POST",
            body: form,
          }
        );

        const obj = await response.json();
        if (obj.result !== false && Object.keys(obj.description).length > 0) {
          setData(obj.description);
        }
      } catch (e) {
        console.log(e);
      }
    };

    mockup_get();
  }, []);

  return (
    <section className="flex-grow mt-5">
      <div className="container mx-auto px-0">
        <div className="text-center">
          <img
            className="img-fluid"
            id="Tbanner_image"
            src={`${import.meta.env.VITE_HOST_URL_TPLANET}${
              data["banner-image"]
            }`}
            alt="Project Banner"
          />
        </div>
      </div>
      <div className="container mx-auto">
        <div className=" py-4">
          <div className="flex justify-center bg-light py-6">
            <div className="col-md-10">
              {/* <p
                id="textarea1"
                className="px-3 md:px-0 text-xl"
                // dangerouslySetInnerHTML={{
                //   __html: data["t-planet-description"],
                // }}
                dangerouslySetInnerHTML={{ __html: html.tPlanet }}
              ></p> */}
              <TrHtml
                id="textarea1"
                className="px-3 md:px-0 text-xl"
                html={data["t-planet-description"]}
              />
            </div>
          </div>
        </div>
        <div className="py-4">
          <div className="flex justify-center">
            <div className="w-full md:w-10/12">
              <div className="text-center">
                <img
                  id="t_planet_img"
                  className="img-fluid"
                  src={`${import.meta.env.VITE_HOST_URL_TPLANET}${
                    data["t-planet-img"]
                  }`}
                  alt="T Planet Map"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
      <div className="bg-light py-4">
        <div className="container mx-auto">
          <div className="flex justify-center">
            <div className="w-full md:w-10/12">
              <div className="card p-2 md:p-4">
                <div className="flex flex-col md:flex-row items-center">
                  <div className="w-full md:w-5/12 text-center">
                    <img
                      id="csr_img"
                      src={`${import.meta.env.VITE_HOST_URL_TPLANET}${
                        data["csr-img"]
                      }`}
                      className="img-fluid p-3 md:p-0"
                      alt="CSR"
                    />
                  </div>
                  <div className="w-full md:w-7/12">
                    <div className="card-body">
                      {/* <p
                        id="textarea2"
                        className="card-text text-xl"
                        dangerouslySetInnerHTML={{
                          __html: data["csr-description"],
                        }}
                      ></p> */}
                    <TrHtml
                      id="textarea2"
                      className="card-text text-xl"
                      html={data["csr-description"]}
                    />
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div className="flex justify-center mt-5">
            <div className="w-full md:w-10/12">
              <div className="card p-2 md:p-4">
                <div className="flex flex-col md:flex-row items-center">
                  <div className="w-full md:w-5/12 text-center">
                    <img
                      id="sdg_img"
                      src={`${import.meta.env.VITE_HOST_URL_TPLANET}${
                        data["sdg-img"]
                      }`}
                      className="img-fluid p-3 md:p-0"
                      alt="SDGs"
                    />
                  </div>
                  <div className="w-full md:w-7/12">
                    <div className="card-body">
                      {/* <p
                        id="textarea3"
                        className="card-text text-xl"
                        dangerouslySetInnerHTML={{
                          __html: data["sdg-description"],
                        }}
                      ></p> */}
                    <TrHtml
                      id="textarea3"
                      className="card-text text-xl"
                      html={data["sdg-description"]}
                    />
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div className="flex justify-center mt-5">
            <div className="w-full md:w-10/12">
              <div className="card p-2 md:p-4">
                <div className="flex flex-col md:flex-row items-center">
                  <div className="w-full md:w-5/12 text-center">
                    <img
                      id="twins_img"
                      src={`${import.meta.env.VITE_HOST_URL_TPLANET}${
                        data["twins-img"]
                      }`}
                      className="img-fluid p-3 md:p-0"
                      alt="Digital Twin"
                    />
                  </div>
                  <div className="w-full md:w-7/12">
                    <div className="card-body">
                      {/* <p
                        id="textarea4"
                        className="card-text text-xl"
                        dangerouslySetInnerHTML={{
                          __html: data["twins-description"],
                        }}
                      ></p> */}
                    <TrHtml
                      id="textarea4"
                      className="card-text text-xl"
                      html={data["twins-description"]}
                    />
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Home;
