import { Component, inject, input } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import { TranslatePipe } from '@ngx-translate/core';
import { Button } from '@shared/ui/button/button';
import { SUCCESS_CONFIRM_RESULT } from '@shared/ui/dialog-confirm-content/dialog-confirm-content.constants';

@Component({
  selector: 'app-dialog-confirm-content',
  imports: [TranslatePipe, Button],
  templateUrl: './dialog-confirm-content.html',
  host: { class: 'flex flex-col gap-9 w-full' },
})
export class DialogConfirmContent {
  private dialogRef = inject(MatDialogRef);
  readonly message = input.required<string>();
  readonly confirmButtonText = input('actions.confirm');
  readonly cancelButtonText = input('actions.cancel');

  cancel() {
    this.dialogRef.close();
  }

  confirm() {
    this.dialogRef.close(SUCCESS_CONFIRM_RESULT);
  }
}
