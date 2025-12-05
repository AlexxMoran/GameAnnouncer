import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';
import { AuthForm } from '@features/auth/ui/auth-form/auth-form';
import { TranslatePipe } from '@ngx-translate/core';

@Component({
  selector: 'app-login',
  imports: [AuthForm, RouterModule, TranslatePipe],
  templateUrl: './login.html',
  host: {
    class: 'flex flex-col justify-center items-center h-full',
  },
})
export class Login {}
