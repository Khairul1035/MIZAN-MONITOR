import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from PIL import Image
import datetime

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="THE COVENANT | Strategic Intelligence Command",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# STABLE READABLE CSS FOR STREAMLIT
# =========================================================
st.markdown(
    """
    <style>
    :root {
        --bg: #0b1220;
        --panel: #111a2a;
        --panel-2: #162235;
        --border: #2d3b52;
        --text: #f3f6fb;
        --muted: #b8c3d3;
        --gold: #d6b25e;
        --success: #123628;
    }

    html, body, [class*="css"] {
        font-family: "Inter", "Segoe UI", sans-serif;
    }

    .stApp {
        background: linear-gradient(180deg, #08111d 0%, #0b1220 55%, #0f1828 100%);
        color: var(--text);
    }

    .block-container {
        max-width: 1450px;
        padding-top: 1.25rem;
        padding-bottom: 2rem;
    }

    h1, h2, h3, h4, h5, h6, p, span, label, li, div {
        color: var(--text);
    }

    h1 {
        color: #ffffff !important;
        font-weight: 800 !important;
        letter-spacing: 0.01em;
    }

    h2, h3 {
        color: #ffffff !important;
        font-weight: 700 !important;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #09111e 0%, #0d1730 100%);
        border-right: 1px solid rgba(214, 178, 94, 0.12);
    }

    section[data-testid="stSidebar"] * {
        color: var(--text) !important;
    }

    /* Hero */
    .hero-wrap {
        background: linear-gradient(90deg, rgba(17,26,42,0.98) 0%, rgba(13,21,32,0.98) 100%);
        border: 1px solid rgba(214, 178, 94, 0.16);
        border-radius: 18px;
        padding: 1.15rem;
        margin-bottom: 1rem;
        box-shadow: 0 10px 24px rgba(0, 0, 0, 0.18);
    }

    .hero-grid {
        display: grid;
        grid-template-columns: 90px 1fr;
        gap: 1rem;
        align-items: center;
    }

    .logo-box {
        width: 80px;
        height: 80px;
        border-radius: 16px;
        background: linear-gradient(180deg, #d8ba72 0%, #b89343 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        color: #0d1520 !important;
        font-size: 1.4rem;
        font-weight: 900;
    }

    .eyebrow {
        font-size: 0.78rem;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #9fb0c8 !important;
        margin-bottom: 0.25rem;
        font-weight: 700;
    }

    .hero-title {
        font-size: 1.9rem;
        font-weight: 900;
        color: #ffffff !important;
        margin-bottom: 0.18rem;
    }

    .hero-subtitle {
        font-size: 1rem;
        color: #d5deea !important;
        line-height: 1.55;
    }

    /* Inputs - force readable text */
    .stSelectbox label,
    .stRadio label,
    .stTextArea label,
    .stFileUploader label,
    .stNumberInput label,
    .stSlider label,
    .stTextInput label {
        color: #f7f9fc !important;
        font-weight: 700 !important;
    }

    div[data-baseweb="select"] > div {
        background: #132033 !important;
        border: 1px solid var(--border) !important;
        border-radius: 10px !important;
        min-height: 44px !important;
    }

    div[data-baseweb="select"] span,
    div[data-baseweb="select"] input,
    div[data-baseweb="select"] svg,
    div[data-baseweb="select"] div {
        color: #ffffff !important;
        fill: #ffffff !important;
    }

    /* Dropdown menu */
    ul[role="listbox"] {
        background: #132033 !important;
        border: 1px solid var(--border) !important;
    }

    ul[role="listbox"] li,
    ul[role="listbox"] div,
    ul[role="listbox"] span {
        background: #132033 !important;
        color: #ffffff !important;
    }

    div[role="radiogroup"] label {
        background: #132033 !important;
        border: 1px solid var(--border) !important;
        padding: 0.42rem 0.72rem;
        border-radius: 8px;
        margin-bottom: 0.35rem;
    }

    .stNumberInput input,
    .stTextInput input,
    .stTextArea textarea {
        background: #132033 !important;
        color: #ffffff !important;
        border: 1px solid var(--border) !important;
        border-radius: 10px !important;
    }

    /* File uploader */
    [data-testid="stFileUploaderDropzone"] {
        background: #132033 !important;
        border: 1px dashed #52627b !important;
        border-radius: 12px !important;
    }

    [data-testid="stFileUploaderDropzone"] * {
        color: #ffffff !important;
    }

    /* Metrics */
    div[data-testid="metric-container"] {
        background: linear-gradient(180deg, #111a2a 0%, #0f1827 100%);
        border: 1px solid rgba(214, 178, 94, 0.20);
        padding: 1rem;
        border-radius: 14px;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.20);
    }

    div[data-testid="metric-container"] label {
        color: var(--muted) !important;
        font-weight: 700 !important;
        font-size: 0.90rem !important;
    }

    div[data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-weight: 800 !important;
    }

    div[data-testid="metric-container"] [data-testid="stMetricDelta"] {
        color: var(--gold) !important;
        font-weight: 700 !important;
    }

    /* Alerts */
    div[data-testid="stAlert"] {
        border-radius: 12px !important;
        border: 1px solid rgba(214, 178, 94, 0.14) !important;
    }

    div[data-testid="stAlert"] * {
        color: #ffffff !important;
    }

    /* Buttons */
    .stButton > button,
    .stDownloadButton > button {
        background: linear-gradient(180deg, #d8ba72 0%, #b89343 100%);
        color: #0d1520 !important;
        border: none;
        border-radius: 10px;
        font-weight: 800;
        padding: 0.56rem 1rem;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover {
        filter: brightness(1.04);
    }

    div[data-testid="stProgressBar"] > div > div {
        background-color: var(--gold) !important;
    }

    .score-card {
        background: linear-gradient(180deg, #121d2e 0%, #0f1724 100%);
        border: 1px solid rgba(214, 178, 94, 0.14);
        border-radius: 14px;
        padding: 1rem;
        text-align: center;
        min-height: 120px;
    }

    .score-label {
        color: var(--muted) !important;
        font-size: 0.82rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-weight: 700;
        margin-bottom: 0.4rem;
    }

    .score-value {
        font-size: 2rem;
        font-weight: 900;
        color: #ffffff !important;
        margin-bottom: 0.2rem;
    }

    .score-band {
        color: var(--gold) !important;
        font-weight: 700;
        font-size: 0.92rem;
    }

    .brief-box {
        background: linear-gradient(180deg, #121d2e 0%, #0f1724 100%);
        border: 1px solid rgba(214, 178, 94, 0.14);
        border-radius: 14px;
        padding: 1rem;
        min-height: 250px;
    }

    .stCaption, .small-note {
        color: #9fb0c8 !important;
    }

    hr {
        border: none;
        border-top: 1px solid rgba(214, 178, 94, 0.14);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# HELPERS
# =========================================================
@st.cache_data(show_spinner=False)
def get_world_bank_data(country_code: str) -> pd.DataFrame:
    indicator = "AG.PRD.FOOD.XD"
    url = f"https://api.worldbank.org/v2/country/{country_code}/indicator/{indicator}?format=json&per_page=50"
    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        payload = response.json()
        if not isinstance(payload, list) or len(payload) < 2 or payload[1] is None:
            raise ValueError("Unexpected API structure")
        df = pd.DataFrame(payload[1])
        if df.empty:
            raise ValueError("Empty dataset")
        df["year"] = pd.to_numeric(df["date"], errors="coerce")
        df["index_value"] = pd.to_numeric(df["value"], errors="coerce")
        df = df.dropna(subset=["year"]).sort_values("year")
        df["index_value"] = df["index_value"].bfill().ffill()
        df = df.dropna(subset=["index_value"])
        return df[["year", "index_value"]]
    except Exception:
        return pd.DataFrame({"year": [2020, 2021, 2022, 2023], "index_value": [100, 104, 108, 111]})


def risk_band(score: int) -> str:
    if score >= 75:
        return "High Priority"
    if score >= 50:
        return "Moderate"
    if score >= 25:
        return "Guarded"
    return "Controlled"


def render_logo_area():
    st.markdown(
        """
        <div class="hero-wrap">
            <div class="hero-grid">
                <div class="logo-box">TC</div>
                <div>
                    <div class="eyebrow">Strategic Intelligence Command</div>
                    <div class="hero-title">THE COVENANT</div>
                    <div class="hero-subtitle">
                        Premium executive dashboard for macro surveillance, forensic integrity analysis,
                        geospatial verification, and board-level risk signalling.
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def corporate_line_chart(df: pd.DataFrame, zone: str):
    fig = px.line(
        df,
        x="year",
        y="index_value",
        markers=True,
        title=f"Food Production Trend | {zone}",
        labels={"year": "Year", "index_value": "Production Index"},
        template="plotly_dark",
    )
    fig.update_layout(
        paper_bgcolor="#0F1724",
        plot_bgcolor="#0F1724",
        font=dict(color="#E9EEF5", size=13),
        title_font=dict(size=20, color="#F5F7FB"),
        xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.06)", zeroline=False),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.06)", zeroline=False),
        margin=dict(l=20, r=20, t=60, b=20),
    )
    fig.update_traces(line=dict(width=3, color="#D6B25E"), marker=dict(size=7, color="#D6B25E"))
    st.plotly_chart(fig, use_container_width=True)


def dataframe_to_csv_bytes(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8")


def text_to_bytes(text: str) -> bytes:
    return text.encode("utf-8")


def generate_executive_brief(zone, intel_type, composite_score, macro_signal, forensic_signal, geo_signal, recommendation):
    now_stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    return f"""THE COVENANT | EXECUTIVE BRIEF
Generated: {now_stamp}
Target Geography: {zone}
Analytical Layer in Focus: {intel_type}

1. Executive Summary
The current dashboard assessment indicates a composite strategic risk score of {composite_score}/100, placing the target environment in the '{risk_band(composite_score)}' band.

2. Signal Overview
- Macro Signal: {macro_signal}
- Forensic Signal: {forensic_signal}
- Geospatial Signal: {geo_signal}

3. Recommended Action
{recommendation}
"""

# =========================================================
# SIDEBAR
# =========================================================
st.sidebar.markdown("## THE COVENANT")
st.sidebar.markdown("**Strategic Intelligence Command**")
st.sidebar.markdown("---")
st.sidebar.subheader("Operational Parameters")
target_zone = st.sidebar.selectbox("Target Geography", ["Qatar", "Denmark", "Global"])
intel_type = st.sidebar.radio("Analytical Layer", ["Macro-Economic", "Forensic Audit", "Satellite Recon"])
st.sidebar.markdown("---")
st.sidebar.subheader("Executive Controls")
risk_appetite = st.sidebar.selectbox("Risk Appetite", ["Conservative", "Balanced", "Elevated Alert"])
brief_mode = st.sidebar.selectbox("Briefing Format", ["Board Summary", "Analyst Review", "Investor Screening"])
st.sidebar.markdown("---")
st.sidebar.subheader("Analyst Desk")
st.sidebar.write("**Profile:** Strategic Finance & Integrity Analyst")
st.sidebar.write(f"**Last Synchronisation:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
st.sidebar.success("System Status: Operational")

# =========================================================
# HEADER
# =========================================================
render_logo_area()
st.title("Strategic Forensic Intelligence Dashboard")
st.markdown(
    "Integrated command environment for **economic monitoring**, **forensic screening**, "
    "**ground-truth verification**, and **export-ready executive reporting**."
)

# =========================================================
# DEFAULT STATE
# =========================================================
macro_score = 28
forensic_score = 24
geo_score = 18
macro_signal = "Macro data not yet interpreted."
forensic_signal = "Forensic screen not yet completed."
geo_signal = "No uploaded verification image yet."
recommendation = "Complete the selected analytical layer, review emerging signals, and escalate only where thresholds are breached."
export_df = pd.DataFrame()

# =========================================================
# MAIN LAYER
# =========================================================
if intel_type == "Macro-Economic":
    st.subheader("Macro-Economic Resilience Assessment")
    code_map = {"Qatar": "QA", "Denmark": "DK", "Global": "WLD"}
    df_intel = get_world_bank_data(code_map[target_zone])
    export_df = df_intel.copy()

    if len(df_intel) >= 2:
        latest = float(df_intel["index_value"].iloc[-1])
        prev = float(df_intel["index_value"].iloc[-2])
        change = ((latest - prev) / prev) * 100 if prev != 0 else 0.0
    else:
        latest = float(df_intel["index_value"].iloc[-1])
        change = 0.0

    if change >= 2:
        macro_score = 18
        macro_signal = f"Positive macro momentum observed, with the latest food production index at {latest:.2f} and a period-on-period change of {change:.2f}%."
    elif change >= 0:
        macro_score = 30
        macro_signal = f"Stable macro trajectory observed, with the latest food production index at {latest:.2f} and mild change of {change:.2f}%."
    else:
        macro_score = 52
        macro_signal = f"Macro caution flag: the latest food production index is {latest:.2f}, reflecting a decline of {abs(change):.2f}% from the prior observation."

    c1, c2, c3 = st.columns(3)
    c1.metric("Current Production Index", f"{latest:.2f}", f"{change:.2f}% vs prior period")
    c2.metric("Sovereign Risk Signal", "Stable" if macro_score < 40 else "Watchlist", risk_band(macro_score))
    c3.metric("Supply Chain Resilience", "92%" if macro_score < 40 else "74%", "External signal")
    corporate_line_chart(df_intel, target_zone)
    st.info("Interpretation: This layer provides an external macro signal for country screening, supply continuity monitoring, and executive risk scanning.")
    recommendation = "Maintain periodic macro monitoring, cross-check sector exposure, and integrate this signal with internal operational data before major capital or partnership decisions."

elif intel_type == "Forensic Audit":
    st.subheader("Forensic Integrity & Ethical Stress Test")
    st.info("This layer evaluates financial covenant pressure and anomaly signals to support preliminary integrity screening and escalation decisions.")
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("### Financial Covenant Review")
        total_assets = st.number_input("Reported Total Assets (USD millions)", min_value=1.0, value=500.0, step=10.0)
        total_debt = st.number_input("Total Debt (USD millions)", min_value=0.0, value=120.0, step=5.0)
        debt_ratio = (total_debt / total_assets) * 100 if total_assets else 0.0
        st.metric("Debt Ratio", f"{debt_ratio:.2f}%")
        if debt_ratio > 33.33:
            st.error(f"Risk Flag: Debt ratio of {debt_ratio:.2f}% exceeds the selected Shariah screening threshold.")
        else:
            st.success(f"Screening Result: Debt ratio of {debt_ratio:.2f}% remains within the selected threshold.")

    with col_b:
        st.markdown("### Earnings Integrity Screen")
        revenue_growth = st.slider("Revenue Growth Index", 0.50, 2.00, 1.10, 0.01)
        asset_quality = st.slider("Asset Quality Index", 0.50, 2.00, 1.00, 0.01)
        anomaly_score = 0
        if revenue_growth > 1.50:
            anomaly_score += 1
        if asset_quality < 0.80:
            anomaly_score += 1
        st.metric("Anomaly Score", f"{anomaly_score}/2")
        if anomaly_score == 2:
            st.warning("Elevated anomaly signal detected: rapid revenue growth combined with deteriorating asset quality may warrant deeper forensic review.")
        elif anomaly_score == 1:
            st.info("Moderate signal detected: one integrity indicator has moved outside the preferred range.")
        else:
            st.success("No material anomaly signal detected under the current assumptions.")

    forensic_score = 18
    forensic_score += 35 if debt_ratio > 33.33 else 18 if debt_ratio > 25 else 6
    forensic_score += 35 if anomaly_score == 2 else 18 if anomaly_score == 1 else 6
    forensic_score = min(forensic_score, 100)
    forensic_signal = f"Forensic screen indicates a debt ratio of {debt_ratio:.2f}% and anomaly score of {anomaly_score}/2, placing the case in the '{risk_band(forensic_score)}' band."
    export_df = pd.DataFrame({
        "metric": ["total_assets_usd_m", "total_debt_usd_m", "debt_ratio_pct", "revenue_growth_index", "asset_quality_index", "anomaly_score", "forensic_score"],
        "value": [total_assets, total_debt, round(debt_ratio, 2), revenue_growth, asset_quality, anomaly_score, forensic_score],
    })
    recommendation = "Escalate to enhanced due diligence where debt screening fails or anomaly patterns converge. Supplement this layer with document review, ratio trend analysis, and management explanations."

else:
    st.subheader("Geospatial Verification & Ground-Truth Review")
    st.write("Use this section to validate physical asset existence or observable activity through uploaded imagery and analyst notes.")
    uploaded_file = st.file_uploader("Upload verification image (JPG, PNG, JPEG)", type=["jpg", "png", "jpeg"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        col_img, col_note = st.columns([2, 1])
        with col_img:
            st.image(image, caption="Uploaded Verification Image", use_container_width=True)
        with col_note:
            st.markdown("### Analyst Observation")
            observation = st.text_area("Intelligence Notes", placeholder="Example: Verified multiple infrastructure clusters and active land-use patterns consistent with reported expansion.")
            confidence = st.slider("Evidence Confidence Score", 0, 100, 95)
            st.progress(confidence)
            if confidence >= 85:
                st.success("Assessment Status: High-confidence verification")
            elif confidence >= 60:
                st.info("Assessment Status: Moderate-confidence verification")
            else:
                st.warning("Assessment Status: Low-confidence verification")
        geo_score = 16 if confidence >= 85 else 36 if confidence >= 60 else 62
        geo_signal = f"Geospatial review completed with an evidence confidence score of {confidence}/100, indicating a '{risk_band(geo_score)}' verification posture."
        export_df = pd.DataFrame({"metric": ["uploaded_image_name", "confidence_score", "observation"], "value": [uploaded_file.name, confidence, observation if observation else "No analyst note recorded"]})
        recommendation = "Archive the uploaded image, formalise observation notes, and pair this evidence with entity records, coordinates, or transaction files before drawing operational conclusions."
    else:
        st.warning("No image uploaded yet. Please provide a satellite or site image to begin verification.")
        st.caption("Recommended sources: Google Earth captures, satellite screenshots, or field-observation images.")
        geo_score = 45
        geo_signal = "No uploaded image is available; geospatial verification remains incomplete."
        export_df = pd.DataFrame({"metric": ["status"], "value": ["No image uploaded"]})
        recommendation = "Obtain image evidence before moving the case beyond preliminary screening. In the absence of physical verification, maintain a guarded assessment posture."

# =========================================================
# COMPOSITE SCORE
# =========================================================
if intel_type == "Macro-Economic":
    composite_score = int((macro_score * 0.60) + (forensic_score * 0.25) + (geo_score * 0.15))
elif intel_type == "Forensic Audit":
    composite_score = int((macro_score * 0.20) + (forensic_score * 0.60) + (geo_score * 0.20))
else:
    composite_score = int((macro_score * 0.20) + (forensic_score * 0.25) + (geo_score * 0.55))

if risk_appetite == "Conservative":
    composite_score = min(composite_score + 8, 100)
elif risk_appetite == "Elevated Alert":
    composite_score = min(composite_score + 15, 100)

st.markdown("---")
st.subheader("Composite Strategic Risk Score")
a, b, c, d = st.columns(4)
for col, label, value in [(a, "Macro Score", macro_score), (b, "Forensic Score", forensic_score), (c, "Geo Score", geo_score), (d, "Composite Score", composite_score)]:
    with col:
        st.markdown(f'<div class="score-card"><div class="score-label">{label}</div><div class="score-value">{value}</div><div class="score-band">{risk_band(value)}</div></div>', unsafe_allow_html=True)

st.progress(composite_score)
st.caption(f"Current composite signal: {composite_score}/100 | Briefing Mode: {brief_mode} | Risk Appetite: {risk_appetite}")

# =========================================================
# EXECUTIVE BRIEF
# =========================================================
st.markdown("---")
st.subheader("Executive Brief")
brief_text = generate_executive_brief(target_zone, intel_type, composite_score, macro_signal, forensic_signal, geo_signal, recommendation)
left, right = st.columns([2, 1])
with left:
    st.markdown('<div class="brief-box">', unsafe_allow_html=True)
    st.markdown("**Key Findings**")
    st.markdown(f"- **Macro:** {macro_signal}")
    st.markdown(f"- **Forensic:** {forensic_signal}")
    st.markdown(f"- **Geospatial:** {geo_signal}")
    st.markdown(f"- **Composite Position:** {composite_score}/100, categorised as **{risk_band(composite_score)}**.")
    st.markdown("**Recommended Action**")
    st.write(recommendation)
    st.markdown('</div>', unsafe_allow_html=True)
with right:
    st.markdown('<div class="brief-box">', unsafe_allow_html=True)
    st.markdown("**Board View**")
    st.write("This dashboard supports executive prioritisation, preliminary integrity review, and internal escalation decisions.")
    st.markdown("**Use Cases**")
    st.markdown("- Board summary\n- Internal screening\n- Strategic due diligence\n- Analyst review\n- Portfolio monitoring")
    st.markdown("**Decision Posture**")
    st.write(risk_band(composite_score))
    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# EXPORTS
# =========================================================
st.markdown("---")
st.subheader("Export Centre")
export_bundle = pd.DataFrame({
    "field": ["target_geography", "analytical_layer", "risk_appetite", "brief_mode", "macro_score", "forensic_score", "geo_score", "composite_score", "macro_signal", "forensic_signal", "geo_signal", "recommendation", "timestamp"],
    "value": [target_zone, intel_type, risk_appetite, brief_mode, macro_score, forensic_score, geo_score, composite_score, macro_signal, forensic_signal, geo_signal, recommendation, datetime.datetime.now().strftime("%Y-%m-%d %H:%M")],
})

x1, x2, x3 = st.columns(3)
with x1:
    st.download_button("Download Executive Brief (.txt)", data=text_to_bytes(brief_text), file_name="executive_brief.txt", mime="text/plain")
with x2:
    st.download_button("Download Dashboard Summary (.csv)", data=dataframe_to_csv_bytes(export_bundle), file_name="dashboard_summary.csv", mime="text/csv")
with x3:
    st.download_button("Download Layer Data (.csv)", data=dataframe_to_csv_bytes(export_df), file_name="layer_data.csv", mime="text/csv")

st.caption("The export centre provides portable outputs for executive reporting, analyst archiving, and portfolio review workflows.")
st.markdown("---")
st.markdown("**Confidentiality Notice:** This dashboard is intended for strategic decision support, risk screening, and preliminary integrity review.")
st.caption("Developed as a premium intelligence-style Streamlit application with executive briefing, composite risk scoring, and export-ready structure.")
