import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px

st.set_page_config(page_title="Market Dashboard", layout="wide")

st.title("Small Cap vs Large Cap Market Analysis")

st.write("""
This dashboard explores the performance of small-cap companies compared to large-cap companies
in the U.S. equity market. Small caps are represented by the Russell 2000 index while large caps
are represented by the S&P 500.
""")

# Load data
@st.cache_data
def load_data(start, end):
    tickers = ["^RUT", "^GSPC"]  # Russell 2000 and S&P 500
    data = yf.download(tickers, start=start, end=end)["Adj Close"]
    data = data.reset_index()
    data = data.rename(columns={
        "^RUT": "Russell 2000",
        "^GSPC": "S&P 500"
    })
    return data

# Sidebar filters
st.sidebar.header("Filters")

start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2015-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("today"))

df = load_data(start_date, end_date)

# ---- Visualization 1: Price Trend ----
st.subheader("Index Performance Over Time")

fig = px.line(
    df,
    x="Date",
    y=["Russell 2000", "S&P 500"],
    title="Market Index Performance"
)

st.plotly_chart(fig, use_container_width=True)

# ---- Visualization 2: Daily Returns ----
returns = df.copy()
returns["Russell_Return"] = returns["Russell 2000"].pct_change()
returns["SP500_Return"] = returns["S&P 500"].pct_change()

st.subheader("Daily Returns Distribution")

fig2 = px.histogram(
    returns,
    x="Russell_Return",
    nbins=100,
    title="Distribution of Russell 2000 Daily Returns"
)

st.plotly_chart(fig2, use_container_width=True)

# ---- Visualization 3: Volatility ----
returns["Rolling_Volatility"] = returns["Russell_Return"].rolling(30).std()

st.subheader("Rolling Volatility (30 Day)")

fig3 = px.line(
    returns,
    x="Date",
    y="Rolling_Volatility",
    title="Russell 2000 Volatility"
)

st.plotly_chart(fig3, use_container_width=True)

# ---- Visualization 4: Index Comparison ----
normalized = df.copy()
normalized["Russell 2000"] = normalized["Russell 2000"] / normalized["Russell 2000"].iloc[0]
normalized["S&P 500"] = normalized["S&P 500"] / normalized["S&P 500"].iloc[0]

st.subheader("Normalized Performance Comparison")

fig4 = px.line(
    normalized,
    x="Date",
    y=["Russell 2000", "S&P 500"],
    title="Growth of $1 Investment"
)

st.plotly_chart(fig4, use_container_width=True)

# ---- Data Source Section ----
st.markdown("---")

st.subheader("Data Source")

st.write("""
Data Source: Yahoo Finance  
Accessed via the yfinance API.

Indices included:
- Russell 2000 (small-cap index)
- S&P 500 (large-cap index)

Data Access Date: Current session download.

Future Updates:
The dashboard can be refreshed automatically by re-running the app,
which will pull the latest data available from Yahoo Finance.
""")