import streamlit as st
import pandas as pd
import base64
from bs4 import BeautifulSoup
import requests
import json
import matplotlib.pyplot as plt

#st.beta_set_page_config(layout="wide")
st.title('Crypto Price App')
st.markdown("""
This app retrieves cryptocurrency prices for the top 100 cryptocurrency from the **CoinMarketCap**!
"""
)
expander_bar=st.beta_expander('About')
expander_bar.markdown("""
* **Python library**: streamlit, pandas, numpy, bs4, time
* **Data source**: [CoinMarketCap](https://www.wikpedia.org/)
""")

col1=st.sidebar
col2,col3=st.beta_columns((2,1))

col1.header('Input Options')
currency_price_unit=col1.selectbox('Select currency for the price',('USD','BTC','ETH'))

#web scraping of coinMarketCap data
@st.cache
def load_data():
    cmc=requests.get('https://coinmarketcap.com/')
    soup=BeautifulSoup(cmc.content, 'html.parser')

    data=soup.find('script',id='__NEXT_DATA__',type='application/json')
    coins={}
    coin_data=json.loads(data.contents[0])
    listings=coin_data['props']['initialState']['cryptocurrency']['listingLatest']['data']
    for i in listings:
        coins[str(i['id'])]=i['slug']

    coin_name=[]
    coin_symbol=[]
    market_cap=[]
    percent_change_1h=[]
    percent_change_24h = []
    percent_change_7d = []
    price=[]
    volume_24h=[]

    for i in listings:
        coin_name.append(i['slug'])
        coin_symbol.append(i['symbol'])
        price.append(i['quote'][currency_price_unit]['price'])
        percent_change_1h.append(i['quote'][currency_price_unit]['percentChange1h'])
        percent_change_24h.append(i['quote'][currency_price_unit]['percentChange24h'])
        percent_change_7d.append(i['quote'][currency_price_unit]['percentChange7d'])
        market_cap.append(i['quote'][currency_price_unit]['marketCap'])
        volume_24h.append(i['quote'][currency_price_unit]['volume24h'])

    df=pd.DataFrame(columns=['coin_name','coin_symbol','market_cap','volume_24h','percent_change_1h','percent_change_24h','percent_change_7d'])
    df['coin_name']=coin_name
    df['coin_symbol']=coin_symbol
    df['market_cap']=market_cap
    df['volume_24h']=volume_24h
    df['percent_change_1h']=percent_change_1h
    df['percent_change_24h'] = percent_change_24h
    df['percent_change_7d'] = percent_change_7d
    return df

df=load_data()

#siderbar
sorted_coin=sorted(df['coin_symbol'])
selected_coin=col1.multiselect('Cryptocurrency',sorted_coin,sorted_coin[:50])

df_selected_coin=df[df['coin_symbol'].isin(selected_coin)]
# siderbar, number of coin to display
num_coin=col1.slider('Display Top N coin',1,100,100)
df_coin_display=df_selected_coin[:num_coin]

#siderbar, percentage of changes
percent_timeframe=col1.selectbox('Percent change time frame',['7d','24h','1h'])
percent_dict={'7d':'percent_change_7d','24h':'percent_change_24h','1h':'percent_change_1h'}
selected_percent_timeframe=percent_dict[percent_timeframe]

#siderbar, sorting values
sort_values=col1.selectbox('Sort values?',['yes','no'])

col2.subheader('Price of selected cryptocurrency')
col2.write('There are '+str(df_coin_display.shape[0])+' cryptocurrency are selected')
col2.dataframe(df_coin_display)

#download data
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
col2.markdown(filedownload(df_coin_display),unsafe_allow_html=True)


# prepare the data for the bar plot
col2.subheader('Table of % Price Change')
df_change=pd.concat([df_coin_display.coin_symbol, df_coin_display.percent_change_1h, df_coin_display.percent_change_24h,df_coin_display.percent_change_7d])
df_change=df_coin_display[['coin_symbol','percent_change_1h','percent_change_24h','percent_change_7d']]
df_change=df_change.set_index('coin_symbol')
df_change['postive_percent_change_1h']=df_change.percent_change_1h>0
df_change['postive_percent_change_24h']=df_change.percent_change_24h>0
df_change['postive_percent_change_7d']=df_change.percent_change_7d>0
col2.dataframe(df_change)

if percent_timeframe=='7d':
    if sort_values=='yes':
        df_change=df_change.sort_values(by=['percent_change_7d'])
    col3.write('*7 days period*')
    plt.figure(figsize=(5, 25))
    plt.subplots_adjust(top=1, bottom=0)
    df_change['percent_change_7d'].plot(kind='barh',color=df_change['postive_percent_change_7d'].map({True: 'g', False: 'r'}))
    col3.pyplot(plt)
elif percent_timeframe=='1h':
    if sort_values=='yes':
        df_change=df_change.sort_values(by=['percent_change_1h'])
    col3.write('*1 hour period*')
    plt.figure(figsize=(5, 25))
    plt.subplots_adjust(top=1, bottom=0)
    df_change['percent_change_1h'].plot(kind='barh',color=df_change['postive_percent_change_1h'].map({True: 'g', False: 'r'}))
    col3.pyplot(plt)
elif percent_timeframe=='24h':
    if sort_values=='yes':
        df_change=df_change.sort_values(by=['percent_change_24h'])
    col3.write('*24 hour period*')
    plt.figure(figsize=(5, 25))
    plt.subplots_adjust(top=1, bottom=0)
    df_change['percent_change_24h'].plot(kind='barh',color=df_change['postive_percent_change_24h'].map({True: 'g',False: 'r'}))
    col3.pyplot(plt)














