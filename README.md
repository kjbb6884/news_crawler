# 📰 RSS 爬虫 & AI 关键词提取

一个基于 Streamlit 的 RSS 新闻爬虫，支持从任意 RSS 源抓取新闻并使用 AI 提取关键词。

## ✨ 功能特点

- 🔗 **可配置 RSS 源**：支持自定义目标 RSS 地址
- 🤖 **AI 关键词提取**：使用 OpenAI API 从新闻标题中提取热点关键词
- ⚙️ **灵活配置**：支持自定义 API Key、Base URL、模型名称
- 💾 **数据存档**：自动保存抓取数据到 Excel
- 🔄 **状态管理**：防止重复抓取，支持一键重置

## 🚀 本地运行

### 1. 克隆仓库
```bash
git clone https://github.com/YOUR_USERNAME/news_crawler.git
cd news_crawler
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 运行应用
```bash
streamlit run app.py
```

### 4. 配置 API Key
在侧边栏输入你的 OpenAI API Key，或设置环境变量：
```bash
export OPENAI_API_KEY="your-api-key-here"
```

---

## ☁️ Streamlit Cloud 部署指南

### 步骤 1: 推送到 GitHub
1. 在 GitHub 创建一个新仓库（如 `news_crawler`）
2. 执行以下命令：
```bash
git remote add origin https://github.com/YOUR_USERNAME/news_crawler.git
git branch -M main
git push -u origin main
```

### 步骤 2: 连接 Streamlit Cloud
1. 访问 [share.streamlit.io](https://share.streamlit.io)
2. 点击 **New app**
3. 选择你的 GitHub 仓库
4. **Main file path**: `app.py`

### 步骤 3: 配置 Secrets (重要!)
1. 在 **Advanced settings** 中添加：
```toml
OPENAI_API_KEY = "your-api-key-here"
```
2. 点击 **Deploy**

> ⚠️ **注意**：不要把 API Key 硬编码在代码中！请使用 Streamlit Secrets 管理。

---

## 📁 项目结构
```
news_crawler/
├── app.py              # Streamlit 主应用
├── requirements.txt    # Python 依赖
├── modules/
│   ├── config.py       # 配置文件
│   ├── network.py      # 网络请求
│   ├── parser.py       # RSS 解析
│   ├── storage.py      # Excel 存储
│   └── ai_reporter.py  # AI 关键词生成
└── README.md
```

## 📝 License
MIT License
