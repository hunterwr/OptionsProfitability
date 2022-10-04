import streamlit as st
st.set_page_config (layout="wide")
import pandas as pd
import altair as alt

st.markdown('# Option Profitability')

col1, col2, col3, col4, col5, col6 = st.columns([1,1,1,1,1,1])




if 'opt' not in st.session_state:
    options = pd.DataFrame()
    st.session_state['opt'] = options


tickr = col1.text_input('Ticker')
strike = col2.number_input('Strike Price')
option_type = col3.selectbox('Call or Put', ['Call', 'Put'])
buysell = col4.selectbox('Buy or Sell', ['Buy', 'Sell'])
commission = col5.number_input('Commision')
gap = col6.number_input('Gap between strikes')


def add_to_list(strike, option_type, buysell, commission):
    if 'opt' not in st.session_state:
        options = pd.DataFrame([{'Strike':strike, 'Type':option_type, 'Direction':buysell, 'Commission':commission, 'Name':buysell+" "+option_type+" at "+str(strike)+" for "+str(commission)}])
        st.session_state['opt'] = options
    row_to_append = pd.DataFrame([{'Strike':strike, 'Type':option_type, 'Direction':buysell, 'Commission':commission, 'Name':buysell+" "+option_type+" at "+str(strike)+" for "+str(commission)}])
    options = st.session_state['opt']
    options = pd.concat([options, row_to_append])
    st.session_state['opt'] = options


btn = st.button("Add to list")
if btn:
    add_to_list(strike, option_type, buysell, commission)
    btn = False
else:
    pass

st.write(st.session_state['opt'])

#st.multiselect('Compare multiple options')

options = st.session_state['opt']
for idx, row in options.iterrows():
    strike = row['Strike']
    option_type = row['Type']
    buysell = row['Direction']
    commission = row['Commission']
    name = row['Name']

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

    if 'df' not in st.session_state:
        df = pd.DataFrame([{'Expiration Price':(strike+(gap*i)), 'Profit':profit, 'Name':name}])
        st.session_state['df'] = df
    else:
        row_to_append = pd.DataFrame([{'Expiration Price':(strike+(gap*i)), 'Profit':profit, 'Name':name}])
        st.session_state['df'] = pd.concat([st.session_state['df'], row_to_append])


chart = alt.Chart(st.session_state['df']).mark_line().encode(
    x='Expiration Price',
    y='Profit',
    color='Name'
)

chart2 = alt.Chart(st.session_state['df']).mark_area().encode(
    x='Expiration Price',
    y='sum(Profit)',
    color=alt.condition(('sum(Profit)' > 0), alt.ColorValue('green'), alt.ColorValue('red'))
)

final_chart = chart2 + chart
st.altair_chart(final_chart, use_container_width=True)