import { Component, inject } from '@angular/core';
import { MAT_SNACK_BAR_DATA, MatSnackBarRef } from '@angular/material/snack-bar';
import { IconButton } from '@shared/ui/icon-button/icon-button';

@Component({
  selector: 'app-snack-bar-message',
  imports: [IconButton],
  template: `<div class="flex justify-between">
    <span class="mat-subtitle-1">{{ data.message }}</span>
    <app-icon-button (clicked)="dismiss()" fontIcon="close" />
  </div>`,
})
export class SnackBarMessage {
  data = inject(MAT_SNACK_BAR_DATA);
  snackBarRef = inject(MatSnackBarRef);

  dismiss() {
    this.snackBarRef.dismiss();
  }
}
