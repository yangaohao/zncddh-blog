---
title: 管理后台
date: 2026-04-24 19:50:00
---

这个页面用于查看博客后台数据。

<div id="admin-login">
  <p>请输入管理密码：</p>
  <input id="admin-token" type="password" style="width: 100%; padding: 8px; box-sizing: border-box;">
  <button id="admin-login-button" style="margin-top: 12px;">进入后台</button>
  <p id="admin-login-result"></p>
</div>

<div id="admin-dashboard" style="display: none;">
  <h2>数据概览</h2>
  <div id="admin-summary">加载中...</div>

  <h2>热门页面</h2>
  <div id="admin-top-pages">加载中...</div>

  <h2>最近留言</h2>
  <div id="admin-comments">加载中...</div>

  <h2>联系消息</h2>
  <div id="admin-contacts">加载中...</div>

  <h2>友链申请</h2>
  <div id="admin-links">加载中...</div>

  <h2>最近访问</h2>
  <div id="admin-visits">加载中...</div>

  <h2>图片管理</h2>
  <div style="border: 1px solid #ddd; border-radius: 8px; padding: 12px; margin-bottom: 12px;">
    <input id="image-file" type="file" accept="image/*">
    <button id="upload-image-button">上传图片</button>
    <p id="upload-image-result"></p>
  </div>
  <div id="admin-images">加载中...</div>


</div>

<script>
const ADMIN_API = "https://api.zncddh.cn/admin/overview";
const IMAGES_API = "https://api.zncddh.cn/images";
const UPLOAD_IMAGE_API = "https://api.zncddh.cn/upload-image";


function escapeHtml(text) {
  return String(text || "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function card(html) {
  return '<div style="border: 1px solid #ddd; border-radius: 8px; padding: 12px; margin-bottom: 12px;">' + html + '</div>';
}

function renderSummary(summary) {
  return card(
    '<p>总访问：' + summary.visits + '</p>' +
    '<p>留言数：' + summary.comments + '</p>' +
    '<p>联系消息：' + summary.contacts + '</p>' +
    '<p>友链申请：' + summary.link_applications + '</p>'
  );
}

function renderTopPages(pages) {
  if (!pages || pages.length === 0) {
    return "<p>暂无页面统计。</p>";
  }

  return pages.map(function(item) {
    return card('<strong>' + escapeHtml(item.page) + '</strong><p>访问次数：' + item.count + '</p>');
  }).join("");
}

function renderComments(comments) {
  if (!comments || comments.length === 0) {
    return "<p>暂无留言。</p>";
  }

  return comments.map(function(item) {
    return card(
      '<strong>' + escapeHtml(item.name) + '</strong>' +
      '<p>' + escapeHtml(item.content) + '</p>' +
      '<small>' + escapeHtml(item.created_at) + '</small>'
    );
  }).join("");
}

function renderContacts(contacts) {
  if (!contacts || contacts.length === 0) {
    return "<p>暂无联系消息。</p>";
  }

  return contacts.map(function(item) {
    return card(
      '<strong>' + escapeHtml(item.name) + '</strong>' +
      '<p>邮箱：' + escapeHtml(item.email) + '</p>' +
      '<p>' + escapeHtml(item.message) + '</p>' +
      '<p>状态：' + escapeHtml(item.status) + '</p>' +
      '<small>' + escapeHtml(item.created_at) + '</small>'
    );
  }).join("");
}

function renderLinks(links) {
  if (!links || links.length === 0) {
    return "<p>暂无友链申请。</p>";
  }

  return links.map(function(item) {
    return card(
      '<strong>' + escapeHtml(item.site_name) + '</strong>' +
      '<p>网址：<a href="' + escapeHtml(item.site_url) + '" target="_blank">' + escapeHtml(item.site_url) + '</a></p>' +
      '<p>头像：' + escapeHtml(item.avatar_url) + '</p>' +
      '<p>简介：' + escapeHtml(item.description) + '</p>' +
      '<p>联系方式：' + escapeHtml(item.contact) + '</p>' +
      '<p>状态：' + escapeHtml(item.status) + '</p>' +
      '<small>' + escapeHtml(item.created_at) + '</small>'
    );
  }).join("");
}

function renderVisits(visits) {
  if (!visits || visits.length === 0) {
    return "<p>暂无访问记录。</p>";
  }

  return visits.map(function(item) {
    return card(
      '<strong>' + escapeHtml(item.page) + '</strong>' +
      '<p>来源：' + escapeHtml(item.referrer || "直接访问") + '</p>' +
      '<p>浏览器：' + escapeHtml(item.user_agent) + '</p>' +
      '<small>' + escapeHtml(item.created_at) + '</small>'
    );
  }).join("");
}

function renderImages(images) {
  if (!images || images.length === 0) {
    return "<p>暂无图片。</p>";
  }

  return images.map(function(item) {
    const markdown = "![](" + item.url + ")";

    return card(
      '<p><strong>' + escapeHtml(item.filename) + '</strong></p>' +
      '<p><img src="' + escapeHtml(item.url) + '" style="max-width: 240px; border-radius: 8px;"></p>' +
      '<p>URL：<a href="' + escapeHtml(item.url) + '" target="_blank">' + escapeHtml(item.url) + '</a></p>' +
      '<p>Markdown：</p>' +
      '<textarea readonly style="width: 100%; min-height: 60px; padding: 8px; box-sizing: border-box;">' + escapeHtml(markdown) + '</textarea>'
    );
  }).join("");
}

async function loadImages(token) {
  const imageList = document.getElementById("admin-images");

  try {
    const response = await fetch(IMAGES_API, {
      headers: {
        "X-Admin-Token": token
      }
    });

    if (!response.ok) {
      imageList.innerHTML = "<p>图片列表加载失败。</p>";
      return;
    }

    const data = await response.json();
    imageList.innerHTML = renderImages(data.images);
  } catch (error) {
    imageList.innerHTML = "<p>图片列表加载失败，请确认后端和 Tunnel 正在运行。</p>";
  }
}

async function uploadImage(token) {
  const fileInput = document.getElementById("image-file");
  const result = document.getElementById("upload-image-result");

  if (!fileInput.files || fileInput.files.length === 0) {
    result.innerHTML = "请选择一张图片。";
    return;
  }

  const formData = new FormData();
  formData.append("file", fileInput.files[0]);

  result.innerHTML = "上传中...";

  try {
    const response = await fetch(UPLOAD_IMAGE_API, {
      method: "POST",
      headers: {
        "X-Admin-Token": token
      },
      body: formData
    });

    if (!response.ok) {
      result.innerHTML = "上传失败。";
      return;
    }

    const data = await response.json();
    result.innerHTML = '上传成功：<a href="' + escapeHtml(data.url) + '" target="_blank">' + escapeHtml(data.url) + '</a>';
    fileInput.value = "";
    await loadImages(token);
  } catch (error) {
    result.innerHTML = "上传失败，请确认后端和 Tunnel 正在运行。";
  }
}


async function loadAdminData(token) {
  const result = document.getElementById("admin-login-result");
  result.innerHTML = "加载中...";

  try {
    const response = await fetch(ADMIN_API, {
      headers: {
        "X-Admin-Token": token
      }
    });

    if (!response.ok) {
      result.innerHTML = "密码错误或后端拒绝访问。";
      return;
    }

    const data = await response.json();

    document.getElementById("admin-login").style.display = "none";
    document.getElementById("admin-dashboard").style.display = "block";

    document.getElementById("admin-summary").innerHTML = renderSummary(data.summary);
    document.getElementById("admin-top-pages").innerHTML = renderTopPages(data.top_pages);
    document.getElementById("admin-comments").innerHTML = renderComments(data.recent_comments);
    document.getElementById("admin-contacts").innerHTML = renderContacts(data.recent_contacts);
    document.getElementById("admin-links").innerHTML = renderLinks(data.recent_link_applications);
    document.getElementById("admin-visits").innerHTML = renderVisits(data.recent_visits);
    await loadImages(token);
  } catch (error) {
    result.innerHTML = "加载失败，请确认后端和 Tunnel 正在运行。";
  }
}

document.getElementById("admin-login-button").addEventListener("click", function() {
  const token = document.getElementById("admin-token").value.trim();

  if (!token) {
    document.getElementById("admin-login-result").innerHTML = "请输入管理密码。";
    return;
  }

  loadAdminData(token);
});

document.getElementById("upload-image-button").addEventListener("click", function() {
  const token = document.getElementById("admin-token").value.trim();

  if (!token) {
    document.getElementById("upload-image-result").innerHTML = "请先输入管理密码并进入后台。";
    return;
  }

  uploadImage(token);
});

</script>
