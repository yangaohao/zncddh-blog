---
title: 留言板
date: 2026-04-24 18:20:00
---

欢迎在这里留言。

<form id="comment-form" style="margin-bottom: 24px;">
<div style="margin-bottom: 12px;">
<label>昵称</label><br>
<input id="comment-name" type="text" maxlength="40" required style="width: 100%; padding: 8px; box-sizing: border-box;">
</div>
<div style="margin-bottom: 12px;">
<label>留言内容</label><br>
<textarea id="comment-content" maxlength="500" required style="width: 100%; min-height: 100px; padding: 8px; box-sizing: border-box;"></textarea>
</div>
<button type="submit">提交留言</button>
</form>

<h2>留言列表</h2>
<div id="comments-list">加载中...</div>

<script>
const API_BASE = "https://api.zncddh.cn";

async function loadComments() {
  const list = document.getElementById("comments-list");

  try {
    const response = await fetch(API_BASE + "/comments");
    const data = await response.json();

    if (!data.comments || data.comments.length === 0) {
      list.innerHTML = "<p>还没有留言，欢迎第一个留言。</p>";
      return;
    }

    list.innerHTML = data.comments
      .slice()
      .reverse()
      .map(function(comment) {
        return '<div style="border: 1px solid #ddd; border-radius: 8px; padding: 12px; margin-bottom: 12px;">'
          + '<strong>' + escapeHtml(comment.name) + '</strong>'
          + '<div style="font-size: 12px; color: #888;">' + new Date(comment.created_at).toLocaleString() + '</div>'
          + '<p>' + escapeHtml(comment.content) + '</p>'
          + '</div>';
      })
      .join("");
  } catch (error) {
    list.innerHTML = "<p>留言加载失败，请确认后端服务正在运行。</p>";
  }
}

function escapeHtml(text) {
  return String(text)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

document.getElementById("comment-form").addEventListener("submit", async function(event) {
  event.preventDefault();

  const nameInput = document.getElementById("comment-name");
  const contentInput = document.getElementById("comment-content");

  const name = nameInput.value.trim();
  const content = contentInput.value.trim();

  if (!name || !content) {
    alert("昵称和留言内容都不能为空。");
    return;
  }

  try {
    const response = await fetch(API_BASE + "/comments", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ name: name, content: content })
    });

    if (!response.ok) {
      alert("提交失败，请稍后再试。");
      return;
    }

    nameInput.value = "";
    contentInput.value = "";
    await loadComments();
  } catch (error) {
    alert("提交失败，请确认后端服务正在运行。");
  }
});

loadComments();
</script>
