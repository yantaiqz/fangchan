import streamlit as st
import pandas as pd
import math
from pathlib import Path
import altair as alt

# -------------------------- 全局配置 --------------------------
st.set_page_config(
    page_title='房价趋势透视',
    page_icon='📈',
    layout='wide', 
    initial_sidebar_state="collapsed"
)

# -------------------------- 核心样式 (极致压缩顶部空白) --------------------------
st.markdown("""
<style>
    /* 隐藏默认元素 */
    #MainMenu, footer, header, [data-testid="stSidebar"], .stDeployButton {display: none !important;}
    
    /* 全局样式 - 完全消除顶部空白 */
    .stApp {
        background: #f8fafc !important;
        font-family: 'Inter', sans-serif !important;
        padding: 0.1rem 1rem 60px !important;  /* 顶部仅0.1rem内边距 */
        margin: 0 !important;
    }
    
    /* 消除block容器的默认顶部空白 */
    .block-container {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
        max-width: 100% !important;
    }

    /* 底部导航 */
    .bottom-nav {
        position: fixed !important;
        bottom: 0 !important;
        left: 0 !important;
        width: 100% !important;
        height: 50px !important;
        background: rgba(255,255,255,0.9) !important;
        backdrop-filter: blur(16px) !important;
        border-top: 1px solid #e2e8f0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: space-around !important;
        padding: 0 5px !important;
        z-index: 9999 !important;
    }
    
    .nav-item {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        width: 100% !important;
        height: 36px !important;
        color: #94a3b8 !important;
        text-decoration: none !important;
        font-size: 0.65rem !important;
        font-weight: 600 !important;
        border-radius: 6px !important;
        margin: 0 1px !important;
    }
    
    .nav-item.active {
        color: #2563eb !important;
        background: rgba(59,130,246,0.1) !important;
    }

    /* 控件极致紧凑化 */
    h1 {
        font-size: 1.5rem !important; 
        margin: 0.2rem 0 0.3rem !important;  /* 标题上下间距极小 */
        line-height: 1.1 !important;
    }
    h2 {
        font-size: 1.1rem !important; 
        margin: 0.5rem 0 0.3rem !important;
    }
    .stSlider, .stMultiselect {
        margin-bottom: 0.5rem !important;
        margin-top: 0 !important;
    }
    [data-testid="stMetric"] {
        padding: 0.6rem !important; 
        margin-bottom: 0.3rem !important;
    }
    [data-testid="stHorizontalBlock"] {
        gap: 0.4rem !important;
        margin-top: 0 !important;
    }
    hr {
        margin: 0.5rem 0 !important;
    }
    
    /* 右上角按钮 - 紧贴顶部 */
    .neal-btn {
        background: #fff !important;
        border: 1px solid #e5e7eb !important;
        color: #111 !important;
        font-size: 12px !important;
        padding: 4px 8px !important;
        border-radius: 6px !important;
        height: 30px !important;
        width: 100% !important;
        cursor: pointer !important;
        text-decoration: none !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        margin-top: 0.2rem !important;
    }
    
    /* 消除图表容器空白 */
    .stAltairChart {
        margin-bottom: 0.5rem !important;
        margin-top: 0 !important;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------- 右上角按钮 (紧贴右上角) --------------------------
col_empty, col_more = st.columns([0.88, 0.12])  # 调整比例，按钮更窄
with col_more:
    st.markdown('<a href="https://haowan.streamlit.app/" target="_blank" class="neal-btn">✨ 更多应用</a>', unsafe_allow_html=True)

# -------------------------- 底部导航 --------------------------
def render_nav():
    nav_html = """
    <div class="bottom-nav">
        <a href="https://youqian.streamlit.app/" class="nav-item">财富排行</a>
        <a href="https://fangchan.streamlit.app/" class="nav-item active">世界房产</a>
        <a href="https://fangjia.streamlit.app/" class="nav-item">城市房价</a>
        <a href="https://chuhai.streamlit.app/" class="nav-item">全球法律</a>
        <a href="https://chuhai.streamlit.app/" class="nav-item">全球企业</a>
        <a href="https://chuhai.streamlit.app/" class="nav-item">合同审查</a>
        <a href="https://qfschina.streamlit.app/" class="nav-item">德国财税</a>
        <a href="https://fangjia.streamlit.app/" class="nav-item">深圳房市</a>
    </div>
    """
    st.markdown(nav_html, unsafe_allow_html=True)

# -------------------------- 数据加载 --------------------------
@st.cache_data
def load_data():
    try:
        df = pd.read_csv(Path(__file__).parent/'data/fangchan_data.csv', delimiter=';')
        df = df.melt(['Country Code'], [str(x) for x in range(1998, 2026)], '时间', '房价')
        df['时间'] = pd.to_numeric(df['时间'])
        return df.rename(columns={'Country Code': '城市'})
    except:
        st.error("数据文件缺失: data/fangchan_data.csv")
        return pd.DataFrame()

df = load_data()

# -------------------------- 页面内容 (无多余空白) --------------------------
# 标题 - 几乎无上下空白
st.markdown("# 📈 房价趋势透视\n<span style='font-size:0.85rem;color:#64748b'>过去30年核心城市房价分析</span>", unsafe_allow_html=True)

# 时间筛选 - 紧贴标题
min_year, max_year = (df['时间'].min(), df['时间'].max()) if not df.empty else (2000, 2025)
from_year, to_year = st.slider('时间区间', min_year, max_year, [2005, max_year], key='time_slider')

# 城市选择 - 紧贴滑块
cities = df['城市'].unique() if not df.empty else ['北京', '上海', '深圳', '杭州', '成都', '烟台']
selected_cities = st.multiselect('城市', cities, ['北京', '上海', '深圳', '杭州', '成都', '烟台'], key='city_select')

# 数据过滤和展示
if not df.empty:
    filtered_df = df[(df['城市'].isin(selected_cities)) & (df['时间'] >= from_year) & (df['时间'] <= to_year)]
    
    # 房价走势图表 - 紧贴选择框
    st.header('房价走势', divider='gray')
    if not filtered_df.empty:
        chart = alt.Chart(filtered_df).encode(
            x=alt.X('时间:O', title='年份', axis=alt.Axis(labelFontSize=9, titleFontSize=10)),
            y=alt.Y('房价', scale=alt.Scale(zero=False), title='均价(元/㎡)', axis=alt.Axis(labelFontSize=9, titleFontSize=10)),
            color='城市'
        )
        chart = (chart.mark_line() + chart.mark_circle(size=30).encode(
            tooltip=['城市', '时间', alt.Tooltip('房价', format=',')]
        )).interactive().properties(height=280)
        st.altair_chart(chart, use_container_width=True)
        
        # 同比增长 - 紧贴图表
        st.header(f'{to_year}年房价同比增长', divider='gray')
        cols = st.columns(min(6, len(selected_cities)))
        for i, city in enumerate(selected_cities):
            with cols[i % len(cols)]:
                first_vals = df[(df['城市']==city) & (df['时间']==from_year)]['房价'].values
                last_vals = df[(df['城市']==city) & (df['时间']==to_year)]['房价'].values
                if len(first_vals) and len(last_vals) and first_vals[0] > 0:
                    growth = f'{(last_vals[0]-first_vals[0])/first_vals[0]:+.2%}'
                    st.metric(city, f'{last_vals[0]:,.0f}', growth)

# 底部导航
render_nav()
