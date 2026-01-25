import { Fab as MuiFab } from "@mui/material";
import type { IFabProps } from "@shared/ui/fab-button/types";
import { Tooltip } from "@shared/ui/tooltip";
import { type FC } from "react";

export const Fab: FC<IFabProps> = ({ tooltip, ...rest }) => {
  return (
    <Tooltip title={tooltip} hidden={!tooltip} placement="left-start">
      <MuiFab {...rest} color="primary" />
    </Tooltip>
  );
};
