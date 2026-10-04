import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

from utils.chart_style import style_chart

from components.header import page_header
from components.section import section
from components.footer import footer
from components.cards import (
    metric_card,
    recommendation_card,
    report_summary_card
)

def report_page():
    page_header(
        "📄 Sustainability Report Generator",
        "Generate sustainability assessments, ESG scores, environmental indicators, and AI-powered recommendations."
    )

    # Organization Information
    section(
        "🏢 Organization Information",
        "Enter your organization's basic details."
    )

    col1, col2 = st.columns(2)

    with col1:
        organization = st.text_input("Organization Name", "ABC Industries")
        location = st.text_input("Location", "Mumbai")

    with col2:
        sector = st.selectbox(
            "Sector",
            ["Manufacturing", "Education", "Healthcare", "IT", "Government", "Energy", "Other"]
        )
        employees = st.number_input("Employees", 1, 100000, 500)

    # Environmental Indicators
    section(
        "🌍 Environmental Indicators",
        "Provide key environmental performance metrics."
    )

    electricity = st.number_input("Annual Electricity (kWh)", 1000, 10000000, 500000)
    water = st.number_input("Annual Water Consumption (KL)", 100, 1000000, 50000)
    waste = st.number_input("Annual Waste (Tonnes)", 1, 50000, 500)
    renewable = st.slider("Renewable Energy (%)", 0, 100, 35)

    carbon = electricity * 0.82 / 1000
    score = round(renewable * 0.5 + max(0, 100 - carbon / 10) * 0.5, 1)

    # Key Metrics
    section(
        "📊 Key Metrics",
        "Overview of sustainability indicators."
    )

    kpi_cols = st.columns(4)

    with kpi_cols[0]:
        metric_card("Carbon Emissions", f"{carbon:.1f} t", "🏭", "#EF4444")
    with kpi_cols[1]:
        metric_card("Renewable Energy", f"{renewable}%", "⚡", "#10B981")
    with kpi_cols[2]:
        metric_card("Employees", f"{employees:,}", "👥", "#3B82F6")
    with kpi_cols[3]:
        metric_card("Sustainability Score", f"{score}/100", "🌱", "#10B981")

    # Environmental Dashboard
    section(
        "📈 Environmental Dashboard",
        "Visual representation of environmental indicators."
    )

    report = pd.DataFrame({
        "Indicator": ["Carbon", "Renewable", "Water", "Waste"],
        "Value": [carbon, renewable, water, waste]
    })

    fig = px.bar(
        report,
        x="Indicator",
        y="Value",
        color="Value",
        title="Environmental Indicators"
    )
    fig = style_chart(fig)
    fig.update_traces(
        texttemplate="%{y:.1f}",
        textposition="outside",
        textfont=dict(
            size=13,
            color="#0F172A"
        )
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # ESG Assessment
    section(
        "🏆 ESG Assessment",
        "Overall sustainability performance evaluation."
    )

    if score >= 80:
        st.success("🌱 Excellent Sustainability Performance")
    elif score >= 60:
        st.info("🌱 Good Sustainability Performance")
    elif score >= 40:
        st.warning("🌱 Average Sustainability Performance")
    else:
        st.error("🌱 Improvement Required")

    # AI Recommendations
    section(
        "💡 AI Recommendations",
        "Suggestions to improve sustainability performance."
    )

    recommendations = []

    if renewable < 50:
        recommendations.append("Increase renewable energy adoption.")
    if water > 100000:
        recommendations.append("Implement water conservation measures.")
    if waste > 1000:
        recommendations.append("Improve recycling and waste segregation.")
    if carbon > 300:
        recommendations.append("Reduce electricity consumption and improve efficiency.")

    if not recommendations:
        recommendations.append("Current sustainability indicators are performing well.")

    recommendation_card("AI Recommendations", recommendations)

    # Executive Summary
    section(
        "📋 Executive Summary",
        "Summary of the sustainability assessment."
    )

    report_summary_card(
        organization,
        sector,
        carbon,
        renewable,
        score,
        datetime.now().strftime("%d %B %Y")
    )

    # Export Report
    section(
        "⬇️ Export Report",
        "Download the generated sustainability report."
    )

    csv_data = report.to_csv(index=False)
    st.download_button(
        label="📥 Download Sustainability Report (CSV)",
        data=csv_data,
        file_name="sustainability_report.csv",
        mime="text/csv",
        use_container_width=True
    )

    footer()