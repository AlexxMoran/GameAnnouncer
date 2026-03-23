import { useDeviceType } from "@shared/hooks/use-device-type";
import { Box } from "@shared/ui/box";
import { Button } from "@shared/ui/button";
import type { IButtonGroupProps } from "@shared/ui/button-group/interfaces";
import { DialogActions } from "@shared/ui/dialog";
import type { FC } from "react";
import { useTranslation } from "react-i18next";

export const ButtonGroup: FC<IButtonGroupProps> = (props) => {
  const { onCancel, onConfirm, isLoading, cancellationText, confirmationText, disabled, isForDialog } = props;

  const { t } = useTranslation();
  const { isMobile } = useDeviceType();

  if (isForDialog) {
    return (
      <DialogActions sx={{ px: 3, pb: isMobile ? 3 : 2, pt: 1, flexDirection: isMobile ? "column" : "row", gap: 1 }}>
        <Button onClick={onCancel} variant="outlined" fullWidth={isMobile} sx={{ order: isMobile ? 2 : 1 }}>
          {cancellationText || t("actions.cancel")}
        </Button>
        <Button
          onClick={onConfirm}
          loading={isLoading}
          fullWidth={isMobile}
          sx={{ order: isMobile ? 1 : 2 }}
          disabled={disabled}
        >
          {confirmationText || t("actions.confirm")}
        </Button>
      </DialogActions>
    );
  }

  return onCancel ? (
    <Box display="flex" gap={2} alignSelf="flex-end">
      <Button variant="outlined" onClick={onCancel}>
        {cancellationText}
      </Button>
      <Button onClick={onConfirm} loading={isLoading} disabled={disabled}>
        {confirmationText}
      </Button>
    </Box>
  ) : (
    <Button onClick={onConfirm} loading={isLoading} disabled={disabled}>
      {confirmationText}
    </Button>
  );
};
