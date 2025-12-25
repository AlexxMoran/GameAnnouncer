import { Component, inject, input, OnDestroy, OnInit, signal } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, ReactiveFormsModule } from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';
import { TranslatePipe } from '@ngx-translate/core';
import { TMaybe } from '@shared/lib/utility-types/additional.types';
import { TObjectAny } from '@shared/lib/utility-types/object.types';
import { Button } from '@shared/ui/button/button';
import { TCreateSubmitObservable, TFormField, TGroupControls } from '@shared/ui/form/form.types';
import { InputField } from '@shared/ui/input-field/input-field';
import { SelectField } from '@shared/ui/select-field/select-field';
import { finalize, Subject, takeUntil } from 'rxjs';

@Component({
  selector: 'app-form',
  imports: [Button, TranslatePipe, ReactiveFormsModule, SelectField, InputField],
  templateUrl: './form.html',
  host: { class: 'w-full' },
})
export class Form<TFormValues extends TObjectAny> implements OnInit, OnDestroy {
  private formBuilder = inject(FormBuilder);
  private dialogRef: TMaybe<MatDialogRef<unknown>> = null;

  readonly controls = input.required<TGroupControls<TFormValues>>();
  readonly formFieldList = input.required<TFormField<TFormValues>[]>();
  readonly createSubmitObservableFn = input<TCreateSubmitObservable<TFormValues>>();
  readonly initialValues = input<TFormValues>();
  readonly buttonText = input('');
  readonly isDialogForm = input(true);

  readonly isLoading = signal(false);
  readonly isSubmitted = signal(false);

  private destroy$ = new Subject<void>();

  form!: FormGroup;

  ngOnInit() {
    if (this.isDialogForm()) {
      this.dialogRef = inject(MatDialogRef);
    }

    this.form = this.formBuilder.group(this.controls());

    const initialValues = this.initialValues();

    if (initialValues) {
      this.form.patchValue(initialValues);
      this.form.markAllAsTouched();
    }
  }

  ngOnDestroy() {
    this.destroy$.next();
    this.destroy$.complete();
  }

  get isAllTouched() {
    return Object.keys(this.form.controls).every((key) => this.getControl(key).touched);
  }

  get isButtonDisabled() {
    return (this.form.invalid && this.isSubmitted()) || (this.form.invalid && this.isAllTouched);
  }

  getControl(name: keyof TFormValues) {
    return this.form.controls[name as string] as FormControl;
  }

  submitForm() {
    this.isSubmitted.set(true);

    if (this.form.invalid) {
      return;
    }

    const values = this.form.value;
    const createSubmitObservable = this.createSubmitObservableFn();
    const observable = createSubmitObservable?.(values);

    if (observable) {
      this.isLoading.set(true);

      observable
        .pipe(
          takeUntil(this.destroy$),
          finalize(() => this.isLoading.set(false)),
        )
        .subscribe(() => this.dialogRef?.close());
    }
  }
}
