import streamlit as st

st.set_page_config(
    page_title="Nifty 100 Analytics",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📈 N100 Financial Intelligence Platform")

st.markdown("""
Welcome to the **Nifty 100 Financial Intelligence Platform**.

Use the sidebar to navigate between:

- 🏠 Home
- 🏢 Company Profile
- 🔍 Stock Screener
- 🤝 Peer Comparison
- 📈 Trend Analysis
- 🏭 Sector Analysis
- 💰 Capital Allocation
- 📄 Annual Reports
""")

st.info("Select a page from the left sidebar to begin.")