import streamlit as st
import pandas as pd
import math
from pathlib import Path
import altair as alt

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
    /* 1. 彻底隐藏干扰元素 */
    #MainMenu, footer, header[data-testid="stHeader"], [data-testid="stSidebar"] { display: none !important; }

    /* 2. 全局容器 - 压缩顶部与底部留白 */
    .stApp {
        background-color: #f8fafc !important;
        padding-bottom: 50px !important;
    }
    .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 2rem !important;
        max-width: 98% !important;
    }

    /* 3. 核心：强制压缩所有组件之间的垂直间距 */
    [data-testid="stVerticalBlock"] {
        gap: 0.3rem !important;
    }

    /* 4. 标题与描述紧凑化 */
    h1 { font-size: 1.4rem !important; margin-bottom: 0px !important; }
    h2 { font-size: 1.1rem !important; margin-top: 0.5rem !important; margin-bottom: 0.2rem !important; }
    .stMarkdown p { margin-bottom: 0px !important; font-size: 0.85rem !important; }

    /* 5. 控件区紧凑化：滑块与多选并排时减小间距 */
    .stSlider { padding-top: 0px !important; }
    div[data-testid="stExpander"] { margin-bottom: 0px !important; }

    /* 6. 指标卡片 (Metric) 样式微调 */
    [data-testid="stMetric"] {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 4px;
        padding: 6px 10px !important;
    }

    /* 7. 底部导航栏 (更矮更精致) */
    .bottom-nav {
        position: fixed; bottom: 0; left: 0; width: 100%; height: 42px;
        background: rgba(255, 255, 255, 0.98); backdrop-filter: blur(10px);
        border-top: 1px solid #e2e8f0; display: flex; align-items: center;
        justify-content: space-around; z-index: 9999;
    }
    .nav-item {
        color: #64748b; text-decoration: none; font-size: 0.7rem; font-weight: 500;
        padding: 5px 10px; border-radius: 4px;
    }
    .nav-item.active { color: #2563eb; background: #eff6ff; }

    /* 8. 右上角按钮 */
    .neal-btn {
        background: white; border: 1px solid #e2e8f0; border-radius: 4px;
        font-size: 0.75rem; padding: 4px 8px; cursor: pointer; height: 30px;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------- 右上角功能区 --------------------------
c_t1, c_t2 = st.columns([0.85, 0.15])
with c_t1:
    st.markdown("<h1>📈 房价趋势透视 <span style='font-size:0.8rem; font-weight:400; color:#64748b; margin-left:10px;'>核心城市30年价格分析</span></h1>", unsafe_allow_html=True)
with c_t2:
    st.markdown('<a href="https://haowan.streamlit.app/" target="_blank"><button class="neal-btn">✨ 更多应用</button></a>', unsafe_allow_html=True)

# -------------------------- 数据处理 --------------------------
@st.cache_data
def get_gdp_data():
    DATA_FILENAME = Path(__file__).parent/'data/fangchan_data.csv'
    try:
        df = pd.read_csv(DATA_FILENAME, delimiter=';')
        min_y, max_y = 1998, 2025
        df = df.melt(['Country Code'], [str(x) for x in range(min_y, max_y + 1)], '时间', '房价')
        df['时间'] = pd.to_numeric(df['时间'])
        df = df.rename(columns={'Country Code': '城市'})
        return df
    except:
        return pd.DataFrame()

gdp_df = get_gdp_data()

# -------------------------- 交互控件并排 (显著节省空间) --------------------------
if not gdp_df.empty:
    c1, c2 = st.columns([1, 1.5])
    with c1:
        years = st.slider('区间', int(gdp_df['时间'].min()), int(gdp_df['时间'].max()), (2005, 2025), label_visibility="collapsed")
    with c2:
        cities = st.multiselect('城市', gdp_df['城市'].unique().tolist(), default=['北京', '上海', '深圳'], label_visibility="collapsed")
    
    filtered_df = gdp_df[(gdp_df['城市'].isin(cities)) & (gdp_df['时间'] >= years[0]) & (gdp_df['时间'] <= years[1])]

    # -------------------------- 图表区 --------------------------
    # 使用简洁分割线
    st.markdown("<hr style='margin: 0.5rem 0;'>", unsafe_allow_html=True)
    
    chart = alt.Chart(filtered_df).mark_line(point=alt.OverlayMarkDef(size=30)).encode(
        x=alt.X('时间:O', axis=alt.Axis(title=None, labelAngle=0, labelFontSize=9)),
        y=alt.Y('房价:Q', scale=alt.Scale(zero=False), axis=alt.Axis(title=None, labelFontSize=9)),
        color=alt.Color('城市:N', legend=alt.Legend(orient='top', title=None, labelFontSize=10)),
        tooltip=['城市', '时间', '房价']
    ).properties(height=260).configure_view(strokeWidth=0) # 减小图表高度
    
    st.altair_chart(chart, use_container_width=True)

    # -------------------------- 指标区 (6列布局) --------------------------
    st.markdown("## 同比增长分析")
    cols = st.columns(6)
    for i, city in enumerate(cities[:12]): # 最多展示两行
        city_data = gdp_df[gdp_df['城市'] == city]
        d_start = city_data[city_data['时间'] == years[0]]['房价']
        d_end = city_data[city_data['时间'] == years[1]]['房价']
        
        if not d_start.empty and not d_end.empty:
            v_start, v_end = d_start.iloc[0], d_end.iloc[0]
            growth = (v_end - v_start) / v_start if v_start != 0 else 0
            with cols[i % 6]:
                st.metric(label=city, value=f"{v_end:,.0f}", delta=f"{growth:+.1%}")
else:
    st.info("数据加载中或文件缺失...")

# -------------------------- 底部导航 --------------------------
NAV_ITEMS = ["财富排行", "世界房产", "城市房价", "全球法律", "全球企业", "合同审查", "德国财税", "深圳房市"]
nav_html = f"""
<div class="bottom-nav">
    {"".join([f'<a href="#" class="nav-item {"active" if i==2 else ""}">{item}</a>' for i, item in enumerate(NAV_ITEMS)])}
</div>
"""
st.markdown(nav_html, unsafe_allow_html=True)
