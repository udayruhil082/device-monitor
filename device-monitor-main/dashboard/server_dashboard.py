import streamlit as st
from datetime import datetime

from backend.server_analytics import analytics
from backend.server_predictor import predictor
from backend.server_alerts import alerts
# =====================================================
# HEADER
# =====================================================

def show_header():

    st.title(" Edge Server Health Monitoring")

    st.markdown(
        """
        Monitor the health and performance of the edge server in real time.
        """
    )

    st.divider()


# =====================================================
# SERVER SUMMARY
# =====================================================

def show_summary():

    analytics_data = st.session_state.server_data

    prediction = st.session_state.server_prediction

    live = analytics_data["live"]

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "❤️ Health Score",
            f'{analytics_data["health_score"]}/100'
        )

    with col2:

        st.metric(
            "📈 Trend",
            analytics_data["trend"]
        )

    with col3:

        st.metric(
            "⚠ Failure Risk",
            prediction["risk"]
        )

    with col4:

        st.metric(
            "🕒 Last Update",
            datetime.now().strftime("%H:%M:%S")
        )

    st.divider()


# =====================================================
# TABS
# =====================================================

def create_tabs():

    return st.tabs(

        [

            " Live Monitoring",

            " Device Information",

            " AI Health & Prediction",

            " External Data"

        ]

    )
    
    # =====================================================
# LIVE MONITORING TAB
# =====================================================

def show_live_monitoring():

    analytics_data = st.session_state.server_data

    live = analytics_data["live"]

    st.subheader(" Live Server Metrics")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "CPU Usage",
            f"{live['cpu']} %"
        )

        st.metric(
            "RAM Usage",
            f"{live['memory']['usage_percent']} %"
        )

    with col2:

        st.metric(
            "Disk Usage",
            f"{live['disk']['usage_percent']} %"
        )

        st.metric(
            "Load Average (1 min)",
            live["load"]["1_min"]
        )

    with col3:

        st.metric(
            "Running Processes",
            live["processes"]
        )

        st.metric(
            "System Uptime",
            live["uptime"]
        )

    st.divider()

    st.subheader(" Live Resource Utilization")

    cpu_col, ram_col, disk_col = st.columns(3)

    with cpu_col:

        st.progress(min(int(live["cpu"]), 100))

        st.caption(f"CPU : {live['cpu']} %")

    with ram_col:

        st.progress(min(int(live["memory"]["usage_percent"]), 100))

        st.caption(f"RAM : {live['memory']['usage_percent']} %")

    with disk_col:

        st.progress(min(int(live["disk"]["usage_percent"]), 100))

        st.caption(f"Disk : {live['disk']['usage_percent']} %")

    st.divider()

    st.success("🟢 Server is connected and live metrics are being monitored.")
    
    # =====================================================
# DEVICE INFORMATION TAB
# =====================================================

def show_device_information():

    analytics_data = st.session_state.server_data

    live = analytics_data["live"]

    cpu_info = live["cpu_info"]

    st.subheader(" Edge Server Information")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### General Information")

        st.info(f"""
**Hostname**

{live["hostname"]}

**IP Address**

{live["ip"]}

**Operating System**

{live["os"]}

**Filesystem**

{live["disk"]["filesystem"]}

**Disk Capacity**

{live["disk"]["total"]}
""")

    with col2:

        st.markdown("### CPU Information")

        st.info(f"""
**CPU Model**

{cpu_info["model"]}

**Architecture**

{cpu_info["architecture"]}

**Sockets**

{cpu_info["sockets"]}

**Cores Per Socket**

{cpu_info["cores"]}

**Total Threads**

{cpu_info["threads"]}
""")

    st.divider()

    st.subheader(" Storage Information")

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(

            "Disk Capacity",

            live["disk"]["total"]

        )

    with c2:

        st.metric(

            "Used",

            live["disk"]["used"]

        )

    with c3:

        st.metric(

            "Free",

            live["disk"]["free"]

        )

    with c4:

        st.metric(

            "Usage",

            live["disk"]["usage"]

        )

    st.divider()

    st.success("✅ Device information fetched successfully from the Edge Server.")
    
   # =====================================================
# AI HEALTH & PREDICTION TAB
# =====================================================

def show_ai_health():

    analytics_data = st.session_state.server_data
    prediction = st.session_state.server_prediction
    alert_list = st.session_state.server_alerts

    st.subheader(" AI Health & Prediction")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "❤️ Health Score",
            f"{analytics_data['health_score']}/100"
        )

    with c2:
        st.metric(
            "📈 Trend",
            analytics_data["trend"]
        )

    with c3:
        st.metric(
            "⚠ Failure Probability",
            f"{prediction['failure_probability']}%"
        )

    with c4:
        st.metric(
            "🎯 Confidence",
            f"{prediction['confidence']}%"
        )

    st.markdown("---")

    status = analytics_data["health_status"]

    if status == "Excellent":
        st.success("🟢 Excellent Health")

    elif status == "Good":
        st.info("🔵 Good Health")

    elif status == "Warning":
        st.warning("🟡 Warning")

    else:
        st.error("🔴 Critical")

    st.markdown("---")

    left, right = st.columns([2, 1])

    with left:

        st.subheader(" AI Diagnosis")

        st.info(
            prediction["diagnosis"]
        )

        st.subheader(" Recommendation")

        st.success(
            prediction["recommendation"]
        )

    with right:

        st.subheader(" Active Alerts")

        for alert in alert_list:

            if alert["level"] == "CRITICAL":

                st.error(
                    f"🔴 {alert['title']}\n\n{alert['message']}"
                )

            elif alert["level"] == "WARNING":

                st.warning(
                    f"🟠 {alert['title']}\n\n{alert['message']}"
                )

            else:

                st.success(
                    f"🟢 {alert['title']}\n\n{alert['message']}"
                )
    # ==========================================
    # Health Summary
    # ==========================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(

            "❤️ Health Score",

            f'{analytics_data["health_score"]}/100'

        )

    with col2:

        st.metric(

            "📈 Trend",

            analytics_data["trend"]

        )

    with col3:

        st.metric(

            "⚠ Failure Probability",

            f'{prediction["failure_probability"]}%'

        )

    with col4:

        st.metric(

            "🎯 Confidence",

            f'{prediction["confidence"]}%'

        )

    st.divider()

    # ==========================================
    # Status
    # ==========================================

    status = analytics_data["health_status"]

    if status == "Excellent":

        st.success(f"🟢 Overall Health : {status}")

    elif status == "Good":

        st.info(f"🔵 Overall Health : {status}")

    elif status == "Warning":

        st.warning(f"🟡 Overall Health : {status}")

    else:

        st.error(f"🔴 Overall Health : {status}")

    st.divider()

    # ==========================================
    # AI Diagnosis
    # ==========================================

    st.subheader(" AI Diagnosis")

    st.info(

        prediction["diagnosis"]

    )

    # ==========================================
    # Recommendation
    # ==========================================

    st.subheader(" Recommendation")

    st.success(

        prediction["recommendation"]

    )

    st.divider()

    # ==========================================
    # Active Alerts
    # ==========================================

    st.subheader(" Active Alerts")

    for alert in alert_list:

        level = alert["level"]

        title = alert["title"]

        message = alert["message"]

        if level == "CRITICAL":

            st.error(

                f"🔴 {title}\n\n{message}"

            )

        elif level == "WARNING":

            st.warning(

                f"🟠 {title}\n\n{message}"

            )

        else:

            st.success(

                f"🟢 {title}\n\n{message}"

            )       
            
import requests


def show_thingspeak():

    st.subheader(" External Data")

    st.caption("Live sensor data from ThingSpeak")

    CHANNEL_ID = "3426883"
    READ_API_KEY = "8XZ1WL6NHYO31JCT"

    url = (
        f"https://api.thingspeak.com/channels/"
        f"{CHANNEL_ID}/feeds/last.json"
        f"?api_key={READ_API_KEY}"
    )

    try:

        response = requests.get(url, timeout=5)

        data = response.json()

        field1 = data.get("field1", "N/A")
        field2 = data.get("field2", "N/A")
        field3 = data.get("field3", "N/A")
        field4 = data.get("field4", "N/A")
        field5 = data.get("field5", "N/A") 
         
        st.success("Connected to ThingSpeak")

        col1, col2 = st.columns(2)


        with col1:
         st.metric("Temperature (°C)", field1)
         st.metric("Humidity (%)", field2)
         st.metric("Gas Sensor", field3)

        with col2:
         st.metric("Digital Vibration", field4)
         st.metric("Analog Vibration", field5)

        st.markdown("---")

        st.write("**Last Updated:**", data.get("created_at"))

    except Exception as e:

        st.error(f"Unable to fetch ThingSpeak data.\n\n{e}")
        
        
         # =====================================================
# MAIN DASHBOARD
# =====================================================

def show_server_dashboard():

    # Collect ONE analytics snapshot
    analytics_data = analytics.get_analytics()

    # Store analytics first
    st.session_state.server_data = analytics_data

    # Generate prediction
    prediction = predictor.predict()

    st.session_state.server_prediction = prediction

    # Generate alerts
    alert_list = alerts.run()

    st.session_state.server_alerts = alert_list
    
    # ==========================================
# Sidebar Status
# ==========================================
    st.sidebar.markdown("---")

    if analytics_data:

     st.sidebar.success("🟢 Server Connected")

    else:

     st.sidebar.error("🔴 Server Offline")

     st.sidebar.markdown("---")



    # ---------------- Header ----------------

    show_header()

    show_summary()

    # ---------------- Tabs ----------------

    tab1, tab2, tab3, tab4 = create_tabs()

    with tab1:

        show_live_monitoring()

    with tab2:

        show_device_information()

    with tab3:

        show_ai_health()
        
    with tab4:

        show_thingspeak()
        
