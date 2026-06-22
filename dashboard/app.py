import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(
    page_title="PhonePe Pulse · India UPI Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background-color: #0f0c1a; }
section[data-testid="stSidebar"] { background-color: #160d2e; border-right: 1px solid #2a1f4e; min-width: 260px !important; max-width: 260px !important; transform: translateX(0) !important; }
[data-testid="collapsedControl"], button[kind="header"], .st-emotion-cache-h5rgaw, .st-emotion-cache-1dp5vir, .eyeqlp53, .e1fqkh3o0 { display: none !important; visibility: hidden !important; opacity: 0 !important; pointer-events: none !important; width: 0 !important; height: 0 !important; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2.5rem; max-width: 1400px; }
.sidebar-brand { font-size: 20px; font-weight: 700; color: #a78bfa; letter-spacing: -0.5px; margin-bottom: 4px; }
.sidebar-sub { font-size: 11px; color: #6b5fa0; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 24px; }
.nav-item { padding: 10px 14px; border-radius: 8px; margin-bottom: 4px; cursor: pointer; font-size: 13px; color: #7b6fa8; font-weight: 500; }
.nav-item.active { background: #2d1f5e; color: #c4b5fd; }
.page-eyebrow { font-size: 11px; font-weight: 600; color: #7c3aed; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 6px; }
.page-title { font-size: 36px; font-weight: 700; color: #f5f0ff; letter-spacing: -1px; line-height: 1.15; margin-bottom: 6px; }
.page-subtitle { font-size: 14px; color: #7b6fa8; margin-bottom: 32px; }
.kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 36px; }
.kpi-card { background: #1a1133; border: 1px solid #2a1f4e; border-radius: 12px; padding: 22px 24px; position: relative; overflow: hidden; }
.kpi-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; background: linear-gradient(90deg, #7c3aed, #a78bfa); border-radius: 12px 12px 0 0; }
.kpi-label { font-size: 11px; font-weight: 600; color: #6b5fa0; text-transform: uppercase; letter-spacing: 1.2px; margin-bottom: 10px; }
.kpi-value { font-size: 28px; font-weight: 700; color: #f5f0ff; letter-spacing: -0.5px; line-height: 1; }
.kpi-delta { font-size: 12px; color: #4ade80; margin-top: 6px; font-weight: 500; }
.section-label { font-size: 11px; font-weight: 600; color: #7c3aed; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 4px; }
.section-title { font-size: 18px; font-weight: 600; color: #e9e0ff; margin-bottom: 16px; letter-spacing: -0.3px; }
.insight-box { background: #1a1133; border: 1px solid #2a1f4e; border-left: 3px solid #7c3aed; border-radius: 8px; padding: 16px 20px; margin-bottom: 28px; font-size: 13px; color: #a99dc8; line-height: 1.6; }
.insight-box strong { color: #c4b5fd; }
.forecast-card { background: #1a1133; border: 1px solid #2a1f4e; border-radius: 12px; padding: 20px 24px; margin-bottom: 16px; }
.forecast-qtr { font-size: 11px; font-weight: 600; color: #6b5fa0; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px; }
.forecast-val { font-size: 22px; font-weight: 700; color: #2dd4bf; }
.forecast-range { font-size: 11px; color: #4b5563; margin-top: 4px; }
.divider { border: none; border-top: 1px solid #2a1f4e; margin: 32px 0; }
.stMultiSelect [data-baseweb="tag"] { background-color: #2d1f5e !important; color: #c4b5fd !important; }
</style>
""", unsafe_allow_html=True)

st.components.v1.html("""
<script>
function hideSidebarToggle() {
    const selectors = ['[data-testid="collapsedControl"]','button[aria-label="Close sidebar"]','button[aria-label="Open sidebar"]','button[aria-label="Collapse sidebar"]','button[kind="header"]'];
    selectors.forEach(sel => { document.querySelectorAll(sel).forEach(el => { el.style.setProperty('display','none','important'); }); });
}
hideSidebarToggle();
const interval = setInterval(hideSidebarToggle, 300);
setTimeout(() => clearInterval(interval), 5000);
</script>
""", height=0)

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

@st.cache_data
def load_forecast():
    try:
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        fc   = pd.read_csv(os.path.join(base, "data", "forecast_combined.csv"), parse_dates=['ds'])
        fc_m = pd.read_csv(os.path.join(base, "data", "manipur_forecast.csv"),  parse_dates=['ds'])
        return fc, fc_m
    except Exception as e:
        return None, None

df_t, df_u = load_data()
fc, fc_m   = load_forecast()

PURPLE      = "#7c3aed"
PURPLE_LITE = "#a78bfa"
TEAL        = "#2dd4bf"
CARD_BG     = "#1a1133"
GRID_COL    = "#1e1535"
TEXT_SEC    = "#7b6fa8"

def chart_layout(fig, height=340):
    fig.update_layout(
        paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG,
        font=dict(family="Inter", color=TEXT_SEC, size=11),
        height=height, margin=dict(l=12, r=12, t=20, b=12),
        xaxis=dict(gridcolor=GRID_COL, linecolor=GRID_COL, tickfont=dict(size=10)),
        yaxis=dict(gridcolor=GRID_COL, linecolor=GRID_COL, tickfont=dict(size=10)),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=10, color=TEXT_SEC)),
        coloraxis_showscale=False,
    )
    return fig

# ── sidebar ───────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-brand">PhonePe Pulse</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-sub">India UPI Analytics · 2018–2025</div>', unsafe_allow_html=True)

    page = st.radio("Navigation", ["📊  Overview", "🔮  Forecast", "📋  SQL Insights"], label_visibility="collapsed")

    st.markdown("---")

    if page == "📊  Overview":
        years         = sorted(df_t['year'].unique())
        selected_years  = st.multiselect("Years", years, default=years)
        states          = sorted(df_t['state'].unique())
        selected_states = st.multiselect("States", states, default=states)
        txn_types       = list(df_t['transaction_type'].unique())
        selected_type   = st.multiselect("Transaction type", txn_types, default=txn_types)
    else:
        selected_years  = sorted(df_t['year'].unique())
        selected_states = sorted(df_t['state'].unique())
        selected_type   = list(df_t['transaction_type'].unique())

    st.markdown("---")
    st.markdown(f'<div style="font-size:11px;color:{TEXT_SEC};">Data · PhonePe Pulse GitHub<br>Built with Python · Streamlit · Plotly · Prophet</div>', unsafe_allow_html=True)

ft = df_t[df_t['year'].isin(selected_years) & df_t['state'].isin(selected_states) & df_t['transaction_type'].isin(selected_type)]
fu = df_u[df_u['year'].isin(selected_years) & df_u['state'].isin(selected_states)]

# ══════════════════════════════════════════════════════════════════════════
# PAGE 1 — OVERVIEW
# ══════════════════════════════════════════════════════════════════════════
if page == "📊  Overview":
    st.markdown('<div class="page-eyebrow">India · Digital Payments Intelligence</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-title">PhonePe Pulse Analytics</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Tracking UPI adoption, transaction growth, and engagement across 36 states — 2018 to 2024</div>', unsafe_allow_html=True)

    total_txn   = ft['count'].sum()
    total_amt   = ft['amount_cr'].sum()
    total_users = fu['registered_users'].sum()
    total_st    = ft['state'].nunique()

    st.markdown(f"""
    <div class="kpi-grid">
      <div class="kpi-card"><div class="kpi-label">Total transactions</div><div class="kpi-value">{total_txn/1e9:.1f}B</div><div class="kpi-delta">↑ Across all quarters</div></div>
      <div class="kpi-card"><div class="kpi-label">Transaction value</div><div class="kpi-value">₹{total_amt/1e5:.1f}L Cr</div><div class="kpi-delta">↑ Cumulative 2018–2024</div></div>
      <div class="kpi-card"><div class="kpi-label">Registered users</div><div class="kpi-value">{total_users/1e7:.1f} Cr</div><div class="kpi-delta">↑ Across selected states</div></div>
      <div class="kpi-card"><div class="kpi-label">States covered</div><div class="kpi-value">{total_st}</div><div class="kpi-delta">Including UTs</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="insight-box">
      <strong>Key insight:</strong> UPI transaction volume grew over <strong>40× between 2018 and 2024</strong>.
      Manipur leads YoY growth among all states — a signal of rapid digital payment adoption in Northeast India.
      States with high registered users but low transactions per user represent the biggest re-engagement opportunity.
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown('<div class="section-label">Growth</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">National UPI transaction value over time</div>', unsafe_allow_html=True)
        national = ft.groupby('period').agg(total_amount=('amount_cr','sum')).reset_index()
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=national['period'], y=national['total_amount'], mode='lines+markers',
            line=dict(color=PURPLE, width=2.5), marker=dict(size=5, color=PURPLE_LITE),
            fill='tozeroy', fillcolor='rgba(124,58,237,0.08)', name='Amount (₹ Cr)'))
        fig.update_xaxes(tickangle=45, tickfont=dict(size=9))
        fig.update_yaxes(title_text="₹ Crores", title_font=dict(size=10))
        chart_layout(fig, 320); st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="section-label">Composition</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Transaction type split</div>', unsafe_allow_html=True)
        type_data = ft.groupby('transaction_type')['count'].sum().reset_index()
        fig2 = px.pie(type_data, names='transaction_type', values='count', hole=0.55,
            color_discrete_sequence=[PURPLE, TEAL, "#a78bfa", "#34d399", "#f472b6"])
        fig2.update_traces(textposition='outside', textinfo='percent+label', textfont_size=10,
            marker=dict(line=dict(color=CARD_BG, width=2)))
        chart_layout(fig2, 320); st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-label">Market size</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Top 10 states by transaction value</div>', unsafe_allow_html=True)
        top_states = ft.groupby('state')['amount_cr'].sum().sort_values(ascending=True).tail(10).reset_index()
        fig3 = px.bar(top_states, x='amount_cr', y='state', orientation='h', color='amount_cr',
            color_continuous_scale=[[0,"#2d1f5e"],[1,PURPLE_LITE]])
        fig3.update_traces(marker_line_width=0); fig3.update_xaxes(title_text="₹ Crores"); fig3.update_yaxes(title_text="")
        chart_layout(fig3, 340); st.plotly_chart(fig3, use_container_width=True)

    with col2:
        st.markdown('<div class="section-label">Momentum</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Fastest growing states (latest year YoY)</div>', unsafe_allow_html=True)
        sy = ft.groupby(['state','year'])['amount_cr'].sum().reset_index()
        sy['prev'] = sy.groupby('state')['amount_cr'].shift(1)
        sy['yoy']  = (sy['amount_cr'] - sy['prev']) / sy['prev'] * 100
        top_g = sy[sy['year']==sy['year'].max()].dropna().sort_values('yoy', ascending=True).tail(10)
        fig4 = px.bar(top_g, x='yoy', y='state', orientation='h', color='yoy',
            color_continuous_scale=[[0,"#0f766e"],[1,TEAL]])
        fig4.update_traces(marker_line_width=0); fig4.update_xaxes(title_text="YoY Growth (%)"); fig4.update_yaxes(title_text="")
        chart_layout(fig4, 340); st.plotly_chart(fig4, use_container_width=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Seasonality</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Average transaction value by quarter — festive spike detector</div>', unsafe_allow_html=True)
    qtr = ft.groupby(['year','quarter'])['amount_cr'].sum().reset_index()
    qtr_avg = qtr.groupby('quarter')['amount_cr'].mean().reset_index()
    qtr_avg['quarter_label'] = qtr_avg['quarter'].map({1:'Q1 · Jan–Mar',2:'Q2 · Apr–Jun',3:'Q3 · Jul–Sep',4:'Q4 · Oct–Dec (Festive)'})
    fig5 = px.bar(qtr_avg, x='quarter_label', y='amount_cr', color='amount_cr',
        color_continuous_scale=[[0,"#2d1f5e"],[1,PURPLE_LITE]])
    fig5.update_traces(marker_line_width=0); fig5.update_xaxes(title_text=""); fig5.update_yaxes(title_text="Avg ₹ Crores")
    chart_layout(fig5, 280); st.plotly_chart(fig5, use_container_width=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Engagement</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">State-level churn risk — users vs transaction activity</div>', unsafe_allow_html=True)
    merged = ft.groupby('state')['count'].sum().reset_index()
    merged = merged.merge(fu.groupby('state')['registered_users'].sum().reset_index(), on='state')
    merged['txn_per_user'] = (merged['count'] / merged['registered_users']).round(2)
    merged['Engagement'] = merged['txn_per_user'].apply(
        lambda x: '🔴  High churn risk' if x < 5 else ('🟡  Average engagement' if x < 15 else '🟢  Highly engaged'))
    merged = merged.sort_values('txn_per_user').rename(columns={'state':'State','count':'Total Transactions','registered_users':'Registered Users','txn_per_user':'Txns / User'})
    st.dataframe(merged[['State','Total Transactions','Registered Users','Txns / User','Engagement']], use_container_width=True, hide_index=True, height=380)

# ══════════════════════════════════════════════════════════════════════════
# PAGE 2 — FORECAST
# ══════════════════════════════════════════════════════════════════════════
elif page == "🔮  Forecast":
    st.markdown('<div class="page-eyebrow">Machine Learning · Prophet Model</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-title">UPI Transaction Forecast</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Facebook Prophet time-series model trained on 2018–2024 quarterly data · Forecasting next 4 quarters</div>', unsafe_allow_html=True)

    if fc is None:
        st.error("Forecast data not found. Please run notebooks/04_forecasting.ipynb first to generate the forecast CSVs.")
    else:
        # ── forecast KPI cards ────────────────────────────────────────────
        future_rows = fc[fc['actual'].isna()].tail(4)
        last_actual = fc[fc['actual'].notna()]['actual'].iloc[-1]

        cols = st.columns(4)
        for i, (_, row) in enumerate(future_rows.iterrows()):
            qtr_label = row['ds'].strftime('%Y Q') + str((row['ds'].month // 3) + 1)
            growth    = ((row['yhat'] - last_actual) / last_actual * 100)
            with cols[i]:
                st.markdown(f"""
                <div class="kpi-card">
                  <div class="kpi-label">{qtr_label}</div>
                  <div class="kpi-value" style="color:#2dd4bf;">₹{row['yhat']/1e3:.0f}K Cr</div>
                  <div class="kpi-delta">↑ {growth:.0f}% vs last actual</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div class="insight-box">
          <strong>Model:</strong> Facebook Prophet with multiplicative seasonality — chosen because UPI growth compounds over time.
          The model captures the festive Q4 spike pattern automatically from historical data.
          <strong>Manipur</strong> specifically shows continued acceleration in its state-level forecast, supporting the merchant acquisition recommendation.
        </div>
        """, unsafe_allow_html=True)

        # ── national forecast chart ───────────────────────────────────────
        st.markdown('<div class="section-label">National forecast</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">India UPI transaction value — actual vs forecast</div>', unsafe_allow_html=True)

        actual_df   = fc[fc['actual'].notna()]
        forecast_df = fc.copy()

        fig_fc = go.Figure()

        # confidence band
        fig_fc.add_trace(go.Scatter(
            x=pd.concat([forecast_df['ds'], forecast_df['ds'][::-1]]),
            y=pd.concat([forecast_df['yhat_upper'], forecast_df['yhat_lower'][::-1]]),
            fill='toself', fillcolor='rgba(45,212,191,0.06)',
            line=dict(color='rgba(0,0,0,0)'), name='Confidence interval', showlegend=True
        ))

        # forecast line
        fig_fc.add_trace(go.Scatter(
            x=forecast_df['ds'], y=forecast_df['yhat'],
            mode='lines', name='Forecast',
            line=dict(color=TEAL, width=2, dash='dash')
        ))

        # actual line
        fig_fc.add_trace(go.Scatter(
            x=actual_df['ds'], y=actual_df['actual'],
            mode='lines+markers', name='Actual',
            line=dict(color=PURPLE, width=2.5),
            marker=dict(size=5, color=PURPLE_LITE)
        ))

        # split line
        fig_fc.add_vline(
            x=actual_df['ds'].max(),
            line_dash="dot", line_color="#4b5563",
            annotation_text="Forecast →",
            annotation_font_color="#6b5fa0",
            annotation_position="top right"
        )

        fig_fc.update_xaxes(title_text="Quarter")
        fig_fc.update_yaxes(title_text="₹ Crores")
        chart_layout(fig_fc, 420)
        st.plotly_chart(fig_fc, use_container_width=True)

        # ── Manipur forecast ──────────────────────────────────────────────
        if fc_m is not None:
            st.markdown('<hr class="divider">', unsafe_allow_html=True)
            st.markdown('<div class="section-label">State spotlight · Manipur</div>', unsafe_allow_html=True)
            st.markdown('<div class="section-title">Manipur — fastest growing state forecast</div>', unsafe_allow_html=True)

            manip_actual = df_t[df_t['state']=='Manipur'].copy()
            def q2d(row):
                m = {1:'01',2:'04',3:'07',4:'10'}[row['quarter']]
                return pd.to_datetime(f"{row['year']}-{m}-01")
            manip_actual['ds'] = manip_actual.apply(q2d, axis=1)
            manip_actual = manip_actual.groupby('ds')['amount_cr'].sum().reset_index()

            fig_m = go.Figure()
            fig_m.add_trace(go.Scatter(
                x=pd.concat([fc_m['ds'], fc_m['ds'][::-1]]),
                y=pd.concat([fc_m['yhat_upper'], fc_m['yhat_lower'][::-1]]),
                fill='toself', fillcolor='rgba(124,58,237,0.06)',
                line=dict(color='rgba(0,0,0,0)'), name='Confidence interval'
            ))
            fig_m.add_trace(go.Scatter(
                x=fc_m['ds'], y=fc_m['yhat'], mode='lines', name='Forecast',
                line=dict(color=TEAL, width=2, dash='dash')
            ))
            fig_m.add_trace(go.Scatter(
                x=manip_actual['ds'], y=manip_actual['amount_cr'],
                mode='lines+markers', name='Actual',
                line=dict(color=PURPLE, width=2.5),
                marker=dict(size=5, color=PURPLE_LITE)
            ))
            fig_m.add_vline(
                x=manip_actual['ds'].max(), line_dash="dot", line_color="#4b5563",
                annotation_text="Forecast →", annotation_font_color="#6b5fa0",
                annotation_position="top right"
            )
            fig_m.update_xaxes(title_text="Quarter")
            fig_m.update_yaxes(title_text="₹ Crores")
            chart_layout(fig_m, 360)
            st.plotly_chart(fig_m, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════
# PAGE 3 — SQL INSIGHTS
# ══════════════════════════════════════════════════════════════════════════
elif page == "📋  SQL Insights":
    st.markdown('<div class="page-eyebrow">SQL Analysis · SQLite</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-title">Business SQL Queries</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">7 business-focused queries written in SQLite using window functions, CTEs, and JOINs</div>', unsafe_allow_html=True)

    import sqlite3
    try:
        conn = sqlite3.connect("../data/phonepe.db")

        queries = {
            "Top 10 states by total transaction value": """
                SELECT state, ROUND(SUM(amount_cr),2) AS total_amount_cr,
                       SUM(count) AS total_transactions,
                       ROUND(SUM(amount_cr)*100.0/(SELECT SUM(amount_cr) FROM transactions),2) AS pct_of_india
                FROM transactions GROUP BY state ORDER BY total_amount_cr DESC LIMIT 10
            """,
            "Year-over-year national growth (LAG window function)": """
                SELECT year, SUM(count) AS total_transactions,
                       ROUND(SUM(amount_cr),0) AS total_amount_cr,
                       ROUND((SUM(amount_cr)-LAG(SUM(amount_cr)) OVER (ORDER BY year))*100.0
                             /LAG(SUM(amount_cr)) OVER (ORDER BY year),2) AS yoy_growth_pct
                FROM transactions GROUP BY year ORDER BY year
            """,
            "Dominant transaction type per state (RANK + PARTITION BY)": """
                WITH ranked AS (
                    SELECT state, transaction_type, SUM(count) AS total_count,
                           RANK() OVER (PARTITION BY state ORDER BY SUM(count) DESC) AS rnk
                    FROM transactions GROUP BY state, transaction_type
                )
                SELECT state, transaction_type, total_count FROM ranked WHERE rnk=1 ORDER BY total_count DESC
            """,
            "State churn risk — transactions per user (JOIN)": """
                WITH state_totals AS (
                    SELECT t.state, SUM(t.count) AS total_transactions,
                           SUM(u.registered_users) AS total_users,
                           ROUND(CAST(SUM(t.count) AS FLOAT)/SUM(u.registered_users),2) AS txn_per_user
                    FROM transactions t
                    JOIN users u ON t.state=u.state AND t.year=u.year AND t.quarter=u.quarter
                    GROUP BY t.state
                )
                SELECT state, total_transactions, total_users, txn_per_user,
                       CASE WHEN txn_per_user < 5 THEN 'High churn risk'
                            WHEN txn_per_user BETWEEN 5 AND 15 THEN 'Average'
                            ELSE 'Highly engaged' END AS engagement
                FROM state_totals ORDER BY txn_per_user ASC
            """
        }

        for title, sql in queries.items():
            st.markdown(f'<div class="section-label">Query</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)
            with st.expander("View SQL"):
                st.code(sql.strip(), language="sql")
            result = pd.read_sql(sql, conn)
            st.dataframe(result, use_container_width=True, hide_index=True)
            st.markdown('<hr class="divider">', unsafe_allow_html=True)

        conn.close()
    except Exception as e:
        st.error(f"Database error: {e}. Make sure you've run notebook 03_sql_analysis.ipynb first.")

st.markdown(f'<div style="font-size:11px;color:{TEXT_SEC};text-align:center;padding:12px 0;">PhonePe Pulse Analytics · Built with Python · Streamlit · Plotly · Prophet · SQLite</div>', unsafe_allow_html=True)