import { Component, inject } from '@angular/core';
import { RouterLink } from '@angular/router';
import { AUTH_FORM_INPUTS } from '@features/auth/model/auth-form.constants';
import { IAuthFormValues } from '@features/auth/model/auth-form.types';
import { TranslatePipe } from '@ngx-translate/core';
import { RegistrationConfirmation } from '@pages/registration/ui/registration-confirmation/registration-confirmation';
import { AuthApiService } from '@shared/api/auth/auth-api.service';
import { DialogService } from '@shared/lib/dialog/dialog.service';
import { StyleFactory } from '@shared/lib/styles/style-factory.service';
import { Form } from '@shared/ui/form/form';
import { tap } from 'rxjs';

@Component({
  selector: 'app-registration-page',
  imports: [Form, RouterLink, TranslatePipe],
  templateUrl: './registration-page.html',
  host: {
    class: 'flex flex-col justify-center items-center h-full',
  },
})
export class RegistrationPage {
  private authApiService = inject(AuthApiService);
  private dialogService = inject(DialogService);

  createSubmitObservableFn = (values: IAuthFormValues) => this.register(values);

  get authFormInputs() {
    return AUTH_FORM_INPUTS;
  }

  get cardClasses() {
    return StyleFactory.card({
      bg: 'container-low',
      shadow: 'shadow-xl',
      classes: 'gap-3 w-150 h-100 items-center justify-center mb-12',
    });
  }

  register(values: IAuthFormValues) {
    return this.authApiService.register({ email: values.username, password: values.password }).pipe(
      tap(() => {
        this.dialogService.open(RegistrationConfirmation, {
          title: 'texts.welcome',
          inputs: { email: values.username },
        });
      }),
    );
  }
}
