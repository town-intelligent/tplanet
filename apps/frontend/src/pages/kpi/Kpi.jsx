import CsrProject from "../../assets/csr-project.png";
import ProjectList from "./components/ProjectList";
import KpiList from "./components/KpiList";
import Chart from "./components/Chart";
import BubbleMap from "./components/BubbleMap";
import KpiChart from "./components/KpiChart";
import KpiHeatMap from "./components/KpiHeatMap";
import { useState, useEffect } from "react";
import { useSearchParams } from "react-router-dom";
import { list_plans, plan_info } from "../../utils/Plan";
import { SITE_HOSTERS } from "../../utils/Config";

const KPI = () => {
  const [searchParams] = useSearchParams();
  const [objListProjects, setObjListProjects] = useState([]);
  const [projects, setProjects] = useState([]);
  const [filteredProjects, setFilteredProjects] = useState([]);
  const [years, setYears] = useState([]);
  const [selectedYear, setSelectedYear] = useState("all");
  const [selectedDep, setSelectedDep] = useState("all");
  const [selectedSdg, setSelectedSdg] = useState("all");

  // 分頁狀態
  const [currentPage, setCurrentPage] = useState(1);

  // 初始化載入權重及專案
  const fetchProjects = async () => {
    try {
      // 判斷是否為「公司個體」模式
      const jwt = localStorage.getItem("jwt");
      const email = localStorage.getItem("email");
      const isLoggedIn = jwt && jwt !== "" && email && email !== "";
      const isPersonalMode = searchParams.get("status") === "loggedin";

      let hosters;
      if (isLoggedIn && isPersonalMode) {
        // 公司個體：只顯示自己的專案
        hosters = [email];
      } else {
        // 跨區跨域：顯示所有人的專案
        hosters = SITE_HOSTERS.length > 1 ? SITE_HOSTERS.slice(1) : SITE_HOSTERS;
      }
      const allProjects = [];
      const projectYears = new Set();

      for (const hoster of hosters) {
        // show debug info
        // console.debug("Fetching projects for hoster:", hoster);
        const objListProjects = await list_plans(hoster, null);
        setObjListProjects(objListProjects);
        for (const uuid of objListProjects.projects) {
          const projectInfo = await plan_info(uuid);
          allProjects.push({ uuid, ...projectInfo });

          if (projectInfo.period) {
            const startYear = new Date(
              projectInfo.period.split("-")[0]
            ).getFullYear();
            if (!isNaN(startYear)) {
              projectYears.add(startYear);
            }
          }
        }
      }

      setProjects(allProjects);
      setFilteredProjects(allProjects);
      setYears(Array.from(projectYears).sort());
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  useEffect(() => {
    fetchProjects();
  }, [searchParams]);

  // 當篩選條件改變時，重置到第一頁
  const resetToFirstPage = () => {
    setCurrentPage(1);
  };

  return (
    <section>
      {/* 只在第一頁顯示完整內容 */}
      {currentPage === 1 && (
        <>
          <div
            className="bg-cover mb-0 block bg-center h-48 md:h-80"
            style={{
              backgroundImage: `url(${CsrProject})`,
            }}
          ></div>
          {/* SDG 17 項主題格狀展示區 */}
          <KpiList projects={objListProjects} />

          {/* 條狀圖 */}
          <Chart />

          {/* 互動式地圖 */}
          <BubbleMap />

          {/* 折線圖 & 圓餅圖 */}
          <KpiChart />

          {/* 熱度圖 */}
          <KpiHeatMap />
        </>
      )}

      {/* 計畫卡片預覽（最多 3 張，其他續下頁，每頁至多 9 張)*/}
      <ProjectList
        projects={projects}
        filteredProjects={filteredProjects}
        setFilteredProjects={setFilteredProjects}
        years={years}
        selectedYear={selectedYear}
        setSelectedYear={setSelectedYear}
        selectedDep={selectedDep}
        setSelectedDep={setSelectedDep}
        selectedSdg={selectedSdg}
        setSelectedSdg={setSelectedSdg}
        currentPage={currentPage}
        setCurrentPage={setCurrentPage}
        resetToFirstPage={resetToFirstPage}
      />
    </section>
  );
};

export default KPI;