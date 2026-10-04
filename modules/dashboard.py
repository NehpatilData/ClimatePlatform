import streamlit as st
import pandas as pd
import plotly.express as px

from components.header import page_header
from components.cards import metric_card, feature_card
from components.footer import footer
from components.section import section
from utils.chart_style import style_chart


@st.cache_data
def load_data():
    temperature = pd.read_csv("datasets/GlobalLandTemperaturesByCountry.csv")
    air = pd.read_csv("datasets/city_day.csv")
    co2 = pd.read_csv("datasets/owid-co2-data.csv")
    return temperature, air, co2


def dashboard_page():
    # Make the sidebar expand button (>>) clearly visible when sidebar is closed
    st.markdown("""
    <style>
        /* Only the expand button that appears when sidebar is collapsed */
        [data-testid="stSidebarCollapsedControl"] {
            background-color: #0F172A !important;
            border: 2px solid #334155 !important;
            border-radius: 10px !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.25) !important;
            width: 42px !important;
            height: 42px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            opacity: 1 !important;
            visibility: visible !important;
        }

        [data-testid="stSidebarCollapsedControl"] svg {
            fill: #FFFFFF !important;
            color: #FFFFFF !important;
            width: 20px !important;
            height: 20px !important;
        }

        [data-testid="stSidebarCollapsedControl"]:hover {
            background-color: #1E293B !important;
            border-color: #64748B !important;
        }
    </style>
    """, unsafe_allow_html=True)

    temperature, air, co2 = load_data()

    page_header(
        "🌍 Climate Intelligence Platform",
        "AI-powered Sustainability Analytics Dashboard"
    )

    # Welcome message
    st.info(
        "Welcome to Climate Intelligence Platform. Explore climate trends, air quality, "
        "carbon emissions and sustainability analytics using interactive visualizations."
    )

    # ── Top KPI Row (4 cards) ─────────────────────────────────────
    section(
        "📈 Key Metrics",
        "Real-time sustainability analytics at a glance"
    )

    k1, k2, k3, k4 = st.columns(4, gap="large")

    with k1:
        metric_card(
            "Temperature Records",
            f"{len(temperature):,}",
            "🌡",
            "#EF4444"
        )
    with k2:
        metric_card(
            "AQI Records",
            f"{len(air):,}",
            "🌫",
            "#F59E0B"
        )
    with k3:
        metric_card(
            "CO₂ Records",
            f"{len(co2):,}",
            "🏭",
            "#10B981"
        )
    with k4:
        metric_card(
            "Countries",
            f"{temperature['Country'].nunique()}",
            "🌍",
            "#3B82F6"
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Main Analytics Row: 70% Chart + 30% Summary ───────────────
    section(
        "📈 Global Temperature Trend",
        "Average global land temperature over time"
    )

    left, right = st.columns([7, 3], gap="large")

    with left:
        temp_chart = temperature.copy()
        temp_chart["dt"] = pd.to_datetime(temp_chart["dt"])
        temp_chart["Year"] = temp_chart["dt"].dt.year

        yearly = (
            temp_chart
            .groupby("Year")["AverageTemperature"]
            .mean()
            .reset_index()
        )

        fig = px.line(
            yearly,
            x="Year",
            y="AverageTemperature",
            markers=True,
            title="Global Average Temperature"
        )
        fig = style_chart(fig)
        fig.update_traces(line=dict(width=3), marker=dict(size=6))
        fig.update_layout(
            height=480,
            xaxis_title="",
            yaxis_title="Average Temperature (°C)"
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False}
        )

    with right:
        st.markdown("""
        <div style="background-color: white; padding: 24px; border-radius: 8px;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.1); height: 100%;">
            <h3 style="margin-top: 0; color: #1f2937;">Climate Summary</h3>
            <ul style="padding-left: 20px; margin-bottom: 0; line-height: 1.7;">
                <li><strong>180+ Countries</strong></li>
                <li><strong>Millions of Records</strong></li>
                <li><strong>Historical Climate Data</strong></li>
                <li><strong>AI Powered Analytics</strong></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Data Sources ─────────────────────────────────────────────
    section(
        "📁 Data Sources",
        "Datasets powering the platform"
    )

    c1, c2, c3 = st.columns(3, gap="large")

    with c1:
        feature_card(
            "🌍",
            "Global Temperature",
            "Global historical temperature observations spanning multiple decades."
        )
    with c2:
        feature_card(
            "🌫",
            "Air Quality",
            "Daily air quality measurements across multiple Indian cities."
        )
    with c3:
        feature_card(
            "🏭",
            "Carbon Emissions",
            "Worldwide carbon emission statistics from the Our World in Data project."
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── AI & Analytics Modules ───────────────────────────────────
    section(
        "🚀 AI & Analytics Modules",
        "Available AI-powered modules"
    )

    f1, f2, f3, f4 = st.columns(4, gap="large")

    with f1:
        feature_card(
            "🌡",
            "Climate Analytics",
            "Explore historical climate trends, patterns and anomalies."
        )
    with f2:
        feature_card(
            "🌫",
            "Air Quality",
            "AQI monitoring and analysis."
        )
    with f3:
        feature_card(
            "♻",
            "Carbon",
            "Estimate and analyze carbon emissions with actionable insights."
        )
    with f4:
        feature_card(
            "🤖",
            "AI Assistant",
            "LLM-powered sustainability assistant."
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Platform Highlights ─────────────────────────────────────
    section(
        "📊 Platform Highlights",
        "Key information about the analytics platform"
    )

    s1, s2, s3, s4 = st.columns(4, gap="large")

    with s1:
        metric_card("Datasets", "3", "📁", "#3B82F6")
    with s2:
        metric_card("AI Modules", "8", "🤖", "#8B5CF6")
    with s3:
        metric_card("Countries Covered", "180+", "🌍", "#10B981")
    with s4:
        metric_card("Interactive Dashboards", "9", "📊", "#F97316")

    footer()