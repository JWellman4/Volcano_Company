import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title='Profits by Product',
    page_icon='volcano',
)

def load_data(file_path):
    return pd.read_csv(file_path)

# Load the data
df = load_data('Financials.csv')
df['Date'] = pd.to_datetime(df['Date'])

st.session_state.update(st.session_state)

# Creating Defs
def add_select_all_option7(options_data7):
    options_with_select_all7 = ['Select All'] + options_data7
    return options_with_select_all7

def options_select7():
    if "selected_options7" in st.session_state:
        if "Select All" in st.session_state["selected_options7"]:
            st.session_state["selected_options7"] = [available_options7[0]]
            st.session_state["max_selections7"] = 1
        else:
            st.session_state["max_selections7"] = len(available_options7)
  
def format_profit(profit_card):
    if abs(profit_card) >= 1_000_000:
        return '${:.1f}M'.format(profit_card / 1_000_000)
    elif abs(profit_card) >= 1_000:
        return '${:.1f}K'.format(profit_card / 1_000)
    else:
        return '${:.1f}'.format(profit_card)
    
def format_sales(gross_sales_card):
    if abs(gross_sales_card) >= 1_000_000:
        return '${:.1f}M'.format(gross_sales_card / 1_000_000)
    elif abs(gross_sales_card) >= 1_000:
        return '${:.1f}K'.format(gross_sales_card / 1_000)
    else:
        return '${:.1f}'.format(gross_sales_card)

# Load options from a CSV file
options_data7 = df['Product'].unique().tolist()
options_with_select_all7 = add_select_all_option7(options_data7)
available_options7 = options_with_select_all7

if "max_selections7" not in st.session_state:
    st.session_state["max_selections7"] = len(available_options7)

with st.sidebar:
    st.sidebar.title('Select Fitlers')
    min_date = min(df['Date'])
    max_date = max(df['Date'])
    select_week = st.date_input(
        label='Select Date(s)',
        value=(min_date, max_date),
    )
    select_options7 =st.multiselect(
            label="Select a Product",
            options=options_with_select_all7,
            key="selected_options7",
            max_selections=st.session_state["max_selections7"],
            on_change=options_select7,
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
if 'Select All' in select_options7:
    df_filtered = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
else:
    df_filtered = df[df['Product'].isin(select_options7) & (df['Date'] >= start_date) & (df['Date'] <= end_date)]

#Calculations
profit_by_product = df_filtered.groupby(by=['Product'], as_index=False)['Profit'].sum()
gross_sales_by_product = df_filtered.groupby(['Product'])['Gross Sales'].sum()
profit_margin_card = (df_filtered['Profit'].sum() / df_filtered['Gross Sales'].sum()) * 100
product_net_profit_margin = df_filtered.groupby(['Product'])['Profit'].sum() / gross_sales_by_product

#Cards
profit_card = df_filtered['Profit'].sum()
profit_formatted = format_profit(profit_card)
gross_sales_card = df_filtered['Sales'].sum()
gross_sales_formatted= format_sales(gross_sales_card)
profit_margin_formatted = "{:,.2f}%".format(profit_margin_card)

# Group by month and year, calculate sum of profits and gross sales
grouped_by_month = df_filtered.groupby(['Date']).agg({'Profit': 'sum', 'Gross Sales': 'sum'}).reset_index()
grouped_by_product = df_filtered.groupby(['Product']).agg({'Profit': 'sum', 'Gross Sales': 'sum'}).reset_index()
grouped_by_country = df_filtered.groupby(['Country']).agg({'Profit': 'sum', 'Gross Sales': 'sum'}).reset_index()

# Calculate net profit margin for each month
grouped_by_month['Net Profit Margin'] = (grouped_by_month['Profit'] / grouped_by_month['Gross Sales'])
formatted_net_profit_margin = [f'{value:.2%}' for value in grouped_by_month['Net Profit Margin']]
grouped_by_product['Net Profit Margin'] = (grouped_by_product['Profit'] / grouped_by_product['Gross Sales'])
formatted_net_profit_margin_product = [f'{value:.2%}' for value in grouped_by_product['Net Profit Margin']]
grouped_by_country['Net Profit Margin'] = (grouped_by_country['Profit'] / grouped_by_country['Gross Sales'])
formatted_net_profit_margin_country = [f'{value:.2%}' for value in grouped_by_country['Net Profit Margin']]

fig = px.line(
        grouped_by_month,
        x='Date',
        y= formatted_net_profit_margin,
        width=500,
        height=300,
        title='Net Profit Margins Trends'
)
fig.update_traces(hovertemplate= '<b>%{x| %B %Y}<br>'+ '%{y:,.2f}%', line_color='#39FF14')
fig.update_xaxes(dtick= 'M1',tickformat='%b %Y')
fig.update_yaxes(ticksuffix='%')
fig.update_layout(xaxis=dict(title=None),yaxis=dict(title=None))

fig2 = px.bar_polar(
        grouped_by_product,
        r='Net Profit Margin',
        theta='Product',
        color = 'Product',
        template='plotly_dark',
        color_discrete_sequence=px.colors.sequential.Plasma_r,
        width=400,
        height=400,
        title='Net Profit Margin by Product'
    )
fig2.update_traces(hovertemplate= '%{r:.2%}')
fig2.update_layout(polar = dict(radialaxis = dict(showticklabels = False)), showlegend=False)

fig3 = px.bar(
        grouped_by_country,
        x=formatted_net_profit_margin_country,
        y='Country',
        text=formatted_net_profit_margin_country,
        orientation='h',
        width=300,
        height=300,
        title='Net Profit Margin by Country'
    )
fig3.update_traces(hovertemplate= '<b>%{y}<br><b>%{x:,.2f}%', marker_color='#39FF14')
fig3.update_xaxes(ticksuffix='%')
fig3.update_layout(yaxis={'categoryorder':'total ascending'}, hovermode="y", showlegend=False)
fig3.update_layout(xaxis=dict(title=None), yaxis=dict(title=None))

#Layout
col1, col2, col3 = st.columns(3)
row1 = st.columns(1)
for col in row1:
    with col1:
        st.metric(label='Total Profit', value=profit_formatted)
    with col2:
        st.metric(label='Total Gross Sales', value=gross_sales_formatted)
    with col3:
        st.metric(label='Net Profit Margin %', value=profit_margin_formatted)

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
