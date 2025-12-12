import { Component, inject, input, output } from '@angular/core';
import { FormBuilder, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { IAuthFormValues } from '@features/auth/model/auth-form.types';
import { TranslatePipe } from '@ngx-translate/core';
import { ValidationErrorsService } from '@shared/lib/validation/validation-errors.service';
import { Button } from '@shared/ui/button/button';

@Component({
  selector: 'app-auth-form',
  imports: [
    FormsModule,
    MatFormFieldModule,
    MatInputModule,
    Button,
    ReactiveFormsModule,
    TranslatePipe,
  ],
  templateUrl: './auth-form.html',
})
export class AuthForm {
  private formBuilder = inject(FormBuilder);
  private validationErrorsService = inject(ValidationErrorsService);
  submitted = output<IAuthFormValues>();
  buttonText = input<string>();
  isLoading = input<boolean>(false);

  authForm = this.formBuilder.group({
    username: ['', [Validators.required, Validators.email]],
    password: ['', [Validators.required, Validators.minLength(8)]],
  });

  submit() {
    if (this.authForm.invalid) {
      return;
    }

    const formData = this.authForm.value;

    const values = {
      username: formData.username || '',
      password: formData.password || '',
    };

    this.submitted.emit(values);
  }

  getErrorMessage(controlName: 'username' | 'password') {
    const control = this.authForm.get(controlName);

    return this.validationErrorsService.getMessage(control);
  }
}
