# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import numpy as np
import pandas as pd
import streamlit as st
from streamlit.hello.utils import show_code


# For simple pie chart with percentage
def alt_pie(data:pd.DataFrame, value_col:str, color_by:str,
            title_name:str=None):
    # Add percentage
    data['percentage'] = data[value_col]/sum(data[value_col])
    
    # Plot normal pie chart
    chart = alt.Chart(data).mark_arc().encode(
        theta=alt.Theta(field=value_col, type="quantitative"),
        color=alt.Color(field=color_by, type="nominal", scale=alt.Scale(scheme='yellowgreenblue')),
        tooltip=[color_by, value_col, alt.Tooltip('percentage:Q', format='.1%')]
    ).properties(
        width=300,
        height=300
    )
    
    # Add title
    if title_name:
        chart = chart.properties(
            title={
                "text": [title_name],
                "fontSize": 12,
                "fontWeight": "bold"
            }
        )
    return chart.configure_view(stroke=None)

# Create a bar chart of the promotion sales by region and Has_Promo using Altair
def alt_bar_horizontal(data:pd.DataFrame, x_col:str, y_col:str, color_by:str,
                       title_name:str=None, sort_bar=True, show_data=False, color_domain_order=None):
    # Add percentage
    numeric_cols = data.select_dtypes(include='number').columns
    y_sum = data.groupby(y_col)[numeric_cols].sum(numeric_only=True)[x_col].reset_index().rename(columns={x_col:'Total'})
    data = data.merge(y_sum, on=y_col, how='left')
    data['percentage'] = data[x_col]/data['Total']

    # Show dataframe result
    if show_data:
        print(data)
        
    # Change color scheme for different use case
    if len(data[color_by].unique()) > 5:
        my_scheme = 'category20'
        color_scale = alt.Scale(scheme=my_scheme)
    else:
        my_scheme = 'yellowgreenblue'
        if color_domain_order:
            color_range = ['#ffffcc', '#a1dab4', '#41b6c4', '#2c7fb8', '#253494']
            color_scale = alt.Scale(domain=color_domain_order, range=color_range)
        else:
            color_scale = alt.Scale(scheme=my_scheme)

    
    # Sort the color by the color domain
    if color_domain_order:
        color_scale = alt.Scale(domain=color_domain_order, range=color_range)
        coloring = alt.Color('%s:N' % color_by,
                legend=alt.Legend(title=color_by, orient='right'),
                scale=color_scale,
                sort=color_domain_order)
    else:
        coloring = alt.Color('%s:N' % color_by,
                        legend=alt.Legend(title=color_by, orient='right'),
                        scale=alt.Scale(scheme=my_scheme))
    # Sort the axis
    if sort_bar:
        sort_by = '-x'
    else:
        sort_by = 'y'

    # Plot bar chart
    chart = alt.Chart(data).mark_bar().encode(
        x=alt.X('%s:Q' % x_col, axis=alt.Axis(labelAngle=0, title=x_col)),
        y=alt.Y('%s:N' % y_col, sort=sort_by),
        color=coloring,
        order=alt.Order('color_%s_sort_index:Q' % color_by),
        tooltip=['%s:N' % color_by, '%s:Q' % x_col, '%s:N' % y_col,
                  alt.Tooltip('percentage:Q', format='.1%')]
    ).properties(
        width=500,
        height=400
    )
    # Mark percentage for boolean category
    if data[color_by].dtype == bool:
        data['X_Loc'] = data.apply(lambda row: row['Total'] if row[color_by] else row[x_col], axis=1)
        data['X_Loc'] = data.loc[(data['Total'] > max(data['Total'])*0.3) | (data[color_by])]['X_Loc']
        data['X_Loc'] = data.loc[(data[x_col] < data['Total']*0.8) | (data[color_by])]['X_Loc']
        text_perc = chart.mark_text(
            align='center',
            baseline='bottom',
            dy=5,
            dx=20
        ).encode(
            y='%s:N' % y_col,
            x=alt.X('X_Loc:Q', axis=alt.Axis(labelAngle=0)),
            text=alt.Text('percentage:Q', format='.1%')
        )

        chart = chart + text_perc

    # Add title
    if title_name:
        chart = chart.properties(
            title={
                "text": [title_name],
                "fontSize": 12,
                "fontWeight": "bold"
            }
        )
    return chart

def alt_bar_vertical(data: pd.DataFrame, x_col: str, y_col: str, color_by: str,
                     title_name: str = None, sort_bar: bool = True, show_data: bool = False,
                     color_domain_order: list = None):

    # Add percentage
    numeric_cols = data.select_dtypes(include='number').columns
    y_sum = data.groupby(y_col)[numeric_cols].sum(numeric_only=True)[x_col].reset_index().rename(columns={x_col:'Total'})
    data = data.merge(y_sum, on=y_col, how='left')
    data['percentage'] = data[x_col]/data['Total']

    # Show dataframe result
    if show_data:
        print(data)
        
    # Change color scheme for different use case
    if len(data[color_by].unique()) > 5:
        my_scheme = 'category20'
        color_scale = alt.Scale(scheme=my_scheme)
    else:
        my_scheme = 'yellowgreenblue'
        if color_domain_order:
            color_range = ['#ffffcc', '#a1dab4', '#41b6c4', '#2c7fb8', '#253494']
            color_scale = alt.Scale(domain=color_domain_order, range=color_range)
        else:
            color_scale = alt.Scale(scheme=my_scheme)

    
    # Sort the color by the color domain
    if color_domain_order:
        color_scale = alt.Scale(domain=color_domain_order, range=color_range)
        coloring = alt.Color('%s:N' % color_by,
                legend=alt.Legend(title=color_by, orient='right'),
                scale=color_scale,
                sort=color_domain_order)
    else:
        coloring = alt.Color('%s:N' % color_by,
                        legend=alt.Legend(title=color_by, orient='right'),
                        scale=alt.Scale(scheme=my_scheme))
    # Sort the axis
    if sort_bar:
        sort_by = '-y'
    else:
        sort_by = 'x'

    # Plot bar chart
    chart = alt.Chart(data).mark_bar().encode(
        y=alt.Y('%s:Q' % x_col),
        x=alt.X('%s:N' % y_col, sort=sort_by, axis=alt.Axis(labelAngle=0, title=y_col)),
        color=coloring,
        order=alt.Order('color_%s_sort_index:Q' % color_by, sort='descending'),
        tooltip=['%s:N' % color_by, '%s:Q' % x_col, '%s:N' % y_col,
                 alt.Tooltip('percentage:Q', format='.1%')]
    ).properties(
        width=400,
        height=500
    )
    
    # Mark percentage for boolean category
    if data[color_by].dtype == bool:
        data['Y_Loc'] = data.apply(lambda row: row['Total'] if row[color_by] else row[x_col], axis=1)
        data['Y_Loc'] = data.loc[(data['Total'] > max(data['Total']) * 0.3) | (data[color_by])]['Y_Loc']
        data['Y_Loc'] = data.loc[(data[x_col] < data['Total'] * 0.8) | (data[color_by])]['Y_Loc']

        text_perc = chart.mark_text(
            align='center',
            baseline='middle',
            dy=-15
        ).encode(
            x='%s:N' % y_col,
            y=alt.Y('Y_Loc:Q', axis=alt.Axis(labelAngle=0)),
            text=alt.Text('percentage:Q', format='.1%')
        )

        chart = chart + text_perc

    # Add title
    if title_name:
        chart = chart.properties(
            title={
                "text": [title_name],
                "fontSize": 12,
                "fontWeight": "bold"
            }
        )
    return chart

st.set_page_config(page_title="Pizzeria EDA", page_icon="📈")
st.markdown("# Pizzeria EDA")
st.sidebar.header("Pizzeria EDA")

import altair as alt
from vega_datasets import data

# Basic Stats
df = pd.read_csv('./pizza_sales.csv')
# Total Meta Stats
ms_total_rev = df['total_price'].sum()
ms_total_sales = df['quantity'].sum()
ms_total_order = df['order_id'].nunique()

# Average Meta Stats
ms_average_rev = ms_total_rev/ms_total_order
ms_average_sales = ms_total_sales/ms_total_order

# Print out the meta stats
st.write(
    """
    This Exploratory Data Analysis demonstrates some data secret of Monte Carlo's Pizzeria
    
    Total Revenue: $ %.2f\\
    Total Sales: %d\\
    Total Order: %d

    Average Revenue: $ %.2f\\
    Average Sales: %.2f

    Here is the ranking of customers' favorite pizzas, category and price range:
    """ % (ms_total_rev, ms_total_sales, ms_total_order, ms_average_rev, ms_average_sales)
)



# Pizza Sales Count (with Size)
name_size_cnt = df.groupby(['pizza_name', 'pizza_size']).count()['order_id'].reset_index()
name_size_cnt = name_size_cnt.rename(columns={'order_id': 'count'})

name_size_p1 = alt_bar_horizontal(name_size_cnt, 'count', 'pizza_name', 'pizza_size',
                   title_name='Pizza Order Distribution',
                   color_domain_order=['S', 'M', 'L', 'XL', 'XXL'])

# Pizza Size Sales Sum
name_size_sum = df.groupby(['pizza_name', 'pizza_size']).sum(numeric_only=True)['total_price'].reset_index()
name_size_sum = name_size_sum.rename(columns={'total_price': 'sales'})

name_size_p2 = alt_bar_horizontal(name_size_sum, 'sales', 'pizza_name', 'pizza_size',
                   title_name='Pizza Sales Distribution',
                   color_domain_order=['S', 'M', 'L', 'XL', 'XXL'])

# Category Sales Count (with Size)
cate_size_cnt = df.groupby(['pizza_category', 'pizza_size']).count()['order_id'].reset_index()
cate_size_cnt = cate_size_cnt.rename(columns={'order_id': 'count'})


cate_size_p1 = alt_bar_vertical(cate_size_cnt, 'count', 'pizza_category', 'pizza_size',
                   title_name='Category Order Distribution',
                   color_domain_order=['S', 'M', 'L', 'XL', 'XXL'])

# Category Sales Sum (with Size)
cate_size_sum = df.groupby(['pizza_category', 'pizza_size']).sum(numeric_only=True)['total_price'].reset_index()
cate_size_sum = cate_size_sum.rename(columns={'total_price': 'sales'})

cate_size_p2 = alt_bar_vertical(cate_size_sum, 'sales', 'pizza_category', 'pizza_size',
                 title_name='Category Sales Distribution',
                 color_domain_order=['S', 'M', 'L', 'XL', 'XXL'])

# Price Point Study
price_cnt = df.groupby(['unit_price', 'pizza_size']).count()['order_id'].reset_index()
price_cnt = price_cnt.rename(columns={'order_id': 'count'})

price_p1 = alt.Chart(price_cnt).mark_point().encode(
    x='unit_price:Q',
    y='count:Q',
    color='pizza_size:N',
    tooltip=['pizza_size:N', 'unit_price:Q', 'count:Q']
).properties(
            title={
                "text": ['Unit Price Distribution'],
                "fontSize": 12,
                "fontWeight": "bold"
            }
        )

# Total Price Study
total_price_cnt = df.groupby(['total_price', 'pizza_size']).count()['order_id'].reset_index()
total_price_cnt = total_price_cnt.rename(columns={'order_id': 'count'})

price_p2 = alt.Chart(total_price_cnt).mark_point().encode(
    x='total_price:Q',
    y='count:Q',
    color='pizza_size:N',
    tooltip=['pizza_size:N', 'total_price:Q', 'count:Q']
).properties(
            title={
                "text": ['Order Price Distribution'],
                "fontSize": 12,
                "fontWeight": "bold"
            }
        )

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Pizza Order", "Pizza Sales",
                                              "Category Order", "Category Sales",
                                              "Unit Price", "Order Price"])

with tab1:
    st.altair_chart(name_size_p1, theme="streamlit", use_container_width=True)
with tab2:
    st.altair_chart(name_size_p2, theme="streamlit", use_container_width=True)
with tab3:
    st.altair_chart(cate_size_p1, theme="streamlit", use_container_width=True)
with tab4:
    st.altair_chart(cate_size_p2, theme="streamlit", use_container_width=True)
with tab5:
    st.altair_chart(price_p1, theme="streamlit", use_container_width=True)
with tab6:
    st.altair_chart(price_p2, theme="streamlit", use_container_width=True)

# Print out the meta stats
st.write(
    """
    Here comes the pizza(pie) charts:
    """ 
)

# Overall Size Sales Count
size_cnt = df.groupby('pizza_size').count()['order_id'].reset_index()
size_cnt = size_cnt.rename(columns={'order_id': 'count'})

pie_size_p1 = alt_pie(size_cnt, 'count', 'pizza_size', title_name='Size Order Pie')

# Overall Size Sales Sum
size_sum = df.groupby('pizza_size').sum(numeric_only=True)['total_price'].reset_index()
size_sum = size_sum.rename(columns={'total_price': 'sales'})

pie_size_p2 = alt_pie(size_sum, 'sales', 'pizza_size', title_name='Size Sales Pie')

# Overall Category Sales Count
cate_cnt = df.groupby('pizza_category').count()['order_id'].reset_index()
cate_cnt = cate_cnt.rename(columns={'order_id': 'count'})

pie_cate_p1 = alt_pie(cate_cnt, 'count', 'pizza_category', title_name='Category Order Pie')

# Overall Category Sales Sum
cate_sum = df.groupby('pizza_category').sum(numeric_only=True)['total_price'].reset_index()
cate_sum = cate_sum.rename(columns={'total_price': 'sales'})

pie_cate_p2 = alt_pie(cate_sum, 'sales', 'pizza_category', title_name='Category Sales Pie')

tab1, tab2, tab3, tab4 = st.tabs(["Size Order", "Size Sales",
                                  "Category Order", "Category Sales"])

with tab1:
    st.altair_chart(pie_size_p1, theme="streamlit", use_container_width=True)
with tab2:
    st.altair_chart(pie_size_p2, theme="streamlit", use_container_width=True)
with tab3:
    st.altair_chart(pie_cate_p1, theme="streamlit", use_container_width=True)
with tab4:
    st.altair_chart(pie_cate_p2, theme="streamlit", use_container_width=True)

# Print out the meta stats
st.write(
    """
    Here comes the time-based analysis:
    """
)

# Most High Sales Season
season_cnt = df.groupby('order_quarter').count()['order_id'].reset_index()
season_cnt = season_cnt.rename(columns={'order_id': 'count'})

season_p = alt_bar_vertical(season_cnt, 'count', 'order_quarter', 'order_quarter',
                        title_name='Pizza Sales Season Distribution',
                        sort_bar=False)

# Most High Sales Month
month_cnt = df.groupby('order_month').count()['order_id'].reset_index()
month_cnt = month_cnt.rename(columns={'order_id': 'count'})

month_p = alt_bar_vertical(month_cnt, 'count', 'order_month', 'order_month',
                        title_name='Pizza Sales Month Distribution',
                        sort_bar=False)

# Most High Sales Weekday
weekday_cnt = df.groupby('order_weekday').count()['order_id'].reset_index()
weekday_cnt = weekday_cnt.rename(columns={'order_id': 'count'})

week_p = alt_bar_vertical(weekday_cnt, 'count', 'order_weekday', 'order_weekday',
                        title_name='Pizza Sales Weekday Distribution',
                        sort_bar=False)

# Most High Sales Hour
hour_cnt = df.groupby('order_hour').count()['order_id'].reset_index()
hour_cnt = hour_cnt.rename(columns={'order_id': 'count'})

day_p = alt_bar_vertical(hour_cnt, 'count', 'order_hour', 'order_hour',
                     title_name='Pizza Sales Hour Distribution',
                     sort_bar=False)

tab1, tab2, tab3, tab4 = st.tabs(["Seasonal Trend", "Monthly Trend",
                                  "Weekly Trend", "Daily Trend"])

with tab1:
    st.altair_chart(season_p, theme="streamlit", use_container_width=True)
with tab2:
    st.altair_chart(month_p, theme="streamlit", use_container_width=True)
with tab3:
    st.altair_chart(week_p, theme="streamlit", use_container_width=True)
with tab4:
    st.altair_chart(day_p, theme="streamlit", use_container_width=True)