import { Component, inject, input } from '@angular/core';
import { FormControl, ReactiveFormsModule } from '@angular/forms';
import { MatInputModule } from '@angular/material/input';
import { TranslatePipe, TranslateService } from '@ngx-translate/core';
import { getValidationErrorMessage } from '@shared/lib/validation/get-validation-error-message.utils';
import { TInputType } from '@shared/ui/input-field/input-field.types';

@Component({
  selector: 'app-input-field',
  imports: [ReactiveFormsModule, MatInputModule, TranslatePipe],
  templateUrl: './input-field.html',
  host: { class: 'w-full' },
})
export class InputField {
  private translateService = inject(TranslateService);
  readonly control = input.required<FormControl>();
  readonly type = input<TInputType>('text');
  readonly label = input('');
  readonly isTextarea = input(false);

  getErrorMessage() {
    const { errors } = this.control();

    if (errors) {
      return getValidationErrorMessage(errors, this.translateService);
    }

    return '';
  }
}
