import { FormControl, ValidatorFn } from '@angular/forms';
import { TObjectAny } from '@shared/lib/utility-types/object.types';
import { TInputType } from '@shared/ui/input-field/input-field.types';
import { ISelectFieldOption } from '@shared/ui/select-field/select-field.types';

export type TFormField<TValues extends TObjectAny> = IInputField<TValues> | ISelectField<TValues>;

export interface IInputField<TValues extends TObjectAny> {
  type: 'input';
  name: keyof TValues;
  label?: string;
  isTextarea?: boolean;
  inputType?: TInputType;
}

export interface ISelectField<TValues extends TObjectAny> {
  type: 'select';
  name: keyof TValues;
  optionList: ISelectFieldOption[];
  label?: string;
  multiple?: boolean;
}

export type TGroupControls<TValues extends TObjectAny> = {
  [K in keyof TValues]: (TValues[K] | ValidatorFn[])[] | FormControl<K>;
};
