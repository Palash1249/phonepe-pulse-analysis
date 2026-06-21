import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="PhonePe Pulse · India UPI Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ── page background ── */
.stApp { background-color: #0f0c1a; }
section[data-testid="stSidebar"] { background-color: #160d2e; border-right: 1px solid #2a1f4e; }

/* ── hide default streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2.5rem 2rem 2.5rem; max-width: 1400px; }

/* ── hide sidebar collapse button — all known selectors ── */
[data-testid="collapsedControl"],
button[kind="header"],
.st-emotion-cache-h5rgaw,
.st-emotion-cache-1dp5vir,
.eyeqlp53,
.e1fqkh3o0 {
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
    pointer-events: none !important;
    width: 0 !important;
    height: 0 !important;
}

/* ── force sidebar always open ── */
section[data-testid="stSidebar"] {
    min-width: 260px !important;
    max-width: 260px !important;
    transform: translateX(0) !important;
}

/* ── sidebar headings ── */
.sidebar-brand {
    font-size: 20px;
    font-weight: 700;
    color: #a78bfa;
    letter-spacing: -0.5px;
    margin-bottom: 4px;
}
.sidebar-sub {
    font-size: 11px;
    color: #6b5fa0;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 24px;
}

/* ── page header ── */
.page-eyebrow {
    font-size: 11px;
    font-weight: 600;
    color: #7c3aed;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 6px;
}
.page-title {
    font-size: 36px;
    font-weight: 700;
    color: #f5f0ff;
    letter-spacing: -1px;
    line-height: 1.15;
    margin-bottom: 6px;
}
.page-subtitle {
    font-size: 14px;
    color: #7b6fa8;
    margin-bottom: 32px;
}

/* ── KPI cards ── */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-bottom: 36px;
}
.kpi-card {
    background: #1a1133;
    border: 1px solid #2a1f4e;
    border-radius: 12px;
    padding: 22px 24px;
    position: relative;
    overflow: hidden;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #7c3aed, #a78bfa);
    border-radius: 12px 12px 0 0;
}
.kpi-label {
    font-size: 11px;
    font-weight: 600;
    color: #6b5fa0;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    margin-bottom: 10px;
}
.kpi-value {
    font-size: 28px;
    font-weight: 700;
    color: #f5f0ff;
    letter-spacing: -0.5px;
    line-height: 1;
}
.kpi-delta {
    font-size: 12px;
    color: #4ade80;
    margin-top: 6px;
    font-weight: 500;
}

/* ── section headers ── */
.section-label {
    font-size: 11px;
    font-weight: 600;
    color: #7c3aed;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 4px;
}
.section-title {
    font-size: 18px;
    font-weight: 600;
    color: #e9e0ff;
    margin-bottom: 16px;
    letter-spacing: -0.3px;
}

/* ── insight callout ── */
.insight-box {
    background: #1a1133;
    border: 1px solid #2a1f4e;
    border-left: 3px solid #7c3aed;
    border-radius: 8px;
    padding: 16px 20px;
    margin-bottom: 28px;
    font-size: 13px;
    color: #a99dc8;
    line-height: 1.6;
}
.insight-box strong { color: #c4b5fd; }

/* ── divider ── */
.divider {
    border: none;
    border-top: 1px solid #2a1f4e;
    margin: 32px 0;
}

/* ── streamlit widget overrides ── */
.stMultiSelect [data-baseweb="tag"] {
    background-color: #2d1f5e !important;
    color: #c4b5fd !important;
}
div[data-testid="stMetricValue"] { color: #f5f0ff !important; font-size: 28px !important; }
label[data-testid="stWidgetLabel"] p { color: #6b5fa0 !important; font-size: 11px !important; text-transform: uppercase; letter-spacing: 1px; }
            
/* nuclear option — hide ALL buttons in top-left corner */
.st-emotion-cache-czk5ss,
.st-emotion-cache-1dp5vir,
[data-testid="collapsedControl"],
[data-testid="stSidebarCollapsedControl"] {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)

# ── JS: hide sidebar toggle button (works on all Streamlit versions) ──────
st.components.v1.html("""
<script>
function hideSidebarToggle() {
    const selectors = [
        '[data-testid="collapsedControl"]',
        'button[aria-label="Close sidebar"]',
        'button[aria-label="Open sidebar"]',
        'button[aria-label="Collapse sidebar"]',
        'button[kind="header"]'
    ];
    selectors.forEach(sel => {
        document.querySelectorAll(sel).forEach(el => {
            el.style.setProperty('display', 'none', 'important');
            el.style.setProperty('visibility', 'hidden', 'important');
            el.style.setProperty('pointer-events', 'none', 'important');
        });
    });
}
hideSidebarToggle();
const interval = setInterval(hideSidebarToggle, 300);
setTimeout(() => clearInterval(interval), 5000);
</script>
""", height=0)

# ── load data ─────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df_t = pd.read_csv("../data/agg_transactions.csv")
    df_u = pd.read_csv("../data/agg_users.csv")
    df_t['state'] = df_t['state'].str.replace('-', ' ').str.title()
    df_u['state'] = df_u['state'].str.replace('-', ' ').str.title()
    df_t['amount_cr'] = df_t['amount'] / 1e7
    df_t['period'] = df_t['year'].astype(str) + ' Q' + df_t['quarter'].astype(str)
    df_u['period'] = df_u['year'].astype(str) + ' Q' + df_u['quarter'].astype(str)
    return df_t, df_u

df_t, df_u = load_data()

PURPLE      = "#7c3aed"
PURPLE_LITE = "#a78bfa"
TEAL        = "#2dd4bf"
CARD_BG     = "#1a1133"
PLOT_BG     = "#0f0c1a"
GRID_COL    = "#1e1535"
TEXT_PRI    = "#f5f0ff"
TEXT_SEC    = "#7b6fa8"

def chart_layout(fig, height=340):
    fig.update_layout(
        paper_bgcolor=CARD_BG,
        plot_bgcolor=CARD_BG,
        font=dict(family="Inter", color=TEXT_SEC, size=11),
        height=height,
        margin=dict(l=12, r=12, t=20, b=12),
        xaxis=dict(gridcolor=GRID_COL, linecolor=GRID_COL, tickfont=dict(size=10)),
        yaxis=dict(gridcolor=GRID_COL, linecolor=GRID_COL, tickfont=dict(size=10)),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=10, color=TEXT_SEC)),
        coloraxis_showscale=False,
    )
    return fig

# ── sidebar ───────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/7/71/PhonePe_Logo.svg", width=180)
    st.markdown('<div class="sidebar-brand">PhonePe Pulse</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-sub">India UPI Analytics · 2018–2024</div>', unsafe_allow_html=True)

    years = sorted(df_t['year'].unique())
    selected_years = st.multiselect("Years", years, default=years)

    states = sorted(df_t['state'].unique())
    selected_states = st.multiselect("States", states, default=states)

    txn_types = list(df_t['transaction_type'].unique())
    selected_type = st.multiselect("Transaction type", txn_types, default=txn_types)

    st.markdown("---")
    st.markdown(f'<div style="font-size:11px;color:#7b6fa8;">Data · PhonePe Pulse GitHub<br>Built with Python · Streamlit · Plotly</div>', unsafe_allow_html=True)

# ── filter ────────────────────────────────────────────────────────────────
ft = df_t[
    df_t['year'].isin(selected_years) &
    df_t['state'].isin(selected_states) &
    df_t['transaction_type'].isin(selected_type)
]
fu = df_u[
    df_u['year'].isin(selected_years) &
    df_u['state'].isin(selected_states)
]

# ── page header ───────────────────────────────────────────────────────────
st.markdown('<div class="page-eyebrow">India · Digital Payments Intelligence</div>', unsafe_allow_html=True)
st.image("https://upload.wikimedia.org/wikipedia/commons/7/71/PhonePe_Logo.svg", width=300)
st.markdown('<div class="page-title">PhonePe Pulse Analytics</div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">Tracking UPI adoption, transaction growth, and engagement across 36 states — 2018 to 2024</div>', unsafe_allow_html=True)

# ── KPI cards ─────────────────────────────────────────────────────────────
total_txn   = ft['count'].sum()
total_amt   = ft['amount_cr'].sum()
total_users = fu['registered_users'].sum()
total_st    = ft['state'].nunique()

st.markdown(f"""
<div class="kpi-grid">
  <div class="kpi-card">
    <div class="kpi-label">Total transactions</div>
    <div class="kpi-value">{total_txn/1e9:.1f}B</div>
    <div class="kpi-delta">↑ Across all quarters</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-label">Transaction value</div>
    <div class="kpi-value">₹{total_amt/1e5:.1f}L Cr</div>
    <div class="kpi-delta">↑ Cumulative 2018–2024</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-label">Registered users</div>
    <div class="kpi-value">{total_users/1e7:.1f} Cr</div>
    <div class="kpi-delta">↑ Across selected states</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-label">States covered</div>
    <div class="kpi-value">{total_st}</div>
    <div class="kpi-delta">Including UTs</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── insight callout ───────────────────────────────────────────────────────
st.markdown("""
<div class="insight-box">
  <strong>Key insight:</strong> UPI transaction volume grew over <strong>40× between 2018 and 2024</strong>.
  Manipur leads YoY growth among all states — a signal of rapid digital payment adoption in Northeast India.
  States with high registered users but low transactions per user represent the biggest re-engagement opportunity.
</div>
""", unsafe_allow_html=True)

# ── row 1: growth trend + transaction type ────────────────────────────────
col1, col2 = st.columns([3, 2])

with col1:
    st.markdown('<div class="section-label">Growth</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">National UPI transaction value over time</div>', unsafe_allow_html=True)

    national = ft.groupby('period').agg(
        total_amount=('amount_cr', 'sum'),
        total_count=('count', 'sum')
    ).reset_index()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=national['period'], y=national['total_amount'],
        mode='lines+markers',
        line=dict(color=PURPLE, width=2.5),
        marker=dict(size=5, color=PURPLE_LITE),
        fill='tozeroy',
        fillcolor='rgba(124,58,237,0.08)',
        name='Amount (₹ Cr)'
    ))
    fig.update_xaxes(tickangle=45, tickfont=dict(size=9))
    fig.update_yaxes(title_text="₹ Crores", title_font=dict(size=10))
    chart_layout(fig, height=320)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown('<div class="section-label">Composition</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Transaction type split</div>', unsafe_allow_html=True)

    type_data = ft.groupby('transaction_type')['count'].sum().reset_index()
    fig2 = px.pie(
        type_data, names='transaction_type', values='count',
        color_discrete_sequence=[PURPLE, TEAL, "#a78bfa", "#34d399", "#f472b6"],
        hole=0.55
    )
    fig2.update_traces(
        textposition='outside',
        textinfo='percent+label',
        textfont_size=10,
        marker=dict(line=dict(color=CARD_BG, width=2))
    )
    chart_layout(fig2, height=320)
    st.plotly_chart(fig2, use_container_width=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── row 2: top states + YoY growth ───────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="section-label">Market size</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Top 10 states by transaction value</div>', unsafe_allow_html=True)

    top_states = (ft.groupby('state')['amount_cr']
                  .sum().sort_values(ascending=True)
                  .tail(10).reset_index())
    fig3 = px.bar(
        top_states, x='amount_cr', y='state',
        orientation='h',
        color='amount_cr',
        color_continuous_scale=[[0, "#2d1f5e"], [1, PURPLE_LITE]]
    )
    fig3.update_traces(marker_line_width=0)
    fig3.update_xaxes(title_text="₹ Crores")
    fig3.update_yaxes(title_text="")
    chart_layout(fig3, height=340)
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    st.markdown('<div class="section-label">Momentum</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Fastest growing states (latest year YoY)</div>', unsafe_allow_html=True)

    sy = ft.groupby(['state', 'year'])['amount_cr'].sum().reset_index()
    sy['prev'] = sy.groupby('state')['amount_cr'].shift(1)
    sy['yoy'] = (sy['amount_cr'] - sy['prev']) / sy['prev'] * 100
    latest_yr = sy['year'].max()
    top_g = (sy[sy['year'] == latest_yr].dropna()
             .sort_values('yoy', ascending=True).tail(10))
    fig4 = px.bar(
        top_g, x='yoy', y='state',
        orientation='h',
        color='yoy',
        color_continuous_scale=[[0, "#0f766e"], [1, TEAL]]
    )
    fig4.update_traces(marker_line_width=0)
    fig4.update_xaxes(title_text="YoY Growth (%)")
    fig4.update_yaxes(title_text="")
    chart_layout(fig4, height=340)
    st.plotly_chart(fig4, use_container_width=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── row 3: quarterly seasonality ─────────────────────────────────────────
st.markdown('<div class="section-label">Seasonality</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Average transaction value by quarter — festive spike detector</div>', unsafe_allow_html=True)

qtr = ft.groupby(['year', 'quarter'])['amount_cr'].sum().reset_index()
qtr_avg = qtr.groupby('quarter')['amount_cr'].mean().reset_index()
qtr_avg['quarter_label'] = qtr_avg['quarter'].map({
    1: 'Q1 · Jan–Mar', 2: 'Q2 · Apr–Jun',
    3: 'Q3 · Jul–Sep', 4: 'Q4 · Oct–Dec (Festive)'
})
fig5 = px.bar(
    qtr_avg, x='quarter_label', y='amount_cr',
    color='amount_cr',
    color_continuous_scale=[[0, "#2d1f5e"], [1, PURPLE_LITE]]
)
fig5.update_traces(marker_line_width=0)
fig5.update_xaxes(title_text="")
fig5.update_yaxes(title_text="Avg ₹ Crores")
chart_layout(fig5, height=280)
st.plotly_chart(fig5, use_container_width=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── row 4: churn risk table ───────────────────────────────────────────────
st.markdown('<div class="section-label">Engagement</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">State-level churn risk — users vs transaction activity</div>', unsafe_allow_html=True)

merged = ft.groupby('state')['count'].sum().reset_index()
merged = merged.merge(
    fu.groupby('state')['registered_users'].sum().reset_index(), on='state'
)
merged['txn_per_user'] = (merged['count'] / merged['registered_users']).round(2)
merged['Engagement'] = merged['txn_per_user'].apply(
    lambda x: '🔴  High churn risk' if x < 5
    else ('🟡  Average engagement' if x < 15 else '🟢  Highly engaged')
)
merged = merged.sort_values('txn_per_user').rename(columns={
    'state': 'State',
    'count': 'Total Transactions',
    'registered_users': 'Registered Users',
    'txn_per_user': 'Txns / User'
})

st.dataframe(
    merged[['State', 'Total Transactions', 'Registered Users', 'Txns / User', 'Engagement']],
    use_container_width=True,
    hide_index=True,
    height=380
)

st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown('<div style="font-size:11px;color:#7b6fa8;text-align:center;padding-bottom:12px;">PhonePe Pulse Analytics · Data sourced from PhonePe Pulse GitHub · Built with Python, Streamlit & Plotly</div>', unsafe_allow_html=True)