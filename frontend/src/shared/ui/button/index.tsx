import { Button as MuiButton } from "@mui/material";
import type { IButtonProps } from "@shared/ui/button/types";
import { type FC } from "react";

export const Button: FC<IButtonProps> = (props) => <MuiButton variant="contained" {...props} />;
