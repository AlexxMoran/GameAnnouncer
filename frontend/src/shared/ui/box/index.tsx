import { Box as MuiBox } from "@mui/material";
import type { IBoxProps } from "@shared/ui/box/types";
import { forwardRef } from "react";

export const Box = forwardRef<HTMLDivElement, IBoxProps>((props, ref) => <MuiBox {...props} ref={ref} />);
