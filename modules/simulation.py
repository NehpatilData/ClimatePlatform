import streamlit as st
import pandas as pd
import plotly.express as px

from utils.chart_style import style_chart

from components.header import page_header
from components.section import section
from components.footer import footer
from components.cards import (
    metric_card,
    recommendation_card,
    simulation_summary_card
)

def simulation_page():
    page_header(
        "🌱 Climate Scenario Simulator",
        "Simulate climate policies and visualize their long-term impact on global temperature and carbon emissions."
    )

    # Policy Simulator Inputs
    section(
        "📋 Policy Simulator",
        "Adjust policy parameters to explore different climate scenarios."
    )

    col1, col2 = st.columns(2)

    with col1:
        emission = st.slider("Emission Reduction (%)", 0, 100, 20)
        renewable = st.slider("Renewable Adoption (%)", 0, 100, 35)

    with col2:
        trees = st.slider("Tree Plantation (Millions)", 0, 500, 50)

    # Calculations
    temperature_drop = (
        emission * 0.02 +
        renewable * 0.01 +
        trees * 0.003
    )

    carbon_reduction = (
        emission * 2 +
        renewable +
        trees * 0.2
    )

    # Future Projection
    years = list(range(2025, 2041))
    future = []
    base = 1.5
    for y in years:
        base += 0.03
        future.append(base - temperature_drop)

    df = pd.DataFrame({
        "Year": years,
        "Temperature": future
    })

    # Key Metrics
    section(
        "📊 Key Metrics",
        "Overview of the simulated climate policy outcomes."
    )

    kpi_cols = st.columns(3)

    with kpi_cols[0]:
        metric_card("Estimated Cooling", f"{temperature_drop:.2f}°C", "❄️", "#3B82F6")
    with kpi_cols[1]:
        metric_card("Carbon Reduction", f"{carbon_reduction:.1f}%", "🌿", "#10B981")
    with kpi_cols[2]:
        metric_card("Renewable Adoption", f"{renewable}%", "⚡", "#F59E0B")

    # Projected Temperature Chart
    section(
        "📈 Projected Temperature",
        "Projected global temperature under the selected scenario."
    )

    fig = px.line(
        df,
        x="Year",
        y="Temperature",
        markers=True,
        title="Projected Temperature"
    )
    fig = style_chart(fig)
    fig.update_traces(
        line=dict(width=3),
        marker=dict(size=7)
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # Policy Recommendation
    section(
        "💡 Policy Recommendation",
        "Suggested actions based on the selected scenario."
    )

    recommendations = []

    if renewable < 40:
        recommendations.append("Increase renewable deployment targets.")
    if emission < 30:
        recommendations.append("Strengthen emission reduction policies.")
    if trees < 100:
        recommendations.append("Scale up large-scale tree plantation programs.")

    if not recommendations:
        recommendations.append("Scenario shows strong positive climate impact.")

    recommendation_card("Policy Recommendations", recommendations)

    # Scenario Summary
    section(
        "📌 Scenario Summary",
        "Overall simulation results."
    )

    simulation_summary_card(
        emission,
        renewable,
        trees,
        temperature_drop
    )

    footer()