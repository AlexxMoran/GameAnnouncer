import CloseIcon from "@mui/icons-material/Close";
import { DialogContent } from "@mui/material";
import { DialogStyled, DialogTitleStyled } from "@shared/ui/dialog/styles";
import type { IDialogProps } from "@shared/ui/dialog/types";
import { IconButton } from "@shared/ui/icon-button";
import { type FC } from "react";

export const Dialog: FC<IDialogProps> = ({
  title = "",
  disableBackdropClick,
  onCloseDialog,
  children,
  ...rest
}) => {
  const handleClose = (
    _: unknown,
    reason: "backdropClick" | "escapeKeyDown"
  ) => {
    if (disableBackdropClick && reason === "backdropClick") {
      return;
    }

    onCloseDialog?.();
  };

  return (
    <DialogStyled onClose={handleClose} maxWidth="lg" {...rest}>
      <IconButton
        onClick={onCloseDialog}
        sx={{ position: "absolute", right: 8, top: 8 }}
      >
        <CloseIcon />
      </IconButton>
      {title && (
        <DialogTitleStyled variant="h6" capitalizeFirst>
          {title}
        </DialogTitleStyled>
      )}
      <DialogContent sx={{ overflowY: "unset" }}>{children}</DialogContent>
    </DialogStyled>
  );
};
