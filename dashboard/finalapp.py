import time
from datetime import date

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import streamlit as st
from supabase import create_client

st.set_page_config(
    page_title="Weather-Adaptive IoT Energy Monitor",
    page_icon=":material/bolt:",
    layout="wide",
    initial_sidebar_state="collapsed",
)

ACCENT = "#615fff"
TEMP_C = "#f59e0b"
POWER_C = "#38bdf8"
SAVE_C = "#34d399"
WARN_C = "#f87171"
MUTED = "#94a3b8"
TEXT = "#e2e8f0"
TEXT_DIM = "#cbd5e1"
BORDER = "#314158"
BORDER_HI = "#475569"
BG = "#1d293d"
BG_ELEV = "#0f172b"

MODE_COLORS = {
    "OFF": "#64748b",
    "LOW": SAVE_C,
    "MEDIUM": ACCENT,
    "HIGH": WARN_C,
}

st.markdown(
    f"""
    <style>
      .block-container {{
        padding-top: 1.25rem !important;
        padding-bottom: 1rem !important;
      }}
      header[data-testid="stHeader"] {{ background: transparent !important; }}
      [data-testid="stToolbar"] {{ background: transparent !important; }}

      [data-testid="stMetricValue"] {{
        font-family: "Space Grotesk", sans-serif;
        font-size: 1.9rem;
        font-weight: 400;
        letter-spacing: -0.015em;
      }}
      [data-testid="stMetricLabel"] {{
        color: {MUTED};
        font-weight: 300;
        font-size: 0.82rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
      }}

      .mode-badge {{
        display: inline-block;
        border-radius: 6px;
        padding: 2px 10px;
        font-size: 0.75rem;
        font-weight: 500;
        letter-spacing: 0.05em;
      }}
      .mode-table {{
        width: 100%;
        border-collapse: collapse;
        font-size: 0.85rem;
      }}
      .mode-table th {{
        color: {MUTED};
        font-weight: 400;
        text-align: left;
        padding: 6px 8px;
        border-bottom: 1px solid {BORDER};
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
      }}
      .mode-table td {{
        padding: 8px;
        border-bottom: 1px solid rgba(49,65,88,0.5);
        color: {TEXT_DIM};
        font-size: 0.86rem;
      }}
      .readings-scroll {{
        max-height: 300px;
        overflow-y: auto;
        scrollbar-width: thin;
        scrollbar-color: {BORDER} transparent;
      }}

      .hero-wrap {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
        margin-bottom: 6px;
      }}
      .live-badge {{
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(97,95,255,0.12);
        border: 1px solid rgba(97,95,255,0.45);
        border-radius: 999px;
        padding: 5px 14px;
        font-size: 0.74rem;
        color: {ACCENT};
        letter-spacing: 0.12em;
        text-transform: uppercase;
      }}
      .live-dot {{
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: {ACCENT};
        box-shadow: 0 0 10px rgba(97,95,255,0.7);
        animation: pulse 1.6s ease-in-out infinite;
      }}
      @keyframes pulse {{
        0%, 100% {{ opacity: 1; transform: scale(1); }}
        50%       {{ opacity: 0.4; transform: scale(0.7); }}
      }}

      .section-lead {{
        color: {MUTED};
        font-size: 0.86rem;
        font-weight: 300;
        margin: -4px 0 10px 0;
        line-height: 1.55;
      }}

      /* tighten bordered containers */
      [data-testid="stVerticalBlockBorderWrapper"] > div:first-child {{
        padding: 10px 14px 10px !important;
      }}

      /* reduce gap between stacked elements */
      [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"] {{
        gap: 0.35rem !important;
      }}

      /* tighten column gaps */
      [data-testid="stHorizontalBlock"] {{
        gap: 0.5rem !important;
      }}

      /* reduce element vertical gaps */
      .element-container {{
        margin-bottom: 0 !important;
      }}

      /* tighten stMarkdown inside containers */
      [data-testid="stVerticalBlockBorderWrapper"] .stMarkdown p,
      [data-testid="stVerticalBlockBorderWrapper"] .stMarkdown div {{
        margin-bottom: 0 !important;
      }}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="hero-wrap">'
    '<div style="display:flex;flex-direction:column;gap:2px;">'
    '<div style="font-size:0.72rem;color:#94a3b8;letter-spacing:0.18em;text-transform:uppercase;">IoT Telemetry</div>'
    '</div>'
    '<div class="live-badge"><div class="live-dot"></div>LIVE</div>'
    '</div>',
    unsafe_allow_html=True,
)

"""
# :material/bolt: Weather-Adaptive Energy Monitor
"""

st.markdown(
    '<div class="section-lead">Live ESP32 fan telemetry streamed through Supabase. '
    'Adjust the controls below, then scroll down to see real-time readings, mode distribution, '
    'and baseline-vs-adaptive energy savings.</div>',
    unsafe_allow_html=True,
)

# --- Secrets ---
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
sb = create_client(SUPABASE_URL, SUPABASE_KEY)


# --- Demo preset ---
_DEMO_DEFAULTS = {
    "ctrl_refresh":    3,
    "ctrl_limit":      500,
    "ctrl_window_h":   24,
    "ctrl_gap_min":    30,
    "ctrl_baseline_w": 2.949,
    "ctrl_price_kwh":  0.16,
}

# Real-world average residential electricity rates (USD/kWh, EIA / IEA 2024)
DEMO_MARKETS = {
    "US Average":  (0.16,  "EIA 2024 national avg"),
    "California":  (0.29,  "EIA 2024 – CA residential"),
    "New York":    (0.22,  "EIA 2024 – NY residential"),
    "Texas":       (0.13,  "EIA 2024 – TX residential"),
    "Florida":     (0.13,  "EIA 2024 – FL residential"),
    "Hawaii":      (0.44,  "EIA 2024 – HI residential (highest US)"),
    "UK":          (0.30,  "Ofgem 2024 unit rate"),
    "EU Average":  (0.28,  "Eurostat 2024 avg"),
    "Germany":     (0.35,  "BDEW 2024 household rate"),
    "Australia":   (0.20,  "AEMC 2024 avg – AUD converted"),
    "Japan":       (0.21,  "METI 2024 avg household"),
}

# --- Top control panel ---
is_demo = st.session_state.get("demo_mode", False)

with st.container(border=True):
    hdr_col, demo_col = st.columns([5, 1])
    with hdr_col:
        label = "DEMO MODE" if is_demo else "CONTROLS"
        st.markdown(
            f'<div style="color:{ACCENT if is_demo else MUTED};font-size:0.72rem;letter-spacing:0.14em;'
            f'text-transform:uppercase;margin-bottom:8px;">{label}</div>',
            unsafe_allow_html=True,
        )
    with demo_col:
        btn_label = "Exit Demo" if is_demo else "Demo Mode"
        if st.button(btn_label, use_container_width=True):
            st.session_state["demo_mode"] = not is_demo
            if not is_demo:
                for k, v in _DEMO_DEFAULTS.items():
                    st.session_state[k] = v
            st.rerun()

    col_live, col_window, col_savings = st.columns(3)

    if not is_demo:
        with col_live:
            st.markdown(f'<div style="color:{TEXT};font-size:0.9rem;margin-bottom:4px;">Live stream</div>', unsafe_allow_html=True)
            DEVICE_ID   = st.text_input("device_id filter", value="esp32_01", key="ctrl_device_id")
            REFRESH_SEC = st.slider("Refresh interval (s)", 1, 10, 3, key="ctrl_refresh")
    else:
        DEVICE_ID = "demo"
        with col_live:
            st.markdown(f'<div style="color:{TEXT};font-size:0.9rem;margin-bottom:4px;">Simulation</div>', unsafe_allow_html=True)
            if "ctrl_num_fans" not in st.session_state:
                st.session_state["ctrl_num_fans"] = 1
            NUM_FANS = st.slider("Number of fans", 1, 10, key="ctrl_num_fans")
            REFRESH_SEC = st.slider("Refresh interval (s)", 1, 10, 3, key="ctrl_refresh")

    with col_window:
        st.markdown(f'<div style="color:{TEXT};font-size:0.9rem;margin-bottom:4px;">Analysis window</div>', unsafe_allow_html=True)
        LIMIT        = st.slider("Rows to display", 50, 1000, 500, key="ctrl_limit")
        WINDOW_HOURS = st.slider("Window (hours)", 1, 168, 24, key="ctrl_window_h")
        MAX_GAP_MIN  = st.slider("Ignore gaps > (minutes)", 1, 180, 30, key="ctrl_gap_min")

    with col_savings:
        if is_demo:
            st.markdown(f'<div style="color:{TEXT};font-size:0.9rem;margin-bottom:4px;">Electricity market</div>', unsafe_allow_html=True)
            market_key = st.selectbox(
                "Region / market", list(DEMO_MARKETS.keys()),
                index=0, key="ctrl_demo_market",
            )
            PRICE_PER_KWH, market_note = DEMO_MARKETS[market_key]
            BASELINE_W = 2.949
            st.markdown(
                f'<div style="color:{MUTED};font-size:0.75rem;margin-top:4px;">'
                f'{market_note}<br>'
                f'<span style="color:{TEXT_DIM};">${PRICE_PER_KWH:.2f}/kWh</span>'
                f'</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(f'<div style="color:{TEXT};font-size:0.9rem;margin-bottom:4px;">Savings assumptions</div>', unsafe_allow_html=True)
            BASELINE_W = st.number_input(
                "Baseline power (W, e.g. HIGH mode)", min_value=0.0, value=2.949, step=0.1,
                key="ctrl_baseline_w",
            )
            PRICE_PER_KWH = st.number_input(
                "Electricity price ($/kWh)", min_value=0.0, value=0.16, step=0.01,
                key="ctrl_price_kwh",
            )

if not is_demo:
    NUM_FANS = 1


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


@st.cache_data(ttl=3600)
def generate_demo_df(window_hours: int = 24, interval_s: int = 30) -> pd.DataFrame:
    """Synthetic 24-hour fan telemetry based on average small desk-fan specs."""
    import numpy as np
    rng = np.random.default_rng(7)
    now = pd.Timestamp.now().floor("s")
    n = int(window_hours * 3600 / interval_s)
    timestamps = [now - pd.Timedelta(seconds=(n - i) * interval_s) for i in range(n)]

    # Realistic daily temperature cycle: cool morning, hot afternoon
    hours = np.array([(t.hour + t.minute / 60.0) for t in timestamps])
    temp_c = 22.0 + 10.0 * np.clip(np.sin((hours - 6.0) * np.pi / 14.0), 0, 1)
    temp_c += rng.normal(0, 0.3, n)

    # Mode thresholds
    med_c  = 27.0
    high_c = 30.5
    modes = np.where(temp_c >= high_c, "HIGH",
            np.where(temp_c >= med_c, "MEDIUM",
            np.where(temp_c >= 24.0, "LOW", "OFF")))

    # Average real-world power per mode (small USB/DC desk fan)
    power_map = {"OFF": 0.08, "LOW": 0.95, "MEDIUM": 1.47, "HIGH": 2.949}
    power_w = np.array([power_map[m] for m in modes])
    power_w += rng.normal(0, 0.015, n)
    power_w = np.clip(power_w, 0.0, None)

    return pd.DataFrame({
        "created_at": timestamps,
        "temp_c":     temp_c,
        "power_w":    power_w,
        "fan_mode":   modes,
        "device_id":  "demo",
    })


# --- Data fetch ---
if is_demo:
    df_all = generate_demo_df(window_hours=WINDOW_HOURS)
else:
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
    st.warning(f"Weather fetch failed: {e}", icon=":material/cloud_off:")
    outdoor_now_f, outdoor_peak_f = None, None

if outdoor_now_f is not None and outdoor_peak_f is not None:
    med_threshold_f, high_threshold_f = weather_thresholds(outdoor_now_f, outdoor_peak_f)
else:
    med_threshold_f, high_threshold_f = None, None

if df.empty:
    st.warning("No rows found yet. Make sure ESP32 is inserting into `fan_readings` and device_id matches.")
else:
    last = df.iloc[-1]
    indoor_f = c_to_f(float(last["temp_c"]))

    # --- Staleness / demo badge ---
    if is_demo:
        fans_label = f"{NUM_FANS} fan{'s' if NUM_FANS > 1 else ''}"
        st.markdown(
            f'<div class="hero-wrap" style="margin-top:4px;"><div></div>'
            f'<div style="display:inline-flex;align-items:center;gap:8px;'
            f'background:rgba(97,95,255,0.14);border:1px solid rgba(97,95,255,0.5);'
            f'border-radius:999px;padding:5px 14px;font-size:0.74rem;color:{ACCENT};'
            f'letter-spacing:0.08em;text-transform:uppercase;">'
            f'<div style="width:8px;height:8px;border-radius:50%;background:{ACCENT};"></div>'
            f'DEMO · {fans_label} · synthetic data</div></div>',
            unsafe_allow_html=True,
        )
    else:
        staleness_s = (pd.Timestamp.now() - last["created_at"]).total_seconds()
        if staleness_s > 60:
            stale_label = f"OFFLINE · last seen {format_duration(staleness_s)} ago"
            st.markdown(
                f'<div class="hero-wrap" style="margin-top:4px;"><div></div>'
                f'<div style="display:inline-flex;align-items:center;gap:8px;'
                f'background:rgba(248,113,113,0.12);border:1px solid rgba(248,113,113,0.45);'
                f'border-radius:999px;padding:5px 14px;font-size:0.74rem;color:{WARN_C};'
                f'letter-spacing:0.08em;text-transform:uppercase;">'
                f'<div style="width:8px;height:8px;border-radius:50%;background:{WARN_C};"></div>'
                f'{stale_label}</div></div>',
                unsafe_allow_html=True,
            )

    max_gap_seconds = float(MAX_GAP_MIN * 60)
    dt_s = df["created_at"].diff().dt.total_seconds().clip(lower=0).fillna(0)
    active_dt_s = dt_s.where(dt_s <= max_gap_seconds, 0.0)

    window_seconds = float(active_dt_s.sum())
    avg_interval_seconds = df["created_at"].diff().dt.total_seconds().dropna().mean()
    avg_interval_seconds = float(avg_interval_seconds) if pd.notna(avg_interval_seconds) else 0.0

    # Per-fan metrics, then scaled by NUM_FANS for display
    actual_kwh_1  = energy_kwh_from_power(df, max_gap_seconds=max_gap_seconds)
    base_kwh_1    = baseline_kwh_constant(df, float(BASELINE_W), max_gap_seconds=max_gap_seconds)
    saved_kwh_1   = max(0.0, base_kwh_1 - actual_kwh_1)
    pct_saved     = (saved_kwh_1 / base_kwh_1 * 100.0) if base_kwh_1 > 0 else 0.0

    actual_kwh = actual_kwh_1 * NUM_FANS
    base_kwh   = base_kwh_1   * NUM_FANS
    saved_kwh  = saved_kwh_1  * NUM_FANS
    cost_used  = actual_kwh * float(PRICE_PER_KWH)
    cost_saved = saved_kwh  * float(PRICE_PER_KWH)

    spark_temp  = make_sparkline(df["temp_c"].tolist()[-40:], TEMP_C)
    spark_power = make_sparkline(df["power_w"].tolist()[-40:], POWER_C)

    current_mode = str(last.get("fan_mode", "—"))
    mode_color = MODE_COLORS.get(current_mode, MUTED)
    outdoor_str = f"{outdoor_now_f:.0f}°F" if outdoor_now_f is not None else "—"
    outdoor_peak_str = f"{outdoor_peak_f:.0f}°F" if outdoor_peak_f is not None else "—"

    # Rolling averages for charts
    df["temp_roll"]  = df["temp_c"].rolling(10, min_periods=1).mean()
    df["power_roll"] = df["power_w"].rolling(10, min_periods=1).mean()

    # Shared chart layout
    _chart_layout = dict(
        margin=dict(l=10, r=10, t=8, b=10),
        height=300,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=TEXT_DIM, family="Space Grotesk, sans-serif", size=12),
        legend=dict(orientation="h", y=1.05, x=0, font=dict(color=MUTED)),
        xaxis=dict(gridcolor="rgba(49,65,88,0.6)", gridwidth=1, zeroline=False,
                   title_font=dict(color=MUTED, size=11), tickfont=dict(color=TEXT_DIM, size=10)),
        yaxis=dict(gridcolor="rgba(49,65,88,0.6)", gridwidth=1, zeroline=False,
                   title_font=dict(color=MUTED, size=11), tickfont=dict(color=TEXT_DIM, size=10)),
        hoverlabel=dict(bgcolor=BG_ELEV, bordercolor=BORDER_HI, font=dict(color=TEXT, family="Space Grotesk")),
    )

    # Weather thresholds bar (above tabs)
    if med_threshold_f is not None:
        st.markdown(
            f'<div style="display:flex;gap:18px;flex-wrap:wrap;align-items:center;'
            f'padding:8px 14px;margin:8px 0 4px;border:1px solid {BORDER};'
            f'border-radius:10px;background:{BG_ELEV};font-size:0.84rem;color:{TEXT_DIM};">'
            f'<span style="color:{MUTED};letter-spacing:0.12em;text-transform:uppercase;font-size:0.72rem;">Weather thresholds</span>'
            f'<span><span style="color:{MUTED};">Now</span> <strong style="color:{TEXT};">{outdoor_now_f:.0f}°F</strong></span>'
            f'<span><span style="color:{MUTED};">Peak</span> <strong style="color:{TEXT};">{outdoor_peak_f:.0f}°F</strong></span>'
            f'<span style="color:{ACCENT};">MED ≥ {med_threshold_f:.0f}°F</span>'
            f'<span style="color:{WARN_C};">HIGH ≥ {high_threshold_f:.0f}°F</span>'
            f'</div>',
            unsafe_allow_html=True,
        )

    # ------------------------------------------------------------------ TABS
    tab_overview, tab_charts, tab_energy, tab_data = st.tabs(
        ["Overview", "Charts", "Energy", "Data"]
    )

    # ================================================================ OVERVIEW
    with tab_overview:
        st.markdown(
            f'<div style="color:{MUTED};font-size:0.72rem;letter-spacing:0.14em;'
            f'text-transform:uppercase;margin:10px 0 6px;">Live Status</div>',
            unsafe_allow_html=True,
        )
        b1, b2, b3, b4 = st.columns(4)
        with b1:
            with st.container(border=True):
                st.markdown(f'<div style="color:{MUTED};font-size:0.72rem;letter-spacing:0.08em;text-transform:uppercase;">Indoor Temp</div>', unsafe_allow_html=True)
                st.markdown(f'<div style="font-size:1.9rem;font-weight:400;color:{TEMP_C};line-height:1.1;margin-top:2px;">{indoor_f:.1f}°F</div>', unsafe_allow_html=True)
                st.markdown(f'<div style="color:{TEXT_DIM};font-size:0.78rem;">{float(last["temp_c"]):.1f}°C</div>{spark_temp}', unsafe_allow_html=True)
        with b2:
            with st.container(border=True):
                st.markdown(f'<div style="color:{MUTED};font-size:0.72rem;letter-spacing:0.08em;text-transform:uppercase;">Outdoor</div>', unsafe_allow_html=True)
                st.markdown(f'<div style="font-size:1.9rem;font-weight:400;color:{TEXT};line-height:1.1;margin-top:2px;">{outdoor_str}</div>', unsafe_allow_html=True)
                st.markdown(f'<div style="color:{TEXT_DIM};font-size:0.78rem;">Peak today: {outdoor_peak_str}</div>', unsafe_allow_html=True)
        with b3:
            with st.container(border=True):
                st.markdown(f'<div style="color:{MUTED};font-size:0.72rem;letter-spacing:0.08em;text-transform:uppercase;">Fan Mode</div>', unsafe_allow_html=True)
                st.markdown(
                    f'<div style="display:flex;align-items:center;gap:8px;margin-top:2px;">'
                    f'<div style="width:10px;height:10px;border-radius:50%;background:{mode_color};box-shadow:0 0 10px {mode_color}aa;"></div>'
                    f'<div style="font-size:1.9rem;font-weight:400;color:{mode_color};line-height:1.1;">{current_mode}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
                st.markdown(f'<div style="color:{TEXT_DIM};font-size:0.78rem;">{float(last["power_w"]) * NUM_FANS:.3f} W total</div>', unsafe_allow_html=True)
        with b4:
            with st.container(border=True):
                st.markdown(f'<div style="color:{MUTED};font-size:0.72rem;letter-spacing:0.08em;text-transform:uppercase;">Energy Saved</div>', unsafe_allow_html=True)
                st.markdown(f'<div style="font-size:1.9rem;font-weight:400;color:{SAVE_C};line-height:1.1;margin-top:2px;">{pct_saved:.1f}%</div>', unsafe_allow_html=True)
                st.markdown(f'<div style="color:{TEXT_DIM};font-size:0.78rem;">{format_cost(cost_saved)} at ${float(PRICE_PER_KWH):.2f}/kWh</div>', unsafe_allow_html=True)

        st.markdown(
            f'<div style="color:{MUTED};font-size:0.72rem;letter-spacing:0.14em;'
            f'text-transform:uppercase;margin:12px 0 6px;">Detailed Metrics</div>',
            unsafe_allow_html=True,
        )
        k1, k2, k3, k4 = st.columns(4)
        with k1:
            with st.container(border=True):
                st.markdown(f'<div style="color:{MUTED};font-size:0.72rem;letter-spacing:0.08em;text-transform:uppercase;">Current Power</div>', unsafe_allow_html=True)
                current_power_disp = float(last["power_w"]) * NUM_FANS
                power_label = f"{current_power_disp:.3f} W" + (f" ({NUM_FANS}×)" if NUM_FANS > 1 else "")
                st.markdown(f'<div style="font-size:1.7rem;font-weight:400;color:{POWER_C};line-height:1.1;margin-top:2px;">{power_label}</div>{spark_power}', unsafe_allow_html=True)
        with k2:
            with st.container(border=True):
                st.markdown(f'<div style="color:{MUTED};font-size:0.72rem;letter-spacing:0.08em;text-transform:uppercase;">Adaptive Energy</div>', unsafe_allow_html=True)
                st.markdown(f'<div style="font-size:1.7rem;font-weight:400;color:{ACCENT};line-height:1.1;margin-top:2px;">{actual_kwh:.4f} kWh</div>', unsafe_allow_html=True)
        with k3:
            with st.container(border=True):
                st.markdown(f'<div style="color:{MUTED};font-size:0.72rem;letter-spacing:0.08em;text-transform:uppercase;">Baseline Energy</div>', unsafe_allow_html=True)
                st.markdown(f'<div style="font-size:1.7rem;font-weight:400;color:{WARN_C};line-height:1.1;margin-top:2px;">{base_kwh:.4f} kWh</div>', unsafe_allow_html=True)
        with k4:
            with st.container(border=True):
                st.markdown(f'<div style="color:{MUTED};font-size:0.72rem;letter-spacing:0.08em;text-transform:uppercase;">Energy Saved</div>', unsafe_allow_html=True)
                st.markdown(f'<div style="font-size:1.7rem;font-weight:400;color:{SAVE_C};line-height:1.1;margin-top:2px;">{saved_kwh:.4f} kWh</div>', unsafe_allow_html=True)
                st.markdown(f'<div style="color:{SAVE_C};font-size:0.78rem;">+{format_cost(cost_saved)} saved</div>', unsafe_allow_html=True)

        d1, d2, d3, d4 = st.columns(4)
        with d1:
            with st.container(border=True):
                st.markdown(f'<div style="color:{MUTED};font-size:0.72rem;letter-spacing:0.08em;text-transform:uppercase;">Analysis Window</div>', unsafe_allow_html=True)
                st.markdown(f'<div style="font-size:1.35rem;font-weight:400;color:{TEXT};line-height:1.1;margin-top:2px;">{format_duration(window_seconds)}</div>', unsafe_allow_html=True)
        with d2:
            with st.container(border=True):
                st.markdown(f'<div style="color:{MUTED};font-size:0.72rem;letter-spacing:0.08em;text-transform:uppercase;">Avg Sample Interval</div>', unsafe_allow_html=True)
                st.markdown(f'<div style="font-size:1.35rem;font-weight:400;color:{TEXT};line-height:1.1;margin-top:2px;">{avg_interval_seconds:.1f}s</div>', unsafe_allow_html=True)
        with d3:
            with st.container(border=True):
                st.markdown(f'<div style="color:{MUTED};font-size:0.72rem;letter-spacing:0.08em;text-transform:uppercase;">Cost Used</div>', unsafe_allow_html=True)
                st.markdown(f'<div style="font-size:1.35rem;font-weight:400;color:{TEXT};line-height:1.1;margin-top:2px;">{format_cost(cost_used)}</div>', unsafe_allow_html=True)
        with d4:
            with st.container(border=True):
                st.markdown(f'<div style="color:{MUTED};font-size:0.72rem;letter-spacing:0.08em;text-transform:uppercase;">Last Reading</div>', unsafe_allow_html=True)
                st.markdown(f'<div style="font-size:1.35rem;font-weight:400;color:{TEXT};line-height:1.1;margin-top:2px;">{last["created_at"].strftime("%H:%M:%S")}</div>', unsafe_allow_html=True)

        # Mode breakdown (donut + table) in overview
        st.markdown(f"<hr style='border:none;border-top:1px solid {BORDER};margin:12px 0 6px;'>", unsafe_allow_html=True)
        st.markdown(f'<div style="color:{MUTED};font-size:0.72rem;letter-spacing:0.14em;text-transform:uppercase;margin:4px 0 6px;">Mode Breakdown</div>', unsafe_allow_html=True)
        _ov_left, _ov_right = st.columns([1.6, 1.2])
        with _ov_left:
            d_mode = df.copy().sort_values("created_at")
            d_mode["dt_s"] = d_mode["created_at"].diff().dt.total_seconds().clip(lower=0).fillna(0)
            d_mode["dt_s"] = d_mode["dt_s"].where(d_mode["dt_s"] <= max_gap_seconds, 0.0)
            d_mode["mode_for_interval"] = d_mode["fan_mode"].shift(1).fillna(d_mode["fan_mode"])
            mode_seconds = d_mode.groupby("mode_for_interval")["dt_s"].sum().sort_values(ascending=False)
            total_s = mode_seconds.sum()
            if total_s > 0:
                mode_pct = (mode_seconds / total_s * 100.0).round(1)
                labels = mode_pct.index.astype(str).tolist()
                colors_donut = [MODE_COLORS.get(m, "#9ca3af") for m in labels]
                donut = go.Figure(go.Pie(
                    labels=labels, values=mode_pct.values, hole=0.62,
                    marker=dict(colors=colors_donut, line=dict(color=BG, width=2)),
                    textinfo="percent",
                    textfont=dict(size=12, color=TEXT, family="Space Grotesk"),
                    hovertemplate="<b>%{label}</b>: %{value:.1f}%<extra></extra>",
                ))
                donut.update_layout(
                    margin=dict(l=0, r=0, t=0, b=0), height=260,
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color=TEXT_DIM, family="Space Grotesk, sans-serif"),
                    legend=dict(orientation="v", y=0.5, x=1.0, xanchor="left", yanchor="middle",
                                font=dict(size=11, color=TEXT_DIM)),
                    hoverlabel=dict(bgcolor=BG_ELEV, bordercolor=BORDER_HI, font=dict(color=TEXT, family="Space Grotesk")),
                )
                st.plotly_chart(donut, use_container_width=True)
            else:
                st.info("Not enough data for mode breakdown.")
        with _ov_right:
            if total_s > 0:
                rows_html = ""
                for mode, pct in mode_pct.items():
                    c = MODE_COLORS.get(str(mode), "#9ca3af")
                    bg = c + "22"
                    rows_html += (
                        f"<tr><td><span class='mode-badge' style='color:{c};background:{bg};'>{mode}</span></td>"
                        f"<td>{mode_seconds[mode]:.0f}s</td><td>{pct:.1f}%</td></tr>"
                    )
                st.markdown(
                    f"<table class='mode-table'><thead><tr><th>Mode</th><th>Seconds</th><th>Share</th></tr></thead>"
                    f"<tbody>{rows_html}</tbody></table>",
                    unsafe_allow_html=True,
                )

        # Fan statistics (computed from full fetch)
        st.markdown(f"<hr style='border:none;border-top:1px solid {BORDER};margin:12px 0 6px;'>", unsafe_allow_html=True)
        st.markdown(f'<div style="color:{MUTED};font-size:0.72rem;letter-spacing:0.14em;text-transform:uppercase;margin:4px 0 6px;">Fan Statistics — all {len(df_all)} readings</div>', unsafe_allow_html=True)

        if not df_all.empty:
            stats = (
                df_all.groupby("fan_mode")["power_w"]
                .agg(avg="mean", mn="min", mx="max", n="count")
                .reset_index()
            )
            temp_stats = df_all.groupby("fan_mode")["temp_c"].mean().rename("avg_temp_c")
            stats = stats.join(temp_stats, on="fan_mode")
            baseline_for_eff = stats.loc[stats["fan_mode"] == "HIGH", "avg"].values
            has_high = len(baseline_for_eff) > 0

            fan_stat_rows = ""
            mode_order = ["OFF", "LOW", "MEDIUM", "HIGH"]
            for m in mode_order:
                row = stats[stats["fan_mode"] == m]
                if row.empty:
                    continue
                r = row.iloc[0]
                mc = MODE_COLORS.get(m, MUTED)
                bg = mc + "22"
                eff_str = "—"
                if has_high and r["avg"] > 0:
                    eff_pct = (1.0 - r["avg"] / baseline_for_eff[0]) * 100.0
                    eff_str = f"{eff_pct:.0f}% less than HIGH" if eff_pct > 0 else "baseline"
                elif m == "HIGH":
                    eff_str = "baseline"
                eff_cell_color = SAVE_C if eff_str not in ("baseline", "—") else MUTED
                fan_stat_rows += (
                    f"<tr>"
                    f"<td><span class='mode-badge' style='color:{mc};background:{bg};'>{m}</span></td>"
                    f"<td style='color:{mc};font-weight:500;'>{r['avg']:.3f} W</td>"
                    f"<td style='color:{TEXT_DIM};'>{r['mn']:.3f} – {r['mx']:.3f} W</td>"
                    f"<td style='color:{TEXT_DIM};'>{r['avg_temp_c']:.1f}°C</td>"
                    f"<td style='color:{MUTED};'>{int(r['n'])}</td>"
                    f"<td style='color:{eff_cell_color};font-size:0.8rem;'>{eff_str}</td>"
                    f"</tr>"
                )
            st.markdown(
                f"<table class='mode-table'>"
                f"<thead><tr><th>Mode</th><th>Avg Power</th><th>Range</th><th>Avg Temp</th><th>Readings</th><th>vs HIGH</th></tr></thead>"
                f"<tbody>{fan_stat_rows}</tbody></table>",
                unsafe_allow_html=True,
            )

    # ================================================================ CHARTS
    with tab_charts:
        _mode_band_colors = {
            "OFF":    "rgba(100,116,139,0.08)",
            "LOW":    "rgba(52,211,153,0.10)",
            "MEDIUM": "rgba(97,95,255,0.08)",
            "HIGH":   "rgba(248,113,113,0.10)",
        }

        def _add_mode_bands(fig, df_src):
            _df_b = df_src[["created_at", "fan_mode"]].copy()
            _i = 0
            while _i < len(_df_b) - 1:
                _m = str(_df_b.iloc[_i]["fan_mode"])
                _x0 = _df_b.iloc[_i]["created_at"]
                _j = _i + 1
                while _j < len(_df_b) and str(_df_b.iloc[_j]["fan_mode"]) == _m:
                    _j += 1
                _x1 = _df_b.iloc[min(_j, len(_df_b) - 1)]["created_at"]
                fig.add_vrect(x0=_x0, x1=_x1,
                    fillcolor=_mode_band_colors.get(_m, "rgba(0,0,0,0)"),
                    line_width=0, layer="below")
                _i = _j

        c1, c2 = st.columns(2)

        with c1:
            st.markdown(f'<div style="color:{TEXT};font-size:1rem;font-weight:500;margin-bottom:4px;">Temperature vs Time</div>', unsafe_allow_html=True)
            legend_items = [("OFF", MODE_COLORS["OFF"]), ("LOW", MODE_COLORS["LOW"]), ("MEDIUM", MODE_COLORS["MEDIUM"]), ("HIGH", MODE_COLORS["HIGH"])]
            legend_html = "".join(
                f"<span style='display:flex;align-items:center;gap:5px;font-size:0.74rem;color:{lc};'>"
                f"<span style='width:10px;height:10px;border-radius:2px;background:{lc}22;border:1px solid {lc}66;display:inline-block;'></span>{lm}"
                f"</span>"
                for lm, lc in legend_items
            )
            st.markdown(f"<div style='display:flex;gap:12px;padding-left:2px;margin-bottom:4px;flex-wrap:wrap;'>{legend_html}</div>", unsafe_allow_html=True)
            temp_fig = go.Figure()
            _add_mode_bands(temp_fig, df)
            temp_fig.add_trace(go.Scatter(
                x=df["created_at"], y=df["temp_c"], mode="lines", name="Indoor temp",
                line=dict(color=TEMP_C, width=2.5, shape="spline", smoothing=0.6),
                fill="tozeroy", fillcolor="rgba(245,158,11,0.10)",
                customdata=df["fan_mode"],
                hovertemplate="<b>%{x|%H:%M:%S}</b><br>%{y:.1f}°C · %{customdata}<extra></extra>",
            ))
            temp_fig.add_trace(go.Scatter(
                x=df["created_at"], y=df["temp_roll"], mode="lines", name="10-pt avg",
                line=dict(color=TEMP_C, width=1.5, dash="dot"),
                opacity=0.5, showlegend=True,
                hovertemplate="<b>%{x|%H:%M:%S}</b><br>Avg: %{y:.1f}°C<extra></extra>",
            ))
            if med_threshold_f is not None:
                med_c = (med_threshold_f - 32.0) * 5.0 / 9.0
                high_c = (high_threshold_f - 32.0) * 5.0 / 9.0
                temp_fig.add_hline(y=med_c, line_dash="dot", line_color=ACCENT,
                                   annotation_text="MED", annotation_font_color=ACCENT)
                temp_fig.add_hline(y=high_c, line_dash="dash", line_color=WARN_C,
                                   annotation_text="HIGH", annotation_font_color=WARN_C)
            if outdoor_now_f is not None:
                outdoor_c = (outdoor_now_f - 32.0) * 5.0 / 9.0
                temp_fig.add_hline(y=outdoor_c, line_dash="longdash", line_color=MUTED,
                                   annotation_text=f"Outdoor {outdoor_now_f:.0f}°F",
                                   annotation_font_color=MUTED)
            temp_fig.update_layout(xaxis_title="Time (LA)", yaxis_title="Temp (°C)", **_chart_layout)
            st.plotly_chart(temp_fig, use_container_width=True)

        with c2:
            st.markdown(f'<div style="color:{TEXT};font-size:1rem;font-weight:500;margin-bottom:4px;">Power vs Time</div>', unsafe_allow_html=True)
            power_fig = go.Figure()
            power_fig.add_trace(go.Scatter(
                x=df["created_at"], y=df["power_w"], mode="lines", name="Power",
                line=dict(color=POWER_C, width=2.5, shape="spline", smoothing=0.6),
                fill="tozeroy", fillcolor="rgba(56,189,248,0.10)",
                customdata=df["fan_mode"],
                hovertemplate="<b>%{x|%H:%M:%S}</b><br>%{y:.3f} W · %{customdata}<extra></extra>",
            ))
            power_fig.add_trace(go.Scatter(
                x=df["created_at"], y=df["power_roll"], mode="lines", name="10-pt avg",
                line=dict(color=POWER_C, width=1.5, dash="dot"),
                opacity=0.5, showlegend=True,
                hovertemplate="<b>%{x|%H:%M:%S}</b><br>Avg: %{y:.3f} W<extra></extra>",
            ))
            power_fig.update_layout(xaxis_title="Time (LA)", yaxis_title="Power (W)", **_chart_layout)
            st.plotly_chart(power_fig, use_container_width=True)

        # Temp vs Power scatter — uses full fetch (df_all) so short windows still show meaningful data
        st.markdown(f"<hr style='border:none;border-top:1px solid {BORDER};margin:12px 0 6px;'>", unsafe_allow_html=True)
        st.markdown(f'<div style="color:{TEXT};font-size:1rem;font-weight:500;margin-bottom:2px;">Temperature vs Power</div>', unsafe_allow_html=True)
        scatter_n = len(df_all)
        st.markdown(
            f'<div class="section-lead">All {scatter_n} fetched readings colored by fan mode — shows where the algorithm switches. '
            f'Jitter applied to separate overlapping discrete power levels.</div>',
            unsafe_allow_html=True,
        )

        import numpy as np
        rng = np.random.default_rng(42)
        scatter_fig = go.Figure()
        for mode_name, mc in MODE_COLORS.items():
            mask = df_all["fan_mode"] == mode_name
            if mask.any():
                xs = df_all.loc[mask, "temp_c"].astype(float).values
                ys = df_all.loc[mask, "power_w"].astype(float).values
                jitter_y = rng.uniform(-0.015, 0.015, size=len(ys))
                scatter_fig.add_trace(go.Scatter(
                    x=xs,
                    y=ys + jitter_y,
                    mode="markers",
                    name=mode_name,
                    marker=dict(color=mc, size=7, opacity=0.65, line=dict(color=BG_ELEV, width=0.5)),
                    hovertemplate=f"<b>{mode_name}</b><br>Temp: %{{x:.1f}}°C<br>Power: %{{y:.3f}} W<extra></extra>",
                ))
        scatter_layout = {**_chart_layout, "height": 340}
        scatter_layout["legend"] = dict(orientation="h", y=1.05, x=0, font=dict(color=MUTED))
        scatter_fig.update_layout(xaxis_title="Indoor Temp (°C)", yaxis_title="Power (W)", **scatter_layout)
        st.plotly_chart(scatter_fig, use_container_width=True)

    # ================================================================ ENERGY
    with tab_energy:
        st.markdown(f'<div style="color:{TEXT};font-size:1rem;font-weight:500;margin-bottom:2px;">Baseline vs Adaptive Energy</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="section-lead">Cumulative energy: adaptive system vs constant baseline over the analysis window.</div>', unsafe_allow_html=True)

        df_sorted = df.copy().sort_values("created_at")
        df_sorted["dt_h"] = df_sorted["created_at"].diff().dt.total_seconds().clip(lower=0).fillna(0) / 3600.0
        df_sorted["dt_h"] = df_sorted["dt_h"].where(df_sorted["dt_h"] * 3600.0 <= max_gap_seconds, 0.0)
        df_sorted["actual_cumkwh"]   = (df_sorted["power_w"].astype(float) * df_sorted["dt_h"] / 1000.0).cumsum()
        df_sorted["baseline_cumkwh"] = (float(BASELINE_W) * df_sorted["dt_h"] / 1000.0).cumsum()

        energy_fig = go.Figure()
        energy_fig.add_trace(go.Scatter(
            x=df_sorted["created_at"], y=df_sorted["baseline_cumkwh"], mode="lines",
            name=f"Baseline ({float(BASELINE_W):.2f}W constant)",
            line=dict(color=WARN_C, width=2, dash="dash"),
            hovertemplate="<b>%{x|%H:%M:%S}</b><br>Baseline: %{y:.5f} kWh<extra></extra>",
        ))
        energy_fig.add_trace(go.Scatter(
            x=df_sorted["created_at"], y=df_sorted["actual_cumkwh"], mode="lines",
            name="Adaptive system",
            line=dict(color=SAVE_C, width=2.5),
            fill="tonexty", fillcolor="rgba(52,211,153,0.12)",
            hovertemplate="<b>%{x|%H:%M:%S}</b><br>Adaptive: %{y:.5f} kWh<extra></extra>",
        ))
        energy_layout = {**_chart_layout, "height": 320}
        energy_layout["legend"] = dict(orientation="h", y=1.06, x=0, font=dict(color=MUTED))
        energy_fig.update_layout(xaxis_title="Time (LA)", yaxis_title="Cumulative energy (kWh)", **energy_layout)
        st.plotly_chart(energy_fig, use_container_width=True)

        # Projected savings
        st.markdown(f"<hr style='border:none;border-top:1px solid {BORDER};margin:12px 0 6px;'>", unsafe_allow_html=True)
        st.markdown(f'<div style="color:{MUTED};font-size:0.72rem;letter-spacing:0.14em;text-transform:uppercase;margin:4px 0 6px;">Projected Savings</div>', unsafe_allow_html=True)
        rate_per_hour = saved_kwh / max(window_seconds / 3600.0, 0.001)
        proj_24h  = rate_per_hour * 24.0 * float(PRICE_PER_KWH)
        proj_30d  = rate_per_hour * 24.0 * 30.0 * float(PRICE_PER_KWH)
        proj_year = rate_per_hour * 24.0 * 365.0 * float(PRICE_PER_KWH)

        window_hours_actual = window_seconds / 3600.0
        fans_suffix = f" · {NUM_FANS} fan{'s' if NUM_FANS > 1 else ''}" if NUM_FANS > 1 else ""
        if window_hours_actual >= 1.0:
            proj_note = f"Based on {format_duration(window_seconds)} of data{fans_suffix}."
        else:
            proj_note = f"Short window ({format_duration(window_seconds)}){fans_suffix} — extend to 1h+ for accuracy."

        p1, p2, p3 = st.columns(3)
        for col, label, val in [(p1, "Projected 24h", proj_24h), (p2, "Projected 30 days", proj_30d), (p3, "Projected 1 year", proj_year)]:
            with col:
                with st.container(border=True):
                    st.markdown(f'<div style="color:{MUTED};font-size:0.72rem;letter-spacing:0.08em;text-transform:uppercase;">{label}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div style="font-size:1.9rem;font-weight:400;color:{SAVE_C};line-height:1.1;margin-top:2px;">{format_cost(val)}</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div style="color:{MUTED};font-size:0.75rem;margin-top:6px;">{proj_note}</div>',
            unsafe_allow_html=True,
        )

    # ================================================================ DATA
    with tab_data:
        left_d, right_d = st.columns([1.6, 1.2])
        with left_d:
            st.markdown(f'<div style="color:{TEXT};font-size:1rem;font-weight:500;margin-bottom:2px;">Latest Readings</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="section-lead">Most recent 50 points for operational monitoring.</div>', unsafe_allow_html=True)
            latest50 = df[["created_at", "temp_c", "power_w", "fan_mode", "device_id"]].tail(50).copy()
            tbl_rows = ""
            for _, row in latest50.iloc[::-1].iterrows():
                mode = str(row["fan_mode"])
                color = MODE_COLORS.get(mode, "#9ca3af")
                bg = color + "22"
                tbl_rows += (
                    f"<tr>"
                    f"<td>{row['created_at'].strftime('%H:%M:%S')}</td>"
                    f"<td>{float(row['temp_c']):.1f}</td>"
                    f"<td>{float(row['power_w']):.3f}</td>"
                    f"<td><span class='mode-badge' style='color:{color};background:{bg};'>{mode}</span></td>"
                    f"<td style='color:{MUTED};font-size:0.78rem;'>{row['device_id']}</td>"
                    f"</tr>"
                )
            st.markdown(
                f"<div class='readings-scroll'><table class='mode-table'>"
                f"<thead><tr><th>Time</th><th>Temp (°C)</th><th>Power (W)</th><th>Mode</th><th>Device</th></tr></thead>"
                f"<tbody>{tbl_rows}</tbody>"
                f"</table></div>",
                unsafe_allow_html=True,
            )
            st.download_button(
                "Download window as CSV",
                data=df.to_csv(index=False).encode(),
                file_name=f"fan_readings_{WINDOW_HOURS}h.csv",
                mime="text/csv",
            )
        with right_d:
            with st.expander("Full dataset", expanded=False):
                st.dataframe(df, use_container_width=True)

    # Footer (below tabs)
    st.markdown(
        f"""
        <div style='border-top:1px solid {BORDER};margin-top:18px;padding:10px 2px 4px;
          display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:6px;
          font-family:"Space Grotesk",sans-serif;'>
          <div style='display:flex;gap:18px;flex-wrap:wrap;'>
            <span style='font-size:0.72rem;color:{MUTED};'>Device: <span style='color:{TEXT};font-weight:500;'>{DEVICE_ID.strip() or "all"}</span></span>
            <span style='font-size:0.72rem;color:{MUTED};'>Source: <span style='color:{TEXT};font-weight:500;'>Supabase · fan_readings</span></span>
            <span style='font-size:0.72rem;color:{MUTED};'>Window: <span style='color:{TEXT};font-weight:500;'>{WINDOW_HOURS}h</span></span>
          </div>
          <div style='font-size:0.72rem;color:{MUTED};'>Last updated: <span style='color:{TEXT_DIM};'>{last['created_at'].strftime('%Y-%m-%d %H:%M:%S')} PT</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# --- Auto refresh (live mode only; demo reruns on interaction) ---
if not is_demo:
    time.sleep(REFRESH_SEC)
    st.rerun()
