import { FormControl, ValidatorFn } from '@angular/forms';
import { TMaybe } from '@shared/lib/utility-types/additional.types';
import { TObjectAny } from '@shared/lib/utility-types/object.types';
import { TInputType } from '@shared/ui/input-field/input-field.types';
import { ISelectFieldOption } from '@shared/ui/select-field/select-field.types';
import { Observable } from 'rxjs';

export type TFormField<TFormValues extends TObjectAny> =
  | IInputField<TFormValues>
  | ISelectField<TFormValues>;

export interface IInputField<TFormValues extends TObjectAny> {
  type: 'input';
  name: keyof TFormValues;
  label?: string;
  isTextarea?: boolean;
  inputType?: TInputType;
}

export interface ISelectField<TFormValues extends TObjectAny> {
  type: 'select';
  name: keyof TFormValues;
  optionList: ISelectFieldOption[];
  label?: string;
  multiple?: boolean;
}

export type TGroupControls<TFormValues extends TObjectAny> = {
  [K in keyof TFormValues]:
    | (TFormValues[K] | ValidatorFn[])[]
    | FormControl<TMaybe<TFormValues[K]>>;
};

export type TCreateSubmitObservable<TFormValues extends TObjectAny> = (
  values: TFormValues,
) => Observable<unknown>;
