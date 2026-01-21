import type { LinkProps } from "@mui/material";
import type { LinkProps as RouterLinkProps } from "react-router";

export interface ILinkProps extends LinkProps, Omit<RouterLinkProps, "color"> {}
