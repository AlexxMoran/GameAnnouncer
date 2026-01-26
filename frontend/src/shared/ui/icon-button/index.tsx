import { IconButton as MuiIconButton } from "@mui/material";
import type { IIconButtonProps } from "@shared/ui/icon-button/types";
import { type FC } from "react";

export const IconButton: FC<IIconButtonProps> = (props) => <MuiIconButton {...props} size="small" />;
