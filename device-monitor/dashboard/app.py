import streamlit as st
import requests
import pandas as pd
import time

st.set_page_config(page_title="Device Health Monitor", layout="wide")
st.title("🖥️ Device Health Monitor")

device = st.sidebar.selectbox(
    "Select Device",
    ["AI Camera", "Drone", "IoT Gateway", "CPE"]
)

st.sidebar.markdown("---")
st.sidebar.subheader("All Alerts")

# Fetch alerts
try:
    alert_response = requests.get("http://127.0.0.1:8000/alerts")
    all_alerts = alert_response.json()["alerts"]
    if all_alerts:
        for alert in reversed(all_alerts[-10:]):
            if alert["level"] == "CRITICAL":
                st.sidebar.error(f"🔴 {alert['message']}")
            else:
                st.sidebar.warning(f"🟡 {alert['message']}")
    else:
        st.sidebar.success("All devices healthy")
except:
    st.sidebar.info("No alerts yet")

# Fetch device readings
response = requests.get(f"http://127.0.0.1:8000/readings/{device}")
data = response.json()["readings"]

if data:
    df = pd.DataFrame(data)

    # Metrics row
    col1, col2, col3 = st.columns(3)
    battery = df['battery'].iloc[0]
    latency = df['latency_ms'].iloc[0]
    connected = df['connected'].iloc[0]

    col1.metric("Battery", f"{battery}%")
    col2.metric("Latency", f"{latency} ms")
    col3.metric("Connected", "Yes" if connected else "No")

    # Alert banners
    if not connected:
        st.error(f"🔴 CRITICAL: {device} is disconnected!")
    if battery < 20:
        st.error(f"🔴 CRITICAL: Battery at {battery}% — charge immediately!")
    elif battery < 50:
        st.warning(f"🟡 WARNING: Battery low at {battery}%")
    else:
        st.success(f"✅ {device} is healthy")

    if latency > 200:
        st.error(f"🔴 CRITICAL: Latency at {latency}ms!")
    elif latency > 100:
        st.warning(f"🟡 WARNING: Latency high at {latency}ms")

    # Charts
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Battery over time")
        st.line_chart(df.set_index("timestamp")["battery"])
    with col_b:
        st.subheader("Latency over time")
        st.line_chart(df.set_index("timestamp")["latency_ms"])

else:
    st.warning("No data yet for this device")

# Auto refresh every 10 seconds
time.sleep(10)
st.rerun()