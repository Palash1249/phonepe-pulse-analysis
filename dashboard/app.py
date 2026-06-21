import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3

# ── page config ──────────────────────────────────────────────
st.set_page_config(
    page_title="PhonePe Pulse Analytics",
    page_icon="https://upload.wikimedia.org/wikipedia/commons/7/71/PhonePe_Logo.svg",
    layout="wide"
)

# ── custom CSS (PhonePe purple theme) ────────────────────────
st.markdown("""
    <style>
    .main { background-color: #f8f4ff; }
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #5C2D91;
        margin: 5px;
    }
    h1, h2, h3 { color: #5C2D91; }
    </style>
""", unsafe_allow_html=True)

# ── load data ─────────────────────────────────────────────────
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

# ── sidebar filters ───────────────────────────────────────────
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/7/71/PhonePe_Logo.svg", width=200)
st.sidebar.title("Filters")

years = sorted(df_t['year'].unique())
selected_years = st.sidebar.multiselect("Select Years", years, default=years)

states = sorted(df_t['state'].unique())
selected_states = st.sidebar.multiselect("Select States", states, default=states)

txn_types = df_t['transaction_type'].unique()
selected_type = st.sidebar.multiselect("Transaction Type", txn_types, default=txn_types)

# apply filters
filtered_t = df_t[
    (df_t['year'].isin(selected_years)) &
    (df_t['state'].isin(selected_states)) &
    (df_t['transaction_type'].isin(selected_type))
]
filtered_u = df_u[
    (df_u['year'].isin(selected_years)) &
    (df_u['state'].isin(selected_states))
]

# ── header ────────────────────────────────────────────────────
st.title("📱 PhonePe Pulse Transaction Analytics")
st.markdown("**Analyzing India's UPI payment trends (2018–2024)**")
st.markdown("---")

# ── KPI cards ─────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_txn = filtered_t['count'].sum()
    st.metric("Total Transactions", f"{total_txn/1e9:.2f}B")

with col2:
    total_amt = filtered_t['amount_cr'].sum()
    st.metric("Total Value", f"₹{total_amt:,.0f} Cr")

with col3:
    total_users = filtered_u['registered_users'].sum()
    st.metric("Registered Users", f"{total_users/1e7:.1f}Cr")

with col4:
    total_states = filtered_t['state'].nunique()
    st.metric("States Covered", total_states)

st.markdown("---")

# ── row 1: national trend + transaction type ──────────────────
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("National UPI Growth Over Time")
    national = filtered_t.groupby('period').agg(
        total_count=('count', 'sum'),
        total_amount=('amount_cr', 'sum')
    ).reset_index()
    fig = px.line(national, x='period', y='total_amount',
                  markers=True, color_discrete_sequence=['#5C2D91'])
    fig.update_layout(
        xaxis_tickangle=45,
        xaxis_title="Quarter",
        yaxis_title="Amount (₹ Crores)",
        plot_bgcolor='white'
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Transaction Type Split")
    type_data = filtered_t.groupby('transaction_type')['count'].sum().reset_index()
    fig2 = px.pie(type_data, names='transaction_type', values='count',
                  color_discrete_sequence=['#5C2D91','#00B9F1','#7B3FB5','#34AFDB','#A67EC8'])
    fig2.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig2, use_container_width=True)

# ── row 2: top states bar + map ───────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("Top 10 States by Transaction Value")
    top_states = (filtered_t.groupby('state')['amount_cr']
                  .sum().sort_values(ascending=False)
                  .head(10).reset_index())
    fig3 = px.bar(top_states, x='amount_cr', y='state',
                  orientation='h',
                  color='amount_cr',
                  color_continuous_scale=['#D4B8E0', '#5C2D91'])
    fig3.update_layout(yaxis={'categoryorder': 'total ascending'},
                       plot_bgcolor='white',
                       xaxis_title="Amount (₹ Crores)",
                       yaxis_title="")
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    st.subheader("YoY Growth by State (Latest Year)")
    state_year = filtered_t.groupby(['state','year'])['amount_cr'].sum().reset_index()
    state_year['prev'] = state_year.groupby('state')['amount_cr'].shift(1)
    state_year['yoy'] = (state_year['amount_cr'] - state_year['prev']) / state_year['prev'] * 100
    latest = state_year[state_year['year'] == state_year['year'].max()].dropna()
    top_g = latest.sort_values('yoy', ascending=False).head(10)
    fig4 = px.bar(top_g, x='yoy', y='state',
                  orientation='h',
                  color='yoy',
                  color_continuous_scale=['#00B9F1', '#5C2D91'])
    fig4.update_layout(yaxis={'categoryorder': 'total ascending'},
                       plot_bgcolor='white',
                       xaxis_title="YoY Growth (%)",
                       yaxis_title="")
    st.plotly_chart(fig4, use_container_width=True)

# ── row 3: churn risk table ───────────────────────────────────
st.markdown("---")
st.subheader("State Engagement Analysis — Churn Risk Detector")

merged = filtered_t.groupby('state')['count'].sum().reset_index()
merged = merged.merge(
    filtered_u.groupby('state')['registered_users'].sum().reset_index(),
    on='state'
)
merged['txn_per_user'] = (merged['count'] / merged['registered_users']).round(2)
merged['risk'] = merged['txn_per_user'].apply(
    lambda x: '🔴 High churn risk' if x < 5
    else ('🟡 Average' if x < 15 else '🟢 Highly engaged')
)
merged = merged.sort_values('txn_per_user')
st.dataframe(merged.rename(columns={
    'state': 'State',
    'count': 'Total Transactions',
    'registered_users': 'Registered Users',
    'txn_per_user': 'Transactions per User',
    'risk': 'Engagement Level'
}), use_container_width=True, hide_index=True)

# ── footer ────────────────────────────────────────────────────
st.markdown("---")
st.markdown("Built with Python · Streamlit · Plotly · PhonePe Pulse Data (2018-2024)")