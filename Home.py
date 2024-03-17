import streamlit as st
import os


from utils.side_bar import side_bar

from rich.traceback import install

install()

# make data dir if it doesn't exist
os.makedirs("data", exist_ok=True)

st.set_page_config(
    page_title="LIDA: Home",
    page_icon="📊",
)

st.write("# LIDA: Automatic Generation of Visualizations and Infographics using Large Language Models 📊")


st.markdown(
    """
    LIDA is a library for generating data visualizations and data-faithful infographics (not used in this demo).
    
    Details on the components of LIDA are described in the [paper here](https://arxiv.org/abs/2303.02927) and in this
    tutorial [notebook](notebooks/tutorial.ipynb). See the project page [here](https://microsoft.github.io/lida/) for updates!.

   This demo shows how to use the LIDA python api with Streamlit. 

   The sidebar on the left allows you to set the OpenAI API key, select the model, and set the temperature for text generation.

    Also, there are additional options to use the cache and select the dataset and summarization method.

    Some additional functionalities include:
    - Data preprocessing guide for the selected dataset.
    - A data explorer for the selected dataset.

    The pages can be accessed using the sidebar on the left.

   ----
""")



