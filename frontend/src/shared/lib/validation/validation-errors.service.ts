import { inject, Injectable } from '@angular/core';
import { AbstractControl } from '@angular/forms';
import { TranslateService } from '@ngx-translate/core';
import { TMaybe } from '@shared/lib/utility-types/additional.types';

@Injectable({ providedIn: 'root' })
export class ValidationErrorsService {
  private translateService = inject(TranslateService);

  getMessage(control: TMaybe<AbstractControl>) {
    const { errors } = control || {};

    if (!errors) return null;

    if (errors['required']) {
      return this.translateService.instant('validationErrors.required');
    }

    if (errors['email']) {
      return this.translateService.instant('validationErrors.email');
    }

    if (errors['minlength']) {
      const { requiredLength } = errors['minlength'];

      return this.translateService.instant('validationErrors.minLength', {
        minLength: requiredLength,
      });
    }

    if (errors['maxlength']) {
      const { requiredLength } = errors['maxlength'];

      return this.translateService.instant('validationErrors.maxLength', {
        maxLength: requiredLength,
      });
    }

    return this.translateService.instant('validationErrors.unknown');
  }
}
