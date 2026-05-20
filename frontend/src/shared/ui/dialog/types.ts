import type { DialogProps } from "@mui/material";
import type { ReactNode } from "react";

export interface IDialogProps extends Omit<DialogProps, "onClose" | "title"> {
  title?: string | ReactNode;
  onCloseDialog?: () => void;
  disableBackdropClick?: boolean;
}
