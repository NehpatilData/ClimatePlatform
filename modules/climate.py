import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

from sklearn.linear_model import LinearRegression

from utils.data_loader import load_temperature
from utils.chart_style import style_chart
from components.header import page_header
from components.section import section
from components.cards import metric_card, info_card
from components.footer import footer


def climate_page():
    temperature = load_temperature()

    temperature["dt"] = pd.to_datetime(temperature["dt"])
    temperature["Year"] = temperature["dt"].dt.year
    temperature["Month"] = temperature["dt"].dt.month_name()

    temperature = temperature.dropna(
        subset=["Country", "AverageTemperature", "Year"]
    )

    countries = sorted(temperature["Country"].unique())
    default_country = "India" if "India" in countries else countries[0]

    page_header(
        "🌡 Climate Analytics",
        "Explore historical climate trends, forecasts, anomalies, and country-level insights."
    )

    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Overview",
        "📈 Statistics",
        "🔮 Forecast",
        "🤖 AI Insights"
    ])

    # ── OVERVIEW TAB ─────────────────────────────────────────────────
    with tab1:
        section("🌍 World Temperature Map", "Global average temperature by country")

        # Filters
        col1, col2 = st.columns([2, 1])
        with col1:
            selected = st.multiselect(
                "Compare Countries",
                countries,
                default=[default_country]
            )
        with col2:
            year_range = st.slider(
                "Year Range",
                int(temperature["Year"].min()),
                int(temperature["Year"].max()),
                (int(temperature["Year"].min()), int(temperature["Year"].max()))
            )

        if not selected:
            st.warning("Please select at least one country.")
            return

        # World Map
        world_avg = (
            temperature
            .groupby("Country")["AverageTemperature"]
            .mean()
            .reset_index()
        )

        fig_map = px.choropleth(
            world_avg,
            locations="Country",
            locationmode="country names",
            color="AverageTemperature",
            color_continuous_scale="Turbo",
            title="Global Average Temperature"
        )
        fig_map = style_chart(fig_map)

        fig_map.update_layout(
            geo=dict(
                showframe=False,
                showcoastlines=True,
                coastlinecolor="#94A3B8",
                bgcolor="rgba(0,0,0,0)"
            ),
            coloraxis_colorbar=dict(
                title="Temperature (°C)",
                tickfont=dict(
                    size=13,
                    color="#0F172A"
                ),
                title_font=dict(
                    size=14,
                    color="#0F172A"
                )
            )
        )
        st.plotly_chart(fig_map, use_container_width=True)

        # KPIs
        section("📊 Key Performance Indicators", "Country-level climate metrics")

        compare_df = temperature[
            (temperature["Country"].isin(selected)) &
            (temperature["Year"] >= year_range[0]) &
            (temperature["Year"] <= year_range[1])
        ]

        compare_yearly = (
            compare_df
            .groupby(["Year", "Country"])["AverageTemperature"]
            .mean()
            .reset_index()
        )

        country = default_country if default_country in selected else selected[0]

        df = temperature[
            (temperature["Country"] == country) &
            (temperature["Year"] >= year_range[0]) &
            (temperature["Year"] <= year_range[1])
        ]

        yearly = (
            df.groupby("Year")["AverageTemperature"]
            .mean()
            .reset_index()
            .sort_values("Year")
        )

        if yearly.empty:
            st.warning("No data available for the selected filters.")
            return

        warming = yearly.iloc[-1]["AverageTemperature"] - yearly.iloc[0]["AverageTemperature"]
        avg_temp = yearly["AverageTemperature"].mean()
        max_temp = yearly["AverageTemperature"].max()
        min_temp = yearly["AverageTemperature"].min()
        std_temp = yearly["AverageTemperature"].std()
        years_available = yearly.shape[0]

        k1, k2, k3 = st.columns(3)
        k4, k5, k6 = st.columns(3)

        with k1: metric_card("Average Temperature", f"{avg_temp:.2f}°C", "🌡", "#EF4444")
        with k2: metric_card("Maximum", f"{max_temp:.2f}°C", "🔥", "#F59E0B")
        with k3: metric_card("Minimum", f"{min_temp:.2f}°C", "❄️", "#3B82F6")
        with k4: metric_card("Std Deviation", f"{0 if pd.isna(std_temp) else std_temp:.2f}°C", "📊", "#8B5CF6")
        with k5: metric_card("Warming", f"{warming:.2f}°C", "📈", "#10B981")
        with k6: metric_card("Years", str(years_available), "📅", "#F97316")

        # Trend Charts
        section("🌎 Multi-Country Temperature Comparison", "Trend analysis across selected countries")
        fig_compare = px.line(
            compare_yearly,
            x="Year",
            y="AverageTemperature",
            color="Country",
            markers=True
        )
        fig_compare = style_chart(fig_compare)

        fig_compare.update_traces(
            line=dict(width=3),
            marker=dict(size=7)
        )
        st.plotly_chart(fig_compare, use_container_width=True)

        section(f"📈 Temperature Trend - {country}", "Historical temperature evolution")
        fig_trend = px.line(
            yearly,
            x="Year",
            y="AverageTemperature",
            markers=True
        )
        fig_trend = style_chart(fig_trend)

        fig_trend.update_traces(
            line=dict(width=3),
            marker=dict(size=7)
        )
        st.plotly_chart(fig_trend, use_container_width=True)

        # Climate Assessment
        section("🌡️ Climate Assessment", "Risk evaluation and recommendations")
        risk_level = "High" if warming > 2 else "Moderate" if warming > 1 else "Low"
        recommendation = "Continue monitoring long-term warming trends." if risk_level == "High" else "Maintain current environmental policies."

        info_card(
            "Climate Assessment Summary",
            f"""
**Country**: {country}  
**Average Temperature**: {avg_temp:.2f}°C  
**Temperature Change**: {warming:.2f}°C  
**Risk Level**: {risk_level}  
**Recommendation**: {recommendation}
"""
        )

    # ── STATISTICS TAB ───────────────────────────────────────────────
    with tab2:
        section("Temperature Distribution", "Distribution of annual temperatures")

        left, right = st.columns(2)
        with left:
            fig_hist = px.histogram(df, x="AverageTemperature", nbins=30)
            fig_hist = style_chart(fig_hist)

            fig_hist.update_layout(
                bargap=0.08
            )
            st.plotly_chart(fig_hist, use_container_width=True)

        with right:
            month_order = ["January", "February", "March", "April", "May", "June",
                          "July", "August", "September", "October", "November", "December"]
            fig_box = px.box(
                df,
                x="Month",
                y="AverageTemperature",
                category_orders={"Month": month_order}
            )
            fig_box = style_chart(fig_box)

            fig_box.update_traces(
                line=dict(width=2)
            )
            st.plotly_chart(fig_box, use_container_width=True)

        section("Top 10 Hottest Countries", "Global ranking by average temperature")
        hottest = (
            temperature
            .groupby("Country")["AverageTemperature"]
            .mean()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )
        fig_hottest = px.bar(
            hottest,
            x="Country",
            y="AverageTemperature",
            color="AverageTemperature"
        )
        fig_hottest = style_chart(fig_hottest)

        fig_hottest.update_traces(
            texttemplate="%{y:.1f}",
            textposition="outside",
            textfont=dict(
                size=13,
                color="#0F172A"
            )
        )
        st.plotly_chart(fig_hottest, use_container_width=True)

        section("Climate Statistics", "Descriptive statistics")
        st.dataframe(yearly.describe(), use_container_width=True)

    # ── FORECAST TAB ─────────────────────────────────────────────────
    with tab3:
        section("📈 Linear Regression Prediction", "Temperature forecast for next 20 years")

        if len(yearly) >= 2:
            model = LinearRegression()
            X = yearly[["Year"]]
            y = yearly["AverageTemperature"]
            model.fit(X, y)

            future = pd.DataFrame({
                "Year": range(int(yearly["Year"].max()) + 1, int(yearly["Year"].max()) + 21)
            })
            future["Prediction"] = model.predict(future[["Year"]])

            fig_future = px.line(
                yearly,
                x="Year",
                y="AverageTemperature",
                title=f"{country} Temperature Forecast"
            )
            fig_future.add_scatter(
                x=future["Year"],
                y=future["Prediction"],
                mode="lines",
                name="Forecast"
            )
            fig_future = style_chart(fig_future)

            fig_future.update_traces(
                line=dict(width=3)
            )
            st.plotly_chart(fig_future, use_container_width=True)
        else:
            st.info("Not enough yearly data to generate a forecast.")

        section("Climate Anomaly Detection", "Temperature anomalies over time")
        yearly_anom = yearly.copy()
        yearly_anom["MovingAverage"] = yearly_anom["AverageTemperature"].rolling(10).mean()
        yearly_anom["Anomaly"] = yearly_anom["AverageTemperature"] - yearly_anom["MovingAverage"]

        fig_anomaly = px.line(
            yearly_anom,
            x="Year",
            y="Anomaly",
            title="Temperature Anomaly"
        )
        fig_anomaly = style_chart(fig_anomaly)

        fig_anomaly.update_traces(
            line=dict(width=3)
        )
        st.plotly_chart(fig_anomaly, use_container_width=True)

    # ── AI INSIGHTS TAB ──────────────────────────────────────────────
    with tab4:
        section("🤖 AI Climate Insights", "AI-powered analysis and recommendations")

        ai_summary = f"""
**Country**: {country}
**Average Temperature**: {avg_temp:.2f} °C
**Maximum**: {max_temp:.2f} °C
**Minimum**: {min_temp:.2f} °C
**Overall Change**: {warming:.2f} °C

Forecast indicates continued warming.
"""
        info_card("AI Climate Summary", ai_summary)

        section("📚 Research Summary", "Key findings from the analysis")
        research_text = f"""
Average temperature of {country} is {avg_temp:.2f} °C.

Maximum observed: {max_temp:.2f} °C
Minimum observed: {min_temp:.2f} °C
Standard deviation: {0 if pd.isna(std_temp) else std_temp:.2f} °C
Warming rate: {warming:.2f} °C
Years analyzed: {years_available}
"""
        info_card("Research Summary", research_text)

        section("📥 Downloads & Reports", "Export your analysis")
        st.download_button(
            "Download Climate Data (CSV)",
            yearly.to_csv(index=False),
            "climate_analysis.csv",
            "text/csv"
        )

        st.info(
            "PDF report generation will include graphs, statistics, and AI summary. "
            "You can integrate ReportLab for formatted PDF export."
        )

    footer()