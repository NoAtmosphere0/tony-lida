import streamlit as st
import os
import pandas as pd

def side_bar(openai_key= None, temperature=0.0, use_cache=True, selected_dataset=None, selected_model="gpt-3.5-turbo-0125", selected_method="columns"):
    """
    Function to display the sidebar and get the user input for the OpenAI API key, dataset, and summarization method.

    Args:
    ----
    - openai_key (str): The OpenAI API key.
    - temperature (float): The temperature to use for text generation. A higher temperature will result in more random outputs.
    - use_cache (bool): Whether to use the cache for text generation.
    - selected_dataset (str): The path to the selected dataset.
    - selected_model (str): The selected text generation model.
    - selected_method (str): The selected summarization method.

    Returns:
    -------
    None
    """
    
    st.sidebar.write("## Setup")

    # Step 1 - Get OpenAI API key
    openai_key = os.getenv("OPENAI_API_KEY")

    if not openai_key:
        openai_key = st.sidebar.text_input("Enter OpenAI API key:")
        if openai_key:
            display_key = openai_key[:2] + "*" * (len(openai_key) - 5) + openai_key[-3:]
            st.sidebar.write(f"Current key: {display_key}")
        else:
            st.sidebar.write("Please enter OpenAI API key.")
    else:
        display_key = openai_key[:2] + "*" * (len(openai_key) - 5) + openai_key[-3:]
        st.sidebar.write(f"OpenAI API key loaded from environment variable: {display_key}")

    
    # Step 2 - Select a dataset and summarization method
    if openai_key:
        # Initialize selected_dataset to None
        selected_dataset = None

        # select model from gpt-4 , gpt-3.5-turbo, gpt-3.5-turbo-16k
        st.sidebar.write("## Text Generation Model")
        selected_model = "gpt-3.5-turbo-0125"
        st.sidebar.write(f"Selected model: {selected_model}")

        # select temperature on a scale of 0.0 to 1.0
        st.sidebar.write("## Text Generation Temperature")
        temperature = st.sidebar.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=0.0)

        # set use_cache in sidebar
        use_cache = st.sidebar.checkbox("Use cache", value=True)

        # Handle dataset selection and upload
        st.sidebar.write("## Data Summarization")
        st.sidebar.write("### Choose a dataset")

        datasets = [
            {"label": "Select a dataset", "url": None},
            {"label": "Covid", "url": "./datasets/covid_data.csv"},
            {"label": "Titanic", "url": "./datasets/titanic.csv"}
        ]

        selected_dataset_label = st.sidebar.selectbox(
            'Choose a dataset',
            options=[dataset["label"] for dataset in datasets],
            index=0
        )

        upload_own_data = st.sidebar.checkbox("Upload your own data")

        if upload_own_data:
            uploaded_file = st.sidebar.file_uploader("Choose a CSV or JSON file", type=["csv", "json"])

            if uploaded_file is not None:
                # Get the original file name and extension
                file_name, file_extension = os.path.splitext(uploaded_file.name)

                # Load the data depending on the file type
                if file_extension.lower() == ".csv":
                    data = pd.read_csv(uploaded_file)
                elif file_extension.lower() == ".json":
                    data = pd.read_json(uploaded_file)

                # Save the data using the original file name in the data dir
                uploaded_file_path = os.path.join("data", uploaded_file.name)
                data.to_csv(uploaded_file_path, index=False)

                selected_dataset = uploaded_file_path

                datasets.append({"label": file_name, "url": uploaded_file_path})

                # st.sidebar.write("Uploaded file path: ", uploaded_file_path)
        else:
            selected_dataset = datasets[[dataset["label"]
                                        for dataset in datasets].index(selected_dataset_label)]["url"]

        if not selected_dataset:
            st.info("To continue, select a dataset from the sidebar on the left or upload your own.")

        st.sidebar.write("### Choose a summarization method")
        # summarization_methods = ["default", "llm", "columns"]
        summarization_methods = [
            {"label": "llm",
            "description":
            "Uses the LLM to generate annotate the default summary, adding details such as semantic types for columns and dataset description"},
            {"label": "default",
            "description": "Uses dataset column statistics and column names as the summary"},

            {"label": "columns", "description": "Uses the dataset column names as the summary"}]

        # selected_method = st.sidebar.selectbox("Choose a method", options=summarization_methods)
        selected_method_label = st.sidebar.selectbox(
            'Choose a method',
            options=[method["label"] for method in summarization_methods],
            index=0
        )

        selected_method = summarization_methods[[
            method["label"] for method in summarization_methods].index(selected_method_label)]["label"]

        # add description of selected method in very small font to sidebar
        selected_summary_method_description = summarization_methods[[
            method["label"] for method in summarization_methods].index(selected_method_label)]["description"]

        if selected_method:
            st.sidebar.markdown(
                f"<span> {selected_summary_method_description} </span>",
                unsafe_allow_html=True)
            
    return openai_key, temperature, use_cache, selected_dataset, selected_model, selected_method
