import streamlit as st
import pandas as pd

# data = pd.read_csv("datasets/titanic.csv")

def is_numerical(obj) -> bool:
    """ Check if the object is numerical

    Args:
    ----
        obj: Any object

    Returns:
    -------
        bool: True if the object is numerical, False otherwise
    """
    return isinstance(obj, float) or isinstance(obj, int) or pd.isna(obj)

def display(description: dict, type: str, layout: list):
    """ Display the description of the column

    Args:
    ----
        description: dict
            The description of the column
        type: str
            The type of the column
        layout: list
            The layout of the display

    Returns:
    -------
        None
    """
    if type == "numerical":

        with st.container():
            col1, col2, col3, col4 = st.columns(layout)

            with col1:
                chart_data = {
                    "Range": description["chart_columns"],
                    "Value": description["chart_data"],
                }
                chart = st.bar_chart(
                    chart_data, x="Range", use_container_width=True
                )
            with col2:
                st.text(
                    """
                        Valid ✅
                        Missing ❌
                        Mean 📏
                        Std. Deviation 📊
                        Quantiles
                        """
                )
            with col3:
                st.text(
                    f"""
                        {description["valid"]}
                        {description["missing"]}
                        {description["mean"]}
                        {description["std_dev"]}
                        {description["quantiles"][0]}
                        {description["quantiles"][1]}
                        {description["quantiles"][2]}
                        {description["quantiles"][3]}
                        {description["quantiles"][4]}
                        """
                )
            with col4:
                st.text(
                    f"""
                        {round(description["valid"]/ (description["valid"] + description["missing"])*100, 2)}%
                        {round(description["missing"]/ (description["valid"] + description["missing"])*100, 2)}%


                        Min
                        25%
                        50%
                        75%
                        Max
                        """
                )
    elif type == "nominal":
        with st.container():
            col1, col2, col3, col4 = st.columns(layout)
            with col1:
                subcol1, subcol2 = st.columns([1, 7])
                with subcol2:
                    st.markdown(
                        f"""
                                # {description["unique"]} #
                                ### unique values ###
                                """
                    )
            with col2:
                st.text(
                    """
                        Valid
                        Missing
                        Unique
                        Most Common
                        """
                )
            with col3:
                st.text(
                    f"""
                        {description["valid"]}
                        {description["missing"]}
                        {description["unique"]}
                        {description["most_com"]}
                        """
                )
            with col4:
                st.text(
                    f"""
                        {round(description["valid"]/ (description["valid"] + description["missing"])*100, 2)}%
                        {round(description["missing"]/ (description["valid"] + description["missing"])*100, 2)}%

                        {round(description["most_com_count"]/(description["valid"] + description["missing"])*100, 2)}%
                        """
                )

def explore_column(data: pd.DataFrame, col: str):
    """ Explore the column

    Args:
    ----
        data: pd.DataFrame
            The dataset
        col: str
            The column to explore

    Returns:
    -------
        None
    """
    layout = [8, 4, 2, 2]

    is_numerical_field = all(data[col].apply(is_numerical))
    if is_numerical_field:
        type = "numerical"
        quantiles = data[col].quantile([0, 0.25, 0.5, 0.75, 1.0]).tolist()
        quantiles = [round(q, 0) for q in quantiles]
        missing_count = data[col].isna().sum()
        unique_count = data[col].nunique()
        mean = round(data[col].mean(), 2)
        std_dev = round(data[col].std(), 2)
        bins_count = unique_count if unique_count <= 5 else 10
        labels = pd.cut(data[col], bins=bins_count)
        bin_dict = dict()
        for label in labels.unique():
            bin_dict[str(label)] = len(data.loc[labels == label, col].tolist())
        description = {
            "id": col,
            "quantiles": quantiles,
            "chart_columns": list(bin_dict.keys()),
            "chart_data": list(bin_dict.values()),
            "valid": data.shape[0] - missing_count,
            "missing": missing_count,
            "mean": mean,
            "std_dev": std_dev,
        }
        display(description, type, layout)
    else:
        type = "nominal"
        missing_count = data[col].isna().sum()
        unique_count = data[col].nunique()
        occurence = data[col].value_counts()
        most_com_count = occurence.max()
        most_com = str(occurence[occurence == most_com_count].index.tolist())[1:-1]
        description = {
            "id": col,
            "valid": data.shape[0] - missing_count,
            "missing": missing_count,
            "unique": unique_count,
            "most_com": most_com,
            "most_com_count": most_com_count,
        }
        display(description, type, layout)


def explore(data):
    columns = data.columns.tolist()
    options = []
    with st.popover("Select columns to explore"):
        st.write("Select columns to explore")
        check_all = st.checkbox("Select all", key="Select all")
        for column  in columns:
            option1 = st.checkbox(column, key=column)
            if option1:
                options.append(column)
        if check_all:
            options = columns

    # st.write("Selected:", options)
    for column in options:
        st.write(column)
        explore_column(data, column)


# explore(data)
