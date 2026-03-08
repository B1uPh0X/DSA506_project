import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px

st.set_page_config(page_title="Market QUEST Dashboard", layout="wide")

# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("Small-Cap vs Large-Cap Market Analysis")

st.write("""
This interactive dashboard explores how small-cap companies compare to large-cap companies
in the U.S. stock market. Small caps are represented by the Russell 2000 index, while
large caps are represented by the S&P 500.
""")

# --------------------------------------------------
# 1 — QUESTION
# --------------------------------------------------

st.header("Framing the Question")

st.write("""
Investors often debate whether smaller companies grow faster than larger established firms.
However, higher potential growth may also come with higher volatility and risk.

Key analytical questions explored in this dashboard:

1. How have small-cap and large-cap stocks performed over time?
2. Are small-cap stocks more volatile than large-cap stocks?
3. How do daily return distributions differ between the indices?
4. If an investor started with $1, which index produced higher growth?
""")

# --------------------------------------------------
# SIDEBAR CONTROLS
# --------------------------------------------------

st.sidebar.header("Dashboard Controls")

start_date = st.sidebar.date_input(
    "Start Date",
    pd.to_datetime("2015-01-01")
)

end_date = st.sidebar.date_input(
    "End Date",
    pd.to_datetime("today")
)

vol_window = st.sidebar.slider(
    "Volatility Window (days)",
    min_value=10,
    max_value=90,
    value=30
)

index_choice = st.sidebar.selectbox(
    "Index for Distribution Analysis",
    ["Russell 2000", "S&P 500"]
)

# --------------------------------------------------
# DATA LOADING
# --------------------------------------------------

@st.cache_data
def load_data(start, end):
    tickers = ["^RUT", "^GSPC"]
    data = yf.download(tickers, start=start, end=end, group_by="ticker")

    df = pd.DataFrame({
        "Date": data.index,
        "Russell 2000": data["^RUT"]["Close"],
        "S&P 500": data["^GSPC"]["Close"]
    }).reset_index(drop=True)

    return df

df = load_data(start_date, end_date)

# --------------------------------------------------
# 2 — UNDERSTAND DATA
# --------------------------------------------------

st.header("Understanding the Data")

st.write("""
The dataset contains daily closing prices for two major U.S. stock market indices:

• Russell 2000 — represents small-capitalization companies  
• S&P 500 — represents large-capitalization companies

From these price series we compute:

• Daily returns  
• Rolling volatility  
• Normalized growth of an investment
""")

# --------------------------------------------------
# CALCULATE RETURNS
# --------------------------------------------------

returns = df.copy()

returns["Russell_Return"] = returns["Russell 2000"].pct_change()
returns["SP500_Return"] = returns["S&P 500"].pct_change()

returns["Russell_Volatility"] = returns["Russell_Return"].rolling(vol_window).std()
returns["SP500_Volatility"] = returns["SP500_Return"].rolling(vol_window).std()

# --------------------------------------------------
# 3 — EXPLORE PATTERNS
# --------------------------------------------------

st.header("Exploring Patterns")

# ---- Visualization 1: Price Trend ----

st.subheader("Market Index Performance Over Time")

fig1 = px.line(
    df,
    x="Date",
    y=["Russell 2000", "S&P 500"],
    title="Index Performance"
)

st.plotly_chart(fig1, use_container_width=True)

# ---- Visualization 2: Return Distribution ----

st.subheader("Daily Return Distribution")

if index_choice == "Russell 2000":
    dist_col = "Russell_Return"
else:
    dist_col = "SP500_Return"

fig2 = px.histogram(
    returns,
    x=dist_col,
    nbins=100,
    title=f"Distribution of Daily Returns: {index_choice}"
)

st.plotly_chart(fig2, use_container_width=True)

# ---- Visualization 3: Rolling Volatility ----

st.subheader(f"Rolling Volatility ({vol_window} Day Window)")

fig3 = px.line(
    returns,
    x="Date",
    y=["Russell_Volatility", "SP500_Volatility"],
    title="Market Volatility Comparison"
)

st.plotly_chart(fig3, use_container_width=True)

# ---- Visualization 4: Normalized Growth ----

st.subheader("Growth of a $1 Investment")

normalized = df.copy()

normalized["Russell 2000"] = normalized["Russell 2000"] / normalized["Russell 2000"].iloc[0]
normalized["S&P 500"] = normalized["S&P 500"] / normalized["S&P 500"].iloc[0]

fig4 = px.line(
    normalized,
    x="Date",
    y=["Russell 2000", "S&P 500"],
    title="Normalized Investment Growth"
)

st.plotly_chart(fig4, use_container_width=True)

# ---- Visualization 5: Correlation ----

st.subheader("Relationship Between Index Returns")

fig5 = px.scatter(
    returns,
    x="Russell_Return",
    y="SP500_Return",
    title="Daily Return Relationship",
    opacity=0.5
)

st.plotly_chart(fig5, use_container_width=True)

# --------------------------------------------------
# 4 — SYNTHESIZE
# --------------------------------------------------

st.header("Key Insights")

st.write("""
Key observations from the exploratory analysis:

• The S&P 500 shows steadier long-term growth compared to the Russell 2000.

• The Russell 2000 generally exhibits higher volatility, reflecting the greater risk
associated with smaller companies.

• Daily return distributions suggest that small-cap stocks experience more extreme
positive and negative movements.

• Over certain periods, small-cap stocks outperform large caps, but they also
experience sharper drawdowns.
""")

# --------------------------------------------------
# TELL THE STORY
# --------------------------------------------------

st.header("Implications")

st.write("""
For investors and financial analysts, the comparison between small-cap and large-cap
stocks highlights a classic trade-off between risk and stability.

Small-cap companies may offer higher growth potential but tend to fluctuate more.
Large-cap companies provide more consistent long-term performance with lower volatility.

A diversified portfolio may benefit from exposure to both segments of the market.
""")

# --------------------------------------------------
# DATA SOURCE
# --------------------------------------------------

st.markdown("---")

st.header("Data Source and Sustainability")

st.write("""
Data Source: Yahoo Finance

Indices Used:
• Russell 2000 (small-cap index)
• S&P 500 (large-cap index)

Access Method:
Data retrieved programmatically using the yfinance API.

Date Accessed:
Data is downloaded dynamically each time the dashboard runs.

Data Sustainability:
The dashboard automatically refreshes when the application is restarted,
allowing the analysis to stay current as new market data becomes available.
""")