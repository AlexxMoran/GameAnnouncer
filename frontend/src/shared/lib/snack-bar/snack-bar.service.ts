import { Component, inject, Injectable } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MAT_SNACK_BAR_DATA, MatSnackBar, MatSnackBarRef } from '@angular/material/snack-bar';

@Component({
  selector: 'snack-bar-message',
  imports: [MatButtonModule, MatIconModule],
  template: `<div class="flex justify-between">
    <span class="mat-subtitle-1">{{ data.message }}</span>
    <button mat-icon-button (click)="dismiss()">
      <mat-icon>close</mat-icon>
    </button>
  </div>`,
})
export class SnackBarMessage {
  data = inject(MAT_SNACK_BAR_DATA);
  snackBarRef = inject(MatSnackBarRef);

  dismiss() {
    this.snackBarRef.dismiss();
  }
}

@Injectable({
  providedIn: 'root',
})
export class SnackBarService {
  private snackBar = inject(MatSnackBar);
  private messageList: string[] = [];

  openSnackBar(message: string, panelClass: string) {
    this.messageList.push(message);

    if (this.messageList.length === 1) {
      this.openNext(panelClass);
    }
  }

  openNext(panelClass: string) {
    if (this.messageList.length === 0) return;

    const message = this.messageList[0];

    const ref = this.snackBar.openFromComponent(SnackBarMessage, {
      panelClass,
      duration: 3000,
      data: { message },
      horizontalPosition: 'right',
    });

    ref.afterDismissed().subscribe(() => {
      setTimeout(() => {
        this.messageList.shift();
        this.openNext(panelClass);
      }, 300);
    });
  }

  showSuccessSnackBar(message: string) {
    this.openSnackBar(message, 'snack-bar__container_success');
  }

  showErrorSnackBar(message: string) {
    this.openSnackBar(message, 'snack-bar__container_error');
  }
}
