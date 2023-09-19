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

import streamlit as st
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)


def run():
    st.set_page_config(
        page_title="Hello",
        page_icon="👋",
    )

    st.write("# Introduction to the Pizza Project! 👋")

    st.write("###### - Made by Keith (Kecheng Xiao)")
    st.write("###### - Data Source: [Pizza Restaurant Sales](https://www.kaggle.com/datasets/shilongzhuang/pizza-sales)")

    st.sidebar.success("Select a section above.")

    st.markdown(
    """
    Welcome to the "Pizza Project," a unique blend of taste, technology, and data-driven innovation. Let's embark on a flavorful journey that explores Monte Carlo's Pizza fiction, dives deep into Pizza Exploratory Data Analysis (EDA), marvels at Pizza Monthly Visualizations, and interacts with the cutting-edge AI Orderbot. This project is an inspired undertaking from the online course "[ChatGPT Prompt Engineering for Developers](https://www.deeplearning.ai/short-courses/chatgpt-prompt-engineering-for-developers/)" which beautifully melds AI prompting with real-world applications.
    
    """)
    
    st.markdown(
    """
      - **Monte Carlo's Pizza Fiction**: In the heart of Napoli, the "Monte Carlo's" pizzeria posed a unique challenge to its customers: estimate π using a pizza for a free meal. Sofia cleverly used the Monte Carlo method and diced olives to approximate π and won the honor.

      - **Pizzeria EDA**: Dive deep into a thorough exploratory data analysis showcasing the current dynamics of "Monte Carlo's" pizzeria. From crowd-favorite pizzas to peak ordering hours, our EDA reveals captivating patterns and insights invaluable to both pizza aficionados and entrepreneurs.
      
      - **Pizza Trend**: With vivid visual depictions, explore the monthly trends and performance of top pizzas in Monte Carlo, offering a clear perspective of their popularity over time.

      - **Pizza Bot**: Gone are the days of traditional pizza ordering. Meet our AI Orderbot - an intuitive, smart, and efficient pizza ordering assistant, designed to understand your pizza preferences and make recommendations tailored just for you.
    """)
    st.markdown(
    """
    
    Greetings to all readers!

    With a strong academic background from the University of Toronto and Western University, combined with my professional experience at Nestle Canada and Sunlight IT Consulting in Shanghai, I've cultivated a deep expertise in data science and analytics. 
    
    Some proud moments include top rankings in the Scotiabank Big Data Case Competition and leading a project on Meta's Metaverse. My technical and analytical skills fuel the detailed data analysis and AI innovations you'll see in the Pizza Project. I hope you enjoy exploring and engaging with it as much as I enjoyed creating it. """)


if __name__ == "__main__":
    run()
