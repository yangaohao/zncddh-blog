---
title: FastAPI 学习笔记：从入门到项目结构
date: 2026-04-24
tags:

* Python
* FastAPI
* Backend
* API
  categories:
* 后端开发
---

# FastAPI 学习笔记：从入门到项目结构

FastAPI 是一个基于 Python 类型提示的现代 Web API 框架，适合用来快速构建高性能、自动生成接口文档、数据校验清晰的后端服务。它的核心体验可以概括为：**用 Python 类型注解写 API，框架帮你完成请求解析、参数校验、文档生成和响应序列化**。

这篇笔记按学习路径整理：先跑起来，再理解路由、参数、请求体、响应模型、依赖注入，最后整理一个较常见的项目结构。

---

## 1. FastAPI 适合解决什么问题

FastAPI 常用于：

* 构建 RESTful API
* 构建前后端分离项目的后端接口
* 构建机器学习模型服务接口
* 构建内部管理系统 API
* 构建微服务中的 HTTP 服务

相比传统 Web 框架，FastAPI 的一个明显特点是：**你写的类型注解不只是给编辑器看的，FastAPI 会直接使用这些类型信息完成参数解析、校验和 OpenAPI 文档生成**。

---

## 2. 安装与启动

建议先创建虚拟环境：

```bash
python -m venv .venv
source .venv/bin/activate  # macOS / Linux
# Windows: .venv\Scripts\activate
```

安装 FastAPI：

```bash
pip install fastapi
```

创建 `main.py`：

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello FastAPI"}
```

启动服务：

```bash
fastapi dev main.py
```

也可以使用 Uvicorn 启动：

```bash
uvicorn main:app --reload
```

访问：

```text
http://127.0.0.1:8000
```

交互式 API 文档：

```text
http://127.0.0.1:8000/docs
```

OpenAPI JSON：

```text
http://127.0.0.1:8000/openapi.json
```

---

## 3. 路径操作：Path Operation

FastAPI 使用装饰器声明接口：

```python
@app.get("/items")
def list_items():
    return [{"id": 1, "name": "Apple"}]
```

这里有几个概念：

* `@app.get("/items")` 表示处理 `GET /items` 请求
* `/items` 是路径
* `get` 是 HTTP 方法
* `list_items` 是路径操作函数
* 返回值会自动转成 JSON 响应

常见 HTTP 方法：

```python
@app.get("/items")
def list_items():
    return []


@app.post("/items")
def create_item():
    return {"message": "created"}


@app.put("/items/{item_id}")
def update_item(item_id: int):
    return {"item_id": item_id}


@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    return {"message": "deleted"}
```

---

## 4. 路径参数

路径参数写在 URL 中，用 `{}` 声明：

```python
@app.get("/items/{item_id}")
def get_item(item_id: int):
    return {"item_id": item_id}
```

请求：

```text
GET /items/123
```

FastAPI 会自动把 `123` 转成 `int`。如果传入的不是整数，例如：

```text
GET /items/abc
```

FastAPI 会自动返回校验错误。

---

## 5. 查询参数

查询参数一般出现在 `?` 后面：

```python
@app.get("/search")
def search_items(keyword: str, limit: int = 10):
    return {
        "keyword": keyword,
        "limit": limit,
    }
```

请求：

```text
GET /search?keyword=python&limit=5
```

如果参数有默认值，它就是可选参数；没有默认值时，就是必填参数。

---

## 6. 请求体与 Pydantic 模型

FastAPI 通常使用 Pydantic 模型定义请求体：

```python
from pydantic import BaseModel


class ItemCreate(BaseModel):
    name: str
    price: float
    description: str | None = None


@app.post("/items")
def create_item(item: ItemCreate):
    return item
```

请求体示例：

```json
{
  "name": "Keyboard",
  "price": 299.0,
  "description": "Mechanical keyboard"
}
```

这个模型会带来三个好处：

1. 自动解析 JSON 请求体
2. 自动校验字段类型
3. 自动生成 API 文档

---

## 7. 响应模型 response_model

请求体模型用于接收数据，响应模型用于控制返回数据结构。

```python
from pydantic import BaseModel


class UserIn(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    username: str


@app.post("/users", response_model=UserOut)
def create_user(user: UserIn):
    return user
```

这里传入的请求体包含 `password`，但接口最终返回时只会保留 `username`。这在用户信息、订单信息等场景中很有用，可以避免把敏感字段返回给前端。

---

## 8. 状态码与接口元信息

可以给路径操作添加状态码、标签、摘要、描述等信息：

```python
from fastapi import status


@app.post(
    "/items",
    status_code=status.HTTP_201_CREATED,
    tags=["items"],
    summary="创建商品",
)
def create_item(item: ItemCreate):
    return item
```

这些信息会体现在自动生成的 API 文档中。

---

## 9. async def 还是 def

FastAPI 支持两种写法：

```python
@app.get("/sync")
def sync_api():
    return {"type": "sync"}
```

```python
@app.get("/async")
async def async_api():
    return {"type": "async"}
```

简单理解：

* 如果函数内部主要是普通同步代码，可以使用 `def`
* 如果函数内部需要 `await`，例如异步数据库、异步 HTTP 请求，可以使用 `async def`

示例：

```python
import httpx


@app.get("/github")
async def get_github():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.github.com")
    return response.json()
```

注意：不要在 `async def` 中直接执行耗时的同步阻塞操作，否则可能影响并发性能。

---

## 10. 依赖注入 Depends

FastAPI 的依赖注入可以用来复用公共逻辑，比如登录校验、数据库连接、分页参数等。

```python
from fastapi import Depends


def common_pagination(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}


@app.get("/items")
def list_items(pagination: dict = Depends(common_pagination)):
    return pagination
```

请求：

```text
GET /items?skip=20&limit=10
```

返回：

```json
{
  "skip": 20,
  "limit": 10
}
```

依赖注入常见用途：

* 获取当前登录用户
* 校验权限
* 获取数据库 Session
* 解析公共查询参数
* 注入配置项

---

## 11. 错误处理

可以使用 `HTTPException` 主动返回错误：

```python
from fastapi import HTTPException


fake_items = {
    1: {"name": "Apple"},
    2: {"name": "Banana"},
}


@app.get("/items/{item_id}")
def get_item(item_id: int):
    item = fake_items.get(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
```

当资源不存在时，返回 404 比返回普通 JSON 更符合 HTTP API 的语义。

---

## 12. APIRouter：拆分路由

当项目变大时，不建议把所有接口都写在 `main.py` 中。可以用 `APIRouter` 拆分模块。

目录结构示例：

```text
app/
├── main.py
├── routers/
│   ├── __init__.py
│   └── items.py
└── schemas/
    ├── __init__.py
    └── item.py
```

`app/schemas/item.py`：

```python
from pydantic import BaseModel


class ItemCreate(BaseModel):
    name: str
    price: float
```

`app/routers/items.py`：

```python
from fastapi import APIRouter
from app.schemas.item import ItemCreate

router = APIRouter(prefix="/items", tags=["items"])


@router.get("")
def list_items():
    return []


@router.post("")
def create_item(item: ItemCreate):
    return item
```

`app/main.py`：

```python
from fastapi import FastAPI
from app.routers import items

app = FastAPI()

app.include_router(items.router)
```

这样做的好处是：

* 每个业务模块单独维护
* `main.py` 更简洁
* 方便多人协作
* 方便后续扩展认证、权限、数据库等功能

---

## 13. 一个更完整的项目结构

下面是一个适合中小型项目的结构：

```text
app/
├── main.py
├── core/
│   ├── config.py
│   └── security.py
├── db/
│   ├── session.py
│   └── models.py
├── schemas/
│   ├── user.py
│   └── item.py
├── routers/
│   ├── users.py
│   └── items.py
├── services/
│   ├── user_service.py
│   └── item_service.py
└── dependencies.py
```

各目录职责：

| 目录                | 作用                 |
| ----------------- | ------------------ |
| `main.py`         | 创建 FastAPI 应用，注册路由 |
| `core/`           | 配置、安全、通用基础设施       |
| `db/`             | 数据库连接、ORM 模型       |
| `schemas/`        | Pydantic 请求/响应模型   |
| `routers/`        | API 路由层            |
| `services/`       | 业务逻辑层              |
| `dependencies.py` | 公共依赖注入函数           |

一个比较清晰的调用链是：

```text
router -> service -> database
```

也就是说：

* `router` 负责接收请求和返回响应
* `service` 负责业务逻辑
* `db` 负责数据库读写

不要把所有业务逻辑都塞进路由函数里，否则项目变大后会很难维护。

---

## 14. 常见开发命令

开发环境启动：

```bash
fastapi dev app/main.py
```

或：

```bash
uvicorn app.main:app --reload
```

生产环境启动可以使用：

```bash
fastapi run app/main.py
```

也可以手动使用 Uvicorn：

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

生成依赖文件：

```bash
pip freeze > requirements.txt
```

安装依赖：

```bash
pip install -r requirements.txt
```

---

## 15. 一个完整的小示例

```python
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI(title="Item API")


class ItemCreate(BaseModel):
    name: str
    price: float
    description: str | None = None


class ItemOut(BaseModel):
    id: int
    name: str
    price: float
    description: str | None = None


items: dict[int, ItemOut] = {}
next_id = 1


@app.get("/items", response_model=list[ItemOut], tags=["items"])
def list_items():
    return list(items.values())


@app.get("/items/{item_id}", response_model=ItemOut, tags=["items"])
def get_item(item_id: int):
    item = items.get(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.post(
    "/items",
    response_model=ItemOut,
    status_code=status.HTTP_201_CREATED,
    tags=["items"],
)
def create_item(item: ItemCreate):
    global next_id
    new_item = ItemOut(id=next_id, **item.model_dump())
    items[next_id] = new_item
    next_id += 1
    return new_item
```

启动后可以访问：

```text
http://127.0.0.1:8000/docs
```

在文档页面里可以直接测试新增、查询、列表接口。

---

## 16. 学习路线建议

建议按这个顺序学习：

1. 跑通 Hello World
2. 学会路径参数、查询参数、请求体
3. 学会 Pydantic 模型
4. 学会响应模型和状态码
5. 学会 `HTTPException` 错误处理
6. 学会 `Depends` 依赖注入
7. 学会 `APIRouter` 拆分项目
8. 接入数据库，例如 SQLAlchemy 或 SQLModel
9. 加入 JWT 登录认证
10. 学习部署和日志监控

---

## 17. 常见坑

### 17.1 忘记安装 ASGI 服务器

如果只安装了很老的组合或手动拆分依赖，可能会缺少运行服务器。现代 FastAPI 安装方式通常已经更方便，但如果使用 Uvicorn 运行失败，可以手动安装：

```bash
pip install uvicorn
```

### 17.2 路径顺序写错

例如：

```python
@app.get("/users/{user_id}")
def get_user(user_id: str):
    return {"user_id": user_id}


@app.get("/users/me")
def get_me():
    return {"user_id": "me"}
```

这种情况下，`/users/me` 可能会先被 `/users/{user_id}` 匹配。更推荐把固定路径写在前面：

```python
@app.get("/users/me")
def get_me():
    return {"user_id": "me"}


@app.get("/users/{user_id}")
def get_user(user_id: str):
    return {"user_id": user_id}
```

### 17.3 在 async def 里写阻塞代码

例如在 `async def` 中直接调用耗时的同步网络请求、同步数据库查询、大文件读写，都可能影响并发性能。要么改用异步库，要么使用普通 `def`，让 FastAPI 以合适方式处理。

### 17.4 Pydantic v2 的写法变化

在 Pydantic v2 中，模型转字典通常使用：

```python
item.model_dump()
```

而不是老版本常见的：

```python
item.dict()
```

如果看旧教程时发现写法不同，要注意版本差异。

---

## 18. 总结

FastAPI 的核心优势是：

* 类型注解驱动开发
* 自动参数校验
* 自动生成 API 文档
* 支持同步和异步接口
* 路由拆分清晰
* 适合快速构建现代 API 服务

学习 FastAPI 不要只停留在写接口本身，更重要的是逐步掌握：

```text
接口设计 -> 参数校验 -> 响应模型 -> 依赖注入 -> 项目分层 -> 数据库 -> 认证 -> 部署
```

掌握这些之后，就可以用 FastAPI 搭建比较完整的后端项目了。
