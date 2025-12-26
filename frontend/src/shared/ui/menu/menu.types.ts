import { IOption } from '@shared/lib/utility-types/base-ui.types';

export interface IIconMenuOption<TName extends string = string> extends IOption<TName> {
  icon?: string;
  click?: (name?: TName) => void;
}
