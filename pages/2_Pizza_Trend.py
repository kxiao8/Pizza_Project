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

from urllib.error import URLError

import altair as alt
import pandas as pd

import streamlit as st
from streamlit.hello.utils import show_code

pizza_name_list = ['The Hawaiian Pizza',
 'The Classic Deluxe Pizza',
 'The Five Cheese Pizza',
 'The Italian Supreme Pizza',
 'The Mexicana Pizza',
 'The Thai Chicken Pizza',
 'The Prosciutto and Arugula Pizza',
 'The Barbecue Chicken Pizza',
 'The Greek Pizza',
 'The Spinach Supreme Pizza',
 'The Green Garden Pizza',
 'The Italian Capocollo Pizza',
 'The Spicy Italian Pizza',
 'The Spinach Pesto Pizza',
 'The Vegetables + Vegetables Pizza',
 'The Southwest Chicken Pizza',
 'The California Chicken Pizza',
 'The Pepperoni Pizza',
 'The Chicken Pesto Pizza',
 'The Big Meat Pizza',
 'The Soppressata Pizza',
 'The Four Cheese Pizza',
 'The Napolitana Pizza',
 'The Calabrese Pizza',
 'The Italian Vegetables Pizza',
 'The Mediterranean Pizza',
 'The Pepper Salami Pizza',
 'The Spinach and Feta Pizza',
 'The Sicilian Pizza',
 'The Chicken Alfredo Pizza',
 'The Pepperoni, Mushroom, and Peppers Pizza',
 'The Brie Carre Pizza']

def pizza_data():
    @st.cache_data
    def get_pizza_data():
        df = pd.read_csv('./pizza_sales_time_range.csv')
        return df

    df = get_pizza_data()
    pizzas = st.multiselect(
        "Choose pizzas", list(df['pizza_name']), ['The Classic Deluxe Pizza', 'The Five Cheese Pizza']
    )
    if not pizzas:
        st.error("Please select at least one pizza.")
    else:
        data = df[df['pizza_name'].isin(pizzas)].set_index('pizza_name')
        st.write("### Pizza Sales Selection", data)

        data = data.T.reset_index()
        data = pd.melt(data, id_vars=["index"]).rename(
            columns={"index": "date", "value": "pizza_sales"}
        )

        # Calculate the monthly total sales for the selected pizzas
        total_sales = data.groupby('date')['pizza_sales'].sum().reset_index()

        # Merge the original data with the total sales
        data_with_percentage = pd.merge(data, total_sales, on="date", suffixes=('', '_total'))

        # Calculate the contribution percentage
        data_with_percentage['percentage'] = (data_with_percentage['pizza_sales'] / data_with_percentage['pizza_sales_total'])

        # Line chart with thicker line
        line_chart = (
            alt.Chart(data_with_percentage)
            .mark_line(opacity=0.3, size=3)  # Adjust the size parameter as needed for thickness
            .encode(
                x=alt.X("date:N", sort=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                                        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                                        axis=alt.Axis(labelAngle=0)),
                y=alt.Y("pizza_sales:Q", stack=None),
                color="pizza_name:N",
            )
        )

        # Dots for each data point
        dots_chart = (
            alt.Chart(data_with_percentage)
            .mark_circle(size=60, opacity=0.8)
            .encode(
                x=alt.X("date:N", sort=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                                        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                                        axis=alt.Axis(labelAngle=0)),
                y=alt.Y("pizza_sales:Q", stack=None),
                color="pizza_name:N",
                tooltip=["date:N", "pizza_sales:Q", "pizza_name:N", alt.Tooltip('percentage:Q', format='.1%', title='percentage')]
            )
        )

        # Combine the line chart and dots chart
        chart1 = line_chart + dots_chart

        st.altair_chart(chart1, use_container_width=True)

        # Calculate the monthly total sales for the selected pizzas
        data_total = data.groupby('date')['pizza_sales'].sum().reset_index()
        data_total['pizza_name'] = 'Total'

        data_total_piv = data_total
        # Define month order
        months_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

        # Convert 'date' to categorical with the month order
        data_total_piv['date'] = pd.Categorical(data_total_piv['date'], categories=months_order, ordered=True)

        # Sort by 'date'
        data_total_piv = data_total_piv.sort_values('date')

        # Pivot table
        data_total_piv = data_total_piv.pivot(index='date', columns='pizza_name', values='pizza_sales')

        st.write("### Pizza Sales Total", data_total_piv.T)

        # Line chart for total sales
        line_chart_total = (
            alt.Chart(data_total)
            .mark_line(opacity=0.7, size=4, color="black")  # Adjust the size parameter as needed for thickness
            .encode(
                x=alt.X("date:N", sort=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                                        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                                        axis=alt.Axis(labelAngle=0)),
                y=alt.Y("pizza_sales:Q"),
                tooltip=["date:N", "pizza_sales:Q", "pizza_name:N"]
            )
        )

        # Dots for each total data point
        dots_chart_total = (
            alt.Chart(data_total)
            .mark_circle(size=70, opacity=0.8, color="black")
            .encode(
                x=alt.X("date:N", sort=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                                        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                                        axis=alt.Axis(labelAngle=0)),
                y=alt.Y("pizza_sales:Q"),
                tooltip=["date:N", "pizza_sales:Q", "pizza_name:N"]
            )
        )

        # Combine the total line chart and dots chart
        chart2 = line_chart_total + dots_chart_total

        st.altair_chart(chart2, use_container_width=True)

st.set_page_config(page_title="Pizza Trend", page_icon="🍕")
st.markdown("# Pizza Trend")
st.sidebar.header("Pizza Trend")
st.write(
    """This interactive plot shows the monthly sales of Monte Carlo's Pizzeria."""
)

pizza_data()



