import type { TextFieldProps } from "@mui/material";

export interface ITextFieldProps
  extends Omit<TextFieldProps<"outlined">, "variant"> {}
