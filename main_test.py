from lida import Manager, TextGenerationConfig, llm
from lida.datamodel import Goal
import os
import pandas as pd
import numpy as np
import json
import logging
import pytest
from prep_guide import GuideExplorer
from lida.utils import clean_code_snippet, read_dataframe
from lida.components import summarizer

import rich
from rich.console import Console
from rich.traceback import install

install()


openai_api_key = os.getenv("OPENAI_API_KEY")

selected_dataset = "C:/Long/Coding/Kaggle/Titanic/titanic/train.csv"

lida = Manager(text_gen=llm("openai", api_key=openai_api_key))
textgen_config = TextGenerationConfig(
    n = 1, 
    temperature= 0.7,
    model = "gpt-3.5-turbo-0125", 
    use_cache=True
)

summary = lida.summarize(
    selected_dataset,
    textgen_config = textgen_config, 
    summary_method="columns"
)

print(summary)
print("____________________")

num_guides = 3

explorer = GuideExplorer()

guides = explorer.generate(
    summary, 
    textgen_config,
    text_gen=lida.text_gen,
    n=num_guides
)

for guide in guides:
    print("Index: ", guide["index"])
    print("Question: ", guide["question"])
    print("Rationale: ", guide["rationale"])
    print("Recommendation: ", guide["recommendation"])
    print("____________________")

