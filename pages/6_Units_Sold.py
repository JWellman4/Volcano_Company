import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title='Units Sold',
    page_icon='volcano',
)

def load_data(file_path):
    return pd.read_csv(file_path)

# Load the data
df = load_data('Financials.csv')
df['Date'] = pd.to_datetime(df['Date'])

st.session_state.update(st.session_state)

# Creating Defs
def add_select_all_option6(options_data6):
    options_with_select_all6 = ['Select All'] + options_data6
    return options_with_select_all6

def options_select6():
    if "selected_options6" in st.session_state:
        if "Select All" in st.session_state["selected_options6"]:
            st.session_state["selected_options6"] = [available_options6[0]]
            st.session_state["max_selections6"] = 1
        else:
            st.session_state["max_selections6"] = len(available_options6)

def date_selected6():
    if "selected_date6" not in st.session_state:
        if len(select_week) > 1:
            end_date = pd.to_datetime(select_week[1])
        else:
            end_date = start_date

def format_sales(sales_card):
    if abs(sales_card) >= 1_000_000:
        return '${:.1f}M'.format(sales_card / 1_000_000)
    elif abs(sales_card) >= 1_000:
        return '${:.1f}K'.format(sales_card / 1_000)
    else:
        return '${:.1f}'.format(sales_card)
    
def format_profit(profit_card):
    if abs(profit_card) >= 1_000_000:
        return '${:.1f}M'.format(profit_card / 1_000_000)
    elif abs(profit_card) >= 1_000:
        return '${:.1f}K'.format(profit_card / 1_000)
    else:
        return '${:.1f}'.format(profit_card)

# Load options from a CSV file
options_data6 = df['Country'].unique().tolist()
options_with_select_all6 = add_select_all_option6(options_data6)
available_options6 = options_with_select_all6

if "max_selections6" not in st.session_state:
    st.session_state["max_selections6"] = len(available_options6)

with st.sidebar:
    st.sidebar.title('Select Fitlers')
    min_date = min(df['Date'])
    max_date = max(df['Date'])
    select_week = st.date_input(
        label='Select Date(s)',
        value=(min_date, max_date),
        key="selected_date6",
        on_change=date_selected6
    )
    select_options6 =st.multiselect(
            label="Select an Option",
            options=options_with_select_all6,
            key="selected_options6",
            max_selections=st.session_state["max_selections6"],
            on_change=options_select6,
            format_func=lambda x: "Select All" if x == "Select All" else f"{x}"
    )

# Convert select_week to datetime64[ns]
start_date = pd.to_datetime(select_week[0])

# Check if select_week contains at least two elements before accessing the second element
if len(select_week) > 1:
    end_date = pd.to_datetime(select_week[1])
else:
    end_date = start_date

# Filter DataFrame based on selected options from both multiselects
if 'Select All' in select_options6:
    df_filtered = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
else:
    df_filtered = df[df['Country'].isin(select_options6) & (df['Date'] >= start_date) & (df['Date'] <= end_date)]

#Calculations
filtered_df_country = df_filtered.groupby(by=['Country'], as_index=False)['Units Sold'].sum()
filtered_df_month = df_filtered.groupby(by=['Date'], as_index=False)['Units Sold'].sum()
filtered_df_segment= df_filtered.groupby(by=['Segment'], as_index=False)['Units Sold'].sum()
filtered_df_net_profit_margin = df_filtered['Profit'].sum() / df_filtered['Gross Sales'].sum()
gross_sales_by_product = df_filtered.groupby(['Product'])['Gross Sales'].sum()
product_net_profit_margin = df_filtered.groupby(['Product'])['Profit'].sum() / gross_sales_by_product

#Cards
sales_card = df_filtered['Sales'].sum()
sales_formatted= format_sales(sales_card)
profit_card = df_filtered['Profit'].sum()
profit_formatted = format_profit(profit_card)
units_sold_card = df_filtered['Units Sold'].sum()
units_sold_formatted = "{:,.0f}".format(units_sold_card)

fig = px.line(
        filtered_df_month,
        x='Date',
        y='Units Sold',
        title='Units Sold Trend',
        width=500,
        height=300,
    )
fig.update_traces(hovertemplate= '<b>%{x| %B %Y}<br>'+ '%{y:,.0f}', line_color='#CC00FF')
fig.update_xaxes(dtick= 'M1', tickformat='%b %Y')
fig.update_layout(xaxis=dict(title=None),yaxis=dict(title=None))

fig2 = px.pie(
        filtered_df_country,
        values='Units Sold',
        names= 'Country',
        color='Units Sold', color_discrete_sequence=px.colors.sequential.haline,
        hole= 0.5,
        title='Total Units Sold by Country',
        width=300,
        height=300
    )
fig2.update_traces(textposition='outside', 
                   textinfo='percent+label',
                   hovertemplate= '<b>%{label}<br>'+ '%{value}')
fig2.update(layout_showlegend=False)

fig3 = px.bar(
        filtered_df_segment,
        x='Units Sold',
        y='Segment',
        text='Units Sold',
        labels={'Segment': '', 'Units Sold': 'Units Sold'},
        orientation='h',
        width=300,
        height=300,
        title='Total Units Sold by Segment'
    )
fig3.update_traces(hovertemplate= '<b>%{y}<br><b>%{x:,.0f}<b>', marker_color = '#CC00FF', texttemplate='%{x:,.0f}')
fig3.update_layout( yaxis={'categoryorder':'total ascending'}, hovermode="y")

#Layout
col1, col2, col3 = st.columns(3)
row1 = st.columns(1)
for col in row1:
    with col1:
        st.metric(label='Total Sales', value=sales_formatted)
    with col2:
        st.metric(label='Total Profit', value=profit_formatted)
    with col3:
        st.metric(label='Total Units Sold', value=units_sold_formatted)

row2 = st.columns(1)
for col in row2:
        st.plotly_chart(fig, use_container_width=True)

col5, col6 = st.columns(2, gap='medium')
row3 = st.columns(1)
for col in row3:
    with col5:
        st.plotly_chart(fig2, use_container_width=True)
    with col6:
        st.plotly_chart(fig3, use_container_width=True)
