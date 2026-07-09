import streamlit as st
from streamlit_autorefresh import st_autorefresh

from dashboard.camera_dashboard import show_camera_dashboard
from dashboard.server_dashboard import show_server_dashboard

st.set_page_config(
    page_title="Intelligent Device Health Monitoring Platform",
    page_icon="🖥️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st_autorefresh(
    interval=10000,
    key="dashboard_refresh"
)

st.sidebar.title("🖥 Device Monitor")

device = st.sidebar.radio(
    "Select Device",
    [
        "📷 AI Camera",
        "🖥 Edge Server",
        "🚁 Drone"
    ]
)

if device == "📷 AI Camera":

    show_camera_dashboard()

elif device == "🖥 Edge Server":

    show_server_dashboard()

else:

    st.info("🚁 Drone Module Coming Soon")