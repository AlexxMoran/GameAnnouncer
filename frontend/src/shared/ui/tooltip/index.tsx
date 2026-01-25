import { Tooltip as MuiTooltip } from "@mui/material";
import type { ITooltipProps } from "@shared/ui/tooltip/types";
import type { FC } from "react";

export const Tooltip: FC<ITooltipProps> = (props) => {
  return <MuiTooltip {...props} />;
};
