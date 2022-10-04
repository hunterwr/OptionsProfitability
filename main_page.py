import streamlit as st
st.set_page_config (layout="wide")
import pandas as pd
import altair as alt

st.markdown('# Option Profitability')

col1, col2, col3, col4, col5, col6 = st.columns([1,1,1,1,1,1])

options = pd.DataFrame()

tickr = col1.text_input('Ticker')
strike = col2.number_input('Strike Price')
option_type = col3.selectbox('Call or Put', ['Call', 'Put'])
buysell = col4.selectbox('Buy or Sell', ['Buy', 'Sell'])
commission = col5.number_input('Commision')
gap = col6.number_input('Gap between strikes')

def add_to_list(strike, option_type, buysell, commission, options):
    row_to_append = pd.DataFrame([{'Strike':strike, 'Type':option_type, 'Direction':buysell, 'Commission':commission, 'Name':buysell+" "+option_type+" at "+str(strike)+" for "+str(commission)}])
    options = pd.concat([options, row_to_append])
    return options

btn = st.button("Add to list")
if btn:
    options = add_to_list(strike, option_type, buysell, commission, options)
    btn = False
else:
    pass

st.write(options)

#st.multiselect('Compare multiple options')


for row in options:
    strike = row['Strike']
    option_type = row['Type']
    buysell = row['Direction']
    commission = row['Commission']

df = pd.DataFrame()

for i in range(-10, 10):
    #define row to add
    price_at_expiration = strike + (i*gap)
    if option_type == 'Call' and price_at_expiration > strike:
        profit = price_at_expiration - strike - commission
    elif option_type == 'Call' and price_at_expiration <= strike:
        profit = commission * -1
    elif option_type == 'Put' and price_at_expiration < strike:
        profit = strike - price_at_expiration - commission
    elif option_type == 'Put' and price_at_expiration >= strike:
        profit = commission * -1

    if buysell == 'Sell':
        profit*=-1

    row_to_append = pd.DataFrame([{'Expiration Price':(strike+(gap*i)), 'Profit':profit}])

    #add row to empty DataFrame
    df = pd.concat([df, row_to_append])


chart = alt.Chart(df).mark_area().encode(
    x='Expiration Price',
    y='Profit'
)

st.altair_chart(chart, use_container_width=True)