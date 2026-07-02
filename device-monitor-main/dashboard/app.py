import streamlit as st
import requests
import pandas as pd
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# -------------------------------------------------------
# CONFIG
# -------------------------------------------------------

API = "http://127.0.0.1:8000"

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

# -------------------------------------------------------
# CSS
# -------------------------------------------------------

st.markdown("""
<style>

[data-testid="stAppViewContainer"]{
    background:#F8FAFC;
}

[data-testid="stSidebar"]{
    background:#FFFFFF;
}

.block-container{
    padding-top:1rem;
    padding-bottom:1rem;
}

.metric-card{
    background:#1F2937;
    padding:15px;
    border-radius:12px;
    border-left:5px solid #00C853;
}

.threshold-box{
    background:#18212F;
    padding:18px;
    border-radius:10px;
    border-left:5px solid #2196F3;
    margin-top:15px;
}

.alert-box{
    background:#202833;
    padding:12px;
    border-radius:10px;
    border-left:5px solid #F44336;
    margin-bottom:10px;
}

h1,h2,h3{
    color:#1F2937;
}
</style>
""", unsafe_allow_html=True)



# -------------------------------------------------------
# API FUNCTIONS
# -------------------------------------------------------

def fetch(endpoint):

    try:

        response = requests.get(
            f"{API}/{endpoint}",
            timeout=3
        )

        if response.status_code == 200:
            return response.json()

    except Exception:
        pass

    return None


latest_data = fetch("latest")
history_data = fetch("history")
alert_data = fetch("alerts")

# -------------------------------------------------------
# SIDEBAR
# -------------------------------------------------------

st.sidebar.title("🖥 Device Monitor")

device = st.sidebar.radio(
    "Select Device",
    [
        "📷 AI Camera",
        "🚁 Drone"
    ]
)

st.sidebar.markdown("---")

if latest_data and latest_data["success"]:

    metrics = latest_data["metrics"]

    if metrics["connection_status"] == "ONLINE":
        st.sidebar.success("🟢 Camera Online")
    else:
        st.sidebar.error("🔴 Camera Offline")

else:
    st.sidebar.error("Backend Offline")

st.sidebar.markdown("---")

st.sidebar.subheader("🚨 Active Alerts")

if alert_data and alert_data["success"]:

    alerts = alert_data["alerts"]

    if len(alerts) == 0:

        st.sidebar.success("No Active Alerts")

    else:

        for alert in alerts:

            level = alert.get("level", "INFO")
            title = alert.get("title", "Alert")

            if level == "CRITICAL":
                st.sidebar.error(title)

            elif level == "WARNING":
                st.sidebar.warning(title)

            else:
                st.sidebar.info(title)

else:

    st.sidebar.info("Waiting for alerts...")

# -------------------------------------------------------
# HEADER
# -------------------------------------------------------

st.title("🖥 Intelligent Device Health Monitoring Platform")

from streamlit.components.v1 import html

html("""
<div style="font-size:16px;font-weight:bold;color:#555;">
Last Updated:
<span id="clock"></span>
</div>

<script>

function updateClock(){

    const now = new Date();

    document.getElementById("clock").innerHTML =
        now.toLocaleTimeString();

}

updateClock();

setInterval(updateClock,1000);

</script>

""",height=35)

st.markdown("---")

# -------------------------------------------------------
# DEVICE SELECT
# -------------------------------------------------------

if device == "🚁 Drone":

    st.info("🚁 Drone integration will be added soon.")

    st.stop()

# -------------------------------------------------------
# TABS
# -------------------------------------------------------

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "📊 Live Metrics",
        "📷 Device Information",
        "📈 Analytics",
        "⚙ Settings"
    ]
)
# -------------------------------------------------------
# LIVE METRICS
# -------------------------------------------------------

with tab1:

    if latest_data and latest_data["success"]:

        metrics = latest_data["metrics"]
        analytics = latest_data["analytics"]

        latency = metrics["latency"]
        status = metrics["connection_status"]
        packet_loss = metrics["packet_loss"]

        health_score = analytics["health_score"]

        # -------------------------------
        # Failure Risk
        # -------------------------------

        if status != "ONLINE":
            failure_risk = "🔴 HIGH"
            prediction = "Device failure expected.\nCamera is offline."

        elif latency < 60:
            failure_risk = "🟢 LOW"
            prediction = "No failure expected."

        elif latency <= 100:
            failure_risk = "🟡 MEDIUM"
            prediction = "Network degradation expected\nwithin next 5 minutes."

        else:
            failure_risk = "🔴 HIGH"
            prediction = "Critical latency detected.\nImmediate attention required."

        last_update = datetime.now().strftime("%I:%M:%S %p")

        st.subheader("📊 Live Device Metrics")

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric(
                "📶 Latency",
                f"{latency} ms"
            )

        with c2:
            st.metric(
                "🟢 Connection",
                status
            )

        with c3:
            st.metric(
                "📉 Packet Loss",
                f"{packet_loss}%"
            )

        c4, c5, c6 = st.columns(3)

        with c4:
            st.metric(
                "💚 Health Score",
                f"{health_score}/100"
            )

        with c5:
            st.metric(
                "🔮 Failure Risk",
                failure_risk
            )

        with c6:
            st.metric(
                "⏱ Last Update",
                last_update
            )

        st.markdown("---")

        st.subheader("🔮 Predicted Failure")

        if "LOW" in failure_risk:
            st.success(prediction)

        elif "MEDIUM" in failure_risk:
            st.warning(prediction)

        else:
            st.error(prediction)

        st.markdown("---")

        st.subheader("📘 Health Thresholds")

        st.info(
            """
🟢 **Latency < 60 ms**
Healthy

🟡 **Latency 60–100 ms**
Moderate Network Delay

🔴 **Latency > 100 ms**
Critical Latency

⚫ **Connection Offline**
Device Failure
"""
        )

        st.markdown("---")

        st.subheader("📈 Latency Trend")

        if history_data and history_data["success"]:

            df = pd.DataFrame(history_data["history"])

            if not df.empty:

                df = df.sort_values("id")

                df["timestamp"] = pd.to_datetime(df["timestamp"])

                df["Time"] = df["timestamp"].dt.strftime("%H:%M:%S")

                chart = df[
                    [
                        "Time",
                        "latency"
                    ]
                ].set_index("Time")

                st.line_chart(chart)

            else:

                st.info("No latency history available.")

        else:

            st.info("Waiting for historical data...")

    else:

        st.error("Unable to connect to backend.")
        # -------------------------------------------------------
# ANALYTICS
# -------------------------------------------------------

with tab3:

    if latest_data and latest_data["success"]:

        analytics = latest_data["analytics"]

        avg_latency = analytics["average_latency"]
        max_latency = analytics["maximum_latency"]
        stability = analytics["connection_stability"]
        health = analytics["health_score"]

        st.subheader("📈 Device Health Analytics")

        c1, c2 = st.columns(2)

        with c1:

            st.metric(
                "Average Latency",
                f"{avg_latency} ms"
            )

            if avg_latency < 60:
                st.success("🟢 Excellent")
            elif avg_latency <= 100:
                st.warning("🟡 Moderate")
            else:
                st.error("🔴 Poor")

        with c2:

            st.metric(
                "Maximum Latency",
                f"{max_latency} ms"
            )

            if max_latency > 100:
                st.error("🔴 Critical Spike Detected")
            else:
                st.success("🟢 Normal")

        st.markdown("---")

        c3, c4 = st.columns(2)

        with c3:

            st.metric(
                "Connection Stability",
                f"{stability}%"
            )

            if stability >= 95:
                st.success("🟢 Stable")
            elif stability >= 80:
                st.warning("🟡 Acceptable")
            else:
                st.error("🔴 Unstable")

        with c4:

            st.metric(
                "Health Score",
                f"{health}/100"
            )

            if health >= 80:
                st.success("Excellent")
            elif health >= 60:
                st.warning("Moderate")
            else:
                st.error("Critical")

        st.markdown("---")

        st.subheader("💚 Health Score")

        st.progress(int(health))

        st.markdown("---")

        st.subheader("🔮 Prediction")

        if avg_latency < 60:

         st.success(
        """
🟢 No failure expected

Average latency is within the healthy range.

Continue monitoring.
"""
    )

        elif avg_latency <= 100:

         st.warning(
        """
🟡 Network degradation expected

Average latency is increasing.

Possible network congestion within the next few minutes.
"""
    )

        else:

         st.error(
        """
🔴 High failure probability

Average latency has crossed the critical threshold.

Immediate inspection is recommended.
"""
    )

st.markdown("---")

st.subheader("🤖 AI Diagnosis")

if health >= 80:

            st.success(
                """
System is healthy.

No signs of imminent failure.

Continue monitoring.
"""
            )

elif health >= 60:

            st.warning(
                """
Increasing latency trend detected.

Possible network congestion.

Inspect network link.
"""
            )

else:

            st.error(
                """
Critical device condition detected.

Immediate investigation recommended.

Check connectivity and hardware status.
"""
            )

st.markdown("---")

st.subheader("🔮 Predicted Failure")

        # -------------------------------------------------------
# SETTINGS
# -------------------------------------------------------

with tab4:


    if latest_data and latest_data["success"]:

        device = latest_data["device"]

        st.subheader("⚙ Camera Configuration")

        st.text_input(
            "IP Address",
            value=device["ip_address"],
            disabled=True,
            key="settings_ip"
        )

        st.text_input(
            "Username",
            value="admin",
            disabled=True,
            key="settings_username"
        )

        st.text_input(
            "Password",
            value="********",
            disabled=True,
            key="settings_password"
        )

        st.number_input(
            "Polling Interval (Seconds)",
            value=3,
            disabled=True,
            key="settings_polling"
        )

        st.markdown("---")

        st.success("Backend Connected")

        st.info(
            "Configuration editing will be available in Version 2."
        )

        c1, c2 = st.columns(2)

        with c1:

            if st.button(
                "Reconnect Camera",
                key="btn_reconnect"
            ):

                st.success(
                    "Reconnect request sent."
                )

        with c2:

            if st.button(
                "Refresh Dashboard",
                key="btn_refresh"
            ):

                st.rerun()

    else:

        st.error("Backend Offline")
        # -------------------------------------------------------
# DEVICE INFORMATION
# -------------------------------------------------------

with tab2:

    if latest_data and latest_data["success"]:

        d = latest_data["device"]

        left, right = st.columns(2)

        with left:

            st.text_input(
                "Device Name",
                d["device_name"],
                disabled=True,
                key="device_name"
            )

            st.text_input(
                "Manufacturer",
                d["manufacturer"],
                disabled=True,
                key="manufacturer"
            )

            st.text_input(
                "Model",
                d["model"],
                disabled=True,
                key="model"
            )

            st.text_input(
                "Firmware",
                d["firmware"],
                disabled=True,
                key="firmware"
            )

            st.text_input(
                "Device ID",
                d["device_id"],
                disabled=True,
                key="device_id"
            )

        with right:

            st.text_input(
                "Serial Number",
                d["serial_number"],
                disabled=True,
                key="serial_number"
            )

            st.text_input(
                "Hardware ID",
                d["hardware_id"],
                disabled=True,
                key="hardware_id"
            )

            st.text_input(
                "IP Address",
                d["ip_address"],
                disabled=True,
                key="ip_address_device"
            )

            st.text_input(
                "MAC Address",
                d["mac_address"],
                disabled=True,
                key="mac_address"
            )

            st.text_input(
                "ONVIF Version",
                d["onvif_version"],
                disabled=True,
                key="onvif_version"
            )

    else:

        st.warning("Device information unavailable.")