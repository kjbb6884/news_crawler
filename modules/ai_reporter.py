import pandas as pd
import openai
import os
import datetime
from .config import AI_CONFIG
from .logger import log


def read_titles(excel_path):
    """
    读取 Excel 文件，提取标题列表。
    (Input Side Effect - for CLI compatibility)
    """
    if not os.path.exists(excel_path):
        log.error(f"Excel 文件未找到: {excel_path}")
        return []

    try:
        df = pd.read_excel(excel_path)
        if 'title' not in df.columns:
            log.error("Excel 文件缺少 'title' 列")
            return []
        
        titles = df['title'].tolist()
        log.info(f"从 Excel 读取到 {len(titles)} 个标题。")
        return titles
    except Exception as e:
        log.error(f"读取 Excel 文件失败: {e}")
        return []


def fetch_ai_briefing(titles, api_key=None, base_url=None, model=None):
    """
    调用 AI API 生成简报内容。
    (Calculation/API Call - Pure function, no file I/O)
    
    Args:
        titles: 标题列表
        api_key: 可选的 API Key，如果不传则从 config 或环境变量获取
        base_url: 可选的 OpenAI Base URL（代理地址），如果不传则从 config 获取
        model: 可选的模型名称（如 gpt-3.5-turbo），如果不传则从 config 获取
    
    Returns:
        str: AI 生成的简报内容，失败返回空字符串
    """
    if not titles:
        log.warning("标题列表为空，跳过 AI 简报生成。")
        return ""

    # 获取 API Key
    if not api_key:
        api_key = AI_CONFIG.get("api_key")
        if api_key == "YOUR_API_KEY_HERE" or not api_key:
            api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        log.error("未找到 API Key，无法生成简报。请设置 OPENAI_API_KEY 环境变量。")
        return ""

    # 获取 Base URL
    if not base_url:
        base_url = AI_CONFIG.get("base_url")

    # 获取 Model
    if not model:
        model = AI_CONFIG.get("model")

    titles_text = "\n".join(titles)
    log.info(f"准备调用 AI，共 {len(titles)} 个标题，模型: {model}...")

    client = openai.OpenAI(
        api_key=api_key,
        base_url=base_url
    )

    prompt = AI_CONFIG["prompt_template"].format(titles=titles_text)

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "你是一个专业的科技新闻分析师，擅长总结和扩写新闻简报。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        
        briefing_content = response.choices[0].message.content
        log.info("AI 简报生成成功。")
        return briefing_content

    except Exception as e:
        log.error(f"AI 生成简报失败: {e}")
        return ""


def save_briefing(content, output_dir="."):
    """
    将简报内容保存为 TXT 文件。
    (Output Side Effect)
    
    Args:
        content: 简报内容
        output_dir: 输出目录
    
    Returns:
        str: 保存的文件名，失败返回空字符串
    """
    if not content:
        log.warning("简报内容为空，跳过保存。")
        return ""

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = os.path.join(output_dir, f"briefing_{timestamp}.txt")
    
    try:
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(content)
        log.info(f"AI 简报已保存至: {output_filename}")
        return output_filename
    except Exception as e:
        log.error(f"保存简报失败: {e}")
        return ""


def generate_briefing(excel_path):
    """
    读取 Excel 文件，提取标题，使用 AI 生成简报并保存为 txt。
    (Composed function for CLI backward compatibility)
    """
    log.info("开始生成 AI 简报...")
    
    # 1. 读取标题
    titles = read_titles(excel_path)
    if not titles:
        return
    
    # 2. 生成简报
    content = fetch_ai_briefing(titles)
    if not content:
        return
    
    # 3. 保存简报
    output_dir = os.path.dirname(excel_path) if os.path.dirname(excel_path) else "."
    save_briefing(content, output_dir)

