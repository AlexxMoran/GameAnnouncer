import { Checkbox as MuiCheckbox } from "@mui/material";
import type { ICheckboxProps } from "@shared/ui/checkbox/types";
import type { FC } from "react";

export const Checkbox: FC<ICheckboxProps> = (props) => {
  return <MuiCheckbox {...props} />;
};
