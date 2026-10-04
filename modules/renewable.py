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


def renewable_page(): 
    page_header(
        "⚡ Renewable Energy Intelligence",
        "Analyze renewable energy production, cost savings, and carbon reduction."
    )

    # Renewable Energy Calculator
    section(
        "📋 Renewable Energy Calculator",
        "Configure your renewable energy setup."
    )

    col1, col2 = st.columns(2)

    with col1:
        daily_demand = st.number_input(
            "Daily Electricity Demand (kWh)",
            100, 100000, 5000
        )
        solar_capacity = st.slider("Solar Capacity (kW)", 0, 5000, 1000)
        wind_capacity = st.slider("Wind Capacity (kW)", 0, 5000, 500)

    with col2:
        sunlight = st.slider("Average Sunlight (hrs/day)", 1.0, 12.0, 5.5)
        wind_hours = st.slider("Wind Utilization (hrs/day)", 1.0, 24.0, 8.0)
        electricity_price = st.slider("Electricity Price (₹/kWh)", 3.0, 15.0, 8.0)

    # Calculations
    solar_generation = solar_capacity * sunlight
    wind_generation = wind_capacity * wind_hours * 0.35
    renewable_generation = solar_generation + wind_generation
    fossil_generation = max(daily_demand - renewable_generation, 0)
    renewable_percent = (renewable_generation / daily_demand) * 100 if daily_demand > 0 else 0
    annual_savings = renewable_generation * electricity_price * 365
    carbon_saved = renewable_generation * 0.82 * 365 / 1000

    # Key Metrics (5 cards)
    section(
        "📊 Key Metrics",
        "Overview of renewable energy performance."
    )

    kpi_cols = st.columns(5)

    with kpi_cols[0]:
        metric_card("Renewable Share", f"{renewable_percent:.1f}%", "⚡", "#10B981")
    with kpi_cols[1]:
        metric_card("Daily Generation", f"{renewable_generation:.0f} kWh", "🌞", "#3B82F6")
    with kpi_cols[2]:
        metric_card("Annual Savings", f"₹{annual_savings:,.0f}", "💰", "#F59E0B")
    with kpi_cols[3]:
        metric_card("CO₂ Saved", f"{carbon_saved:.1f} t", "🌍", "#10B981")
    with kpi_cols[4]:
        metric_card("Fossil Generation", f"{fossil_generation:.0f} kWh", "🏭", "#EF4444")

    # Energy Mix Charts
    section(
        "📈 Energy Mix & Generation",
        "Visualize renewable and fossil energy generation."
    )

    energy = pd.DataFrame({
        "Source": ["Solar", "Wind", "Fossil"],
        "Energy": [solar_generation, wind_generation, fossil_generation]
    })

    left, right = st.columns(2)

    with left:
        fig_pie = px.pie(
            energy,
            names="Source",
            values="Energy",
            hole=0.55,
            title="Energy Mix"
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

    with right:
        fig_bar = px.bar(
            energy,
            x="Source",
            y="Energy",
            color="Energy",
            title="Generation Comparison"
        )
        fig_bar = style_chart(fig_bar)
        fig_bar.update_traces(
            texttemplate="%{y:.0f}",
            textposition="outside",
            textfont=dict(
                size=13,
                color="#0F172A"
            )
        )
        st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})

    # AI Recommendations
    section(
        "💡 AI Energy Recommendations",
        "Suggestions to improve renewable energy utilization."
    )

    recommendations = []

    if renewable_percent < 40:
        recommendations.append("Increase solar capacity to boost renewable share.")
    if wind_capacity < solar_capacity / 2:
        recommendations.append("Evaluate additional wind installations for better diversification.")
    if sunlight < 4:
        recommendations.append("Improve panel orientation or consider solar tracking systems.")
    if fossil_generation > daily_demand * 0.3:
        recommendations.append("Consider battery storage to reduce fossil fuel dependence.")

    if not recommendations:
        recommendations.append("Excellent renewable utilization! Your setup is well optimized.")

    recommendation_card("AI Recommendations", recommendations)

    # Renewable Summary
    section(
        "📌 Renewable Summary",
        "Overall renewable energy performance summary."
    )

    renewable_summary_card(
        daily_demand,
        renewable_generation,
        renewable_percent,
        annual_savings,
        carbon_saved
    )

    footer()