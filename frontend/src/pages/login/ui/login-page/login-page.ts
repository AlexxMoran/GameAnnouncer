import { Component, inject } from '@angular/core';
import { RouterModule } from '@angular/router';
import { AUTH_FORM_INPUTS } from '@features/auth/model/auth-form.constants';
import { TranslatePipe } from '@ngx-translate/core';
import { ILoginDto } from '@shared/api/auth/auth-api-service.types';
import { AuthService } from '@shared/lib/auth/auth.service';
import { StyleFactory } from '@shared/lib/styles/style-factory.service';
import { EAppRoutes } from '@shared/routes/routes.constants';
import { Form } from '@shared/ui/form/form';

@Component({
  selector: 'app-login',
  imports: [Form, RouterModule, TranslatePipe],
  templateUrl: './login-page.html',
  host: {
    class: 'flex flex-col justify-center items-center h-full',
  },
})
export class LoginPage {
  private authService = inject(AuthService);

  createSubmitObservableFn = (values: ILoginDto) => this.login(values);

  login = (params: ILoginDto) => {
    return this.authService.login(params);
  };

  get authFormInputs() {
    return AUTH_FORM_INPUTS;
  }

  get registrationRoute() {
    return EAppRoutes.Registration;
  }

  get cardClasses() {
    return StyleFactory.card({
      bg: 'container-low',
      shadow: 'shadow-xl',
      classes: 'gap-3 w-150 h-100 items-center justify-center mb-12',
    });
  }
}
