import type { TypographyProps } from "@mui/material";

export interface ITStylesProps {
  capitalizeFirst?: boolean;
}

export interface ITypographyProps extends TypographyProps, ITStylesProps {}
