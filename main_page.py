import streamlit as st
st.set_page_config (layout="wide")
import pandas as pd
import altair as alt

st.markdown('# Option Profitability')

col1, col2, col3, col4, col5= st.columns([1,1,1,1,1])




if 'opt' not in st.session_state:
    options = pd.DataFrame()
    st.session_state['opt'] = options


tickr = col1.text_input('Ticker')
strike = col2.number_input('Strike Price')
option_type = col3.selectbox('Call or Put', ['Call', 'Put'])
buysell = col4.selectbox('Buy or Sell', ['Buy', 'Sell'])
commission = col5.number_input('Commision')
#gap = col6.number_input('Gap between strikes')


def add_to_list(strike, option_type, buysell, commission):
    if 'opt' not in st.session_state:
        options = pd.DataFrame([{'Strike':strike, 'Type':option_type, 'Direction':buysell, 'Commission':commission, 'Name':buysell+" "+option_type+" at "+str(strike)+" for "+str(commission)}])
        st.session_state['opt'] = options
    row_to_append = pd.DataFrame([{'Strike':strike, 'Type':option_type, 'Direction':buysell, 'Commission':commission, 'Name':buysell+" "+option_type+" at "+str(strike)+" for "+str(commission)}])
    options = st.session_state['opt']
    options = pd.concat([options, row_to_append])
    st.session_state['opt'] = options


btn = col1.button("Add to list")
if btn:
    add_to_list(strike, option_type, buysell, commission)
    if 'df' in st.session_state:
        del st.session_state['df']
    options = st.session_state['opt']
    center = round(options['Strike'].mean(), 0)

    for idx in range(0, len(options)):
        
        strike = options['Strike'].values[idx]
        option_type = options['Type'].values[idx]
        buysell = options['Direction'].values[idx]
        commission = options['Commission'].values[idx]
        name = options['Name'].values[idx]

        for i in range(-1*int((center/0.10)/2), int((center/0.10)/2)):
            #define row to add
            price_at_expiration = center + (i*0.10)
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

            profit *= 100
            

            if 'df' not in st.session_state:
                df = pd.DataFrame([{'Expiration Price':price_at_expiration, 'Profit':profit, 'Name':name}])
                st.session_state['df'] = df
            else:
                row_to_append = pd.DataFrame([{'Expiration Price':price_at_expiration, 'Profit':profit, 'Name':name}])
                st.session_state['df'] = pd.concat([st.session_state['df'], row_to_append])
        btn = False
else:
    pass

if 'opt' in st.session_state:

    btn2 = col2.button("Clear list")
    if btn2:
        del st.session_state['opt']
        btn = False
    else:
        pass
    st.write(st.session_state['opt'])



#st.multiselect('Compare multiple options')

if 'opt' not in st.session_state:
    pass
else:
    chart = alt.Chart(st.session_state['df']).mark_line().encode(
        x='Expiration Price',
        y='Profit',
        color='Name'
    )


    totals = st.session_state['df'].groupby('Expiration Price')['Profit'].sum().reset_index()
    totals['Profit/Loss'] = 'Profit'
    totals.loc[totals['Profit'] < 0, 'Profit/Loss'] = 'Loss'


    chart2 = alt.Chart(totals).mark_area(opacity=0.5).encode(
        x='Expiration Price',
        y='Profit',
        color = alt.Color('Profit/Loss', scale=alt.Scale(domain=['Profit', 'Loss'], range=['green', 'red']))
    )

    chart3 = alt.Chart(totals).mark_line().encode(
        x='Expiration Price',
        y='Profit',
        color = alt.Color('Profit/Loss', scale=alt.Scale(domain=['Profit', 'Loss'], range=['green', 'red']))
    )

    final_chart = chart2 + chart3
    st.altair_chart(chart, use_container_width=True)
    st.altair_chart(final_chart, use_container_width=True)