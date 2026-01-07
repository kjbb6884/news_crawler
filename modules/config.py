# e:\project\python\py312_learn\news_crawler\modules\config.py

# 目标设置
TARGET_URL = "https://sspai.com/feed"
STORAGE_FILE = "sspai_headlines.xlsx"

# AI 设置
AI_CONFIG = {
    "api_key": "sk-qivLs2BakFZmuOnaRqFK4QYgb3Y2yL0MnEuRTCd273v3xzSY",  # 建议从环境变量获取 os.getenv("OPENAI_API_KEY")
    "base_url": "https://api.chatanywhere.tech/v1",
    "model": "gpt-5.2-2025-12-11",
    "prompt_template": "请提取以下新闻标题中的关键信息，并总结为10个左右的关键词或短语，用逗号分隔：\n\n{titles}"
}

# 网络请求设置
RETRY_COUNT = 3
TIMEOUT = 10
DELAY_RANGE = (1.5, 3.5)

# User-Agent 轮询池
UA_POOL = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.46"
]

# 解析选择器 (通用)
SELECTORS = {
    "article_link": "a.article-item-title"  # 保留备用
}
