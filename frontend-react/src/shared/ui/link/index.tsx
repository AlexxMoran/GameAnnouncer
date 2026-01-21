import { Link as MuiLink } from "@mui/material";
import type { ILinkProps } from "@shared/ui/link/types";
import { type FC } from "react";
import { Link as RouterLink } from "react-router";

export const Link: FC<ILinkProps> = (props) => (
  <MuiLink {...props} component={RouterLink} />
);
