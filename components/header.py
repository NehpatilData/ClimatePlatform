import streamlit as st

def page_header(title: str, subtitle: str, icon: str = "🌍"):
    st.markdown(
        f"""
        <div class="page-header">
            <div style="display: flex; align-items: center; gap: 16px;">
                <div style="font-size: 48px;">{icon}</div>
                <div>
                    <div class="page-title">{title}</div>
                    <div class="page-subtitle">{subtitle}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )