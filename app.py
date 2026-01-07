# e:\project\python\pythonpachong\news_crawler\app.py
import streamlit as st
import pandas as pd
import os

# Import modules
from modules.config import TARGET_URL, STORAGE_FILE
from modules.network import get_rss
from modules.parser import parse_rss
from modules.storage import save_to_excel
from modules.ai_reporter import fetch_ai_briefing

# --- Page Config ---
st.set_page_config(
    page_title="SSPai News Crawler",
    page_icon="📰",
    layout="centered"
)

# --- Title ---
st.title("📰 RSS 爬虫 & AI 关键词提取")

# --- Target URL Input ---
target_url_input = st.text_input(
    "目标 RSS 地址 (Target URL)",
    value=TARGET_URL,
    help="输入需要抓取的 RSS 订阅源地址"
)

# --- API Key & Base URL Configuration ---
# Always show sidebar for configuration
with st.sidebar:
    st.header("⚙️ 配置")
    
    # API Key Input
    api_key_input = st.text_input(
        "OpenAI API Key",
        type="password",
        help="请输入您的 OpenAI API Key",
        key="api_key_input"
    )
    
    # Base URL Input
    from modules.config import AI_CONFIG
    default_base_url = AI_CONFIG.get("base_url", "https://api.openai.com/v1")
    base_url_input = st.text_input(
        "OpenAI 代理地址 (Base URL)",
        value=default_base_url,
        help="如需使用代理服务器，请修改此地址"
    )
    
    # Model Name Input
    default_model = AI_CONFIG.get("model", "gpt-3.5-turbo")
    model_input = st.text_input(
        "OpenAI 模型名称 (Model)",
        value=default_model,
        help="如 gpt-3.5-turbo、gpt-4 等"
    )
    
    st.divider()
    st.caption("💡 提示：API Key 支持从环境变量 `OPENAI_API_KEY` 读取")

# Determine final API Key (Priority: secrets > env > input)
api_key = None
try:
    api_key = st.secrets.get("OPENAI_API_KEY")
except Exception:
    pass

if not api_key:
    api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    api_key = api_key_input

if not api_key:
    st.sidebar.warning("⚠️ 请输入 API Key 以启用 AI 简报功能")

# Determine final Base URL
base_url = base_url_input if base_url_input else default_base_url

# Determine final Model
model = model_input if model_input else default_model

# --- Session State Initialization ---
if "news_data" not in st.session_state:
    st.session_state.news_data = None
if "ai_briefing" not in st.session_state:
    st.session_state.ai_briefing = None
if "crawl_completed" not in st.session_state:
    st.session_state.crawl_completed = False

# --- Main UI ---
col1, col2 = st.columns([3, 1])

with col1:
    start_button = st.button("🚀 开始抓取", type="primary", use_container_width=True)

with col2:
    if st.button("🔄 重置", use_container_width=True):
        st.session_state.news_data = None
        st.session_state.ai_briefing = None
        st.session_state.crawl_completed = False
        st.rerun()

# --- Crawling Logic ---
if start_button and not st.session_state.crawl_completed:
    if not api_key:
        st.error("❌ 请先在侧边栏输入 API Key！")
    else:
        with st.status("🔄 正在处理...", expanded=True) as status:
            try:
                # Step 1: Fetch RSS
                status.write("📡 正在获取 RSS 数据...")
                feed = get_rss(target_url_input)
                if not feed:
                    raise Exception("RSS 抓取失败，请检查网络连接")
                status.write("✅ RSS 数据获取成功")

                # Step 2: Parse Data
                status.write("📝 正在解析数据...")
                news_list = parse_rss(feed)
                if not news_list:
                    raise Exception("未找到任何有效的新闻条目")
                st.session_state.news_data = news_list
                status.write(f"✅ 成功解析 {len(news_list)} 条新闻")

                # Step 3: Archive to Excel (Side effect, non-blocking)
                status.write("💾 正在存档到 Excel...")
                try:
                    save_to_excel(news_list, STORAGE_FILE)
                    status.write(f"✅ 已存档至 {STORAGE_FILE}")
                except Exception as e:
                    status.write(f"⚠️ 存档失败（非致命错误）: {e}")

                # Step 4: Generate AI Keywords
                status.write("🤖 正在提取 AI 关键词...")
                titles = [item["title"] for item in news_list]
                briefing = fetch_ai_briefing(titles, api_key=api_key, base_url=base_url, model=model)
                if not briefing:
                    raise Exception("AI 关键词提取失败，请检查 API Key 和网络连接")
                st.session_state.ai_briefing = briefing
                status.write("✅ AI 关键词提取成功")

                # Mark as completed
                st.session_state.crawl_completed = True
                status.update(label="✅ 处理完成！", state="complete", expanded=False)

            except Exception as e:
                status.update(label="❌ 处理失败", state="error", expanded=True)
                st.error(f"错误详情: {e}")

# --- Display Results ---
if st.session_state.ai_briefing:
    st.divider()
    st.subheader("🔑 AI 关键词")
    st.markdown(st.session_state.ai_briefing)

if st.session_state.news_data:
    st.divider()
    with st.expander("📊 查看原始数据", expanded=False):
        df = pd.DataFrame(st.session_state.news_data)
        st.dataframe(df, use_container_width=True)
        st.caption(f"共 {len(df)} 条新闻")
