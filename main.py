import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

st.set_page_config(layout="wide")
col1, col2 = st.columns(2)

ticker = col1.text_input('Ticker: ', 'AAPL')
oticker = ticker
odate = col2.text_input('Options Expiration Date: ', '2022-12-16')
osymbol = yf.Ticker(oticker)

#options

opt = osymbol.option_chain(odate)

cstrike = opt.calls['strike']
cvol = opt.calls['volume'].fillna(0)
coi = opt.calls['openInterest'].fillna(0)
clast = opt.calls['lastPrice']
cpremium = round((clast * coi) * 100, 0)
cpremiumvol = round((clast * cvol) * 100, 0)
pstrike = opt.puts['strike']
pvol = opt.puts['volume'].fillna(0)
poi = opt.puts['openInterest'].fillna(0)
plast = opt.puts['lastPrice']
ppremium = round((plast * poi) * 100, 0)
ppremiumvol = round((plast * pvol) * 100, 0)
ctotaloi = sum(coi)
ctotalvol = sum(cvol)
ptotaloi = sum(poi)
ptotalvol = sum(pvol)
ctotalprem = sum(cpremium)
ptotalprem = sum(ppremium)
ctotalpremvol = sum(cpremiumvol)
ptotalpremvol = sum(ppremiumvol)
pcoi = round((ptotaloi / ctotaloi), 2)
pcvol = round((ptotalvol / ctotalvol), 2)
pcprem = round((ptotalprem / ctotalprem), 2)
pcpremvol = round((ptotalpremvol / ctotalpremvol), 2)
cppremvol = round((ctotalpremvol / ptotalpremvol), 2)
cpoi = round((ctotaloi / ptotaloi), 2)
cpvol = round((ctotalvol / ptotalvol), 2)
cpprem = round((ctotalprem / ptotalprem), 2)
colors = ['green', 'red']

#Figures

st.header('Put vs Call Stats')

col1_1, col2_1, col3_1 = st.columns((1,1,1))

volumePie = go.Figure(data=go.Pie(
    labels=['Call Volume', 'Put Volume'],
    text=['Call Volume', 'Put Volume'],
    hoverinfo='skip',
    values=[ctotalvol, ptotalvol],
    textinfo='text+value+percent'))
volumePie.update_layout(width=400)
volumePie.update_traces(showlegend=False,
                     marker=dict(colors=colors))
with col1_1:
    st.write(volumePie)

oiPie = go.Figure(data=go.Pie(
    labels=['Call Open Interest', 'Put Open Interest'],
    text=['Call Open Interest', 'Put Open Interest'],
    hoverinfo='skip',
    values=[ctotaloi, ptotaloi],
    textinfo='text+value+percent'))
oiPie.update_layout(width=400)
oiPie.update_traces(showlegend=False,
                    marker=dict(colors=colors))
with col2_1:
    st.write(oiPie)

premiumPie = go.Figure(data=go.Pie(
    labels=['Call Premium', 'Put Premium'],
    text=['Call Premium', 'Put Premium'],
    hoverinfo='skip',
    values=[ctotalprem, ptotalprem],
    textinfo='text+value+percent'))
premiumPie.update_layout(width=400)
premiumPie.update_traces(showlegend=False,
                         marker=dict(colors=colors))
with col3_1:
   st.write(premiumPie)

col1_2, col2_2 = st.columns((1,1,))

oibar = go.Figure()
oibar.add_trace(go.Bar(
    x=cstrike,
    y=coi,
    name='Call OI',
    marker_color='green'))
oibar.add_trace(go.Bar(
    x=pstrike,
    y=poi,
    name='Put OI',
    marker_color='red'))
oibar.update_layout(
    title='Open Interest By Strike',
    xaxis_tickfont_size=14,
    yaxis=dict(
        titlefont_size=16,
        tickfont_size=14,),
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'),
    barmode='group',
    bargap=0.15,
    bargroupgap=0.1,
    hovermode="x",
    width=600)
with col1_2:
    st.write(oibar)

prembar = go.Figure()
prembar.add_trace(go.Bar(
    x=cstrike,
    y=cpremium,
    name='Call Premium',
    marker_color='green'))
prembar.add_trace(go.Bar(
    x=pstrike,
    y=ppremium,
    name='Put Premium',
    marker_color='red'))
prembar.update_layout(
    title='Option Premium By Strike',
    xaxis_tickfont_size=14,
    yaxis=dict(
        titlefont_size=16,
        tickfont_size=14,),
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'),
    barmode='group',
    bargap=0.15,
    bargroupgap=0.1,
    hovermode="x",
    width=1250)
st.write(prembar)

volbar = go.Figure()
volbar.add_trace(go.Bar(
    x=cstrike,
    y=cvol,
    name='Call Volume',
    marker_color='green'))
volbar.add_trace(go.Bar(
    x=pstrike,
    y=pvol,
    name='Put Volume',
    marker_color='red'))
volbar.update_layout(
    title='Option Volume By Strike',
    xaxis_tickfont_size=14,
    yaxis=dict(
        titlefont_size=16,
        tickfont_size=14,),
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'),
    barmode='group',
    bargap=0.15,
    bargroupgap=0.1,
    hovermode="x",
    width=600)
with col2_2:
 st.write(volbar)

col1_2, col2_2 = st.columns((1,1,))

callChain = go.Figure(data=go.Table(
    header=dict(values=['Calls Strike', 'Call Volume', 'Call Open Interest', 'Last Price', 'Premium'],
                fill_color='green',
                line_color='black',
                align='center'),
    cells=dict(values=[cstrike, cvol, coi, clast, cpremium],
               fill_color = 'lightgrey',
               line_color = 'gray',
               font_color = "black",
               format=[".,d", ",d", ",d", ".d", "$,d"],
               align=['center', 'left'])))
callChain.update_layout(margin=dict(l=5,r=5,b=10,t=10),
                       width=600)
with col1_2:
    st.write(callChain)

putChain = go.Figure(data=go.Table(
    header=dict(values=['Puts Strike', 'Put Volume', 'Put Open Interest', 'Last Price', 'Premium'],
                fill_color='red',
                line_color = 'black',
                align='center'),
    cells=dict(values=[pstrike, pvol, poi, plast, ppremium],
               fill_color = 'lightgrey',
               line_color = 'grey',
               font_color = "black",
               format=[".,d", ",d", ",d", ".d", "$,d"],
               align=['center', 'left'])))
putChain.update_layout(margin=dict(l=5,r=5,b=10,t=10),
                      width=600)
with col2_2:
    st.write(putChain)
