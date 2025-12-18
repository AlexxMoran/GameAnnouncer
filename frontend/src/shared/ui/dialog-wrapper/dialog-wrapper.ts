import { Component, inject, input } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import { IconButton } from '@shared/ui/icon-button/icon-button';

@Component({
  selector: 'app-dialog-wrapper',
  imports: [IconButton],
  templateUrl: './dialog-wrapper.html',
  host: { class: 'relative flex flex-col items-center gap-5 px-7 pt-5 pb-8' },
})
export class DialogWrapper {
  readonly dialogRef = inject(MatDialogRef);
  readonly title = input.required<string>();

  closeDialog = () => {
    this.dialogRef.close();
  };
}
