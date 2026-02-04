import { Zoom as MuiZoom } from "@mui/material";
import type { IZoomProps } from "@shared/ui/zoom/types";
import type { FC } from "react";

export const Zoom: FC<IZoomProps> = (props) => {
  return <MuiZoom {...props} />;
};
