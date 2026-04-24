(function () {
  const API_BASE = "https://api.zncddh.cn";

  function trackVisit() {
    fetch(API_BASE + "/track", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        page: window.location.pathname,
        referrer: document.referrer || ""
      })
    }).catch(function () {
      // 统计失败不影响页面正常浏览
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", trackVisit);
  } else {
    trackVisit();
  }
})();
