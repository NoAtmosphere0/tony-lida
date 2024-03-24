import streamlit as st
import pandas as pd

from utils.side_bar import side_bar
from utils.data_explorer import explore

st.set_page_config(
    page_title="LIDA: Data Explorer",
    page_icon="📊",
)

st.title("Data Explorer")

openai_key = None
selected_dataset = None
selected_method = None
temperature = 0.0
selected_model = "gpt-3.5-turbo-0125"
use_cache = True

openai_key, temperature, use_cache, selected_dataset, selected_model, selected_method = side_bar(
    openai_key, 
    temperature, 
    use_cache, 
    selected_dataset, 
    selected_model, 
    selected_method
)


if selected_dataset is not None:
    data = pd.read_csv(str(selected_dataset))   
    explore(data)