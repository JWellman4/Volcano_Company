import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title='Sales',
    page_icon='volcano',
)

def load_data(file_path):
    return pd.read_csv(file_path)

# Load the data
df = load_data('C:/Users/jonat/Downloads/Financials.csv')
df['Date'] = pd.to_datetime(df['Date'])

st.session_state.update(st.session_state)

# Creating Defs
def add_select_all_option3(options_data3):
    options_with_select_all3 = ['Select All'] + options_data3
    return options_with_select_all3

def options_select3():
    if "selected_options3" in st.session_state:
        if "Select All" in st.session_state["selected_options3"]:
            st.session_state["selected_options3"] = [available_options3[0]]
            st.session_state["max_selections3"] = 1
        else:
            st.session_state["max_selections3"] = len(available_options3)

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
options_data3 = df['Country'].unique().tolist()
options_with_select_all3 = add_select_all_option3(options_data3)
available_options3 = options_with_select_all3

if "max_selections3" not in st.session_state:
    st.session_state["max_selections3"] = len(available_options3)

with st.sidebar:
    st.sidebar.title('Select Fitlers')
    min_date = min(df['Date'])
    max_date = max(df['Date'])
    select_week = st.date_input(
        label='Select Date(s)',
        value=(min_date, max_date),
    )
    select_options3 =st.multiselect(
            label="Select an Option",
            options=options_with_select_all3,
            key="selected_options3",
            max_selections=st.session_state["max_selections3"],
            on_change=options_select3,
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
if 'Select All' in select_options3:
    df_filtered = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
else:
    df_filtered = df[df['Country'].isin(select_options3) & (df['Date'] >= start_date) & (df['Date'] <= end_date)]

#Calculations
filtered_df_country = df_filtered.groupby(by=['Country'], as_index=False)['Sales'].sum()
filtered_df_month = df_filtered.groupby(by=['Date'], as_index=False)['Sales'].sum()
filtered_df_segment= df_filtered.groupby(by=['Segment'], as_index=False)['Sales'].sum()

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
        y='Sales',
        title='Sales Trend',
        width=500,
        height=300,
    )
fig.update_traces(hovertemplate= '<b>%{x| %B %Y}<br>'+ '$%{y:,.0f}', line_color='#FF0099')
fig.update_xaxes(dtick= 'M1',tickformat='%b %Y')
fig.update_yaxes(tickprefix='$')
fig.update_layout(xaxis=dict(title=None),yaxis=dict(title=None))

fig2 = px.pie(
        filtered_df_country,
        values='Sales',
        names= 'Country',
        color='Sales', color_discrete_sequence=px.colors.sequential.Viridis,
        hole= 0.5,
        title='Total Sales by Country',
        width=300,
        height=300
    )
fig2.update_traces(textposition='outside', 
                   textinfo='percent+label',
                   hovertemplate= '<b>%{label}<br>'+ '$%{value}')
fig2.update(layout_showlegend=False)

fig3 = px.bar(
        filtered_df_segment,
        x='Sales',
        y='Segment',
        text='Sales',
        labels={'Segment': '', 'Sales': 'Sales'},
        orientation='h',
        width=300,
        height=300,
        title='Total Sales by Segment'
    )
fig3.update_xaxes(title='', tickprefix='$')
fig3.update_traces(hovertemplate= '<b>%{y}<br><b>$%{x:,.0f}<b>', marker_color = '#FF0099', texttemplate='$%{x:,.0f}')
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

