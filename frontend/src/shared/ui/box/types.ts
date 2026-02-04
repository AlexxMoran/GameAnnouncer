import type { BoxProps } from "@mui/material";
import type { Ref } from "react";

export interface IBoxProps extends BoxProps {
  ref?: Ref<HTMLDivElement>;
}
