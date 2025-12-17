# -------------------------- 核心样式 (极致压缩版) --------------------------
st.markdown("""
<style>
    /* 1. 彻底隐藏默认干扰元素及占位 */
    #MainMenu, footer, header, [data-testid="stHeader"], [data-testid="stSidebar"], .stDeployButton {
        display: none !important;
        height: 0 !important;
    }
    
    /* 2. 核心：压缩内容容器的顶部留白 */
    .block-container {
        padding-top: 1rem !important;    /* 默认通常是 6rem，改为 1rem */
        padding-bottom: 5rem !important; /* 为底部导航留空间 */
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }

    /* 3. 压缩组件之间的默认间距 */
    [data-testid="stVerticalBlock"] {
        gap: 0.5rem !important;
    }

    /* 4. 全局紧凑化 */
    .stApp {
        background: #f8fafc !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* 5. 标题区域极致紧凑 */
    h1 {
        font-size: 1.4rem !important; 
        margin-top: -0.5rem !important; /* 向上微调 */
        margin-bottom: 0.2rem !important;
        line-height: 1.2 !important;
    }
    
    /* 按钮对齐微调 */
    .stHorizontalBlock {
        align-items: center !important;
    }

    /* 底部导航 (保持原样) */
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
        z-index: 9999 !important;
    }
    
    .nav-item {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        flex: 1 !important;
        height: 100% !important;
        color: #94a3b8 !important;
        text-decoration: none !important;
        font-size: 0.65rem !important;
        font-weight: 600 !important;
    }
    
    .nav-item.active {
        color: #2563eb !important;
        background: rgba(59,130,246,0.1) !important;
    }
</style>
""", unsafe_allow_html=True)
