import streamlit as st
import pandas as pd
import plotly.express as px

from utils.chart_style import style_chart

from components.header import page_header
from components.section import section
from components.cards import (
    metric_card, 
    recommendation_card, 
    renewable_summary_card
)
from components.footer import footer


def climate_risk_page():
    page_header(
        "🔥 Climate Risk Prediction",
        "Assess climate-related risks based on environmental, demographic, and pollution indicators."
    )

    # Risk Assessment Inputs
    section(
        "📋 Risk Assessment",
        "Provide environmental parameters to estimate climate-related risks."
    )

    col1, col2 = st.columns(2)

    with col1:
        temperature = st.slider("Average Temperature (°C)", 10, 50, 32)
        rainfall = st.slider("Annual Rainfall (mm)", 0, 5000, 900)
        humidity = st.slider("Humidity (%)", 10, 100, 60)

    with col2:
        population = st.slider("Population Density", 100, 30000, 4000)
        forest = st.slider("Forest Cover (%)", 0, 100, 25)
        pollution = st.slider("Pollution Index", 0, 500, 180)

    # Risk Calculation
    risk = (
        temperature * 2 +
        pollution * 0.25 +
        population / 1000 -
        forest * 0.3 -
        rainfall * 0.002
    )
    risk = max(risk, 0)

    if risk < 30:
        level = "Low"
        level_color = "#10B981"
    elif risk < 60:
        level = "Moderate"
        level_color = "#F59E0B"
    elif risk < 80:
        level = "High"
        level_color = "#F97316"
    else:
        level = "Extreme"
        level_color = "#EF4444"

    heat = min(100, temperature * 2 + pollution * 0.1)
    flood = max(0, rainfall / 50 - humidity / 5)
    flood = min(flood, 100)

    # Key Metrics
    section(
        "📊 Key Metrics",
        "Overall climate risk indicators."
    )

    kpi_cols = st.columns(4)

    with kpi_cols[0]:
        metric_card("Risk Score", f"{risk:.1f}/100", "🔥", "#EF4444")
    with kpi_cols[1]:
        metric_card("Risk Level", level, "⚠️", level_color)
    with kpi_cols[2]:
        metric_card("Forest Cover", f"{forest}%", "🌳", "#10B981")
    with kpi_cols[3]:
        metric_card("Pollution Index", f"{pollution}", "🏭", "#F97316")

    # Risk Contributors Charts
    section(
        "📈 Risk Contributors",
        "Contribution of each factor to the overall climate risk."
    )

    risk_df = pd.DataFrame({
        "Factor": ["Temperature", "Pollution", "Population", "Forest", "Rainfall"],
        "Contribution": [
            temperature * 2,
            pollution * 0.25,
            population / 1000,
            forest * 0.3,
            rainfall * 0.002
        ]
    })

    left, right = st.columns(2)

    with left:
        fig_bar = px.bar(
            risk_df,
            x="Factor",
            y="Contribution",
            color="Contribution",
            title="Risk Contributors"
        )
        fig_bar = style_chart(fig_bar)
        fig_bar.update_traces(
            texttemplate="%{y:.1f}",
            textposition="outside",
            textfont=dict(
                size=13,
                color="#0F172A"
            )
        )
        st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})

    with right:
        fig_pie = px.pie(
            risk_df,
            names="Factor",
            values="Contribution",
            hole=0.55,
            title="Contribution Share"
        )
        fig_pie = style_chart(fig_pie)
        fig_pie.update_layout(
            legend=dict(
                font=dict(
                    size=13,
                    color="#0F172A"
                )
            )
        )
        st.plotly_chart(fig_pie, use_container_width=True, config={"displayModeBar": False})

    # Heatwave Analysis
    section(
        "🌡️ Heatwave Analysis",
        "Estimated probability of heatwave occurrence."
    )

    st.progress(int(heat))
    st.markdown(f"**{heat:.1f}% Probability**")

    # Flood Analysis
    section(
        "🌊 Flood Analysis",
        "Estimated probability of flooding."
    )

    st.progress(int(flood))
    st.markdown(f"**{flood:.1f}% Probability**")

    # AI Recommendations
    section(
        "💡 Risk Mitigation Recommendations",
        "AI-generated suggestions to reduce climate risk."
    )

    recommendations = []

    if forest < 20:
        recommendations.append("Increase afforestation efforts.")
    if pollution > 200:
        recommendations.append("Reduce industrial emissions and promote clean energy.")
    if temperature > 35:
        recommendations.append("Implement urban cooling strategies like green roofs.")
    if rainfall < 500:
        recommendations.append("Strengthen water conservation and drought preparedness.")

    if not recommendations:
        recommendations.append("Current indicators are relatively stable.")

    recommendation_card("AI Risk Mitigation Recommendations", recommendations)

    # Risk Summary
    section(
        "📌 Risk Summary",
        "Overall climate risk assessment."
    )

    renewable_summary_card(
        f"{risk:.1f}/100",
        level,
        f"{heat:.1f}%",
        f"{flood:.1f}%"
    )

    footer()