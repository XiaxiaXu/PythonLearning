import yfinance as yf
import streamlit as st
import pandas as pd

import datetime
today = datetime.date.today()
deltaYear = datetime.timedelta(days=365)
startDate= today-deltaYear

myInterestStocks=[['AMZN','GOOGL','AAPL','MSFT','DIS'],['NVDA','TSM','ADBE','MCD','WMT']]


for tickerSymbols,col in zip(myInterestStocks,st.beta_columns(2)):
    with col:
        for tickerSymbol in tickerSymbols:
            # get data on this ticker
            tickerData= yf.Ticker(tickerSymbol)
            tickerRecom= tickerData.recommendations
            tickerDf = tickerData.history(period='1d', start=startDate)  # Open, High, Low, Close,Volume,Dividends

            # streamlit display
            st.write(tickerSymbol,today,',  Close price=',tickerDf.Close[-1])
            st.line_chart(tickerDf.Close)









