# e:\project\python\py312_learn\news_crawler\modules\parser.py
from .logger import log

def clean_text(text):
    if not text:
        return ""
    return " ".join(text.split())

def parse_rss(feed):
    """
    解析 RSS feed 中的数据
    """
    if not feed:
        log.error("RSS feed 对象为空。")
        return []
    
    if feed.bozo:
        log.warning(f"RSS 解析警告: {getattr(feed, 'bozo_exception', '未知错误')}")
    
    if not feed.entries:
        log.error(f"RSS entries 为空。Feed 版本: {getattr(feed, 'version', '未知')}")
        return []

    news_list = []
    log.info(f"成功从 RSS 获取到 {len(feed.entries)} 条新闻。")

    for entry in feed.entries:
        title = getattr(entry, 'title', '')
        link = getattr(entry, 'link', '')
        
        if title and link:
            news_list.append({
                "title": clean_text(title),
                "url": link
            })
            
    return news_list

def get_parser(url):
    return parse_rss
