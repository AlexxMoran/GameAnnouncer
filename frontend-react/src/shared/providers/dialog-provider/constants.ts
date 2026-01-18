import type { IDialogProviderContext } from "@shared/providers/dialog-provider/types";
import noop from "lodash/noop";
import { createContext } from "react";

const DEFAULT_MODAL_PROVIDER_STATE: IDialogProviderContext = {
  closeDialog: noop,
  openDialog: noop,
  confirm: () =>
    new Promise((resolve, reject) => {
      resolve({ closeDialog: noop, setIsLoading: noop });
      reject(false);
    }),
};

export const DialogContext = createContext<IDialogProviderContext>(
  DEFAULT_MODAL_PROVIDER_STATE
);
