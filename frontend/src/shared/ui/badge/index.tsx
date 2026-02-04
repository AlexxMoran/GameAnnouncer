import { Badge as MuiBadge } from "@mui/material";
import type { IBadgeProps } from "@shared/ui/badge/types";
import { forwardRef } from "react";

export const Badge = forwardRef<HTMLDivElement, IBadgeProps>((props, ref) => (
  <MuiBadge {...props} sx={{ ...props.sx, width: "fit-content" }} ref={ref} />
));
