import streamlit as st
from lida import Manager, TextGenerationConfig, llm
from lida.datamodel import Goal
import pandas as pd

from utils.side_bar import side_bar

st.set_page_config(
    page_title="LIDA: Goals and Visualization",
    page_icon="📊",
)

st.title("Goals and Visualization")

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

def goals_visualizations(openai_key, selected_dataset, selected_method, temperature, selected_model, use_cache):
    # Step 3 - Generate data summary
    if openai_key and selected_dataset and selected_method:
        lida = Manager(text_gen=llm("openai", api_key=openai_key))
        textgen_config = TextGenerationConfig(
            n=1,
            temperature=temperature,
            model=selected_model,
            use_cache=use_cache)

        st.write("## Summary")

        summary = []
        # **** lida.summarize *****
        
        summary = lida.summarize(
            selected_dataset,
            summary_method=selected_method,
            textgen_config=textgen_config)

        if "dataset_description" in summary:
            st.write(summary["dataset_description"])

        if "fields" in summary:
            fields = summary["fields"]
            nfields = []
            for field in fields:
                flatted_fields = {}
                flatted_fields["column"] = field["column"]
                # flatted_fields["dtype"] = field["dtype"]
                for row in field["properties"].keys():
                    if row != "samples":
                        flatted_fields[row] = field["properties"][row]
                    else:
                        flatted_fields[row] = str(field["properties"][row])
                # flatted_fields = {**flatted_fields, **field["properties"]}
                nfields.append(flatted_fields)
            nfields_df = pd.DataFrame(nfields)
            st.write(nfields_df)
        else:
            st.write(str(summary))

        # Step 4 - Generate goals
        if summary:
            st.sidebar.write("### Goal Selection")

            num_goals = st.sidebar.slider(
                "Number of goals to generate",
                min_value=1,
                max_value=10,
                value=3)
            own_goal = st.sidebar.checkbox("Add Your Own Goal")

            # **** lida.goals *****
            goals = lida.goals(summary, n=num_goals, textgen_config=textgen_config)
            st.write(f"## Goals ({len(goals)})")

            default_goal = goals[0].question
            goal_questions = [goal.question for goal in goals]

            if own_goal:
                user_goal = st.sidebar.text_input("Describe Your Goal")

                if user_goal:

                    new_goal = Goal(question=user_goal, visualization=user_goal, rationale="")
                    goals.append(new_goal)
                    goal_questions.append(new_goal.question)

            selected_goal = st.selectbox('Choose a generated goal', options=goal_questions, index=0)

            # st.markdown("### Selected Goal")
            selected_goal_index = goal_questions.index(selected_goal)
            st.write(goals[selected_goal_index])

            selected_goal_object = goals[selected_goal_index]

            # Step 5 - Generate visualizations
            if selected_goal_object:
                st.sidebar.write("## Visualization Library")
                visualization_libraries = ["seaborn", "matplotlib", "plotly"]

                selected_library = st.sidebar.selectbox(
                    'Choose a visualization library',
                    options=visualization_libraries,
                    index=1
                )

                # Update the visualization generation call to use the selected library.
                st.write("## Visualizations")

                # slider for number of visualizations
                num_visualizations = st.sidebar.slider(
                    "Number of visualizations to generate",
                    min_value=1,
                    max_value=10,
                    value=2)

                textgen_config = TextGenerationConfig(
                    n=num_visualizations, temperature=temperature,
                    model=selected_model,
                    use_cache=use_cache)
                
                # viz_button = st.button("Generate Visualizations")
                # if viz_button:
                # **** lida.visualize *****
                visualizations = lida.visualize(
                    summary=summary,
                    goal=selected_goal_object,
                    textgen_config=textgen_config,
                    library=selected_library)

                viz_titles = [f'Visualization {i+1}' for i in range(len(visualizations))]

                selected_viz_title = st.selectbox('Choose a visualization', options=viz_titles, index=0)

                selected_viz = visualizations[viz_titles.index(selected_viz_title)]

                if selected_viz.raster:
                    from PIL import Image
                    import io
                    import base64

                    imgdata = base64.b64decode(selected_viz.raster)
                    img = Image.open(io.BytesIO(imgdata))
                    st.image(img, caption=selected_viz_title, use_column_width=True)

                with st.expander("Show Visualization Code"):
                    st.write("### Visualization Code")
                    st.code(selected_viz.code)

                if visualizations and len(visualizations) > 0:
                    viz_edit_tab, viz_explain_tab, viz_eval_tab, viz_rec_tab = st.tabs(
                        ["Edit", "Explain", "Evaluate", "Recommend"]
                    )

                    with viz_edit_tab:
                        instructions = st.text_input("Give instructions on how to edit the viz")
                        edited_viz = lida.edit(
                            code=selected_viz.code, 
                            instructions=instructions, 
                            summary=summary,
                            library=selected_library,
                            textgen_config=textgen_config
                        )
                        
                        edited_viz = edited_viz[0]

                        if edited_viz.raster:
                            edit_imgdata = base64.b64decode(edited_viz.raster)
                            edit_img = Image.open(io.BytesIO(edit_imgdata))
                            st.image(edit_img, caption="Edited Visualization", use_column_width=True)


                            with st.expander("Show Edited Visualization Code"):
                                st.write("### Edited Visualization Code")
                                st.code(edited_viz.code)

    

                    with viz_explain_tab:
                        explanation = lida.explain(
                            code=selected_viz.code,
                        )
                        explanation = explanation[0]

                        for section in explanation:
                            section_name = section["section"]
                            section_explanation = section["explanation"]

                            st.write(f"### {section_name}")
                            st.write(section_explanation)

                        

                    with viz_eval_tab:
                        evaluation = lida.evaluate(
                            code=selected_viz.code,
                            goal=selected_goal_object,
                            library=selected_library
                        )

                        evaluation = evaluation[0]

                        for dimension in evaluation:
                            dimension_name = dimension["dimension"]
                            dimension_score = dimension["score"]
                            dimension_rationale = dimension["rationale"]

                            st.write(f"### {dimension_name}, Score: **{dimension_score}**")
                            st.write(dimension_rationale)


                    with viz_rec_tab:
                        recommendations = lida.recommend(
                            code = selected_viz.code,
                            summary=summary,
                            n = 2, 
                            textgen_config=textgen_config
                        )

                        for recommendation in recommendations:
                            st.write(recommendation)


                        

goals_visualizations(openai_key, selected_dataset, selected_method, temperature, selected_model, use_cache)