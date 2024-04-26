
# gradio_leaderboard

## 🔋⚡️🥇 Super fast, batteries included Leaderboards with minimal code.
<img alt="Static Badge" src="https://img.shields.io/badge/version%20-%200.0.3%20-%20orange">  


The `gradio_leaderboard` package helps you build fully functional and performant leaderboard demos with `gradio`.

Place the `gradio_leaderboard.Leaderboard` component anywhere in your Gradio application (and optionally pass in some configuration). That's it!

For example usage, please see the [Usage](#usage) section.

For details on configuration, please see the [Configuration](#configuration) section.

For the API reference, see the [Initialization](#initialization) section.

## Installation

```bash
pip install gradio_leaderboard
```

or add `gradio_leaderboard` to your `requirements.txt`.

## Usage

```python

import gradio as gr
from gradio_leaderboard import Leaderboard
from pathlib import Path
import pandas as pd

abs_path = Path(__file__).parent

# Any pandas-compatible data
df = pd.read_json(str(abs_path / "leaderboard_data.json"))

with gr.Blocks() as demo:
    gr.Markdown("""
    # 🥇 Leaderboard Component
    """)
    Leaderboard(
        value=df,
        select_columns=["T", "Model", "Average ⬆️", "ARC",
            "HellaSwag", "MMLU", "TruthfulQA",
            "Winogrande", "GSM8K"],
        search_columns=["model_name_for_query", "Type"],
        hide_columns=["model_name_for_query", "Model Size"],
        filter_columns=["T", "Precision", "Model Size"],
    )

if __name__ == "__main__":
    demo.launch()
```

## Configuration

### Selecting

When column selection is enabled, a checkboxgroup will be displayed in the top left corner of the leaderboard that lets users
select which columns are displayed.

You can disable/configure the column selection behavior of the `Leaderboard` with the `select_columns` parameter.
It's value can be:

* `None`: Column selection is not allowed and all of the columns are displayed when the leaderboard loads.
* `list of column names`: All columns can be selected and the elements of this list correspond to the initial set of selected columns.
* `SelectColumns instance`: You can import `SelectColumns` from `gradio_leaderboard` for full control of the column selection behavior as well as the checkboxgroup appearance. See an example below.

#### Demo

```python
import pandas as pd
import gradio as gr
from gradio_leaderboard import Leaderboard, SelectColumns

with gr.Blocks() as demo:
    Leaderboard(
        value=pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6], "c": [7, 8, 9]}),
        select_columns=SelectColumns(default_selection=["a", "b"],
                                    cant_deselect="a",
                                    label="Select The Columns",
                                    info="Helpful information")
    )

demo.launch()
```

![](https://github.com/freddyaboulton/gradio-leaderboard/assets/41651716/ea073681-c01e-4d40-814c-1f3cd56ef292)


### Searching

When searching is enabled, a textbox will appear in the top left corner of the leaderboard.
Users will be able to display rows that match their search query.

Searching follows the following rules:

1. Multiple queries can be separated by a semicolon `;`.
2. Any subquery is matched against the `primary search column` by default.
3. To match against a `secondary search column`, the query must be preceded by the column name and a colon (`:`), e.g. `Name: Maria`.
4. The returned rows are those that match against `ANY` primary search column and `ALL` secondary search columns.

You can configure searching with the `search_columns` parameter. It's value can be:
* `a list`: In which case the first element is the `primary search column` and the remaining are the `secondary search columns`.
* A `SearchColumns` instance. This lets you specify the primary and secondary columns explicitly as well as customize the search textbox appearance.


#### Demo

```python
import pandas as pd
import gradio as gr
from gradio_leaderboard import Leaderboard, SearchColumns

with gr.Blocks() as demo:
    Leaderboard(
        value=pd.DataFrame({"name": ["Freddy", "Maria", "Mark"], "country": ["USA", "Mexico", "USA"]}),
        search_columns=SearchColumns(primary_column="name", secondary_columns="country",
                                     placeholder="Search by name or country. To search by country, type 'country:<query>'",
                                     label="Search"),
    )

demo.launch()
```

![colum_search_gif](https://github.com/freddyaboulton/gradio-leaderboard/assets/41651716/4725f812-ffca-4ef9-951f-77574accd159)


### Filtering

You can let users filter out rows from the leaderboard with the `filter_columns` parameter.
This will display a series of form elements that users can use to select/deselect which rows are displayed.

This parameter must be a `list` but it's elements must be:

* `a string`: Corresponding to the column name you'd like to add a filter for
* `a ColumnFilter`: A special class for full control of the filter's type, e.g. `checkboxgroup`, `boolean`, `slider`, or `dropdown`, as well as it's appearance in the UI.

If the `type` of the `ColumnFilter` is not specified, a heuristic will be used to choose the most appropriate type. If the data in the column is boolean-valued, a `boolean` type will be used. If it is numeric, a slider will be used. For all others, a `checkboxgroup` will be used.

All `ColumnFilters` of type `boolean` will be displayed together in a checkbox group. When a `checkbox` in that group is selected, only those rows that have a true value for that column will be displayed. When it is deselected, the table will not be filtered by that column.
You can add a label to the `boolean` `checkboxgroup` with the `bool_checkboxgroup_label` parameter. 


#### Demo 

```python
import pandas as pd
import gradio as gr
from gradio_leaderboard import Leaderboard, ColumnFilter

with gr.Blocks() as demo:
    Leaderboard(
        value=pd.DataFrame({"name": ["Freddy", "Maria", "Mark"], "country": ["USA", "Mexico", "USA"],
                            "age": [25, 30, 35], "score": [100, 200, 300],
                            "registered": [True, False, True]}),
        filter_columns=[
            "name",
            ColumnFilter("country", type="dropdown", label="Select Country 🇺🇸🇲🇽"),
            ColumnFilter("age", type="slider", min=20, max=40),
            ColumnFilter("score", type="slider", min=50, max=350),
            "registered"],
        bool_checkboxgroup_label="Only show registered"
    )

demo.launch()
```

![filter_columns_gif](https://github.com/freddyaboulton/gradio-leaderboard/assets/41651716/07dc39a5-687c-414b-b96e-777fd01ebe00)


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
<td align="left"><code>search_columns</code></td>
<td align="left" style="width: 25%;">

```python
list[str] | SearchColumns
```

</td>
<td align="left"><code>None</code></td>
<td align="left">See Configuration section of docs for details.</td>
</tr>

<tr>
<td align="left"><code>select_columns</code></td>
<td align="left" style="width: 25%;">

```python
list[str] | SelectColumns
```

</td>
<td align="left"><code>None</code></td>
<td align="left">See Configuration section of docs for details.</td>
</tr>

<tr>
<td align="left"><code>filter_columns</code></td>
<td align="left" style="width: 25%;">

```python
list[str | ColumnFilter] | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">See Configuration section of docs for details.</td>
</tr>

<tr>
<td align="left"><code>bool_checkboxgroup_label</code></td>
<td align="left" style="width: 25%;">

```python
str | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">Label for the checkboxgroup filter for boolean columns.</td>
</tr>

<tr>
<td align="left"><code>hide_columns</code></td>
<td align="left" style="width: 25%;">

```python
list[str] | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">List of columns to hide by default. They will not be displayed in the table but they can still be used for searching, filtering.</td>
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