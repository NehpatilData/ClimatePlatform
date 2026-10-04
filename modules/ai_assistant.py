import streamlit as st
from utils.gemini import ask_ai

from components.header import page_header
from components.section import section
from components.cards import ai_response_card
from components.footer import footer


def ai_assistant_page():
    page_header(
        "🤖 AI Sustainability Assistant",
        "Ask AI about climate change, sustainability, renewable energy, carbon emissions and environmental analytics."
    )

    section(
        "💬 Ask a Question",
        "Enter any sustainability-related question and receive an AI-generated response."
    )

    question = st.text_area(
        "Your Question",
        placeholder="Example: How can AI help reduce carbon emissions in smart cities?",
        height=180
    )

    # Centered buttons
    left, middle, right = st.columns([1, 1, 4])

    with middle:
        generate = st.button("🚀 Generate", use_container_width=True)

    with left:
        clear = st.button("🗑 Clear", use_container_width=True)

    if clear:
        st.rerun()

    if generate:
        if not question.strip():
            st.warning("Please enter a question.")
            return

        with st.spinner("🧠 Analyzing your question... Generating AI-powered sustainability insights..."):
            answer = ask_ai(question)

        st.markdown("<br>", unsafe_allow_html=True)

        section(
            "🧠 AI Response",
            "Generated using Google Gemini"
        )

        ai_response_card(answer)

    st.markdown("<br>", unsafe_allow_html=True)

    # Suggested Questions
    section(
        "💡 Suggested Questions",
        "Click any example and paste it into the question box."
    )

    c1, c2 = st.columns(2)

    with c1:
        st.info("""
• What causes global warming?  
• Explain carbon neutrality.  
• What is the AQI?  
• What are greenhouse gases?  
• How do electric vehicles reduce emissions?
""")

    with c2:
        st.info("""
• Explain the Paris Climate Agreement.  
• Benefits of renewable energy.  
• How can AI help climate change?  
• Sustainable Development Goals.  
• Carbon footprint reduction strategies.
""")

    footer()