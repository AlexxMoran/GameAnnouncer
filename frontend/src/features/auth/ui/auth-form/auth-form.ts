import { Component, inject, input, output } from '@angular/core';
import { FormBuilder, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { IAuthFormValues } from '@features/auth/model/auth-form.types';
import { Button } from '@shared/ui/button/button';
import { InputField } from '@shared/ui/input-field/input-field';

@Component({
  selector: 'app-auth-form',
  imports: [ReactiveFormsModule, MatFormFieldModule, FormsModule, InputField, Button],
  templateUrl: './auth-form.html',
})
export class AuthForm {
  private formBuilder = inject(FormBuilder);
  submitted = output<IAuthFormValues>();
  buttonText = input<string>();
  isLoading = input<boolean>(false);

  authForm = this.formBuilder.group({
    username: ['', [Validators.required, Validators.email]],
    password: ['', [Validators.required, Validators.minLength(8)]],
  });

  get usernameControl() {
    return this.authForm.controls['username'];
  }

  get passwordControl() {
    return this.authForm.controls['password'];
  }

  get disabled() {
    return this.authForm.invalid;
  }

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
}
