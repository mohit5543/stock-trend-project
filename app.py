import streamlit as st
import yfinance as yf
import plotly.express as px

#1. Page configuration
st.set_page_config(page_title="Stock trend Dashboard", layout="wide")
st.title("Stock Market Trend Dashboard")

#2. Sidebar for control 
st.sidebar.header("User Input")
ticker = st.sidebar.text_input("Enter Ticker Symbol", "AAPL")
time_period = st.sidebar.selectbox("Select Time Period", ["6mo", "1y", "2y", "5y"])

#3. Fetching data
data = yf.download(ticker, period=time_period)

if not data.empty:
    #4. Data science logic : 50 day moving average 
    # This smooth out price noise to show the actual trend
    data['MA50'] = data['Close'].rolling(window=50).mean()

    #5. The main chart
    fig = px.line(data, x=data.index, y=['Close', 'MA50'],
                  title=f"{ticker} price vs 50-Day Moving Average",
                  labels={'value': 'Price (USD)', 'Date': 'Date'})
    st.plotly_chart(fig, use_container_width=True)

    #6. Statistics Table 
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Market Summary")
        st.dataframe(data.describe(), use_container_width=True)
    with col2:
        st.subheader("Latest Data")
        st.write(data.tail())
else:
    st.error("Please enter a valid ticker (e.g. TSLA, GOOGL, MSFT)")