import { Type } from '@angular/core';
import { TExtractInputs, TExtractOutputs } from '@shared/lib/utility-types/extract-component.types';

export interface IOpenDialogOptions<TComponent> {
  title: string;
  inputs?: TExtractInputs<TComponent>;
  outputs?: TExtractOutputs<TComponent>;
}

export interface IDialogData<TComponent> {
  component: Type<TComponent>;
  options: IOpenDialogOptions<TComponent>;
}
