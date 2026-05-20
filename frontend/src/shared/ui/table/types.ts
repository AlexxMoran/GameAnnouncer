import type { TObjectAny } from "@shared/types/main.types";

export type TTableRow = TObjectAny & { id: string };

export interface IColumn<T extends TTableRow> {
  id: keyof T;
  label?: string;
  render?: (row: T) => React.ReactNode;
}

export interface ITableProps<T extends TTableRow> {
  columnList?: IColumn<T>[];
  rowList?: T[];
  hasHeader?: boolean;
}
