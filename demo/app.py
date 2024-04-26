import gradio as gr
from gradio_leaderboard import Leaderboard, SelectColumns, ColumnFilter
import config
from pathlib import Path
import pandas as pd
import random

abs_path = Path(__file__).parent

df = pd.read_json(str(abs_path / "leaderboard_data.json"))
# Randomly set True/ False for the "MOE" column
df["MOE"] = [random.random() > 0.5 for _ in range(len(df))]
df["Flagged"] = [random.random() > 0.5 for _ in range(len(df))]

with gr.Blocks() as demo:
    gr.Markdown("""
    # 🥇 Leaderboard Component
    """)
    with gr.Tabs():
        with gr.Tab("Demo"):
            Leaderboard(
                value=df,
                select_columns=SelectColumns(
                    default_selection=config.ON_LOAD_COLUMNS,
                    cant_deselect=["T", "Model"],
                    label="Select Columns to Display:",
                ),
                search_columns=["model_name_for_query", "Type"],
                hide_columns=["model_name_for_query", "Model Size"],
                filter_columns=[
                    "T",
                    "Precision",
                    ColumnFilter("MOE", type="checkbox", default=False, label="MoE"),
                    ColumnFilter("Flagged", type="checkbox", default=False),
                    ColumnFilter("#Params (B)", default=[30, 80]),
                ],
                datatype=config.TYPES,
                column_widths=["2%", "33%"],
            )
        with gr.Tab("Docs"):
            gr.Markdown((Path(__file__).parent / "docs.md").read_text())

if __name__ == "__main__":
    demo.launch()
