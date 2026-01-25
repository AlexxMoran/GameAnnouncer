import { Divider as MuiDivider } from "@mui/material";
import type { IDividerProps } from "@shared/ui/divider/types";
import type { FC } from "react";

export const Divider: FC<IDividerProps> = (props) => {
  return <MuiDivider {...props} />;
};
