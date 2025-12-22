import { inject, Injectable, Type } from '@angular/core';
import { MatDialog, MatDialogConfig } from '@angular/material/dialog';
import { IConfirmOptions } from '@shared/lib/dialog/dialog-service.types';
import { DialogConfirmContent } from '@shared/ui/dialog-confirm-content/dialog-confirm-content';
import { DialogWrapper } from '@shared/ui/dialog-wrapper/dialog-wrapper';
import { IOpenDialogOptions } from '@shared/ui/dialog-wrapper/dialog-wrapper.types';

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
