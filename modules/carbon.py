import streamlit as st
import plotly.express as px
import pandas as pd

from utils.chart_style import style_chart

from components.header import page_header
from components.section import section
from components.cards import (
    metric_card, 
    rating_card, 
    recommendation_card, 
    emission_summary_card
)
from components.footer import footer


def calculate_emissions(
    electricity: float,
    petrol: float,
    flights: int,
    waste: float,
    lpg: int,
    meat: int
) -> dict:
    """Calculate carbon emissions from all sources."""
    electricity_emission = electricity * 0.82
    petrol_emission = petrol * 2.31
    flight_emission = flights * 250
    waste_emission = waste * 0.55
    lpg_emission = lpg * 42
    meat_emission = meat * 20

    total_monthly = (
        electricity_emission +
        petrol_emission +
        flight_emission +
        waste_emission +
        lpg_emission +
        meat_emission
    )

    total_annual = total_monthly * 12 / 1000
    trees_needed = int(total_monthly * 12 / 22)

    emission_df = pd.DataFrame({
        "Source": ["Electricity", "Petrol", "Flights", "Waste", "LPG", "Food"],
        "Emission (kg CO₂)": [
            round(electricity_emission, 2),
            round(petrol_emission, 2),
            round(flight_emission, 2),
            round(waste_emission, 2),
            round(lpg_emission, 2),
            round(meat_emission, 2)
        ]
    })

    return {
        "monthly": total_monthly,
        "annual": total_annual,
        "trees": trees_needed,
        "df": emission_df,
        "breakdown": {
            "Electricity": electricity_emission,
            "Petrol": petrol_emission,
            "Flights": flight_emission,
            "Waste": waste_emission,
            "LPG": lpg_emission,
            "Food": meat_emission
        }
    }


def get_carbon_rating(annual: float) -> tuple[str, str, str, str]:
    """Return rating, emoji, color and description."""
    if annual < 2:
        return "Excellent", "🟢", "#10b981", "Your footprint is very low. Keep up the great work!"
    elif annual < 5:
        return "Average", "🟡", "#eab308", "Moderate footprint. Small changes can make a big difference."
    elif annual < 8:
        return "High", "🟠", "#f59e0b", "Consider actionable steps to reduce your emissions."
    else:
        return "Very High", "🔴", "#ef4444", "Significant reduction opportunities available."


def carbon_page():
    """Carbon Footprint Calculator page."""
    page_header(
        title="Carbon Footprint Calculator",
        subtitle="Estimate your personal annual CO₂ emissions and discover practical ways to reduce your climate impact.",
        icon="🌍"
    )

    # Input Section
    section(
        "📋 Personal Carbon Calculator",
        "Enter your monthly and annual lifestyle details."
    )

    st.markdown("**Enter your monthly / annual habits**")

    col1, col2 = st.columns(2)

    with col1:
        electricity = st.number_input("Monthly Electricity Consumption (kWh)", min_value=0, max_value=5000, value=300, step=10)
        petrol = st.number_input("Monthly Petrol Consumption (Litres)", min_value=0, max_value=500, value=50, step=5)
        flights = st.number_input("Number of Flights per Year", min_value=0, max_value=100, value=2, step=1)

    with col2:
        waste = st.number_input("Monthly Waste Generated (kg)", min_value=0, max_value=500, value=30, step=5)
        lpg = st.number_input("LPG Cylinders per Year", min_value=0, max_value=30, value=8, step=1)
        meat = st.slider("Meat-based Meals per Week", min_value=0, max_value=21, value=5)

    # Centered Calculate Button
    _, center_col, _ = st.columns([1, 2, 1])
    with center_col:
        calculate_clicked = st.button(
            "Calculate Carbon Footprint",
            type="primary",
            use_container_width=True
        )

    # Results
    if calculate_clicked:
        results = calculate_emissions(electricity, petrol, flights, waste, lpg, meat)
        monthly = results["monthly"]
        annual = results["annual"]
        trees = results["trees"]
        emission_df = results["df"]

        # KPI Cards
        section(
            "📊 Emission Overview",
            "Your estimated carbon footprint."
        )

        kpi_cols = st.columns(4)
        with kpi_cols[0]:
            metric_card("Monthly CO₂", f"{monthly:.1f} kg", "📅", "#3b82f6")
        with kpi_cols[1]:
            metric_card("Annual CO₂", f"{annual:.2f} t", "🌍", "#ef4444")
        with kpi_cols[2]:
            metric_card("Trees Needed", f"{trees}", "🌳", "#10b981")
        with kpi_cols[3]:
            rating, _, color, _ = get_carbon_rating(annual)
            metric_card("Sustainability Rating", rating, "🏷️", color)

        # Rating Card
        rating, emoji, color, description = get_carbon_rating(annual)
        section(
            "⭐ Sustainability Rating",
            "Overall environmental performance."
        )

        rating_card(rating, emoji, color, description)

        # Emission Analysis Charts
        section(
            "📈 Emission Analysis",
            "Contribution of each emission source."
        )

        chart_cols = st.columns(2)

        with chart_cols[0]:
            fig_pie = px.pie(
                emission_df,
                values="Emission (kg CO₂)",
                names="Source",
                hole=0.55
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

        with chart_cols[1]:
            fig_bar = px.bar(
                emission_df.sort_values("Emission (kg CO₂)", ascending=False),
                x="Source",
                y="Emission (kg CO₂)",
                color="Emission (kg CO₂)",
                color_continuous_scale="Reds"
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

        # Recommendations
        section(
            "💡 Reduction Recommendations",
            "Personalized suggestions to reduce emissions."
        )

        tips = []
        if electricity > 250: tips.append("Switch to energy-efficient appliances and LED lighting.")
        if petrol > 80: tips.append("Consider carpooling, public transport, or an electric vehicle.")
        if flights > 4: tips.append("Reduce air travel. Combine trips when possible.")
        if meat > 7: tips.append("Incorporate more plant-based meals.")
        if waste > 40: tips.append("Practice Reduce, Reuse, Recycle and compost organic waste.")

        recommendation_card("Reduction Recommendations", tips)

        # Emission Summary
        section(
            "📌 Emission Summary",
            "Overall carbon footprint summary."
        )

        emission_summary_card(monthly, annual, trees)

        # Export
        section(
            "⬇️ Export Analysis",
            "Download your analysis."
        )

        csv_data = emission_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Carbon Report (CSV)",
            data=csv_data,
            file_name="carbon_footprint_report.csv",
            mime="text/csv",
            use_container_width=True
        )

    else:
        st.info(
            "👆 Fill in your details and click **Calculate Carbon Footprint** to generate "
            "your personalized emissions report and reduction recommendations."
        )

    footer()