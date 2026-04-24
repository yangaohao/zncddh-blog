---
title: 联系我
date: 2026-04-24 19:10:00
---

如果你想联系我，可以在这里留言。消息会发送到我的后端系统。

<form id="contact-form" style="margin-bottom: 24px;">
<div style="margin-bottom: 12px;">
<label>你的名字</label><br>
<input id="contact-name" type="text" maxlength="40" required style="width: 100%; padding: 8px; box-sizing: border-box;">
</div>

<div style="margin-bottom: 12px;">
<label>你的邮箱</label><br>
<input id="contact-email" type="email" maxlength="120" required style="width: 100%; padding: 8px; box-sizing: border-box;">
</div>

<div style="margin-bottom: 12px;">
<label>想说的话</label><br>
<textarea id="contact-message" maxlength="1000" required style="width: 100%; min-height: 140px; padding: 8px; box-sizing: border-box;"></textarea>
</div>

<button type="submit">发送</button>
</form>

<div id="contact-result"></div>

<script>
const CONTACT_API = "https://api.zncddh.cn/contact";

document.getElementById("contact-form").addEventListener("submit", async function(event) {
  event.preventDefault();

  const result = document.getElementById("contact-result");
  const nameInput = document.getElementById("contact-name");
  const emailInput = document.getElementById("contact-email");
  const messageInput = document.getElementById("contact-message");

  const name = nameInput.value.trim();
  const email = emailInput.value.trim();
  const message = messageInput.value.trim();

  if (!name || !email || !message) {
    result.innerHTML = "<p>请完整填写名字、邮箱和内容。</p>";
    return;
  }

  try {
    const response = await fetch(CONTACT_API, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ name: name, email: email, message: message })
    });

    if (!response.ok) {
      result.innerHTML = "<p>发送失败，请稍后再试。</p>";
      return;
    }

    nameInput.value = "";
    emailInput.value = "";
    messageInput.value = "";
    result.innerHTML = "<p>发送成功，我会尽快查看。</p>";
  } catch (error) {
    result.innerHTML = "<p>发送失败，请确认后端服务正在运行。</p>";
  }
});
</script>
