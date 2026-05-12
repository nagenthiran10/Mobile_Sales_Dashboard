import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Global Mobile Sales Insights Dashboard",
    layout="wide",
    initial_sidebar_state="auto"
)

st.markdown("""
<style>
    /* ── Base ── */
    .stApp { background-color: #121212; color: #f8fafc; }
    header { visibility: hidden !important; display: none !important; }
    
    /* Allow sidebar collapse button on mobile */
    [data-testid="stSidebarCollapseButton"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }

    /* Remove all scrollbars entirely on desktop */
    ::-webkit-scrollbar { display: none !important; width: 0 !important; height: 0 !important; }
    * { scrollbar-width: none !important; -ms-overflow-style: none !important; }
    
    [data-testid="stSidebarUserContent"], [data-testid="stSidebarContent"] {
        overflow: hidden !important;
    }
    
    .block-container {
        padding-top: 0rem;
        padding-bottom: 0rem;
        padding-left: 0.5rem;
        padding-right: 0.5rem;
        margin-bottom: 2px !important;
        overflow: hidden !important;
    }

    /* ── Static (no-scroll) page — DESKTOP ONLY ── */
    @media (min-width: 769px) {
        .stApp,
        [data-testid="stAppViewContainer"],
        [data-testid="stMain"],
        section.main {
            overflow: hidden !important;
            height: 100vh !important;
        }
    }

    /* ── MOBILE: allow scrolling, reset overflow ── */
    @media (max-width: 768px) {
        .stApp,
        [data-testid="stAppViewContainer"],
        [data-testid="stMain"],
        section.main {
            overflow: auto !important;
            height: auto !important;
        }
        .block-container {
            overflow: visible !important;
            padding-left: 0.3rem !important;
            padding-right: 0.3rem !important;
        }
        /* Hide sidebar entirely on mobile — filters move inline */
        [data-testid="stSidebar"] {
            display: none !important;
        }
    }

    /* ── Sidebar — Burnt Orange ── */
    [data-testid="stSidebar"] {
        background-color: #F26419 !important;
        border-right: 1px solid #333333;
        min-width: 200px !important;
        max-width: 240px !important;
        overflow: hidden !important;
    }
    
    [data-testid="stSidebarHeader"] { display: none !important; }
    [data-testid="stSidebarUserContent"] { padding-top: 20px !important; }
    [data-testid="stSidebarContent"] { padding-top: 0rem !important; }
    [data-testid="stSidebarContent"] > div:first-child {
        padding-top: 0rem !important;
    }
    
    [data-testid="stSidebar"] * { color: #fff !important; }
    [data-testid="stSidebar"] .stSelectbox > div > div {
        background-color: rgba(0,0,0,0.25) !important;
        border: 1px solid rgba(255,255,255,0.3) !important;
        border-radius: 0px !important;
        font-size: 11px !important;
        color: #fff !important;
    }
    
    /* Sidebar big title */
    .sb-title {
        font-size: 22px;
        font-weight: 800;
        color: #fff !important;
        line-height: 1.3;
        padding: 0 6px 0px 6px;
        margin-top: 0;
        margin-bottom: 12px;
        border-bottom: 1px solid rgba(255,255,255,0.25);
        padding-bottom: 10px;
    }
    
    /* ── Mini Insight Cards — flat style ── */
    .insight-card {
        background-color: rgba(0,0,0,0.2);
        border-left: 3px solid #fff;
        border-radius: 0px;
        padding: 6px 8px;
        margin: 4px 6px 6px 6px;
        font-size: 11px;
    }
    .insight-title {
        color: rgba(255,255,255,0.65);
        font-size: 9px;
        text-transform: uppercase;
        margin-bottom: 2px;
    }
    .insight-value {
        color: #fff;
        font-weight: 700;
        font-size: 11px;
        white-space: normal;
        word-wrap: break-word;
        line-height: 1.2;
    }

    /* ── KPI Row — enterprise hierarchy ── */
    .kpi-row {
        display: flex;
        justify-content: space-around;
        gap: 0px;
        margin: 0;
        padding: 18px 0;
        border-bottom: 1px solid #2D2D2D;
    }
    .kpi-card {
        flex: 1;
        background: transparent;
        border-left: 5px solid #F26419;
        border-right: 1px solid #2D2D2D;
        border-top: none;
        border-bottom: none;
        border-radius: 0px;
        padding: 6px 20px;
        text-align: center;
        box-shadow: none;
    }
    .kpi-card:last-child { border-right: none; }
    .kpi-label {
        font-size: 13px;
        color: #cccccc;
        margin-bottom: 4px;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 700;
        text-align: center;
    }
    .kpi-value {
        font-size: 32px;
        font-weight: 600;
        color: #ffffff;
        line-height: 1.1;
        margin-bottom: 5px;
        text-align: center;
    }
    .kpi-sub {
        font-size: 12px;
        font-weight: 500;
        white-space: nowrap;
        text-align: center;
        letter-spacing: 0.3px;
    }

    /* ── Main Dashboard Grid (70/30 Split) & Border Sync ── */
    [data-testid="stMain"] [data-testid="stHorizontalBlock"] {
        gap: 0rem !important;
    }
    [data-testid="stMain"] [data-testid="stVerticalBlock"] {
        gap: 0rem !important;
    }
    
    [data-testid="stPlotlyChart"] {
        background-color: #121212 !important;
        border: 1px solid #333333 !important;
        box-sizing: border-box !important;
        display: flex; 
        justify-content: center;
        padding: 0 !important;
        margin-top: 0px !important;
        margin-bottom: 0px !important;
        height: 100% !important;
        width: 100% !important;
    }

    /* Collapse Borders via negative margins */
    /* Right column */
    [data-testid="stMain"] [data-testid="stHorizontalBlock"]:first-of-type > [data-testid="column"]:nth-of-type(2) [data-testid="stPlotlyChart"] {
        margin-left: -1px !important;
    }
    
    /* ── Bottom Row (3 Columns) ── */
    [data-testid="column"] [data-testid="stHorizontalBlock"] {
        align-items: stretch !important;
    }
    
    [data-testid="column"] [data-testid="stHorizontalBlock"] > [data-testid="column"] {
        background-color: #121212 !important;
        border-top: 1px solid #333333 !important;
        border-bottom: 1px solid #333333 !important;
        border-right: 1px solid #333333 !important;
        border-left: none !important;
        height: 400px !important;
        max-height: 400px !important;
        margin-top: 18px !important;
        margin-left: 0px !important;
        margin-right: 0px !important;
        padding-top: 15px !important;
        box-sizing: border-box !important;
        overflow: visible !important;
        position: relative !important;
    }

    /* First column gets the left border to close the grid */
    [data-testid="column"] [data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-of-type(1) {
        border-left: 1px solid #333333 !important;
    }

    [data-testid="column"] [data-testid="stHorizontalBlock"] > [data-testid="column"] > div {
        display: flex !important;
        flex-direction: column !important;
        justify-content: flex-start !important;
        align-items: stretch !important;
        height: 100% !important;
        width: 100% !important;
        margin: 0px !important;
        padding: 0px !important;
    }

    [data-testid="column"] [data-testid="stHorizontalBlock"] > [data-testid="column"] .element-container {
        margin: 0px !important;
        padding: 0px !important;
    }

    /* Graphic Layer — height = container minus title bar (~34px) */
    [data-testid="column"] [data-testid="stHorizontalBlock"] > [data-testid="column"] [data-testid="stPlotlyChart"] {
        margin-top: 0px !important;
        margin-bottom: 0px !important;
        padding: 0px !important;
        border: none !important;
        background-color: transparent !important;
        height: calc(100% - 34px) !important;
        flex-shrink: 0 !important;
    }

    /* Padding for Treemap and Donut */
    [data-testid="column"] [data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-of-type(1) [data-testid="stPlotlyChart"],
    [data-testid="column"] [data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-of-type(2) [data-testid="stPlotlyChart"] {
        padding-top: 40px !important;
        padding-bottom: 40px !important;
    }

    [data-testid="column"] [data-testid="stHorizontalBlock"] > [data-testid="column"] [data-testid="stPlotlyChart"] canvas,
    [data-testid="column"] [data-testid="stHorizontalBlock"] > [data-testid="column"] [data-testid="stPlotlyChart"] svg {
        object-fit: contain !important;
    }

    /* Modebar — hide by default, show on hover, sit BELOW the title strip */
    [data-testid="column"] [data-testid="stHorizontalBlock"] > [data-testid="column"] .modebar-container {
        z-index: 999 !important;
        overflow: visible !important;
        bottom: 4px !important;
        top: auto !important;
        right: 4px !important;
        position: absolute !important;
        opacity: 0 !important;
        transition: opacity 0.2s ease !important;
    }
    [data-testid="column"] [data-testid="stHorizontalBlock"] > [data-testid="column"]:hover .modebar-container {
        opacity: 1 !important;
    }
    [data-testid="column"] [data-testid="stHorizontalBlock"] > [data-testid="column"] .modebar {
        background: rgba(30,30,30,0.92) !important;
        border-radius: 4px !important;
        border: 1px solid #444 !important;
    }

    /* Styling pills/radio for Year */
    div[role="radiogroup"] {
        display: flex;
        flex-direction: row;
        flex-wrap: wrap;
        gap: 4px;
        padding: 0 0 0px 0;
        width: 100%;
    }
    div[role="radiogroup"] > label {
        background-color: rgba(0,0,0,0.2);
        border: 1px solid rgba(255,255,255,0.3);
        border-radius: 0px;
        padding: 4px 0px;
        margin: 0 !important;
        flex: 1 0 45%;
        text-align: center;
        cursor: pointer;
    }
    div[role="radiogroup"] > label:first-child {
        flex: 1 0 100%;
    }
    div[role="radiogroup"] > label[data-checked="true"] {
        background-color: rgba(0,0,0,0.35) !important;
        border-color: #fff !important;
        color: #fff !important;
    }
    div[role="radiogroup"] > label > div:first-child { display: none; }
    div[role="radiogroup"] > label > div:last-child { 
        margin-left: 0; 
        font-size: 11px; 
        font-weight: 600; 
    }

    /* ══════════════════════════════════════════
       MOBILE OVERRIDES
    ══════════════════════════════════════════ */
    @media (max-width: 768px) {

        /* KPI row: 2 columns grid instead of 5 in a row */
        .kpi-row {
            display: grid !important;
            grid-template-columns: 1fr 1fr !important;
            gap: 8px !important;
            padding: 10px 4px !important;
        }
        .kpi-card {
            border-left: 3px solid #F26419 !important;
            border-right: none !important;
            border-top: 1px solid #2D2D2D !important;
            border-bottom: 1px solid #2D2D2D !important;
            padding: 8px 10px !important;
        }
        /* 5th KPI card spans full width */
        .kpi-card:last-child {
            grid-column: 1 / -1 !important;
        }
        .kpi-value {
            font-size: 22px !important;
        }
        .kpi-label {
            font-size: 10px !important;
            letter-spacing: 0.5px !important;
        }
        .kpi-sub {
            font-size: 9px !important;
            white-space: normal !important;
        }

        /* All st.columns stack vertically */
        div[data-testid="column"] {
            width: 100% !important;
            min-width: 100% !important;
            flex: 0 0 100% !important;
            height: auto !important;
            max-height: none !important;
            margin-bottom: 0px !important;
            border: none !important;
        }

        /* Bottom row columns: remove fixed height */
        [data-testid="column"] [data-testid="stHorizontalBlock"] > [data-testid="column"] {
            height: auto !important;
            max-height: none !important;
            margin-top: 4px !important;
            border: 1px solid #333333 !important;
        }

        /* Charts: auto height on mobile */
        [data-testid="stPlotlyChart"] {
            height: auto !important;
        }

        /* Mobile header strip */
        .mobile-header {
            display: flex !important;
        }
    }

    /* Hide mobile header on desktop */
    .mobile-header {
        display: none;
        background-color: #F26419;
        padding: 10px 12px;
        margin-bottom: 8px;
        border-bottom: 1px solid rgba(255,255,255,0.2);
    }
    .mobile-header-title {
        font-size: 16px;
        font-weight: 800;
        color: #fff;
        line-height: 1.2;
    }
    .mobile-filters-toggle {
        font-size: 11px;
        font-weight: 700;
        color: rgba(255,255,255,0.75);
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 4px;
        cursor: pointer;
    }
</style>
""", unsafe_allow_html=True)

# ── Mobile Detection via query param ─────────────────────────────────────────
st.markdown("""
<script>
(function() {
    if (window.innerWidth <= 768) {
        var url = new URL(window.location.href);
        if (url.searchParams.get('mobile') !== '1') {
            url.searchParams.set('mobile', '1');
            window.location.replace(url.toString());
        }
    } else {
        var url = new URL(window.location.href);
        if (url.searchParams.get('mobile') === '1') {
            url.searchParams.delete('mobile');
            window.location.replace(url.toString());
        }
    }
})();
</script>
""", unsafe_allow_html=True)

is_mobile = st.query_params.get("mobile", "0") == "1"

# ── Number Formatter (K / L / B) ─────────────────────────────────────────────
def fmt(val, prefix=""):
    if val >= 1_000_000_000:
        return f"{prefix}{val/1_000_000_000:.2f}B"
    elif val >= 100_000:
        return f"{prefix}{val/100_000:.2f}L"
    elif val >= 1_000:
        return f"{prefix}{val/1_000:.2f}K"
    return f"{prefix}{val:,.0f}"

def fmt_curr(val): return fmt(val, prefix="$")
def fmt_num(val):  return fmt(val)

# ── Data Loading ──────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("data/mobile_sales_dataset.csv")
    df['price_range'] = pd.qcut(
        df['selling_price'], q=4,
        labels=['Budget', 'Mid-Range', 'Premium', 'Ultra-Premium'],
        duplicates='drop'
    ).astype(str)
    df['inward_date'] = pd.to_datetime(df['inward_date'], errors='coerce')
    df['month_year']  = df['inward_date'].dt.to_period('M').astype(str)
    return df

df = load_data()

# ── Sidebar (desktop) / Inline filters (mobile) ──────────────────────────────

years = ["All"] + sorted(df["year"].dropna().unique().astype(int).astype(str).tolist())

if is_mobile:
    # ── Mobile: compact header + inline filter expander ──
    st.markdown("""
    <div class='mobile-header'>
        <div>
            <div class='mobile-header-title'>Global Mobile Sales<br>Insights Dashboard</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("🔽 Filters & Quick Insights", expanded=False):
        sel_year_str = st.radio("Year", years, horizontal=True)
        sel_year = int(sel_year_str) if sel_year_str != "All" else "All"
        df_y = df[df["year"] == sel_year] if sel_year != "All" else df.copy()

        brands     = ["All"] + sorted(df_y["brand"].dropna().unique().tolist())
        price_rngs = ["All"] + ['Budget', 'Mid-Range', 'Premium', 'Ultra-Premium']
        countries  = ["All"] + sorted(df_y["country"].dropna().unique().tolist())

        mc1, mc2, mc3 = st.columns(3)
        with mc1: sel_brand   = st.selectbox("Brand 📱",   brands,     key="m_brand")
        with mc2: sel_price   = st.selectbox("Price 💰",   price_rngs, key="m_price")
        with mc3: sel_country = st.selectbox("Country 🌍", countries,  key="m_country")

        # Quick Insights inline
        df_yi = df_y.copy()
        if sel_brand   != "All": df_yi = df_yi[df_yi["brand"]       == sel_brand]
        if sel_price   != "All": df_yi = df_yi[df_yi["price_range"] == sel_price]
        if sel_country != "All": df_yi = df_yi[df_yi["country"]     == sel_country]

        if not df_yi.empty:
            top_brand_s = df_yi.groupby("brand")["revenue"].sum()
            top_brand   = top_brand_s.idxmax()
            top_brand_val = top_brand_s.max()
            top_country_s = df_yi.groupby("country")["units_sold"].sum()
            top_country   = top_country_s.idxmax()
            top_country_val = top_country_s.max()
            top_model_s = df_yi.groupby(["brand","model"])["units_sold"].sum()
            top_brand_model = top_model_s.idxmax()
            top_model = f"{top_brand_model[0]} {top_brand_model[1]}"
            top_model_val = top_model_s.max()
            st.markdown(f"""
            <div style='display:grid;grid-template-columns:1fr 1fr 1fr;gap:6px;margin-top:8px;'>
              <div style='background:rgba(242,100,25,0.15);border-left:3px solid #F26419;padding:6px 8px;border-radius:4px;'>
                <div style='font-size:9px;color:#aaa;text-transform:uppercase;'>🏆 Top Brand</div>
                <div style='font-size:11px;font-weight:700;color:#fff;'>{top_brand}<br><span style='color:#F26419;'>{fmt_curr(top_brand_val)}</span></div>
              </div>
              <div style='background:rgba(242,100,25,0.15);border-left:3px solid #F26419;padding:6px 8px;border-radius:4px;'>
                <div style='font-size:9px;color:#aaa;text-transform:uppercase;'>🌍 Top Country</div>
                <div style='font-size:11px;font-weight:700;color:#fff;'>{top_country}<br><span style='color:#F26419;'>{fmt_num(top_country_val)} units</span></div>
              </div>
              <div style='background:rgba(242,100,25,0.15);border-left:3px solid #F26419;padding:6px 8px;border-radius:4px;'>
                <div style='font-size:9px;color:#aaa;text-transform:uppercase;'>📱 Top Model</div>
                <div style='font-size:11px;font-weight:700;color:#fff;'>{top_model}<br><span style='color:#F26419;'>{fmt_num(top_model_val)} units</span></div>
              </div>
            </div>
            """, unsafe_allow_html=True)

else:
    # ── Desktop: original sidebar ──
    st.sidebar.markdown("<div class='sb-title'>Global Mobile<br>Sales Insights<br>dashboard</div>", unsafe_allow_html=True)
    st.sidebar.markdown("<div style='font-size:11px; font-weight:700; color:#888; text-transform:uppercase; margin-bottom:2px; margin-left:6px;'>year</div>", unsafe_allow_html=True)
    sel_year_str = st.sidebar.radio("Year", years, horizontal=True, label_visibility="collapsed")
    sel_year = int(sel_year_str) if sel_year_str != "All" else "All"
    df_y = df[df["year"] == sel_year] if sel_year != "All" else df.copy()

    if not df_y.empty:
        top_brand_s = df_y.groupby("brand")["revenue"].sum()
        top_brand = top_brand_s.idxmax()
        top_brand_val = top_brand_s.max()
        top_country_s = df_y.groupby("country")["units_sold"].sum()
        top_country = top_country_s.idxmax()
        top_country_val = top_country_s.max()
        top_model_s = df_y.groupby(["brand", "model"])["units_sold"].sum()
        top_brand_model = top_model_s.idxmax()
        top_model = f"{top_brand_model[0]} {top_brand_model[1]}"
        top_model_val = top_model_s.max()
        brand_text = f"{top_brand} ({fmt_curr(top_brand_val)})"
        country_text = f"{top_country} ({fmt_num(top_country_val)} units)"
        model_text = f"{top_model}<br>({fmt_num(top_model_val)} units)"
    else:
        brand_text = country_text = model_text = "N/A"

    st.sidebar.markdown("<div style='font-size:11px; font-weight:700; color:#888; margin-top:4px; margin-bottom:4px; margin-left:6px; text-transform:uppercase;'>QUICK INSIGHTS</div>", unsafe_allow_html=True)
    st.sidebar.markdown(f"""
    <div class='insight-card'>
        <div class='insight-title'>🏆 Top Brand</div>
        <div class='insight-value'>{brand_text}</div>
    </div>
    <div class='insight-card'>
        <div class='insight-title'>🌍 Top Country</div>
        <div class='insight-value'>{country_text}</div>
    </div>
    <div class='insight-card'>
        <div class='insight-title'>📱 Top Model</div>
        <div class='insight-value'>{model_text}</div>
    </div>
    """, unsafe_allow_html=True)
    st.sidebar.markdown("<hr style='border: none; border-top: 1px solid rgba(255,255,255,0.25); margin: 12px 0;'>", unsafe_allow_html=True)

    brands     = ["All"] + sorted(df_y["brand"].dropna().unique().tolist())
    price_rngs = ["All"] + ['Budget', 'Mid-Range', 'Premium', 'Ultra-Premium']
    countries  = ["All"] + sorted(df_y["country"].dropna().unique().tolist())
    sel_brand   = st.sidebar.selectbox("Brand 📱",   brands)
    sel_price   = st.sidebar.selectbox("Price 💰",   price_rngs)
    sel_country = st.sidebar.selectbox("Country 🌍", countries)

# ── Filters ───────────────────────────────────────────────────────────────────
df_f = df_y.copy()
if sel_brand   != "All": df_f = df_f[df_f["brand"]       == sel_brand]
if sel_price   != "All": df_f = df_f[df_f["price_range"] == sel_price]
if sel_country != "All": df_f = df_f[df_f["country"]     == sel_country]

# ── KPI Calculations ──────────────────────────────────────────────────────────
if not df_f.empty:
    tot_revenue = df_f["revenue"].sum()
    tot_qty     = df_f["units_sold"].sum()
    avg_price   = df_f["selling_price"].mean()
    tot_orders  = df_f["order_id"].nunique()
    
    # Calculate MoM Growth for Revenue
    monthly_rev = df_f.groupby("month_year")["revenue"].sum().sort_index()
    if len(monthly_rev) >= 2:
        last_month_rev = monthly_rev.iloc[-1]
        prev_month_rev = monthly_rev.iloc[-2]
        if prev_month_rev > 0:
            growth_pct = ((last_month_rev - prev_month_rev) / prev_month_rev) * 100
            growth_str = f"+{growth_pct:.1f}%" if growth_pct > 0 else f"{growth_pct:.1f}%"
        else:
            growth_str = "N/A"
    else:
        growth_str = "N/A"

    # ── YoY Comparison ────────────────────────────────────────────────────────
    cur_year = sel_year if sel_year != "All" else df["year"].max()
    prev_year = cur_year - 1 if sel_year != "All" else df["year"].max() - 1

    # Apply same brand/price/country filters to previous year
    df_py = df[df["year"] == prev_year].copy()
    if sel_brand   != "All": df_py = df_py[df_py["brand"]       == sel_brand]
    if sel_price   != "All": df_py = df_py[df_py["price_range"] == sel_price]
    if sel_country != "All": df_py = df_py[df_py["country"]     == sel_country]

    def yoy_sub(cur, prev, prefix=""):
        if prev and prev > 0:
            diff = cur - prev
            pct  = (diff / prev) * 100
            sign = "+" if diff >= 0 else ""
            arrow = "▲" if diff >= 0 else "▼"
            color = "#2ECC71" if diff >= 0 else "#FFD1BA"
            text  = f"{sign}{fmt(diff, prefix)} | {sign}{pct:.1f}% {arrow} vs LY"
            return f"<span style='color:{color};'>{text}</span>"
        return "<span style='color:#666;'>No prior year data</span>"

    if not df_py.empty:
        py_rev    = df_py["revenue"].sum()
        py_qty    = df_py["units_sold"].sum()
        py_price  = df_py["selling_price"].mean()
        py_orders = df_py["order_id"].nunique()
        sub_rev    = yoy_sub(tot_revenue, py_rev, prefix="$")
        sub_qty    = yoy_sub(tot_qty, py_qty)
        sub_price  = yoy_sub(avg_price, py_price, prefix="$")
        sub_orders = yoy_sub(tot_orders, py_orders)
    else:
        sub_rev = sub_qty = sub_price = sub_orders = "No prior year data"
    sub_growth = (
        f"<span style='color:#2ECC71;'>{growth_str} MoM ▲</span>"
        if growth_str.startswith("+")
        else f"<span style='color:#FFD1BA;'>{growth_str} MoM ▼</span>"
        if growth_str not in ("N/A", "")
        else f"<span style='color:#666;'>N/A</span>"
    )
else:
    tot_revenue = tot_qty = avg_price = tot_orders = 0
    growth_str = "N/A"
    sub_rev = sub_qty = sub_price = sub_orders = "<span style='color:#666;'>—</span>"
    sub_growth = "<span style='color:#666;'>—</span>"

# ── KPI Row ───────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="kpi-row">
  <div class="kpi-card">
    <div class="kpi-label">💰 TOTAL REVENUE</div>
    <div class="kpi-value">{fmt_curr(tot_revenue)}</div>
    <div class="kpi-sub">{sub_rev}</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-label">📦 TOTAL UNITS SOLD</div>
    <div class="kpi-value">{fmt_num(tot_qty)}</div>
    <div class="kpi-sub">{sub_qty}</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-label">🏷️ AVG SELLING PRICE</div>
    <div class="kpi-value">{fmt_curr(avg_price)}</div>
    <div class="kpi-sub">{sub_price}</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-label">📈 REVENUE GROWTH</div>
    <div class="kpi-value">{growth_str}</div>
    <div class="kpi-sub">{sub_growth}</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-label">🧾 TOTAL ORDERS</div>
    <div class="kpi-value">{fmt_num(tot_orders)}</div>
    <div class="kpi-sub">{sub_orders}</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Chart Helper ──────────────────────────────────────────────────────────────
def base_layout(fig, height=380):
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#bdbdbd",
        margin=dict(l=8, r=8, t=32, b=8),
        xaxis=dict(showgrid=False, zeroline=False, title=None),
        yaxis=dict(showgrid=True, gridcolor="#2a2a2a", zeroline=False, title=None),
        height=height,
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=10)),
        title_font=dict(size=13, color="#eeeeee"),
        autosize=True
    )
    return fig

CHART_COLOR = "#F26419"
CHART_FILL  = "rgba(242,100,25,0.15)"
CHART_LABEL = "#FFD1BA"

# ══════════════════════════════════════════════════════════
#  MAIN VISUALS : Left (70%) | Right (30%) — stacked on mobile
# ══════════════════════════════════════════════════════════
if is_mobile:
    col_left, col_right = st.columns([1, 1])  # equal width on mobile isn't great, so use tabs
    # On mobile we use a tab layout instead of side-by-side columns
    tab_trend, tab_brands = st.tabs(["📈 Sales Trend", "🏆 Top Brands"])
    col_left  = tab_trend
    col_right = tab_brands
else:
    col_left, col_right = st.columns([7, 3])

with col_left:
    # 📈 Line – Sales Trend Over Time
    if not df_f.empty:
        line_data = (
            df_f.groupby("month_year")["units_sold"]
            .sum().reset_index().sort_values("month_year")
        )
        y_min = int(line_data["units_sold"].min() * 0.90) if not line_data.empty else 0
        y_max = int(line_data["units_sold"].max()) if not line_data.empty else 1

        fig_line = px.line(
            line_data, x="month_year", y="units_sold",
            color_discrete_sequence=[CHART_COLOR], markers=True
        )
        fig_line.update_traces(
            line=dict(width=2),
            marker=dict(size=5),
            fill="tozeroy",
            fillcolor=CHART_FILL,
            hovertemplate="<b>Date:</b> %{x}<br><b>Units:</b> %{y:,}<extra></extra>"
        )
        # 50% height
        line_h = 240 if is_mobile else 330
        fig_line = base_layout(fig_line, height=line_h)
        fig_line.update_layout(
            title=dict(
                text="📈 Sales Trend Over Time",
                x=0, y=0.98,
                pad=dict(l=5, t=5, r=0, b=0),
                font=dict(size=13, color="#eeeeee")
            ),
            margin=dict(l=5, r=5, t=30, b=5),
            plot_bgcolor="#121212",
            paper_bgcolor="#121212",
            hovermode="closest",
            xaxis=dict(showgrid=True, gridcolor="#1A1A1A", tickangle=-30, tickfont=dict(size=9), title=None),
            yaxis=dict(
                showgrid=True, gridcolor="#1A1A1A",
                range=[y_min, y_max],
                tickformat=",.0f", title=None
            )
        )
        st.plotly_chart(fig_line, use_container_width=True, key="line_chart", config={"displayModeBar": False})
    else:
        st.info("No data.")

    # ══════════════════════════════════════════════════════════
    #  BOTTOM SECTION : Treemap | Donut | Map
    # ══════════════════════════════════════════════════════════
    st.markdown('<div style="height: 10px;"></div>', unsafe_allow_html=True)
    
    if is_mobile:
        # On mobile: tabs for bottom charts
        tab_tree, tab_donut, tab_map = st.tabs(["🌳 Age Groups", "🏷️ Price Segments", "🌍 By Country"])
        col_bl, col_bm, col_br = tab_tree, tab_donut, tab_map
        bottom_h = 250
    else:
        col_bl, col_bm, col_br = st.columns(3)
        bottom_h = 300

    with col_bl:
        if not df_f.empty:
            st.markdown(
                "<div style='"
                "margin: 0px !important;"
                "padding: 4px 0px 4px 8px !important;"
                "font-size: 13px;"
                "font-weight: bold;"
                "color: #eeeeee;"
                "text-align: left;"
                "position: relative;"
                "z-index: 10;"
                "background-color: #121212;"
                "'>🌳 Age Group Distribution</div>",
                unsafe_allow_html=True
            )
            tree_data = df_f.groupby("buyer_age_group")["units_sold"].sum().reset_index()
            tree_data["units_k"] = tree_data["units_sold"].apply(lambda v: f"{v/1000:.1f}K")

            fig_tree = px.treemap(
                tree_data, path=["buyer_age_group"], values="units_sold",
                color="units_sold",
                color_continuous_scale=["#FFD1BA", "#F26419"],
                custom_data=["units_k"]
            )
            fig_tree.update_traces(
                texttemplate="<b>%{label}</b><br>%{customdata[0]}",
                textfont=dict(size=11, color="#000000"),
                hovertemplate="<b>%{label}</b><br>Units: %{customdata[0]}<extra></extra>",
                textposition="middle center",
                marker=dict(pad=dict(t=2, l=2, r=2, b=2))
            )
            fig_tree.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="#bdbdbd",
                margin=dict(l=0, r=0, t=0, b=0),
                height=bottom_h,
                coloraxis_showscale=False
            )
            st.plotly_chart(fig_tree, use_container_width=True, key="treemap_chart", config={"displayModeBar": False})
        else:
            st.info("No data.")

    with col_bm:
        if not df_f.empty:
            st.markdown(
                "<div style='"
                "margin: 0px !important;"
                "margin-bottom: 20px !important;"
                "padding: 4px 0px 4px 8px !important;"
                "font-size: 13px;"
                "font-weight: bold;"
                "color: #eeeeee;"
                "text-align: left;"
                "position: relative;"
                "z-index: 10;"
                "background-color: #121212;"
                "'>🏷️ Price Segment Distribution</div>",
                unsafe_allow_html=True
            )
            donut_data = {
                'Price Range': ['Budget', 'Mid-Range', 'Premium', 'Ultra-Premium'],
                'Count': [17221, 12076, 6136, 5105]
            }
            fig_donut = px.pie(
                donut_data, names='Price Range', values='Count',
                hole=0.6,
                color_discrete_sequence=['#FFD8B1', '#FFAD66', '#FF8C33', '#E65100']
            )
            fig_donut.update_traces(
                textposition="outside",
                textinfo="label+percent",
                textfont=dict(size=11, color="#ffffff"),
                hovertemplate="<b>%{label}</b><br>%{percent}<extra></extra>",
                domain=dict(x=[0.20, 0.80], y=[0.20, 0.80])
            )
            fig_donut.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="#bdbdbd",
                margin=dict(l=10, r=10, t=5, b=5),
                height=bottom_h,
                showlegend=False
            )
            st.plotly_chart(fig_donut, use_container_width=True, key="donut_chart", config={"displayModeBar": False})
        else:
            st.info("No data.")

    with col_br:
        if not df_f.empty:
            st.markdown(
                "<div style='"
                "margin: 0px !important;"
                "padding: 4px 0px 4px 8px !important;"
                "font-size: 13px;"
                "font-weight: bold;"
                "color: #eeeeee;"
                "text-align: left;"
                "position: relative;"
                "z-index: 10;"
                "background-color: #121212;"
                "'>🌍 Sales by Country</div>",
                unsafe_allow_html=True
            )
            map_data = df_f.groupby("country")["units_sold"].sum().reset_index()
            fig_map = px.choropleth(
                map_data,
                locations="country", locationmode="country names",
                color="units_sold",
                color_continuous_scale=["#FFD1BA", "#F26419"]
            )
            fig_map.update_traces(
                hovertemplate="<b>Country:</b> %{location}<br><b>Units:</b> %{z:,}<extra></extra>"
            )
            fig_map.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="#bdbdbd",
                geo=dict(
                    visible=False,
                    showframe=False, showcoastlines=False,
                    projection_type="natural earth",
                    bgcolor="rgba(0,0,0,0)",
                    showland=True, landcolor="#2a2a2a",
                    showocean=True, oceancolor="#121212",
                    showcountries=True, countrycolor="#444444",
                    lataxis=dict(range=[-55, 80], showgrid=False),
                    lonaxis=dict(range=[-160, 170], showgrid=False),
                ),
                margin=dict(l=10, r=10, t=10, b=10),
                height=bottom_h,
                coloraxis_showscale=False
            )
            st.plotly_chart(fig_map, use_container_width=True, key="map_chart", config={"displayModeBar": False})
        else:
            st.info("No data.")

with col_right:
    # 📊 Bar – Top Brands by Revenue (Full Height)
    if not df_f.empty:
        bar_data = (
            df_f.groupby("brand")["revenue"]
            .sum().nlargest(15).reset_index()
            .sort_values("revenue", ascending=False)
        )
        bar_data["rev_label"] = bar_data["revenue"].apply(fmt_curr)

        # Reverse so largest renders at top in plotly horizontal bar
        bar_data = bar_data.iloc[::-1].reset_index(drop=True)

        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            y=bar_data["brand"],
            x=bar_data["revenue"],
            orientation="h",
            marker=dict(color=CHART_COLOR, line=dict(width=0)),
            text=bar_data["rev_label"],
            textposition="outside",
            textfont=dict(size=10, color="#ffffff"),
            cliponaxis=False,
            hovertemplate="<b>%{y}</b><br>Revenue: %{text}<extra></extra>"
        ))

        # Height 659px aligns perfectly with left column (330px + 330px - 1px overlap)
        bar_h = 350 if is_mobile else 659
        fig_bar.update_layout(
            title=dict(text="🏆 Top Brands by Revenue", font=dict(size=13, color="#eeeeee"), x=0),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#bdbdbd",
            height=bar_h,
            margin=dict(l=4, r=8, t=36, b=24),
            xaxis=dict(
                showgrid=True, gridcolor="#1A1A1A",
                showticklabels=False,
                zeroline=False,
                title=None,
                range=[0, bar_data["revenue"].max() * 1.10]
            ),
            yaxis=dict(
                showgrid=False,
                zeroline=False,
                title=None,
                tickfont=dict(size=11, color="#cccccc"),
                automargin=True,
                range=[-0.5, len(bar_data) - 0.5]
            ),
            bargap=0.30,
            showlegend=False
        )
        st.plotly_chart(fig_bar, use_container_width=True, key="bar_chart", config={"displayModeBar": False})
    else:
        st.info("No data.")