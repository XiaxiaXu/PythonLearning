import streamlit as st
import pandas as pd
import base64
from bs4 import BeautifulSoup
import requests
import json

currency_price_unit='USD'
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
    print(i['quote'][currency_price_unit])
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

