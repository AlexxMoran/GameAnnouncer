import { Typography } from "@mui/material";
import type { ITypographyProps } from "@shared/ui/typography/types";
import { forwardRef } from "react";

export const T = forwardRef<HTMLParagraphElement, ITypographyProps>((props, ref) => (
  <Typography {...props} ref={ref} />
));
