# dashboard.py

import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from datetime import datetime
import io
import os

# Database path
DB_PATH = "data/violations.db"

# ── Page Setup ────────────────────────────────────────
st.set_page_config(
    page_title="Helmet Detection Dashboard",
    page_icon="🪖",
    layout="wide"
)

st.title("🪖 Smart Helmet Detection — Live Dashboard")
st.markdown("---")

# ── Load Data from Database ───────────────────────────
def load_data():
    if not os.path.exists(DB_PATH):
        return pd.DataFrame()
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(
        "SELECT * FROM violations ORDER BY id DESC",
        conn
    )
    conn.close()
    return df

# ── Sidebar Settings ──────────────────────────────────
st.sidebar.title("Settings")
refresh = st.sidebar.slider("Auto Refresh (seconds)", 5, 60, 10)
st.sidebar.info(f"Dashboard refreshes every {refresh} seconds")

# Load data
df = load_data()

# ── Show Stats ────────────────────────────────────────
st.subheader("📊 Live Statistics")

if df.empty:
    st.warning("No data found. Please run main.py first.")
else:
    latest = df.iloc[0]

    # Top 3 counters
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="🚗 Total Vehicles",
            value=int(latest['total_vehicles'])
        )

    with col2:
        st.metric(
            label="✅ Safe (With Helmet)",
            value=int(latest['safe_count'])
        )

    with col3:
        st.metric(
            label="❌ Violations (No Helmet)",
            value=int(latest['violation_count'])
        )

    st.markdown("---")

    # ── Bar Chart ─────────────────────────────────────
    st.subheader("📈 Violation Trend")

    chart_df = df[['time', 'violation_count', 'safe_count']].tail(20)

    fig = px.bar(
        chart_df,
        x='time',
        y=['safe_count', 'violation_count'],
        barmode='group',
        labels={'value': 'Count', 'time': 'Time'},
        color_discrete_map={
            'safe_count': '#28a745',
            'violation_count': '#dc3545'
        },
        title="Last 20 Entries — Safe vs Violations"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ── Data Table ────────────────────────────────────
    st.subheader("📋 All Recorded Events")
    st.dataframe(df, use_container_width=True)

    st.markdown("---")

    # ── Snapshot Preview ──────────────────────────────
    st.subheader("📷 Latest Violation Snapshot")
    last_image = df[df['image_path'] != '']['image_path'].head(1)

    if not last_image.empty and os.path.exists(last_image.values[0]):
        st.image(last_image.values[0], caption="Latest Violation", width=400)
    else:
        st.info("No snapshot available yet.")

    st.markdown("---")

    # ── Download Excel Report ─────────────────────────
    st.subheader("⬇️ Download Report")

    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Violations')

    st.download_button(
        label="📥 Download Excel Report",
        data=buffer.getvalue(),
        file_name=f"report_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
        mime="application/vnd.ms-excel"
    )

# ── Auto Refresh ──────────────────────────────────────
import time
time.sleep(refresh)
st.rerun()