import { LinearProgress as MuiLinearProgress } from "@mui/material";
import type { ILinearProgressProps } from "@shared/ui/linear-progress/types";
import { type FC } from "react";

export const LinearProgress: FC<ILinearProgressProps> = (props) => <MuiLinearProgress {...props} />;
