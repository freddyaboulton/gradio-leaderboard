<script lang="ts">
	import { afterUpdate, tick } from "svelte";
	import type { Gradio, SelectData } from "@gradio/utils";
	import { Block } from "@gradio/atoms";
	import Table from "./shared/Table.svelte";
	import { StatusTracker } from "@gradio/statustracker";
	import type { LoadingStatus } from "@gradio/statustracker";
	import Form from "@gradio/form";
	import type { Headers, Data, Metadata, Datatype, SearchColumns,
		SelectColumns, FilterColumns, ColumnFilter } from "./shared/utils";
	import Row from "@gradio/row";
	import Column from "@gradio/column";
	import Checkboxgroup from "./shared/Checkboxgroup.svelte";
	import Simpletextbox from "./shared/SimpleTextbox.svelte";
	import { BaseMultiselect } from "@gradio/dropdown";
    import RangeSlider from "./shared/RangeSlider.svelte";

	export let headers: Headers = [];
	export let elem_id = "";
	export let elem_classes: string[] = [];
	export let visible = true;
	export let value: { data: Data; headers: Headers; metadata: Metadata } = {
		data: [["", "", ""]],
		headers: ["1", "2", "3"],
		metadata: null
	};
	export let bool_checkboxgroup_label: string | null = null;
	let old_value = "";
	export let value_is_output = false;
	export let col_count: [number, "fixed" | "dynamic"];
	export let label: string | null = null;
	export let show_label = true;
	export let wrap: boolean;
	export let datatype: Datatype | Datatype[];
	export let scale: number | null = null;
	export let min_width: number | undefined = undefined;
	export let root: string;
	export let filter_columns: FilterColumns = [];
	export let select_columns_config: SelectColumns;
	export let hide_columns: string[];
	export let search_columns: SearchColumns | null = null;

	export let line_breaks = true;
	export let column_widths: string[] = [];
	export let gradio: Gradio<{
		change: never;
		select: SelectData;
		input: never;
		submit: string;
		warning: string;
	}>;
	export let latex_delimiters: {
		left: string;
		right: string;
		display: boolean;
	}[];
	export let height: number | undefined = undefined;

	export let loading_status: LoadingStatus;
	export let interactive: boolean;

	let _headers: Headers;
	let original_headers = value.headers.map(s => s);
	let original_data = value.data.map(s => s);
	let display_value: string[][] | null;
	let styling: string[][] | null;
	let values: (string | number)[][];
	let filter_values: [string,  number][] = [];
	let search_value: string | null = null;
	let default_selection = select_columns_config.default_selection.length ? select_columns_config.default_selection : original_headers;

	async function handle_change(data?: {
		data: Data;
		headers: Headers;
		metadata: Metadata;
	}): Promise<void> {
		let _data = data || value;

		_headers = original_headers;
		values = original_data ? [...original_data] : [];
		const display_headers = _headers.filter(h => default_selection.includes(h));
		const display_indices = display_headers.map(name => _headers.indexOf(name));
		_headers = display_headers;
		values = values.map(row => display_indices.map(i => row[i]));
		display_value = _data?.metadata?.display_value
			? [..._data?.metadata?.display_value]
			: null;
		styling = _data?.metadata?.styling ? [..._data?.metadata?.styling] : null;
		await tick();

		gradio.dispatch("change");
		if (!value_is_output) {
			gradio.dispatch("input");
		}
	}

	function select_columns(values, on_load_columns){
		const display_headers = original_headers.filter(h => on_load_columns.includes(h));
		const display_indices = display_headers.map(name => original_headers.indexOf(name));
		_headers = display_headers;
		values = values.map(row => display_indices.map(i => row[i]));
		return values;
	}

	function compare(val, min, max) {
		return val >= min && val <= max;
	}

 	function filter_column(column: ColumnFilter, value: any[] | any){
		if (column.type === "checkbox" && !value) {
			return Array(original_data.length).fill(true);
		}
		values = original_data;
		if (Array.isArray(value) && !value.length) {
			return Array(values.length).fill(false);
		}
		let filter
		if (column.type === "slider") {
			const [min, max] = value;
			filter = (row) => {
				return compare(row[original_headers.indexOf(column.column)], min, max);
			}
		} else if (column.type == "checkbox") {
			filter = (row) => {
				return row[original_headers.indexOf(column.column)] === value;
			}
		} else {
			filter = (row) => {
				return value.some(v => row[original_headers.indexOf(column.column)] === v);
			}
		}
		return values.map(filter);
	}

	function search_column_values(values, headers, search_columns: SearchColumns, search_value) {
		if (!search_value) {
			return new Array(values.length).fill(true);
		}
		const query_values = search_value.split(';').map(s => s.trim()).filter(s => s.length);
		const mask = new Array(values.length).fill(false);
		let triggered_warning = false

		for (let i = 0; i < values.length; i++) {
			let primary_column_matches = Array();
			let secondary_column_matches = Array();
			for (let j = 0; j < query_values.length; j++) {
				
				let query_value = query_values[j];
				let column_index = headers.indexOf(search_columns.primary_column);

				// Check if the query value is column-specific
				const colon_index = query_value.indexOf(':');
				if (colon_index !== -1) {
					const col_name = query_value.substring(0, colon_index);
					if (!search_columns.secondary_columns.length || !search_columns.secondary_columns.includes(col_name)) {
						if (! triggered_warning)
							gradio.dispatch("warning", `Column ${col_name} not found in secondary columns of search_columns`);
						triggered_warning = true;
						continue;
					}

					const col_index = headers.indexOf(col_name);
					if (col_index !== -1) {
						column_index = col_index;
						query_value = query_value.substring(colon_index + 1).trim();
					}
				}

				const push_to = colon_index !== -1 ? secondary_column_matches : primary_column_matches;

				if (values[i][column_index].toString().toLowerCase().includes(query_value.toLowerCase())) {
					push_to.push(true);
				} else {
					push_to.push(false);
				}
			}
			if (primary_column_matches.length && !secondary_column_matches.length){
				mask[i] = primary_column_matches.some(s => s);
			} else if (secondary_column_matches.length && !primary_column_matches.length){
				mask[i] = secondary_column_matches.every(s => Boolean(s));
			} else if (primary_column_matches.length && secondary_column_matches.length){
				mask[i] = primary_column_matches.some(s => s) && secondary_column_matches.every(s => Boolean(s));
			}
		}
  		return mask;
	}

	function get_column_filter(column: string){
		return filter_columns.find(f => f.column === column);
	}

	function filter_column_values(values, headers, filter_values: [string, any][], search_columns, search_value){
		console.log("filter_values", filter_values);
		const search_value_mask = search_column_values(original_data, headers, search_columns, search_value);
		const masks = filter_values.map((tup) => filter_column(get_column_filter(tup[0]), tup[1])).concat([search_value_mask]);
		return values.filter((row, i) => masks.every(mask => mask[i]));
	}

	function update_data(_on_load_columns, filter_values, search_value){
		values = select_columns(original_data, _on_load_columns);
		values = filter_column_values(values, original_headers, filter_values, search_columns, search_value);
		if (values.length === 0) {
			values =  [Array(_on_load_columns.length).fill("")];
		}
	}

	$: update_data(default_selection, filter_values, search_value);

	handle_change();

	afterUpdate(() => {
		value_is_output = false;
	});

	$: {
		if (old_value && JSON.stringify(value) !== old_value) {
			old_value = JSON.stringify(value);
			handle_change();
		}
	}

	if (
		(Array.isArray(value) && value?.[0]?.length === 0) ||
		value.data?.[0]?.length === 0
	) {
		value = {
			data: [Array(col_count?.[0] || 3).fill("")],
			headers: Array(col_count?.[0] || 3)
				.fill("")
				.map((_, i) => `${i + 1}`),
			metadata: null
		};
	}

	const non_checkbox_filter_columns = filter_columns.filter(col => col.type !== "checkbox");
	const checkbox_filter_columns = filter_columns.filter(col => col.type === "checkbox");
	checkbox_filter_columns.forEach((col, i) => {
		if (col.default) {
			filter_values[non_checkbox_filter_columns.length + i] = [col.column, col.default];
		}
	});

</script>

<Row>
	<Column>
		{#if search_columns.primary_column}
			<Row>
				<Simpletextbox
					label={search_columns.label ?? "Search"}
					show_label={true}
					placeholder={search_columns.placeholder ?? "Separate multiple queries with ';'."}
					interactive={true}
					{gradio}
					on:submit={(e) => search_value = e.detail}
				/>
			</Row>
		{/if}
		{#if select_columns_config.allow}
			<Row>
				<Checkboxgroup
					label={select_columns_config.label || "Select Columns to Show"}
					show_label={select_columns_config.show_label}
					info={select_columns_config.info}
					{gradio}
					bind:value={default_selection}
					choices={headers.filter(s => !(hide_columns.includes(s) || select_columns_config.cant_deselect.includes(s))).map(s => [s, s])}
					{loading_status}
				/>
			</Row>
		{/if}
	</Column>
	<Column>
		<Form>
			{#each non_checkbox_filter_columns as col, i}
				{#if col.type === "checkboxgroup"}
					<Checkboxgroup
						label={col.label || `Filter ${col.column}`}
						{gradio}
						{loading_status}
						choices={col.choices}
						value={col.default.map((s, i) => s[0])}
						info={col.info}
						show_label={col.show_label}
						on:input={(e) => filter_values[i] = [col.column, e.detail]}
					/>
				{:else if col.type == "dropdown"}
					<Block>
						<BaseMultiselect 
						label={col.label || `Filter ${col.column}`}
						info={col.info}
						value={col.default.map((s, i) => s[0])}
						choices={col.choices}
						show_label={col.show_label}
						i18n={gradio.i18n}
						container={true}
						on:change={(e) => filter_values[i] = [col.column, e.detail]}
						/>
					</Block>
				{:else}
					<RangeSlider
						label={col.label || `Filter ${col.column}`}
						show_label={col.show_label}
						min={col.min}
						max={col.max}
						selected_min={col.default[0]}
						selected_max={col.default[1]}
						on:change={(e) => filter_values[i] = [col.column, e.detail]}
					/>
				{/if}
			{/each}
			<Checkboxgroup
				label={bool_checkboxgroup_label || "Show Rows with the Following Values"}
				show_label={true}
				{gradio}
				{loading_status}
				choices={checkbox_filter_columns.map(col => [col.label ?? col.column, col.column])}
				value={checkbox_filter_columns.map(col => col.default ? col.column : null).filter(s => s)}
				on:input={(e) => {
					checkbox_filter_columns.forEach((col, i) => {
						filter_values[non_checkbox_filter_columns.length + i] = [col.column, e.detail.includes(col.column)]
					});
				}}
			/>
		</Form>
	</Column>
</Row>
<!-- insert empty space below -->
<Block height="20px" container={false}/>
<Row>
	<StatusTracker
	autoscroll={gradio.autoscroll}
	i18n={gradio.i18n}
	{...loading_status}
/>
	<Table
		{root}
		{label}
		{show_label}
		row_count={[values.length, "fixed"]}
		col_count={[_headers.length, "fixed"]}
		{values}
		{display_value}
		{styling}
		headers={_headers}
		on:select={(e) => gradio.dispatch("select", e.detail)}
		{wrap}
		{datatype}
		{latex_delimiters}
		editable={interactive}
		{height}
		i18n={gradio.i18n}
		{line_breaks}
		{column_widths}
		{hide_columns}
	/>
</Row>