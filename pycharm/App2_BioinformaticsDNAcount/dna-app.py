import pandas as pd
import streamlit as st
import  altair as alt
from PIL import  Image

st.sidebar.header('Enter DNA sequence')
st.header('Enter DNA sequence')

sequence_input= '>DAN Query 2\nGATCCAACGCCTTAAACCCGG\nAAACCCTTTACTGACTGGGGAAA'

sequence=st.text_area('Sequence input', sequence_input,height=250)
sequence=sequence.split()
sequence=sequence[1:]
sequence=''.join(sequence) # concatenates list to string

# line
st.write("""
***
"""
)

# print the input DNA sequence
st.header('Input (DNA Query)')
sequence

#DNA nucleotide count
st.header('Output (DNA nucleotide count)')

#1. print dictionary
st.subheader('1. Print dictionary')
def DNA_nucleotide_count(seq):
    d=dict([
        ('A', seq.count('A')),
        ('T',seq.count('T')),
        ('C',seq.count('C')),
        ('G',seq.count('G'))
        ])
    return d

X=DNA_nucleotide_count(sequence)
X_label=list(X)
X_values=list(X.values())

X

#2. print text
st.subheader('Print text')
st.write('there are '+ str(X['A'])+ ' A')
st.write('there are '+ str(X['T'])+ 'T')
st.write('there are '+ str(X['C'])+ 'C')
st.write('there are '+ str(X['G'])+'G')

#3. Display dataframe
st.subheader('3. Display dataframe')
df=pd.DataFrame.from_dict(X,orient='index')
df=df.rename({0:'count'},axis='columns')
df.reset_index(inplace=True)
df=df.rename(columns={'index':'nucleotide'})
st.write(df)

#4. display bar chart using altair
st.subheader('4. Display bar chart')
p=alt.Chart(df).mark_bar().encode(
    x='nucleotide',
    y='count'
)
p=p.properties(
    width=alt.Step(80)
)
st.write(p)
























