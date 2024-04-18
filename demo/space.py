import gradio as gr
from app import demo as app
import os

_docs = {
    "Leaderboard": {
        "description": "This component displays a table of value spreadsheet-like component. Can be used to display data as an output component, or as an input to collect data from the user.",
        "members": {
            "__init__": {
                "value": {
                    "type": "pd.DataFrame | None",
                    "default": "None",
                    "description": "Default value to display in the DataFrame. If a Styler is provided, it will be used to set the displayed value in the DataFrame (e.g. to set precision of numbers) if the `interactive` is False. If a Callable function is provided, the function will be called whenever the app loads to set the initial value of the component.",
                },
                "datatype": {
                    "type": "str | list[str]",
                    "default": '"str"',
                    "description": 'Datatype of values in sheet. Can be provided per column as a list of strings, or for the entire sheet as a single string. Valid datatypes are "str", "number", "bool", "date", and "markdown".',
                },
                "search_column": {
                    "type": "str | None",
                    "default": "None",
                    "description": None,
                },
                "filter_columns": {
                    "type": "list[str] | None",
                    "default": "None",
                    "description": None,
                },
                "hide_columns": {
                    "type": "list[str] | None",
                    "default": "None",
                    "description": None,
                },
                "allow_column_select": {
                    "type": "bool",
                    "default": "True",
                    "description": None,
                },
                "on_load_columns": {
                    "type": "list[str] | None",
                    "default": "None",
                    "description": None,
                },
                "latex_delimiters": {
                    "type": "list[dict[str, str | bool]] | None",
                    "default": "None",
                    "description": 'A list of dicts of the form {"left": open delimiter (str), "right": close delimiter (str), "display": whether to display in newline (bool)} that will be used to render LaTeX expressions. If not provided, `latex_delimiters` is set to `[{ "left": "$$", "right": "$$", "display": True }]`, so only expressions enclosed in $$ delimiters will be rendered as LaTeX, and in a new line. Pass in an empty list to disable LaTeX rendering. For more information, see the [KaTeX documentation](https://katex.org/docs/autorender.html). Only applies to columns whose datatype is "markdown".',
                },
                "label": {
                    "type": "str | None",
                    "default": "None",
                    "description": "The label for this component. Appears above the component and is also used as the header if there are a table of examples for this component. If None and used in a `gr.Interface`, the label will be the name of the parameter this component is assigned to.",
                },
                "show_label": {
                    "type": "bool | None",
                    "default": "None",
                    "description": "if True, will display label.",
                },
                "every": {
                    "type": "float | None",
                    "default": "None",
                    "description": "If `value` is a callable, run the function 'every' number of seconds while the client connection is open. Has no effect otherwise. The event can be accessed (e.g. to cancel it) via this component's .load_event attribute.",
                },
                "height": {
                    "type": "int",
                    "default": "500",
                    "description": "The maximum height of the dataframe, specified in pixels if a number is passed, or in CSS units if a string is passed. If more rows are created than can fit in the height, a scrollbar will appear.",
                },
                "scale": {
                    "type": "int | None",
                    "default": "None",
                    "description": "relative size compared to adjacent Components. For example if Components A and B are in a Row, and A has scale=2, and B has scale=1, A will be twice as wide as B. Should be an integer. scale applies in Rows, and to top-level Components in Blocks where fill_height=True.",
                },
                "min_width": {
                    "type": "int",
                    "default": "160",
                    "description": "minimum pixel width, will wrap if not sufficient screen space to satisfy this value. If a certain scale value results in this Component being narrower than min_width, the min_width parameter will be respected first.",
                },
                "interactive": {
                    "type": "bool | None",
                    "default": "None",
                    "description": "if True, will allow users to edit the dataframe; if False, can only be used to display data. If not provided, this is inferred based on whether the component is used as an input or output.",
                },
                "visible": {
                    "type": "bool",
                    "default": "True",
                    "description": "If False, component will be hidden.",
                },
                "elem_id": {
                    "type": "str | None",
                    "default": "None",
                    "description": "An optional string that is assigned as the id of this component in the HTML DOM. Can be used for targeting CSS styles.",
                },
                "elem_classes": {
                    "type": "list[str] | str | None",
                    "default": "None",
                    "description": "An optional list of strings that are assigned as the classes of this component in the HTML DOM. Can be used for targeting CSS styles.",
                },
                "render": {
                    "type": "bool",
                    "default": "True",
                    "description": "If False, component will not render be rendered in the Blocks context. Should be used if the intention is to assign event listeners now but render the component later.",
                },
                "wrap": {
                    "type": "bool",
                    "default": "False",
                    "description": "If True, the text in table cells will wrap when appropriate. If False and the `column_width` parameter is not set, the column widths will expand based on the cell contents and the table may need to be horizontally scrolled. If `column_width` is set, then any overflow text will be hidden.",
                },
                "line_breaks": {
                    "type": "bool",
                    "default": "True",
                    "description": 'If True (default), will enable Github-flavored Markdown line breaks in chatbot messages. If False, single new lines will be ignored. Only applies for columns of type "markdown."',
                },
                "column_widths": {
                    "type": "list[str | int] | None",
                    "default": "None",
                    "description": 'An optional list representing the width of each column. The elements of the list should be in the format "100px" (ints are also accepted and converted to pixel values) or "10%". If not provided, the column widths will be automatically determined based on the content of the cells. Setting this parameter will cause the browser to try to fit the table within the page width.',
                },
            },
            "postprocess": {
                "value": {
                    "type": "pd.DataFrame",
                    "description": "Expects data any of these formats: `pandas.DataFrame`, `pandas.Styler`, `numpy.array`, `polars.DataFrame`, `list[list]`, `list`, or a `dict` with keys 'data' (and optionally 'headers'), or `str` path to a csv, which is rendered as the spreadsheet.",
                }
            },
            "preprocess": {
                "return": {
                    "type": "pd.DataFrame",
                    "description": "Passes the uploaded spreadsheet data as a `pandas.DataFrame`, `numpy.array`, `polars.DataFrame`, or native 2D Python `list[list]` depending on `type`",
                },
                "value": None,
            },
        },
        "events": {
            "change": {
                "type": None,
                "default": None,
                "description": "Triggered when the value of the Leaderboard changes either because of user input (e.g. a user types in a textbox) OR because of a function update (e.g. an image receives a value from the output of an event trigger). See `.input()` for a listener that is only triggered by user input.",
            },
            "input": {
                "type": None,
                "default": None,
                "description": "This listener is triggered when the user changes the value of the Leaderboard.",
            },
            "select": {
                "type": None,
                "default": None,
                "description": "Event listener for when the user selects or deselects the Leaderboard. Uses event data gradio.SelectData to carry `value` referring to the label of the Leaderboard, and `selected` to refer to state of the Leaderboard. See EventData documentation on how to use this event data",
            },
        },
    },
    "__meta__": {"additional_interfaces": {}, "user_fn_refs": {"Leaderboard": []}},
}

abs_path = os.path.join(os.path.dirname(__file__), "css.css")

with gr.Blocks(
    css=abs_path,
    theme=gr.themes.Default(
        font_mono=[
            gr.themes.GoogleFont("Inconsolata"),
            "monospace",
        ],
    ),
) as demo:
    gr.Markdown(
        """
# `gradio_leaderboard`

<div style="display: flex; gap: 7px;">
<img alt="Static Badge" src="https://img.shields.io/badge/version%20-%200.0.1%20-%20orange">  
</div>

Super fast , batteries included Leaderboard component ⚡️
""",
        elem_classes=["md-custom"],
        header_links=True,
    )
    app.render()
    gr.Markdown(
        """
## Installation

```bash
pip install gradio_leaderboard
```

## Usage

```python

import gradio as gr
from gradio_leaderboard import Leaderboard
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
df["Model Size"] = params_column.apply(lambda x: next(s for s in numeric_interval if x in s))


with gr.Blocks() as demo:
    gr.Markdown(\"\"\"
    # 🥇 Leaderboard Component
    \"\"\")
    Leaderboard(value=df,
                allow_column_select=True,
                on_load_columns=config.ON_LOAD_COLUMNS,
                search_column="model_name_for_query",
                hide_columns=["model_name_for_query", "Model Size"],
                filter_columns=config.FILTER_COLUMNS,
                datatype=config.TYPES,
                column_widths=["2%", "33%"])

if __name__ == "__main__":
    demo.launch()

```
""",
        elem_classes=["md-custom"],
        header_links=True,
    )

    gr.Markdown(
        """
## `Leaderboard`

### Initialization
""",
        elem_classes=["md-custom"],
        header_links=True,
    )

    gr.ParamViewer(value=_docs["Leaderboard"]["members"]["__init__"], linkify=[])

    gr.Markdown("### Events")
    gr.ParamViewer(value=_docs["Leaderboard"]["events"], linkify=["Event"])

    gr.Markdown(
        """

### User function

The impact on the users predict function varies depending on whether the component is used as an input or output for an event (or both).

- When used as an Input, the component only impacts the input signature of the user function.
- When used as an output, the component only impacts the return signature of the user function.

The code snippet below is accurate in cases where the component is used as both an input and an output.

- **As input:** Is passed, passes the uploaded spreadsheet data as a `pandas.DataFrame`, `numpy.array`, `polars.DataFrame`, or native 2D Python `list[list]` depending on `type`.
- **As output:** Should return, expects data any of these formats: `pandas.DataFrame`, `pandas.Styler`, `numpy.array`, `polars.DataFrame`, `list[list]`, `list`, or a `dict` with keys 'data' (and optionally 'headers'), or `str` path to a csv, which is rendered as the spreadsheet.

 ```python
def predict(
    value: pd.DataFrame
) -> pd.DataFrame:
    return value
```
""",
        elem_classes=["md-custom", "Leaderboard-user-fn"],
        header_links=True,
    )

    demo.load(
        None,
        js=r"""function() {
    const refs = {};
    const user_fn_refs = {
          Leaderboard: [], };
    requestAnimationFrame(() => {

        Object.entries(user_fn_refs).forEach(([key, refs]) => {
            if (refs.length > 0) {
                const el = document.querySelector(`.${key}-user-fn`);
                if (!el) return;
                refs.forEach(ref => {
                    el.innerHTML = el.innerHTML.replace(
                        new RegExp("\\b"+ref+"\\b", "g"),
                        `<a href="#h-${ref.toLowerCase()}">${ref}</a>`
                    );
                })
            }
        })

        Object.entries(refs).forEach(([key, refs]) => {
            if (refs.length > 0) {
                const el = document.querySelector(`.${key}`);
                if (!el) return;
                refs.forEach(ref => {
                    el.innerHTML = el.innerHTML.replace(
                        new RegExp("\\b"+ref+"\\b", "g"),
                        `<a href="#h-${ref.toLowerCase()}">${ref}</a>`
                    );
                })
            }
        })
    })
}

""",
    )

demo.launch()
