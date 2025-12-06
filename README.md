# [房价趋势透视](https://fangchan.streamlit.app/) 

该 Readme 重点突出应用的核心功能（**核心城市房价可视化**、**时间轴对比**）和使用的关键技术（**Streamlit**、**Pandas**、**Altair**）。

-----

# 📈 核心城市房价趋势透视看板 (Housing Price Trend Dashboard)

本应用是一个基于 **Streamlit** 构建的**核心城市房产数据分析看板**。它利用 **Pandas** 进行高效数据处理，并使用 **Altair** 生成高度交互式的可视化图表，帮助用户直观地分析和对比过去 **30 年间**选定城市的**房价走势**和**增长情况**。

🚀 **[点击此处访问应用]** (请替换为您的 Streamlit App 链接)

-----

## ✨ 核心功能与亮点 (SEO 关键词优化)

  * **城市房价对比分析 (City Price Comparison):** 支持用户在多选框中选择多个核心城市（如北京、上海、深圳等），将所有城市的历史房价数据叠加在同一图表上进行对比。
  * **时序趋势可视化 (Time Series Visualization):** 通过 Altair **交互式折线图**，清晰展示选定时间区间内的房价波动和长期趋势。
  * **灵活时间轴筛选 (Flexible Time Range):** 用户可通过滑块选择任意时间区间（如 2005 年至今），精确聚焦特定年份段的增长情况。
  * **关键指标速览 (Key Metric Display):** 自动计算并以 `st.metric` 卡片形式展示选定时间段内的**房价同比增长率**（或复合增长率），直观了解不同城市的投资回报潜力。
  * **数据预处理：** 应用内建有数据加载和 `pd.melt` 转换逻辑，将宽格式数据转换为长格式，优化了 Streamlit 的数据渲染性能。

-----

## 🔑 核心关键词 (SEO 优化)

| 关键词类别 | 核心术语 |
| :--- | :--- |
| **应用主题** | **房价趋势**, **城市房价分析**, **房地产数据**, **时序分析**, **数据可视化看板** |
| **地理范围** | **中国城市房产**, **核心城市房价**, **北京**, **上海**, **深圳** |
| **技术栈** | **Streamlit**, **Pandas**, **Altair Chart**, **Python 数据分析** |

-----

## ⚙️ 如何本地部署 (Quick Start)

### 1\. 数据准备

本应用依赖一个名为 `fangchan_data.csv` 的数据文件。请确保在项目根目录内创建 `data` 文件夹，并将您的数据文件放置其中。

**数据格式要求：** 文件应为分号分隔 (`delimiter=;`) 的宽格式 CSV，至少包含 `Country Code` (城市名称) 列，以及以年份命名的价格数据列（如 `1998` 到 `2025`）。

### 2\. 克隆仓库

```bash
git clone [您的仓库链接]
cd [您的仓库名]
```

### 3\. 环境与依赖

```bash
# 创建并激活虚拟环境
python -m venv venv
source venv/bin/activate # Linux/macOS

# 安装依赖
pip install streamlit pandas altair pathlib
```

### 4\. 运行应用

```bash
streamlit run app.py
```

-----

## 🗺️ 底部导航栏概览 (Nav Bar Overview)

为了提供完整的生态体验，此应用集成了多个相关的**外部工具**和**数据看板**：

| 链接名称 | 目标功能 |
| :--- | :--- |
| **财富排行** | 🔗 外部链接 (`youqian.streamlit.app`) |
| **世界房产** | 🔗 外部链接 (`fangchan.streamlit.app`) **(当前页面)** |
| **城市房价** | 🔗 外部链接 (`fangjia.streamlit.app`) |
| **全球法律** | 🔗 外部链接 (`chuhai.streamlit.app`) |
| **全球企业** | 🔗 外部链接 (`chuhai.streamlit.app`) |
| **合同审查** | 🔗 外部链接 (`chuhai.streamlit.app`) |
| **德国财税** | 🔗 外部链接 (`qfschina.streamlit.app`) |
| **深圳房市** | 🔗 外部链接 (`fangjia.streamlit.app`) |
