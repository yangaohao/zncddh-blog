---
title: Docker、Nginx 与 Hexo 学习总结
date: 2026-04-20 15:00:00
tags:
  - Docker
  - Nginx
  - Hexo
  - WSL
categories:
  - 学习记录
---

# Docker、Nginx 与 Hexo 学习总结

这篇文章记录了我从零开始学习 Docker、Nginx 和 Hexo 的过程。

## 一、我先学会了 Docker 的基础概念

一开始，我先理解了 Docker 里最重要的两个概念：

- 镜像（image）是模板
- 容器（container）是镜像运行出来的实例

我练习了这些常用命令：

```bash
docker images
docker ps
docker ps -a
docker run hello-world
docker run -it ubuntu bash
docker exec -it my-ubuntu bash
docker stop my-ubuntu
docker rm my-ubuntu
```

通过这些练习，我搞明白了：

- `docker ps` 看的是正在运行的容器
- `docker ps -a` 看的是所有容器
- 容器停止后不会自动消失
- 删除容器和停止容器不是一回事

## 二、我理解了容器的运行方式

我先运行了 `hello-world` 容器，确认 Docker 环境正常。

然后我又运行了 Ubuntu 容器，进入容器内部执行命令，确认容器里也有自己的文件系统和操作环境。

我学到了：

- `docker run` 是新建并启动容器
- `docker exec` 是进入一个已经运行中的容器
- `exit` 在不同场景下效果不同

例如：

- 如果是 `docker run -it ubuntu bash` 进入的，退出后容器通常就停止
- 如果是 `docker exec -it my-ubuntu bash` 进入的，退出后后台容器仍然继续运行

## 三、我学会了端口映射

接着我运行了一个 Nginx 容器：

```bash
docker run -d --name my-nginx -p 8080:80 nginx
```

这里最关键的是：

```bash
-p 8080:80
```

它表示：

- 宿主机的 8080 端口
- 映射到容器里的 80 端口

这样我就在浏览器里通过 `http://localhost:8080` 访问到了 Nginx 欢迎页。

这一步让我真正理解了 Web 服务在 Docker 里是怎么暴露给外部访问的。

## 四、我学会了 Nginx 提供静态页面

进入 Nginx 容器后，我找到了默认网页目录：

```bash
/usr/share/nginx/html
```

我还看到了默认首页文件：

```bash
/usr/share/nginx/html/index.html
```

然后我直接修改了这个首页文件，刷新浏览器后，页面内容立刻发生变化。

这让我明白：

**Nginx 的核心作用，就是把目录里的文件返回给浏览器。**

## 五、我学会了挂载目录

接下来我没有继续在容器里手动改文件，而是改成在 WSL 里创建网站目录，再挂载给 Nginx。

例如：

```bash
-v ~/docker-learn/my-site:/usr/share/nginx/html:ro
```

这表示：

- 左边是 WSL 里的目录
- 右边是容器里的目录
- `:ro` 表示只读挂载

这样做之后，我在 WSL 里改 `index.html`，浏览器里的页面也会立刻更新。

这一点非常重要，因为后面博客、配置文件、项目目录，都会用这种方式管理。

## 六、我学会了挂载 Nginx 配置文件

除了挂载网页目录，我还学会了挂载配置文件。

例如把 WSL 里的 `default.conf` 挂载到：

```bash
/etc/nginx/conf.d/default.conf
```

这样我就可以在宿主机直接修改 Nginx 配置，而不是每次进容器手改。

我还写了一个最基础的配置：

```nginx
server {
    listen 80;
    server_name localhost;

    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

通过这个配置，我理解了几个很重要的概念：

- `listen`：监听哪个端口
- `root`：网站根目录
- `index`：默认首页文件
- `location`：请求路径如何处理

## 七、我学会了看日志和检查配置

为了更像真实环境，我还练习了这些命令：

```bash
docker logs my-nginx
docker exec -it my-nginx nginx -t
docker exec -it my-nginx nginx -s reload
```

这几步让我明白：

- 网页打不开时，要先看日志
- 改配置后，先用 `nginx -t` 检查语法
- 配置没问题后，再用 `nginx -s reload` 重载服务

我还配置了一个 `/test` 路径：

```nginx
location /test {
    return 200 'hello from /test';
    add_header Content-Type text/plain;
}
```

然后成功访问了：

```text
http://localhost:8080/test
```

这让我理解了 Nginx 的路由配置是怎么生效的。

## 八、我学会了使用 Docker Compose

手敲 `docker run` 很方便学习，但实际项目更适合用 `docker-compose.yml` 管理。

我后面把 Nginx 服务改成了 Compose 方式启动，例如：

```yaml
services:
  nginx:
    image: nginx
    container_name: my-nginx
    ports:
      - "8080:80"
    volumes:
      - /home/yah/docker-learn/my-site:/usr/share/nginx/html:ro
      - /home/yah/docker-learn/nginx-conf/default.conf:/etc/nginx/conf.d/default.conf:ro
```

然后我学会了：

```bash
docker compose up -d
docker compose ps
docker compose logs
docker compose down
```

这让我理解了：

- Compose 可以把复杂命令写进配置文件
- 更适合管理完整项目
- 后面多服务协作时会非常方便

## 九、我开始学习 Hexo

在学完 Docker 和 Nginx 基础后，我开始引入 Hexo。

我先用 Node 容器初始化了 Hexo 项目，在容器里执行了：

```bash
npm install -g hexo-cli
hexo init .
npm install
```

初始化后，我看到了这些目录和文件：

- `_config.yml`
- `source/`
- `themes/`
- `scaffolds/`
- `package.json`

这一步让我明白：

**Hexo 本质上是一个静态博客生成器。**

## 十、我理解了 Hexo 的 public 目录

接着我执行了：

```bash
hexo clean
hexo generate
```

生成之后，我看到了 `public/` 目录，里面有：

- `index.html`
- `archives/`
- `css/`
- `js/`

这让我理解了：

- `source/` 是博客源内容
- `public/` 是生成出来的网站成品

也就是说，Hexo 并不是必须长期在线运行，它最重要的作用其实是：

**把博客内容生成成静态网页文件。**

## 十一、我学会了用 Docker 跑 Hexo 预览

为了能在浏览器里看博客，我又用 Docker 跑了 Hexo 预览服务，并且做了端口映射：

```bash
docker run --rm -it \
  -p 4000:4000 \
  -v $(pwd):/app \
  -w /app \
  node:20-bullseye \
  bash
```

然后在容器里执行：

```bash
npx hexo server --host 0.0.0.0
```

这样我就可以在浏览器访问：

```text
http://localhost:4000
```

这一步让我明白：

- Hexo 可以作为开发预览服务来用
- 容器里跑的服务，要记得映射端口
- `--host 0.0.0.0` 很重要，否则外部访问不到

## 十二、我把 Hexo 和 Nginx 串起来了

最后，我学会了把 Hexo 和 Nginx 结合起来：

- Hexo 负责生成 `public/`
- Nginx 负责托管 `public/`

我写了一个新的 `docker-compose.yml`，让 Nginx 直接挂载：

```text
/home/yah/docker-learn/hexo-blog/public
```

然后通过 Nginx 发布 Hexo 生成的博客页面。

这让我真正理解了静态博客的典型部署思路：

1. 写文章
2. Hexo 生成静态文件
3. Nginx 托管静态文件
4. 浏览器访问网站

## 十三、这次学习我最大的收获

通过这次从零实践，我不只是搭了一个博客，更重要的是建立了下面这套完整理解：

- Docker 解决环境运行问题
- Nginx 解决网页访问问题
- Hexo 解决静态博客生成问题

它们三者的关系可以总结成一句话：

**Hexo 生成网页，Nginx 提供网页，Docker 管理运行环境。**

## 十四、下一步计划

接下来我准备继续学习这些内容：

- Hexo 主题配置
- 标签、分类、归档页面
- Dockerfile 的写法
- Compose 管多个服务
- Nginx 更复杂的配置
- 把博客真正部署到服务器

## 结语

这次学习路线让我第一次把 Docker、Nginx 和静态博客真正串起来。

以前这些概念看起来很散，但实际做完以后就清楚了：

- Docker 不是只会背命令
- Nginx 不是只会装和开
- Hexo 也不只是写文章工具

它们组合起来，正好构成了一套很典型的现代开发和部署练习项目。

补充一句：这是生产镜像更新测试。
