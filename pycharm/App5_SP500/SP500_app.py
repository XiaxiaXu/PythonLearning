import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import base64
import datetime
today = datetime.date.today()
deltaYear = datetime.timedelta(days=30)
startDate_5d= today-deltaYear
deltaYear = datetime.timedelta(days=365)
startDate_1y= today-deltaYear

#https://en.wikipedia.org/wiki/List_of_S%26P_500_companies
st.title('S&P 500 App')
st.markdown("""
   This app reviews the list of the [**S&P 500**](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies) and its corresponding **stock closing price**
   * ** Python libraries** :base64, pandas, streamlit, matplotlib
   * ** Data source** : [Wikipedia](https://wikipedia.org/)
"""
)

## prepare data
@st.cache
def load_data(url):
    html=pd.read_html(url,header=0)
    df=html[0]
    return df
url='https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
df_sp500=load_data(url)
#sector=df_sp500.groupby('GICS Sector')

## siderbar 1. Section
st.sidebar.header('GICS sector')
unique_gicsSector=sorted(df_sp500['GICS Sector'].unique())
selectSection=st.sidebar.multiselect('',unique_gicsSector, unique_gicsSector[0])

# Main part 1. Companies in the Sector
df_sp500_selectSector=df_sp500[df_sp500['GICS Sector'].isin(selectSection)]
companies_in_sector=sorted(df_sp500_selectSector.Symbol)
st.header('Display companies in selected Sector')
st.write('There are total '+ str(df_sp500_selectSector.shape[0])+' companies')
st.dataframe(df_sp500_selectSector[['Symbol','Security','GICS Sector']])

## siderbar 2. interested companies------------------------------------------

interested_company=['AMZN','GOOGL','AAPL','MSFT','DIS','NVDA','TSM','ADBE','MCD','WMT','GME','AMC']
all_company=interested_company+companies_in_sector
st.sidebar.header('Interested Company')
selectCompanies=st.sidebar.multiselect('',all_company,interested_company)

# get finance data, https://pypi.org/project/yfinance/

st.header('Stock closing price')
col1,col2=st.beta_columns(2)
for tickerSymbol in list(selectCompanies):
    tickerData = yf.Ticker(tickerSymbol)
    tickerDf_1y = tickerData.history(period='1d', interval='1d',start=startDate_1y)  # Open, High, Low, Close,Volume,Dividends
    tickerDf_5d = tickerData.history(period='1d', interval='2m', start=startDate_5d)  # Open, High, Low, Close,Volume,Dividends
    with col1:
        st.write(tickerSymbol, today)
        st.line_chart(tickerDf_1y.Close)
    with col2:
        st.write('Price=', round(tickerDf_5d.Close[-1],2),'$,    ',round(0.83*tickerDf_5d.Close[-1],2),'€')
        st.bar_chart(tickerDf_5d.Close)

