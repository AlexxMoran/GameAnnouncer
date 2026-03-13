export interface IDialogButtonGroupProps {
  onCancel?: () => void;
  onConfirm?: () => void;
  isLoading?: boolean;
  disabled?: boolean;
  cancellationText?: string;
  confirmationText?: string;
  isForDialog?: boolean;
}
