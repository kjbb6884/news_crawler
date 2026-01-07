# e:\project\python\py312_learn\news_crawler\main.py
from modules.config import TARGET_URL, STORAGE_FILE
from modules.network import get_rss
from modules.parser import parse_rss
from modules.storage import save_to_excel
from modules.ai_reporter import generate_briefing
from modules.logger import log

def run():
    log.info(f"--- 开始新闻抓取任务 (RSS 版 + AI 简报) ---")
    log.info(f"目标源: {TARGET_URL}")
    
    # 1. 获取 RSS 数据
    feed = get_rss(TARGET_URL)
    if not feed:
        log.error("RSS 抓取失败。")
        return

    # 2. 解析数据
    log.info("正在提取 RSS 项...")
    news_list = parse_rss(feed)

    # 3. 保存数据
    if news_list:
        save_to_excel(news_list, STORAGE_FILE)
        
        # 4. 生成 AI 简报
        generate_briefing(STORAGE_FILE)
    else:
        log.warning("未找到任何有效的新闻。")

    log.info("--- 任务执行完毕 ---")

if __name__ == "__main__":
    run()
