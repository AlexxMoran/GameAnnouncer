import { AsyncPipe } from '@angular/common';
import { Component, inject, input, OnInit } from '@angular/core';
import { FormControl, ReactiveFormsModule } from '@angular/forms';
import { MatSelectModule } from '@angular/material/select';
import { TranslatePipe } from '@ngx-translate/core';
import { IOption } from '@shared/lib/utility-types/base-ui.types';
import { ValidationErrorsService } from '@shared/lib/validation/validation-errors.service';
import { distinctUntilChanged, map, Observable, startWith } from 'rxjs';

export interface ISelectFieldOption<TName extends string = string> extends IOption<TName> {}

@Component({
  selector: 'app-select-field',
  imports: [ReactiveFormsModule, MatSelectModule, TranslatePipe, AsyncPipe],
  templateUrl: './select-field.html',
})
export class SelectField implements OnInit {
  private validationErrorsService = inject(ValidationErrorsService);
  control = input.required<FormControl>();
  optionList = input.required<ISelectFieldOption[]>();
  label = input('');
  errorMessage$: Observable<string> | undefined;

  ngOnInit() {
    this.errorMessage$ = this.control().valueChanges.pipe(
      startWith(null),
      map(() => this.validationErrorsService.getMessage(this.control())),
      distinctUntilChanged(),
    );
  }
}
