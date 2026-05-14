import type { IButtonProps } from "@shared/ui/button/types";
export interface IButtonGroupProps {
  onCancel?: () => void;
  onConfirm?: () => void;
  isLoading?: boolean;
  disabled?: boolean;
  cancellationText?: string;
  confirmationText?: string;
  confirmationColor?: IButtonProps["color"];
  isForDialog?: boolean;
}
