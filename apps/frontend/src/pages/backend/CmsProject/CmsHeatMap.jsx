import { useState } from "react";
import { Form, Button } from "react-bootstrap";
import { MapContainer, TileLayer, CircleMarker, Tooltip } from "react-leaflet";
import "leaflet/dist/leaflet.css";

const sdgs = [
  "SDG1",
  "SDG2",
  "SDG3",
  "SDG4",
  "SDG5",
  "SDG6",
  "SDG7",
  "SDG8",
  "SDG9",
  "SDG10",
  "SDG11",
  "SDG12",
  "SDG13",
  "SDG14",
  "SDG15",
  "SDG16",
  "SDG17",
];

const data = {
  city: [
    {
      name: "南投縣南投市",
      coordinates: [120.685, 23.905],
      population: 100000,
    },
    { name: "南投縣埔里鎮", coordinates: [120.969, 23.964], population: 80000 },
    {
      name: "南投縣草屯鎮",
      coordinates: [120.685, 23.977],
      population: 90000,
    },
    { name: "南投縣竹山鎮", coordinates: [120.684, 23.756], population: 70000 },
    { name: "南投縣集集鎮", coordinates: [120.783, 23.827], population: 11000 },
    { name: "南投縣名間鄉", coordinates: [120.702, 23.834], population: 37000 },
    { name: "南投縣鹿谷鄉", coordinates: [120.754, 23.746], population: 17000 },
    {
      name: "南投縣中寮鄉",
      coordinates: [120.773, 23.879],
      population: 15000,
      children: [{ name: "新聞及行政處" }, { name: "民政處" }],
    },
    { name: "南投縣魚池鄉", coordinates: [120.936, 23.896], population: 15000 },
    { name: "南投縣國姓鄉", coordinates: [120.858, 24.048], population: 18000 },
    { name: "南投縣水里鄉", coordinates: [120.855, 23.812], population: 17000 },
    {
      name: "南投縣信義鄉",
      coordinates: [120.902, 23.696],
      population: 17000,
      children: [{ name: "觀光處" }],
    },
    {
      name: "南投縣仁愛鄉",
      coordinates: [121.137, 24.022],
      population: 15000,
      children: [{ name: "觀光處" }],
    },
  ],
  minLat: 23.6,
  maxLat: 24.2,
  minLong: 120.9,
  maxLong: 121.0,
};

const HeatMap = () => {
  const [district, setDistrict] = useState("all");
  const [selectedSdg, setSelectedSdg] = useState("all");
  const centerLat = (data.minLat + data.maxLat) / 2;
  const distanceLat = data.maxLat - data.minLat;
  const bufferLat = distanceLat * 0.05;
  const centerLong = (data.minLong + data.maxLong) / 2;
  const distanceLong = data.maxLong - data.minLong;
  const bufferLong = distanceLong * 0.15;

  return (
    <div className="w-5/6 mx-auto mt-4">
      <p className="text-4xl">永續主題：國家推動事務發展計畫</p>
      <div className="flex gap-4">
        <div className="w-32">
          <Form.Select
            aria-label="行政區域"
            value={district}
            onChange={(e) => setDistrict(e.target.value)}
          >
            <option value="">行政區域</option>
            <option value="南投市">南投市</option>
            <option value="埔里鎮">埔里鎮</option>
            <option value="草屯鎮">草屯鎮</option>
            <option value="竹山鎮">竹山鎮</option>
            <option value="集集鎮">集集鎮</option>
            <option value="名間鄉">名間鄉</option>
            <option value="鹿谷鄉">鹿谷鄉</option>
            <option value="中寮鄉">中寮鄉</option>
            <option value="魚池鄉">魚池鄉</option>
            <option value="國姓鄉">國姓鄉</option>
            <option value="水里鄉">水里鄉</option>
            <option value="信義鄉">信義鄉</option>
            <option value="仁愛鄉">仁愛鄉</option>
          </Form.Select>
        </div>
        <div className="w-40">
          <Form.Select
            aria-label="選擇永續發展指標"
            id="sdg_filter"
            value={selectedSdg}
            onChange={(e) => setSelectedSdg(e.target.value)}
          >
            <option value="all">永續發展指標</option>
            {sdgs.map((sdg) => (
              <option key={sdg} value={sdg}>
                {sdg}
              </option>
            ))}
          </Form.Select>
        </div>
      </div>
      <div className="my-4">
        <MapContainer
          className="w-full h-[480px]"
          zoom={10}
          center={[centerLat, centerLong]}
          bounds={[
            [data.minLat - bufferLat, data.minLong - bufferLong],
            [data.maxLat + bufferLat, data.maxLong + bufferLong],
          ]}
        >
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          {data.city.map((city, k) => (
            <CircleMarker
              key={k}
              center={[city.coordinates[1], city.coordinates[0]]}
              radius={city.population / 2000}
              fillOpacity={0.5}
              stroke={false}
            >
              <Tooltip direction="right" offset={[-8, -2]} opacity={1}>
                <div className="flex gap-2.5 p-2 font-semibold">
                  <div className="text-right">
                    <span>南投縣各鄉鎮</span>
                    <br />
                    <span>南投縣各政府各局處</span>
                    <br />
                    <span>總投入經費</span>
                    <br />
                    <span>永續發展指標指標</span>
                  </div>
                  <div>
                    <span>{city.name}</span>
                    <br />
                    <span>地政處</span>
                    <br />
                    <span>{city.population}</span>
                    <br />
                    <span>SDG 13 氣候行動</span>
                  </div>
                </div>
              </Tooltip>
            </CircleMarker>
          ))}
        </MapContainer>
      </div>
      <div className="flex justify-end mb-4">
        <Button
          variant="dark"
          className="w-32"
          onClick={() => window.history.back()}
        >
          返回
        </Button>
      </div>
    </div>
  );
};

export default HeatMap;
