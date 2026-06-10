# 情绪对话助手 (Emotion Chat)

基于 **FastAPI + Vue 3 + DeepSeek API** 的智能情绪感知对话机器人，能够识别用户情绪并以富有同理心的方式回应。无需注册登录，打开即用。

---

## 技术栈

| 层级 | 技术选型 |
|------|----------|
| 后端框架 | FastAPI + Uvicorn |
| 数据库 | MySQL 8.0（aiomysql + SQLAlchemy 2.0 async） |
| LLM | DeepSeek API（OpenAI 兼容接口） |
| 前端框架 | Vue 3 + Composition API + TypeScript |
| 构建工具 | Vite 6 |
| UI 组件 | Element Plus + Element Plus Icons |
| 状态管理 | Pinia |
| 图表 | ECharts 5 + vue-echarts 7 |
| HTTP 客户端 | Axios |
| 部署 | Docker + Docker Compose + Nginx 反向代理 |

---

## 功能

- **情绪感知对话** — 分析用户输入文本中的情绪（快乐、委屈、烦躁、焦虑、孤单、疲惫、生气、平淡共 8 种），生成带有情绪感知的回复
- **多对话管理** — 侧边栏切换历史对话，支持创建新对话
- **情绪趋势分析** — 以折线图可视化展示用户情绪变化趋势，统计各情绪出现频次
- **免登录使用** — 基于设备标识（device_id）自动识别，无需注册/登录
- **容器化部署** — Docker Compose 一键启动，Nginx 反向代理

---

## 项目结构

```
PP_Pig/
├─ backend/                          # FastAPI 后端
│  ├─ app/
│  │  ├─ main.py                     # 应用入口 & 生命周期
│  │  ├─ core/
│  │  │  └─ config.py                # 环境变量配置
│  │  ├─ db/
│  │  │  └─ database.py              # 数据库模型 & 会话管理
│  │  ├─ schemas/
│  │  │  └─ schemas.py               # Pydantic 请求/响应模型
│  │  ├─ services/
│  │  │  ├─ chat_service.py          # 对话业务逻辑
│  │  │  └─ llm_service.py           # DeepSeek API 封装
│  │  ├─ api/
│  │  │  └─ v1/endpoints/
│  │  │     ├─ chat.py               # 发送消息 / 对话管理
│  │  │     └─ emotion.py            # 情绪分析 / 情绪趋势
│  │  └─ ws/
│  │     └─ manager.py               # WebSocket 连接管理器
│  ├─ requirements.txt
│  └─ Dockerfile
├─ frontend/                         # Vue 3 前端
│  ├─ src/
│  │  ├─ main.ts                     # 入口
│  │  ├─ router/index.ts             # 路由配置
│  │  ├─ stores/user.ts              # 设备状态管理
│  │  ├─ api/index.ts                # HTTP 请求封装
│  │  └─ views/
│  │     ├─ ChatView.vue             # 对话主界面
│  │     └─ TrendsView.vue           # 情绪趋势图表页
│  ├─ Dockerfile
│  └─ vite.config.ts
├─ docker-compose.yml                # 容器编排
├─ nginx.conf                        # Nginx 反向代理配置
└─ .env.example                      # 环境变量模板
```

---

## 快速开始

### 前置条件

- Docker & Docker Compose
- DeepSeek API Key（[官网申请](https://platform.deepseek.com/)）

### 启动服务

```bash
# 1. 克隆项目
git clone <your-repo-url> && cd PP_Pig

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env，填入你的 DEEPSEEK_API_KEY

# 3. 一键启动
docker-compose up -d

# 4. 访问 http://localhost
```

### 本地开发（无 Docker）

#### 后端

```bash
cd backend
pip install -r requirements.txt

# 确保本地 MySQL 已运行，并创建 emotion_chat 数据库
# 修改 backend/.env 中 DATABASE_URL 为本地连接串

uvicorn app.main:app --reload --port 8002
```

#### 前端

```bash
cd frontend
npm install
npm run dev
# 开发服务器运行在 http://localhost:5173
# Vite 自动代理 /api -> http://localhost:8002
```

---

## API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/v1/chat/send | 发送消息（自动情绪分析） |
| GET | /api/v1/chat/conversations | 获取对话列表 |
| GET | /api/v1/chat/conversations/{id}/messages | 获取对话消息历史 |
| POST | /api/v1/emotion/analyze | 情绪分析 |
| GET | /api/v1/emotion/trends | 情绪趋势数据 |
| GET | /health | 健康检查 |

### 情绪标签

| 标签 | 中文 | 说明 |
|------|------|------|
| happy | 快乐 | 积极正向情绪 |
| aggrieved | 委屈 | 被误解冤枉 |
| irritated | 烦躁 | 焦虑恼怒 |
| anxious | 焦虑 | 紧张不安 |
| lonely | 孤单 | 寂寞无人陪伴 |
| tired | 疲惫 | 身心俱疲 |
| angry | 生气 | 愤怒不满 |
| calm | 平淡 | 中性状态 |

---

## 部署

### 服务器要求

- **系统**: CentOS 7+ / Ubuntu 20.04+
- **配置**: 2核 4G / 50GB 磁盘 / 公网 200Mbps
- **软件**: Docker + Docker Compose

### 部署步骤

```bash
# 1. 安装 Docker
curl -fsSL https://get.docker.com | bash
systemctl start docker && systemctl enable docker

# 2. 创建项目目录
mkdir -p /www/pp_pig && cd /www/pp_pig

# 3. 上传项目文件（或 git clone）
#   确保以下文件就位：
#   - docker-compose.yml
#   - nginx.conf
#   - backend/ 目录
#   - frontend/ 目录

# 4. 配置环境变量
cat > .env << 'EOF'
DEEPSEEK_API_KEY=sk-your-api-key
EOF

# 5. 构建并启动
docker compose up -d --build

# 6. 验证
curl http://localhost:8000/health
curl -X POST http://localhost:8000/api/v1/chat/send \
  -H "Content-Type: application/json" \
  -d '{"device_id":"test","message":"你好"}'
```

### 数据库认证模式

若使用 MySQL 8.0，默认认证插件为 `caching_sha2_password`，部分客户端不兼容，可切换为 `mysql_native_password`：

```bash
docker exec -it emotion-chat-db mysql -uroot -p1234 -e "
ALTER USER '"'"'root'"'"'@'"'"'%'"'"' IDENTIFIED WITH mysql_native_password BY '"'"'1234'"'"';
FLUSH PRIVILEGES;
"
```

---

## 维护

### 日志查看

```bash
docker compose logs -f backend      # 查看后端日志
docker compose logs -f frontend     # 查看前端日志
docker compose logs -f db           # 查看 MySQL 日志
```

### 服务管理

```bash
docker compose ps                   # 查看容器状态
docker compose restart backend      # 重启后端
docker compose stop backend         # 停止后端
docker compose start backend        # 启动后端
docker compose down                 # 停止所有服务
docker compose up -d                # 启动所有服务
```

### 更新代码

```bash
# 直接修改文件后重启
docker compose restart backend

# 或使用 git 拉取更新
git pull
docker compose up -d --build
```

### 数据库备份

```bash
# 导出
docker exec emotion-chat-db mysqldump -uroot -p1234 emotion_chat > backup.sql

# 导入
cat backup.sql | docker exec -i emotion-chat-db mysql -uroot -p1234 emotion_chat

# 备份整个项目配置
tar -czf pp_pig_backup.tar.gz docker-compose.yml .env nginx.conf
```

### 容器重建（无缓存）

```bash
docker compose build --no-cache backend
docker compose up -d --build
```

---

## 情绪感知对话流程

1. 用户发送消息
2. DeepSeek 分析消息中的情绪标签 + 强度评分
3. 保存用户消息及情绪数据到数据库
4. 加载对话历史上下文
5. DeepSeek 根据情绪感知生成富有同理心的回复
6. 保存机器人回复并返回给前端

---

## 更新日志

### 2026-06-10
- 移除用户认证/登录功能，改为设备标识（device_id）自动识别
- 清理数据库 User 模型及相关代码
- 修复中文乱码问题
- 优化 Docker 部署流程
- 更新文档

### 2026-05-20
- 初始版本发布
- 实现情绪感知对话、多对话管理、情绪趋势分析
- 支持 Docker 容器化部署
- 集成 DeepSeek API