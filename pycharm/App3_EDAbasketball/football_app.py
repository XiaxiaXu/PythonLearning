import pandas as pd
import streamlit as st
import numpy as np
import base64
import matplotlib.pyplot as plt
import seaborn as sns

st.title('NFL football stats (rushing) explorer')

st.markdown("""
This app performs simple webscraping of NFL Football stats data
* ** Python libraries:** base64, pandas, streamlit, matplot, numpy,seaborn
* ** data source:** [pro-football-reference.com] (https://www.pro-football-reference.com/years/2019/rushing.htm)
""")

st.sidebar.header('User input features')
select_year=st.sidebar.selectbox('Year', list(reversed(range(1995,2020))))

#web scraping of NBA PLAYER stats
@st.cache
def load_data(year):
    url='https://www.pro-football-reference.com/years/' + str(year)+ '/rushing.htm' #link is not work
    html=pd.read_html(url,header=1)
    df=html[0]
    raw=df.drop(df[df.Age== 'Age'].index) # delete repeating
    raw=raw.fillna(0)
    playerstats=raw.drop(['Rk'],axis=1)
    return playerstats
playerstats=load_data(select_year)

# Sidebar -- team selection
sorted_unique_team=sorted(playerstats.Tm.unique())
select_team=st.sidebar.multiselect('Team',sorted_unique_team,sorted_unique_team)

#sidebar -- position selection
#sorted_unique_Pos=sorted(playerstats.Pos.unique())
unique_Pos=['RB','QB','WR','TE','FB']
select_pos=st.sidebar.multiselect('Position',unique_Pos,unique_Pos)

#filtering the value
df_selected_team=playerstats[(playerstats.Tm.isin(select_team)) & (playerstats.Pos.isin(select_pos))]

st.header('Display player stats of selected team (s)')
st.write('Data dimension: '+ str(df_selected_team.shape[0]) + ' rows and '+str(df_selected_team.shape[1]) )
st.dataframe(df_selected_team)

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

st.markdown(filedownload(df_selected_team),unsafe_allow_html=True)

# heatmap
if st.button('Intercorrelation Heatmap'):
    st.header('Intercorrelation Matrix heatmap')
    df_selected_team.to_csv('output.csv', index=False) # read in and read out, guess just because the format of the data
    df=pd.read_csv('output.csv')

    corr=df.corr()
    mask=np.zeros_like(corr)
    mask[np.triu_indices_from(mask)]= True
    with sns.axes_style('white'):
        f, ax= plt.subplots(figsize=(7,5))
        ax=sns.heatmap(corr,mask=mask,vmax=1,square=True)
        #st.set_option('deprecation.showPyplotGlobalUse', False)

    st.pyplot()







































