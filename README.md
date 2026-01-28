# 反诈全国快讯解析

基于 Flask 和飞书多维表格的反诈资讯聚合平台，采用苹果设计风格，融入中国红主题色。

## 功能特点

- 📝 反诈快讯展示（标题、日期、摘要、来源）
- 🔍 搜索功能（支持标题、摘要、来源搜索）
- 💬 评论系统
- 🎨 苹果风格设计 + 中国红主题
- 📱 响应式设计，支持移动端
- ⚡ 数据缓存，提升性能

## 技术栈

- **后端**: Python Flask 3.0.0
- **前端**: 原生 HTML/CSS/JavaScript
- **数据源**: 飞书多维表格
- **数据库**: SQLite (评论功能)
- **缓存**: Flask-Caching

## 快速开始

### 1. 克隆项目

```bash
git clone <repository-url>
cd blog
```

### 2. 创建虚拟环境

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置环境变量

复制 `.env.example` 为 `.env`：

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入您的飞书应用信息：

```env
FEISHU_APP_ID=your_app_id_here
FEISHU_APP_SECRET=your_app_secret_here
BASE_ID=your_base_id_here
TABLE_ID=your_table_id_here
SECRET_KEY=your_secret_key_here
```

### 5. 创建飞书应用

1. 访问 [飞书开放平台](https://open.feishu.cn/)
2. 创建企业自建应用
3. 获取 App ID 和 App Secret
4. 开启权限：`bitable:record:read`
5. 创建多维表格，包含以下字段：
   - 标题
   - 日期
   - 摘要
   - 账号

### 6. 运行应用

```bash
python app.py
```

访问 http://localhost:5000

## 项目结构

```
blog/
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── vercel.json          # Vercel 部署配置
├── config.py            # 配置类
├── app.py               # 应用入口
├── models/
│   ├── article.py       # 文章模型
│   └── comment.py       # 评论模型
├── services/
│   ├── feishu_client.py # 飞书 API 客户端
│   └── cache.py         # 缓存服务
├── routes/
│   ├── __init__.py
│   ├── views.py         # 页面路由
│   └── api.py           # API 路由
├── static/
│   ├── css/
│   │   ├── style.css    # 主样式
│   │   └── responsive.css
│   └── js/
│       ├── main.js      # 主交互
│       ├── search.js    # 搜索功能
│       └── comments.js  # 评论功能
├── templates/
│   ├── base.html        # 基础模板
│   ├── index.html       # 首页
│   ├── detail.html      # 详情页
│   ├── search.html      # 搜索页
│   ├── 404.html
│   └── 500.html
└── database/
    └── comments.db      # SQLite 数据库
```

## 部署到 Vercel

### 1. 准备工作

- 将代码推送到 GitHub
- 注册 [Vercel](https://vercel.com/)

### 2. 导入项目

1. 在 Vercel 控制台点击 "Import Project"
2. 选择您的 GitHub 仓库
3. Vercel 会自动检测 Python 项目

### 3. 配置环境变量

在 Vercel 项目设置中添加以下环境变量：

```
FEISHU_APP_ID
FEISHU_APP_SECRET
BASE_ID
TABLE_ID
SECRET_KEY
```

### 4. 注意事项

- Vercel 的文件系统是只读的，评论数据库需要使用外部服务（如 Supabase）
- 当前配置适合本地开发，生产环境建议使用云数据库

## 开发建议

### 本地开发

```bash
# 启用调试模式
export FLASK_ENV=development
python app.py
```

### 数据管理

在飞书多维表格中编辑内容，系统会自动更新缓存。

### 测试

```bash
# 运行测试
python -m pytest tests/
```

## 常见问题

### 1. 数据显示异常

- 检查飞书应用权限是否正确开启
- 验证多维表格的字段名称是否与配置一致
- 确认表格中已添加数据

### 2. 样式显示问题

- 确保浏览器支持现代 CSS 特性
- 清除浏览器缓存

### 3. 部署后评论功能不工作

- Vercel 文件系统只读，需要迁移到云数据库
- 考虑使用 Supabase 或其他云数据库服务

## 许可证

MIT License

## 联系方式

如有问题或建议，请提交 Issue。
