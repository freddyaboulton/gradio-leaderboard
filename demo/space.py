import pandas as pd
import gradio as gr
from gradio_leaderboard import Leaderboard, ColumnFilter

with gr.Blocks() as demo:
    Leaderboard(
        value=pd.DataFrame(
            {
                "name": ["Freddy", "Maria", "Mark"],
                "country": ["USA", "Mexico", "USA"],
                "age": [25, 30, 35],
                "score": [100, 200, 300],
                "registered": [True, False, True],
            }
        ),
        filter_columns=[
            "name",
            ColumnFilter("country", type="dropdown", label="Select Country 🇺🇸🇲🇽"),
            ColumnFilter("age", type="slider", min=20, max=40, default=[25, 35]),
            ColumnFilter("score", type="slider", min=50, max=350, default=[100, 300]),
            "registered",
        ],
        bool_checkboxgroup_label="Only show registered",
    )

demo.launch()
