import streamlit as st

# ==========================================
# Page Configuration (Must be First)
# ==========================================

st.set_page_config(
    page_title="Climate Intelligence Platform",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==========================================
# Load Global Styles
# ==========================================

def load_css():
    with open("styles/style.css", encoding="utf-8") as css:
        st.markdown(
            f"<style>{css.read()}</style>",
            unsafe_allow_html=True,
        )


load_css()

# ==========================================
# Import Pages
# ==========================================

from modules.dashboard import dashboard_page
from modules.climate import climate_page
from modules.air_quality import air_quality_page
from modules.carbon import carbon_page
from modules.renewable import renewable_page
from modules.climate_risk import climate_risk_page
from modules.simulation import simulation_page
from modules.report import report_page
from modules.ai_assistant import ai_assistant_page

# ==========================================
# Sidebar Branding
# ==========================================

st.sidebar.markdown(
    """
<div class="sidebar-logo">
    <div class="logo-circle">
        🌍
    </div>
    <h1>ClimateAI</h1>
    <p>Climate Intelligence Platform</p>
</div>
""",
    unsafe_allow_html=True,
)

# ==========================================
# Navigation
# ==========================================

PAGES = {
    "🏠 Dashboard": dashboard_page,
    "🌡 Climate Analytics": climate_page,
    "🌫 Air Quality": air_quality_page,
    "♻ Carbon Footprint": carbon_page,
    "⚡ Renewable Energy": renewable_page,
    "🌪 Climate Risk": climate_risk_page,
    "🧪 Climate Simulation": simulation_page,
    "📄 Sustainability Report": report_page,
    "🤖 AI Assistant": ai_assistant_page,
}

page = st.sidebar.radio(
    "Navigation",
    list(PAGES.keys()),
    label_visibility="visible",
)

# ==========================================
# Render Selected Page
# ==========================================

PAGES[page]()

# ==========================================
# Sidebar Footer
# ==========================================

st.sidebar.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)

st.sidebar.markdown(
    """
<div class="sidebar-footer">
    <div class="footer-title">
        Climate Intelligence Platform
    </div>
    <div class="footer-version">
        Version 2.0 • 2026
    </div>
    <div style="font-size: 0.75rem; color: #6b7280; margin-top: 8px;">
        Built with ❤️ for a sustainable future
    </div>
</div>
""",
    unsafe_allow_html=True,
)