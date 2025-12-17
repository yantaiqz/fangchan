import streamlit as st
import pandas as pd
import math
from pathlib import Path
import altair as alt
import datetime

# -------------------------- 0. 全局配置 --------------------------
st.set_page_config(
    page_title='房价趋势透视',
    page_icon='📈',
    layout='wide', 
    initial_sidebar_state="collapsed"
)

# -------------------------- 核心样式 (极致紧凑版+) --------------------------
st.markdown("""
<style>
    /* 1. 基础隐藏 */
    #MainMenu, footer, header[data-testid="stHeader"], [data-testid="stSidebar"] {display: none !important;}

    /* 2. 全局容器 - 消除顶部留白 */
    .stApp {
        background-color: #f8fafc !important;
        font-family: 'Inter', sans-serif !important;
    }
    .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 4rem !important; /* 留出底部导航空间 */
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: 100% !important;
    }

    /* 3. 关键：强制压缩组件垂直间距 */
    [data-testid="stVerticalBlock"] {
        gap: 0.3rem !important; /* 默认是1rem，这里改得很小 */
    }
    
    /* 4. 标题紧凑化 */
    h1 {
        font-size: 1.4rem !important;
        margin-bottom: 0 !important;
        padding-bottom: 0 !important;
    }
    h3 {
        font-size: 1rem !important;
        margin-top: 0.5rem !important;
        margin-bottom: 0.2rem !important;
        padding: 0 !important;
    }
    
    /* 5. 控件紧凑化 */
    .stSlider { padding-top: 0px !important; margin-top: -10px !important;}
    .stMultiselect { padding-top: 0px !important; }
    
    /* 6. Metric 指标卡片紧凑化 */
    [data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        padding: 8px 10px !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    [data-testid="stMetricLabel"] { font-size: 0.75rem !important; color: #64748b; }
    [data-testid="stMetricValue"] { font-size: 1.1rem !important; color: #0f172a; }
    [data-testid="stMetricDelta"] { font-size: 0.75rem !important; margin-top: -2px; }

    /* 7. 底部导航 (保持你的样式) */
    .bottom-nav {
        position: fixed; bottom: 0; left: 0; width: 100%; height: 48px;
        background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(10px);
        border-top: 1px solid #e2e8f0; display: flex; justify-content: space-around;
        padding: 0 5px; z-index: 9999;
    }
    .nav-item {
        flex: 1; display: flex; align-items: center; justify-content: center;
        font-size: 0.7rem; color: #64748b; text-decoration: none; height: 100%;
        font-weight: 500;
    }
    .nav-item.active { color: #2563eb; background: rgba(37, 99, 235, 0.05); }

    /* 8. 右上角按钮 */
    .neal-btn {
        background: white; border: 1px solid #e2e8f0; border-radius: 6px;
        padding: 4px 8px; font-size: 0.75rem; color: #334155; cursor: pointer;
        width: 100%; font-weight: 600;
    }
    .neal-btn:hover { border-color: #3b82f6; color: #3b82f6; }
</style>
""", unsafe_allow_html=True)

# -------------------------- 数据加载 --------------------------
@st.cache_data
def get_gdp_data():
    DATA_FILENAME = Path(__file__).parent/'data/fangchan_data.csv'
    try:
        raw_gdp_df = pd.read_csv(DATA_FILENAME, delimiter=';')
    except FileNotFoundError:
        # 如果找不到文件，生成一些模拟数据以供展示布局效果
        data = {
            'Country Code': ['北京', '上海', '深圳', '杭州', '成都', '烟台'] * 26,
            '时间': sorted([year for year in range(2000, 2026)] * 6),
            '房价': [x * 100 + (x**1.5) for x in range(2000, 2026)] * 6 # 假数据
        }
        return pd.DataFrame(data)

    MIN_YEAR = 1998
    MAX_YEAR = 2025
    gdp_df = raw_gdp_df.melt(['Country Code'], [str(x) for x in range(MIN_YEAR, MAX_YEAR + 1)], '时间', '房价')
    gdp_df['时间'] = pd.to_numeric(gdp_df['时间'])
    gdp_df = gdp_df.rename(columns={'Country Code': '城市'})
    return gdp_df

gdp_df = get_gdp_data()

# -------------------------- 顶部布局：标题与按钮 --------------------------
col_h1, col_h2 = st.columns([0.85, 0.15])
with col_h1:
    st.markdown("<h1>📈 房价趋势透视 <span style='font-size:0.8rem;color:#64748b;font-weight:400;margin-left:10px'>核心城市30年数据</span></h1>", unsafe_allow_html=True)
with col_h2:
    st.markdown("""<a href="#" target="_self" style="text-decoration:none;"><button class="neal-btn">✨ 更多应用</button></a>""", unsafe_allow_html=True)

# -------------------------- 控制区：并排布局 (节省纵向空间) --------------------------
if not gdp_df.empty:
    min_value, max_value = gdp_df['时间'].min(), gdp_df['时间'].max()
else:
    min_value, max_value = 2000, 2025

# 使用列布局将控件并排
c1, c2 = st.columns([1, 1.5])
with c1:
    from_year, to_year = st.slider('📅 时间区间', min_value=min_value, max_value=max_value, value=[2010, max_value])
with c2:
    countries = gdp_df['城市'].unique() if not gdp_df.empty else ['北京', '上海']
    selected_countries = st.multiselect('🏙️ 选择城市', countries, default=['北京', '上海', '深圳'][:3], label_visibility="visible")

# 数据过滤
if not gdp_df.empty:
    filtered_gdp_df = gdp_df[(gdp_df['城市'].isin(selected_countries)) & (gdp_df['时间'] <= to_year) & (from_year <= gdp_df['时间'])]
else:
    filtered_gdp_df = pd.DataFrame()

# -------------------------- 图表区域 --------------------------
if not filtered_gdp_df.empty:
    # 1. 紧凑型折线图
    base = alt.Chart(filtered_gdp_df).encode(
        x=alt.X('时间', axis=alt.Axis(format='d', title=None, labelFontSize=10, tickCount=10)), # 移除X轴标题节省空间
        y=alt.Y('房价', scale=alt.Scale(zero=False), axis=alt.Axis(title=None, labelFontSize=10, format='~s')), # 移除Y轴标题
        color=alt.Color('城市', legend=alt.Legend(orient='top', title=None, symbolLimit=0)) # 图例放顶部
    )
    
    chart = (base.mark_line(strokeWidth=2) + base.mark_circle(size=30)).interactive().properties(
        height=260 # 进一步压缩高度
    ).configure_view(strokeWidth=0).configure_axis(gridColor='#f1f5f9')
    
    st.altair_chart(chart, use_container_width=True)

    # -------------------------- 指标区域 --------------------------
    st.markdown(f"### {to_year}年 同比增长概览")
    
    cols = st.columns(len(selected_countries)) if len(selected_countries) > 0 else st.columns(1)
    
    for i, country in enumerate(selected_countries):
        if country in gdp_df['城市'].values:
            first_data = gdp_df[(gdp_df['城市'] == country) & (gdp_df['时间'] == from_year)]
            last_data = gdp_df[(gdp_df['城市'] == country) & (gdp_df['时间'] == to_year)]
            
            if not first_data.empty and not last_data.empty:
                val_start = first_data['房价'].iat[0]
                val_end = last_data['房价'].iat[0]
                
                pct = (val_end - val_start) / val_start if val_start != 0 else 0
                
                with cols[i]:
                    st.metric(
                        label=country,
                        value=f"{val_end:,.0f}",
                        delta=f"{pct:+.1%}"
                    )
else:
    st.info("暂无数据")

# -------------------------- 底部导航 --------------------------
NAV_ITEMS = {
    "nav_1": "财富排行", "nav_2": "世界房产", "nav_3": "城市房价", "nav_4": "全球法律",
    "nav_5": "全球企业", "nav_6": "合同审查", "nav_7": "德国财税", "nav_8": "深圳房市"
}

nav_html = f"""
<div class="bottom-nav">
    {''.join([f'<a href="#" class="nav-item {"active" if k=="nav_3" else ""}">{v}</a>' for k,v in NAV_ITEMS.items()])}
</div>
"""
st.markdown(nav_html, unsafe_allow_html=True)
