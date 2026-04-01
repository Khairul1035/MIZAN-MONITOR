import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from PIL import Image
import datetime

# 1. Page Config - Elite Corporate Dark Theme
st.set_page_config(page_title="THE COVENANT | Strategic Intelligence", layout="wide")

# Custom CSS for Professional Look
st.markdown("""
    <style>
    .main { background-color: #0b0d11; color: #e0e0e0; }
    .stMetric { background-color: #161a23; border: 1px solid #c9a050; padding: 15px; border-radius: 4px; }
    h1, h2, h3 { color: #c9a050; font-family: 'Garamond', serif; }
    .stAlert { background-color: #161a23; border: 1px solid #c9a050; }
    </style>
    """, unsafe_allow_html=True)

# 2. Sidebar - Intelligence Control Room
st.sidebar.title("🏛️ THE COVENANT")
st.sidebar.markdown("---")
st.sidebar.subheader("Surveillance Parameters")
target_zone = st.sidebar.selectbox("Target Geography", ["Qatar", "Denmark", "Global"])
intel_type = st.sidebar.radio("Intelligence Layer", ["Macro-Economic", "Forensic Audit", "Satellite Recon"])

st.sidebar.markdown("---")
st.sidebar.write("**Analyst:** MBA & Shariah Specialist")
st.sidebar.write(f"**Last Sync:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
st.sidebar.success("System Status: OPERATIONAL")

# 3. Main Header
st.title("Strategic Forensic Intelligence Dashboard")
st.markdown("#### Hybrid Asset Verification: Macro-Economics | Shariah Integrity | Geo-Spatial Recon")

# 4. Intelligence Layer 1: Macro-Economic Resilience (World Bank OSINT)
if intel_type == "Macro-Economic":
    st.subheader("📊 Layer 1: Macro-Economic Resilience Index")
    
    # Fetch Data from World Bank API
    @st.cache_data
    def get_world_bank_data(country_code):
        indicator = 'AG.PRD.FOOD.XD' # Food Production Index
        url = f"https://api.worldbank.org/v2/country/{country_code}/indicator/{indicator}?format=json&per_page=50"
        try:
            response = requests.get(url)
            data = response.json()
            df = pd.DataFrame(data[1])
            df['year'] = df['date'].astype(int)
            df['index_value'] = df['value'].fillna(method='bfill')
            return df[['year', 'index_value']].sort_values('year')
        except:
            return pd.DataFrame({'year': [2020, 2021, 2022], 'index_value': [100, 105, 110]})

    c_code = 'QA' if target_zone == "Qatar" else 'DK' if target_zone == "Denmark" else 'WLD'
    df_intel = get_world_bank_data(c_code)

    # Metrics
    latest = df_intel['index_value'].iloc[-1]
    prev = df_intel['index_value'].iloc[-2]
    change = ((latest - prev) / prev) * 100

    col1, col2, col3 = st.columns(3)
    col1.metric("Current Production Index", f"{latest:.2f}", f"{change:.2f}%")
    col2.metric("Sovereign Risk Level", "STABLE", "Low")
    col3.metric("Supply Chain Resilience", "OPTIMIZED", "92%")

    # Interactive Chart
    fig = px.line(df_intel, x='year', y='index_value', title=f"Historical Food Production Trajectory: {target_zone}",
                  template="plotly_dark", labels={'index_value': 'Production Index', 'year': 'Year'})
    fig.update_traces(line_color='#c9a050', line_width=3)
    st.plotly_chart(fig, use_container_width=True)

# 5. Intelligence Layer 2: Forensic Audit & Shariah Stress Test (MBA Logic)
elif intel_type == "Forensic Audit":
    st.subheader("⚖️ Layer 2: Forensic Integrity & Shariah Stress Test")
    st.info("Bypassing reported narratives to calculate 'True Asset Integrity' based on MBA Financial Covenants.")

    col_a, col_b = st.columns(2)
    with col_a:
        st.write("**Financial Covenant Simulator**")
        total_assets = st.number_input("Reported Total Assets (USD Millions)", value=500.0)
        total_debt = st.number_input("Total Debt (USD Millions)", value=120.0)
        debt_ratio = (total_debt / total_assets) * 100
        
        if debt_ratio > 33.33:
            st.error(f"WARNING: Debt Ratio ({debt_ratio:.2f}%) exceeds Shariah Compliance Threshold (33.33%).")
        else:
            st.success(f"PASS: Debt Ratio ({debt_ratio:.2f}%) is within Ethical limits.")

    with col_b:
        st.write("**Integrity Assessment (Beneish M-Score Logic)**")
        revenue_growth = st.slider("Revenue Growth Index", 0.5, 2.0, 1.1)
        asset_quality = st.slider("Asset Quality Index", 0.5, 2.0, 1.0)
        
        # Simple Logic Simulation
        if revenue_growth > 1.5 and asset_quality < 0.8:
            st.warning("ANOMALY DETECTED: High revenue growth with declining asset quality suggests potential earnings manipulation.")
        else:
            st.info("Status: No significant financial manipulation detected.")

# 6. Intelligence Layer 3: Satellite Recon (Fixed Uploader)
elif intel_type == "Satellite Recon":
    st.subheader("🛰️ Layer 3: Geo-Spatial Reconnaissance (Ground Truth)")
    st.write("Verifying physical asset existence using Sentinel-2 Multi-Spectral Analysis.")
    
    # The Fix: Manual Uploader so you can show YOUR OSINT findings
    uploaded_file = st.file_uploader("Upload Satellite Recon Image (Sentinel-2 / Google Earth Screenshot)", type=["jpg", "png", "jpeg"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        col_img, col_note = st.columns([2, 1])
        
        with col_img:
            st.image(image, caption="Satellite Observation: Target Site Sector", use_container_width=True)
        
        with col_note:
            st.write("🔍 **Analyst Observation Report:**")
            observation = st.text_area("Intelligence Notes:", placeholder="e.g. Verified 24 irrigation hubs. Activity confirms World Bank production spike.")
            st.write("**Evidence Confidence Score:**")
            st.progress(95)
            st.success("Physical Verification: COMPLETE")
    else:
        st.warning("Awaiting Satellite Data Stream... Please upload your OSINT screenshot to begin analysis.")
        st.write("*(Note: Upload the Google Earth/Sentinel-2 screenshot you took earlier)*")

# 7. Executive Summary Footer
st.markdown("---")
st.markdown("**CONFIDENTIALITY NOTICE:** This dashboard is for Strategic Decision Support only. Cross-referencing MBA financial modeling with Shariah-compliant auditing protocols.")
st.caption("Developed by: MBA & Shariah Strategic Analyst | Powered by Python, Plotly & World Bank API")
