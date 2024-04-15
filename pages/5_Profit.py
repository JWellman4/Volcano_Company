import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title='Profit',
    page_icon='volcano',
)

def load_data(file_path):
    return pd.read_csv(file_path)

# Load the data
df = load_data('Financials.csv')
df['Date'] = pd.to_datetime(df['Date'])
min_date = min(df['Date'])
max_date = max(df['Date'])

st.session_state.update(st.session_state)

# Creating Defs
def add_select_all_option5(options_data5):
    options_with_select_all5 = ['Select All'] + options_data5
    return options_with_select_all5

def options_select5():
    if "selected_options5" in st.session_state:
        if "Select All" in st.session_state["selected_options5"]:
            st.session_state["selected_options5"] = [available_options5[0]]
            st.session_state["max_selections5"] = 1
        else:
            st.session_state["max_selections5"] = len(available_options5)

def date_selected5():
    if "selected_date5" not in st.session_state:
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
options_data5 = df['Country'].unique().tolist()
options_with_select_all5 = add_select_all_option5(options_data5)
available_options5 = options_with_select_all5

if "max_selections5" not in st.session_state:
    st.session_state["max_selections5"] = len(available_options5)

if "selected_date5" not in st.session_state:
    st.session_state["selected_date5"] = (min_date, max_date)

with st.sidebar:
    st.sidebar.title('Select Fitlers')
    select_week = st.date_input(
        label='Select Date(s)',
        on_change=date_selected5
    )
    select_options5 =st.multiselect(
            label="Select an Option",
            options=options_with_select_all5,
            key="selected_options5",
            max_selections=st.session_state["max_selections5"],
            on_change=options_select5,
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
if 'Select All' in select_options5:
    df_filtered = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
else:
    df_filtered = df[df['Country'].isin(select_options5) & (df['Date'] >= start_date) & (df['Date'] <= end_date)]

#Calculations
filtered_df_country = df_filtered.groupby(by=['Country'], as_index=False)['Profit'].sum()
filtered_df_month = df_filtered.groupby(by=['Date'], as_index=False)['Profit'].sum()
filtered_df_segment= df_filtered.groupby(by=['Segment'], as_index=False)['Profit'].sum()

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
        y='Profit',
        title='Profit Trend',
        width=500,
        height=300,
    )
fig.update_traces(hovertemplate= '<b>%{x| %B %Y}<br>'+ '$%{y:,.0f}', line_color='#FF6600')
fig.update_xaxes(dtick= 'M1',tickformat='%b %Y')
fig.update_yaxes(tickprefix='$')
fig.update_layout(xaxis=dict(title=None),yaxis=dict(title=None))

fig2 = px.pie(
        filtered_df_country,
        values='Profit',
        names= 'Country',
        color='Profit', color_discrete_sequence=px.colors.sequential.Plasma,
        hole= 0.5,
        title='Total Profit by Country',
        width=300,
        height=300
    )
fig2.update_traces(textposition='outside', 
                   textinfo='percent+label',
                   hovertemplate= '<b>%{label}<br>'+ '$%{value}')
fig2.update(layout_showlegend=False)

fig3 = px.bar(
        filtered_df_segment,
        x='Profit',
        y='Segment',
        text='Profit',
        labels={'Segment': '', 'Profit': 'Profit'},
        orientation='h',
        width=300,
        height=300,
        title='Total Profit by Segment'
    )
fig3.update_xaxes(title='', tickprefix='$')
fig3.update_traces(hovertemplate= '<b>%{y}<br><b>$%{x:,.0f}<b>', marker_color = '#FF6600',textfont_color='white',texttemplate='$%{x:,.0f}')
fig3.update_traces(textposition="inside")
fig3.update_layout( yaxis={'categoryorder':'total ascending'}, hovermode="y",uniformtext_minsize=10, 
                   uniformtext_mode='hide')

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
