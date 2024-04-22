import gradio as gr
from gradio_leaderboard import Leaderboard, SelectColumns
import config
from pathlib import Path
import pandas as pd

abs_path = Path(__file__).parent

df = pd.read_json(str(abs_path / "leaderboard_data.json"))

# Make a model size column
numeric_interval = pd.IntervalIndex(
    sorted([config.NUMERIC_INTERVALS[s] for s in config.NUMERIC_INTERVALS.keys()])
)
params_column = pd.to_numeric(df["#Params (B)"], errors="coerce")
df["Model Size"] = params_column.apply(
    lambda x: next(s for s in numeric_interval if x in s)
)


with gr.Blocks() as demo:
    gr.Markdown("""
    # 🥇 Leaderboard Component
    Please read the documentation [here](https://huggingface.co/spaces/freddyaboulton/gradio_leaderboard/blob/main/README.md)
    """)
    Leaderboard(
        value=df,
        select_columns=SelectColumns(
            default_selection=config.ON_LOAD_COLUMNS,
            cant_deselect=["T", "Model"],
            label="Select Columns to Display:",
        ),
        search_columns=["model_name_for_query", "Type"],
        hide_columns=["model_name_for_query", "Model Size"],
        filter_columns=config.FILTER_COLUMNS,
        datatype=config.TYPES,
        column_widths=["2%", "33%"],
    )

if __name__ == "__main__":
    demo.launch()
