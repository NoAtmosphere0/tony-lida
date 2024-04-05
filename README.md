# tony-lida
A web-based implementation of [LIDA](https://github.com/microsoft/lida) - a library for generating data visualizations and data-faithful infographics; with more functionalities and a user-friendly interface.

## App structure
.  
├── datasets/  
│   ├── covid_data.csv  
│   └── titanic.csv  
├── pages/  
│   ├── 01_Goals and Visualization.py  
│   ├── 02_Data Explorer.py  
│   └── 03_Data Prep.py  
├── utils/    
│   ├── data_explorer.py  
│   ├── prep_guide.py  
│   └── side_bar.py  
├── .gitignore  
├── Home.py  
├── LICENSE  
├── README.md  
└── requirements.txt

## Features of this implementation
- Generate goal-oriented data visualizations
- Data exploration
- Data preprocessing guides

## Getting started
**Note:** The app requires an OpenAI API key to run.

The original LIDA library is built on top of [llmx](https://github.com/victordibia/llmx) and can use different LLM providers such as [OpenAI, AzureOpenAI, PaLM, Cohere and local HuggingFace Models].

1. Clone the repository
```bash
git clone https://github.com/NoAtmosphere0/tony-lida
```
2. Install the dependencies
```bash
cd tony-lida
pip install -r requirements.txt
```
3. Run the app
```bash
streamlit run Home.py
```

You can also see the app in action [here](https://tony-lida-demo.streamlit.app/)



