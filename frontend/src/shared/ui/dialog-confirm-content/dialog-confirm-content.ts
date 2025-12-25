import { Component, inject, input, OnDestroy, signal } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import { TranslatePipe } from '@ngx-translate/core';
import { Button } from '@shared/ui/button/button';
import { finalize, Observable, Subject, takeUntil } from 'rxjs';

@Component({
  selector: 'app-dialog-confirm-content',
  imports: [TranslatePipe, Button],
  templateUrl: './dialog-confirm-content.html',
  host: { class: 'flex flex-col gap-9 w-full' },
})
export class DialogConfirmContent implements OnDestroy {
  private dialogRef = inject(MatDialogRef);

  readonly message = input.required<string>();
  readonly confirmButtonText = input('actions.confirm');
  readonly cancelButtonText = input('actions.cancel');
  readonly confirmObservable = input<Observable<unknown>>();

  readonly isLoading = signal(false);

  private destroy$ = new Subject<void>();

  cancel() {
    this.dialogRef.close();
  }

  confirm() {
    this.isLoading.set(true);

    this.confirmObservable()
      ?.pipe(
        takeUntil(this.destroy$),
        finalize(() => this.isLoading.set(false)),
      )
      .subscribe(() => this.dialogRef.close());
  }

  ngOnDestroy() {
    this.destroy$.next();
    this.destroy$.complete();
  }
}
