import { AsyncPipe } from '@angular/common';
import { Component, inject, input, OnInit } from '@angular/core';
import { FormControl, ReactiveFormsModule } from '@angular/forms';
import { MatInputModule } from '@angular/material/input';
import { TranslatePipe } from '@ngx-translate/core';
import { ValidationErrorsService } from '@shared/lib/validation/validation-errors.service';
import { distinctUntilChanged, map, Observable, startWith } from 'rxjs';

type TInputType = 'text' | 'password' | 'email';

@Component({
  selector: 'app-input-field',
  imports: [ReactiveFormsModule, MatInputModule, TranslatePipe, AsyncPipe],
  templateUrl: './input-field.html',
})
export class InputField implements OnInit {
  private validationErrorsService = inject(ValidationErrorsService);
  readonly control = input.required<FormControl>();
  readonly label = input('');
  readonly type = input<TInputType>('text');
  readonly isTextarea = input(false);
  errorMessage$: Observable<string> | undefined;

  ngOnInit() {
    this.errorMessage$ = this.control().valueChanges.pipe(
      startWith(null),
      map(() => this.validationErrorsService.getMessage(this.control())),
      distinctUntilChanged(),
    );
  }
}
