import type { IButtonProps } from "@shared/ui/button/types";
import type { IDialogProps } from "@shared/ui/dialog/types";
import type { Dispatch, SetStateAction } from "react";

export interface IDialogProviderContext {
  closeDialog: () => void;
  openDialog: (options: IOpenDialogOptions) => void;
  confirm: IConfirmFunction;
}

export interface IOpenDialogOptions extends Omit<IDialogProps, "open"> {
  confirmationText?: string;
  cancellationText?: string;
  confirmationColor?: IButtonProps["color"];
}

export interface IConfirmReturnResult {
  closeDialog: () => void;
  setIsLoading: Dispatch<SetStateAction<boolean>>;
}

export type TConfirmReturnValue = Promise<false | IConfirmReturnResult>;
export type TResolveReject = ((params: false | IConfirmReturnResult) => void)[];

export interface IConfirmFunction {
  (params: IOpenDialogOptions): TConfirmReturnValue;
}
