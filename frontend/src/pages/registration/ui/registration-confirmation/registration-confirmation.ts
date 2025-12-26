import { DialogRef } from '@angular/cdk/dialog';
import { Component, inject, input } from '@angular/core';
import { TranslatePipe, TranslateService } from '@ngx-translate/core';
import { Button } from '@shared/ui/button/button';

@Component({
  selector: 'app-registration-confirmation',
  imports: [TranslatePipe, Button],
  template: `<span>{{ confirmationText }}</span
    ><app-button (clicked)="confirm()">{{ 'texts.ok' | translate }}</app-button>`,
  host: { class: 'flex flex-col gap-8  max-w-110' },
})
export class RegistrationConfirmation {
  private translateService = inject(TranslateService);
  private dialogRef = inject(DialogRef);

  readonly email = input('');

  get confirmationText() {
    return this.translateService.instant('texts.registrationConfirmation', {
      email: this.email(),
    });
  }

  confirm = () => {
    this.dialogRef.close();
  };
}
