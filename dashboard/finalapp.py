import time
from datetime import date

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import streamlit as st
from supabase import create_client

st.set_page_config(page_title="Smart Fan Energy Watch", layout="wide")

st.markdown(
    """
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@600;700&display=swap');
      :root {
        --bg: #07111f;
        --card: #091521;
        --text: #edf2fa;
        --muted: #8aa4be;
        --border: #1e3248;
        --temp: #f59e0b;
        --power: #22d3ee;
        --save: #84cc16;
        --warn: #ef4444;
        --font-display: "Space Grotesk", "Inter", sans-serif;
        --font-body: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      }
      .stApp {
        background:
          radial-gradient(1400px 600px at 10% -15%, #0e3a6699, transparent 55%),
          radial-gradient(1100px 500px at 90% -25%, #0d6e6288, transparent 50%),
          radial-gradient(800px 400px at 50% 100%, #0a1f3344, transparent 60%),
          var(--bg);
        font-family: var(--font-body);
      }
      .block-container {
        padding-top: 0.75rem !important;
        padding-bottom: 0.5rem !important;
      }
      header[data-testid="stHeader"] {
        background: transparent !important;
        backdrop-filter: none !important;
      }
      [data-testid="stToolbar"] {
        background: transparent !important;
      }
      h1, h2, h3, [data-testid="stSidebarHeader"] {
        font-family: var(--font-display);
        letter-spacing: -0.01em;
      }
      [data-testid="stMetric"] {
        background: linear-gradient(160deg, #102238 0%, var(--card) 100%);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 6px;
      }
      [data-testid="stMetricLabel"] {
        font-family: var(--font-body);
        font-weight: 500;
      }
      [data-testid="stMetricValue"] {
        font-family: var(--font-display);
        font-size: 2.15rem;
        line-height: 1.1;
      }
      .section-title {
        color: var(--text);
        font-size: 0.95rem;
        font-weight: 700;
        margin: 4px 0 2px 0;
        font-family: var(--font-display);
        padding-left: 10px;
        border-left: 3px solid var(--save);
        line-height: 1.3;
      }
      .section-title-lg-top {
        margin-top: 10px;
      }
      .section-subtitle {
        color: var(--muted);
        font-size: 0.8rem;
        margin-bottom: 5px;
        padding-left: 13px;
      }
      .mode-badge {
        display: inline-block;
        border-radius: 6px;
        padding: 2px 9px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.05em;
      }
      .mode-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.84rem;
        margin-top: 10px;
      }
      .mode-table th {
        color: var(--muted);
        font-weight: 500;
        text-align: left;
        padding: 4px 8px;
        border-bottom: 1px solid var(--border);
        font-size: 0.78rem;
      }
      .mode-table td {
        padding: 6px 8px;
        border-bottom: 1px solid rgba(31,51,71,0.5);
        color: var(--text);
      }
      .kpi-row-gap-tight {
        margin-top: 6px;
      }
      .kpi-card {
        background: linear-gradient(160deg, #0d2640 0%, var(--card) 100%);
        border: 1px solid var(--border);
        border-left: 3px solid var(--kpi-accent, var(--border));
        border-radius: 12px;
        padding: 10px 14px 8px 12px;
        height: 100%;
      }
      .kpi-label {
        font-family: var(--font-body);
        font-weight: 500;
        font-size: 0.78rem;
        color: var(--muted);
        margin-bottom: 2px;
      }
      .kpi-value {
        font-family: var(--font-display);
        font-size: 1.75rem;
        font-weight: 700;
        color: var(--text);
        line-height: 1.1;
      }
      .kpi-delta {
        font-size: 0.78rem;
        color: var(--save);
        margin-top: 2px;
        font-weight: 500;
      }
      .kpi-card-secondary {
        background: linear-gradient(160deg, #0a1c30 0%, var(--card) 100%);
        border: 1px solid var(--border);
        border-left: 3px solid rgba(159,179,200,0.25);
        border-radius: 12px;
        padding: 8px 14px 7px 12px;
        height: 100%;
        opacity: 0.82;
      }
      .kpi-card-secondary .kpi-label {
        font-size: 0.74rem;
      }
      .kpi-card-secondary .kpi-value {
        font-size: 1.3rem;
      }
      .sidebar-section-header {
        display: flex;
        align-items: center;
        gap: 7px;
        font-family: var(--font-display);
        font-size: 0.82rem;
        font-weight: 700;
        color: var(--muted);
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin: 4px 0 10px 0;
      }
      .sidebar-section-header::before {
        content: "";
        display: inline-block;
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: var(--save);
        flex-shrink: 0;
      }
      .sidebar-divider {
        border: none;
        border-top: 1px solid var(--border);
        margin: 14px 0;
      }
      .weather-box {
        background: rgba(34,197,94,0.07);
        border: 1px solid rgba(34,197,94,0.20);
        border-radius: 10px;
        padding: 10px 12px;
        font-size: 0.82rem;
        color: var(--muted);
        line-height: 1.6;
        margin-top: 6px;
      }
      .weather-box strong {
        color: var(--text);
      }
      .section-divider {
        border: none;
        border-top: 1px solid var(--border);
        margin: 10px 0 8px 0;
      }
      .readings-scroll {
        max-height: 260px;
        overflow-y: auto;
        scrollbar-width: thin;
        scrollbar-color: var(--border) transparent;
      }
      .system-banner {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr 1fr;
        gap: 10px;
        background: linear-gradient(135deg, #0c2040 0%, #081628 100%);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 12px 18px;
        margin-bottom: 10px;
      }
      .banner-cell {
        display: flex;
        flex-direction: column;
        gap: 4px;
      }
      .banner-cell + .banner-cell {
        border-left: 1px solid var(--border);
        padding-left: 20px;
      }
      .banner-label {
        font-size: 0.75rem;
        font-weight: 600;
        color: var(--muted);
        text-transform: uppercase;
        letter-spacing: 0.07em;
      }
      .banner-value {
        font-family: var(--font-display);
        font-size: 1.55rem;
        font-weight: 700;
        color: var(--text);
        line-height: 1.1;
      }
      .banner-sub {
        font-size: 0.78rem;
        color: var(--muted);
        margin-top: 2px;
      }
      .mode-indicator {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        font-family: var(--font-display);
        font-size: 1.55rem;
        font-weight: 700;
        line-height: 1.1;
      }
      .mode-indicator-dot {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        flex-shrink: 0;
      }
      .status-pill {
        display: inline-block;
        border: 1px solid var(--border);
        border-radius: 999px;
        color: var(--muted);
        padding: 4px 10px;
        font-size: 0.78rem;
        margin-right: 6px;
      }
      .hero-bar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 2px 0 10px 0;
        border-bottom: 1px solid var(--border);
        margin-bottom: 10px;
      }
      .hero-title {
        font-family: var(--font-display);
        font-size: 1.7rem;
        font-weight: 700;
        color: var(--text);
        letter-spacing: -0.02em;
        margin: 0;
      }
      .hero-title span {
        color: var(--save);
      }
      .live-badge {
        display: flex;
        align-items: center;
        gap: 7px;
        background: rgba(34,197,94,0.10);
        border: 1px solid rgba(34,197,94,0.30);
        border-radius: 999px;
        padding: 6px 14px;
        font-size: 0.82rem;
        font-weight: 600;
        color: var(--save);
        letter-spacing: 0.04em;
      }
      .live-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: var(--save);
        animation: pulse 1.6s ease-in-out infinite;
      }
      @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50%       { opacity: 0.4; transform: scale(0.75); }
      }
      .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        border: 1px solid var(--border);
        border-radius: 999px;
        color: var(--muted);
        padding: 4px 11px;
        font-size: 0.78rem;
        margin-right: 6px;
        background: rgba(255,255,255,0.02);
      }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero-bar">
      <h1 class="hero-title">Smart Fan <span>Energy</span> Watch</h1>
      <div class="live-badge"><div class="live-dot"></div>LIVE</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- Secrets ---
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
sb = create_client(SUPABASE_URL, SUPABASE_KEY)


# --- Sidebar controls ---
st.sidebar.markdown("<div class='sidebar-section-header'>Live settings</div>", unsafe_allow_html=True)
REFRESH_SEC = st.sidebar.slider("Refresh interval (seconds)", 1, 10, 2)
DEVICE_ID = st.sidebar.text_input("device_id filter (optional)", value="esp32_01")
LIMIT = st.sidebar.slider("Rows to display", 50, 1000, 200)
WINDOW_HOURS = st.sidebar.slider("Analysis window (hours)", 1, 168, 24)
MAX_GAP_MIN = st.sidebar.slider("Ignore gaps larger than (minutes)", 1, 180, 30)

st.sidebar.markdown("<hr class='sidebar-divider'>", unsafe_allow_html=True)
st.sidebar.markdown("<div class='sidebar-section-header'>Savings assumptions</div>", unsafe_allow_html=True)
BASELINE_W = st.sidebar.number_input(
    "Baseline power (W) (e.g., HIGH mode)", min_value=0.0, value=2.949, step=0.1
)
PRICE_PER_KWH = st.sidebar.number_input(
    "Electricity price ($/kWh)", min_value=0.0, value=0.35, step=0.01
)


# --- Helper: fetch latest rows ---
@st.cache_data(ttl=1)
def fetch_latest(limit: int, device_id: str | None):
    q = (
        sb.table("fan_readings")
        .select("created_at,temp_c,power_w,fan_mode,device_id")
        .order("created_at", desc=True)
        .limit(limit)
    )
    if device_id:
        q = q.eq("device_id", device_id)
    data = q.execute().data
    df = pd.DataFrame(data)
    if df.empty:
        return df
    df["created_at"] = (
        pd.to_datetime(df["created_at"], utc=True)
        .dt.tz_convert("America/Los_Angeles")
        .dt.tz_localize(None)
    )
    df = df.sort_values("created_at")
    return df


def _interval_hours(df: pd.DataFrame, time_col: str, max_gap_seconds: float | None) -> pd.Series:
    dt_h = df[time_col].diff().dt.total_seconds().clip(lower=0) / 3600.0
    if max_gap_seconds is not None:
        dt_h = dt_h.where(dt_h * 3600.0 <= max_gap_seconds, 0.0)
    return dt_h.fillna(0)


def energy_kwh_from_power(
    df: pd.DataFrame, time_col="created_at", power_col="power_w", max_gap_seconds: float | None = None
) -> float:
    d = df.copy().sort_values(time_col)
    dt_h = _interval_hours(d, time_col, max_gap_seconds)
    return float((d[power_col].astype(float) * dt_h).sum() / 1000.0)


def baseline_kwh_constant(
    df: pd.DataFrame, baseline_watts: float, time_col="created_at", max_gap_seconds: float | None = None
) -> float:
    d = df.copy().sort_values(time_col)
    dt_h = _interval_hours(d, time_col, max_gap_seconds)
    return float((baseline_watts * dt_h).sum() / 1000.0)


def make_sparkline(values: list, color: str, width: int = 96, height: int = 28) -> str:
    if len(values) < 2:
        return ""
    lo, hi = min(values), max(values)
    span = hi - lo if hi != lo else 1.0
    xs = [i * width / (len(values) - 1) for i in range(len(values))]
    ys = [height - ((v - lo) / span) * (height - 4) - 2 for v in values]
    pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in zip(xs, ys))
    fill_pts = f"0,{height} " + pts + f" {width},{height}"
    uid = abs(hash(color)) % 9999
    return (
        f"<svg width='{width}' height='{height}' viewBox='0 0 {width} {height}' "
        f"style='display:block;margin-top:6px;overflow:visible;'>"
        f"<defs><linearGradient id='sg{uid}' x1='0' y1='0' x2='0' y2='1'>"
        f"<stop offset='0%' stop-color='{color}' stop-opacity='0.25'/>"
        f"<stop offset='100%' stop-color='{color}' stop-opacity='0.0'/>"
        f"</linearGradient></defs>"
        f"<polygon points='{fill_pts}' fill='url(#sg{uid})'/>"
        f"<polyline points='{pts}' fill='none' stroke='{color}' stroke-width='1.5' "
        f"stroke-linejoin='round' stroke-linecap='round'/>"
        f"</svg>"
    )


def format_cost(value: float) -> str:
    if value == 0:
        return "$0.000"
    if value < 0.001:
        return f"${value:.5f}"
    if value < 0.01:
        return f"${value:.4f}"
    return f"${value:.3f}"


def format_duration(seconds: float) -> str:
    seconds = max(0, int(round(seconds)))
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    if h > 0:
        return f"{h}h {m}m {s}s"
    if m > 0:
        return f"{m}m {s}s"
    return f"{s}s"


@st.cache_data(ttl=1800)
def get_weather_today(lat: float, lon: float):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "temperature_unit": "fahrenheit",
        "timezone": "America/Los_Angeles",
        "current": "temperature_2m",
        "daily": "temperature_2m_max",
    }

    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    j = r.json()

    cur = j.get("current", {}).get("temperature_2m", None)
    if cur is None:
        raise ValueError("Open-Meteo current temperature missing")
    current_f = float(cur)

    today_str = date.today().isoformat()
    days = j["daily"]["time"]
    peaks = j["daily"]["temperature_2m_max"]

    if today_str in days:
        i = days.index(today_str)
        peak_f = float(peaks[i])
    else:
        peak_f = float(peaks[0])

    return current_f, peak_f


def weather_thresholds(now_f: float, peak_f: float):
    med_at = float(now_f)
    high_at = float(peak_f) - 1.0
    if high_at < med_at + 2:
        high_at = med_at + 2
    return med_at, high_at


def c_to_f(c: float) -> float:
    return c * 9.0 / 5.0 + 32.0


# --- Live status ---
df_all = fetch_latest(LIMIT, DEVICE_ID.strip() if DEVICE_ID.strip() else None)
if not df_all.empty:
    cutoff = df_all["created_at"].max() - pd.Timedelta(hours=WINDOW_HOURS)
    df = df_all[df_all["created_at"] >= cutoff].copy()
else:
    df = df_all

LAT = 32.6859
LON = -117.1831

try:
    outdoor_now_f, outdoor_peak_f = get_weather_today(LAT, LON)
except Exception as e:
    st.sidebar.warning(f"Weather fetch failed: {e}")
    outdoor_now_f, outdoor_peak_f = None, None

if outdoor_now_f is not None and outdoor_peak_f is not None:
    med_threshold_f, high_threshold_f = weather_thresholds(outdoor_now_f, outdoor_peak_f)
else:
    med_threshold_f, high_threshold_f = None, None

if med_threshold_f is not None:
    st.sidebar.markdown("<hr class='sidebar-divider'>", unsafe_allow_html=True)
    st.sidebar.markdown("<div class='sidebar-section-header'>Weather thresholds</div>", unsafe_allow_html=True)
    st.sidebar.markdown(
        f"<div class='weather-box'>"
        f"<strong>Now:</strong> {outdoor_now_f:.0f}°F &nbsp;|&nbsp; <strong>Peak:</strong> {outdoor_peak_f:.0f}°F<br>"
        f"MED &ge; {med_threshold_f:.0f}°F &nbsp;&nbsp; HIGH &ge; {high_threshold_f:.0f}°F"
        f"</div>",
        unsafe_allow_html=True,
    )

status_cols = st.columns([1.1, 1.1, 2.8])
status_cols[0].markdown("<span class='status-pill'><span style='color:#22c55e;'>⬤</span>&nbsp;Live polling</span>", unsafe_allow_html=True)
status_cols[1].markdown(
    f"<span class='status-pill'>↻&nbsp;Refresh: {REFRESH_SEC}s</span>",
    unsafe_allow_html=True,
)
status_cols[2].markdown(
    f"<span class='status-pill'>⬡&nbsp;Device: {DEVICE_ID.strip() or 'all devices'}</span>",
    unsafe_allow_html=True,
)

if df.empty:
    st.warning("No rows found yet. Make sure ESP32 is inserting into `fan_readings` and device_id matches.")
else:
    last = df.iloc[-1]
    indoor_f = c_to_f(float(last["temp_c"]))

    max_gap_seconds = float(MAX_GAP_MIN * 60)
    dt_s = df["created_at"].diff().dt.total_seconds().clip(lower=0).fillna(0)
    active_dt_s = dt_s.where(dt_s <= max_gap_seconds, 0.0)

    window_seconds = float(active_dt_s.sum())
    avg_interval_seconds = df["created_at"].diff().dt.total_seconds().dropna().mean()
    avg_interval_seconds = float(avg_interval_seconds) if pd.notna(avg_interval_seconds) else 0.0

    actual_kwh = energy_kwh_from_power(df, max_gap_seconds=max_gap_seconds)
    base_kwh = baseline_kwh_constant(df, float(BASELINE_W), max_gap_seconds=max_gap_seconds)
    saved_kwh = max(0.0, base_kwh - actual_kwh)
    pct_saved = (saved_kwh / base_kwh * 100.0) if base_kwh > 0 else 0.0

    cost_used = actual_kwh * float(PRICE_PER_KWH)
    cost_saved = saved_kwh * float(PRICE_PER_KWH)

    spark_temp  = make_sparkline(df["temp_c"].tolist()[-40:], "#f59e0b")
    spark_power = make_sparkline(df["power_w"].tolist()[-40:], "#22d3ee")

    # --- System status banner ---
    current_mode = str(last.get("fan_mode", "—"))
    mode_color = {"OFF": "#4b5563", "LOW": "#22c55e", "MEDIUM": "#22d3ee", "HIGH": "#ef4444"}.get(current_mode, "#9fb3c8")
    outdoor_str = f"{outdoor_now_f:.0f}°F" if outdoor_now_f is not None else "—"
    outdoor_peak_str = f"{outdoor_peak_f:.0f}°F" if outdoor_peak_f is not None else "—"
    st.markdown(
        f"""
        <div class='system-banner'>
          <div class='banner-cell'>
            <div class='banner-label'>Indoor Temp</div>
            <div class='banner-value' style='color:#f59e0b;'>{indoor_f:.1f}°F</div>
            <div class='banner-sub'>{float(last['temp_c']):.1f}°C</div>
            {spark_temp}
          </div>
          <div class='banner-cell'>
            <div class='banner-label'>Outdoor</div>
            <div class='banner-value'>{outdoor_str}</div>
            <div class='banner-sub'>Peak today: {outdoor_peak_str}</div>
          </div>
          <div class='banner-cell'>
            <div class='banner-label'>Fan Mode</div>
            <div class='mode-indicator'>
              <div class='mode-indicator-dot' style='background:{mode_color};box-shadow:0 0 8px {mode_color}88;'></div>
              <span style='color:{mode_color};'>{current_mode}</span>
            </div>
            <div class='banner-sub'>{float(last['power_w']):.3f} W</div>
          </div>
          <div class='banner-cell'>
            <div class='banner-label'>Energy Saved</div>
            <div class='banner-value' style='color:#22c55e;'>{pct_saved:.1f}%</div>
            <div class='banner-sub'>{format_cost(cost_saved)} at ${float(PRICE_PER_KWH):.2f}/kWh</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div class='section-title'>Detailed Metrics</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='section-subtitle'>Energy breakdown and session statistics for the current analysis window.</div>",
        unsafe_allow_html=True,
    )

    k1, k2, k3, k4 = st.columns(4)
    k1.markdown(f"""
        <div class='kpi-card' style='--kpi-accent:#22d3ee;'>
          <div class='kpi-label'>Current Power</div>
          <div class='kpi-value'>{float(last['power_w']):.3f} W</div>
          {spark_power}
        </div>""", unsafe_allow_html=True)
    k2.markdown(f"""
        <div class='kpi-card' style='--kpi-accent:#22c55e;'>
          <div class='kpi-label'>Adaptive Energy Used</div>
          <div class='kpi-value'>{actual_kwh:.4f} kWh</div>
        </div>""", unsafe_allow_html=True)
    k3.markdown(f"""
        <div class='kpi-card' style='--kpi-accent:#f97316;'>
          <div class='kpi-label'>Baseline Energy</div>
          <div class='kpi-value'>{base_kwh:.4f} kWh</div>
        </div>""", unsafe_allow_html=True)
    k4.markdown(f"""
        <div class='kpi-card' style='--kpi-accent:#22c55e;'>
          <div class='kpi-label'>Energy Saved</div>
          <div class='kpi-value'>{saved_kwh:.4f} kWh</div>
          <div class='kpi-delta'>+{format_cost(cost_saved)} saved</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div class='kpi-row-gap-tight'></div>", unsafe_allow_html=True)
    d1, d2, d3, d4 = st.columns(4)
    d1.markdown(f"""
        <div class='kpi-card-secondary'>
          <div class='kpi-label'>Analysis Window</div>
          <div class='kpi-value'>{format_duration(window_seconds)}</div>
        </div>""", unsafe_allow_html=True)
    d2.markdown(f"""
        <div class='kpi-card-secondary'>
          <div class='kpi-label'>Avg Sample Interval</div>
          <div class='kpi-value'>{avg_interval_seconds:.1f}s</div>
        </div>""", unsafe_allow_html=True)
    d3.markdown(f"""
        <div class='kpi-card-secondary'>
          <div class='kpi-label'>Cost Used</div>
          <div class='kpi-value'>{format_cost(cost_used)}</div>
        </div>""", unsafe_allow_html=True)
    d4.markdown(f"""
        <div class='kpi-card-secondary'>
          <div class='kpi-label'>Last Reading</div>
          <div class='kpi-value'>{last['created_at'].strftime('%H:%M:%S')}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    MODE_COLORS = {
        "OFF":    "#4b5563",
        "LOW":    "#84cc16",
        "MEDIUM": "#22d3ee",
        "HIGH":   "#ef4444",
    }

    left, right = st.columns([1.6, 1.2])

    with left:
        st.markdown("<div class='section-title section-title-lg-top'>Latest Readings</div>", unsafe_allow_html=True)
        st.markdown(
            "<div class='section-subtitle'>Most recent 50 points for operational monitoring.</div>",
            unsafe_allow_html=True,
        )
        latest50 = df[["created_at", "temp_c", "power_w", "fan_mode", "device_id"]].tail(50).copy()
        tbl_rows = ""
        for _, row in latest50.iloc[::-1].iterrows():
            mode = str(row["fan_mode"])
            color = MODE_COLORS.get(mode, "#9fb3c8")
            bg = color + "22"
            tbl_rows += (
                f"<tr>"
                f"<td>{row['created_at'].strftime('%H:%M:%S')}</td>"
                f"<td>{float(row['temp_c']):.1f}</td>"
                f"<td>{float(row['power_w']):.3f}</td>"
                f"<td><span class='mode-badge' style='color:{color};background:{bg};'>{mode}</span></td>"
                f"<td style='color:var(--muted);font-size:0.78rem;'>{row['device_id']}</td>"
                f"</tr>"
            )
        st.markdown(
            f"<div class='readings-scroll'><table class='mode-table'>"
            f"<thead><tr><th>Time</th><th>Temp (°C)</th><th>Power (W)</th><th>Mode</th><th>Device</th></tr></thead>"
            f"<tbody>{tbl_rows}</tbody>"
            f"</table></div>",
            unsafe_allow_html=True,
        )

        with st.expander("Show full raw table"):
            st.dataframe(df, use_container_width=True)

    with right:
        st.markdown("<div class='section-title section-title-lg-top'>Mode Breakdown</div>", unsafe_allow_html=True)
        st.markdown(
            "<div class='section-subtitle'>Time-weighted share of each fan mode in this window.</div>",
            unsafe_allow_html=True,
        )

        d = df.copy().sort_values("created_at")
        d["dt_s"] = d["created_at"].diff().dt.total_seconds().clip(lower=0).fillna(0)
        d["dt_s"] = d["dt_s"].where(d["dt_s"] <= max_gap_seconds, 0.0)
        d["mode_for_interval"] = d["fan_mode"].shift(1).fillna(d["fan_mode"])

        mode_seconds = d.groupby("mode_for_interval")["dt_s"].sum().sort_values(ascending=False)
        total_seconds = mode_seconds.sum()

        if total_seconds > 0:
            mode_pct = (mode_seconds / total_seconds * 100.0).round(1)
            labels = mode_pct.index.astype(str).tolist()
            colors = [MODE_COLORS.get(m, "#9fb3c8") for m in labels]

            donut = go.Figure(go.Pie(
                labels=labels,
                values=mode_pct.values,
                hole=0.6,
                marker=dict(colors=colors, line=dict(color="#07111f", width=2)),
                textinfo="percent",
                textfont=dict(size=12, color="#e6edf7"),
                hovertemplate="%{label}: %{value:.1f}%<extra></extra>",
            ))
            donut.update_layout(
                margin=dict(l=0, r=0, t=0, b=0),
                height=300,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#dbe7f3"),
                legend=dict(orientation="v", y=0.5, x=1.0, xanchor="left", yanchor="middle", font=dict(size=11)),
                showlegend=True,
            )
            st.plotly_chart(donut, use_container_width=True)

            rows = ""
            for mode, pct in mode_pct.items():
                color = MODE_COLORS.get(str(mode), "#9fb3c8")
                bg = color + "22"
                secs = mode_seconds[mode]
                rows += (
                    f"<tr>"
                    f"<td><span class='mode-badge' style='color:{color};background:{bg};'>{mode}</span></td>"
                    f"<td>{secs:.0f}s</td>"
                    f"<td>{pct:.1f}%</td>"
                    f"</tr>"
                )
            st.markdown(
                f"<table class='mode-table'>"
                f"<thead><tr><th>Mode</th><th>Seconds</th><th>Share</th></tr></thead>"
                f"<tbody>{rows}</tbody>"
                f"</table>",
                unsafe_allow_html=True,
            )
        else:
            st.info("Not enough time range yet to compute mode breakdown.")

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)

    with c1:
        st.markdown("<div class='section-title section-title-lg-top'>Temperature vs Time</div>", unsafe_allow_html=True)
        st.markdown(
            """
            <div style='display:flex;gap:12px;padding-left:13px;margin-bottom:2px;flex-wrap:wrap;'>
              <span style='display:flex;align-items:center;gap:5px;font-size:0.74rem;color:#9fb3c8;'>
                <span style='width:10px;height:10px;border-radius:2px;background:#4b556322;border:1px solid #4b5563;display:inline-block;'></span>OFF
              </span>
              <span style='display:flex;align-items:center;gap:5px;font-size:0.74rem;color:#9fb3c8;'>
                <span style='width:10px;height:10px;border-radius:2px;background:#22c55e22;border:1px solid #22c55e66;display:inline-block;'></span>LOW
              </span>
              <span style='display:flex;align-items:center;gap:5px;font-size:0.74rem;color:#9fb3c8;'>
                <span style='width:10px;height:10px;border-radius:2px;background:#22d3ee22;border:1px solid #22d3ee66;display:inline-block;'></span>MEDIUM
              </span>
              <span style='display:flex;align-items:center;gap:5px;font-size:0.74rem;color:#9fb3c8;'>
                <span style='width:10px;height:10px;border-radius:2px;background:#ef444422;border:1px solid #ef444466;display:inline-block;'></span>HIGH
              </span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        temp_fig = go.Figure()

        # Mode background bands
        _mode_band_colors = {"OFF": "rgba(75,85,99,0.12)", "LOW": "rgba(34,197,94,0.08)",
                             "MEDIUM": "rgba(34,211,238,0.08)", "HIGH": "rgba(239,68,68,0.10)"}
        _df_bands = df[["created_at", "fan_mode"]].copy()
        _i = 0
        while _i < len(_df_bands) - 1:
            _mode = str(_df_bands.iloc[_i]["fan_mode"])
            _x0 = _df_bands.iloc[_i]["created_at"]
            _j = _i + 1
            while _j < len(_df_bands) and str(_df_bands.iloc[_j]["fan_mode"]) == _mode:
                _j += 1
            _x1 = _df_bands.iloc[min(_j, len(_df_bands) - 1)]["created_at"]
            temp_fig.add_vrect(x0=_x0, x1=_x1,
                fillcolor=_mode_band_colors.get(_mode, "rgba(0,0,0,0)"),
                line_width=0, layer="below")
            _i = _j

        temp_fig.add_trace(
            go.Scatter(
                x=df["created_at"],
                y=df["temp_c"],
                mode="lines",
                name="Indoor temp (°C)",
                line=dict(color="#f59e0b", width=2.5),
                fill="tozeroy",
                fillcolor="rgba(245,158,11,0.10)",
                customdata=df["fan_mode"],
                hovertemplate="<b>%{x|%H:%M:%S}</b><br>Temp: %{y:.1f}°C<br>Mode: %{customdata}<extra></extra>",
            )
        )

        if med_threshold_f is not None:
            med_c = (med_threshold_f - 32.0) * 5.0 / 9.0
            high_c = (high_threshold_f - 32.0) * 5.0 / 9.0
            temp_fig.add_hline(y=med_c, line_dash="dot", line_color="#38bdf8", annotation_text="MED threshold")
            temp_fig.add_hline(y=high_c, line_dash="dash", line_color="#ef4444", annotation_text="HIGH threshold")

        temp_fig.update_layout(
            xaxis_title="Time (LA)",
            yaxis_title="Temp (°C)",
            margin=dict(l=10, r=10, t=8, b=10),
            height=300,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#dbe7f3"),
            legend=dict(orientation="h", y=1.05, x=0),
            xaxis=dict(gridcolor="rgba(31,51,71,0.7)", gridwidth=1, zeroline=False),
            yaxis=dict(gridcolor="rgba(31,51,71,0.7)", gridwidth=1, zeroline=False),
        )
        st.plotly_chart(temp_fig, use_container_width=True)

    with c2:
        st.markdown("<div class='section-title section-title-lg-top'>Power vs Time</div>", unsafe_allow_html=True)
        power_fig = go.Figure()
        power_fig.add_trace(
            go.Scatter(
                x=df["created_at"],
                y=df["power_w"],
                mode="lines",
                name="Power (W)",
                line=dict(color="#22d3ee", width=2.5),
                fill="tozeroy",
                fillcolor="rgba(34,211,238,0.12)",
                customdata=df["fan_mode"],
                hovertemplate="<b>%{x|%H:%M:%S}</b><br>Power: %{y:.3f} W<br>Mode: %{customdata}<extra></extra>",
            )
        )
        power_fig.update_layout(
            xaxis_title="Time (LA)",
            yaxis_title="Power (W)",
            margin=dict(l=10, r=10, t=8, b=10),
            height=300,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#dbe7f3"),
            legend=dict(orientation="h", y=1.05, x=0),
            xaxis=dict(gridcolor="rgba(31,51,71,0.7)", gridwidth=1, zeroline=False),
            yaxis=dict(gridcolor="rgba(31,51,71,0.7)", gridwidth=1, zeroline=False),
        )
        st.plotly_chart(power_fig, use_container_width=True)

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Baseline vs Adaptive Energy</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='section-subtitle'>Cumulative energy usage: adaptive system vs constant baseline over the analysis window.</div>",
        unsafe_allow_html=True,
    )

    df_sorted = df.copy().sort_values("created_at")
    df_sorted["dt_h"] = df_sorted["created_at"].diff().dt.total_seconds().clip(lower=0).fillna(0) / 3600.0
    df_sorted["dt_h"] = df_sorted["dt_h"].where(df_sorted["dt_h"] * 3600.0 <= max_gap_seconds, 0.0)
    df_sorted["actual_cumkwh"]   = (df_sorted["power_w"].astype(float) * df_sorted["dt_h"] / 1000.0).cumsum()
    df_sorted["baseline_cumkwh"] = (float(BASELINE_W) * df_sorted["dt_h"] / 1000.0).cumsum()

    energy_fig = go.Figure()
    energy_fig.add_trace(go.Scatter(
        x=df_sorted["created_at"],
        y=df_sorted["baseline_cumkwh"],
        mode="lines",
        name=f"Baseline ({float(BASELINE_W):.2f}W constant)",
        line=dict(color="#ef4444", width=2, dash="dash"),
        hovertemplate="<b>%{x|%H:%M:%S}</b><br>Baseline: %{y:.5f} kWh<extra></extra>",
    ))
    energy_fig.add_trace(go.Scatter(
        x=df_sorted["created_at"],
        y=df_sorted["actual_cumkwh"],
        mode="lines",
        name="Adaptive system",
        line=dict(color="#22c55e", width=2.5),
        fill="tonexty",
        fillcolor="rgba(34,197,94,0.08)",
        hovertemplate="<b>%{x|%H:%M:%S}</b><br>Adaptive: %{y:.5f} kWh<extra></extra>",
    ))
    energy_fig.update_layout(
        xaxis_title="Time (LA)",
        yaxis_title="Cumulative energy (kWh)",
        margin=dict(l=10, r=10, t=8, b=10),
        height=300,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#dbe7f3"),
        legend=dict(orientation="h", y=1.06, x=0),
        xaxis=dict(gridcolor="rgba(31,51,71,0.7)", gridwidth=1, zeroline=False),
        yaxis=dict(gridcolor="rgba(31,51,71,0.7)", gridwidth=1, zeroline=False),
    )
    st.plotly_chart(energy_fig, use_container_width=True)

    # --- Footer ---
    st.markdown(
        f"""
        <div style='
          border-top: 1px solid #1f3347;
          margin-top: 18px;
          padding: 10px 2px 4px 2px;
          display: flex;
          justify-content: space-between;
          align-items: center;
          flex-wrap: wrap;
          gap: 6px;
        '>
          <div style='display:flex;gap:18px;flex-wrap:wrap;'>
            <span style='font-size:0.74rem;color:#9fb3c8;'>
              Device: <span style='color:#e6edf7;font-weight:500;'>{DEVICE_ID.strip() or "all"}</span>
            </span>
            <span style='font-size:0.74rem;color:#9fb3c8;'>
              Source: <span style='color:#e6edf7;font-weight:500;'>Supabase · fan_readings</span>
            </span>
            <span style='font-size:0.74rem;color:#9fb3c8;'>
              Window: <span style='color:#e6edf7;font-weight:500;'>{WINDOW_HOURS}h</span>
            </span>
          </div>
          <div style='font-size:0.74rem;color:#4b5563;'>
            Last updated: <span style='color:#9fb3c8;'>{last['created_at'].strftime('%Y-%m-%d %H:%M:%S')} PT</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# --- Auto refresh ---
time.sleep(REFRESH_SEC)
st.rerun()
