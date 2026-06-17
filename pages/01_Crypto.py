import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils.crypto_data import (
    get_bitcoin_price,
    get_ethereum_price,
    get_fear_greed_index,
    get_cmc_hot_tokens,
    get_vix_data,
    get_bitcoin_etf_flows,
    get_contract_open_interest,
    get_crypto_correlation_data,
    get_narratives
)

st.sidebar.title("W3Intelligence")
st.title("💰 Crypto Dashboard")

col1, col2, col3 = st.columns(3)

btc_data = get_bitcoin_price()
if "error" not in btc_data:
    with col1:
        st.metric("Bitcoin Price", f"${btc_data['usd']:,.2f}", f"{btc_data['usd_24h_change']:.2f}%")

eth_data = get_ethereum_price()
if "error" not in eth_data:
    with col2:
        st.metric("Ethereum Price", f"${eth_data['usd']:,.2f}", f"{eth_data['usd_24h_change']:.2f}%")

fg_index = get_fear_greed_index()
if "error" not in fg_index:
    with col3:
        st.metric("Fear & Greed Index", fg_index["value"], fg_index["classification"])

st.markdown("---")

st.subheader("Bitcoin ETF Flows")
etfs = get_bitcoin_etf_flows()
etf_df = [{"ETF": e["name"], "Full Name": e["full_name"]} for e in etfs]
st.table(etf_df)

st.markdown("---")

st.subheader("Futures Open Interest (BTC/ETH)")
oi_data = get_contract_open_interest()
fig_oi = go.Figure(data=[
    go.Bar(name='BTC OI (B $)', x=[o["exchange"] for o in oi_data], y=[o["btc_oi"] for o in oi_data]),
    go.Bar(name='ETH OI (B $)', x=[o["exchange"] for o in oi_data], y=[o["eth_oi"] for o in oi_data])
])
fig_oi.update_layout(barmode='group', template="plotly_dark")
st.plotly_chart(fig_oi, use_container_width=True)

st.markdown("---")

st.subheader("BTC Correlation with Traditional Assets")
corr_data = get_crypto_correlation_data()
fig_corr = px.bar(corr_data, x="asset", y="correlation", color="correlation",
                  color_continuous_scale="RdBu", range_color=[-1, 1])
fig_corr.update_layout(template="plotly_dark")
st.plotly_chart(fig_corr, use_container_width=True)

st.markdown("---")

st.subheader("VIX Index (30-day)")
vix_data = get_vix_data()
if "error" not in vix_data:
    fig_vix = px.line(vix_data, y="VIX", title="VIX Volatility Index")
    fig_vix.update_layout(template="plotly_dark")
    st.plotly_chart(fig_vix, use_container_width=True)

st.markdown("---")

st.subheader("Hot Narratives")
narratives = get_narratives()
for n in narratives:
    trend_icon = "📈" if n["trend"] == "up" else "📉" if n["trend"] == "down" else "➡️"
    st.write(f"**{trend_icon} {n['topic']}** - {n['description']}")

st.markdown("---")

st.subheader("Top Tokens by Market Cap")
hot_tokens = get_cmc_hot_tokens()
if "error" not in hot_tokens:
    token_df = [{
        "Name": t["name"],
        "Symbol": t["symbol"],
        "Price": f"${t['price']:,.2f}",
        "24h Change": f"{t['change_24h']:.2f}%",
        "Market Cap": f"${t['market_cap']/1e9:,.2f}B"
    } for t in hot_tokens]
    st.table(token_df)