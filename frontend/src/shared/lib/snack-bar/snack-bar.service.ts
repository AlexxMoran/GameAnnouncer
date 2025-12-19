import { inject, Injectable } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { SnackBarMessage } from '@shared/ui/snack-bar-message/snack-bar-message';

interface ISnackBarMessage {
  message: string;
  panelClass: string;
}

@Injectable({
  providedIn: 'root',
})
export class SnackBarService {
  private snackBar = inject(MatSnackBar);
  private messageList: ISnackBarMessage[] = [];

  private openSnackBar(message: string, panelClass: string) {
    this.messageList.push({ message, panelClass });

    if (this.messageList.length === 1) {
      this.openNext();
    }
  }

  private openNext() {
    if (this.messageList.length === 0) return;

    const { message, panelClass } = this.messageList[0];

    const ref = this.snackBar.openFromComponent(SnackBarMessage, {
      panelClass,
      duration: 3000,
      data: { message },
      horizontalPosition: 'right',
    });

    ref.afterDismissed().subscribe(() => {
      setTimeout(() => {
        this.messageList.shift();
        this.openNext();
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
