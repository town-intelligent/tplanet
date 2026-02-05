// src/App.jsx
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { useEffect } from "react";
import Nav from "./pages/components/Nav";
import Footer from "./pages/components/Footer";

import Home from "./pages/Home";
import Kpi from "./pages/kpi/Kpi";
import ProjectContent from "./pages/kpi/components/ProjectContent";
import KpiFilter from "./pages/kpi/KpiFilter";
import NewList from "./pages/NewList";
import NewsContent from "./pages/NewContent";
import ContactUs from "./pages/ContactUs";

import AISecretary from "./pages/backend/AISecretary";
import AccountList from "./pages/backend/AccountList";
import AddAccount from "./pages/backend/AddAccount";
import UserPage from "./pages/backend/UserPage";
import Dashboard from "./pages/backend/Dashboard";
import AdminDashboard from "./pages/backend/AdminDashboard";
import CmsAgent from "./pages/backend/CmsAgent";

import HeatMap from "./pages/backend/CmsProject/CmsHeatMap";
import SROI from "./pages/backend/CmsProject/CmsSROI";
import CmsSroiEvidence from "./pages/backend/CmsProject/CmsSroiEvidence";
import CmsPlanInfo from "./pages/backend/CmsProject/CmsPlanInfo";
import CmsSdgsSetting from "./pages/backend/CmsProject/CmsSdgsSetting";
import CmsImpact from "./pages/backend/CmsProject/CmsImpact";
import CmsContactPerson from "./pages/backend/CmsProject/CmsContactPerson";
import AdminIndex from "./pages/backend/PageManage/AdminIndex";
import AdminNewsList from "./pages/backend/PageManage/AdminNewsList";
import AdminContactUs from "./pages/backend/PageManage/AdminContactUs";
import DeleteAccount from "./pages/backend/DeleteAccount";

import SignIn from "./pages/SignIn";
import SignUp from "./pages/SignUp";
import ForgetPw from "./pages/ForgetPw";
import ResetPw from "./pages/ResetPw";
import { AuthProvider } from "./utils/ProtectRoute";

import TranslateScope from "./utils/TranslateScope";

function App() {
  // 訪客計數功能
  useEffect(() => {
    const recordVisitor = async () => {
      // 檢查是否已經在本次 session 記錄過
      if (!sessionStorage.getItem('visitor_recorded')) {
        try {
          const response = await fetch(`${import.meta.env.VITE_HOST_URL_TPLANET}/dashboard/visitors`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
          });
          
          if (response.ok) {
            const data = await response.json();
            console.log('Visitor recorded:', data);
            // 標記此 session 已記錄
            sessionStorage.setItem('visitor_recorded', 'true');
          } else {
            console.error('Failed to record visitor:', response.status);
          }
        } catch (error) {
          console.error('Error recording visitor:', error);
        }
      }
    };

    // 在應用程式載入時記錄訪客
    recordVisitor();
  }, []); // 只在組件初次掛載時執行

  const Layout = ({ children, footerFixed = false }) => {
    if (footerFixed) {
      return (
        <div className="h-full flex flex-col">
          <div className="flex-1 overflow-auto">{children}</div>
          <div className="flex-shrink-0">
            <Footer />
          </div>
        </div>
      );
    }
    return (
      <div className="min-h-full flex flex-col">
        <div className="flex-1">{children}</div>
        <Footer />
      </div>
    );
  };

  return (
    <AuthProvider>
      <BrowserRouter>
        <div className="h-screen flex flex-col">
          <a
            href="#main-content"
            tabIndex="1"
            className="sr-only focus:not-sr-only absolute top-0 left-0 px-4 py-2 z-99 bg-amber-300"
            title="跳到主要內容"
          >
            跳到主要內容
          </a>

          {/* Header */}
          <div className="bg-white shadow-md flex-shrink-0 fixed top-0 left-0 right-0 z-50">
            <Nav />
          </div>

          {/* Main Content */}
          <main id="main-content" className="flex-1 w-full bg-gray-100 pt-20">
            <TranslateScope>
            <Routes>
              {/* Frontend */}
              <Route path="/" element={<Layout><Home /></Layout>} />
              <Route path="/kpi" element={<Layout><Kpi /></Layout>} />
              <Route path="/content/:id" element={<Layout><ProjectContent /></Layout>} />
              <Route path="/kpi_filter/:id" element={<Layout><KpiFilter /></Layout>} />
              <Route path="/news_list" element={<Layout><NewList /></Layout>} />
              <Route path="/news_content/:id" element={<Layout footerFixed><NewsContent /></Layout>} />
              <Route path="/contact_us" element={<Layout><ContactUs /></Layout>} />
              <Route path="/signin" element={<Layout><SignIn /></Layout>} />
              <Route path="/signup" element={<Layout><SignUp /></Layout>} />
              <Route path="/forget_pw" element={<Layout><ForgetPw /></Layout>} />

              {/* Backend */}
              <Route path="/backend/ai-secretary" element={<AISecretary />} />
              <Route path="/backend/account-list" element={<Layout footerFixed><AccountList /></Layout>} />
              <Route path="/backend/account-list/add-account" element={<Layout footerFixed><AddAccount /></Layout>} />
              <Route path="/backend/user-page" element={<Layout footerFixed><UserPage /></Layout>} />
              <Route path="/backend/dashboard" element={<Layout footerFixed><Dashboard /></Layout>} />
              <Route path="/backend/cms_agent" element={<Layout><CmsAgent /></Layout>} />
              <Route path="/backend/admin_dashboard" element={<Layout footerFixed><AdminDashboard /></Layout>} />
              <Route path="/backend/heat_map/:id" element={<Layout><HeatMap /></Layout>} />
              <Route path="/backend/reset_pw" element={<Layout><ResetPw /></Layout>} />
              {/* 本 PR 新增兩條 SROI 路由（比照其他 CmsProject 頁，不固定 footer） */}
              <Route path="/backend/cms_sroi/:id" element={<Layout><SROI /></Layout>} />
              <Route path="/backend/cms_sroi_evidence/:id" element={<Layout><CmsSroiEvidence /></Layout>} />
              <Route path="/backend/cms_plan_info/:id" element={<Layout><CmsPlanInfo /></Layout>} />
              <Route path="/backend/cms_sdgs_setting/:id" element={<Layout><CmsSdgsSetting /></Layout>} />
              <Route path="/backend/cms_impact/:id" element={<Layout><CmsImpact /></Layout>} />
              <Route path="/backend/cms_contact_person/:id" element={<Layout><CmsContactPerson /></Layout>} />
              <Route path="/backend/admin_index" element={<Layout footerFixed><AdminIndex /></Layout>} />
              <Route path="/backend/admin_news_list" element={<Layout><AdminNewsList /></Layout>} />
              <Route path="/backend/admin_contact_us" element={<Layout><AdminContactUs /></Layout>} />
              <Route path="/backend/admin_agent_accountDelete" element={<Layout><DeleteAccount /></Layout>} />
            </Routes>
            </TranslateScope>
          </main>
        </div>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;