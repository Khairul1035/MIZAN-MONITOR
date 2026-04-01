import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from PIL import Image
from io import BytesIO
import base64
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
# THEME / CSS
# =========================================================
st.markdown(
    """
    <style>
    html, body, [class*="css"] {
        font-family: "Inter", "Segoe UI", sans-serif;
    }

    .stApp {
        background: linear-gradient(180deg, #09101a 0%, #0d1623 55%, #111c2b 100%);
        color: #E9EEF5;
    }

    .block-container {
        max-width: 1450px;
        padding-top: 1.2rem;
        padding-bottom: 2rem;
    }

    h1 {
        color: #D9B86A !important;
        font-weight: 800 !important;
        letter-spacing: 0.02em;
    }

    h2, h3 {
        color: #F5F7FB !important;
        font-weight: 700 !important;
    }

    p, div, span, label, li {
        color: #E9EEF5 !important;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a1220 0%, #101a2d 100%);
        border-right: 1px solid rgba(217, 184, 106, 0.15);
    }

    section[data-testid="stSidebar"] * {
        color: #E9EEF5 !important;
    }

    div[data-baseweb="select"] > div,
    .stNumberInput input,
    .stTextArea textarea,
    .stTextInput input {
        background-color: #121c2b !important;
        color: #F5F7FB !important;
        border: 1px solid #2b364a !important;
        border-radius: 10px !important;
    }

    div[role="radiogroup"] label {
        background-color: #121c2b;
        border: 1px solid #2b364a;
        padding: 0.4rem 0.7rem;
        border-radius: 8px;
        margin-bottom: 0.35rem;
        display: block;
    }

    div[data-testid="metric-container"] {
        background: linear-gradient(180deg, #111b2a 0%, #0e1622 100%);
        border: 1px solid rgba(217, 184, 106, 0.22);
        padding: 1rem;
        border-radius: 14px;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.22);
    }

    div[data-testid="metric-container"] label {
        color: #AAB6C7 !important;
        font-weight: 600 !important;
        font-size: 0.92rem !important;
    }

    div[data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #FFFFFF !important;
        font-weight: 800 !important;
    }

    div[data-testid="metric-container"] [data-testid="stMetricDelta"] {
        color: #D9B86A !important;
        font-weight: 700 !important;
    }

    div[data-testid="stAlert"] {
        background-color: #111b2a !important;
        border: 1px solid rgba(217, 184, 106, 0.18) !important;
        border-radius: 12px !important;
    }

    .stButton > button {
        background: linear-gradient(180deg, #D9B86A 0%, #BC994C 100%);
        color: #0b1220 !important;
        border: none;
        border-radius: 10px;
        font-weight: 800;
        padding: 0.55rem 1rem;
    }

    .stDownloadButton > button {
        background: linear-gradient(180deg, #D9B86A 0%, #BC994C 100%);
        color: #0b1220 !important;
        border: none;
        border-radius: 10px;
        font-weight: 800;
        padding: 0.55rem 1rem;
    }

    div[data-testid="stProgressBar"] > div > div {
        background-color: #D9B86A !important;
    }

    .premium-panel {
        background: linear-gradient(180deg, #111b2a 0%, #0d1520 100%);
        border: 1px solid rgba(217, 184, 106, 0.18);
        border-radius: 16px;
        padding: 1rem 1.1rem;
        margin-bottom: 1rem;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.18);
    }

    .hero-wrap {
        background: linear-gradient(90deg, rgba(17,27,42,0.96) 0%, rgba(14,22,34,0.96) 100%);
        border: 1px solid rgba(217, 184, 106, 0.18);
        border-radius: 18px;
        padding: 1.2rem 1.2rem 1rem 1.2rem;
        margin-bottom: 1rem;
        box-shadow: 0 10px 24px rgba(0, 0, 0, 0.20);
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
        background: linear-gradient(180deg, #D9B86A 0%, #A37D37 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        color: #0d1520 !important;
        font-size: 1.4rem;
        font-weight: 900;
        box-shadow: inset 0 0 0 1px rgba(255,255,255,0.18);
    }

    .eyebrow {
        font-size: 0.78rem;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #9FB0C8 !important;
        margin-bottom: 0.25rem;
        font-weight: 700;
    }

    .hero-title {
        font-size: 1.85rem;
        font-weight: 900;
        color: #F7F9FC !important;
        margin-bottom: 0.18rem;
    }

    .hero-subtitle {
        font-size: 0.98rem;
        color: #BDCADB !important;
    }

    .small-note {
        color: #9FB0C8 !important;
        font-size: 0.86rem;
    }

    .score-card {
        background: linear-gradient(180deg, #121c2b 0%, #0f1724 100%);
        border: 1px solid rgba(217, 184, 106, 0.15);
        border-radius: 14px;
        padding: 1rem;
        text-align: center;
        min-height: 120px;
    }

    .score-label {
        color: #AAB6C7 !important;
        font-size: 0.82rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-weight: 700;
        margin-bottom: 0.4rem;
    }

    .score-value {
        font-size: 2rem;
        font-weight: 900;
        color: #FFFFFF !important;
        margin-bottom: 0.2rem;
    }

    .score-band {
        color: #D9B86A !important;
        font-weight: 700;
        font-size: 0.92rem;
    }

    .brief-box {
        background: linear-gradient(180deg, #121c2b 0%, #0f1724 100%);
        border: 1px solid rgba(217, 184, 106, 0.15);
        border-radius: 14px;
        padding: 1rem 1rem;
        min-height: 250px;
    }

    hr {
        border: none;
        border-top: 1px solid rgba(217, 184, 106, 0.16);
    }

    .stCaption {
        color: #9FB0C8 !important;
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
        return pd.DataFrame(
            {
                "year": [2020, 2021, 2022, 2023],
                "index_value": [100, 104, 108, 111],
            }
        )


def risk_band(score: int) -> str:
    if score >= 75:
        return "High Priority"
    if score >= 50:
        return "Moderate"
    if score >= 25:
        return "Guarded"
    return "Controlled"


def gauge_text(score: int) -> str:
    return f"{score}/100"


def render_logo_area():
    st.markdown(
        f"""
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
    fig.update_traces(line=dict(width=3, color="#D9B86A"), marker=dict(size=7, color="#D9B86A"))
    st.plotly_chart(fig, use_container_width=True)


def dataframe_to_csv_bytes(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8")


def text_to_bytes(text: str) -> bytes:
    return text.encode("utf-8")


def generate_executive_brief(
    zone: str,
    intel_type: str,
    composite_score: int,
    macro_signal: str,
    forensic_signal: str,
    geo_signal: str,
    recommendation: str,
) -> str:
    now_stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    brief = f"""
THE COVENANT | EXECUTIVE BRIEF
Generated: {now_stamp}
Target Geography: {zone}
Analytical Layer in Focus: {intel_type}

1. Executive Summary
The current dashboard assessment indicates a composite strategic risk score of {composite_score}/100, placing the target environment in the '{risk_band(composite_score)}' band. The operating picture combines macro-level resilience, forensic integrity screening, and geospatial verification logic to support high-level decision-making.

2. Signal Overview
- Macro Signal: {macro_signal}
- Forensic Signal: {forensic_signal}
- Geospatial Signal: {geo_signal}

3. Analytical Interpretation
The dashboard should be interpreted as an executive screening environment rather than a final investigative conclusion. Its purpose is to identify early warning signals, prioritise review resources, and strengthen evidence-based escalation.

4. Recommended Action
{recommendation}

5. Governance Note
This brief is intended for internal strategic use, board discussion, due diligence support, and preliminary integrity review.
""".strip()
    return brief


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
st.sidebar.markdown("### Executive Controls")
risk_appetite = st.sidebar.selectbox("Risk Appetite", ["Conservative", "Balanced", "Elevated Alert"])
brief_mode = st.sidebar.selectbox("Briefing Format", ["Board Summary", "Analyst Review", "Investor Screening"])

st.sidebar.markdown("---")
st.sidebar.markdown("### Analyst Desk")
st.sidebar.write("**Profile:** Strategic Finance & Integrity Analyst")
st.sidebar.write(f"**Last Synchronisation:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
st.sidebar.success("System Status: Operational")

# =========================================================
# HEADER / LOGO AREA
# =========================================================
render_logo_area()

st.title("Strategic Forensic Intelligence Dashboard")
st.markdown(
    "Integrated command environment for **economic monitoring**, **forensic screening**, "
    "**ground-truth verification**, and **export-ready executive reporting**."
)

# =========================================================
# STATE DEFAULTS
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
# PRIMARY LAYER CONTENT
# =========================================================
if intel_type == "Macro-Economic":
    st.subheader("Macro-Economic Resilience Assessment")

    code_map = {"Qatar": "QA", "Denmark": "DK", "Global": "WLD"}
    c_code = code_map[target_zone]
    df_intel = get_world_bank_data(c_code)
    export_df = df_intel.copy()

    if len(df_intel) >= 2:
        latest = float(df_intel["index_value"].iloc[-1])
        prev = float(df_intel["index_value"].iloc[-2])
        change = ((latest - prev) / prev) * 100 if prev != 0 else 0.0
    else:
        latest = float(df_intel["index_value"].iloc[-1])
        change = 0.0

    # Macro scoring logic
    if change >= 2:
        macro_score = 18
        macro_signal = f"Positive macro momentum observed, with the latest food production index at {latest:.2f} and a period-on-period change of {change:.2f}%."
    elif change >= 0:
        macro_score = 30
        macro_signal = f"Stable macro trajectory observed, with the latest food production index at {latest:.2f} and mild change of {change:.2f}%."
    else:
        macro_score = 52
        macro_signal = f"Macro caution flag: the latest food production index is {latest:.2f}, reflecting a decline of {abs(change):.2f}% from the prior observation."

    col1, col2, col3 = st.columns(3)
    col1.metric("Current Production Index", f"{latest:.2f}", f"{change:.2f}% vs prior period")
    col2.metric("Sovereign Risk Signal", "Stable" if macro_score < 40 else "Watchlist", risk_band(macro_score))
    col3.metric("Supply Chain Resilience", "92%" if macro_score < 40 else "74%", "External signal")

    corporate_line_chart(df_intel, target_zone)

    st.info(
        "Interpretation: This layer provides an external macro signal for country screening, supply continuity monitoring, and executive risk scanning."
    )

    recommendation = (
        "Maintain periodic macro monitoring, cross-check sector exposure, and integrate this signal with internal operational data before major capital or partnership decisions."
    )

elif intel_type == "Forensic Audit":
    st.subheader("Forensic Integrity & Ethical Stress Test")
    st.info(
        "This layer evaluates financial covenant pressure and anomaly signals to support preliminary integrity screening and escalation decisions."
    )

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

    # Forensic scoring logic
    forensic_score = 18
    if debt_ratio > 33.33:
        forensic_score += 35
    elif debt_ratio > 25:
        forensic_score += 18
    else:
        forensic_score += 6

    if anomaly_score == 2:
        forensic_score += 35
    elif anomaly_score == 1:
        forensic_score += 18
    else:
        forensic_score += 6

    forensic_score = min(forensic_score, 100)
    forensic_signal = (
        f"Forensic screen indicates a debt ratio of {debt_ratio:.2f}% and anomaly score of {anomaly_score}/2, placing the case in the '{risk_band(forensic_score)}' band."
    )

    export_df = pd.DataFrame(
        {
            "metric": [
                "total_assets_usd_m",
                "total_debt_usd_m",
                "debt_ratio_pct",
                "revenue_growth_index",
                "asset_quality_index",
                "anomaly_score",
                "forensic_score",
            ],
            "value": [
                total_assets,
                total_debt,
                round(debt_ratio, 2),
                revenue_growth,
                asset_quality,
                anomaly_score,
                forensic_score,
            ],
        }
    )

    recommendation = (
        "Escalate to enhanced due diligence where debt screening fails or anomaly patterns converge. Supplement this layer with document review, ratio trend analysis, and management explanations."
    )

elif intel_type == "Satellite Recon":
    st.subheader("Geospatial Verification & Ground-Truth Review")
    st.write(
        "Use this section to validate physical asset existence or observable activity through uploaded imagery and analyst notes."
    )

    uploaded_file = st.file_uploader("Upload verification image (JPG, PNG, JPEG)", type=["jpg", "png", "jpeg"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)

        col_img, col_note = st.columns([2, 1])
        with col_img:
            st.image(image, caption="Uploaded Verification Image", use_container_width=True)

        with col_note:
            st.markdown("### Analyst Observation")
            observation = st.text_area(
                "Intelligence Notes",
                placeholder="Example: Verified multiple infrastructure clusters and active land-use patterns consistent with reported expansion.",
            )
            confidence = st.slider("Evidence Confidence Score", 0, 100, 95)
            st.progress(confidence)

            if confidence >= 85:
                st.success("Assessment Status: High-confidence verification")
            elif confidence >= 60:
                st.info("Assessment Status: Moderate-confidence verification")
            else:
                st.warning("Assessment Status: Low-confidence verification")

        # Geospatial scoring logic
        if confidence >= 85:
            geo_score = 16
        elif confidence >= 60:
            geo_score = 36
        else:
            geo_score = 62

        geo_signal = (
            f"Geospatial review completed with an evidence confidence score of {confidence}/100, indicating a '{risk_band(geo_score)}' verification posture."
        )

        export_df = pd.DataFrame(
            {
                "metric": ["uploaded_image_name", "confidence_score", "observation"],
                "value": [uploaded_file.name, confidence, observation if observation else "No analyst note recorded"],
            }
        )

        recommendation = (
            "Archive the uploaded image, formalise observation notes, and pair this evidence with entity records, coordinates, or transaction files before drawing operational conclusions."
        )
    else:
        st.warning("No image uploaded yet. Please provide a satellite or site image to begin verification.")
        st.caption("Recommended sources: Google Earth captures, satellite screenshots, or field-observation images.")
        geo_score = 45
        geo_signal = "No uploaded image is available; geospatial verification remains incomplete."
        export_df = pd.DataFrame({"metric": ["status"], "value": ["No image uploaded"]})
        recommendation = (
            "Obtain image evidence before moving the case beyond preliminary screening. In the absence of physical verification, maintain a guarded assessment posture."
        )

# =========================================================
# COMPOSITE RISK ENGINE
# =========================================================
weights = {"Macro-Economic": 0.35, "Forensic Audit": 0.40, "Satellite Recon": 0.25}
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

# =========================================================
# COMPOSITE SCORE AREA
# =========================================================
st.markdown("---")
st.subheader("Composite Strategic Risk Score")

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(
        f"""
        <div class="score-card">
            <div class="score-label">Macro Score</div>
            <div class="score-value">{macro_score}</div>
            <div class="score-band">{risk_band(macro_score)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with c2:
    st.markdown(
        f"""
        <div class="score-card">
            <div class="score-label">Forensic Score</div>
            <div class="score-value">{forensic_score}</div>
            <div class="score-band">{risk_band(forensic_score)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with c3:
    st.markdown(
        f"""
        <div class="score-card">
            <div class="score-label">Geo Score</div>
            <div class="score-value">{geo_score}</div>
            <div class="score-band">{risk_band(geo_score)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with c4:
    st.markdown(
        f"""
        <div class="score-card">
            <div class="score-label">Composite Score</div>
            <div class="score-value">{composite_score}</div>
            <div class="score-band">{risk_band(composite_score)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.progress(composite_score)
st.caption(f"Current composite signal: {gauge_text(composite_score)} | Briefing Mode: {brief_mode} | Risk Appetite: {risk_appetite}")

# =========================================================
# EXECUTIVE BRIEF
# =========================================================
st.markdown("---")
st.subheader("Executive Brief")

brief_text = generate_executive_brief(
    zone=target_zone,
    intel_type=intel_type,
    composite_score=composite_score,
    macro_signal=macro_signal,
    forensic_signal=forensic_signal,
    geo_signal=geo_signal,
    recommendation=recommendation,
)

left_brief, right_brief = st.columns([2, 1])

with left_brief:
    st.markdown('<div class="brief-box">', unsafe_allow_html=True)
    st.markdown("**Key Findings**")
    st.markdown(f"- **Macro:** {macro_signal}")
    st.markdown(f"- **Forensic:** {forensic_signal}")
    st.markdown(f"- **Geospatial:** {geo_signal}")
    st.markdown(f"- **Composite Position:** {composite_score}/100, categorised as **{risk_band(composite_score)}**.")
    st.markdown("**Recommended Action**")
    st.write(recommendation)
    st.markdown('</div>', unsafe_allow_html=True)

with right_brief:
    st.markdown('<div class="brief-box">', unsafe_allow_html=True)
    st.markdown("**Board View**")
    st.write(
        "This dashboard is designed to support executive prioritisation, preliminary integrity review, and internal escalation decisions."
    )
    st.markdown("**Use Cases**")
    st.markdown(
        "- Board summary\n- Internal screening\n- Strategic due diligence\n- Analyst review\n- Portfolio monitoring"
    )
    st.markdown("**Decision Posture**")
    st.write(risk_band(composite_score))
    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# EXPORT-READY STRUCTURE
# =========================================================
st.markdown("---")
st.subheader("Export Centre")

export_bundle = pd.DataFrame(
    {
        "field": [
            "target_geography",
            "analytical_layer",
            "risk_appetite",
            "brief_mode",
            "macro_score",
            "forensic_score",
            "geo_score",
            "composite_score",
            "macro_signal",
            "forensic_signal",
            "geo_signal",
            "recommendation",
            "timestamp",
        ],
        "value": [
            target_zone,
            intel_type,
            risk_appetite,
            brief_mode,
            macro_score,
            forensic_score,
            geo_score,
            composite_score,
            macro_signal,
            forensic_signal,
            geo_signal,
            recommendation,
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        ],
    }
)

col_export1, col_export2, col_export3 = st.columns(3)

with col_export1:
    st.download_button(
        label="Download Executive Brief (.txt)",
        data=text_to_bytes(brief_text),
        file_name="executive_brief.txt",
        mime="text/plain",
    )

with col_export2:
    st.download_button(
        label="Download Dashboard Summary (.csv)",
        data=dataframe_to_csv_bytes(export_bundle),
        file_name="dashboard_summary.csv",
        mime="text/csv",
    )

with col_export3:
    st.download_button(
        label="Download Layer Data (.csv)",
        data=dataframe_to_csv_bytes(export_df),
        file_name="layer_data.csv",
        mime="text/csv",
    )

st.caption("The export centre provides portable outputs for executive reporting, analyst archiving, and portfolio review workflows.")

# =========================================================
# FOOTER
# =========================================================
st.markdown("---")
st.markdown(
    "**Confidentiality Notice:** This dashboard is intended for strategic decision support, risk screening, and preliminary integrity review."
)
st.caption(
    "Developed as a premium intelligence-style Streamlit application with executive briefing, composite risk scoring, and export-ready structure."
)
