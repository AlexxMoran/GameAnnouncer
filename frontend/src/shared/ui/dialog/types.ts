import type { DialogProps } from "@mui/material";

export interface IDialogProps
  extends Omit<DialogProps, "onClose">,
    ITStylesProps {
  title?: string;
  onCloseDialog?: () => void;
  disableBackdropClick?: boolean;
}

export interface ITStylesProps {
  capitalizeFirst?: boolean;
}
