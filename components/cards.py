import streamlit as st


def metric_card(title: str, value: str | int | float, icon: str = "", color: str = "#3B82F6"):
    """Reusable KPI metric card."""
    st.markdown(
        f"""
        <div style="background: white; padding: 1.5rem; border-radius: 12px; 
                    box-shadow: 0 1px 3px rgba(0,0,0,0.1); text-align: center; height: 100%;">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">{icon}</div>
            <div style="font-size: 2.1rem; font-weight: 700; color: {color};">{value}</div>
            <div style="color: #6b7280; font-size: 0.95rem; margin-top: 0.25rem;">{title}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def feature_card(icon, title, description):
    """Feature card used in dashboard."""
    st.markdown(
        f"""
        <div class="feature-card">
            <div class="feature-icon">{icon}</div>
            <div class="feature-title">{title}</div>
            <div class="feature-description">{description}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def info_card(title, content):
    st.markdown(
        f"""
        <div class="info-card">
            <div class="info-title">{title}</div>
            <div class="info-content">{content}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def aqi_status_card(aqi: float, category: str, emoji: str, color: str):
    """Dedicated AQI status card."""
    st.markdown(
        f"""
        <div style="background: white; padding: 2rem; border-radius: 16px; 
                    border: 1px solid #e5e7eb; text-align: center;">
            <div style="font-size: 3.5rem; margin-bottom: 0.5rem;">{emoji}</div>
            <div style="font-size: 1.8rem; font-weight: 700; color: {color};">{category}</div>
            <div style="font-size: 4rem; font-weight: 800; color: {color}; margin: 0.5rem 0;">{int(aqi)}</div>
            <div style="color: #6b7280; font-size: 1.1rem;">Air Quality Index • Latest Reading</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def summary_card(city: str, avg_aqi: float, max_aqi: float, min_aqi: float, records: int, category: str, emoji: str):
    """Research summary card."""
    st.markdown(
        f"""
        <div style="background: white; padding: 2rem; border-radius: 16px; border: 1px solid #e5e7eb;">
            <h3 style="margin-top: 0; color: #1f2937;">{city}</h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1.5rem; margin-top: 1.5rem;">
                <div>
                    <div style="color: #6b7280; font-size: 0.9rem;">AVERAGE AQI</div>
                    <div style="font-size: 2.2rem; font-weight: 700; color: #1f2937;">{avg_aqi:.1f}</div>
                    <div style="color: #10b981; font-size: 1rem;">{emoji} {category}</div>
                </div>
                <div>
                    <div style="color: #6b7280; font-size: 0.9rem;">MAXIMUM AQI</div>
                    <div style="font-size: 2.2rem; font-weight: 700; color: #ef4444;">{max_aqi:.1f}</div>
                </div>
                <div>
                    <div style="color: #6b7280; font-size: 0.9rem;">MINIMUM AQI</div>
                    <div style="font-size: 2.2rem; font-weight: 700; color: #10b981;">{min_aqi:.1f}</div>
                </div>
                <div>
                    <div style="color: #6b7280; font-size: 0.9rem;">TOTAL RECORDS</div>
                    <div style="font-size: 2.2rem; font-weight: 700; color: #1f2937;">{records}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def rating_card(rating: str, emoji: str, color: str, description: str):
    """Rating card used in Carbon Footprint."""
    st.markdown(
        f"""
        <div style="background: white; padding: 2.5rem; border-radius: 16px; 
                    border: 1px solid #e5e7eb; text-align: center;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">{emoji}</div>
            <div style="font-size: 2.2rem; font-weight: 700; color: {color};">{rating}</div>
            <div style="margin: 1.5rem 0; color: #4b5563; font-size: 1.1rem;">{description}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def recommendation_card(title: str, tips: list):
    """Reusable recommendation card."""
    if not tips:
        tips = ["Great job! Your impact is already relatively low."]

    html_tips = "".join([f"<li style='margin: 0.8rem 0; font-size: 1.05rem;'>✅ {tip}</li>" for tip in tips])

    st.markdown(
        f"""
        <div style="background: white; padding: 2rem; border-radius: 16px; border: 1px solid #e5e7eb;">
            <h4 style="margin-top: 0;">{title}</h4>
            <ul style="list-style: none; padding: 0;">
                {html_tips}
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )


def emission_summary_card(monthly: float, annual: float, trees: int):
    """Carbon summary card."""
    st.markdown(
        f"""
        <div style="background: white; padding: 2rem; border-radius: 16px; border: 1px solid #e5e7eb;">
            <h4 style="margin-top: 0;">Your Estimated Impact</h4>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1.5rem; margin-top: 1.5rem;">
                <div>
                    <div style="color: #6b7280;">Monthly Emissions</div>
                    <div style="font-size: 2rem; font-weight: 700;">{monthly:.1f} kg CO₂</div>
                </div>
                <div>
                    <div style="color: #6b7280;">Annual Emissions</div>
                    <div style="font-size: 2rem; font-weight: 700;">{annual:.2f} tonnes CO₂</div>
                </div>
                <div>
                    <div style="color: #6b7280;">Equivalent Trees</div>
                    <div style="font-size: 2rem; font-weight: 700;">{trees} trees/year</div>
                </div>
            </div>
            <div style="margin-top: 2rem; padding-top: 1.5rem; border-top: 1px solid #e5e7eb; color: #6b7280; font-size: 0.95rem;">
                This is an educational estimate.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def renewable_summary_card(daily_demand, renewable_gen, renewable_percent, annual_savings, carbon_saved):
    """Renewable energy summary card."""
    st.markdown(
        f"""
        <div style="background: white; padding: 2rem; border-radius: 16px; border: 1px solid #e5e7eb;">
            <h4 style="margin-top: 0;">Renewable Energy Summary</h4>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1.5rem; margin-top: 1.5rem;">
                <div><div style="color: #6b7280;">Daily Demand</div><div style="font-size: 1.8rem; font-weight: 700;">{daily_demand:.0f} kWh</div></div>
                <div><div style="color: #6b7280;">Renewable Generation</div><div style="font-size: 1.8rem; font-weight: 700;">{renewable_gen:.0f} kWh</div></div>
                <div><div style="color: #6b7280;">Renewable Share</div><div style="font-size: 1.8rem; font-weight: 700;">{renewable_percent:.1f}%</div></div>
                <div><div style="color: #6b7280;">Annual Savings</div><div style="font-size: 1.8rem; font-weight: 700;">₹{annual_savings:,.0f}</div></div>
                <div><div style="color: #6b7280;">Carbon Reduction</div><div style="font-size: 1.8rem; font-weight: 700;">{carbon_saved:.1f} t/year</div></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def simulation_summary_card(emission, renewable, trees, temperature_drop):
    # Force dark text on metrics
    st.markdown("""
    <style>
    div[data-testid="stMetricValue"] {
        color: #0F172A !important;
        font-size: 1.8rem !important;
        font-weight: 800 !important;
    }
    div[data-testid="stMetricLabel"] {
        color: #475569 !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    with st.container(border=True):
        st.subheader("Scenario Summary")

        c1, c2 = st.columns(2)
        c3, c4 = st.columns(2)

        with c1:
            st.metric("Emission Reduction", f"{emission}%")
        with c2:
            st.metric("Renewable Adoption", f"{renewable}%")
        with c3:
            st.metric("Trees Planted", f"{trees} Million")
        with c4:
            st.metric("Projected Cooling", f"{temperature_drop:.2f}°C")


def report_summary_card(organization, sector, carbon, renewable, score, generated_on):
    # Force dark text on metrics
    st.markdown("""
    <style>
    div[data-testid="stMetricValue"] {
        color: #0F172A !important;
        font-size: 1.6rem !important;
        font-weight: 800 !important;
    }
    div[data-testid="stMetricLabel"] {
        color: #475569 !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    with st.container(border=True):
        st.subheader("Executive Summary")

        c1, c2 = st.columns(2)
        c3, c4 = st.columns(2)
        c5, c6 = st.columns(2)

        with c1:
            st.metric("Organization", organization)
        with c2:
            st.metric("Sector", sector)
        with c3:
            st.metric("Carbon Emissions", f"{carbon:.2f} tonnes")
        with c4:
            st.metric("Renewable Energy", f"{renewable}%")
        with c5:
            st.metric("Sustainability Score", f"{score}/100")
        with c6:
            st.metric("Generated On", generated_on)


def ai_response_card(answer: str):
    """AI response card for assistant page."""
    st.markdown(
        f"""
        <div style="background: white; padding: 25px; border-radius: 18px; border: 1px solid #E5E7EB; box-shadow: 0 2px 10px rgba(0,0,0,.06); line-height: 1.8; font-size: 16px;">
            {answer}
        </div>
        """,
        unsafe_allow_html=True
    )