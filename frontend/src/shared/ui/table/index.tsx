import { Table as MuiTable, TableBody, TableCell, TableHead, TableRow } from "@mui/material";
import type { ITableProps, TTableRow } from "@shared/ui/table/types";

export const Table = <T extends TTableRow>({ columnList, rowList, hasHeader = true }: ITableProps<T>) => {
  return (
    <MuiTable>
      {hasHeader && (
        <TableHead>
          <TableRow>
            {columnList?.map((col) => (
              <TableCell sx={{ border: "none", padding: 1 }} key={String(col.id)}>
                {col.label}
              </TableCell>
            ))}
          </TableRow>
        </TableHead>
      )}
      <TableBody>
        {rowList?.map((row, rowIndex) => {
          const isDark = rowIndex % 2 === 0;

          return (
            <TableRow key={rowIndex}>
              {columnList?.map((col, colIndex) => {
                const isFirst = colIndex === 0;
                const isLast = colIndex === columnList.length - 1;

                return (
                  <TableCell
                    key={String(col.id)}
                    sx={{
                      backgroundColor: (theme) => (isDark ? theme.palette.background.accent : "inherit"),
                      borderTopLeftRadius: (theme) => (isFirst ? theme.shape.borderRadius : 0),
                      borderTopRightRadius: (theme) => (isLast ? theme.shape.borderRadius : 0),
                      borderBottomLeftRadius: (theme) => (isFirst ? theme.shape.borderRadius : 0),
                      borderBottomRightRadius: (theme) => (isLast ? theme.shape.borderRadius : 0),
                      padding: 1,
                      border: "none",
                    }}
                  >
                    {col.render ? col.render(row) : (row[col.id as keyof T] as React.ReactNode)}
                  </TableCell>
                );
              })}
            </TableRow>
          );
        })}
      </TableBody>
    </MuiTable>
  );
};
