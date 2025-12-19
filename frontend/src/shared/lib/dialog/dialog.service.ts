import { inject, Injectable, Type } from '@angular/core';
import { MatDialog, MatDialogConfig } from '@angular/material/dialog';
import { DialogWrapper, IOpenDialogOptions } from '@shared/ui/dialog-wrapper/dialog-wrapper';

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
}
