import { Validators } from '@angular/forms';
import { IAuthFormValues } from '@features/auth/model/auth-form.types';
import { TFormField, TGroupControls } from '@shared/ui/form/form.types';

const AUTH_FORM_FIELD_LIST: TFormField<IAuthFormValues>[] = [
  {
    type: 'input' as const,
    name: 'username' as const,
    inputType: 'email' as const,
    label: 'entities.email',
  },
  {
    type: 'input' as const,
    name: 'password' as const,
    inputType: 'password' as const,
    label: 'entities.password',
  },
];

const AUTH_FORM_CONTROLS: TGroupControls<IAuthFormValues> = {
  username: ['', [Validators.required, Validators.email]],
  password: ['', [Validators.required, Validators.minLength(8)]],
};

export const AUTH_FORM_INPUTS = {
  controls: AUTH_FORM_CONTROLS,
  formFieldList: AUTH_FORM_FIELD_LIST,
};
