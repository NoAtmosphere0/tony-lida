import streamlit as st
import pandas as pd

from lida import Manager, TextGenerationConfig, llm
from utils.side_bar import side_bar
from utils.prep_guide import GuideExplorer

st.set_page_config(
    page_title="LIDA: Data Preprocessing Guide",
    page_icon="📊",
)

st.title("Data Preprocessing Guide")

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



if openai_key and selected_dataset and selected_method:
    lida = Manager(text_gen=llm("openai", api_key=openai_key))
    textgen_config = TextGenerationConfig(
        n=1,
        temperature=temperature,
        model=selected_model,
        use_cache=use_cache
    )

    summary = lida.summarize(
        selected_dataset,
        summary_method=selected_method,
        textgen_config=textgen_config
    )

    num_guides = st.slider("Number of Guides", min_value=1, max_value=10, value=3)

    explorer = GuideExplorer()

    guides = explorer.generate(
        summary, 
        textgen_config,
        text_gen=lida.text_gen,
        n=num_guides
    )

    for guide in guides:
        st.write("**Index**: ", guide["index"])
        st.write("**Question** ❓: ", guide["question"])
        st.write("**Rationale** 📖: ", guide["rationale"])
        st.write("**Recommendation** 🧾: ", guide["recommendation"])
        st.write("____________________")