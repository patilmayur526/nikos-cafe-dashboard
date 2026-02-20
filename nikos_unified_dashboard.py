#!/usr/bin/env python3
"""
Nikos Cafe — Unified Dashboard
Sales + Inventory | 5 Business Questions + Break-Even + WoW + Protein Alert + Slow Day Recovery
"""

from pathlib import Path
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta

# ─────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────
st.set_page_config(
    page_title="Nikos Cafe — Command Center",
    page_icon="/Users/mayurpatil/Downloads/NIKOS_2026/image.jpg",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── GLOBAL PLOTLY DEFAULTS ────────────────
# Warm cream background, dark readable text, subtle grid
import plotly.io as pio
CREAM   = '#F5EFE6'
INK     = '#1E1612'
MUTED   = '#6B5B52'
GRID    = '#E0D5C8'
CLAY    = '#C45C3A'
GOLD    = '#C4922A'
OLIVE   = '#4A5E2A'

pio.templates["nikos"] = pio.templates["plotly_white"]
pio.templates["nikos"].layout.update(
    paper_bgcolor=CREAM,
    plot_bgcolor=CREAM,
    font=dict(family='DM Sans, sans-serif', color=INK, size=12),
    title_font=dict(family='Playfair Display, serif', color=INK, size=15),
    colorway=[CLAY, GOLD, OLIVE, '#8B3A22', '#2980B9', '#8E44AD', '#BDC3C7'],
    xaxis=dict(gridcolor=GRID, linecolor=GRID, zerolinecolor=GRID,
               tickfont=dict(color=INK), title_font=dict(color=INK)),
    yaxis=dict(gridcolor=GRID, linecolor=GRID, zerolinecolor=GRID,
               tickfont=dict(color=INK), title_font=dict(color=INK)),
    legend=dict(bgcolor='rgba(245,239,230,0.92)', bordercolor=GRID, borderwidth=1,
                font=dict(color=INK)),
    hoverlabel=dict(bgcolor='#FFFAF5', font_color=INK, bordercolor=GRID),
)
pio.templates.default = "nikos"

# ── HELPER: stamp black text on every chart ──────────────────
_AXIS = dict(tickfont=dict(color=INK, size=11), title_font=dict(color=INK, size=12),
             gridcolor=GRID, linecolor=GRID, zerolinecolor=GRID)
_LEG  = dict(font=dict(color=INK, size=11), bgcolor='rgba(245,239,230,0.92)',
             bordercolor=GRID, borderwidth=1)

def ink(fig, **extra):
    """Call after every figure is fully built to guarantee all text is black."""
    fig.update_layout(
        paper_bgcolor=CREAM, plot_bgcolor=CREAM,
        font=dict(color=INK, family='DM Sans, sans-serif', size=12),
        title_font=dict(color=INK, family='Playfair Display, serif', size=14),
        xaxis=_AXIS, yaxis=_AXIS, legend=_LEG,
        **extra
    )
    for ax in ['xaxis2','yaxis2','xaxis3','yaxis3']:
        try:
            fig.update_layout(**{ax: _AXIS})
        except:
            pass
    fig.update_traces(textfont=dict(color=INK))
    return fig

# ─────────────────────────────────────────
# CUSTOM CSS — warm mediterranean palette
# ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=DM+Sans:wght@300;400;500&display=swap');

/* ── FORCE LIGHT MODE EVERYWHERE ── */
:root {
    --clay:    #C45C3A;
    --gold:    #C4922A;
    --olive:   #4A5E2A;
    --cream:   #F5EFE6;
    --card:    #FFFAF5;
    --ink:     #1E1612;
    --muted:   #6B5B52;
    --border:  #E0D5C8;
    --danger:  #A93226;
    --success: #1E6B3A;
    --info:    #1A5276;
}

/* Page background */
html, body,
[data-testid="stApp"],
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.main, .block-container,
[class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
    background-color: var(--cream) !important;
    color: var(--ink) !important;
}

/* Force all text dark */
p, span, div, label, h1, h2, h3, h4, h5, h6,
.stMarkdown, .stText, [data-testid="stMarkdownContainer"] {
    color: var(--ink) !important;
}

/* Sidebar — warm parchment, not dark */
section[data-testid="stSidebar"] {
    background: #3D2B1F !important;
    border-right: 1px solid #5C3D2E !important;
}
section[data-testid="stSidebar"] * { color: #F0E6DC !important; }
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 { color: #F5C882 !important; }
section[data-testid="stSidebar"] .stCaption { color: #C4A882 !important; }

/* Input fields */
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input {
    background: #FFFAF5 !important;
    color: var(--ink) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
}
section[data-testid="stSidebar"] [data-testid="stTextInput"] input,
section[data-testid="stSidebar"] [data-testid="stNumberInput"] input {
    background: #5C3D2E !important;
    color: #F0E6DC !important;
    border: 1px solid #7A5540 !important;
}

/* Header banner */
.header-banner {
    background: linear-gradient(135deg, #B8502F 0%, #7A3418 100%);
    color: white !important;
    padding: 26px 32px; border-radius: 14px;
    margin-bottom: 20px; display: flex;
    justify-content: space-between; align-items: center;
    box-shadow: 0 4px 20px rgba(180,80,47,0.25);
}
.header-banner * { color: white !important; }
.header-banner h1 { font-family: 'Playfair Display', serif !important; font-size: 1.9rem; margin: 0; letter-spacing: -0.5px; }
.header-banner p  { margin: 4px 0 0; opacity: 0.85; font-size: 0.88rem; }
.header-badge {
    background: rgba(255,255,255,0.18); border-radius: 8px;
    padding: 8px 14px; font-size: 0.83rem; text-align: center;
    border: 1px solid rgba(255,255,255,0.25);
}
.header-badge b { font-size: 1.25rem; display: block; color: white !important; }

/* KPI cards */
.kpi-card {
    background: var(--card);
    border-radius: 12px; padding: 18px 22px;
    border-left: 4px solid var(--clay);
    box-shadow: 0 1px 8px rgba(30,22,18,0.08);
    margin-bottom: 8px;
}
.kpi-card.gold   { border-left-color: var(--gold); }
.kpi-card.olive  { border-left-color: var(--olive); }
.kpi-card.danger { border-left-color: var(--danger); }
.kpi-label {
    font-size: 0.73rem; color: var(--muted) !important;
    text-transform: uppercase; letter-spacing: 0.6px; margin-bottom: 4px;
}
.kpi-value {
    font-family: 'Playfair Display', serif !important;
    font-size: 1.6rem; color: var(--ink) !important; line-height: 1.15;
}
.kpi-sub { font-size: 0.76rem; color: var(--muted) !important; margin-top: 3px; }

/* Section headers */
.section-header {
    font-family: 'Playfair Display', serif !important;
    font-size: 1.2rem; color: var(--clay) !important;
    border-bottom: 2px solid var(--gold);
    padding-bottom: 6px; margin: 22px 0 14px;
}

/* Tab bar */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px; background: var(--card);
    padding: 5px; border-radius: 10px;
    box-shadow: 0 1px 6px rgba(30,22,18,0.08);
    border: 1px solid var(--border);
}
.stTabs [data-baseweb="tab"] {
    border-radius: 7px; padding: 8px 18px;
    font-weight: 500; color: var(--muted) !important;
    background: transparent !important;
}
.stTabs [aria-selected="true"] {
    background: var(--clay) !important;
    color: white !important;
}

/* Alert boxes — all have explicit dark text */
.alert-box {
    padding: 13px 17px; border-radius: 9px;
    margin: 8px 0; font-size: 0.88rem;
    color: var(--ink) !important;
}
.alert-warn { background: #FEF5D9; border-left: 4px solid var(--gold); color: #4A3800 !important; }
.alert-good { background: #E6F4EC; border-left: 4px solid var(--olive); color: #0D3320 !important; }
.alert-bad  { background: #FDECEA; border-left: 4px solid var(--danger); color: #5C0A04 !important; }
.alert-info { background: #E8F1FA; border-left: 4px solid var(--info); color: #0B2A45 !important; }
.alert-warn *, .alert-good *, .alert-bad *, .alert-info * { color: inherit !important; }

/* Protein card — stays dark with white text */
.protein-card {
    background: linear-gradient(135deg, #7A3418 0%, #B8502F 100%);
    color: white !important; border-radius: 12px;
    padding: 18px 22px; margin-bottom: 8px;
    box-shadow: 0 2px 12px rgba(120,50,24,0.3);
}
.protein-card .kpi-label { color: rgba(255,255,255,0.75) !important; }
.protein-card .kpi-value { color: #FFE8D6 !important; }
.protein-card .kpi-sub   { color: rgba(255,255,255,0.65) !important; }

/* Streamlit metric widgets */
[data-testid="stMetricLabel"] { color: var(--muted) !important; }
[data-testid="stMetricValue"] { color: var(--ink) !important; font-weight: 600; }
[data-testid="stMetricDelta"] { font-size: 0.82rem; }

/* Info / warning boxes from st.info / st.warning */
[data-testid="stAlert"] { border-radius: 9px !important; }

/* Dataframe */
.stDataFrame { border-radius: 10px; overflow: hidden; border: 1px solid var(--border); }

/* Horizontal rule */
hr { border-color: var(--border) !important; }

/* st.caption */
.stCaption { color: var(--muted) !important; }

/* Scrollbar — subtle */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--cream); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🥙 Nikos Command Center")
    st.markdown("---")
    sales_path = st.text_input("Sales Excel Path",
        value="/Users/mayurpatil/Downloads/NIKOS_2026/Sales_data/Combined_reports/combined_sales_data.xlsx")
    inv_path = st.text_input("Inventory Excel Path",
        value="/Users/mayurpatil/Downloads/NIKOS_2026/order_data/COMBINED_Master_Analysis.xlsx")
    st.markdown("### ⚙️ Financial Settings")
    st.caption("💡 Aramark/Sodexo sets discounts — these are contract terms, not operational choices.")
    aramark_rate      = st.number_input("Aramark/Sodexo Commission %", 0.0, 100.0, 20.0, 0.5) / 100
    cc_fee_rate       = st.number_input("Credit Card Fee %", 0.0, 10.0, 3.0, 0.1) / 100
    target_food_cost  = st.number_input("Target Food Cost % (vs Net)", 10.0, 70.0, 38.0, 1.0,
        help="University contract dining benchmark: 35–42%. Your discounts are set by Aramark/Sodexo, so net sales are structurally lower than independent restaurants.")
    st.markdown("### 🎯 Break-Even & Alert Settings")
    daily_fixed_cost  = st.number_input("Daily Fixed Costs ($)", 0.0, 10000.0, 800.0, 50.0,
        help="Rent, labor, utilities divided by operating days")
    protein_alert_pct = st.number_input("Protein Budget Alert (% of inv.)", 10.0, 60.0, 35.0, 1.0,
        help="Alert fires when protein exceeds this % of total inventory spend")
    st.markdown("### 📊 Display Settings")
    top_pct  = st.slider("Peak slots (Top %)",    1, 30, 10) / 100
    slow_pct = st.slider("Slow slots (Bottom %)", 1, 50, 20) / 100
    st.markdown("---")
    st.caption("Data refreshes on reload • Thu–Wed week cycle")

# ─────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────
def get_week_label(date):
    days_since_thu = (date.weekday() - 3) % 7
    ws = date - timedelta(days=days_since_thu)
    we = ws + timedelta(days=6)
    return f"{ws.strftime('%b %d')} – {we.strftime('%b %d')}", ws

@st.cache_data
def load_sales(path):
    xl = pd.ExcelFile(path)
    rows, slot_rows = [], []
    for sheet in xl.sheet_names:
        try:
            df   = pd.read_excel(path, sheet_name=sheet, header=None)
            date = pd.to_datetime(sheet)
            day  = str(df.iloc[1, 1]) if df.shape[0] > 1 else ''
            m    = {'Date': date, 'Day': day}
            for _, row in df.iterrows():
                k = str(row[0]).strip() if pd.notna(row[0]) else ''
                try:
                    v = float(row[1])
                    if k == 'Gross Sales Before Discounts': m['gross_before'] = v
                    if k == 'Total Discounts':              m['discounts']    = v
                    if k == 'Sales Net VAT':                m['net_sales']    = v
                    if k == 'Credit Card':                  m['credit_card']  = v
                    if k == 'Cash':                         m['cash']         = v
                except: pass
            ts_start = None
            for i, row in df.iterrows():
                if str(row[0]).strip().lower() == 'time_slots':
                    ts_start = i; break
            if ts_start is not None:
                for _, row in df.iloc[ts_start+1:].iterrows():
                    slot = str(row[0]).strip()
                    if not slot or slot.lower() in ['nan','total']: continue
                    try:
                        slot_rows.append({'Date': date, 'Day': day, 'Slot': slot,
                                          'Sales': float(row[1]),
                                          'Txns':  float(row[2]) if pd.notna(row[2]) else 0})
                    except: pass
            rows.append(m)
        except: pass
    fin = pd.DataFrame(rows).sort_values('Date')
    for col in ['gross_before','discounts','net_sales','credit_card','cash']:
        fin[col] = pd.to_numeric(fin.get(col, 0), errors='coerce').fillna(0)
    fin['discount_rate'] = (fin['discounts'] / fin['gross_before'].replace(0, np.nan) * 100).fillna(0)
    fin['week_label'], fin['week_start'] = zip(*fin['Date'].map(get_week_label))
    slots = pd.DataFrame(slot_rows)
    if not slots.empty:
        slots['Avg_Ticket'] = np.where(slots['Txns'] > 0, slots['Sales'] / slots['Txns'], 0)
    return fin, slots

@st.cache_data
def load_inventory(path):
    df = pd.read_excel(path, sheet_name='ALL_DATA')
    df['Invoice_Date']   = pd.to_datetime(df['Invoice_Date'])
    df['Category/Class'] = df['Category/Class'].fillna('Uncategorized')
    df['Subcategory']    = df['Subcategory'].fillna('General')
    df['Vendor']         = df['Source'].str.strip()
    df['week_label'], df['week_start'] = zip(*df['Invoice_Date'].map(get_week_label))
    return df

# ─────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────
try:
    fin_df, slots_df = load_sales(sales_path)
    inv_df           = load_inventory(inv_path)
except Exception as e:
    st.error(f"⚠️ Could not load data: {e}\n\nPlease update the file paths in the sidebar.")
    st.stop()

# ─────────────────────────────────────────
# WEEKLY MERGED DATA
# ─────────────────────────────────────────
weekly_sales = fin_df.groupby(['week_label','week_start']).agg(
    net_sales    = ('net_sales',   'sum'),
    gross_before = ('gross_before','sum'),
    discounts    = ('discounts',   'sum'),
    credit_card  = ('credit_card', 'sum'),
    cash         = ('cash',        'sum'),
).reset_index().sort_values('week_start')

weekly_inv = inv_df.groupby(['week_label','week_start']).agg(
    inv_spend=('Total_Price','sum')
).reset_index().sort_values('week_start')

weekly = weekly_sales.merge(weekly_inv, on=['week_label','week_start'], how='left')
weekly['inv_spend']     = weekly['inv_spend'].fillna(0)
weekly['food_cost_pct'] = (weekly['inv_spend'] / weekly['net_sales'].replace(0, np.nan) * 100).round(1)
weekly['gross_profit']  = weekly['net_sales'] - weekly['inv_spend']
weekly['discount_rate'] = (weekly['discounts'] / weekly['gross_before'].replace(0, np.nan) * 100).round(1)
weekly['wow_net']       = weekly['net_sales'].pct_change()   * 100
weekly['wow_gross']     = weekly['gross_before'].pct_change() * 100

# Overall KPIs
total_sales         = fin_df['net_sales'].sum()
total_gross         = fin_df['gross_before'].sum()
total_inv           = inv_df['Total_Price'].sum()
total_discounts     = fin_df['discounts'].sum()
overall_fc_pct      = round(total_inv / total_sales * 100, 1)   # vs net — operational view
overall_fc_pct_gross= round(total_inv / total_gross * 100, 1)   # vs gross — contract view
contract_disc_pct   = round(total_discounts / total_gross * 100, 1)  # Aramark/Sodexo discount rate
cc_sales_pct        = round(fin_df['credit_card'].sum() / total_gross * 100, 1)  # full-price CC %
avg_daily_net       = fin_df['net_sales'].mean()
avg_daily_gross     = fin_df['gross_before'].mean()
date_range_str      = f"{fin_df['Date'].min().strftime('%b %d')} – {fin_df['Date'].max().strftime('%b %d, %Y')}"

# Protein data
protein_df     = inv_df[inv_df['Category/Class'] == 'PROTEIN']
total_protein  = protein_df['Total_Price'].sum()
protein_pct    = round(total_protein / total_inv * 100, 1)
protein_weekly = protein_df.groupby(['week_label','week_start'])['Total_Price'].sum().reset_index().sort_values('week_start')
prot_inv_merge = protein_weekly.merge(weekly_inv, on=['week_label','week_start'], how='left')
protein_weekly['pct_of_inv'] = (prot_inv_merge['Total_Price'] / prot_inv_merge['inv_spend'] * 100).round(1).values

# Day of week stats
dow_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
dow_stats = fin_df.groupby('Day').agg(
    avg_net   = ('net_sales',    'mean'),
    avg_gross = ('gross_before', 'mean'),
    avg_disc  = ('discount_rate','mean'),
    count     = ('Date',         'count')
).reindex(dow_order).reset_index()

# ─────────────────────────────────────────
# LOGO — base64 embed so it renders in st.markdown
# ─────────────────────────────────────────
import base64, mimetypes

def load_logo_b64(path):
    try:
        mime = mimetypes.guess_type(path)[0] or "image/jpeg"
        with open(path, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        return f"data:{mime};base64,{data}"
    except Exception:
        return None

LOGO_URI = (
    load_logo_b64("/Users/mayurpatil/Downloads/NIKOS_2026/image.jpg") or
    load_logo_b64("data/image.jpg") or
    load_logo_b64("image.jpg")
)

if LOGO_URI:
    banner_left = f"""
  <div style="display:flex;align-items:center;gap:18px;">
    <img src="{LOGO_URI}"
         style="height:90px;width:90px;object-fit:contain;border-radius:12px;
                background:rgba(255,255,255,0.12);padding:4px;
                box-shadow:0 2px 12px rgba(0,0,0,0.25);" />
    <div>
      <h1 style="margin:0;font-family:'Playfair Display',serif;
                 font-size:1.9rem;color:white;letter-spacing:-0.5px;">Nikos Cafe</h1>
      <p style="margin:4px 0 0;opacity:0.85;font-size:0.88rem;color:white;">
        Unified Sales &amp; Inventory Command Center &nbsp;|&nbsp; {date_range_str}
      </p>
    </div>
  </div>"""
else:
    banner_left = f"""
  <div>
    <h1>&#x1F959; Nikos Cafe</h1>
    <p>Unified Sales &amp; Inventory Command Center &nbsp;|&nbsp; {date_range_str}</p>
  </div>"""

# ─────────────────────────────────────────
# HEADER BANNER
# ─────────────────────────────────────────
st.markdown(f"""
<div class="header-banner">
  {banner_left}
  <div style="display:flex;gap:12px;">
    <div class="header-badge"><b>${total_gross:,.0f}</b>Gross Sales</div>
    <div class="header-badge"><b>${total_sales:,.0f}</b>Net Sales</div>
    <div class="header-badge"><b>${total_inv:,.0f}</b>Inv. Spend</div>
    <div class="header-badge"><b>{overall_fc_pct}%</b>Food Cost</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# TABS
# ─────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Overview",
    "📈 Sales & Peak Periods",
    "📦 Inventory Spending",
    "💰 Food Cost & Margins",
    "⚠️ Overstock & Waste",
    "🔔 Alerts & Recovery"
])

# ══════════════════════════════════════════
# TAB 1 — OVERVIEW
# ══════════════════════════════════════════
with tab1:
    st.markdown('<div class="section-header">Key Performance Indicators</div>', unsafe_allow_html=True)
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    fc_color = "danger" if overall_fc_pct > target_food_cost else "olive"
    be_gap   = avg_daily_net - daily_fixed_cost
    be_color = "olive" if be_gap >= 0 else "danger"

    with c1:
        st.markdown(f'<div class="kpi-card"><div class="kpi-label">Gross Sales</div><div class="kpi-value">${total_gross:,.0f}</div><div class="kpi-sub">before discounts</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="kpi-card gold"><div class="kpi-label">Net Sales</div><div class="kpi-value">${total_sales:,.0f}</div><div class="kpi-sub">{fin_df["Date"].nunique()} operating days</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="kpi-card gold"><div class="kpi-label">Aramark/Sodexo Discounts</div><div class="kpi-value">${total_discounts:,.0f}</div><div class="kpi-sub">{contract_disc_pct}% contract rate — not negotiable</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="kpi-card olive"><div class="kpi-label">Inv. Spend</div><div class="kpi-value">${total_inv:,.0f}</div><div class="kpi-sub">RD + PFS combined</div></div>', unsafe_allow_html=True)
    with c5:
        st.markdown(f'<div class="kpi-card {fc_color}"><div class="kpi-label">Food Cost %</div><div class="kpi-value">{overall_fc_pct}%</div><div class="kpi-sub">Target: {target_food_cost:.0f}%</div></div>', unsafe_allow_html=True)
    with c6:
        st.markdown(f'<div class="kpi-card {be_color}"><div class="kpi-label">Avg Daily vs Break-Even</div><div class="kpi-value">{("+" if be_gap>=0 else "")}{be_gap:,.0f}</div><div class="kpi-sub">Break-even: ${daily_fixed_cost:,.0f}/day</div></div>', unsafe_allow_html=True)

    # ── BREAK-EVEN TRACKER ──────────────────────
    st.markdown('<div class="section-header">🎯 Daily Break-Even Tracker</div>', unsafe_allow_html=True)

    be_df = fin_df[['Date','Day','gross_before','net_sales','discounts']].copy()
    be_df['gap_gross'] = be_df['gross_before'] - daily_fixed_cost
    be_df['gap_net']   = be_df['net_sales']    - daily_fixed_cost
    days_above_gross   = (be_df['gap_gross'] >= 0).sum()
    days_above_net     = (be_df['gap_net']   >= 0).sum()
    total_days         = len(be_df)

    bm1, bm2, bm3, bm4 = st.columns(4)
    bm1.metric("Break-Even Target",   f"${daily_fixed_cost:,.0f}/day")
    bm2.metric("Days Above (Gross)",  f"{days_above_gross}/{total_days}", f"{days_above_gross/total_days*100:.0f}% of days")
    bm3.metric("Days Above (Net)",    f"{days_above_net}/{total_days}",   f"{days_above_net/total_days*100:.0f}% of days")
    bm4.metric("Avg Daily Net vs BE", f"${avg_daily_net - daily_fixed_cost:+,.0f}",
               "surplus" if avg_daily_net >= daily_fixed_cost else "shortfall",
               delta_color="normal" if avg_daily_net >= daily_fixed_cost else "inverse")

    fig_be = go.Figure()
    bar_colors_gross = ['#C45C3A' if v >= daily_fixed_cost else '#E8C4B8' for v in be_df['gross_before']]
    bar_colors_net   = ['#5A6B3A' if v >= daily_fixed_cost else '#BDC3C7' for v in be_df['net_sales']]
    fig_be.add_trace(go.Bar(x=be_df['Date'], y=be_df['gross_before'],
                            name='Gross Sales', marker_color=bar_colors_gross, opacity=0.6))
    fig_be.add_trace(go.Bar(x=be_df['Date'], y=be_df['net_sales'],
                            name='Net Sales', marker_color=bar_colors_net))
    fig_be.add_hline(y=daily_fixed_cost, line_dash='dash', line_color='#C0392B', line_width=2,
                     annotation_text=f'Break-Even ${daily_fixed_cost:,.0f}',
                     annotation_font_color='#A93226')
    fig_be.update_layout(
        barmode='overlay', height=380, plot_bgcolor=CREAM, paper_bgcolor=CREAM,
        hovermode='x unified', yaxis=dict(tickprefix='$', title='Sales ($)'),
        legend=dict(orientation='h', y=1.1),
        title='Daily Gross & Net Sales vs. Break-Even Line (dark = above, light = below)'
    )
    ink(fig_be)
    st.plotly_chart(fig_be, use_container_width=True)

    # ── WEEK-OVER-WEEK GROWTH ────────────────────
    st.markdown('<div class="section-header">📈 Week-over-Week Sales Growth</div>', unsafe_allow_html=True)

    w1, w2 = st.columns(2)
    with w1:
        fig_wow = go.Figure()
        wow_colors_gross = ['#C45C3A' if (pd.notna(v) and v >= 0) else '#C0392B' for v in weekly['wow_gross']]
        wow_colors_net   = ['#5A6B3A' if (pd.notna(v) and v >= 0) else '#8B3A22' for v in weekly['wow_net']]
        fig_wow.add_trace(go.Bar(
            x=weekly['week_label'], y=weekly['wow_gross'], name='Gross WoW %',
            marker_color=wow_colors_gross, opacity=0.7,
            text=weekly['wow_gross'].map(lambda x: f'{x:+.1f}%' if pd.notna(x) else 'Base'),
            textposition='outside'))
        fig_wow.add_trace(go.Bar(
            x=weekly['week_label'], y=weekly['wow_net'], name='Net WoW %',
            marker_color=wow_colors_net,
            text=weekly['wow_net'].map(lambda x: f'{x:+.1f}%' if pd.notna(x) else 'Base'),
            textposition='inside'))
        fig_wow.add_hline(y=0, line_color=INK, line_width=1)
        fig_wow.update_layout(
            barmode='group', height=340, title='Week-over-Week Growth: Gross vs Net Sales',
            plot_bgcolor=CREAM, paper_bgcolor=CREAM,
            yaxis=dict(ticksuffix='%'), legend=dict(orientation='h', y=1.1))
        ink(fig_wow)
        st.plotly_chart(fig_wow, use_container_width=True)

    with w2:
        st.markdown("**Weekly Growth Summary**")
        wow_table = weekly[['week_label','gross_before','net_sales','wow_gross','wow_net','discounts','discount_rate']].copy()
        wow_table.columns = ['Week','Gross Sales','Net Sales','Gross WoW %','Net WoW %','Aramark/Sodexo Disc.','Contract Disc. %']
        st.dataframe(
            wow_table.style
                .format({
                    'Gross Sales': '${:,.0f}', 'Net Sales': '${:,.0f}',
                    'Gross WoW %': lambda x: f'{x:+.1f}%' if pd.notna(x) else 'Base',
                    'Net WoW %':   lambda x: f'{x:+.1f}%' if pd.notna(x) else 'Base',
                    'Aramark/Sodexo Disc.': '${:,.0f}', 'Contract Disc. %': '{:.1f}%'
                })
                .background_gradient(subset=['Net WoW %'], cmap='RdYlGn', vmin=-30, vmax=30)
                .background_gradient(subset=['Contract Disc. %'], cmap='Blues', vmin=0, vmax=50),
            use_container_width=True, hide_index=True)

    st.markdown('<div class="section-header">Weekly Summary Table</div>', unsafe_allow_html=True)
    display_w = weekly[['week_label','gross_before','net_sales','discounts','discount_rate','inv_spend','food_cost_pct','gross_profit']].copy()
    display_w.columns = ['Week','Gross Sales','Net Sales','Aramark/Sodexo Disc.','Contract Disc. %','Inv. Spend','Food Cost % (Net)','Gross Profit']
    st.dataframe(
        display_w.style
            .format({'Gross Sales':'${:,.2f}','Net Sales':'${:,.2f}','Aramark/Sodexo Disc.':'${:,.2f}',
                     'Contract Disc. %':'{:.1f}%','Inv. Spend':'${:,.2f}','Food Cost % (Net)':'{:.1f}%','Gross Profit':'${:,.2f}'})
            .background_gradient(subset=['Food Cost % (Net)'], cmap='RdYlGn_r', vmin=25, vmax=60)
            .background_gradient(subset=['Net Sales'], cmap='Greens'),
        use_container_width=True, hide_index=True)

# ══════════════════════════════════════════
# TAB 2 — SALES & PEAK PERIODS
# ══════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-header">Daily Sales Trend</div>', unsafe_allow_html=True)

    fig_daily = go.Figure()
    fig_daily.add_trace(go.Scatter(x=fin_df['Date'], y=fin_df['gross_before'],
                                   name='Gross Sales', mode='lines',
                                   line=dict(color='#E8C4B8', width=1.5),
                                   fill='tozeroy', fillcolor='rgba(196,92,58,0.06)'))
    fig_daily.add_trace(go.Scatter(x=fin_df['Date'], y=fin_df['net_sales'],
                                   name='Net Sales', mode='lines+markers',
                                   line=dict(color='#C45C3A', width=2.5), marker=dict(size=5)))
    fig_daily.add_trace(go.Bar(x=fin_df['Date'], y=fin_df['discounts'],
                               name='Discounts', marker_color='rgba(212,168,83,0.6)', yaxis='y2'))
    fig_daily.add_hline(y=daily_fixed_cost, line_dash='dot', line_color='#8E44AD',
                        annotation_text=f'Break-Even ${daily_fixed_cost:,.0f}',
                        annotation_font_color='#6C3483')
    fig_daily.update_layout(
        height=400, plot_bgcolor=CREAM, paper_bgcolor=CREAM, hovermode='x unified',
        yaxis=dict(tickprefix='$', title='Sales ($)'),
        yaxis2=dict(title='Discounts ($)', overlaying='y', side='right', tickprefix='$', showgrid=False),
        legend=dict(orientation='h', y=1.12))
    ink(fig_daily)
    st.plotly_chart(fig_daily, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-header">Gross & Net Sales by Day of Week</div>', unsafe_allow_html=True)
        fig_dow = go.Figure()
        fig_dow.add_trace(go.Bar(x=dow_stats['Day'], y=dow_stats['avg_gross'], name='Avg Gross',
                                 marker_color='#E8C4B8',
                                 text=dow_stats['avg_gross'].map(lambda x: f'${x:,.0f}'), textposition='outside'))
        fig_dow.add_trace(go.Bar(x=dow_stats['Day'], y=dow_stats['avg_net'], name='Avg Net',
                                 marker_color='#C45C3A',
                                 text=dow_stats['avg_net'].map(lambda x: f'${x:,.0f}'), textposition='inside'))
        fig_dow.update_layout(barmode='overlay', height=340, plot_bgcolor=CREAM, paper_bgcolor=CREAM,
                              yaxis=dict(tickprefix='$'), legend=dict(orientation='h', y=1.1))
        ink(fig_dow)
        st.plotly_chart(fig_dow, use_container_width=True)

        best_day  = dow_stats.loc[dow_stats['avg_net'].idxmax(), 'Day']
        worst_day = dow_stats.loc[dow_stats['avg_net'].idxmin(), 'Day']
        best_row  = dow_stats[dow_stats['Day'] == best_day].iloc[0]
        worst_row = dow_stats[dow_stats['Day'] == worst_day].iloc[0]
        st.markdown(f'<div class="alert-box alert-good">🔥 <b>Best day: {best_day}</b> — avg gross ${best_row["avg_gross"]:,.0f} / net ${best_row["avg_net"]:,.0f}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="alert-box alert-warn">🐌 <b>Slowest day: {worst_day}</b> — avg gross ${worst_row["avg_gross"]:,.0f} / net ${worst_row["avg_net"]:,.0f}</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-header">Aramark/Sodexo Contract Discount Rate by Day</div>', unsafe_allow_html=True)
        fig_disc = go.Figure()
        fig_disc.add_trace(go.Bar(x=dow_stats['Day'], y=dow_stats['avg_disc'], marker_color='#2980B9',
                                  text=dow_stats['avg_disc'].map(lambda x: f'{x:.1f}%'), textposition='outside'))
        fig_disc.update_layout(height=340, plot_bgcolor=CREAM, paper_bgcolor=CREAM,
                               yaxis=dict(ticksuffix='%', title='Avg Contract Discount Rate'))
        ink(fig_disc)
        st.plotly_chart(fig_disc, use_container_width=True)
        high_disc_day = dow_stats.loc[dow_stats['avg_disc'].idxmax(), 'Day']
        st.markdown(f'<div class="alert-box alert-warn">ℹ️ <b>{high_disc_day} has the highest Aramark/Sodexo discount rate ({dow_stats["avg_disc"].max():.1f}%)</b> — this reflects your university contract (meal plans, faculty IDs). It is not controllable but is important context when reading food cost % on this day.</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-header">⏰ Time Slot Drill-Down</div>', unsafe_allow_html=True)
    if not slots_df.empty:
        day_choice = st.selectbox("Select Date", fin_df['Date'].dt.strftime('%Y-%m-%d').tolist())
        day_slots  = slots_df[slots_df['Date'] == pd.to_datetime(day_choice)].copy()
        if not day_slots.empty:
            def sort_slot(s):
                try: return datetime.strptime(s.split(' - ')[0].strip(), '%I:%M %p')
                except: return datetime(2000,1,1)
            day_slots['_sort'] = day_slots['Slot'].apply(sort_slot)
            day_slots = day_slots.sort_values('_sort')
            peak_t = day_slots['Sales'].quantile(1 - top_pct)
            slow_t = day_slots['Sales'].quantile(slow_pct)
            day_slots['color'] = day_slots['Sales'].apply(
                lambda x: '#C45C3A' if x >= peak_t else ('#D4A853' if x > slow_t else '#BDC3C7'))

            day_fin = fin_df[fin_df['Date'] == pd.to_datetime(day_choice)].iloc[0]
            m1, m2, m3, m4, m5 = st.columns(5)
            m1.metric("Gross Sales",  f"${day_fin['gross_before']:,.2f}")
            m2.metric("Net Sales",    f"${day_fin['net_sales']:,.2f}")
            m3.metric("Discounts",    f"${day_fin['discounts']:,.2f}", f"-{day_fin['discount_rate']:.1f}%")
            m4.metric("Total Txns",   f"{day_slots['Txns'].sum():.0f}")
            avg_t = day_slots['Sales'].sum() / max(day_slots['Txns'].sum(), 1)
            m5.metric("Avg Ticket",   f"${avg_t:.2f}")

            fig_slots = px.bar(day_slots, x='Slot', y='Sales', color='color',
                               color_discrete_map='identity',
                               title=f"Sales by 15-min slot — {day_choice}")
            fig_slots.update_layout(height=320, plot_bgcolor=CREAM, paper_bgcolor=CREAM,
                                    showlegend=False, xaxis_tickangle=-45, yaxis=dict(tickprefix='$'))
            ink(fig_slots)
            st.plotly_chart(fig_slots, use_container_width=True)

            p1, p2 = st.columns(2)
            with p1:
                st.markdown(f"**🔥 Peak Slots (Top {int(top_pct*100)}%)**")
                peaks = day_slots[day_slots['Sales'] >= peak_t][['Slot','Sales','Txns','Avg_Ticket']].sort_values('Sales', ascending=False)
                st.dataframe(peaks.style.format({'Sales':'${:,.2f}','Avg_Ticket':'${:.2f}','Txns':'{:.0f}'}),
                             hide_index=True, use_container_width=True)
            with p2:
                st.markdown(f"**🐌 Slow Slots (Bottom {int(slow_pct*100)}%)**")
                slows = day_slots[day_slots['Sales'] <= slow_t][['Slot','Sales','Txns','Avg_Ticket']].sort_values('Sales')
                st.dataframe(slows.style.format({'Sales':'${:,.2f}','Avg_Ticket':'${:.2f}','Txns':'{:.0f}'}),
                             hide_index=True, use_container_width=True)

# ══════════════════════════════════════════
# TAB 3 — INVENTORY SPENDING
# ══════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-header">Inventory Spend Overview</div>', unsafe_allow_html=True)
    rd_spend  = inv_df[inv_df['Vendor'] == 'Restaurant Depot']['Total_Price'].sum()
    pfs_spend = inv_df[inv_df['Vendor'] == 'Performance Food Service']['Total_Price'].sum()

    k1, k2, k3, k4, k5 = st.columns(5)
    with k1:
        st.markdown(f'<div class="kpi-card"><div class="kpi-label">Total Inv. Spend</div><div class="kpi-value">${total_inv:,.0f}</div><div class="kpi-sub">{inv_df["Category/Class"].nunique()} categories</div></div>', unsafe_allow_html=True)
    with k2:
        st.markdown(f'<div class="kpi-card gold"><div class="kpi-label">Restaurant Depot</div><div class="kpi-value">${rd_spend:,.0f}</div><div class="kpi-sub">{rd_spend/total_inv*100:.1f}% of total</div></div>', unsafe_allow_html=True)
    with k3:
        st.markdown(f'<div class="kpi-card olive"><div class="kpi-label">Perf. Food Service</div><div class="kpi-value">${pfs_spend:,.0f}</div><div class="kpi-sub">{pfs_spend/total_inv*100:.1f}% of total</div></div>', unsafe_allow_html=True)
    with k4:
        st.markdown(f'<div class="kpi-card danger"><div class="kpi-label">Protein Spend</div><div class="kpi-value">${total_protein:,.0f}</div><div class="kpi-sub">{protein_pct}% of inv. spend</div></div>', unsafe_allow_html=True)
    with k5:
        st.markdown(f'<div class="kpi-card"><div class="kpi-label">Unique Items</div><div class="kpi-value">{inv_df["Standard_Item_Name"].nunique()}</div></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        cat_spend = inv_df.groupby('Category/Class')['Total_Price'].sum().sort_values(ascending=False).reset_index()
        fig_cat = px.pie(cat_spend, names='Category/Class', values='Total_Price',
                         title='Spend by Category', hole=0.4,
                         color_discrete_sequence=px.colors.sequential.Redor)
        fig_cat.update_layout(height=380, paper_bgcolor=CREAM)
        ink(fig_cat)
        st.plotly_chart(fig_cat, use_container_width=True)
    with col2:
        top_items = inv_df.groupby('Standard_Item_Name')['Total_Price'].sum().sort_values(ascending=False).head(12).reset_index()
        fig_items = px.bar(top_items, x='Total_Price', y='Standard_Item_Name', orientation='h',
                           title='Top 12 Items by Spend',
                           color='Total_Price', color_continuous_scale=['#E8C4B8','#C45C3A'])
        fig_items.update_layout(height=380, plot_bgcolor=CREAM, paper_bgcolor=CREAM,
                                coloraxis_showscale=False, yaxis=dict(autorange='reversed'),
                                xaxis=dict(tickprefix='$'))
        ink(fig_items)
        st.plotly_chart(fig_items, use_container_width=True)

    st.markdown('<div class="section-header">Weekly Inventory Trend by Vendor</div>', unsafe_allow_html=True)
    fig_wk = go.Figure()
    for vendor, color in [('Restaurant Depot','#C45C3A'),('Performance Food Service','#D4A853')]:
        vd = inv_df[inv_df['Vendor']==vendor].groupby(['week_label','week_start'])['Total_Price'].sum().reset_index().sort_values('week_start')
        fig_wk.add_trace(go.Bar(x=vd['week_label'], y=vd['Total_Price'], name=vendor, marker_color=color))
    fig_wk.update_layout(barmode='stack', height=320, plot_bgcolor=CREAM, paper_bgcolor=CREAM,
                         yaxis=dict(tickprefix='$'), legend=dict(orientation='h', y=1.1))
    ink(fig_wk)
    st.plotly_chart(fig_wk, use_container_width=True)

    st.markdown('<div class="section-header">Category Drill-Down</div>', unsafe_allow_html=True)
    sel_cat = st.selectbox("Select Category", sorted(inv_df['Category/Class'].unique()))
    cat_df  = inv_df[inv_df['Category/Class'] == sel_cat]
    col_a, col_b = st.columns(2)
    with col_a:
        subcat = cat_df.groupby('Subcategory')['Total_Price'].sum().sort_values(ascending=False).reset_index()
        fig_sub = px.bar(subcat, x='Subcategory', y='Total_Price', title=f'{sel_cat} — by Subcategory',
                         color='Total_Price', color_continuous_scale=['#E8C4B8','#C45C3A'])
        fig_sub.update_layout(height=300, plot_bgcolor=CREAM, paper_bgcolor=CREAM,
                              coloraxis_showscale=False, yaxis=dict(tickprefix='$'))
        ink(fig_sub)
        st.plotly_chart(fig_sub, use_container_width=True)
    with col_b:
        items_cat = cat_df.groupby(['Standard_Item_Name','Vendor']).agg(
            spend=('Total_Price','sum'), qty=('Qty','sum')
        ).reset_index().sort_values('spend', ascending=False).head(10)
        st.dataframe(items_cat.style.format({'spend':'${:,.2f}','qty':'{:,.1f}'}),
                     use_container_width=True, hide_index=True)

# ══════════════════════════════════════════
# TAB 4 — FOOD COST & MARGINS
# ══════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-header">Food Cost % by Week</div>', unsafe_allow_html=True)
    latest_fc = weekly['food_cost_pct'].iloc[-1]
    # University contract dining benchmark is 35-42%, not 28-34% like independent restaurants
    UNIV_BENCHMARK_LOW, UNIV_BENCHMARK_HIGH = 35, 42
    if latest_fc > target_food_cost + 8:
        st.markdown(f'<div class="alert-box alert-bad">🚨 <b>Latest week food cost is {latest_fc}% (vs net sales)</b> — {latest_fc - target_food_cost:.1f}pp above your {target_food_cost:.0f}% target. Note: your net sales are structurally compressed by Aramark/Sodexo contract discounts ({contract_disc_pct}% of gross). Review protein spend and portion sizes.</div>', unsafe_allow_html=True)
    elif latest_fc > target_food_cost:
        st.markdown(f'<div class="alert-box alert-warn">⚠️ <b>Food cost at {latest_fc}% (vs net sales)</b> — slightly above your {target_food_cost:.0f}% target. University contract benchmark is {UNIV_BENCHMARK_LOW}–{UNIV_BENCHMARK_HIGH}%.</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="alert-box alert-good">✅ <b>Food cost at {latest_fc}% (vs net sales)</b> — within your {target_food_cost:.0f}% target. University contract dining benchmark: {UNIV_BENCHMARK_LOW}–{UNIV_BENCHMARK_HIGH}%.</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([3,2])
    with col1:
        fig_fc = go.Figure()
        fig_fc.add_trace(go.Bar(x=weekly['week_label'], y=weekly['gross_before'],
                                name='Gross Sales', marker_color='rgba(196,92,58,0.15)'))
        fig_fc.add_trace(go.Bar(x=weekly['week_label'], y=weekly['net_sales'],
                                name='Net Sales', marker_color='rgba(196,92,58,0.35)'))
        fig_fc.add_trace(go.Bar(x=weekly['week_label'], y=weekly['inv_spend'],
                                name='Inv. Spend', marker_color='#C45C3A'))
        fig_fc.add_trace(go.Scatter(x=weekly['week_label'], y=weekly['food_cost_pct'],
                                    name='Food Cost %', mode='lines+markers+text',
                                    line=dict(color='#2B2420', width=2.5), marker=dict(size=10),
                                    text=weekly['food_cost_pct'].map(lambda x: f'{x:.1f}%'),
                                    textposition='top center', yaxis='y2'))
        fig_fc.add_hline(y=target_food_cost, line_dash='dash', line_color='#27AE60',
                         annotation_text=f'Target {target_food_cost:.0f}%',
                         annotation_position='right', yref='y2')
        fig_fc.update_layout(
            barmode='overlay', height=400, plot_bgcolor=CREAM, paper_bgcolor=CREAM,
            yaxis=dict(tickprefix='$', title='Dollars'),
            yaxis2=dict(title='Food Cost %', overlaying='y', side='right',
                        ticksuffix='%', showgrid=False, range=[0, weekly['food_cost_pct'].max()*1.3]),
            legend=dict(orientation='h', y=1.12))
        ink(fig_fc)
        st.plotly_chart(fig_fc, use_container_width=True)
    with col2:
        st.markdown("**Weekly Margin Detail**")
        margin_table = weekly[['week_label','gross_before','net_sales','discounts','inv_spend','food_cost_pct','gross_profit']].copy()
        margin_table['fc_pct_gross'] = (margin_table['inv_spend'] / margin_table['gross_before'] * 100).round(1)
        margin_table.columns = ['Week','Gross Sales','Net Sales','Aramark/Sodexo Disc.','Inv. Cost','FC% (Net)','Gross Profit','FC% (Gross)']
        st.dataframe(
            margin_table.style
                .format({'Gross Sales':'${:,.0f}','Net Sales':'${:,.0f}','Aramark/Sodexo Disc.':'${:,.0f}',
                         'Inv. Cost':'${:,.0f}','FC% (Net)':'{:.1f}%','Gross Profit':'${:,.0f}','FC% (Gross)':'{:.1f}%'})
                .background_gradient(subset=['FC% (Net)'], cmap='RdYlGn_r', vmin=25, vmax=65),
            use_container_width=True, hide_index=True)

    st.markdown('<div class="section-header">Net Profitability After All Fees</div>', unsafe_allow_html=True)
    aramark_fee = total_sales * aramark_rate
    cc_fee      = fin_df['credit_card'].sum() * cc_fee_rate
    net_after   = total_sales - total_inv - aramark_fee - cc_fee
    f1, f2, f3, f4, f5 = st.columns(5)
    f1.metric("Gross Sales",              f"${total_gross:,.0f}")
    f2.metric("Net Sales (after Aramark disc.)", f"${total_sales:,.0f}", f"-${total_discounts:,.0f} contract disc.", delta_color='inverse')
    f3.metric("Aramark/Sodexo Commission",f"-${aramark_fee:,.0f}", f"{aramark_rate*100:.1f}% of net sales", delta_color='inverse')
    f4.metric("CC Processing Fee",        f"-${cc_fee:,.0f}",      f"{cc_fee_rate*100:.1f}% of CC sales", delta_color='inverse')
    f5.metric("Est. Net After All Fees",  f"${net_after:,.0f}",    f"{net_after/total_sales*100:.1f}% net margin")

    st.markdown('<div class="section-header">🏛️ Contract Economics — Two Ways to Read Food Cost</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="alert-box alert-warn">
    ℹ️ <b>University contract context:</b> Aramark/Sodexo sets your discount rate as part of the campus dining contract (meal plans, faculty/staff IDs, student discounts).
    These are <b>not promotional discounts you control</b> — they are contract obligations. This means food cost % looks very different depending on which revenue base you use.
    </div>
    """, unsafe_allow_html=True)

    ec1, ec2, ec3, ec4 = st.columns(4)
    ec1.metric("Gross Sales",         f"${total_gross:,.0f}", "before contract discounts")
    ec2.metric("Aramark/Sodexo Disc.",f"${total_discounts:,.0f}", f"{contract_disc_pct}% of gross — contract rate")
    ec3.metric("FC% vs Net Sales",    f"{overall_fc_pct}%",  "kitchen operations view")
    ec4.metric("FC% vs Gross Sales",  f"{overall_fc_pct_gross}%", "contract economics view")

    # Side-by-side comparison chart
    comparison_data = {
        'View': ['FC% vs Net Sales\n(Operational)', 'FC% vs Gross Sales\n(Contract)'],
        'FC%':  [overall_fc_pct, overall_fc_pct_gross],
        'Color':['#C45C3A', '#2980B9']
    }
    fig_compare = go.Figure()
    fig_compare.add_trace(go.Bar(
        x=comparison_data['View'], y=comparison_data['FC%'],
        marker_color=comparison_data['Color'],
        text=[f"{v}%" for v in comparison_data['FC%']],
        textposition='outside', width=0.4
    ))
    fig_compare.add_hline(y=38, line_dash='dash', line_color=CLAY,
                          annotation_text='Univ. contract target ~38% (net view)')
    fig_compare.add_hline(y=27, line_dash='dash', line_color='#2980B9',
                          annotation_text='Univ. contract target ~27% (gross view)')
    fig_compare.update_layout(
        height=320, plot_bgcolor=CREAM, paper_bgcolor=CREAM,
        yaxis=dict(ticksuffix='%', title='Food Cost %', range=[0, 70]),
        title='Food Cost % — Operational View vs. Contract Economics View',
        showlegend=False
    )
    ink(fig_compare)
    st.plotly_chart(fig_compare, use_container_width=True)

    st.markdown("""
    <div style="background:#F0F4F8;border-radius:10px;padding:16px 20px;font-size:0.88rem;color:#2B2420;">
    <b>Which number to use when:</b><br><br>
    🔴 <b>FC% vs Net Sales ({fc_net}%)</b> — Use this for <b>kitchen management</b>: portion control, protein cost, waste reduction, ordering decisions. This is the true cost of running your kitchen against money actually received.<br><br>
    🔵 <b>FC% vs Gross Sales ({fc_gross}%)</b> — Use this when <b>reporting to Aramark/Sodexo or the university</b> or evaluating your contract value. This shows performance against the full transaction volume before contract discounts are applied.<br><br>
    ⚠️ <b>Never compare your FC% directly to an independent restaurant's benchmark</b> — their net and gross sales are nearly identical. Yours differ by {disc_pct}% due to the contract.
    </div>
    """.format(fc_net=overall_fc_pct, fc_gross=overall_fc_pct_gross, disc_pct=contract_disc_pct),
    unsafe_allow_html=True)
    cat_spend2 = inv_df.groupby('Category/Class')['Total_Price'].sum().sort_values(ascending=False).reset_index()
    cat_spend2['% of Inv']       = (cat_spend2['Total_Price'] / total_inv    * 100).round(1)
    cat_spend2['% of Net Sales'] = (cat_spend2['Total_Price'] / total_sales  * 100).round(1)
    cat_spend2['% of Gross']     = (cat_spend2['Total_Price'] / total_gross  * 100).round(1)
    fig_cat3 = go.Figure()
    fig_cat3.add_trace(go.Bar(x=cat_spend2['Category/Class'], y=cat_spend2['% of Inv'],
                              name='% of Inv. Spend', marker_color='#C45C3A'))
    fig_cat3.add_trace(go.Bar(x=cat_spend2['Category/Class'], y=cat_spend2['% of Net Sales'],
                              name='% of Net Sales', marker_color='#D4A853'))
    fig_cat3.add_trace(go.Bar(x=cat_spend2['Category/Class'], y=cat_spend2['% of Gross'],
                              name='% of Gross Sales', marker_color='#5A6B3A'))
    fig_cat3.update_layout(barmode='group', height=360, plot_bgcolor=CREAM, paper_bgcolor=CREAM,
                           yaxis=dict(ticksuffix='%'), legend=dict(orientation='h', y=1.1))
    ink(fig_cat3)
    st.plotly_chart(fig_cat3, use_container_width=True)

# ══════════════════════════════════════════
# TAB 5 — OVERSTOCK & WASTE
# ══════════════════════════════════════════
with tab5:
    st.markdown('<div class="section-header">Overstock & Understock Analysis</div>', unsafe_allow_html=True)
    st.info("💡 Compares what you bought each week vs. a consistent ordering baseline. Weeks far above average signal overstock / waste risk.")

    avg_wk_spend = weekly['inv_spend'].mean()
    weekly['spend_vs_avg'] = ((weekly['inv_spend'] - avg_wk_spend) / avg_wk_spend * 100).round(1)
    weekly['status'] = weekly['spend_vs_avg'].apply(
        lambda x: '🔴 Over' if x > 20 else ('🟢 Normal' if x > -20 else '🟡 Under'))

    fig_os = go.Figure()
    os_colors = weekly['spend_vs_avg'].apply(lambda x: '#C0392B' if x > 20 else ('#27AE60' if x > -20 else '#D4A853'))
    fig_os.add_trace(go.Bar(x=weekly['week_label'], y=weekly['spend_vs_avg'],
                            marker_color=os_colors.tolist(),
                            text=weekly['spend_vs_avg'].map(lambda x: f'{x:+.1f}%'),
                            textposition='outside'))
    fig_os.add_hline(y=0,   line_color=INK, line_width=1)
    fig_os.add_hline(y=20,  line_dash='dash', line_color='#C0392B',  annotation_text='Overstock threshold')
    fig_os.add_hline(y=-20, line_dash='dash', line_color='#D4A853', annotation_text='Understock threshold')
    fig_os.update_layout(title='Weekly Spend vs. Average', height=320,
                         plot_bgcolor=CREAM, paper_bgcolor=CREAM, yaxis=dict(ticksuffix='%'))
    ink(fig_os)
    st.plotly_chart(fig_os, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Weekly Purchasing Status**")
        status_table = weekly[['week_label','inv_spend','spend_vs_avg','status','gross_before','net_sales']].copy()
        status_table.columns = ['Week','Inv. Spend','vs Avg %','Status','Gross Sales','Net Sales']
        st.dataframe(status_table.style.format(
            {'Inv. Spend':'${:,.0f}','vs Avg %':'{:+.1f}%','Gross Sales':'${:,.0f}','Net Sales':'${:,.0f}'}),
            use_container_width=True, hide_index=True)
    with col2:
        st.markdown("**Waste Risk by Week**")
        weekly['spend_per_sales'] = (weekly['inv_spend'] / weekly['net_sales'] * 100).round(1)
        for _, row in weekly.iterrows():
            ratio = row['spend_per_sales']
            color = 'alert-bad' if ratio > target_food_cost+15 else ('alert-warn' if ratio > target_food_cost else 'alert-good')
            icon  = '🚨' if ratio > target_food_cost+15 else ('⚠️' if ratio > target_food_cost else '✅')
            st.markdown(
                f'<div class="alert-box {color}">{icon} <b>{row["week_label"]}:</b> {ratio}% food cost '
                f'— gross ${row["gross_before"]:,.0f} / net ${row["net_sales"]:,.0f} / inv ${row["inv_spend"]:,.0f}</div>',
                unsafe_allow_html=True)

    st.markdown('<div class="section-header">Purchasing Consistency by Category</div>', unsafe_allow_html=True)
    cat_weekly2 = inv_df.groupby(['week_label','week_start','Category/Class'])['Total_Price'].sum().reset_index()
    cat_avg2    = cat_weekly2.groupby('Category/Class')['Total_Price'].mean().reset_index(); cat_avg2.columns = ['Category','Avg Weekly Spend']
    cat_std2    = cat_weekly2.groupby('Category/Class')['Total_Price'].std().fillna(0).reset_index(); cat_std2.columns = ['Category','Std Dev']
    cat_stats   = cat_avg2.merge(cat_std2, on='Category')
    cat_stats['CV %'] = (cat_stats['Std Dev'] / cat_stats['Avg Weekly Spend'] * 100).round(1)
    cat_stats['Risk'] = cat_stats['CV %'].apply(lambda x: '🔴 High' if x > 50 else ('🟡 Moderate' if x > 25 else '🟢 Consistent'))
    st.dataframe(
        cat_stats.sort_values('CV %', ascending=False)
            .style.format({'Avg Weekly Spend':'${:,.0f}','Std Dev':'${:,.0f}','CV %':'{:.1f}%'})
            .background_gradient(subset=['CV %'], cmap='RdYlGn_r', vmin=0, vmax=80),
        use_container_width=True, hide_index=True)

    st.markdown('<div class="section-header">High-Volume Perishables — Spoilage Watch</div>', unsafe_allow_html=True)
    perishable_cats = ['PRODUCE','DAIRY PROD & SUBS','PROTEIN','SEAFOOD','GROCERY REFRIGERATED']
    p_items = inv_df[inv_df['Category/Class'].isin(perishable_cats)].groupby(
        ['Standard_Item_Name','Category/Class']
    ).agg(total_spend=('Total_Price','sum'), total_qty=('Qty','sum'), orders=('Invoice_No','nunique')).reset_index()
    p_items = p_items.sort_values('total_spend', ascending=False).head(15)
    fig_perish = px.scatter(p_items, x='total_qty', y='total_spend', size='orders',
                            color='Category/Class', hover_name='Standard_Item_Name',
                            title='Perishable Items — Spend vs. Quantity (bubble = # of orders)',
                            color_discrete_sequence=['#C45C3A','#D4A853','#5A6B3A','#8B3A22','#2B2420'])
    fig_perish.update_layout(height=380, plot_bgcolor=CREAM, paper_bgcolor=CREAM,
                             xaxis_title='Total Qty Ordered', yaxis=dict(tickprefix='$'))
    ink(fig_perish)
    st.plotly_chart(fig_perish, use_container_width=True)

# ══════════════════════════════════════════
# TAB 6 — ALERTS & RECOVERY
# ══════════════════════════════════════════
with tab6:

    # ── PROTEIN COST ALERT ───────────────────────
    st.markdown('<div class="section-header">🥩 Protein Cost Alert</div>', unsafe_allow_html=True)

    beef_spend = inv_df[inv_df['Standard_Item_Name']=='Beef']['Total_Price'].sum()
    lamb_spend = inv_df[inv_df['Standard_Item_Name']=='Lamb']['Total_Price'].sum()
    avg_protein_weekly = protein_weekly['Total_Price'].mean()
    latest_protein_pct = protein_weekly['pct_of_inv'].iloc[-1] if not protein_weekly.empty else 0

    p1, p2, p3, p4 = st.columns(4)
    with p1:
        st.markdown(f'<div class="protein-card"><div class="kpi-label">Total Protein Spend</div><div class="kpi-value">${total_protein:,.0f}</div><div class="kpi-sub">{protein_pct}% of all inventory</div></div>', unsafe_allow_html=True)
    with p2:
        st.markdown(f'<div class="protein-card"><div class="kpi-label">Avg Weekly Protein</div><div class="kpi-value">${avg_protein_weekly:,.0f}</div><div class="kpi-sub">per week</div></div>', unsafe_allow_html=True)
    with p3:
        alert_color = "danger" if protein_pct > protein_alert_pct else "olive"
        st.markdown(f'<div class="kpi-card {alert_color}"><div class="kpi-label">Latest Week Protein %</div><div class="kpi-value">{latest_protein_pct:.1f}%</div><div class="kpi-sub">Alert threshold: {protein_alert_pct:.0f}%</div></div>', unsafe_allow_html=True)
    with p4:
        st.markdown(f'<div class="kpi-card danger"><div class="kpi-label">Beef + Lamb Alone</div><div class="kpi-value">${beef_spend+lamb_spend:,.0f}</div><div class="kpi-sub">{(beef_spend+lamb_spend)/total_protein*100:.0f}% of protein budget</div></div>', unsafe_allow_html=True)

    if protein_pct > protein_alert_pct:
        st.markdown(f'<div class="alert-box alert-bad">🚨 <b>Protein is {protein_pct}% of total inventory spend</b> — above your {protein_alert_pct:.0f}% alert threshold. Beef (${beef_spend:,.0f}) and Lamb (${lamb_spend:,.0f}) are the top drivers. Consider menu pricing review or supplier negotiation.</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="alert-box alert-good">✅ <b>Protein at {protein_pct}% of inventory spend</b> — within your {protein_alert_pct:.0f}% threshold.</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        fig_prot = go.Figure()
        fig_prot.add_trace(go.Bar(x=protein_weekly['week_label'], y=protein_weekly['Total_Price'],
                                  name='Protein Spend', marker_color='#8B3A22'))
        fig_prot.add_hline(y=avg_protein_weekly, line_dash='dash', line_color=CLAY,
                           annotation_text=f'Avg ${avg_protein_weekly:,.0f}')
        fig_prot.update_layout(title='Weekly Protein Spend', height=300,
                               plot_bgcolor=CREAM, paper_bgcolor=CREAM, yaxis=dict(tickprefix='$'))
        ink(fig_prot)
        st.plotly_chart(fig_prot, use_container_width=True)
    with col2:
        prot_items = protein_df.groupby('Standard_Item_Name')['Total_Price'].sum().sort_values(ascending=False).reset_index()
        fig_pi = px.pie(prot_items, names='Standard_Item_Name', values='Total_Price',
                        title='Protein Spend by Item', hole=0.35,
                        color_discrete_sequence=['#8B3A22','#C45C3A','#D4A853','#E8C4B8','#5A6B3A','#2B2420','#8C7B72','#BDC3C7'])
        fig_pi.update_layout(height=300, paper_bgcolor=CREAM)
        ink(fig_pi)
        st.plotly_chart(fig_pi, use_container_width=True)

    # Price trend for top proteins
    prot_price   = protein_df.groupby(['Standard_Item_Name','Invoice_Date']).agg(unit_price=('Unit_Price','mean')).reset_index().sort_values('Invoice_Date')
    top_proteins = prot_items['Standard_Item_Name'].head(4).tolist()
    if top_proteins:
        st.markdown("**Unit Price Trend — Top Protein Items** (watch for supplier price creep)")
        fig_pp = go.Figure()
        for i, item in enumerate(['#8B3A22','#C45C3A','#D4A853','#5A6B3A']):
            if i >= len(top_proteins): break
            name = top_proteins[i]
            d = prot_price[prot_price['Standard_Item_Name'] == name]
            if len(d) > 1:
                fig_pp.add_trace(go.Scatter(x=d['Invoice_Date'], y=d['unit_price'],
                                            name=name, mode='lines+markers',
                                            line=dict(color=item, width=2), marker=dict(size=7)))
        fig_pp.update_layout(height=280, plot_bgcolor=CREAM, paper_bgcolor=CREAM,
                             yaxis=dict(tickprefix='$', title='Unit Price'),
                             legend=dict(orientation='h', y=1.1))
        ink(fig_pp)
        st.plotly_chart(fig_pp, use_container_width=True)

    st.markdown("---")

    # ── SLOW DAY RECOVERY SUGGESTIONS ───────────────
    st.markdown('<div class="section-header">🐌 Slow Day Recovery Suggestions</div>', unsafe_allow_html=True)
    st.markdown("Data-driven strategies for your 3 slowest days. Note: discount rates reflect Aramark/Sodexo contract terms and are not levers you can pull.")

    slow_days_ranked = dow_stats.dropna(subset=['avg_net']).sort_values('avg_net')

    for _, day_row in slow_days_ranked.head(3).iterrows():
        day         = day_row['Day']
        avg_net     = day_row['avg_net']
        avg_gross   = day_row['avg_gross']
        avg_disc    = day_row['avg_disc']
        gap_to_be   = avg_net - daily_fixed_cost
        gap_to_best = dow_stats['avg_net'].max() - avg_net

        suggestions = []

        # Contract context — don't suggest changing discounts
        suggestions.append(f"ℹ️ The {avg_disc:.1f}% discount rate on {day}s is set by your Aramark/Sodexo contract — focus on increasing <b>transaction volume</b>, not discount depth.")

        # University-specific traffic levers
        if day in ['Sunday','Saturday']:
            suggestions.append("📣 Weekend foot traffic on a university campus drops when students leave. Consider promoting to local community, faculty families, or campus event attendees.")
            suggestions.append("🍽️ Offer a weekend-only menu item or combo exclusive to Saturday/Sunday — creates a reason to visit even with a lighter campus population.")
        if day in ['Monday']:
            suggestions.append("📚 Monday is often a recovery day after the weekend. Target early lunch through campus digital boards or email blasts before 10am.")
        if day in ['Tuesday']:
            suggestions.append("🎯 Tuesday tends to be mid-week low — consider coordinating with campus student orgs or clubs for group orders or catering pickups on this day.")
        if day == 'Friday':
            suggestions.append("🕐 Fridays often see a lunch rush then a sharp afternoon drop as students leave campus. Maximize the lunch window — fast service and visible specials board matter most.")
            suggestions.append("📦 Consider a 'grab and go for the weekend' bundle on Fridays — students leaving for the weekend may buy extra if prompted.")

        # Credit card vs meal plan context
        suggestions.append(f"💳 Credit card transactions (full price, no Aramark discount) are your highest-margin sales. Find ways to attract off-campus visitors or faculty on {day}s who pay by card.")

        # Break-even and inventory sizing
        if gap_to_be < 0:
            suggestions.append(f"🚨 This day averages ${abs(gap_to_be):,.0f} <b>below break-even</b>. Right-sizing staffing and prep quantities on {day}s is the most direct lever you have.")
        else:
            suggestions.append(f"✅ Clears break-even by ${gap_to_be:,.0f} on average, but still has ${gap_to_best:,.0f} of upside vs. your best day ({dow_stats.loc[dow_stats['avg_net'].idxmax(),'Day']}).")

        suggestions.append(f"📦 Scale your inventory ordering down for {day}s — over-prepping for low-volume days directly inflates food cost % and waste risk.")

        sugg_html = "".join([f"<li style='margin:6px 0;'>{s}</li>" for s in suggestions])
        st.markdown(f"""
        <div style="background:white;border-radius:14px;padding:20px 24px;
                    border-left:5px solid #D4A853;box-shadow:0 2px 12px rgba(0,0,0,0.06);margin-bottom:16px;">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
            <div>
              <span style="font-family:'Playfair Display',serif;font-size:1.2rem;color:#C45C3A;font-weight:700;">{day}</span>
              <span style="color:#8C7B72;font-size:0.85rem;margin-left:12px;">
                Avg Gross: <b>${avg_gross:,.0f}</b> &nbsp;|&nbsp; Avg Net: <b>${avg_net:,.0f}</b> &nbsp;|&nbsp;
                Contract Disc: <b>{avg_disc:.1f}%</b> (Aramark/Sodexo)
              </span>
            </div>
            <div style="background:#FAF6F0;border-radius:8px;padding:6px 14px;font-size:0.85rem;">
              {'🔴 Below break-even' if gap_to_be < 0 else f'🟢 +${gap_to_be:,.0f} above break-even'}
            </div>
          </div>
          <ul style="margin:0;padding-left:18px;color:#2B2420;font-size:0.9rem;">{sugg_html}</ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">📋 All Days — Performance vs Break-Even</div>', unsafe_allow_html=True)
    be_summary = dow_stats[['Day','avg_gross','avg_net','avg_disc','count']].copy()
    be_summary['vs_break_even'] = be_summary['avg_net'] - daily_fixed_cost
    be_summary['status'] = be_summary['vs_break_even'].apply(
        lambda x: '🔴 Below BE' if x < 0 else ('🟡 Near BE' if x < 200 else '🟢 Above BE'))
    be_summary.columns = ['Day','Avg Gross','Avg Net','Contract Disc % (Aramark)','# Days Observed','vs Break-Even','Status']
    st.dataframe(
        be_summary.style
            .format({'Avg Gross':'${:,.0f}','Avg Net':'${:,.0f}','Contract Disc % (Aramark)':'{:.1f}%','vs Break-Even':'${:+,.0f}'})
            .background_gradient(subset=['Avg Net'],       cmap='RdYlGn', vmin=800,  vmax=2500)
            .background_gradient(subset=['vs Break-Even'], cmap='RdYlGn', vmin=-500, vmax=1500),
        use_container_width=True, hide_index=True)

# ─────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<div style='text-align:center;color:#8C7B72;font-size:0.8rem;'>"
    "Nikos Cafe Command Center &nbsp;|&nbsp; "
    "Sales: Oracle Micros Symphony + GetApp &nbsp;·&nbsp; "
    "Inventory: Restaurant Depot + Performance Food Service &nbsp;|&nbsp; "
    "Thu–Wed week cycle"
    "</div>",
    unsafe_allow_html=True)
