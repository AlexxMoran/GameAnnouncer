import CloseIcon from "@mui/icons-material/Close";
import { DialogContent, DialogTitle } from "@mui/material";
import { DialogStyled } from "@shared/ui/dialog/styles";
import type { IDialogProps } from "@shared/ui/dialog/types";
import { IconButton } from "@shared/ui/icon-button";
import { type FC } from "react";

export const Dialog: FC<IDialogProps> = (props) => {
  const {
    title = "",
    disableBackdropClick,
    onCloseDialog,
    children,
    ...rest
  } = props;

  const handleClose = (
    _: unknown,
    reason: "backdropClick" | "escapeKeyDown",
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
        <DialogTitle
          variant="h6"
          sx={{
            "&::first-letter": {
              textTransform: "capitalize",
            },
          }}
        >
          {title}
        </DialogTitle>
      )}
      <DialogContent sx={{ overflowY: "unset" }}>{children}</DialogContent>
    </DialogStyled>
  );
};
