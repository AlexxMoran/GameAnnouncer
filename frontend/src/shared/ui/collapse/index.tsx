import { Collapse as MuiCollapse } from "@mui/material";
import type { ICollapseProps } from "@shared/ui/collapse/types";
import type { FC } from "react";

export const Collapse: FC<ICollapseProps> = (props) => {
  return <MuiCollapse {...props} />;
};
