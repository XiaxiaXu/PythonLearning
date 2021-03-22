import pandas as pd
import streamlit as st
import numpy as np
import base64
import matplotlib as plt
import seaborn as sns

url='https://www.basketball-reference.com/leagues/'
html=pd.read_html(url,header=0)
df=html[0]
print(df.columns.values.tolist())