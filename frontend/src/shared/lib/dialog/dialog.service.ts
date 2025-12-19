import { inject, Injectable, Type } from '@angular/core';
import { MatDialog, MatDialogConfig } from '@angular/material/dialog';
import { DialogConfirmContent } from '@shared/ui/dialog-confirm-content/dialog-confirm-content';
import { DialogWrapper, IOpenDialogOptions } from '@shared/ui/dialog-wrapper/dialog-wrapper';

export interface IConfirmOptions {
  message: string;
  confirmButtonText?: string;
  cancelButtonText?: string;
}

@Injectable({ providedIn: 'root' })
export class DialogService {
  dialog = inject(MatDialog);

  open = <TComponent>(
    component: Type<TComponent>,
    { config, ...options }: IOpenDialogOptions<TComponent> & { config?: MatDialogConfig },
  ) => {
    const dialogRef = this.dialog.open(DialogWrapper, {
      data: { component, options },
      ...config,
    });

    return dialogRef;
  };

  confirm = (options: IConfirmOptions) => {
    return this.open(DialogConfirmContent, { title: 'entities.confirmation', inputs: options });
  };
}
