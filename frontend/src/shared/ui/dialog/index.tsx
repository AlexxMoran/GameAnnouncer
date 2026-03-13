import CloseIcon from "@mui/icons-material/Close";
import {
  DialogTitle,
  Dialog as MuiDialog,
  DialogActions as MuiDialogActions,
  DialogContent as MuiDialogContent,
  type DialogActionsProps,
  type DialogContentProps,
} from "@mui/material";
import { useDeviceType } from "@shared/hooks/use-device-type";
import type { IDialogProps } from "@shared/ui/dialog/types";
import { IconButton } from "@shared/ui/icon-button";
import { type FC } from "react";

export const DialogActions: FC<DialogActionsProps> = ({ children, ...props }) => {
  return <MuiDialogActions {...props}>{children}</MuiDialogActions>;
};

export const DialogContent: FC<DialogContentProps> = ({ children, ...props }) => {
  return <MuiDialogContent {...props}>{children}</MuiDialogContent>;
};

export const Dialog: FC<IDialogProps> = (props) => {
  const { title = "", disableBackdropClick, onCloseDialog, children, ...rest } = props;

  const { isMobile } = useDeviceType();

  const handleClose = (_: unknown, reason: "backdropClick" | "escapeKeyDown") => {
    if (disableBackdropClick && reason === "backdropClick") {
      return;
    }

    onCloseDialog?.();
  };

  return (
    <MuiDialog onClose={handleClose} maxWidth="lg" {...rest}>
      {!isMobile && (
        <IconButton onClick={onCloseDialog} sx={{ position: "absolute", right: 8, top: 8 }}>
          <CloseIcon />
        </IconButton>
      )}
      {title && (
        <DialogTitle variant="h6" className="capitalize-first">
          {title}
        </DialogTitle>
      )}
      {children}
    </MuiDialog>
  );
};
