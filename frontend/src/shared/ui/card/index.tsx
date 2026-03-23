import { Card as MuiCard } from "@mui/material";
import type { ICardProps } from "@shared/ui/card/types";
import { forwardRef } from "react";

export const Card = forwardRef<HTMLDivElement, ICardProps>((props, ref) => <MuiCard {...props} ref={ref} />);
