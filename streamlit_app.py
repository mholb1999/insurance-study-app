# streamlit_app.py
import streamlit as st
import pandas as pd
import json

# Page config optimized for mobile viewing
st.set_page_config(page_title="Hound Hub", page_icon="🐾", layout="centered")

st.title("🐾 Hound Hub")
st.markdown("### Real-Time Asset Tracking")

# Technical Constraint: Utilizing st.connection for stateful MQTT
# This expects your secrets to be in Streamlit Cloud's secret manager (mirroring your config.yaml)
try:
    mqtt_conn = st.connection("mqtt", type="mqtt", **st.secrets["mqtt"])
    # Subscribe to the GPS and Alert topics
    gps_data = mqtt_conn.subscribe("churchtech/dog/gps")
    alert_status = mqtt_conn.subscribe("churchtech/dog/alert")
except Exception as e:
    st.error(f"Failed to connect to the MQTT Broker: {e}")
    st.stop()

# --- Dashboard UI ---
st.divider()

col1, col2 = st.columns(2)

with col1:
    st.metric(label="Status", value="SECURE" if alert_status != "BREACH" else "BREACH", delta="Normal" if alert_status != "BREACH" else "-WARNING", delta_color="inverse")

with col2:
    # Assuming GPS payload is JSON like {"lat": 42.3314, "lon": -83.0458, "battery": 88}
    try:
        if gps_data:
            gps_dict = json.loads(gps_data)
            st.metric(label="Collar Battery", value=f"{gps_dict.get('battery', '--')}%")
    except:
        st.metric(label="Collar Battery", value="Offline")

# --- Map Rendering ---
st.subheader("Last Known Location")
if gps_data:
    try:
        gps_dict = json.loads(gps_data)
        df = pd.DataFrame([{"lat": gps_dict['lat'], "lon": gps_dict['lon']}])
        st.map(df, zoom=16)
    except:
        st.info("Awaiting valid GPS telemetry from Pillar 1 worker...")
else:
    st.info("Waiting for data. Did the dog eat the tracker again?")
