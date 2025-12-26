import { Component, inject, input } from '@angular/core';
import { FormControl, ReactiveFormsModule } from '@angular/forms';
import { MatSelectModule } from '@angular/material/select';
import { TranslatePipe, TranslateService } from '@ngx-translate/core';
import { getValidationErrorMessage } from '@shared/lib/validation/get-validation-error-message.utils';
import { ISelectFieldOption } from '@shared/ui/select-field/select-field.types';

@Component({
  selector: 'app-select-field',
  imports: [ReactiveFormsModule, MatSelectModule, TranslatePipe],
  templateUrl: './select-field.html',
  host: { class: 'w-full' },
})
export class SelectField {
  private translateService = inject(TranslateService);
  readonly optionList = input.required<ISelectFieldOption[]>();
  readonly control = input.required<FormControl>();
  readonly label = input('');
  readonly multiple = input(false);

  getErrorMessage() {
    const { errors } = this.control();

    if (errors) {
      return getValidationErrorMessage(errors, this.translateService);
    }

    return '';
  }
}
