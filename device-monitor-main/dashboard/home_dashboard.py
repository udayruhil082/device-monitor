import requests
import streamlit as st

from backend.server_analytics import analytics as server_analytics
from backend.gateway_analytics import analytics as gateway_analytics

API = "http://127.0.0.1:8000"


def fetch(endpoint):
    try:
        response = requests.get(f"{API}/{endpoint}", timeout=3)

        if response.status_code == 200:
            return response.json()

    except Exception:
        return None

    return None


def show_home_dashboard():

    # --------------------------------------------------
    # Fetch Live Data
    # --------------------------------------------------

    latest_data = fetch("latest")

    server = server_analytics.get_analytics()

    gateway = gateway_analytics.get_analytics()

    # --------------------------------------------------
    # Camera Data
    # --------------------------------------------------

    if latest_data and latest_data.get("success"):

        camera_status = latest_data["metrics"]["connection_status"]
        camera_health = latest_data["analytics"]["health_score"]

    else:

        camera_status = "Offline"
        camera_health = 0

    # --------------------------------------------------
    # Server Data
    # --------------------------------------------------

    server_health = server["health_score"]
    server_status = "Online"

    # --------------------------------------------------
    # Gateway Data
    # --------------------------------------------------

    gateway_health = gateway["health_score"]
    gateway_status = "Connected"

    # --------------------------------------------------
    # System Summary
    # --------------------------------------------------

    devices_online = 0

    if camera_status == "ONLINE":
        devices_online += 1

    if server_status == "Online":
        devices_online += 1

    if gateway_status == "Connected":
        devices_online += 1

    average_health = round(
        (
            camera_health +
            server_health +
            gateway_health
        ) / 3
    )

    critical_devices = sum([
        camera_health < 60,
        server_health < 60,
        gateway_health < 60
    ])

    if critical_devices == 0:
        overall_status = "Healthy"
    elif critical_devices == 1:
        overall_status = "Warning"
    else:
        overall_status = "Critical"

    # --------------------------------------------------
    # UI
    # --------------------------------------------------

    st.title(" Intelligent Device Health Monitoring Platform IIIT-D")

    st.markdown(
        "Real-time monitoring and health status of connected intelligent devices."
    )

    st.divider()

    # --------------------------------------------------
    # Overall Status
    # --------------------------------------------------

    st.subheader(" Overall System Status")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("System Status", overall_status)

    with col2:
        st.metric("Devices Online", f"{devices_online} / 3")

    st.divider()

    # --------------------------------------------------
    # Device Overview
    # --------------------------------------------------

    st.subheader(" Device Overview")

    col1, col2, col3 = st.columns(3)

    card_style = """
    <div style="
    padding:20px;
    border-radius:12px;
    border:2px solid #2ECC71;
    background-color:#F8F9FA;
    text-align:center;
    box-shadow:0 2px 8px rgba(0,0,0,0.1);
    ">
    <h3>{icon} {name}</h3>
    <hr>
    <p><b>Status</b></p>
    <h4 style="color:green;">🟢 {status}</h4>

    <p><b>Health Score</b></p>
    <h2>{score}</h2>
    </div>
    """

    with col1:
        st.markdown(
            card_style.format(
                icon="📷",
                name="AI Camera",
                status=camera_status,
                score=f"{camera_health} / 100"
            ),
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            card_style.format(
                icon="🖥",
                name="Edge Server",
                status=server_status,
                score=f"{server_health} / 100"
            ),
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            card_style.format(
                icon="🌐",
                name="IoT Gateway",
                status=gateway_status,
                score=f"{gateway_health} / 100"
            ),
            unsafe_allow_html=True
        )

    st.divider()

    # --------------------------------------------------
    # System Summary
    # --------------------------------------------------

    st.subheader(" System Summary")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Devices Online",
            f"{devices_online} / 3"
        )

    with col2:
        st.metric(
            "Average Health",
            f"{average_health}%"
        )

    with col3:
        st.metric(
            "Critical Devices",
            critical_devices
        )

    with col4:
        st.metric(
            "Overall Status",
            overall_status
        )