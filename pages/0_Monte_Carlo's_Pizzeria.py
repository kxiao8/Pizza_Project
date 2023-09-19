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

from typing import Any
import numpy as np
import streamlit as st
from streamlit.hello.utils import show_code


st.set_page_config(page_title="Monte Carlo's Pizza", page_icon="📹")
st.markdown("# Monte Carlo's Pizza")
st.sidebar.header("Monte Carlo's Pizza")
st.write("""**Monte Carlo's Pizzeria and the Mysterious π**

In the bustling streets of Napoli, there was a quirky little pizzeria named "Monte Carlo's." Unlike other pizzerias, Monte Carlo's was known for more than just its scrumptious pizzas; it was known for a century-old puzzle, inscribed on the wall beside the wood-fired oven. The puzzle stated, "If you can estimate π using a pizza, your meal is on the house!"

Over the years, many tried, yet failed, to crack the riddle. People would draw circles, measure diameters, and discuss advanced math, but no one could relate π and pizza in a way that satisfied the owner.

One evening, a young math enthusiast named Sofia entered the pizzeria. Intrigued by the challenge, she ordered the largest pizza on the menu. As she waited, she pondered how the pizza could be used to estimate π.

When the pizza arrived, Sofia had an idea. She remembered the Monte Carlo method she had learned in her statistics class. She asked the chef for some diced olives and began her experiment.

First, she drew a square boundary on a parchment paper, ensuring the pizza fit entirely within. Then, she started placing diced olives randomly all over the pizza and the parchment paper, ensuring she did not look while dropping them.

After hundreds of olives, Sofia began her calculations. She counted the number of olives that landed on the pizza and those that landed outside. Knowing the pizza was a perfect circle (Monte Carlo's pizzeria was known for its perfectly round pizzas) and the parchment paper formed a square, she realized that the ratio of olives on the pizza to the total number of olives would give her an approximation of π/4. 

She quickly did the math:

```
π/4 = (number of olives on the pizza) / (total number of olives)
π = 4 * (number of olives on the pizza) / (total number of olives)
```

Eureka! Her approximation was incredibly close to the known value of π.

The owner, having observed the entire process, was astounded. He not only gave Sofia her meal for free but also named a pizza after her, "Sofia's πzza."

From that day on, every year, on Pi Day (March 14th), Monte Carlo's Pizzeria would host the "Estimate π with Pizza" contest, keeping the delightful combination of math and pizza alive in Napoli's heart.

And that, my friend, is the tale of Monte Carlo's Pizza and the ingenious method to estimate π.
                  
- Fiction Author: ChatGPT"""
)

def monte_carlo_pi(num_points, width, height):
    inside_circle = 0
    radius = width // 2
    center_x, center_y = width // 2, height // 2

    # Initialize a white image
    image = np.ones((height, width))

    for _ in range(num_points):
        x, y = np.random.randint(0, width), np.random.randint(0, height)

        # Calculate distance from the center
        distance = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5

        # Check if the point is inside the circle
        if distance <= radius:
            inside_circle += 1
            image[y, x] = 0  # color the point black

    # Using a full circle
    pi_approx = 4 * inside_circle / num_points
    return pi_approx, image

def animation_pi():
    st.title("Sofia's πzza")

    max_darts = st.sidebar.slider("Number of olives", 1000, 5000, 1000)
    num_trials = st.sidebar.slider("Number of trials", 0, 200, 100)

    width, height = 640, 640

    progress_bar = st.sidebar.progress(0)
    trial_text = st.sidebar.empty()
    image_placeholder = st.empty()
    average_pi_text = st.empty()  # New text element to display the average pi value

    #num_trials = 100
    total_pi = 0  # Initialize a total to compute the average

    for trial_num in range(num_trials):
        num_darts = max(1, int(max_darts * (trial_num + 1) / num_trials))
        pi_approx, img = monte_carlo_pi(num_darts, width, height)

        total_pi += pi_approx
        average_pi = total_pi / (trial_num + 1)
        average_pi_text.text(f"Average π value over {trial_num + 1} trials: {average_pi:.4f}")

        progress_bar.progress((trial_num + 1) / num_trials)  # Corrected here
        trial_text.text(f"trial {trial_num + 1}/{num_trials} - Current π ≈ {pi_approx:.4f}")

        # Display the image
        image_placeholder.image(img, use_column_width=True, clamp=True)


    progress_bar.empty()
    trial_text.empty()

    st.button("Re-run")

# Call the function
animation_pi()

