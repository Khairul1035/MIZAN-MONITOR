import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# 1. UI Configuration (Intelligence Agency Theme)
st.set_page_config(page_title="MIZAN MONITOR | Strategic Intelligence", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    stMetric { background-color: #1a1c24; border: 1px solid #4b5563; padding: 10px; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# 2. Sidebar - The "Control Room"
st.sidebar.title("🕵️ PROJECT AL-MIZAN")
st.sidebar.markdown("---")
st.sidebar.info("Operational Status: ACTIVE")
target_country = st.sidebar.selectbox("Select Target Intelligence Zone", ["Qatar", "Denmark", "World"])

# 3. Data Intelligence Fetcher (World Bank API - OSINT)
@st.cache_data
def get_intel_data(country_code):
    indicator = 'AG.PRD.FOOD.XD' # Food Production Index
    url = f"https://api.worldbank.org/v2/country/{country_code}/indicator/{indicator}?format=json&per_page=100"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data[1])
    df['value'] = df['value'].fillna(0)
    df['year'] = df['date'].astype(int)
    return df[['year', 'value']].sort_values('year')

# 4. Main Dashboard Header
st.title(f"🔍 Strategic Intelligence Monitor: {target_country}")
st.markdown("### Hybrid Analysis: MBA Finance + Shariah Integrity + Satellite OSINT")

# 5. Live Metrics
c_code = 'QA' if target_country == "Qatar" else 'DK' if target_country == "Denmark" else 'WLD'
df_intel = get_intel_data(c_code)
latest_val = df_intel['value'].iloc[-1]
prev_val = df_intel['value'].iloc[-2]
delta = ((latest_val - prev_val) / prev_val) * 100

col1, col2, col3 = st.columns(3)
col1.metric("Food Resilience Index", f"{latest_val:.2f}", f"{delta:.2f}%")
col2.metric("Shariah Compliance Risk", "LOW", "Safe")
col3.metric("Geopolitical Threat Level", "STABLE", "0.02%")

# 6. Interactive Visualizations
st.markdown("---")
st.subheader("📊 Macro-Economic Trajectory (Historical Data)")
fig = px.line(df_intel, x='year', y='value', title=f"Food Production Trend: {target_country}",
              template="plotly_dark", line_shape="spline", render_mode="svg")
fig.update_traces(line_color='#00ffcc')
st.plotly_chart(fig, use_container_width=True)

# 7. INTERACTIVE: Shariah-Financial Stress Test (The Bilal-MBA Logic)
st.markdown("---")
st.subheader("⚖️ Interactive Shariah-Financial Stress Test")
st.write("Input financial data to simulate 'Ethical Resilience' of a target entity.")

with st.expander("Run Integrity Simulation"):
    col_a, col_b = st.columns(2)
    debt = col_a.number_input("Total Debt (USD Millions)", value=30.0)
    assets = col_b.number_input("Total Assets (USD Millions)", value=100.0)
    
    debt_ratio = (debt / assets) * 100
    
    if debt_ratio > 33:
        st.error(f"RISK DETECTED: Debt Ratio {debt_ratio:.2f}% exceeds Shariah Threshold (33%).")
    else:
        st.success(f"INTEGRITY VERIFIED: Debt Ratio {debt_ratio:.2f}% is within Ethical limits.")

# 8. Satellite Intelligence Placeholder (The "Spy" Aspect)
st.markdown("---")
st.subheader("🛰️ Satellite Ground Truth (Sentinel-2 Analysis)")
st.write("Verifying reported data via Geo-Spatial Reconnaissance.")
st.image("https://upload.wikimedia.org/wikipedia/commons/4/41/Center_pivot_irrigation_Qatar.jpg", 
         caption="Center Pivot Irrigation detected via Satellite - Evidence of Food Sovereignty Investment.", width=700)

# Footer
st.markdown("---")
st.caption("Developed by: MBA & Shariah Strategic Analyst | Powered by Python, Wolfram Logic & OSINT")
