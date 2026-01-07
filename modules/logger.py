# e:\project\python\py312_learn\news_crawler\modules\logger.py
import logging
import os

def setup_logger(name="crawler", log_file="crawler.log"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # 格式化
    formatter = logging.Formatter('%(asctime)s - [%(levelname)s] - %(message)s')

    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # 文件处理器
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

# 全局初始化
log = setup_logger()
