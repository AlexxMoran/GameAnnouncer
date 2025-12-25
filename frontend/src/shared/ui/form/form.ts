import { Component, inject, input, OnInit, output, signal } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, ReactiveFormsModule } from '@angular/forms';
import { TranslatePipe } from '@ngx-translate/core';
import { TObjectAny } from '@shared/lib/utility-types/object.types';
import { Button } from '@shared/ui/button/button';
import { TFormField, TGroupControls } from '@shared/ui/form/form.types';
import { InputField } from '@shared/ui/input-field/input-field';
import { SelectField } from '@shared/ui/select-field/select-field';

@Component({
  selector: 'app-form',
  imports: [Button, TranslatePipe, ReactiveFormsModule, SelectField, InputField],
  templateUrl: './form.html',
  host: { class: 'w-full' },
})
export class Form<TValues extends TObjectAny> implements OnInit {
  private formBuilder = inject(FormBuilder);

  readonly controls = input.required<TGroupControls<TValues>>();
  readonly formFieldList = input.required<TFormField<TValues>[]>();
  readonly initialValues = input<TValues>();
  readonly buttonText = input('');
  readonly isLoading = input(false);

  readonly submitted = output<TValues>();

  readonly isSubmitted = signal(false);

  form!: FormGroup;

  ngOnInit() {
    this.form = this.formBuilder.group(this.controls());

    const initialValues = this.initialValues();

    if (initialValues) {
      this.form.patchValue(initialValues);
      this.form.markAllAsTouched();
    }
  }

  get isAllTouched() {
    return Object.keys(this.form.controls).every((key) => this.getControl(key).touched);
  }

  get isButtonDisabled() {
    return (this.form.invalid && this.isSubmitted()) || (this.form.invalid && this.isAllTouched);
  }

  getControl(name: keyof TValues) {
    return this.form.controls[name as string] as FormControl;
  }

  submitForm() {
    this.isSubmitted.set(true);

    if (this.form.invalid) {
      return;
    }

    const values = this.form.value;

    this.submitted.emit(values);
  }
}
