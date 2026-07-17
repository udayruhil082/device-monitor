import streamlit as st
from datetime import datetime

from backend.gateway_service import gateway
from backend.gateway_analytics import analytics
from backend.gateway_predictor import predictor
from backend.gateway_alerts import alerts


# =====================================================
# HEADER
# =====================================================

def show_header():

    st.title(" IoT Gateway Health Monitoring")

    st.caption(
        "Real-time monitoring, AI analytics and predictive maintenance for the IoT Gateway."
    )

    st.divider()


# =====================================================
# SUMMARY
# =====================================================

def show_summary(data, analytics_data, prediction):

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(
            "❤️ Health Score",
            f"{analytics_data['health_score']}/100"
        )

    with c2:

        st.metric(
            "🖥 CPU Usage",
            f"{data['cpu']['usage']} %"
        )

    with c3:

        st.metric(
            "💾 RAM Usage",
            f"{data['memory']['usage_percent']} %"
        )

    with c4:

        st.metric(
            "⚠ Failure Risk",
            prediction["risk"]
        )

    st.divider()


# =====================================================
# CREATE TABS
# =====================================================

def create_tabs():

    return st.tabs(
        [
            " Live Monitoring",
            " Gateway Information",
            " Network & Connectivity",
            " AI Health & Prediction"
        ]
    )


# =====================================================
# LIVE MONITORING
# =====================================================

def show_live_monitoring(data):

    st.subheader(" Live Gateway Metrics")

    col1, col2 = st.columns(2)

    with col1:

        cpu = data["cpu"]["usage"]

        st.metric(
            "CPU Usage",
            f"{cpu} %"
        )

        st.progress(
            min(int(cpu), 100)
        )

    with col2:

        ram = data["memory"]["usage_percent"]

        st.metric(
            "Memory Usage",
            f"{ram} %"
        )

        st.progress(
            min(int(ram), 100)
        )

    st.divider()

    c1, c2, c3 = st.columns(3)

    with c1:

        uptime = round(
            data["system"]["uptime"] / 3600,
            1
        )

        st.metric(
            "Uptime",
            f"{uptime} Hr"
        )

    with c2:

        load = round(
            data["system"]["load"][0] / 65535,
            2
        )

        st.metric(
            "Load Average",
            load
        )

    with c3:

        if data["lan"]["up"]:

            st.metric(
                "Gateway Status",
                "🟢 Online"
            )

        else:

            st.metric(
                "Gateway Status",
                "🔴 Offline"
            )

    st.success("Gateway monitoring is active.")

    st.divider()
    
    # =====================================================
# GATEWAY INFORMATION
# =====================================================

def show_gateway_information(data):

    board = data["board"]

    release = board["release"]

    st.subheader(" Gateway Information")

    col1, col2 = st.columns(2)

    with col1:

        st.info(f"""
### General Information

**Hostname:** {board.get("hostname","N/A")}

**Model:** {board.get("model","N/A")}

**Board:** {board.get("board_name","N/A")}

**System:** {board.get("system","N/A")}
""")

    with col2:

        st.info(f"""
### Software

**Distribution:** {release.get("distribution","N/A")}

**Version:** {release.get("version","N/A")}

**Kernel:** {board.get("kernel","N/A")}

**Target:** {release.get("target","N/A")}
""")

    st.divider()


# =====================================================
# NETWORK & CONNECTIVITY
# =====================================================

def show_network(data):

    st.subheader(" Network & Connectivity")

    lan = data.get("lan", {})

    airtel = data.get("airtel", {})

    wifi = data.get("wifi", {})

    # -----------------------------
    # Safe Values
    # -----------------------------

    lan_ip = "Not Available"

    subnet = "N/A"

    if lan.get("ipv4-address"):

        lan_ip = lan["ipv4-address"][0].get(
            "address",
            "Not Available"
        )

        subnet = lan["ipv4-address"][0].get(
            "mask",
            "N/A"
        )

    wan_ip = "10.45.0.6"

    if airtel.get("ipv4-address"):

     wan_ip = airtel["ipv4-address"][0].get(
        "address",
        wan_ip
    )

    gateway_ip = "10.45.0.1"

    if airtel.get("route"):

     gateway_ip = airtel["route"][0].get(
        "nexthop",
        gateway_ip
    )

    dns = "8.8.8.8"

    if airtel.get("dns-server"):

     dns = ", ".join(
        airtel["dns-server"]
    )

    # -----------------------------
    # Modem Status
    # -----------------------------

    if airtel.get("available"):

      modem_status = "🟢 Available"

    else:

     modem_status = "🔴 Unavailable"

    # -----------------------------
    # Cards
    # -----------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.info(f"""
###  LAN

**Status:** {"🟢 Connected" if lan.get("up") else "🔴 Offline"}

**Protocol:** {lan.get("proto","N/A")}

**IP Address:** {lan_ip}

**Subnet:** /{subnet}
""")

    with col2:

        st.info(f"""
###  5G Interface

**Status:** {modem_status}

**Protocol:** {airtel.get("proto","N/A")}

**IP Address:** {wan_ip}

**Gateway:** {gateway_ip}

**DNS:** {dns}
""")

    st.divider()

    st.subheader(" WiFi Information")

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "SSID",
            wifi.get("ssid","N/A")
        )

    with c2:

        st.metric(
            "Channel",
            wifi.get("channel","N/A")
        )

    with c3:

        st.metric(
            "Encryption",
            wifi.get("encryption","N/A")
        )

    st.success("Network information collected successfully.")

    st.divider()
    
# =====================================================
# AI HEALTH & PREDICTION
# =====================================================

def show_ai_health(analytics_data, prediction, alert_list):

    st.subheader(" AI Device Health Analysis")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Health Score", f"{analytics_data['health_score']}/100")

    with col2:
        st.metric("Health Status", analytics_data["health_status"])

    with col3:
        st.metric("Trend", analytics_data["trend"])

    st.divider()

    # -----------------------------
    # Prediction
    # -----------------------------

    st.subheader(" Predictive Maintenance")

    c1, c2 = st.columns(2)

    with c1:
        st.metric("Failure Risk", prediction["risk"])

    with c2:
        st.metric(
            "Failure Probability",
            f"{prediction['failure_probability']}%"
        )

    st.info(prediction["recommendation"])

    # -----------------------------
    # AI Interpretation
    # -----------------------------

    score = analytics_data["health_score"]
    status = analytics_data["health_status"]
    risk = prediction["risk"]

    if score >= 90:
        score_range = "90–100"
    elif score >= 75:
        score_range = "75–89"
    elif score >= 60:
        score_range = "60–74"
    else:
        score_range = "Below 60"

    st.success(
        f"""
###  AI Health Interpretation

The gateway currently has a **Health Score of {score}/100**, which falls in the **{score_range}** range.

- **Health Status:** {status}
- **Predicted Failure Risk:** {risk}

**Reason:**
The AI health engine analyzes CPU usage, memory utilization, LAN connectivity, and 5G interface status to compute an overall health score. Based on this score, it predicts the current device health and estimates the likelihood of future failures.

**Recommendation:**
{prediction["recommendation"]}
"""
    )

    st.divider()

    # -----------------------------
    # Alerts
    # -----------------------------

    st.subheader(" Active Alerts")

    if not alert_list:

        st.success("✅ No active alerts.")

    else:

        for alert in alert_list:

            severity = alert.get("severity", "LOW").upper()
            title = alert.get("title", "")
            message = alert.get("message", "")
            action = alert.get("action", "")
            if severity == "HIGH":

                st.error(
                   f"""
                 🔴 **{title}**

                 **Issue**
                   {message}

                 **Recommended Action**
                  {action}
                   """
                  )

            elif severity == "MEDIUM":

                st.warning(
                 f"""
                 🟡 **{title}**

                 **Issue**
                 {message}

                 **Recommended Action**
                 {action}
                 """
                 )

            else:

                st.success(
                 f"""
                 🟢 **{title}**

                 **Status**
                 {message}

                  **Action**
                 {action}
                 """
                 )

    st.divider()

# =====================================================
# MAIN DASHBOARD
# =====================================================

def show_gateway_dashboard():

    # Fetch Data
    data = gateway.get_all_data()

    analytics_data = analytics.get_analytics()

    prediction = predictor.predict()

    alert_list = alerts.get_alerts()

    # Header
    show_header()

    # Last Updated
    st.caption(f"Last Updated: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")

    # Summary Cards
    show_summary(
        data,
        analytics_data,
        prediction
    )

    # Tabs
    tab1, tab2, tab3, tab4 = create_tabs()

    with tab1:
        show_live_monitoring(data)

    with tab2:
        show_gateway_information(data)

    with tab3:
        show_network(data)

    with tab4:
        show_ai_health(
            analytics_data,
            prediction,
            alert_list
        )


