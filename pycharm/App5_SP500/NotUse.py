import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import numpy as np
import base64


#https://en.wikipedia.org/wiki/List_of_S%26P_500_companies
st.title('S&P 500 App')
st.markdown("""
   This app reviews the list of the [**S&P 500**](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies) and its corresponding **stock closing price**
   * ** Python libraries** :base64, pandas, streamlit, numpy, matplotlib, seaborn
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

## siderbar 2. Companies from selected Sector
st.sidebar.header('Companies in Sector')
df_sp500_selectSector=df_sp500[df_sp500['GICS Sector'].isin(selectSection)]
companies_in_sector=sorted(df_sp500_selectSector.Symbol)
number_company=st.sidebar.slider(' ',1,10)
selectCompanies=st.sidebar.multiselect(' ',companies_in_sector,companies_in_sector[:number_company])

# Main part 1. Companies in the Sector
st.header('Display companies in selected Sector')
st.write('There are total '+ str(df_sp500_selectSector.shape[0])+' companies')
st.dataframe(df_sp500_selectSector[['Symbol','Security','GICS Sector']])

#download NBA player stats data
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806/2
def filedownload(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}" download="player.csv">Download csv file</a>'
    return href

st.markdown(filedownload(df_sp500_selectSector),unsafe_allow_html=True)

# get finance data, https://pypi.org/project/yfinance/
data = yf.download(  # or pdr.get_data_yahoo(...
        # tickers list or string as well
        tickers = list(df_sp500_selectSector[:10].Symbol),

        # use "period" instead of start/end
        # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
        # (optional, default is '1mo')
        period = "ytd",

        # fetch data by interval (including intraday if period < 60 days)
        # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
        # (optional, default is '1d')
        interval = "1d",

        # group by ticker (to access via data['SPY'])
        # (optional, default is 'column')
        group_by = 'ticker',

        # adjust all OHLC automatically
        # (optional, default is False)
        auto_adjust = True,

        # download pre/post regular market hours data
        # (optional, default is False)
        prepost = True,

        # use threads for mass downloading? (True/False/Integer)
        # (optional, default is True)
        threads = True,

        # proxy URL scheme use use when downloading?
        # (optional, default is None)
        proxy = None
    )

def price_plot(symbol):
    df=pd.DataFrame(data[symbol].Close)
    df['Date']=df.index
    plt.fill_between(df.Date, df.Close, color='skyblue', alpha=0.3)
    plt.plot(df.Date,df.Close,color='skyblue',alpha=0.8)
    plt.xticks(rotation=90)
    plt.title(symbol,fontweight='bold')
    plt.xlabel('Date', fontweight='bold')
    plt.ylabel('Closing Price', fontweight='bold')
    return plt.show()

## main part 2, plot
if st.button('Show stock plots from Selected Sector'):
    st.header('Stock closing price')
    for i in list(selectCompanies):
        price_plot(i)

## siderbar 3. interested companies------------------------------------------
interested_company=['AMZN','GOOGL','AAPL','MSFT','DIS','NVDA','TSM','ADBE','MCD','WMT']
st.sidebar.multiselect('Interested Company',interested_company,interested_company)
if st.button('Show stock plots from Interested company'):
    st.header('Stock closing price')
    for i in list(interested_company):
        price_plot(i)
