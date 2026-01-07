# e:\project\python\py312_learn\news_crawler\modules\storage.py
import pandas as pd
import datetime
import os
from .logger import log

def save_to_excel(data, filename):
    """
    将提取的数据保存到 Excel 文件中
    """
    if not data:
        log.warning("没有可保存的数据。")
        return

    # 添加爬取时间
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for row in data:
        row['crawl_time'] = current_time

    df_new = pd.DataFrame(data)

    try:
        if os.path.exists(filename):
            # 如果文件存在，读取旧数据并追加
            # 注意：这里假设旧数据结构兼容
             with pd.ExcelWriter(filename, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
                 # 简单处理：追加模式比较复杂，为了简化，我们读取旧文件，合并，然后重写
                 # 这里为了稳健，先读取旧文件
                 df_old = pd.read_excel(filename)
                 df_combined = pd.concat([df_old, df_new], ignore_index=True)
                 df_combined.to_excel(filename, index=False)
        else:
            # 新文件直接写入
            df_new.to_excel(filename, index=False)
        
        log.info(f"成功保存 {len(data)} 条数据至 {filename}")
    except Exception as e:
        log.error(f"保存数据时出错: {e}")
