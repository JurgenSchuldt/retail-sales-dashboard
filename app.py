import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from src.clean_data import load_and_clean

# ── Configuración de página ──────────────────────────────────────
st.set_page_config(
    page_title="Retail Sales Analytics",
    page_icon="📊",
    layout="wide"
)

# ── Estilos Corporate Blue ───────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #f0f4f8; }
    .block-container { padding-top: 1.5rem; }
    .dashboard-header {
        background-color: #1e3a5f;
        padding: 16px 24px;
        border-radius: 8px;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .dashboard-title { color: white; font-size: 20px; font-weight: 600; margin: 0; }
    .dashboard-sub { color: #8ab4d4; font-size: 13px; margin: 0; }
    .kpi-card {
        background: white;
        border-left: 4px solid #1e3a5f;
        border-radius: 6px;
        padding: 14px 18px;
    }
    .kpi-value { font-size: 24px; font-weight: 600; color: #1e3a5f; margin: 0; }
    .kpi-label { font-size: 12px; color: #888; margin: 0; }
    .kpi-delta { font-size: 12px; color: #1D9E75; margin: 0; }
    .section-title {
        font-size: 13px; font-weight: 600;
        color: #1e3a5f; margin-bottom: 8px;
        text-transform: uppercase; letter-spacing: 0.05em;
    }
</style>
""", unsafe_allow_html=True)

# ── Carga de datos ───────────────────────────────────────────────
@st.cache_data
def get_data():
    return load_and_clean("data/online_retail_II.csv")

df = get_data()

# ── Header ───────────────────────────────────────────────────────
st.markdown("""
<div class="dashboard-header">
    <div>
        <p class="dashboard-title">Retail Sales Analytics</p>
        <p class="dashboard-sub">Online Retail — UK & International Markets</p>
    </div>
    <div style="text-align:right">
        <p class="dashboard-sub">Periodo: Dec 2009 – Dec 2011</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Sidebar filtros ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("### Filtros")
    
    years = sorted(df['Year'].unique())
    selected_years = st.multiselect("Año", years, default=years)
    
    countries = sorted(df['Country'].unique())
    selected_countries = st.multiselect(
        "País", countries,
        default=["United Kingdom", "Germany", "France", "Netherlands", "EIRE"]
    )

# ── Filtrado ─────────────────────────────────────────────────────
mask = (
    df['Year'].isin(selected_years) &
    df['Country'].isin(selected_countries)
)
dff = df[mask]

# ── KPIs ─────────────────────────────────────────────────────────
total_revenue = dff['Revenue'].sum()
total_customers = dff['Customer ID'].nunique()
total_orders = dff['Invoice'].nunique()
avg_order_value = total_revenue / total_orders if total_orders > 0 else 0

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <p class="kpi-label">Ingresos totales</p>
        <p class="kpi-value">£{total_revenue:,.0f}</p>
    </div>""", unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card">
        <p class="kpi-label">Clientes únicos</p>
        <p class="kpi-value">{total_customers:,}</p>
    </div>""", unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card">
        <p class="kpi-label">Pedidos totales</p>
        <p class="kpi-value">{total_orders:,}</p>
    </div>""", unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="kpi-card">
        <p class="kpi-label">Ticket medio</p>
        <p class="kpi-value">£{avg_order_value:,.2f}</p>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Gráfico 1: Ingresos por mes ──────────────────────────────────
st.markdown('<p class="section-title">Evolución de ingresos</p>', unsafe_allow_html=True)

monthly = dff.groupby('YearMonth')['Revenue'].sum().reset_index()
monthly = monthly.sort_values('YearMonth')

fig1 = px.bar(
    monthly, x='YearMonth', y='Revenue',
    color_discrete_sequence=['#1e3a5f']
)
fig1.update_layout(
    plot_bgcolor='white', paper_bgcolor='white',
    margin=dict(t=10, b=10, l=10, r=10),
    xaxis_title="", yaxis_title="Ingresos (£)",
    xaxis_tickangle=-45,
    height=280
)
st.plotly_chart(fig1, use_container_width=True)

# ── Gráfico 2: Top productos + Top países ────────────────────────
col_left, col_right = st.columns([3, 2])

with col_left:
    st.markdown('<p class="section-title">Top 10 productos por ingresos</p>', unsafe_allow_html=True)
    top_products = (
        dff.groupby('Description')['Revenue']
        .sum().reset_index()
        .sort_values('Revenue', ascending=True)
        .tail(10)
    )
    fig2 = px.bar(
        top_products, x='Revenue', y='Description',
        orientation='h', color_discrete_sequence=['#378ADD']
    )
    fig2.update_layout(
        plot_bgcolor='white', paper_bgcolor='white',
        margin=dict(t=10, b=10, l=10, r=10),
        xaxis_title="Ingresos (£)", yaxis_title="",
        height=320
    )
    st.plotly_chart(fig2, use_container_width=True)

with col_right:
    st.markdown('<p class="section-title">Ingresos por país</p>', unsafe_allow_html=True)
    top_countries = (
        dff.groupby('Country')['Revenue']
        .sum().reset_index()
        .sort_values('Revenue', ascending=False)
        .head(10)
    )
    fig3 = px.bar(
        top_countries, x='Revenue', y='Country',
        orientation='h', color_discrete_sequence=['#1e3a5f']
    )
    fig3.update_layout(
        plot_bgcolor='white', paper_bgcolor='white',
        margin=dict(t=10, b=10, l=10, r=10),
        xaxis_title="Ingresos (£)", yaxis_title="",
        height=320
    )
    st.plotly_chart(fig3, use_container_width=True)

# ── Gráfico 3: Análisis RFM ──────────────────────────────────────
st.markdown('<p class="section-title">Segmentación de clientes (RFM)</p>', unsafe_allow_html=True)

snapshot_date = dff['InvoiceDate'].max()
rfm = dff.groupby('Customer ID').agg(
    Recency=('InvoiceDate', lambda x: (snapshot_date - x.max()).days),
    Frequency=('Invoice', 'nunique'),
    Monetary=('Revenue', 'sum')
).reset_index()

rfm['R_score'] = pd.qcut(rfm['Recency'], 4, labels=[4, 3, 2, 1])
rfm['F_score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 4, labels=[1, 2, 3, 4])
rfm['M_score'] = pd.qcut(rfm['Monetary'].rank(method='first'), 4, labels=[1, 2, 3, 4])
rfm['RFM_score'] = rfm['R_score'].astype(str) + rfm['F_score'].astype(str) + rfm['M_score'].astype(str)

def segment(row):
    r, f, m = int(row['R_score']), int(row['F_score']), int(row['M_score'])
    if r >= 3 and f >= 3 and m >= 3:
        return 'Champions'
    elif r >= 3 and f >= 2:
        return 'Loyal'
    elif r >= 3:
        return 'Recent'
    elif f >= 3:
        return 'At Risk'
    else:
        return 'Lost'

rfm['Segment'] = rfm.apply(segment, axis=1)

col_rfm1, col_rfm2 = st.columns(2)

with col_rfm1:
    seg_counts = rfm['Segment'].value_counts().reset_index()
    seg_counts.columns = ['Segment', 'Customers']
    fig4 = px.pie(
        seg_counts, values='Customers', names='Segment',
        color_discrete_sequence=['#1e3a5f', '#378ADD', '#5DCAA5', '#8ab4d4', '#d0e4f5']
    )
    fig4.update_layout(
        plot_bgcolor='white', paper_bgcolor='white',
        margin=dict(t=10, b=10, l=10, r=10),
        height=280
    )
    st.plotly_chart(fig4, use_container_width=True)

with col_rfm2:
    fig5 = px.scatter(
        rfm, x='Recency', y='Monetary',
        color='Segment', size='Frequency',
        color_discrete_sequence=['#1e3a5f', '#378ADD', '#5DCAA5', '#8ab4d4', '#d0e4f5'],
        opacity=0.7
    )
    fig5.update_layout(
        plot_bgcolor='white', paper_bgcolor='white',
        margin=dict(t=10, b=10, l=10, r=10),
        xaxis_title="Recencia (días)", yaxis_title="Ingresos (£)",
        height=280
    )
    st.plotly_chart(fig5, use_container_width=True)