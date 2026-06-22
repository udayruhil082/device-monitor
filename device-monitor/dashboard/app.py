import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Device Health Monitor", layout="wide")
st.title("Device Health Monitor")

device = st.sidebar.selectbox(
    "Select Device",
    ["AI Camera", "Drone", "IoT Gateway", "CPE"]
)

response = requests.get(f"http://127.0.0.1:8000/readings/{device}")
data = response.json()["readings"]

if data:
    df = pd.DataFrame(data)
    col1, col2, col3 = st.columns(3)
    col1.metric("Battery", f"{df['battery'].iloc[0]}%")
    col2.metric("Latency", f"{df['latency_ms'].iloc[0]} ms")
    col3.metric("Connected", "Yes" if df['connected'].iloc[0] else "No")
    st.subheader("Battery over time")
    st.line_chart(df.set_index("timestamp")["battery"])
else:
    st.warning("No data yet for this device")