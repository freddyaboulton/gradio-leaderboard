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

df = pd.DataFrame({"A" : [14, 4, 5, 4, 1], 
				"B" : [5, 2, 54, 3, 2], 
				"C" : [20, 20, 7, 3, 8], 
				"D" : [14, 3, 6, 2, 6], 
				"E" : [23, 45, 64, 32, 23]}) 

t = df.style.highlight_max(color = 'lightgreen', axis = 0)

with gr.Blocks() as demo:
    gr.Markdown("""
    # 🥇 Leaderboard Component
    Please read the documentation [here](https://huggingface.co/spaces/freddyaboulton/gradio_leaderboard/blob/main/README.md)
    """)
    Leaderboard(
        value=t,
        select_columns=SelectColumns(
            default_selection=["A", "B", "C"],
        ),
        filter_columns=["D", "E"],
    )

if __name__ == "__main__":
    demo.launch()
