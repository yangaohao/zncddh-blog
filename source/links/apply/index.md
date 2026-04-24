---
title: 友情链接申请
date: 2026-04-24 19:20:00
---

欢迎申请友情链接。提交后我会在后台查看并手动审核。

<form id="link-apply-form" style="margin-bottom: 24px;">
<div style="margin-bottom: 12px;">
<label>网站名称</label><br>
<input id="site-name" type="text" maxlength="80" required style="width: 100%; padding: 8px; box-sizing: border-box;">
</div>

<div style="margin-bottom: 12px;">
<label>网站地址</label><br>
<input id="site-url" type="url" maxlength="300" required placeholder="https://example.com" style="width: 100%; padding: 8px; box-sizing: border-box;">
</div>

<div style="margin-bottom: 12px;">
<label>头像地址，可选</label><br>
<input id="avatar-url" type="url" maxlength="300" placeholder="https://example.com/avatar.png" style="width: 100%; padding: 8px; box-sizing: border-box;">
</div>

<div style="margin-bottom: 12px;">
<label>网站简介</label><br>
<textarea id="description" maxlength="300" required style="width: 100%; min-height: 100px; padding: 8px; box-sizing: border-box;"></textarea>
</div>

<div style="margin-bottom: 12px;">
<label>联系方式，可选</label><br>
<input id="contact" type="text" maxlength="120" placeholder="邮箱 / QQ / 其他联系方式" style="width: 100%; padding: 8px; box-sizing: border-box;">
</div>

<button type="submit">提交申请</button>
</form>

<div id="link-apply-result"></div>

<script>
const LINK_APPLY_API = "https://api.zncddh.cn/link-apply";

document.getElementById("link-apply-form").addEventListener("submit", async function(event) {
  event.preventDefault();

  const result = document.getElementById("link-apply-result");

  const siteNameInput = document.getElementById("site-name");
  const siteUrlInput = document.getElementById("site-url");
  const avatarUrlInput = document.getElementById("avatar-url");
  const descriptionInput = document.getElementById("description");
  const contactInput = document.getElementById("contact");

  const site_name = siteNameInput.value.trim();
  const site_url = siteUrlInput.value.trim();
  const avatar_url = avatarUrlInput.value.trim();
  const description = descriptionInput.value.trim();
  const contact = contactInput.value.trim();

  if (!site_name || !site_url || !description) {
    result.innerHTML = "<p>请填写网站名称、网站地址和网站简介。</p>";
    return;
  }

  try {
    const response = await fetch(LINK_APPLY_API, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        site_name: site_name,
        site_url: site_url,
        avatar_url: avatar_url,
        description: description,
        contact: contact
      })
    });

    if (!response.ok) {
      result.innerHTML = "<p>提交失败，请稍后再试。</p>";
      return;
    }

    siteNameInput.value = "";
    siteUrlInput.value = "";
    avatarUrlInput.value = "";
    descriptionInput.value = "";
    contactInput.value = "";

    result.innerHTML = "<p>申请已提交，我会尽快查看。</p>";
  } catch (error) {
    result.innerHTML = "<p>提交失败，请确认后端服务正在运行。</p>";
  }
});
</script>
