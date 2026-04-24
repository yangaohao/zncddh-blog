---
title: 总路线
date: 2026-04-23 11:33:45
tags:
  - Docker
  - Nginx
  - Hexo
  - WSL
categories:
  - 总结
---
# Docker + Nginx + Hexo 最终速查版命令清单

## 一、项目结构

```text
~/docker-learn/
├── hello-docker/      # Docker/Nginx 基础练习
├── my-site/           # 最早练习用的静态网页目录
├── nginx-conf/        # 最早练习用的 Nginx 配置
├── hexo-blog/         # Hexo 博客项目（开发 + 生产构建）
└── hexo-nginx/        # 挂载式 Nginx 发布（开发式发布）
```

---

## 二、开发环境：Hexo 本地预览

目录：

```bash
cd ~/docker-learn/hexo-blog
```

启动开发环境：

```bash
docker compose up -d
```

查看状态：

```bash
docker compose ps
```

查看日志：

```bash
docker compose logs --tail 50
```

进入运行中的 Hexo 容器：

```bash
docker compose exec hexo bash
```

浏览器访问：

```text
http://localhost:4000
```

停止开发环境：

```bash
docker compose down
```

---

## 三、Hexo 常用命令

### 1. 新建文章

```bash
docker compose exec hexo hexo new post "文章标题"
```

或者一次性容器方式：

```bash
docker compose run --rm hexo bash -lc "hexo new post '文章标题'"
```

### 2. 重新生成静态文件

```bash
docker compose run --rm hexo bash -lc "hexo clean && hexo generate"
```

### 3. 查看文章目录

```bash
ls source/_posts
```

### 4. 查看生成结果

```bash
ls public
find public -maxdepth 2 -type f | head
```

---

## 四、开发式发布：Nginx 挂载 public 目录

目录：

```bash
cd ~/docker-learn/hexo-nginx
```

启动挂载式发布环境：

```bash
docker compose up -d
```

查看状态：

```bash
docker compose ps
```

查看日志：

```bash
docker compose logs --tail 50
```

进入 Nginx 容器检查静态文件：

```bash
docker exec -it hexo-nginx ls -la /usr/share/nginx/html
docker exec -it hexo-nginx ls -la /usr/share/nginx/html/index.html
```

浏览器访问：

```text
http://localhost:8081
```

停止挂载式发布环境：

```bash
docker compose down
```

---

## 五、生产环境：多阶段构建镜像

目录：

```bash
cd ~/docker-learn/hexo-blog
```

### 1. 手动构建生产镜像

```bash
docker build -f Dockerfile.prod -t hexo-prod .
```

查看镜像：

```bash
docker images | grep hexo-prod
```

### 2. 手动启动生产容器

```bash
docker run --rm -d -p 8082:80 --name hexo-prod-test hexo-prod
```

查看运行状态：

```bash
docker ps
```

查看日志：

```bash
docker logs --tail 50 hexo-prod-test
```

检查容器内静态文件：

```bash
docker exec -it hexo-prod-test ls -la /usr/share/nginx/html | head
```

浏览器访问：

```text
http://localhost:8082
```

删除测试容器：

```bash
docker rm -f hexo-prod-test
```

---

## 六、生产环境：Compose 管理

目录：

```bash
cd ~/docker-learn/hexo-blog
```

### 1. 启动生产环境

```bash
docker compose -f docker-compose.prod.yml up -d --build
```

### 2. 查看状态

```bash
docker compose -f docker-compose.prod.yml ps
```

### 3. 查看日志

```bash
docker compose -f docker-compose.prod.yml logs --tail 50
```

### 4. 停止生产环境

```bash
docker compose -f docker-compose.prod.yml down
```

### 5. 强制重建生产环境

```bash
docker compose -f docker-compose.prod.yml up -d --build --force-recreate
```

浏览器访问：

```text
http://localhost:8082
```

---

## 七、日常完整工作流

### 场景 1：写文章并本地预览

```bash
cd ~/docker-learn/hexo-blog
docker compose up -d
```

访问：

```text
http://localhost:4000
```

### 场景 2：改完文章后生成静态文件

```bash
cd ~/docker-learn/hexo-blog
docker compose run --rm hexo bash -lc "hexo clean && hexo generate"
```

### 场景 3：查看挂载式发布结果

```bash
cd ~/docker-learn/hexo-nginx
docker compose up -d
```

访问：

```text
http://localhost:8081
```

### 场景 4：更新生产环境

```bash
cd ~/docker-learn/hexo-blog
docker compose -f docker-compose.prod.yml up -d --build
```

访问：

```text
http://localhost:8082
```

---

## 八、最常用排错命令

### 1. 看容器是否在运行

```bash
docker ps
docker compose ps
docker compose -f docker-compose.prod.yml ps
```

### 2. 看日志

```bash
docker logs 容器名
docker compose logs --tail 50
docker compose -f docker-compose.prod.yml logs --tail 50
```

### 3. 进入容器

```bash
docker exec -it 容器名 bash
docker compose exec hexo bash
```

### 4. 看端口占用

```bash
docker ps
```

重点看类似：

```text
0.0.0.0:4000->4000/tcp
0.0.0.0:8081->80/tcp
0.0.0.0:8082->80/tcp
```

### 5. 如果报端口冲突

删除旧容器：

```bash
docker rm -f 容器名
```

### 6. 检查挂载目录是否正确

宿主机查看：

```bash
ls -la ~/docker-learn/hexo-blog/public
ls -la ~/docker-learn/hexo-blog/public/index.html
```

容器里查看：

```bash
docker exec -it hexo-nginx ls -la /usr/share/nginx/html
docker exec -it hexo-nginx ls -la /usr/share/nginx/html/index.html
```

### 7. 检查 Nginx 配置语法

```bash
docker exec -it my-nginx nginx -t
```

### 8. 重载 Nginx 配置

```bash
docker exec -it my-nginx nginx -s reload
```

---

## 九、当前几个地址的意义

### 开发预览
```text
http://localhost:4000
```

用途：
- 写文章时本地预览
- Hexo 开发环境

### 挂载式发布
```text
http://localhost:8081
```

用途：
- Nginx 直接挂载 `public/`
- 开发式发布验证

### 生产式发布
```text
http://localhost:8082
```

用途：
- 多阶段构建后的生产镜像
- 更接近真实部署

---

## 十、当前几个核心文件的作用

### hexo-blog/docker-compose.yml
开发环境 compose 文件

### hexo-blog/Dockerfile
开发镜像 Dockerfile（my-hexo）

### hexo-blog/Dockerfile.prod
生产镜像多阶段构建文件

### hexo-blog/docker-compose.prod.yml
生产环境 compose 文件

### hexo-nginx/docker-compose.yml
挂载式 Nginx 发布配置

---

## 十一、几个关键概念一句话版

### Docker
负责管理环境、镜像、容器。

### Hexo
负责把 Markdown 文章生成成静态网页。

### Nginx
负责把静态网页提供给浏览器访问。

### bind mount
把宿主机目录直接映射进容器。

### named volume
让 Docker 管理某个数据目录。

### Dockerfile
定义“镜像怎么构建”。

### multi-stage build
第一阶段构建，第二阶段运行，适合生产环境。

---

## 十二、一句话总总结

**Hexo 生成网页，Nginx 提供网页，Docker 管理运行环境。**

