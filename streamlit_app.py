import streamlit as st
import pandas as pd
import math
from pathlib import Path
import altair as alt

import json
import datetime
import os

# -------------------------- 0. 全局配置 (必须置顶) --------------------------
st.set_page_config(
    page_title='房价趋势透视',
    page_icon='📈',
    layout='wide', 
    initial_sidebar_state="collapsed"
)

# -------------------------- 1. 核心样式 (底部导航 + 居中布局) --------------------------

st.markdown("""
<style>
    /* 1. 彻底隐藏Streamlit默认干扰元素 */
    header, [data-testid="stSidebar"], footer, .stDeployButton, [data-testid="stToolbar"] {
        display: none !important;
    }

    /* 2. 全局容器调整 - 确保底部留白 */
    .stApp {
        background-color: #f8fafc !important;
        font-family: 'Inter', sans-serif !important;
        padding-bottom: 80px !important; /* 关键：给底部导航留出空间 */
        margin: 0 !important;
    }

    /* 3. 底部导航核心样式 - 纯文字现代风 (8个项) */
    .bottom-nav {
        position: fixed !important;
        bottom: 0 !important;
        left: 0 !important;
        width: 100% !important;
        height: 60px !important;
        background-color: rgba(255, 255, 255, 0.90) !important;
        backdrop-filter: blur(16px) !important;
        border-top: 1px solid rgba(226, 232, 240, 0.8) !important;
        display: flex !important;
        align-items: center !important;
        justify-content: space-between !important;
        padding: 0 10px !important;
        box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.03) !important;
        z-index: 9999 !important;
        box-sizing: border-box !important;
    }
    
    /* 4. 导航项样式 */
    .nav-item {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        width: 100% !important;
        height: 40px !important;
        color: #94a3b8 !important;
        text-decoration: none !important;
        font-size: 0.70rem !important; /* 缩小适配8个项 */
        font-weight: 600 !important;
        letter-spacing: -0.01em !important;
        border-radius: 8px !important;
        transition: all 0.2s ease !important;
        margin: 0 2px !important;
        white-space: nowrap !important; /* 禁止换行 */
        overflow: hidden !important; /* 超出隐藏 */
        text-overflow: ellipsis !important; /* 超长显示省略号 */
    }
    
    .nav-item:hover {
        background-color: rgba(241, 245, 249, 0.8) !important;
        color: #64748b !important;
    }
    
    .nav-item.active {
        color: #2563eb !important;
        background-color: rgba(59, 130, 246, 0.1) !important;
    }
    
    .nav-item.active::before {
        display: none !important;
    }
    
    /* 适配手机端 */
    @media (max-width: 640px) {
        .nav-item {
            font-size: 0.65rem !important;
            margin: 0 1px !important;
        }
    }
</style>
""", unsafe_allow_html=True)


# -------------------------- 2. 安全的计数器逻辑 --------------------------
COUNTER_FILE = "visit_stats.json"

def update_daily_visits():
    """安全更新访问量，如果出错则返回 0，绝不让程序崩溃"""
    try:
        today_str = datetime.date.today().isoformat()
        
        # 1. 检查 Session，防止刷新页面重复计数
        if "has_counted" in st.session_state:
            if os.path.exists(COUNTER_FILE):
                try:
                    with open(COUNTER_FILE, "r") as f:
                        return json.load(f).get("count", 0)
                except:
                    return 0
            return 0

        # 2. 读取或初始化数据
        data = {"date": today_str, "count": 0}
        
        if os.path.exists(COUNTER_FILE):
            try:
                with open(COUNTER_FILE, "r") as f:
                    file_data = json.load(f)
                    if file_data.get("date") == today_str:
                        data = file_data
            except:
                pass # 文件损坏则从0开始
        
        # 3. 计数 +1
        data["count"] += 1
        
        # 4. 写入文件
        with open(COUNTER_FILE, "w") as f:
            json.dump(data, f)
        
        st.session_state["has_counted"] = True
        return data["count"]
        
    except Exception as e:
        # 如果发生任何错误，静默失败
        return 0


# -------- 每日访问统计 --------
daily_visits = update_daily_visits()
visit_text = f"今日访问: {daily_visits}"

st.markdown(f"""
<div style="text-align: center; color: #64748b; font-size: 0.7rem; margin-top: 10px; padding-bottom: 20px;">
    {visit_text}
</div>
""", unsafe_allow_html=True)


# -------------------------- 3. 导航数据 (中文) --------------------------
NAV_ITEMS = {
    "nav_1": "财富排行",
    "nav_2": "世界房产",
    "nav_3": "城市房价",
    "nav_4": "全球法律",
    "nav_5": "全球企业",
    "nav_6": "合同审查",
    "nav_7": "德国财税",
    "nav_8": "深圳房市"
}

def render_bottom_nav(nav_data):
    # 此页面应被视为激活状态
    # 假设 '城市房价' 是此页面，设置为 active
    nav_html = f"""
    <div class="bottom-nav">
        <a href="https://youqian.streamlit.app/" class="nav-item" target="_blank">
            {nav_data['nav_1']}
        </a>
        <a href="https://fangchan.streamlit.app/" class="nav-item" target="_blank">
            {nav_data['nav_2']}
        </a>
        <a href="https://fangjia.streamlit.app/" class="nav-item active" target="_self"> 
            {nav_data['nav_3']}
        </a>
        <a href="https://chuhai.streamlit.app/" class="nav-item" target="_blank">
            {nav_data['nav_4']}
        </a>
        <a href="https://chuhai.streamlit.app/" class="nav-item" target="_blank">
            {nav_data['nav_5']}
        </a>
        <a href="https://chuhai.streamlit.app/" class="nav-item" target="_blank">
            {nav_data['nav_6']}
        </a>
        <a href="https://qfschina.streamlit.app/" class="nav-item" target="_blank">
            {nav_data['nav_7']}
        </a>
        <a href="https://fangjia.streamlit.app/" class="nav-item" target="_blank">
            {nav_data['nav_8']}
        </a>
    </div>
    """
    st.markdown(nav_html, unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# Declare some useful functions.

@st.cache_data
def get_gdp_data():
    """Grab GDP data from a CSV file."""

    DATA_FILENAME = Path(__file__).parent/'data/fangchan_data.csv'
    # 假设 'data/fangchan_data.csv' 存在
    try:
        raw_gdp_df = pd.read_csv(DATA_FILENAME, delimiter=';')
    except FileNotFoundError:
        st.error("错误：找不到数据文件 'data/fangchan_data.csv'")
        return pd.DataFrame() # 返回空 DataFrame 避免后续代码崩溃

    MIN_YEAR = 1998
    MAX_YEAR = 2025

    gdp_df = raw_gdp_df.melt(
        ['Country Code'],
        [str(x) for x in range(MIN_YEAR, MAX_YEAR + 1)],
        '时间',
        '房价',
    )
    
    # Convert years from string to integers
    gdp_df['时间'] = pd.to_numeric(gdp_df['时间'])
    gdp_df = gdp_df.rename(columns={'Country Code': '城市'})
    return gdp_df

gdp_df = get_gdp_data()

# -----------------------------------------------------------------------------
# Draw the actual page

# Set the title that appears at the top of the page.
'''
# 📈 房价趋势透视
过去30年核心城市房产价格趋势数据分析
'''

# Add some spacing
''
''

if not gdp_df.empty:
    min_value = gdp_df['时间'].min()
    max_value = gdp_df['时间'].max()
else:
    min_value = 2000
    max_value = 2025

from_year, to_year = st.slider(
    '时间区间',
    min_value=min_value,
    max_value=max_value,
    value=[2005, max_value])

countries = gdp_df['城市'].unique()

if not len(countries):
    st.warning("请选择至少一个城市")
    countries = ['北京', '上海', '深圳', '杭州', '成都', '烟台'] # 使用默认值以防万一

selected_countries = st.multiselect(
    '城市',
    countries,
    ['北京', '上海', '深圳', '杭州', '成都', '烟台'])

''
''
''

# Filter the data
if not gdp_df.empty:
    filtered_gdp_df = gdp_df[
        (gdp_df['城市'].isin(selected_countries))
        & (gdp_df['时间'] <= to_year)
        & (from_year <= gdp_df['时间'])
    ]
else:
    filtered_gdp_df = pd.DataFrame()


st.header('房价走势', divider='gray')

if not filtered_gdp_df.empty:
    # 1. 定义基础图表 (Base Chart)
    base = alt.Chart(filtered_gdp_df).encode(
        x=alt.X('时间', axis=alt.Axis(format='d', title='年份')),
        y=alt.Y('房价', 
                scale=alt.Scale(zero=False), 
                axis=alt.Axis(title='平均房价 (元/㎡)')),
        color='城市'
    )

    # 2. 创建折线层 (Line Layer)
    lines = base.mark_line()

    # 3. 创建圆点层 (Points Layer)
    points = base.mark_circle(size=60).encode(
        opacity=alt.value(1), 
        tooltip=[
            alt.Tooltip('城市', title='城市'),
            alt.Tooltip('时间', title='年份'),
            alt.Tooltip('房价', title='均价(元)', format=',')
        ]
    )

    # 4. 组合并渲染 (Combine and Render)
    chart = (lines + points).interactive() 

    st.altair_chart(chart, use_container_width=True)
    
    # 计算同比增长指标
    first_year = gdp_df[gdp_df['时间'] == from_year]
    last_year = gdp_df[gdp_df['时间'] == to_year]

    st.header(f'{to_year}年房价同比增长', divider='gray')

    ''

    cols = st.columns(4)

    for i, country in enumerate(selected_countries):
        # 确保数据存在
        if country in first_year['城市'].values and country in last_year['城市'].values:
            col = cols[i % len(cols)]

            with col:
                first_gdp = first_year[first_year['城市'] == country]['房价'].iat[0]
                last_gdp = last_year[last_year['城市'] == country]['房价'].iat[0]

                if math.isnan(first_gdp) or first_gdp == 0:
                    growth = 'n/a'
                    delta_color = 'off'
                    value_str = f'{last_gdp:,.0f}'
                else:
                    pct_change = (last_gdp - first_gdp) / first_gdp
                    growth = f'{pct_change:+.2%}'
                    delta_color = 'normal'
                    value_str = f'{last_gdp:,.0f}'
                    
                st.metric(
                    label=f'{country}',
                    value=value_str,
                    delta=growth,
                    delta_color=delta_color
                )
        else:
            # 如果某城市的某年份数据缺失，则跳过
            pass
else:
    st.info("请加载数据文件并选择城市进行分析。")
    
# -------------------------- 最后的调用 --------------------------
render_bottom_nav(NAV_ITEMS)
