"""gr.Leaderboard() component"""

from __future__ import annotations

import warnings
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    List,
    Optional,
    Tuple,
    Union,
)

import numpy as np
import semantic_version
from gradio_client.documentation import document

from gradio.components import Component
from gradio.data_classes import GradioModel
from gradio.events import Events

if TYPE_CHECKING:
    import pandas as pd
    from pandas.io.formats.style import Styler



class DataframeData(GradioModel):
    headers: List[str]
    data: Union[List[List[Any]], List[Tuple[Any, ...]]]
    metadata: Optional[Dict[str, Optional[List[Any]]]] = None


class Leaderboard(Component):
    """
    This component displays a table of value spreadsheet-like component. Can be used to display data as an output component, or as an input to collect data from the user.
    Demos: filter_records, matrix_transpose, tax_calculator, sort_records
    """

    EVENTS = [Events.change, Events.input, Events.select]

    data_model = DataframeData

    def __init__(
        self,
        value: pd.DataFrame | None = None,
        *,
        datatype: str | list[str] = "str",
        search_column: str | None = None,
        filter_columns: list[str] | None = None,
        hide_columns: list[str] | None = None,
        allow_column_select: bool = True,
        on_load_columns: list[str] | None = None,
        latex_delimiters: list[dict[str, str | bool]] | None = None,
        label: str | None = None,
        show_label: bool | None = None,
        every: float | None = None,
        height: int = 500,
        scale: int | None = None,
        min_width: int = 160,
        interactive: bool | None = None,
        visible: bool = True,
        elem_id: str | None = None,
        elem_classes: list[str] | str | None = None,
        render: bool = True,
        wrap: bool = False,
        line_breaks: bool = True,
        column_widths: list[str | int] | None = None,
    ):
        """
        Parameters:
            value: Default value to display in the DataFrame. If a Styler is provided, it will be used to set the displayed value in the DataFrame (e.g. to set precision of numbers) if the `interactive` is False. If a Callable function is provided, the function will be called whenever the app loads to set the initial value of the component.
            row_count: Limit number of rows for input and decide whether user can create new rows. The first element of the tuple is an `int`, the row count; the second should be 'fixed' or 'dynamic', the new row behaviour. If an `int` is passed the rows default to 'dynamic'
            col_count: Limit number of columns for input and decide whether user can create new columns. The first element of the tuple is an `int`, the number of columns; the second should be 'fixed' or 'dynamic', the new column behaviour. If an `int` is passed the columns default to 'dynamic'
            datatype: Datatype of values in sheet. Can be provided per column as a list of strings, or for the entire sheet as a single string. Valid datatypes are "str", "number", "bool", "date", and "markdown".
            type: Type of value to be returned by component. "pandas" for pandas dataframe, "numpy" for numpy array, "polars" for polars dataframe, or "array" for a Python list of lists.
            label: The label for this component. Appears above the component and is also used as the header if there are a table of examples for this component. If None and used in a `gr.Interface`, the label will be the name of the parameter this component is assigned to.
            latex_delimiters: A list of dicts of the form {"left": open delimiter (str), "right": close delimiter (str), "display": whether to display in newline (bool)} that will be used to render LaTeX expressions. If not provided, `latex_delimiters` is set to `[{ "left": "$$", "right": "$$", "display": True }]`, so only expressions enclosed in $$ delimiters will be rendered as LaTeX, and in a new line. Pass in an empty list to disable LaTeX rendering. For more information, see the [KaTeX documentation](https://katex.org/docs/autorender.html). Only applies to columns whose datatype is "markdown".
            label: The label for this component. Appears above the component and is also used as the header if there are a table of examples for this component. If None and used in a `gr.Interface`, the label will be the name of the parameter this component is assigned to.
            show_label: if True, will display label.
            every: If `value` is a callable, run the function 'every' number of seconds while the client connection is open. Has no effect otherwise. The event can be accessed (e.g. to cancel it) via this component's .load_event attribute.
            height: The maximum height of the dataframe, specified in pixels if a number is passed, or in CSS units if a string is passed. If more rows are created than can fit in the height, a scrollbar will appear.
            scale: relative size compared to adjacent Components. For example if Components A and B are in a Row, and A has scale=2, and B has scale=1, A will be twice as wide as B. Should be an integer. scale applies in Rows, and to top-level Components in Blocks where fill_height=True.
            min_width: minimum pixel width, will wrap if not sufficient screen space to satisfy this value. If a certain scale value results in this Component being narrower than min_width, the min_width parameter will be respected first.
            interactive: if True, will allow users to edit the dataframe; if False, can only be used to display data. If not provided, this is inferred based on whether the component is used as an input or output.
            visible: If False, component will be hidden.
            elem_id: An optional string that is assigned as the id of this component in the HTML DOM. Can be used for targeting CSS styles.
            elem_classes: An optional list of strings that are assigned as the classes of this component in the HTML DOM. Can be used for targeting CSS styles.
            render: If False, component will not render be rendered in the Blocks context. Should be used if the intention is to assign event listeners now but render the component later.
            wrap: If True, the text in table cells will wrap when appropriate. If False and the `column_width` parameter is not set, the column widths will expand based on the cell contents and the table may need to be horizontally scrolled. If `column_width` is set, then any overflow text will be hidden.
            line_breaks: If True (default), will enable Github-flavored Markdown line breaks in chatbot messages. If False, single new lines will be ignored. Only applies for columns of type "markdown."
            column_widths: An optional list representing the width of each column. The elements of the list should be in the format "100px" (ints are also accepted and converted to pixel values) or "10%". If not provided, the column widths will be automatically determined based on the content of the cells. Setting this parameter will cause the browser to try to fit the table within the page width.
        """
        self.wrap = wrap
        self.headers = [str(s) for s in value.columns]
        self.datatype = datatype
        self.search_column = search_column or ""
        self.filter_columns = filter_columns or []
        self.hide_columns = hide_columns or []
        self.on_load_columns = on_load_columns or []
        self.col_count = (len(self.headers), "fixed")
        self.row_count = (value.shape[0], "fixed")
        self.allow_column_select = allow_column_select

        if latex_delimiters is None:
            latex_delimiters = [{"left": "$$", "right": "$$", "display": True}]
        self.latex_delimiters = latex_delimiters
        self.height = height
        self.line_breaks = line_breaks
        self.column_widths = [
            w if isinstance(w, str) else f"{w}px" for w in (column_widths or [])
        ]
        super().__init__(
            label=label,
            every=every,
            show_label=show_label,
            scale=scale,
            min_width=min_width,
            interactive=interactive,
            visible=visible,
            elem_id=elem_id,
            elem_classes=elem_classes,
            render=render,
            value=value,
        )
    
    def get_config(self):
        return {"row_count": self.row_count,
                "col_count": self.col_count,
                "headers": self.headers,
                **super().get_config()
        }

    def preprocess(
        self, payload: DataframeData
    ) -> pd.DataFrame:
        """
        Parameters:
            payload: the uploaded spreadsheet data as an object with `headers` and `data` attributes
        Returns:
            Passes the uploaded spreadsheet data as a `pandas.DataFrame`, `numpy.array`, `polars.DataFrame`, or native 2D Python `list[list]` depending on `type`
        """
        import pandas as pd

        if payload.headers is not None:
            return pd.DataFrame(
                [] if payload.data == [[]] else payload.data,
                columns=payload.headers,
            )
        else:
            return pd.DataFrame(payload.data)

    def postprocess(
        self,
        value: pd.DataFrame
    ) -> DataframeData:
        """
        Parameters:
            value: Expects data any of these formats: `pandas.DataFrame`, `pandas.Styler`, `numpy.array`, `polars.DataFrame`, `list[list]`, `list`, or a `dict` with keys 'data' (and optionally 'headers'), or `str` path to a csv, which is rendered as the spreadsheet.
        Returns:
            the uploaded spreadsheet data as an object with `headers` and `data` attributes
        """
        import pandas as pd
        from pandas.io.formats.style import Styler

        if value is None:
            return self.postprocess(pd.DataFrame({"column 1": []}))
        if isinstance(value, (str, pd.DataFrame)):
            if isinstance(value, str):
                value = pd.read_csv(value)  # type: ignore
            if len(value) == 0:
                return DataframeData(
                    headers=list(value.columns),  # type: ignore
                    data=[[]],  # type: ignore
                )
            return DataframeData(
                headers=list(value.columns),  # type: ignore
                data=value.to_dict(orient="split")["data"],  # type: ignore
            )
        elif isinstance(value, Styler):
            if semantic_version.Version(pd.__version__) < semantic_version.Version(
                "1.5.0"
            ):
                raise ValueError(
                    "Styler objects are only supported in pandas version 1.5.0 or higher. Please try: `pip install --upgrade pandas` to use this feature."
                )
            if self.interactive:
                warnings.warn(
                    "Cannot display Styler object in interactive mode. Will display as a regular pandas dataframe instead."
                )
            df: pd.DataFrame = value.data  # type: ignore
            if len(df) == 0:
                return DataframeData(
                    headers=list(df.columns),
                    data=[[]],
                    metadata=self.__extract_metadata(value),  # type: ignore
                )
            return DataframeData(
                headers=list(df.columns),
                data=df.to_dict(orient="split")["data"],  # type: ignore
                metadata=self.__extract_metadata(value),  # type: ignore
            )

    @staticmethod
    def __get_cell_style(cell_id: str, cell_styles: list[dict]) -> str:
        styles_for_cell = []
        for style in cell_styles:
            if cell_id in style.get("selectors", []):
                styles_for_cell.extend(style.get("props", []))
        styles_str = "; ".join([f"{prop}: {value}" for prop, value in styles_for_cell])
        return styles_str

    @staticmethod
    def __extract_metadata(df: Styler) -> dict[str, list[list]]:
        metadata = {"display_value": [], "styling": []}
        style_data = df._compute()._translate(None, None)  # type: ignore
        cell_styles = style_data.get("cellstyle", [])
        for i in range(len(style_data["body"])):
            metadata["display_value"].append([])
            metadata["styling"].append([])
            for j in range(len(style_data["body"][i])):
                cell_type = style_data["body"][i][j]["type"]
                if cell_type != "td":
                    continue
                display_value = style_data["body"][i][j]["display_value"]
                cell_id = style_data["body"][i][j]["id"]
                styles_str = Leaderboard.__get_cell_style(cell_id, cell_styles)
                metadata["display_value"][i].append(display_value)
                metadata["styling"][i].append(styles_str)
        return metadata

    def process_example(
        self,
        value: pd.DataFrame
        | Styler
        | str
        | None,
    ):
        import pandas as pd

        if value is None:
            return ""
        value_df_data = self.postprocess(value)
        value_df = pd.DataFrame(value_df_data.data, columns=value_df_data.headers)
        return value_df.head(n=5).to_dict(orient="split")["data"]

    def example_payload(self) -> Any:
        return {"headers": ["a", "b"], "data": [["foo", "bar"]]}

    def example_value(self) -> Any:
        return {"headers": ["a", "b"], "data": [["foo", "bar"]]}
