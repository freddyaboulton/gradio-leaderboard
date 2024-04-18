
# `gradio_leaderboard`
<img alt="Static Badge" src="https://img.shields.io/badge/version%20-%200.0.1%20-%20orange">  

Super fast , batteries included Leaderboard component ⚡️

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
    gr.Markdown("""
    # 🥇 Leaderboard Component
    """)
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

## `Leaderboard`

### Initialization

<table>
<thead>
<tr>
<th align="left">name</th>
<th align="left" style="width: 25%;">type</th>
<th align="left">default</th>
<th align="left">description</th>
</tr>
</thead>
<tbody>
<tr>
<td align="left"><code>value</code></td>
<td align="left" style="width: 25%;">

```python
pd.DataFrame | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">Default value to display in the DataFrame. If a Styler is provided, it will be used to set the displayed value in the DataFrame (e.g. to set precision of numbers) if the `interactive` is False. If a Callable function is provided, the function will be called whenever the app loads to set the initial value of the component.</td>
</tr>

<tr>
<td align="left"><code>datatype</code></td>
<td align="left" style="width: 25%;">

```python
str | list[str]
```

</td>
<td align="left"><code>"str"</code></td>
<td align="left">Datatype of values in sheet. Can be provided per column as a list of strings, or for the entire sheet as a single string. Valid datatypes are "str", "number", "bool", "date", and "markdown".</td>
</tr>

<tr>
<td align="left"><code>search_column</code></td>
<td align="left" style="width: 25%;">

```python
str | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">None</td>
</tr>

<tr>
<td align="left"><code>filter_columns</code></td>
<td align="left" style="width: 25%;">

```python
list[str] | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">None</td>
</tr>

<tr>
<td align="left"><code>hide_columns</code></td>
<td align="left" style="width: 25%;">

```python
list[str] | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">None</td>
</tr>

<tr>
<td align="left"><code>allow_column_select</code></td>
<td align="left" style="width: 25%;">

```python
bool
```

</td>
<td align="left"><code>True</code></td>
<td align="left">None</td>
</tr>

<tr>
<td align="left"><code>on_load_columns</code></td>
<td align="left" style="width: 25%;">

```python
list[str] | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">None</td>
</tr>

<tr>
<td align="left"><code>latex_delimiters</code></td>
<td align="left" style="width: 25%;">

```python
list[dict[str, str | bool]] | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">A list of dicts of the form {"left": open delimiter (str), "right": close delimiter (str), "display": whether to display in newline (bool)} that will be used to render LaTeX expressions. If not provided, `latex_delimiters` is set to `[{ "left": "$$", "right": "$$", "display": True }]`, so only expressions enclosed in $$ delimiters will be rendered as LaTeX, and in a new line. Pass in an empty list to disable LaTeX rendering. For more information, see the [KaTeX documentation](https://katex.org/docs/autorender.html). Only applies to columns whose datatype is "markdown".</td>
</tr>

<tr>
<td align="left"><code>label</code></td>
<td align="left" style="width: 25%;">

```python
str | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">The label for this component. Appears above the component and is also used as the header if there are a table of examples for this component. If None and used in a `gr.Interface`, the label will be the name of the parameter this component is assigned to.</td>
</tr>

<tr>
<td align="left"><code>show_label</code></td>
<td align="left" style="width: 25%;">

```python
bool | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">if True, will display label.</td>
</tr>

<tr>
<td align="left"><code>every</code></td>
<td align="left" style="width: 25%;">

```python
float | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">If `value` is a callable, run the function 'every' number of seconds while the client connection is open. Has no effect otherwise. The event can be accessed (e.g. to cancel it) via this component's .load_event attribute.</td>
</tr>

<tr>
<td align="left"><code>height</code></td>
<td align="left" style="width: 25%;">

```python
int
```

</td>
<td align="left"><code>500</code></td>
<td align="left">The maximum height of the dataframe, specified in pixels if a number is passed, or in CSS units if a string is passed. If more rows are created than can fit in the height, a scrollbar will appear.</td>
</tr>

<tr>
<td align="left"><code>scale</code></td>
<td align="left" style="width: 25%;">

```python
int | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">relative size compared to adjacent Components. For example if Components A and B are in a Row, and A has scale=2, and B has scale=1, A will be twice as wide as B. Should be an integer. scale applies in Rows, and to top-level Components in Blocks where fill_height=True.</td>
</tr>

<tr>
<td align="left"><code>min_width</code></td>
<td align="left" style="width: 25%;">

```python
int
```

</td>
<td align="left"><code>160</code></td>
<td align="left">minimum pixel width, will wrap if not sufficient screen space to satisfy this value. If a certain scale value results in this Component being narrower than min_width, the min_width parameter will be respected first.</td>
</tr>

<tr>
<td align="left"><code>interactive</code></td>
<td align="left" style="width: 25%;">

```python
bool | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">if True, will allow users to edit the dataframe; if False, can only be used to display data. If not provided, this is inferred based on whether the component is used as an input or output.</td>
</tr>

<tr>
<td align="left"><code>visible</code></td>
<td align="left" style="width: 25%;">

```python
bool
```

</td>
<td align="left"><code>True</code></td>
<td align="left">If False, component will be hidden.</td>
</tr>

<tr>
<td align="left"><code>elem_id</code></td>
<td align="left" style="width: 25%;">

```python
str | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">An optional string that is assigned as the id of this component in the HTML DOM. Can be used for targeting CSS styles.</td>
</tr>

<tr>
<td align="left"><code>elem_classes</code></td>
<td align="left" style="width: 25%;">

```python
list[str] | str | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">An optional list of strings that are assigned as the classes of this component in the HTML DOM. Can be used for targeting CSS styles.</td>
</tr>

<tr>
<td align="left"><code>render</code></td>
<td align="left" style="width: 25%;">

```python
bool
```

</td>
<td align="left"><code>True</code></td>
<td align="left">If False, component will not render be rendered in the Blocks context. Should be used if the intention is to assign event listeners now but render the component later.</td>
</tr>

<tr>
<td align="left"><code>wrap</code></td>
<td align="left" style="width: 25%;">

```python
bool
```

</td>
<td align="left"><code>False</code></td>
<td align="left">If True, the text in table cells will wrap when appropriate. If False and the `column_width` parameter is not set, the column widths will expand based on the cell contents and the table may need to be horizontally scrolled. If `column_width` is set, then any overflow text will be hidden.</td>
</tr>

<tr>
<td align="left"><code>line_breaks</code></td>
<td align="left" style="width: 25%;">

```python
bool
```

</td>
<td align="left"><code>True</code></td>
<td align="left">If True (default), will enable Github-flavored Markdown line breaks in chatbot messages. If False, single new lines will be ignored. Only applies for columns of type "markdown."</td>
</tr>

<tr>
<td align="left"><code>column_widths</code></td>
<td align="left" style="width: 25%;">

```python
list[str | int] | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">An optional list representing the width of each column. The elements of the list should be in the format "100px" (ints are also accepted and converted to pixel values) or "10%". If not provided, the column widths will be automatically determined based on the content of the cells. Setting this parameter will cause the browser to try to fit the table within the page width.</td>
</tr>
</tbody></table>


### Events

| name | description |
|:-----|:------------|
| `change` | Triggered when the value of the Leaderboard changes either because of user input (e.g. a user types in a textbox) OR because of a function update (e.g. an image receives a value from the output of an event trigger). See `.input()` for a listener that is only triggered by user input. |
| `input` | This listener is triggered when the user changes the value of the Leaderboard. |
| `select` | Event listener for when the user selects or deselects the Leaderboard. Uses event data gradio.SelectData to carry `value` referring to the label of the Leaderboard, and `selected` to refer to state of the Leaderboard. See EventData documentation on how to use this event data |



### User function

The impact on the users predict function varies depending on whether the component is used as an input or output for an event (or both).

- When used as an Input, the component only impacts the input signature of the user function.
- When used as an output, the component only impacts the return signature of the user function.

The code snippet below is accurate in cases where the component is used as both an input and an output.

- **As output:** Is passed, passes the uploaded spreadsheet data as a `pandas.DataFrame`, `numpy.array`, `polars.DataFrame`, or native 2D Python `list[list]` depending on `type`.
- **As input:** Should return, expects data any of these formats: `pandas.DataFrame`, `pandas.Styler`, `numpy.array`, `polars.DataFrame`, `list[list]`, `list`, or a `dict` with keys 'data' (and optionally 'headers'), or `str` path to a csv, which is rendered as the spreadsheet.

 ```python
 def predict(
     value: pd.DataFrame
 ) -> pd.DataFrame:
     return value
 ```
 
