import streamlit as st
import pandas as pd
import math
from pathlib import Path

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='房价趋势透视',
    page_icon='📈', # This is an emoji shortcode. Could be a URL too.
)

# -----------------------------------------------------------------------------
# Declare some useful functions.

@st.cache_data
def get_gdp_data():
    """Grab GDP data from a CSV file.

    This uses caching to avoid having to read the file every time. If we were
    reading from an HTTP endpoint instead of a file, it's a good idea to set
    a maximum age to the cache with the TTL argument: @st.cache_data(ttl='1d')
    """

    # Instead of a CSV on disk, you could read from an HTTP endpoint here too.
    DATA_FILENAME = Path(__file__).parent/'data/fangchan_data.csv'
    raw_gdp_df = pd.read_csv(DATA_FILENAME, delimiter=';')

    MIN_YEAR = 1998
    MAX_YEAR = 2025

    # The data above has columns like:
    # - Country Name
    # - Country Code
    # - [Stuff I don't care about]
    # - GDP for 1960
    # - GDP for 1961
    # - GDP for 1962
    # - ...
    # - GDP for 2022
    #
    # ...but I want this instead:
    # - Country Name
    # - Country Code
    # - Year
    # - GDP
    #
    # So let's pivot all those year-columns into two: Year and GDP


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

min_value = gdp_df['时间'].min()
max_value = gdp_df['时间'].max()

from_year, to_year = st.slider(
    '时间区间',
    min_value=min_value,
    max_value=max_value,
    value=[2005, max_value])

countries = gdp_df['城市'].unique()

if not len(countries):
    st.warning("Select at least one country")

selected_countries = st.multiselect(
    '城市',
    countries,
    ['北京', '上海', '深圳', '杭州', '成都', '烟台'])

''
''
''

# Filter the data
filtered_gdp_df = gdp_df[
    (gdp_df['城市'].isin(selected_countries))
    & (gdp_df['时间'] <= to_year)
    & (from_year <= gdp_df['时间'])
]

st.header('房价走势', divider='gray')

''

st.line_chart(
    filtered_gdp_df,
    x='时间',
    y='房价',
    color='城市',
)

''
''
import altair as alt  # 确保你导入了 altair

# ... (你之前的过滤代码保持不变) ...

st.header('房价走势', divider='gray')

# 1. 计算当前过滤后数据的最小值和最大值 (为了设置坐标轴范围)
# 为了视觉美观，通常会在最低价基础上留一点缓冲空间 (例如减去 5% 或直接用 min)
y_min = filtered_gdp_df['房价'].min()
y_max = filtered_gdp_df['房价'].max()

# 2. 使用 Altair 构建图表
chart = alt.Chart(filtered_gdp_df).mark_line().encode(
    # X轴设置：format='d' 确保年份显示为 2020 而不是 2,020
    x=alt.X('时间', axis=alt.Axis(format='d', title='年份')),
    
    # Y轴设置：关键在于 scale=alt.Scale(domain=[min, max])
    # zero=False 表示不强制包含0刻度
    y=alt.Y('房价', 
            scale=alt.Scale(domain=[y_min, y_max], zero=False), 
            axis=alt.Axis(title='平均房价 (元/㎡)')),
            
    # 颜色区分城市
    color='城市',
    
    # 鼠标悬停显示具体数值
    tooltip=['城市', '时间', '房价']
).interactive() # 允许缩放和平移

# 3. 渲染图表
st.altair_chart(chart, use_container_width=True)




first_year = gdp_df[gdp_df['时间'] == from_year]
last_year = gdp_df[gdp_df['时间'] == to_year]

st.header(f'{to_year}年房价同比增长', divider='gray')

''

cols = st.columns(4)

for i, country in enumerate(selected_countries):
    col = cols[i % len(cols)]

    with col:
        first_gdp = first_year[first_year['城市'] == country]['房价'].iat[0] 
        last_gdp = last_year[last_year['城市'] == country]['房价'].iat[0] 

        if math.isnan(first_gdp):
            growth = 'n/a'
            delta_color = 'off'
        else:
            # growth = f'{last_gdp / first_gdp:,.2f}x'
            # delta_color = 'normal'

            pct_change = (last_gdp - first_gdp) / first_gdp
            growth = f'{pct_change:+.2%}'
            delta_color = 'normal'
            
        st.metric(
            label=f'{country}',
            value=f'{last_gdp:,.0f}',
            delta=growth,
            delta_color=delta_color
        )
