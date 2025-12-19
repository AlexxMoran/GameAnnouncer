import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';
import { AuthForm } from '@features/auth/ui/auth-form/auth-form';
import { TranslatePipe } from '@ngx-translate/core';
import { StyleFactory } from '@shared/lib/styles/style-factory.service';

@Component({
  selector: 'app-registration',
  imports: [AuthForm, RouterLink, TranslatePipe],
  templateUrl: './registration.html',
  host: {
    class: 'flex flex-col justify-center items-center h-full',
  },
})
export class Registration {
  get cardClasses() {
    return StyleFactory.card({
      bg: 'container-low',
      shadow: 'shadow-xl',
      classes: 'gap-3 w-150 h-100 items-center justify-center mb-12',
    });
  }
}
