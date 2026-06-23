import streamlit as st
import requests
import pandas as pd
import time

st.set_page_config(page_title="Device Health Monitor", layout="wide")
st.title("🖥️ Device Health Monitor")

DEVICES = ["AI Camera", "Drone", "IoT Gateway", "CPE"]

device = st.sidebar.selectbox("Select Device", DEVICES)

st.sidebar.markdown("---")
st.sidebar.subheader("🚨 All Alerts")
try:
    all_alerts = requests.get("http://127.0.0.1:8000/alerts").json()["alerts"]
    if all_alerts:
        for alert in reversed(all_alerts[-10:]):
            if alert["level"] == "CRITICAL":
                st.sidebar.error(f"🔴 {alert['message']}")
            else:
                st.sidebar.warning(f"🟡 {alert['message']}")
    else:
        st.sidebar.success("✅ All devices healthy")
except:
    st.sidebar.info("No alerts yet")

# Fetch prediction
try:
    pred = requests.get(f"http://127.0.0.1:8000/predict/{device}").json()
except:
    pred = None

# Fetch readings
try:
    readings = requests.get(f"http://127.0.0.1:8000/readings/{device}").json()["readings"]
    df = pd.DataFrame(readings) if readings else None
except:
    df = None

# Health score banner
if pred and pred.get("health_score") is not None:
    score = pred["health_score"]
    status = pred["status"]

    if status == "HEALTHY":
        st.success(f"✅ {device} — {status} | Health Score: {score}/100")
    elif status == "AT RISK":
        st.warning(f"⚠️ {device} — {status} | Health Score: {score}/100")
    else:
        st.error(f"🔴 {device} — {status} | Health Score: {score}/100")

    st.info(f"🔮 Prediction: {pred['message']}")

    # Prediction metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Battery", f"{pred['current_battery']}%")
    col2.metric("Battery Health", f"{pred['battery_health']}%")
    col3.metric("Latency", f"{pred['current_latency_ms']} ms")
    col4.metric("Connection Stability", f"{pred['connection_stability']}%")

    st.markdown("---")
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Latency trend")
        trend = pred["latency_trend"]
        if "RISING FAST" in trend:
            st.error(f"📈 {trend}")
        elif "increasing" in trend:
            st.warning(f"📈 {trend}")
        else:
            st.success(f"📉 {trend}")
    with col_b:
        st.subheader("Time to failure")
        ttd = pred.get("time_to_die_mins")
        if ttd and ttd < 5:
            st.error(f"⚡ ~{ttd} minutes remaining")
        elif ttd:
            st.warning(f"🕐 ~{ttd} minutes remaining")
        else:
            st.success("♾️ Battery stable")

elif pred:
    st.info(f"📡 {pred['message']}")

# Charts
if df is not None and not df.empty:
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Battery over time")
        st.line_chart(df.set_index("timestamp")["battery"])
    with col2:
        st.subheader("Latency over time")
        st.line_chart(df.set_index("timestamp")["latency_ms"])
else:
    st.warning("No readings yet for this device")

time.sleep(10)
st.rerun()