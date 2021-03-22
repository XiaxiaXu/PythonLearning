st.write("""
# Simple Stock Price App

Shown are the stock closing price and volume of google!

""")

#tickerInfo= tickerData.info
#tickerCalendar= tickerData.calendar

# get historical price for this ticker
#tickerDf= tickerData.history(period='1d', start='2010-5-31',end='2021-2-26')

#st.line_chart(tickerDf.Volume)
#st.line_chart(tickerDf.Open)


#print(tickerDf)
#print(tickerInfo)
#print(tickerCalendar)
#print(tickerRecom)

#st.write(list(tickerDf))
#st.write(tickerInfo)
#st.write(list(tickerCalendar))
#st.write(list(tickerRecom))




# define the ticker symbol
tickerSymbol = 'GOOGL'

# get data on this ticker
tickerData= yf.Ticker(tickerSymbol)
tickerRecom= tickerData.recommendations

# streamlit display
st.write(tickerSymbol)
st.write(tickerRecom.truncate(before=RecommDate))

tickerDf= tickerData.history(period='1d', start=startTime)   # Open, High, Low, Close,Volume,Dividends
st.line_chart(tickerDf.Close)








