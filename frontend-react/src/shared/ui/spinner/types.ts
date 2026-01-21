import type { CircularProgressProps } from "@mui/material";

export interface ISpinnerProps extends CircularProgressProps {
  type?: "single" | "pagination" | "backdrop";
}
