import type { TextFieldProps } from "@mui/material";
import type { ReactNode } from "react";

export interface ITextFieldProps extends Omit<TextFieldProps<"outlined">, "variant"> {
  loading?: boolean;
  endAdornment?: ReactNode;
}
