export interface IIconMenuOption<TName extends string = string> {
  name: TName;
  label: string;
  icon?: string;
  click?: (name?: TName) => void;
}
