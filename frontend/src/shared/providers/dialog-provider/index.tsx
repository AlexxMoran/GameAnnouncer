import { DialogContext } from "@shared/providers/dialog-provider/constants";
import type { IConfirmFunction, IOpenDialogOptions, TResolveReject } from "@shared/providers/dialog-provider/types";
import type { TMaybe } from "@shared/types/main.types";
import { Box } from "@shared/ui/box";
import { Button } from "@shared/ui/button";
import { Dialog } from "@shared/ui/dialog";
import { useCallback, useState, type FC, type PropsWithChildren } from "react";
import { useTranslation } from "react-i18next";

export const DialogProvider: FC<PropsWithChildren> = ({ children }) => {
  const { t } = useTranslation();
  const [options, setOptions] = useState<TMaybe<IOpenDialogOptions>>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [resolveReject, setResolveReject] = useState<TResolveReject>([]);

  const [contentType, setContentType] = useState<TMaybe<"default" | "confirm">>(null);

  const [resolve, reject] = resolveReject;

  const openDialog = useCallback((options: IOpenDialogOptions) => {
    setOptions(options);
    setContentType("default");
  }, []);

  const closeDialog = useCallback(() => {
    setOptions(null);
    setResolveReject([]);
    setIsLoading(false);
    setContentType(null);
  }, []);

  const confirm: IConfirmFunction = useCallback((options: IOpenDialogOptions) => {
    return new Promise((res, rej) => {
      setOptions(options);
      setContentType("confirm");
      setResolveReject([res, rej]);
    });
  }, []);

  const handleConfirm = () => {
    resolve({ setIsLoading, closeDialog });
  };

  const handleCancel = () => {
    reject(false);
    closeDialog();
  };

  return (
    <DialogContext.Provider value={{ openDialog, closeDialog, confirm }}>
      {Boolean(options) && (
        <Dialog {...options} onCloseDialog={closeDialog} open>
          {contentType === "default" && options?.children}
          {contentType === "confirm" && (
            <Box display="flex" flexDirection="column" gap={8}>
              {options?.children}
              <Box display="flex" alignSelf="flex-end" gap={2}>
                <Button onClick={handleCancel} variant="outlined">
                  {options?.cancellationText || t("actions.cancel")}
                </Button>
                <Button onClick={handleConfirm} loading={isLoading}>
                  {options?.confirmationText || t("actions.confirm")}
                </Button>
              </Box>
            </Box>
          )}
        </Dialog>
      )}
      {children}
    </DialogContext.Provider>
  );
};
