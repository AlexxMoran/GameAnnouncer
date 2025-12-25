import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';
import { AUTH_FORM_INPUTS } from '@features/auth/model/auth-form.constants';
import { TranslatePipe } from '@ngx-translate/core';
import { StyleFactory } from '@shared/lib/styles/style-factory.service';
import { Form } from '@shared/ui/form/form';

@Component({
  selector: 'app-registration',
  imports: [Form, RouterLink, TranslatePipe],
  templateUrl: './registration.html',
  host: {
    class: 'flex flex-col justify-center items-center h-full',
  },
})
export class Registration {
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
}
