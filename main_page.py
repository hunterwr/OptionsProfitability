import streamlit as st
import pandas as pd
import altair as alt

st.markdown('# Option Profitability')

col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1])

tickr = col1.text_input('Ticker')
strike = col2.number_input('Strike Price')
option_type = col3.selectbox('Call or Put', ['Call', 'Put'])
buysell = col4.selectbox('Buy or Sell', ['Buy', 'Sell'])
gap = col5.number_input('Gap between strikes')


df = pd.DataFrame()

for i in range(-10, 10):
    #define row to add
    row_to_append = pd.DataFrame([{'Expiration Price':(strike-(gap*i)), 'points':i}])

    #add row to empty DataFrame
    df = pd.concat([df, row_to_append])


