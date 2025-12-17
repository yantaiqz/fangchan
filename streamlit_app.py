import streamlit as st
import pandas as pd
import math
from pathlib import Path
import altair as alt

import json
import datetime
import os
import time

# -------------------------- 0. 全局配置 (必须置顶) --------------------------
st.set_page_config(
    page_title='房价趋势透视',
    page_icon='📈',
    layout='wide', 
    initial_sidebar_state="collapsed"
)

# -------------------------- 核心样式 (极致紧凑版) --------------------------
st.markdown("""
<style>
    /* 1. 彻底隐藏Streamlit默认干扰元素 */
    #MainMenu, footer, header[data-testid="stHeader"], [data-testid="stSidebar"], .stDeployButton, [data-testid="stToolbar"] {
        display: none !important;
    }

    /* 2. 全局容器调整 - 极致紧凑 */
    .stApp {
        background-color: #f8fafc !important;
        font-family: 'Inter', sans-serif !important;
        padding-bottom: 60px !important; /* 减少底部留白 */
        margin: 0 !important;
        padding-top: 0.5rem !important; /* 减少顶部留白 */
    }

    /* 3. 底部导航核心样式 - 更紧凑 */
    .bottom-nav {
        position: fixed !important;
        bottom: 0 !important;
        left: 0 !important;
        width: 100% !important;
        height: 50px !important; /* 降低导航栏高度 */
        background-color: rgba(255, 255, 255, 0.90) !important;
        backdrop-filter: blur(16px) !important;
        border-top: 1px solid rgba(226, 232, 240, 0.8) !important;
        display: flex !important;
        align-items: center !important;
        justify-content: space-between !important;
        padding: 0 5px !important; /* 更少内边距 */
        box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.02) !important;
        z-index: 9999 !important;
        box-sizing: border-box !important;
    }
    
    /* 4. 导航项样式 - 极致紧凑 */
    .nav-item {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        width: 100% !important;
        height: 36px !important; /* 降低高度 */
        color: #94a3b8 !important;
        text-decoration: none !important;
        font-size: 0.65rem !important; /* 更小字体 */
        font-weight: 600 !important;
        letter-spacing: -0.02em !important;
        border-radius: 6px !important;
        transition: all 0.2s ease !important;
        margin: 0 1px !important; /* 最小间距 */
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
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
            font-size: 0.60rem !important;
            margin: 0 0.5px !important;
        }
    }

    /* 5. 右上角按钮样式 - 更紧凑 */
    .neal-btn {
        font-family: 'Inter', sans-serif;
        background: #fff;
        border: 1px solid #e5e7eb;
        color: #111;
        font-weight: 600;
        font-size: 12px !important; /* 更小字体 */
        padding: 6px 10px !important; /* 更少内边距 */
        border-radius: 6px !important;
        cursor: pointer;
        transition: all 0.2s;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        white-space: nowrap;
        text-decoration: none !important;
        width: 100%;
        height: 34px !important; /* 更矮高度 */
    }
    .neal-btn:hover {
        background: #f9fafb;
        border-color: #111;
        transform: translateY(-1px);
    }
    .neal-btn-link { 
        text-decoration: none; 
        width: 100%; 
        display: block; 
    }

    /* 6. 标题和内容紧凑化 */
    h1 {
        font-size: 1.6rem !important; /* 更小标题 */
        font-weight: 700 !important;
        margin-bottom: 0.3rem !important; /* 极少间距 */
        line-height: 1.2 !important;
    }
    h2 {
        font-size: 1.2rem !important;
        margin-bottom: 0.5rem !important;
        margin-top: 0.8rem !important;
    }
    p {
        margin-bottom: 0.5rem !important;
        line-height: 1.3 !important;
    }

    /* 7. 控件紧凑化 */
    .stSlider {
        margin-bottom: 0.8rem !important;
    }
    .stMultiselect {
        margin-bottom: 0.8rem !important;
    }
    [data-testid="stMetric"] {
        padding: 0.8rem !important; /* 减少Metric卡片内边距 */
        margin-bottom: 0.5rem !important;
    }
    [data-testid="stMetricLabel"] {
        font-size: 0.9rem !important;
    }
    [data-testid="stMetricValue"] {
        font-size: 1.1rem !important;
    }
    [data-testid="stMetricDelta"] {
        font-size: 0.8rem !important;
    }

    /* 8. 图表容器紧凑化 */
    .stAltairChart {
        margin-bottom: 0.8rem !important;
    }

    /* 9. 列间距紧凑化 */
    [data-testid="stHorizontalBlock"] {
        gap: 0.6rem !important; /* 更小列间距 */
    }

    /* 10. 分割线更紧凑 */
    hr {
        margin-top: 0.8rem !important;
        margin-bottom: 0.8rem !important;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------- 右上角功能区 (更紧凑) --------------------------
col_empty, col_more = st.columns([0.85, 0.15])  # 调整比例更紧凑

with col_more:
    st.markdown(
        f"""
        <a href="https://haowan.streamlit.app/" target="_blank" class="neal-btn-link">
            <button class="neal-btn">✨ 更多好玩应用</button>
        </a>
        """, 
        unsafe_allow_html=True
    )

# -------------------------- 导航数据 (中文) --------------------------
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
    nav_html = f"""
    <div class="bottom-nav">
        <a href="https://youqian.streamlit.app/" class="nav-item" target="_blank">
            {nav_data['nav_1']}
        </a>
        <a href="https://fangchan.streamlit.app/" class="nav-item active" target="_blank">
            {nav_data['nav_2']}
        </a>
        <a href="https://fangjia.streamlit.app/" class="nav-item" target="_blank"> 
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
# 数据加载函数
@st.cache_data
def get_gdp_data():
    """Grab GDP data from a CSV file."""
    DATA_FILENAME = Path(__file__).parent/'data/fangchan_data.csv'
    
    try:
        raw_gdp_df = pd.read_csv(DATA_FILENAME, delimiter=';')
    except FileNotFoundError:
        st.error("错误：找不到数据文件 'data/fangchan_data.csv'")
        return pd.DataFrame()

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
# 页面内容 (极致紧凑版)
# 标题区域 - 更紧凑
st.markdown("""
# 📈 房价趋势透视
<span style="font-size:0.9rem; color:#64748b;">过去30年核心城市房产价格趋势数据分析</span>
""", unsafe_allow_html=True)

# 极少的间距
st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

# 时间滑块
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
    value=[2005, max_value],
    help="选择要分析的年份范围"
)

# 城市选择
countries = gdp_df['城市'].unique() if not gdp_df.empty else []

if not len(countries):
    st.warning("请选择至少一个城市")
    countries = ['北京', '上海', '深圳', '杭州', '成都', '烟台']

selected_countries = st.multiselect(
    '城市',
    countries,
    ['北京', '上海', '深圳', '杭州', '成都', '烟台'],
    help="选择要分析的城市"
)

# 极小间距
st.markdown("<div style='height:5px'></div>", unsafe_allow_html=True)

# 过滤数据
if not gdp_df.empty:
    filtered_gdp_df = gdp_df[
        (gdp_df['城市'].isin(selected_countries))
        & (gdp_df['时间'] <= to_year)
        & (from_year <= gdp_df['时间'])
    ]
else:
    filtered_gdp_df = pd.DataFrame()

# 房价走势图表
st.header('房价走势', divider='gray')

if not filtered_gdp_df.empty:
    # 1. 定义基础图表 (更紧凑的尺寸)
    base = alt.Chart(filtered_gdp_df).encode(
        x=alt.X('时间', axis=alt.Axis(format='d', title='年份', labelFontSize=10, titleFontSize=11)),
        y=alt.Y('房价', 
                scale=alt.Scale(zero=False), 
                axis=alt.Axis(title='平均房价 (元/㎡)', labelFontSize=10, titleFontSize=11)),
        color='城市'
    )

    # 2. 创建折线层
    lines = base.mark_line()

    # 3. 创建圆点层 (更小的点)
    points = base.mark_circle(size=40).encode(  # 更小的圆点
        opacity=alt.value(1), 
        tooltip=[
            alt.Tooltip('城市', title='城市'),
            alt.Tooltip('时间', title='年份'),
            alt.Tooltip('房价', title='均价(元)', format=',')
        ]
    )

    # 4. 组合并渲染 (更紧凑的图表)
    chart = (lines + points).interactive().properties(height=300)  # 更矮的图表
    st.altair_chart(chart, use_container_width=True)
    
    # 同比增长指标 (更紧凑的布局)
    st.header(f'{to_year}年房价同比增长', divider='gray')
    st.markdown("<div style='height:5px'></div>", unsafe_allow_html=True)

    # 使用6列布局更紧凑
    cols = st.columns(min(6, len(selected_countries)))

    for i, country in enumerate(selected_countries):
        if country in gdp_df['城市'].values:
            first_year_data = gdp_df[(gdp_df['城市'] == country) & (gdp_df['时间'] == from_year)]
            last_year_data = gdp_df[(gdp_df['城市'] == country) & (gdp_df['时间'] == to_year)]
            
            if not first_year_data.empty and not last_year_data.empty:
                with cols[i % len(cols)]:
                    first_gdp = first_year_data['房价'].iat[0]
                    last_gdp = last_year_data['房价'].iat[0]

                    if math.isnan(first_gdp) or first_gdp == 0:
                        growth = 'n/a'
                        delta_color = 'off'
                        value_str = f'{last_gdp:,.0f}' if not math.isnan(last_gdp) else 'n/a'
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
    st.info("请加载数据文件并选择城市进行分析。")

# -------------------------- 渲染底部导航 --------------------------
render_bottom_nav(NAV_ITEMS)
