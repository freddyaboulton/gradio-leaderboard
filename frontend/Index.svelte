<script context="module" lang="ts">
	export { default as BaseDataFrame } from "./shared/Table.svelte";
	export { default as BaseExample } from "./Example.svelte";
</script>

<script lang="ts">
	import { afterUpdate, tick } from "svelte";
	import type { Gradio, SelectData } from "@gradio/utils";
	import { Block } from "@gradio/atoms";
	import Table from "./shared/Table.svelte";
	import { StatusTracker } from "@gradio/statustracker";
	import type { LoadingStatus } from "@gradio/statustracker";
	import type { Headers, Data, Metadata, Datatype } from "./shared/utils";
	import Row from "@gradio/row";
	import Column from "@gradio/column";
	import Checkboxgroup from "./shared/Checkboxgroup.svelte";
	import Simpletextbox from "./shared/SimpleTextbox.svelte";
	import Group from "@gradio/group";
	export let headers: Headers = [];
	export let elem_id = "";
	export let elem_classes: string[] = [];
	export let visible = true;
	export let value: { data: Data; headers: Headers; metadata: Metadata } = {
		data: [["", "", ""]],
		headers: ["1", "2", "3"],
		metadata: null
	};
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
	export let filter_columns: string[] = [];
	export let on_load_columns: string[] | [];
	export let hide_columns: string[] | [];
	export let search_column: string | null = null;
	export let allow_column_select: boolean;

	export let line_breaks = true;
	export let column_widths: string[] = [];
	export let gradio: Gradio<{
		change: never;
		select: SelectData;
		input: never;
		submit: string;
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
	let search_column_data = value.data.map(s => s[value.headers.indexOf(search_column)]);
	let original_data = value.data.map(s => s);
	let display_value: string[][] | null;
	let styling: string[][] | null;
	let values: (string | number)[][];
	let filter_values = filter_columns.map(s => get_unique_values(s));
	let search_value: string | null = null;
	let _on_load_columns = on_load_columns.length ? on_load_columns: original_headers;

	async function handle_change(data?: {
		data: Data;
		headers: Headers;
		metadata: Metadata;
	}): Promise<void> {
		let _data = data || value;

		_headers = original_headers;
		values = original_data ? [...original_data] : [];
		const display_headers = _headers.filter(h => _on_load_columns.includes(h));
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

 	function filter_column(column_name: string, value: any[]){
		values = original_data;
		if (!value.length) {
			return Array(values.length).fill(true);
		}
		const mask = values.map(row => {
			return value.some(v => row[original_headers.indexOf(column_name)] === v);
		});
		return mask;
	}

	function filter_column_values(values, filter_values, search_value){
		let search_value_mask;
		if (!search_value) {
			search_value_mask = Array(values.length).fill(true);
		} else {
			const search_values = search_value.split(";");
			search_value_mask = search_column_data.map(s => {
				const row_value = s.toString().toLowerCase()
				return search_values.some(search_value => row_value.includes(search_value.toLowerCase()));
			});
		}
		const masks = filter_values.map((value, i) => filter_column(filter_columns[i], value)).concat([search_value_mask]);
		return values.filter((row, i) => masks.every(mask => mask[i]));
	}

	function update_data(_on_load_columns, filter_values, search_value){
		values = select_columns(original_data, _on_load_columns);
		values = filter_column_values(values, filter_values, search_value);
		if (values.length === 0) {
			values =  [Array(_on_load_columns.length).fill("")];
		}
	}

	$: update_data(_on_load_columns, filter_values, search_value);


	function get_unique_values(filter_column) {
		const column_index = original_headers.indexOf(filter_column);
		return [...new Set(original_data.map(row => row[column_index]))];
	}

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

	async function handle_value_change(data: {
		data: Data;
		headers: Headers;
		metadata: Metadata;
	}): Promise<void> {
		if (JSON.stringify(data) !== old_value) {
			value = { ...data };
			old_value = JSON.stringify(value);
			handle_change(data);
		}
	}

	$: console.log("value", values);

</script>

<Block
	{visible}
	padding={false}
	{elem_id}
	{elem_classes}
	container={false}
	{scale}
	{min_width}
	allow_overflow={false}
>
	<Row>
		<Column>
			{#if search_column}
				<Row>
					<Simpletextbox
						label={"Model name search"}
						show_label={true}
						placeholder={"Search for a model by name. Separate multiple queries with ';'."}
						interactive={true}
						{gradio}
						on:submit={(e) => search_value = e.detail}
					/>
				</Row>
			{/if}
			{#if allow_column_select}
				<Row>
					<Checkboxgroup
						label={"Columns to Show"}
						{gradio}
						bind:value={_on_load_columns}
						choices={headers.filter(s => !hide_columns.includes(s)).map(s => [s, s])}
						{loading_status}
					/>
				</Row>
			{/if}
		</Column>
		<Column>
			<Group>
				{#each filter_columns as col, i}
					<Checkboxgroup
						label={`Filter ${col}`}
						{gradio}
						{loading_status}
						choices={get_unique_values(col).map(s => [s, s])}
						on:input={(e) => filter_values[i] = e.detail}
					/>
				{/each}
			</Group>
		</Column>
	</Row>
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

</Block>
