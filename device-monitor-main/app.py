import streamlit as st
from streamlit_autorefresh import st_autorefresh

from dashboard.home_dashboard import show_home_dashboard
from dashboard.camera_dashboard import show_camera_dashboard
from dashboard.server_dashboard import show_server_dashboard
from dashboard.gateway_dashboard import show_gateway_dashboard

from backend.gateway_service import gateway


# MUST BE FIRST STREAMLIT COMMAND
st.set_page_config(
    page_title="Intelligent Device Health Monitoring Platform IIIT-D",
    page_icon="🖥️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Global CSS
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html,
body,
.stApp,
.main,
[data-testid="stAppViewContainer"],
[data-testid="stMain"]{
    font-family:'Inter',sans-serif;
    background:#EEF3F8;
}

/* Sidebar */
[data-testid="stSidebar"]{
    background:#FFFFFF;
    border-right:1px solid #E5E7EB;
}

/* Metric Cards */
div[data-testid="metric-container"]{
    background:#FFFFFF;
    border-radius:14px;
    border:1px solid #E5E7EB;
    box-shadow:0 2px 8px rgba(0,0,0,.08);
    padding:15px;
}

</style>
""", unsafe_allow_html=True)



st_autorefresh(
    interval=10000,
    key="dashboard_refresh"
)

st.sidebar.title(" Device Monitor")

device = st.sidebar.radio(
    "Select Device",
    [
        "🏠 Home",
        "📷 AI Camera",
        "🖥 Edge Server",
        "🌐 IoT Gateway",
    ]
)

if device == "🏠 Home":
    show_home_dashboard()

elif device == "📷 AI Camera":
    show_camera_dashboard()

elif device == "🖥 Edge Server":
    show_server_dashboard()

elif device == "🌐 IoT Gateway":
    st.sidebar.markdown("---")
    data = gateway.get_all_data()

    if data["lan"]["up"]:
        st.sidebar.success("🟢 Gateway Connected")
    else:
        st.sidebar.error("🔴 Gateway Offline")

    show_gateway_dashboard()
