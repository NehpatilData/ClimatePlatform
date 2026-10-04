import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import load_air_quality
from utils.chart_style import style_chart

from components.header import page_header
from components.section import section
from components.cards import (
    metric_card, 
    aqi_status_card, 
    summary_card
)
from components.footer import footer


def get_aqi_category(aqi: float) -> tuple[str, str, str]:
    """Return AQI category, emoji, and color for consistent display."""
    if aqi <= 50:
        return "Good", "🟢", "#505150"
    elif aqi <= 100:
        return "Satisfactory", "🔵", "#3b82f6"
    elif aqi <= 200:
        return "Moderate", "🟠", "#f59e0b"
    elif aqi <= 300:
        return "Poor", "🔴", "#ef4444"
    elif aqi <= 400:
        return "Very Poor", "🔴", "#b91c1c"
    else:
        return "Severe", "⚫", "#1f2937"


def air_quality_page():
    """Air Quality Analytics page for the Climate Intelligence Platform."""
    page_header(
        title="Air Quality Analytics",
        subtitle="Real-time monitoring and insights into urban air pollution across major cities. "
                 "Track AQI trends, pollutant levels, and health implications.",
        icon="🌫️"
    )

    # Load and prepare data
    air = load_air_quality()
    air["Date"] = pd.to_datetime(air["Date"])
    air["Year"] = air["Date"].dt.year
    air["Month"] = air["Date"].dt.month_name()

    cities = sorted(air["City"].dropna().unique())

    # Filters
    section(
        "🔎 Filters",
        "Select a city to analyze air quality."
    )

    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        selected_city = st.selectbox(
            "Select City",
            options=cities,
            index=cities.index("Delhi") if "Delhi" in cities else 0,
            help="Choose a city to analyze its air quality data"
        )

    # Filter data
    city_df = air[air["City"] == selected_city].copy()
    if city_df.empty:
        st.error("No data available for the selected city.")
        return

    latest = city_df.iloc[-1]
    current_aqi = float(latest["AQI"])

    # KPI Cards
    section(
        "📊 Key Metrics",
        "Latest air quality indicators."
    )

    kpi_cols = st.columns(4)

    with kpi_cols[0]:
        metric_card(
            title="AQI",
            value=int(current_aqi),
            icon="🌬️",
            color="#ef4444"
        )

    with kpi_cols[1]:
        metric_card(
            title="PM2.5",
            value=round(float(latest.get("PM2.5", 0)), 1),
            icon="☁️",
            color="#f97316"
        )

    with kpi_cols[2]:
        metric_card(
            title="PM10",
            value=round(float(latest.get("PM10", 0)), 1),
            icon="🌫️",
            color="#f59e0b"
        )

    with kpi_cols[3]:
        metric_card(
            title="NO₂",
            value=round(float(latest.get("NO2", 0)), 1),
            icon="🚗",
            color="#10b981"
        )

    # AQI Status
    category, emoji, color = get_aqi_category(current_aqi)
    section(
        "📍 Current AQI Status",
        "Current air quality category."
    )

    aqi_status_card(current_aqi, category, emoji, color)

    # AQI Trend
    section(
        "📈 AQI Trend Over Time",
        "Historical average AQI."
    )

    yearly = city_df.groupby("Year")["AQI"].mean().reset_index()

    fig_trend = px.line(
        yearly,
        x="Year",
        y="AQI",
        markers=True,
        color_discrete_sequence=["#ef4444"]
    )
    fig_trend = style_chart(fig_trend)

    fig_trend.update_traces(
        line=dict(width=3),
        marker=dict(size=7)
    )

    st.plotly_chart(fig_trend, use_container_width=True, config={"displayModeBar": False})

    # Distribution Charts
    section(
        "📊 AQI Distribution & Seasonality",
        "Distribution and monthly variation."
    )

    dist_cols = st.columns(2)

    with dist_cols[0]:
        fig_hist = px.histogram(
            city_df,
            x="AQI",
            nbins=40,
            color_discrete_sequence=["#64748b"]
        )
        fig_hist = style_chart(fig_hist)

        fig_hist.update_layout(
            title="AQI Distribution",
            bargap=0.08
        )
        st.plotly_chart(fig_hist, use_container_width=True, config={"displayModeBar": False})

    with dist_cols[1]:
        fig_monthly = px.box(
            city_df,
            x="Month",
            y="AQI",
            color_discrete_sequence=["#3b82f6"]
        )
        fig_monthly = style_chart(fig_monthly)

        fig_monthly.update_layout(
            title="Monthly AQI Variation"
        )

        fig_monthly.update_traces(
            line=dict(width=2)
        )
        st.plotly_chart(fig_monthly, use_container_width=True, config={"displayModeBar": False})

    # Pollutant Analysis (Violin)
    section(
        "🧪 Pollutant Analysis",
        "Distribution of major pollutants."
    )

    pollutants = ["PM2.5", "PM10", "NO", "NO2", "NOx", "NH3", "CO", "SO2", "O3", "Benzene", "Toluene", "Xylene"]
    available_pollutants = [p for p in pollutants if p in city_df.columns]

    if available_pollutants:
        fig_pollutants = px.violin(
            city_df,
            y=available_pollutants,
            template="plotly_white",
            color_discrete_sequence=px.colors.qualitative.Set3,
            box=True
        )
        fig_pollutants = style_chart(fig_pollutants)

        fig_pollutants.update_layout(
            title="Distribution of Key Pollutants",
            yaxis_title="Concentration",
            xaxis_title="Pollutant"
        )

        fig_pollutants.update_traces(
            line=dict(width=2)
        )
        st.plotly_chart(fig_pollutants, use_container_width=True, config={"displayModeBar": False})
    else:
        st.info("No pollutant data available for detailed analysis.")

    # Top Polluted Cities
    section(
        "🏆 Top 10 Most Polluted Cities",
        "Cities ranked by average AQI."
    )

    top_cities = (
        air.groupby("City")["AQI"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig_top = px.bar(
        top_cities,
        x="AQI",
        y="City",
        orientation="h",
        color="AQI",
        color_continuous_scale="Reds"
    )
    fig_top = style_chart(fig_top)
    fig_top.update_layout(
        title="Average AQI by City (Highest to Lowest)",
        xaxis_title="Average AQI",
        yaxis_title=""
    )
    fig_top.update_traces(
        texttemplate="%{x:.1f}",
        textposition="outside",
        textfont=dict(
            size=13,
            color="#0F172A"
        )
    )

    st.plotly_chart(fig_top, use_container_width=True, config={"displayModeBar": False})

    # Research Summary
    avg_aqi = city_df["AQI"].mean()
    max_aqi = city_df["AQI"].max()
    min_aqi = city_df["AQI"].min()
    num_records = len(city_df)

    summary_category, summary_emoji, _ = get_aqi_category(avg_aqi)

    section(
        "📋 Research Summary",
        "Overall analysis for the selected city."
    )

    summary_card(
        selected_city,
        avg_aqi,
        max_aqi,
        min_aqi,
        num_records,
        summary_category,
        summary_emoji
    )

    # Export
    section(
        "⬇️ Export Analysis",
        "Download the filtered dataset."
    )

    csv_data = city_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Air Quality Dataset",
        data=csv_data,
        file_name=f"air_quality_{selected_city.lower().replace(' ', '_')}.csv",
        mime="text/csv",
        use_container_width=True,
        help="Download the filtered dataset for the selected city as CSV"
    )

    footer()