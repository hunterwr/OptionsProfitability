import streamlit as st
import pandas as pd
import altair as alt

st.markdown('# Option Profitability')

col1, col2, col3, col4 = st.columns([1,1,1,1])

tickr = col1.text_input('Ticker')
strike = col2.number_input('Strike Price')
option_type = col3._selectbox('Call or Put', ['Call', 'Put'])
buysell = col3._selectbox('Buy or Sell', ['Buy', 'Sell'])

