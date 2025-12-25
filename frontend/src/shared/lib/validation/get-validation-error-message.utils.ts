import { ValidationErrors } from '@angular/forms';
import { TranslateService } from '@ngx-translate/core';

export const getValidationErrorMessage = (
  errors: ValidationErrors,
  translateService: TranslateService,
) => {
  if (!errors) return null;

  if (errors['required']) {
    return translateService.instant('validationErrors.required');
  }

  if (errors['email']) {
    return translateService.instant('validationErrors.email');
  }

  if (errors['minlength']) {
    const { requiredLength } = errors['minlength'];

    return translateService.instant('validationErrors.minLength', {
      minLength: requiredLength,
    });
  }

  if (errors['maxlength']) {
    const { requiredLength } = errors['maxlength'];

    return translateService.instant('validationErrors.maxLength', {
      maxLength: requiredLength,
    });
  }

  return translateService.instant('validationErrors.unknown');
};
