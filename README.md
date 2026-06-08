# 🤖 情绪对话助手 (Emotion Chat)

基于 **FastAPI + Vue 3 + DeepSeek API** 的智能情绪感知对话机器人，能够识别用户情绪并以富有同理心的方式回应。

## ✨ 功能特性

- **情绪感知对话** — 分析用户输入文本中的情绪（开心、难过、愤怒、焦虑等 8 种情绪），生成带有情绪感知的回复
- **对话管理** — 多对话支持，侧栏切换历史对话
- **情绪趋势分析** — 可视化展示用户情绪变化趋势图表
- **用户认证** — 注册/登录，JWT 令牌鉴权
- **实时推送** — WebSocket 连接管理（预留实时能力）
- **容器化部署** — Docker Compose 一键启动

## 🏗️ 技术栈

| 层级 | 技术选型 |
|------|----------|
| 后端框架 | FastAPI + Uvicorn |
| 数据库 | MySQL 8.0（aiomysql + SQLAlchemy 2.0 async）|
| LLM | DeepSeek API（OpenAI 兼容接口）|
| 认证 | JWT（python-jose）+ bcrypt |
| 前端框架 | Vue 3 + Composition API + TypeScript |
| 构建工具 | Vite 6 |
| UI 组件 | Element Plus |
| 状态管理 | Pinia |
| 图表 | ECharts + vue-echarts |
| 部署 | Docker + Docker Compose + Nginx 反代 |

## 📁 项目结构

`
PP_Pig/
├── backend/                          # FastAPI 后端
│   ├── app/
│   │   ├── main.py                   # 应用入口
│   │   ├── core/                     # 配置 & 安全
│   │   │   ├── config.py             # 环境变量配置
│   │   │   └── security.py           # JWT + 密码哈希
│   │   ├── db/
│   │   │   └── database.py           # 数据库模型 & 会话管理
│   │   ├── schemas/
│   │   │   └── schemas.py            # Pydantic 请求/响应模型
│   │   ├── services/
│   │   │   ├── llm_service.py        # DeepSeek API 封装
│   │   │   └── chat_service.py       # 对话业务逻辑
│   │   ├── api/
│   │   │   ├── deps.py               # JWT 依赖注入
│   │   │   └── v1/endpoints/
│   │   │       ├── auth.py           # 注册/登录/用户信息
│   │   │       ├── chat.py           # 发送消息/对话管理/WebSocket
│   │   │       └── emotion.py        # 情绪分析/情绪趋势
│   │   └── ws/
│   │       └── manager.py            # WebSocket 连接管理器
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/                         # Vue 3 前端
│   ├── src/
│   │   ├── main.ts                   # 入口
│   │   ├── router/index.ts           # 路由配置
│   │   ├── stores/user.ts            # 用户状态管理
│   │   ├── api/index.ts              # HTTP 请求封装
│   │   └── views/
│   │       ├── LoginView.vue         # 登录页
│   │       ├── RegisterView.vue      # 注册页
│   │       ├── ChatView.vue          # 对话主界面
│   │       └── TrendsView.vue        # 情绪趋势图表页
│   ├── Dockerfile
│   └── vite.config.ts
├── docker-compose.yml                # 容器编排
├── nginx.conf                        # Nginx 反代配置
└── .env.example                      # 环境变量模板
`

## 🚀 快速开始

### 前置条件

- Docker & Docker Compose
- DeepSeek API Key（[官网申请](https://platform.deepseek.com/)）

### 启动服务

`ash
# 1. 克隆项目
git clone <your-repo-url> && cd PP_Pig

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env，填入你的 DEEPSEEK_API_KEY 和 SECRET_KEY

# 3. 一键启动
docker-compose up -d

# 4. 访问 http://localhost
`

### 本地开发（无 Docker）

#### 后端

`ash
cd backend
pip install -r requirements.txt

# 确保本地 MySQL 已运行，并创建 emotion_chat 数据库
# 修改 .env 中 DATABASE_URL 为本地连接串

uvicorn app.main:app --reload --port 8000
`

#### 前端

`ash
cd frontend
npm install
npm run dev
# 开发服务器运行在 http://localhost:3000
# Vite 自动代理 /api -> http://localhost:8000
`

## 🔧 API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/v1/auth/register | 用户注册 |
| POST | /api/v1/auth/login | 用户登录 |
| GET | /api/v1/auth/me | 获取当前用户信息 |
| POST | /api/v1/chat/send | 发送消息（自动情绪分析） |
| GET | /api/v1/chat/conversations | 获取对话列表 |
| GET | /api/v1/chat/conversations/{id}/messages | 获取对话消息历史 |
| POST | /api/v1/emotion/analyze | 情绪分析 |
| GET | /api/v1/emotion/trends | 情绪趋势数据 |
| GET | /health | 健康检查 |

## 📊 情绪标签

| 标签 | 中文 | 说明 |
|------|------|------|
| happy | 开心 😊 | 积极正向情绪 |
| sad | 难过 😢 | 悲伤失落 |
| angry | 愤怒 😠 | 生气不满 |
| anxious | 焦虑 😰 | 紧张不安 |
| neutral | 平静 😐 | 中性状态 |
| surprised | 惊讶 😮 | 意外惊喜或惊吓 |
| fearful | 恐惧 😨 | 害怕担忧 |
| disgusted | 厌恶 🤢 | 反感排斥 |

## 🧠 情绪感知对话流程

1. 用户发送消息
2. DeepSeek 分析消息中的情绪标签 + 强度评分
3. 保存用户消息及情绪数据到数据库
4. 加载对话历史上下文
5. DeepSeek 根据情绪感知生成富有同理心的回复
6. 保存机器人回复并返回给前端
