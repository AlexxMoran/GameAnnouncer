import { AsyncPipe } from '@angular/common';
import { Component, inject, input, OnInit } from '@angular/core';
import { FormControl, ReactiveFormsModule } from '@angular/forms';
import { MatSelectModule } from '@angular/material/select';
import { TranslatePipe } from '@ngx-translate/core';
import { ValidationErrorsService } from '@shared/lib/validation/validation-errors.service';
import { ISelectFieldOption } from '@shared/ui/select-field/select-field.types';
import { distinctUntilChanged, map, Observable, startWith } from 'rxjs';

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
