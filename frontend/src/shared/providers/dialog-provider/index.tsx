import { Slide } from "@mui/material";
import type { TransitionProps } from "@mui/material/transitions";
import { useDeviceType } from "@shared/hooks/use-device-type";
import { DialogContext } from "@shared/providers/dialog-provider/constants";
import type { IConfirmFunction, IOpenDialogOptions, TResolveReject } from "@shared/providers/dialog-provider/types";
import type { TMaybe } from "@shared/types/main.types";
import { Dialog, DialogContent } from "@shared/ui/dialog";
import { DialogButtonGroup } from "@shared/ui/dialog-button-group";
import { forwardRef, useCallback, useState, type FC, type PropsWithChildren, type ReactElement, type Ref } from "react";

const Transition = forwardRef(function Transition(
  props: TransitionProps & {
    children: ReactElement;
  },
  ref: Ref<unknown>
) {
  return <Slide direction="up" ref={ref} {...props} />;
});

export const DialogProvider: FC<PropsWithChildren> = ({ children }) => {
  const { isMobile } = useDeviceType();
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
      <Dialog
        {...options}
        onCloseDialog={closeDialog}
        fullScreen={isMobile}
        slots={{ transition: isMobile ? Transition : undefined }}
        open={!!options}
      >
        {contentType === "default" && options?.children}
        {contentType === "confirm" && (
          <>
            <DialogContent>{options?.children}</DialogContent>
            <DialogButtonGroup
              onCancel={handleCancel}
              onConfirm={handleConfirm}
              isLoading={isLoading}
              cancellationText={options?.cancellationText}
              confirmationText={options?.confirmationText}
            />
          </>
        )}
      </Dialog>
      {children}
    </DialogContext.Provider>
  );
};
