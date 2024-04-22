export type Headers = string[];
export type Data = (string | number)[][];
export type Datatype = "str" | "markdown" | "html" | "number" | "bool" | "date";
export type Metadata = {
	[key: string]: string[][] | null;
} | null;
export type HeadersWithIDs = { value: string; id: string }[];
export type SearchColumns = {
	primary_column: string | null;
	secondary_columns: string[];
}
export type SelectColumns = {
	default_selection: string[];
    cant_deselect: string[];
    allow: boolean;
    label: string | null;
    show_label: boolean;
    info: string | null;
}


export type ColumnFilter = {
	column: string,
	type: "slider" | "dropdown" | "checkboxgroup",
	default: number | string | [string, string][],
	choices: [string, string][],
	label: string | null,
	show_label: boolean,
	info: string | null,
	greater_than: boolean,
	min: number | null,
	max: number | null,
}
export type FilterColumns = ColumnFilter[];

