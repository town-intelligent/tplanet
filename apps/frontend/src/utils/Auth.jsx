async function verifyToken(token) {
  const formdata = new FormData();
  formdata.append("token", token);

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

    const returnData = await response.json();
    if (returnData.result) {
      console.log("JWT still available");
      return true;
    } else {
      console.log("JWT expired");

      // Clear all local storage
      localStorage.clear();

      // Redirect to signin page
      if (window.location.pathname.includes("/backend/")) {
        window.location.replace(`/signin`);
      }
      return false;
    }
  } catch (error) {
    console.error("Error:", error);
    return false;
  }
}

async function checkAuth() {
  const jwt = localStorage.getItem("jwt");
  if (!jwt) {
    const path = window.location.pathname;
    const page = path.split("/").pop();

    if (path.includes("/backend/") && page !== "signin" && page !== "signup") {
      window.location.replace(`/signin`);
    }
    return false;
  } else {
    console.log("Verifying JWT ...");
    return await verifyToken(jwt);
  }
}

export { verifyToken, checkAuth };
