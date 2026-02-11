import { FormControlLabel as MuiFormControlLabel } from "@mui/material";
import type { IFormControlLabelProps } from "@shared/ui/form-control-label/types";
import type { FC } from "react";

export const FormControlLabel: FC<IFormControlLabelProps> = (props) => {
  return <MuiFormControlLabel {...props} />;
};
