# e:\project\python\py312_learn\news_crawler\modules\network.py
import requests
import time
import random
import feedparser
from .config import UA_POOL, RETRY_COUNT, TIMEOUT, DELAY_RANGE
from .logger import log

def get_rss(url):
    """
    获取并解析 RSS Feed
    """
    delay = random.uniform(*DELAY_RANGE)
    log.info(f"等待 {delay:.2f} 秒以模拟人类行为...")
    time.sleep(delay)

    headers = {
        "User-Agent": random.choice(UA_POOL),
        "Accept": "application/xml,application/rss+xml,text/xml;q=0.9",
        "Referer": "https://36kr.com/"
    }

    for attempt in range(1, RETRY_COUNT + 1):
        try:
            log.info(f"正在请求 RSS: {url} (尝试 {attempt}/{RETRY_COUNT})")
            # 某些 RSS 可能被墙或需要代理，这里默认直连
            response = requests.get(url, headers=headers, timeout=TIMEOUT)
            response.raise_for_status()
            
            # 使用 feedparser 解析内容
            feed = feedparser.parse(response.text)
            
            # 验证 feedparser 解析结果
            if feed.bozo:
                log.warning(f"RSS 解析存在问题: {feed.bozo_exception}")
            
            if not feed.entries:
                log.warning("RSS 返回了空的 entries 列表")
                
            return feed
        except Exception as e:
            log.warning(f"RSS 请求失败: {e}")
            if attempt == RETRY_COUNT:
                return None
            time.sleep(attempt * 3)
    return None

def get_json_api(url, payload):
    return None

def get_html(url):
    return None
