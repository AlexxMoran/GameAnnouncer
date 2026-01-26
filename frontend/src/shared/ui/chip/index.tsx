import { Chip as MuiChip } from "@mui/material";
import type { IChipProps } from "@shared/ui/chip/types";
import type { FC } from "react";

export const Chip: FC<IChipProps> = (props) => {
  return <MuiChip {...props} sx={{ cursor: "pointer" }} />;
};
