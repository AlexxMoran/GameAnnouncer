import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';
import { AuthForm } from '@features/auth/ui/auth-form/auth-form';
import { TranslatePipe } from '@ngx-translate/core';

@Component({
  selector: 'app-registration',
  imports: [AuthForm, RouterLink, TranslatePipe],
  templateUrl: './registration.html',
  host: {
    class: 'flex flex-col justify-center items-center h-full',
  },
})
export class Registration {}
