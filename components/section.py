import streamlit as st

def section(title: str, subtitle: str = "", icon: str = ""):
    st.markdown(
        f"""
        <div class="section-block">
            <div class="section-title">
                {icon} {title}
            </div>
            {f'<div class="section-subtitle">{subtitle}</div>' if subtitle else ''}
        </div>
        """,
        unsafe_allow_html=True
    )