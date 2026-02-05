export async function getGroup(email) {
  const formdata = new FormData();
  formdata.append("email", email);

  try {
    const response = await fetch(
      `${import.meta.env.VITE_HOST_URL_TPLANET}/accounts/get_group`,
      {
        method: "POST",
        body: formdata,
        redirect: "follow",
      }
    );

    if (!response.ok) {
      throw new Error("Network response was not ok");
    }

    const returnData = await response.json();
    localStorage.setItem("group", returnData.group);
    return returnData.group;
  } catch (error) {
    console.error("There was a problem with the fetch operation:", error);
    return null;
  }
}

export async function logout() {
  const formdata = new FormData();
  formdata.append("token", localStorage.getItem("jwt"));

  try {
    const response = await fetch(
      `${import.meta.env.VITE_HOST_URL_TPLANET}/accounts/verify_jwt`,
      {
        method: "POST",
        body: formdata,
        redirect: "follow",
      }
    );

    if (!response.ok) {
      throw new Error("Network response was not ok");
    }

    //const returnData = await response.json();
    localStorage.clear();
    window.location.replace("/");
  } catch (error) {
    console.error("There was a problem with the fetch operation:", error);
  }
}

export async function forgotPassword(email) {
  const formdata = new FormData();
  formdata.append("email", email);

  try {
    const response = await fetch(
      `${import.meta.env.VITE_HOST_URL_TPLANET}/accounts/forgot_password`,
      {
        method: "POST",
        body: formdata,
        redirect: "follow",
      }
    );

    // ✅ 判斷 status code 是否為 2xx
    if (response.ok) {
      // 2xx 都視為成功
      console.log("✅ Password reset email sent successfully");
      return true;
    } else {
      console.error(`❌ Server returned status: ${response.status}`);
      return false;
    }
  } catch (error) {
    console.error("There was a problem with the forgotPassword API:", error);
    return false;
  }
}

export async function deleteAccount(email) {
  const formdata = new FormData();
  formdata.append("email", email);

  try {
    const response = await fetch(
      `${import.meta.env.VITE_HOST_URL_TPLANET}/accounts/delete`,
      {
        method: "POST",
        body: formdata,
        redirect: "follow",
      }
    );

    if (!response.ok) {
      console.error(`❌ Server returned status: ${response.status}`);
      return { success: false, message: `刪除失敗 (${response.status})` };
    }

    const result = await response.json().catch(() => ({}));
    console.log("✅ deleteAccount response:", result);

    // 假設後端回傳格式如 { result: true, message: "deleted" }
    if (result.result === true) {
      return { success: true, message: "帳號已刪除" };
    } else {
      return { success: false, message: result.message || "刪除失敗" };
    }
  } catch (error) {
    console.error("There was a problem with the deleteAccount API:", error);
    return { success: false, message: error.message || "刪除帳號時發生錯誤" };
  }
}

// 取得帳號狀態（active）
export async function getAccountStatus(email) {
  const formdata = new FormData();
  formdata.append("email", email);

  try {
    const response = await fetch(
      `${import.meta.env.VITE_HOST_URL_TPLANET}/accounts/get_user_info`,
      {
        method: "POST",
        body: formdata,
        redirect: "follow",
      }
    );

    if (!response.ok) {
      throw new Error(`Network response was not ok (${response.status})`);
    }

    const data = await response.json();
    console.log("✅ getAccountStatus response:", data);

    let active = null;
    let userInfo = null;

    if (Array.isArray(data.content) && data.content.length >= 2) {
      userInfo = data.content[1];
      active = !!userInfo.active;
    } else if (data.content && typeof data.content === "object") {
      userInfo = data.content;
      active = !!userInfo.active;
    }

    return {
      success: true,
      active,      // true / false / null
      userInfo,    // 完整 user 資訊
    };
  } catch (error) {
    console.error("There was a problem with getAccountStatus:", error);
    return {
      success: false,
      active: null,
      userInfo: null,
      message: error.message || "取得帳號狀態失敗",
    };
  }
}

// 設定帳號啟用 / 停用狀態
// isActive 為 boolean：true = 啟用, false = 停用
export async function setAccountActiveStatus(email, isActive) {
  try {
    const response = await fetch(
      `${import.meta.env.VITE_HOST_URL_TPLANET}/accounts/activate_user`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email,
          is_active: isActive ? "True" : "False",   // 後端期待字串
        }),
        redirect: "follow",
      }
    );

    if (!response.ok) {
      console.error(`❌ Server returned status: ${response.status}`);
      return {
        success: false,
        message: `更新失敗 (${response.status})`,
      };
    }

    const data = await response.json().catch(() => ({}));
    console.log("✅ setAccountActiveStatus response:", data);

    if (data.result === true) {
      return {
        success: true,
        message: data.content || "User activation status updated successfully",
      };
    } else {
      return {
        success: false,
        message: data.content || data.message || "更新失敗",
      };
    }
  } catch (error) {
    console.error("There was a problem with setAccountActiveStatus:", error);
    return {
      success: false,
      message: error.message || "更新帳號啟用狀態時發生錯誤",
    };
  }
}

// 新增帳號 API
export async function addAccount(payload) {
  try {
    const response = await fetch(
      `${import.meta.env.VITE_HOST_URL_TPLANET}/accounts/add_user`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
        redirect: "follow",
      }
    );

    if (!response.ok) {
      return {
        success: false,
        message: `建立失敗（HTTP ${response.status})`,
      };
    }

    const data = await response.json().catch(() => ({}));

    if (!data?.email) {
      return { success: false, message: "建立失敗（請確定帳號格式正確或已經存在）" };
    }

    return {
      success: true,
      message: `已建立使用者：${data.email}`,
      data,
    };
  } catch (error) {
    console.error("❌ There was a problem with addAccount API:", error);
    return { success: false, message: error.message || "建立帳號時發生錯誤" };
  }
}