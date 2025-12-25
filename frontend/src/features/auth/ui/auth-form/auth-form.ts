import { Component, input, output } from '@angular/core';
import { AUTH_FORM_INPUTS } from '@features/auth/model/auth-form.constants';
import { IAuthFormValues } from '@features/auth/model/auth-form.types';
import { Form } from '@shared/ui/form/form';

@Component({
  selector: 'app-auth-form',
  imports: [Form],
  template: `<app-form
    [controls]="authFormInputs.controls"
    [formFieldList]="authFormInputs.formFieldList"
    [buttonText]="buttonText() || ''"
    [isLoading]="isLoading() || false"
    (submitted)="submitted.emit($event)"
  ></app-form> `,
  host: { class: 'w-100' },
})
export class AuthForm {
  readonly submitted = output<IAuthFormValues>();
  readonly buttonText = input<string>();
  readonly isLoading = input<boolean>(false);

  get authFormInputs() {
    return AUTH_FORM_INPUTS;
  }
}
